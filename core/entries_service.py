"""M3 — Saisie des entrées de timesheet (tâches et livrables).

Chaque entrée fige à la saisie :
  * `taux_applique` — le TJM de l'expert pour l'unité choisie ;
  * `heures_par_jour_snap` — la conversion jours → heures (option C), et
    seulement si l'unité est le jour.

Modifier ensuite le TJM (M2) ou `heures_par_jour` ne retouche donc jamais une
entrée existante.

Verrouillage : une entrée rattachée à une facture **émise** n'est plus ni
modifiable ni supprimable. Rattachée à un **brouillon**, elle le reste — le
brouillon est alors recalculé.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from core.audit import journaliser
from core.db import get_config
from core.enums import StatutFacture, TypeActivite, Unite
from core.integrity import arrondi_money, jours_consommes_entry
from core.models import Allocation, Deliverable, Entry, Invoice, Project, User


@dataclass
class Totaux:
    """Totaux de bas de liste (M3 §3.3)."""

    nb_entrees: int = 0
    heures: Decimal = Decimal("0")
    jours: Decimal = Decimal("0")
    montant_facturable: Decimal = Decimal("0")
    montant_non_facturable: Decimal = Decimal("0")

    @property
    def montant_total(self) -> Decimal:
        return self.montant_facturable + self.montant_non_facturable


def _vers_decimal(valeur: Any) -> Decimal | None:
    if valeur is None or valeur == "":
        return None
    try:
        return Decimal(str(valeur))
    except (InvalidOperation, ValueError):
        return None


# --------------------------------------------------------------------------- #
# Verrouillage
# --------------------------------------------------------------------------- #
def entree_verrouillee(session: Session, entry: Entry) -> str | None:
    """Raison du verrouillage d'une entrée, ou `None` si elle est modifiable."""
    if entry.invoice_id is None:
        return None
    facture = session.get(Invoice, entry.invoice_id)
    if facture is None:
        return None
    if StatutFacture(facture.statut) is StatutFacture.BROUILLON:
        return None
    reference = facture.numero or f"#{facture.id}"
    return (
        f"Entrée rattachée à la facture {reference} ({facture.statut}) : "
        "détachez-la d'abord de la facture."
    )


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
def valider_entree(
    session: Session,
    user_id: int,
    project_id: int,
    unite: Unite | str,
    quantite: Any,
    deliverable_id: int | None = None,
) -> tuple[list[str], Decimal | None]:
    """Valide une saisie et renvoie `(erreurs, taux_applique)`."""
    erreurs: list[str] = []

    qte = _vers_decimal(quantite)
    if qte is None:
        erreurs.append("La quantité doit être numérique.")
    elif qte <= 0:
        erreurs.append("La quantité doit être strictement positive.")

    user = session.get(User, user_id)
    if user is None:
        return ["Expert inconnu."], None
    if not user.actif:
        erreurs.append("Ce compte est désactivé.")

    projet = session.get(Project, project_id)
    if projet is None:
        erreurs.append("Projet inconnu.")
    else:
        alloue = session.scalars(
            select(Allocation).where(
                Allocation.user_id == user_id, Allocation.project_id == project_id
            )
        ).first()
        if alloue is None:
            erreurs.append(
                f"Le projet « {projet.nom} » n'est pas alloué à {user.nom} "
                "(allocation à créer par l'admin)."
            )

    if deliverable_id is not None:
        livrable = session.get(Deliverable, deliverable_id)
        if livrable is None:
            erreurs.append("Livrable inconnu.")
        elif livrable.project_id != project_id:
            erreurs.append("Le livrable choisi n'appartient pas au projet sélectionné.")

    unite_val = Unite(unite)
    taux = user.tjm_pour(unite_val)
    if taux is None or Decimal(taux) <= 0:
        libelle = "tjm_jour" if unite_val is Unite.JOUR else "tjm_heure"
        erreurs.append(
            f"Le {libelle} de {user.nom} n'est pas défini : "
            "définir le TJM de l'expert (admin)."
        )
        taux = None

    return erreurs, Decimal(taux) if taux is not None else None


# --------------------------------------------------------------------------- #
# Création / édition / suppression
# --------------------------------------------------------------------------- #
def creer_entree(
    session: Session,
    auteur_id: int | None,
    user_id: int,
    project_id: int,
    date_entry: date,
    unite: Unite | str,
    quantite: Any,
    type_activite: TypeActivite | str,
    deliverable_id: int | None = None,
    note_livrable: str | None = None,
    facturable: bool = True,
) -> tuple[Entry | None, list[str]]:
    """Crée une entrée en figeant TJM et conversion heures/jour."""
    erreurs, taux = valider_entree(
        session, user_id, project_id, unite, quantite, deliverable_id
    )
    if erreurs or taux is None:
        return None, erreurs

    unite_val = Unite(unite)
    qte = Decimal(str(quantite))
    hpj_snap = (
        Decimal(get_config(session).heures_par_jour) if unite_val is Unite.JOUR else None
    )

    entry = Entry(
        user_id=user_id,
        project_id=project_id,
        deliverable_id=deliverable_id,
        date_entry=date_entry,
        unite=unite_val,
        quantite=qte,
        taux_applique=taux,
        montant=arrondi_money(qte * taux),
        heures_par_jour_snap=hpj_snap,
        note_livrable=(note_livrable or "").strip() or None,
        type_activite=TypeActivite(type_activite),
        facturable=bool(facturable),
    )
    session.add(entry)
    session.flush()
    journaliser(
        session, auteur_id, "entry_create", "entries", entry.id,
        {
            "user_id": user_id,
            "project_id": project_id,
            "date_entry": date_entry,
            "unite": str(unite_val),
            "quantite": qte,
            "taux_applique": taux,
            "montant": entry.montant,
            "pour_le_compte_de": user_id if auteur_id != user_id else None,
        },
    )
    return entry, []


def modifier_entree(
    session: Session,
    auteur_id: int | None,
    entry_id: int,
    reappliquer_tjm: bool = False,
    **champs: Any,
) -> tuple[Entry | None, list[str]]:
    """Modifie une entrée non verrouillée.

    Le `taux_applique` reste le snapshot d'origine sauf `reappliquer_tjm=True`,
    qui le réaligne explicitement sur le TJM courant de l'expert.
    """
    entry = session.get(Entry, entry_id)
    if entry is None:
        return None, ["Entrée inconnue."]
    verrou = entree_verrouillee(session, entry)
    if verrou:
        return None, [verrou]

    fusion = {
        "project_id": champs.get("project_id", entry.project_id),
        "unite": champs.get("unite", entry.unite),
        "quantite": champs.get("quantite", entry.quantite),
        "deliverable_id": champs.get("deliverable_id", entry.deliverable_id),
    }
    erreurs, taux_courant = valider_entree(session, entry.user_id, **fusion)
    if erreurs:
        return None, erreurs

    ancien_unite = Unite(entry.unite)
    nouvelle_unite = Unite(fusion["unite"])
    modifies: dict[str, Any] = {}

    for cle in (
        "project_id", "deliverable_id", "date_entry", "note_livrable",
        "type_activite", "facturable",
    ):
        if cle not in champs:
            continue
        valeur = champs[cle]
        if cle == "note_livrable":
            valeur = (valeur or "").strip() or None
        elif cle == "type_activite":
            valeur = TypeActivite(valeur)
        elif cle == "facturable":
            valeur = bool(valeur)
        if getattr(entry, cle) != valeur:
            modifies[cle] = valeur
            setattr(entry, cle, valeur)

    if nouvelle_unite is not ancien_unite:
        modifies["unite"] = str(nouvelle_unite)
        entry.unite = nouvelle_unite
        # Changer d'unité invalide le snapshot de taux : celui de l'ancienne
        # unité ne veut plus rien dire, on reprend le TJM courant.
        reappliquer_tjm = True
        entry.heures_par_jour_snap = (
            Decimal(get_config(session).heures_par_jour)
            if nouvelle_unite is Unite.JOUR
            else None
        )
        modifies["heures_par_jour_snap"] = entry.heures_par_jour_snap

    nouvelle_qte = Decimal(str(fusion["quantite"]))
    if Decimal(entry.quantite) != nouvelle_qte:
        modifies["quantite"] = nouvelle_qte
        entry.quantite = nouvelle_qte

    if reappliquer_tjm and taux_courant is not None and Decimal(entry.taux_applique) != taux_courant:
        modifies["taux_applique"] = taux_courant
        entry.taux_applique = taux_courant

    nouveau_montant = arrondi_money(Decimal(entry.quantite) * Decimal(entry.taux_applique))
    if arrondi_money(entry.montant) != nouveau_montant:
        modifies["montant"] = nouveau_montant
        entry.montant = nouveau_montant

    if modifies:
        session.flush()
        journaliser(session, auteur_id, "entry_update", "entries", entry_id, modifies)
        if entry.invoice_id is not None:
            from core.invoice_service import recalculer_brouillon

            recalculer_brouillon(session, entry.invoice_id)
    return entry, []


def supprimer_entree(session: Session, auteur_id: int | None, entry_id: int) -> list[str]:
    entry = session.get(Entry, entry_id)
    if entry is None:
        return ["Entrée inconnue."]
    verrou = entree_verrouillee(session, entry)
    if verrou:
        return [verrou]
    invoice_id = entry.invoice_id
    journaliser(
        session, auteur_id, "entry_delete", "entries", entry_id,
        {
            "user_id": entry.user_id,
            "project_id": entry.project_id,
            "date_entry": entry.date_entry,
            "montant": entry.montant,
        },
    )
    session.delete(entry)
    session.flush()
    if invoice_id is not None:
        from core.invoice_service import recalculer_brouillon

        recalculer_brouillon(session, invoice_id)
    return []


def dupliquer_entree(
    session: Session, auteur_id: int | None, entry_id: int, nouvelle_date: date | None = None
) -> tuple[Entry | None, list[str]]:
    """Saisie rapide : duplique une entrée, avec les TJM et config du jour."""
    source = session.get(Entry, entry_id)
    if source is None:
        return None, ["Entrée inconnue."]
    return creer_entree(
        session,
        auteur_id,
        user_id=source.user_id,
        project_id=source.project_id,
        date_entry=nouvelle_date or source.date_entry,
        unite=source.unite,
        quantite=source.quantite,
        type_activite=source.type_activite,
        deliverable_id=source.deliverable_id,
        note_livrable=source.note_livrable,
        facturable=source.facturable,
    )


# --------------------------------------------------------------------------- #
# Lecture
# --------------------------------------------------------------------------- #
def lister_entrees(
    session: Session,
    user_id: int | None = None,
    annee: int | None = None,
    mois: int | None = None,
    project_id: int | None = None,
    facturable: bool | None = None,
    non_facturees: bool = False,
    debut: date | None = None,
    fin: date | None = None,
) -> list[Entry]:
    """Entrées filtrées, triées par date puis par identifiant.

    `user_id` est le garde-fou du cloisonnement : les appelants passent
    `auth.perimetre_user_id()` pour un expert, et un expert choisi pour les
    rôles transversaux.
    """
    requete = (
        select(Entry)
        .options(selectinload(Entry.project), selectinload(Entry.deliverable))
        .order_by(Entry.date_entry, Entry.id)
    )
    if user_id is not None:
        requete = requete.where(Entry.user_id == user_id)
    if annee is not None:
        requete = requete.where(func.extract("year", Entry.date_entry) == annee)
    if mois is not None:
        requete = requete.where(func.extract("month", Entry.date_entry) == mois)
    if project_id is not None:
        requete = requete.where(Entry.project_id == project_id)
    if facturable is not None:
        requete = requete.where(Entry.facturable.is_(facturable))
    if non_facturees:
        requete = requete.where(Entry.invoice_id.is_(None))
    if debut is not None:
        requete = requete.where(Entry.date_entry >= debut)
    if fin is not None:
        requete = requete.where(Entry.date_entry <= fin)
    return list(session.scalars(requete))


def calculer_totaux(session: Session, entrees: Iterable[Entry]) -> Totaux:
    """Totaux heures / jours / montants sur un ensemble d'entrées."""
    hpj = Decimal(get_config(session).heures_par_jour)
    totaux = Totaux()
    for entry in entrees:
        totaux.nb_entrees += 1
        totaux.heures += entry.heures_timesheet
        totaux.jours += jours_consommes_entry(entry, hpj)
        if entry.facturable:
            totaux.montant_facturable += Decimal(entry.montant)
        else:
            totaux.montant_non_facturable += Decimal(entry.montant)
    totaux.heures = totaux.heures.quantize(Decimal("0.01"))
    totaux.jours = totaux.jours.quantize(Decimal("0.01"))
    return totaux


def apercu_entree(
    session: Session, unite: Unite | str, quantite: Any, taux: Decimal | None
) -> dict[str, Decimal | None]:
    """Aperçu avant validation : montant USD et heures timesheet équivalentes."""
    qte = _vers_decimal(quantite)
    if qte is None or qte <= 0 or taux is None:
        return {"montant": None, "heures_timesheet": None}
    unite_val = Unite(unite)
    hpj = Decimal(get_config(session).heures_par_jour)
    heures = qte if unite_val is Unite.HEURE else qte * hpj
    return {
        "montant": arrondi_money(qte * Decimal(taux)),
        "heures_timesheet": heures.quantize(Decimal("0.01")),
    }
