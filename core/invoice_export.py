"""M5 — Génération de la facture au format du modèle d'origine (+ PDF).

Le classeur produit est `templates/invoice_template.xlsx` rempli : titre,
en-têtes, couleurs, tableau Excel, bloc signature et mentions sont ceux du
modèle, inchangés.

Trois corrections sont appliquées au modèle, parce qu'il contient des formules
héritées fausses qui rendraient la facture arithmétiquement incorrecte :

1. `G27:G29` (Amount ODC) porte dans le modèle une formule qui référence
   `InvoiceDetails[[#This Row],[Hours]]`, hors du tableau LABOR : elle renvoie
   une cellule vide. Remplacée par `=E{r}*F{r}` (signalée au §5.5 du cahier
   des charges).
2. `G30` (sous-total ODC) somme `InvoiceDetails[Amount]`, c'est-à-dire la
   colonne du tableau **LABOR** : le sous-total ODC valait donc le sous-total
   LABOR, et `Total = G24+G30` comptait le labor deux fois. Remplacée par une
   somme de la plage ODC réelle.
3. La colonne `Hours` / `Units` est formatée `0` dans le modèle : une quantité
   de 7,5 s'affichait « 8 » en regard d'un montant calculé sur 7,5. Format
   porté à `#,##0.##`, qui affiche les entiers comme des entiers.

Hors ces trois points, aucune cellule du modèle n'est restylée.
"""
from __future__ import annotations

import re
from decimal import Decimal
from io import BytesIO

from sqlalchemy.orm import Session

from core.db import get_config
from core.enums import StatutFacture
from core.invoice_service import lignes_labor_brouillon
from core.models import Invoice, User
from core.xlsx_utils import charger_modele, inserer_lignes, vers_bytes, vider_cellules

MODELE = "invoice_template.xlsx"
NOM_TABLE = "InvoiceDetails"

# Cartographie du modèle `Invoice`.
CELLULES_SOCIETE = {
    "G2": "societe_nom",
    "G3": "societe_adresse",
    "G4": "societe_ville_zip",
    "G5": "societe_phone",
    "G6": "societe_email",
}
CELL_BILL_TO_NOM, CELL_BILL_TO_VILLE, CELL_BILL_TO_EMAIL = "G10", "G11", "G12"
CELL_NUMERO, CELL_DATE_EMISSION, CELL_DATE_ECHEANCE = "C10", "C11", "C12"

LABOR_PREMIERE, LABOR_DERNIERE, LABOR_SOUS_TOTAL = 16, 23, 24
ODC_PREMIERE, ODC_DERNIERE, ODC_SOUS_TOTAL = 27, 29, 30
LIGNE_TOTAL, LIGNE_AVANCE, LIGNE_TOTAL_NET = 31, 32, 33

COL_ITEM, COL_PROJET, COL_LIBELLE, COL_QTE, COL_TAUX, COL_MONTANT = 2, 3, 4, 5, 6, 7

CAPACITE_LABOR = LABOR_DERNIERE - LABOR_PREMIERE + 1  # 8 lignes
CAPACITE_ODC = ODC_DERNIERE - ODC_PREMIERE + 1  # 3 lignes

# Formule Amount du modèle, à référence structurée : conservée telle quelle et
# recopiée sur les lignes ajoutées en cas de débordement.
FORMULE_AMOUNT_LABOR = (
    '=IF(ISBLANK(InvoiceDetails[[#This Row],[Hours]]),"",'
    '(IFERROR(InvoiceDetails[[#This Row],[Hours]]*'
    'InvoiceDetails[[#This Row],[Rate/Hour]],"")))'
)
FORMAT_QUANTITE = "#,##0.##"


def nom_fichier_facture(numero: str | None, invoice_id: int, extension: str = "xlsx") -> str:
    """`Invoice_{numero}.xlsx`, ou un repli lisible pour un brouillon."""
    base = numero or f"brouillon-{invoice_id}"
    propre = re.sub(r"[^\w\-.]+", "_", base).strip("_") or f"facture-{invoice_id}"
    return f"Invoice_{propre}.{extension}"


def _lignes_labor(session: Session, facture: Invoice) -> list[dict]:
    """Lignes LABOR : les snapshots figés si la facture est émise, sinon le
    calcul courant du brouillon."""
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return [
            {
                "item": ligne.item,
                "projet": ligne.projet,
                "deliverable_output": ligne.deliverable_output,
                "quantite": Decimal(ligne.quantite),
                "taux": Decimal(ligne.taux),
                "montant": Decimal(ligne.montant),
            }
            for ligne in sorted(facture.labor_lines, key=lambda l: l.item)
        ]
    return lignes_labor_brouillon(session, facture.id)


def generer_facture(session: Session, invoice_id: int) -> tuple[BytesIO, str]:
    """Produit le classeur de la facture et son nom de fichier."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        raise ValueError(f"facture inconnue : {invoice_id}")
    expert = session.get(User, facture.user_id)
    if expert is None:
        raise ValueError(f"expert inconnu : {facture.user_id}")
    config = get_config(session)

    lignes_labor = _lignes_labor(session, facture)
    lignes_odc = sorted(facture.odc_lines, key=lambda o: o.item)

    workbook = charger_modele(MODELE)
    ws = workbook.active

    # --- En-têtes -------------------------------------------------------- #
    for cellule, champ in CELLULES_SOCIETE.items():
        ws[cellule] = getattr(expert, champ) or None
    ws[CELL_BILL_TO_NOM] = config.bill_to_nom
    ws[CELL_BILL_TO_VILLE] = config.bill_to_ville
    ws[CELL_BILL_TO_EMAIL] = config.bill_to_email
    ws[CELL_NUMERO] = facture.numero or "BROUILLON — non émise"
    ws[CELL_DATE_EMISSION] = facture.date_emission
    ws[CELL_DATE_ECHEANCE] = facture.date_echeance

    # --- Débordement ----------------------------------------------------- #
    # LABOR d'abord : l'insertion décale tout ce qui suit, ODC compris.
    extra_labor = max(0, len(lignes_labor) - CAPACITE_LABOR)
    if extra_labor:
        inserer_lignes(
            ws,
            index=LABOR_SOUS_TOTAL,
            nb_lignes=extra_labor,
            ligne_modele=LABOR_DERNIERE,
            nom_table=NOM_TABLE,
        )
    odc_premiere = ODC_PREMIERE + extra_labor
    odc_derniere = ODC_DERNIERE + extra_labor

    extra_odc = max(0, len(lignes_odc) - CAPACITE_ODC)
    if extra_odc:
        inserer_lignes(
            ws,
            index=ODC_SOUS_TOTAL + extra_labor,
            nb_lignes=extra_odc,
            ligne_modele=odc_derniere,
        )
        odc_derniere += extra_odc

    labor_derniere = LABOR_DERNIERE + extra_labor
    labor_sous_total = LABOR_SOUS_TOTAL + extra_labor
    decalage_total = extra_labor + extra_odc
    odc_sous_total = ODC_SOUS_TOTAL + decalage_total
    ligne_total = LIGNE_TOTAL + decalage_total
    ligne_avance = LIGNE_AVANCE + decalage_total
    ligne_total_net = LIGNE_TOTAL_NET + decalage_total

    # --- LABOR ----------------------------------------------------------- #
    for decalage, ligne in enumerate(lignes_labor):
        r = LABOR_PREMIERE + decalage
        ws.cell(row=r, column=COL_ITEM).value = ligne["item"]
        ws.cell(row=r, column=COL_PROJET).value = ligne["projet"]
        ws.cell(row=r, column=COL_LIBELLE).value = ligne["deliverable_output"]
        cellule_qte = ws.cell(row=r, column=COL_QTE)
        cellule_qte.value = float(ligne["quantite"])
        cellule_qte.number_format = FORMAT_QUANTITE
        ws.cell(row=r, column=COL_TAUX).value = float(ligne["taux"])
        # Amount : la formule du modèle, conservée (et recopiée si débordement).
        ws.cell(row=r, column=COL_MONTANT).value = FORMULE_AMOUNT_LABOR

    for r in range(LABOR_PREMIERE + len(lignes_labor), labor_derniere + 1):
        vider_cellules(ws, r, (COL_ITEM, COL_PROJET, COL_LIBELLE, COL_QTE, COL_TAUX))
        # La formule du modèle renvoie "" tant que Hours est vide : on la garde.
        ws.cell(row=r, column=COL_MONTANT).value = FORMULE_AMOUNT_LABOR

    # --- ODC ------------------------------------------------------------- #
    for decalage, ligne in enumerate(lignes_odc):
        r = odc_premiere + decalage
        ws.cell(row=r, column=COL_ITEM).value = ligne.item
        ws.cell(row=r, column=COL_PROJET).value = ligne.projet
        ws.cell(row=r, column=COL_LIBELLE).value = ligne.odc
        cellule_units = ws.cell(row=r, column=COL_QTE)
        cellule_units.value = float(ligne.units)
        cellule_units.number_format = FORMAT_QUANTITE
        ws.cell(row=r, column=COL_TAUX).value = float(ligne.unit_cost)
        # Correction 1 : montant ODC = units x unit cost.
        ws.cell(row=r, column=COL_MONTANT).value = f"=E{r}*F{r}"

    for r in range(odc_premiere + len(lignes_odc), odc_derniere + 1):
        vider_cellules(
            ws, r, (COL_ITEM, COL_PROJET, COL_LIBELLE, COL_QTE, COL_TAUX, COL_MONTANT)
        )

    # --- Sous-totaux et totaux ------------------------------------------- #
    # Correction 2 : le sous-total ODC somme la plage ODC, pas le tableau LABOR.
    ws.cell(row=odc_sous_total, column=COL_MONTANT).value = (
        f"=SUM(G{odc_premiere}:G{odc_derniere})"
    )
    # Totaux : formules du modèle, réécrites avec les lignes effectives.
    ws.cell(row=ligne_total, column=COL_MONTANT).value = (
        f"=G{labor_sous_total}+G{odc_sous_total}"
    )
    ws.cell(row=ligne_avance, column=COL_MONTANT).value = float(Decimal(facture.avance))
    ws.cell(row=ligne_total_net, column=COL_MONTANT).value = (
        f"=G{ligne_total}-G{ligne_avance}"
    )

    return vers_bytes(workbook), nom_fichier_facture(facture.numero, facture.id)


def totaux_attendus(session: Session, invoice_id: int) -> dict[str, Decimal]:
    """Totaux attendus côté Python — contrôle de ce que calcule Excel."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        raise ValueError(f"facture inconnue : {invoice_id}")
    labor = sum((l["montant"] for l in _lignes_labor(session, facture)), Decimal("0"))
    odc = sum((Decimal(o.montant) for o in facture.odc_lines), Decimal("0"))
    avance = Decimal(facture.avance)
    return {
        "sous_total_labor": labor,
        "sous_total_odc": odc,
        "total": labor + odc,
        "avance": avance,
        "total_net": labor + odc - avance,
    }
