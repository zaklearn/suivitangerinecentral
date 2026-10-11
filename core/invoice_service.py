"""M5 — Cycle de vie des factures : brouillon, émission, paiement.

Trois états :

* **brouillon** — l'expert choisit une période et des entrées facturables non
  encore facturées. Les entrées retenues portent déjà `invoice_id` : c'est ce
  qui permet d'« annuler le brouillon pour libérer les entrées », et c'est
  pourquoi une entrée rattachée à un brouillon reste modifiable (M3).
* **émise** — transaction atomique : numéro attribué, lignes LABOR recopiées
  dans `invoice_labor`, totaux arrêtés. La facture devient immuable et ses
  entrées sont verrouillées.
* **payée** — marquage manuel.

Les lignes ODC vivent dans `invoice_odc` dès le brouillon (elles n'ont pas
d'autre support) ; elles se figent elles aussi à l'émission.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.audit import journaliser
from core.db import get_config
from core.enums import ModeNumerotation, StatutFacture
from core.integrity import arrondi_money
from core.models import Entry, Invoice, InvoiceLabor, InvoiceOdc, Project, User

DELAI_PAIEMENT_JOURS = 30
MAX_TENTATIVES_NUMERO = 5


def _vers_decimal(valeur: Any, defaut: Decimal | None = None) -> Decimal | None:
    if valeur is None or valeur == "":
        return defaut
    try:
        return Decimal(str(valeur))
    except (InvalidOperation, ValueError):
        return None


# --------------------------------------------------------------------------- #
# Numérotation (M2 §2.4 / M5 §5.4)
# --------------------------------------------------------------------------- #
def code_facture_defaut(nom: str) -> str:
    """Initiales d'un expert, majuscules, 2 à 4 lettres : « Jane Doe » → « JD »."""
    initiales = "".join(mot[0] for mot in re.findall(r"[^\W\d_]+", nom or "", re.UNICODE))
    code = initiales.upper()[:4]
    return code or "XX"


def assurer_code_facture(session: Session, user: User) -> str:
    """Garantit un `code_facture` unique à l'expert, dérivé de son nom."""
    if user.code_facture:
        return user.code_facture
    base = code_facture_defaut(user.nom)
    candidat, suffixe = base, 1
    while session.scalars(
        select(User).where(User.code_facture == candidat, User.id != user.id)
    ).first():
        suffixe += 1
        candidat = f"{base}{suffixe}"[:8]
    user.code_facture = candidat
    session.flush()
    return candidat


def prochain_numero(session: Session, user_id: int, annee: int) -> str:
    """Numéro suivant, selon le mode de numérotation configuré.

    `par_expert` produit `{prefixe}-{code}-{AAAA}-{seq:03d}` : le code expert
    est ce qui rend une séquence par expert compatible avec l'unicité globale
    de `invoices.numero`.
    """
    config = get_config(session)
    prefixe = config.prefixe_facture.strip()
    mode = ModeNumerotation(config.mode_numerotation)

    if mode is ModeNumerotation.PAR_EXPERT:
        user = session.get(User, user_id)
        if user is None:
            raise ValueError(f"expert inconnu : {user_id}")
        code = assurer_code_facture(session, user)
        racine = f"{prefixe}-{code}-{annee:04d}-"
    else:
        racine = f"{prefixe}-{annee:04d}-"

    motif = re.compile(rf"^{re.escape(racine)}(\d+)$")
    sequence_max = 0
    for (numero,) in session.execute(
        select(Invoice.numero).where(Invoice.numero.like(f"{racine}%"))
    ):
        correspondance = motif.match(numero or "")
        if correspondance:
            sequence_max = max(sequence_max, int(correspondance.group(1)))
    return f"{racine}{sequence_max + 1:03d}"


# --------------------------------------------------------------------------- #
# Brouillon
# --------------------------------------------------------------------------- #
def entrees_facturables(
    session: Session,
    user_id: int,
    debut: date | None = None,
    fin: date | None = None,
    project_ids: list[int] | None = None,
) -> list[Entry]:
    """Entrées éligibles : facturables, non encore rattachées à une facture."""
    requete = (
        select(Entry)
        .where(
            Entry.user_id == user_id,
            Entry.facturable.is_(True),
            Entry.invoice_id.is_(None),
        )
        .order_by(Entry.date_entry, Entry.id)
    )
    if debut is not None:
        requete = requete.where(Entry.date_entry >= debut)
    if fin is not None:
        requete = requete.where(Entry.date_entry <= fin)
    if project_ids:
        requete = requete.where(Entry.project_id.in_(project_ids))
    return list(session.scalars(requete))


def creer_brouillon(
    session: Session,
    auteur_id: int | None,
    user_id: int,
    periode_debut: date | None = None,
    periode_fin: date | None = None,
    entry_ids: list[int] | None = None,
    avance: Any = 0,
) -> tuple[Invoice | None, list[str]]:
    """Ouvre un brouillon de facture pour un expert."""
    if session.get(User, user_id) is None:
        return None, ["Expert inconnu."]
    if periode_debut and periode_fin and periode_fin < periode_debut:
        return None, ["La fin de période doit être postérieure à son début."]
    montant_avance = _vers_decimal(avance, Decimal("0"))
    if montant_avance is None or montant_avance < 0:
        return None, ["L'avance doit être un montant positif ou nul."]

    facture = Invoice(
        user_id=user_id,
        statut=StatutFacture.BROUILLON,
        periode_debut=periode_debut,
        periode_fin=periode_fin,
        avance=arrondi_money(montant_avance),
    )
    session.add(facture)
    session.flush()
    journaliser(
        session, auteur_id, "invoice_draft_create", "invoices", facture.id,
        {"user_id": user_id, "periode_debut": periode_debut, "periode_fin": periode_fin},
    )
    if entry_ids:
        erreurs = attacher_entrees(session, auteur_id, facture.id, entry_ids)
        if erreurs:
            return None, erreurs
    recalculer_brouillon(session, facture.id)
    return facture, []


def attacher_entrees(
    session: Session, auteur_id: int | None, invoice_id: int, entry_ids: list[int]
) -> list[str]:
    """Rattache des entrées à un brouillon."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return ["Facture déjà émise : elle n'est plus modifiable."]

    for entry_id in entry_ids:
        entry = session.get(Entry, entry_id)
        if entry is None:
            return [f"Entrée {entry_id} inconnue."]
        if entry.user_id != facture.user_id:
            return [f"L'entrée {entry_id} appartient à un autre expert."]
        if not entry.facturable:
            return [f"L'entrée {entry_id} est marquée non facturable."]
        if entry.invoice_id not in (None, invoice_id):
            return [f"L'entrée {entry_id} est déjà rattachée à une autre facture."]
        entry.invoice_id = invoice_id
    session.flush()
    journaliser(
        session, auteur_id, "invoice_entries_attach", "invoices", invoice_id,
        {"entry_ids": entry_ids},
    )
    recalculer_brouillon(session, invoice_id)
    return []


def detacher_entrees(
    session: Session, auteur_id: int | None, invoice_id: int, entry_ids: list[int]
) -> list[str]:
    """Détache des entrées d'un brouillon (elles redeviennent facturables)."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return ["Facture déjà émise : les entrées ne peuvent plus être détachées."]
    for entry_id in entry_ids:
        entry = session.get(Entry, entry_id)
        if entry is not None and entry.invoice_id == invoice_id:
            entry.invoice_id = None
    session.flush()
    journaliser(
        session, auteur_id, "invoice_entries_detach", "invoices", invoice_id,
        {"entry_ids": entry_ids},
    )
    recalculer_brouillon(session, invoice_id)
    return []


def definir_avance(
    session: Session, auteur_id: int | None, invoice_id: int, avance: Any
) -> list[str]:
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return ["Facture déjà émise : l'avance n'est plus modifiable."]
    montant = _vers_decimal(avance, Decimal("0"))
    if montant is None or montant < 0:
        return ["L'avance doit être un montant positif ou nul."]
    facture.avance = arrondi_money(montant)
    session.flush()
    recalculer_brouillon(session, invoice_id)
    journaliser(
        session, auteur_id, "invoice_advance", "invoices", invoice_id, {"avance": montant}
    )
    return []


# --------------------------------------------------------------------------- #
# ODC
# --------------------------------------------------------------------------- #
def ajouter_odc(
    session: Session,
    auteur_id: int | None,
    invoice_id: int,
    projet: str,
    odc: str,
    units: Any,
    unit_cost: Any,
) -> tuple[InvoiceOdc | None, list[str]]:
    """Ajoute une ligne de coût direct. `montant = units × unit_cost`."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return None, ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return None, ["Facture déjà émise : les ODC ne sont plus modifiables."]
    nb_units = _vers_decimal(units)
    cout = _vers_decimal(unit_cost)
    erreurs: list[str] = []
    if not str(projet or "").strip():
        erreurs.append("Le projet de la ligne ODC est obligatoire.")
    if not str(odc or "").strip():
        erreurs.append("Le libellé ODC est obligatoire.")
    if nb_units is None or nb_units <= 0:
        erreurs.append("Les unités doivent être strictement positives.")
    if cout is None or cout < 0:
        erreurs.append("Le coût unitaire ne peut pas être négatif.")
    if erreurs:
        return None, erreurs

    item = 1 + max((l.item for l in facture.odc_lines), default=0)
    ligne = InvoiceOdc(
        item=item,
        projet=str(projet).strip(),
        odc=str(odc).strip(),
        units=nb_units,
        unit_cost=cout,
        montant=arrondi_money(nb_units * cout),
    )
    # Append sur la relation : la collection chargée reste synchronisée, sans
    # quoi deux ODC ajoutées dans la même session porteraient le même item.
    facture.odc_lines.append(ligne)
    session.flush()
    journaliser(
        session, auteur_id, "invoice_odc_add", "invoice_odc", ligne.id,
        {"invoice_id": invoice_id, "odc": ligne.odc, "montant": ligne.montant},
    )
    recalculer_brouillon(session, invoice_id)
    return ligne, []


def supprimer_odc(session: Session, auteur_id: int | None, odc_id: int) -> list[str]:
    ligne = session.get(InvoiceOdc, odc_id)
    if ligne is None:
        return ["Ligne ODC inconnue."]
    facture = session.get(Invoice, ligne.invoice_id)
    if facture is None or StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return ["Facture déjà émise : les ODC ne sont plus modifiables."]
    invoice_id = ligne.invoice_id
    journaliser(session, auteur_id, "invoice_odc_delete", "invoice_odc", odc_id)
    session.delete(ligne)
    session.flush()
    # Renumérotation des items pour rester 1..n sans trou.
    for position, restante in enumerate(
        sorted(facture.odc_lines, key=lambda o: o.item), start=1
    ):
        restante.item = position
    session.flush()
    recalculer_brouillon(session, invoice_id)
    return []


# --------------------------------------------------------------------------- #
# Totaux
# --------------------------------------------------------------------------- #
def lignes_labor_brouillon(session: Session, invoice_id: int) -> list[dict]:
    """Lignes LABOR d'un brouillon : **une ligne par entrée**, triée par date.

    Aucun regroupement : la colonne « Hours » du modèle reçoit la quantité
    telle qu'elle a été saisie — heures ou jours — et `Rate/Hour` le taux
    correspondant. Aucune conversion n'intervient dans la facturation.
    """
    entrees = list(
        session.scalars(
            select(Entry).where(Entry.invoice_id == invoice_id).order_by(Entry.date_entry, Entry.id)
        )
    )
    lignes: list[dict] = []
    for item, entree in enumerate(entrees, start=1):
        projet = session.get(Project, entree.project_id)
        libelle = None
        if entree.deliverable_id is not None and entree.deliverable is not None:
            libelle = entree.deliverable.intitule
        lignes.append(
            {
                "item": item,
                "entry_id": entree.id,
                "date_entry": entree.date_entry,
                "projet": projet.nom if projet else "",
                "deliverable_output": libelle or entree.note_livrable,
                "quantite": Decimal(entree.quantite),
                "unite": str(entree.unite),
                "taux": Decimal(entree.taux_applique),
                "montant": arrondi_money(Decimal(entree.quantite) * Decimal(entree.taux_applique)),
            }
        )
    return lignes


def recalculer_brouillon(session: Session, invoice_id: int) -> Invoice | None:
    """Recalcule les totaux d'un brouillon. Sans effet sur une facture émise."""
    facture = session.get(Invoice, invoice_id)
    if facture is None or StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return facture
    labor = sum((l["montant"] for l in lignes_labor_brouillon(session, invoice_id)), Decimal("0"))
    odc = sum((Decimal(o.montant) for o in facture.odc_lines), Decimal("0"))
    facture.sous_total_labor = arrondi_money(labor)
    facture.sous_total_odc = arrondi_money(odc)
    facture.total_net = arrondi_money(labor + odc - Decimal(facture.avance))
    session.flush()
    return facture


# --------------------------------------------------------------------------- #
# Émission / paiement / annulation
# --------------------------------------------------------------------------- #
def emettre(
    session: Session,
    auteur_id: int | None,
    invoice_id: int,
    date_emission: date | None = None,
    date_echeance: date | None = None,
) -> tuple[Invoice | None, list[str]]:
    """Émet la facture : numéro, gel des lignes, totaux arrêtés, immuabilité."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return None, ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return None, [f"Facture déjà {facture.statut} : elle ne peut pas être réémise."]

    lignes = lignes_labor_brouillon(session, invoice_id)
    if not lignes and not facture.odc_lines:
        return None, ["Facture vide : rattachez au moins une entrée ou une ligne ODC."]

    emission = date_emission or date.today()
    echeance = date_echeance or emission + timedelta(days=DELAI_PAIEMENT_JOURS)
    if echeance < emission:
        return None, ["L'échéance doit être postérieure à la date d'émission."]

    sous_total_labor = arrondi_money(sum((l["montant"] for l in lignes), Decimal("0")))
    sous_total_odc = arrondi_money(
        sum((Decimal(o.montant) for o in facture.odc_lines), Decimal("0"))
    )
    avance = arrondi_money(Decimal(facture.avance))
    if avance > sous_total_labor + sous_total_odc:
        return None, [
            f"L'avance ({avance}) dépasse le total de la facture "
            f"({sous_total_labor + sous_total_odc})."
        ]

    # Gel des lignes LABOR : on recopie, on ne référence pas.
    facture.labor_lines.clear()
    session.flush()
    for ligne in lignes:
        # Append sur la relation, pas session.add : la collection chargée reste
        # ainsi synchronisée pour la génération du classeur qui suit.
        facture.labor_lines.append(
            InvoiceLabor(
                item=ligne["item"],
                projet=ligne["projet"],
                deliverable_output=ligne["deliverable_output"],
                quantite=ligne["quantite"],
                taux=ligne["taux"],
                montant=ligne["montant"],
            )
        )
    session.flush()

    facture.date_emission = emission
    facture.date_echeance = echeance
    facture.sous_total_labor = sous_total_labor
    facture.sous_total_odc = sous_total_odc
    facture.total_net = arrondi_money(sous_total_labor + sous_total_odc - avance)
    facture.statut = StatutFacture.EMISE

    derniere_erreur: Exception | None = None
    for _ in range(MAX_TENTATIVES_NUMERO):
        numero = prochain_numero(session, facture.user_id, emission.year)
        facture.numero = numero
        try:
            session.flush()
            break
        except IntegrityError as exc:
            # Course entre deux émissions simultanées : on reprend un numéro.
            derniere_erreur = exc
            session.rollback()
            facture = session.get(Invoice, invoice_id)
            if facture is None:
                return None, ["Facture introuvable après conflit de numérotation."]
    else:
        return None, [
            "Impossible d'attribuer un numéro de facture unique après plusieurs "
            f"tentatives ({derniere_erreur})."
        ]

    journaliser(
        session, auteur_id, "invoice_issue", "invoices", invoice_id,
        {
            "numero": facture.numero,
            "date_emission": emission,
            "sous_total_labor": sous_total_labor,
            "sous_total_odc": sous_total_odc,
            "avance": avance,
            "total_net": facture.total_net,
            "nb_lignes_labor": len(lignes),
        },
    )
    return facture, []


def marquer_payee(
    session: Session,
    auteur_id: int | None,
    invoice_id: int,
    date_paiement: date | None = None,
    note: str | None = None,
) -> tuple[Invoice | None, list[str]]:
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return None, ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.EMISE:
        return None, [f"Seule une facture émise peut être marquée payée (statut : {facture.statut})."]
    paiement = date_paiement or date.today()
    facture.statut = StatutFacture.PAYEE
    mention = f"Payée le {paiement.isoformat()}"
    if note:
        mention += f" — {note.strip()}"
    facture.note = f"{facture.note}\n{mention}" if facture.note else mention
    session.flush()
    journaliser(
        session, auteur_id, "invoice_paid", "invoices", invoice_id,
        {"date_paiement": paiement, "total_net": facture.total_net},
    )
    return facture, []


def annuler_brouillon(session: Session, auteur_id: int | None, invoice_id: int) -> list[str]:
    """Supprime un brouillon et libère ses entrées."""
    facture = session.get(Invoice, invoice_id)
    if facture is None:
        return ["Facture inconnue."]
    if StatutFacture(facture.statut) is not StatutFacture.BROUILLON:
        return ["Seul un brouillon peut être annulé."]
    for entry in session.scalars(select(Entry).where(Entry.invoice_id == invoice_id)):
        entry.invoice_id = None
    journaliser(
        session, auteur_id, "invoice_draft_cancel", "invoices", invoice_id,
        {"user_id": facture.user_id},
    )
    session.delete(facture)
    session.flush()
    return []


def lister_factures(
    session: Session,
    user_id: int | None = None,
    statut: StatutFacture | str | None = None,
) -> list[Invoice]:
    requete = select(Invoice).order_by(
        Invoice.date_emission.is_(None).desc(), Invoice.date_emission.desc(), Invoice.id.desc()
    )
    if user_id is not None:
        requete = requete.where(Invoice.user_id == user_id)
    if statut is not None:
        requete = requete.where(Invoice.statut == StatutFacture(statut))
    return list(session.scalars(requete))
