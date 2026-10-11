"""M4 — Génération du timesheet mensuel au format du modèle d'origine.

Le classeur produit est le fichier-modèle `templates/timesheet_template.xlsx`
rempli : en-tête, instructions, en-têtes de colonnes, bloc de certification et
signatures sont ceux du modèle, inchangés. Seules sont écrites les valeurs de
`B3`, `B4` et des lignes de données.

La colonne « Number of Hours » reçoit `heures_timesheet`, c'est-à-dire la
quantité en heures telle quelle, ou la quantité en jours convertie par le
**snapshot** `heures_par_jour_snap` de l'entrée (option C) — jamais par la
valeur courante de la configuration.
"""
from __future__ import annotations

import re
from datetime import date
from decimal import Decimal
from io import BytesIO

from sqlalchemy.orm import Session

from core.entries_service import lister_entrees
from core.models import User
from core.xlsx_utils import charger_modele, inserer_lignes, vers_bytes, vider_cellules

MODELE = "timesheet_template.xlsx"
NOM_TABLE = "Table224567893"

# Cartographie du modèle — toute modification de ces constantes change le rendu.
CELL_NOM = "B3"
CELL_MOIS = "B4"
LIGNE_PREMIERE_DONNEE = 9
LIGNE_DERNIERE_DONNEE = 39
LIGNE_TOTAL = 40
COL_DATE, COL_PROJET, COL_NUMERO, COL_HEURES, COL_NOTE = 1, 2, 3, 4, 5

CAPACITE_MODELE = LIGNE_DERNIERE_DONNEE - LIGNE_PREMIERE_DONNEE + 1  # 31 lignes

# Le modèle laisse la colonne Date au format « General » : une date y
# apparaîtrait comme un numéro de série. On pose donc un format de date, en
# cohérence avec le format mm-dd-yy du modèle de facture (client US).
FORMAT_DATE = "mm/dd/yyyy"

MOIS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def libelle_mois(annee: int, mois: int) -> str:
    """« October 2026 » — indépendant de la locale du serveur."""
    if not 1 <= mois <= 12:
        raise ValueError(f"mois invalide : {mois}")
    return f"{MOIS_EN[mois - 1]} {annee}"


def nom_fichier_timesheet(nom_expert: str, annee: int, mois: int, extension: str = "xlsx") -> str:
    """`Timesheet_{nom}_{AAAA-MM}.xlsx`, nettoyé pour un système de fichiers."""
    propre = re.sub(r"[^\w\-]+", "_", nom_expert.strip()).strip("_") or "expert"
    return f"Timesheet_{propre}_{annee:04d}-{mois:02d}.{extension}"


def generer_timesheet(session: Session, user_id: int, annee: int, mois: int) -> tuple[BytesIO, str]:
    """Produit le timesheet d'un expert pour un mois.

    Toute l'activité du mois est reportée — federal, non-federal, admin et
    business development, facturable ou non : le modèle est un *effort record*,
    pas un relevé de facturation.
    """
    expert = session.get(User, user_id)
    if expert is None:
        raise ValueError(f"expert inconnu : {user_id}")

    entrees = lister_entrees(session, user_id=user_id, annee=annee, mois=mois)

    workbook = charger_modele(MODELE)
    ws = workbook.active

    mois_libelle = libelle_mois(annee, mois)
    ws[CELL_NOM] = expert.nom
    ws[CELL_MOIS] = mois_libelle
    ws.title = mois_libelle

    # Débordement : on insère juste avant la ligne TOTAL, en recopiant
    # l'habillage de la dernière ligne de données du modèle.
    lignes_a_inserer = max(0, len(entrees) - CAPACITE_MODELE)
    if lignes_a_inserer:
        inserer_lignes(
            ws,
            index=LIGNE_TOTAL,
            nb_lignes=lignes_a_inserer,
            ligne_modele=LIGNE_DERNIERE_DONNEE,
            nom_table=NOM_TABLE,
        )

    derniere_ligne_donnee = LIGNE_DERNIERE_DONNEE + lignes_a_inserer
    ligne_total = LIGNE_TOTAL + lignes_a_inserer

    for decalage, entree in enumerate(entrees):
        ligne = LIGNE_PREMIERE_DONNEE + decalage
        cellule_date = ws.cell(row=ligne, column=COL_DATE)
        cellule_date.value = entree.date_entry
        cellule_date.number_format = FORMAT_DATE
        ws.cell(row=ligne, column=COL_PROJET).value = entree.project.nom
        ws.cell(row=ligne, column=COL_NUMERO).value = entree.project.numero
        ws.cell(row=ligne, column=COL_HEURES).value = float(entree.heures_timesheet)
        ws.cell(row=ligne, column=COL_NOTE).value = entree.note_livrable

    # Lignes de données non utilisées : vidées, habillage conservé.
    for ligne in range(LIGNE_PREMIERE_DONNEE + len(entrees), derniere_ligne_donnee + 1):
        vider_cellules(ws, ligne, range(COL_DATE, COL_NOTE + 1))

    # TOTAL HOURS reste une formule, étendue à la plage réelle.
    ws.cell(row=ligne_total, column=COL_HEURES).value = (
        f"=SUBTOTAL(109,D{LIGNE_PREMIERE_DONNEE}:D{derniere_ligne_donnee})"
    )

    return vers_bytes(workbook), nom_fichier_timesheet(expert.nom, annee, mois)


def total_heures_attendu(session: Session, user_id: int, annee: int, mois: int) -> Decimal:
    """Σ des heures timesheet du mois — contrôle du total calculé par Excel."""
    entrees = lister_entrees(session, user_id=user_id, annee=annee, mois=mois)
    return sum((e.heures_timesheet for e in entrees), Decimal("0")).quantize(Decimal("0.01"))


def mois_disponibles(session: Session, user_id: int) -> list[tuple[int, int]]:
    """Couples (année, mois) pour lesquels l'expert a saisi des entrées."""
    mois_vus: set[tuple[int, int]] = set()
    for entree in lister_entrees(session, user_id=user_id):
        jour: date = entree.date_entry
        mois_vus.add((jour.year, jour.month))
    return sorted(mois_vus, reverse=True)
