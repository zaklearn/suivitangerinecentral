"""M7 — Agrégations pour le dashboard.

Tout est agrégé **en SQL** : aucune boucle Python sur le volume d'entrées.
La conversion jours ↔ heures suit l'option C :

* heures affichées  = `quantite` si l'unité est l'heure, sinon
  `quantite × heures_par_jour_snap` (le snapshot de l'entrée) ;
* jours consommés   = `quantite` si l'unité est le jour, sinon
  `quantite / heures_par_jour` (valeur courante de la config, puisqu'une
  entrée en heures ne porte pas de snapshot).
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import Select, case, func, select
from sqlalchemy.orm import Session

from core.db import heures_par_jour as _heures_par_jour_courant
from core.enums import StatutFacture, StatutLivrable, StatutProjet, Unite
from core.models import Deliverable, Entry, Invoice, Project, User

CENT = Decimal("0.01")


def _expr_heures():
    """Expression SQL des heures timesheet d'une entrée (option C)."""
    return case(
        (Entry.unite == Unite.HEURE, Entry.quantite),
        else_=Entry.quantite * func.coalesce(Entry.heures_par_jour_snap, 0),
    )


def _expr_jours(heures_par_jour: Decimal):
    """Expression SQL des jours consommés d'une entrée (option C)."""
    return case(
        (Entry.unite == Unite.JOUR, Entry.quantite),
        else_=Entry.quantite / float(heures_par_jour),
    )


def _filtrer_entrees(
    requete: Select,
    user_id: int | None = None,
    project_id: int | None = None,
    debut: date | None = None,
    fin: date | None = None,
) -> Select:
    if user_id is not None:
        requete = requete.where(Entry.user_id == user_id)
    if project_id is not None:
        requete = requete.where(Entry.project_id == project_id)
    if debut is not None:
        requete = requete.where(Entry.date_entry >= debut)
    if fin is not None:
        requete = requete.where(Entry.date_entry <= fin)
    return requete


def _dec(valeur: Any) -> Decimal:
    if valeur is None:
        return Decimal("0")
    return Decimal(str(valeur)).quantize(CENT)


# --------------------------------------------------------------------------- #
# 7.2 KPIs
# --------------------------------------------------------------------------- #
def kpis_taches(
    session: Session,
    user_id: int | None = None,
    project_id: int | None = None,
    debut: date | None = None,
    fin: date | None = None,
) -> dict[str, Decimal | int]:
    """Nombre d'entrées, heures et jours équivalents sur la période."""
    hpj = _heures_par_jour_courant(session)
    requete = _filtrer_entrees(
        select(
            func.count(Entry.id),
            func.sum(_expr_heures()),
            func.sum(_expr_jours(hpj)),
            func.sum(case((Entry.facturable.is_(True), Entry.montant), else_=0)),
            func.sum(case((Entry.facturable.is_(False), Entry.montant), else_=0)),
        ),
        user_id,
        project_id,
        debut,
        fin,
    )
    nb, heures, jours, facturable, non_facturable = session.execute(requete).one()
    return {
        "nb_entrees": int(nb or 0),
        "heures": _dec(heures),
        "jours": _dec(jours),
        "montant_facturable": _dec(facturable),
        "montant_non_facturable": _dec(non_facturable),
    }


def kpis_factures(
    session: Session,
    user_id: int | None = None,
    debut: date | None = None,
    fin: date | None = None,
) -> dict[str, Any]:
    """Nombre et montants de factures par statut.

    « en attente » = factures émises non encore payées.
    """
    requete = select(
        Invoice.statut, func.count(Invoice.id), func.sum(Invoice.total_net)
    ).group_by(Invoice.statut)
    if user_id is not None:
        requete = requete.where(Invoice.user_id == user_id)
    if debut is not None:
        requete = requete.where(Invoice.date_emission >= debut)
    if fin is not None:
        requete = requete.where(Invoice.date_emission <= fin)

    par_statut = {
        str(statut): {"nb": int(nb or 0), "montant": _dec(montant)}
        for statut, nb, montant in session.execute(requete)
    }
    for statut in StatutFacture:
        par_statut.setdefault(str(statut), {"nb": 0, "montant": Decimal("0")})

    emise = par_statut[str(StatutFacture.EMISE)]
    payee = par_statut[str(StatutFacture.PAYEE)]
    return {
        "par_statut": par_statut,
        "montant_facture": emise["montant"] + payee["montant"],
        "montant_paye": payee["montant"],
        "montant_en_attente": emise["montant"],
        "nb_total": sum(v["nb"] for v in par_statut.values()),
    }


def kpis_projets(session: Session, user_id: int | None = None) -> dict[str, int]:
    """Projets actifs et avancement des livrables."""
    requete_projets = select(func.count(Project.id)).where(
        Project.statut == StatutProjet.ACTIF
    )
    requete_livrables = select(
        func.count(Deliverable.id),
        func.sum(case((Deliverable.statut == StatutLivrable.LIVRE, 1), else_=0)),
    )
    if user_id is not None:
        # Périmètre d'un expert : les projets sur lesquels il a des entrées.
        projets_expert = (
            select(Entry.project_id).where(Entry.user_id == user_id).distinct().scalar_subquery()
        )
        requete_projets = requete_projets.where(Project.id.in_(projets_expert))
        requete_livrables = requete_livrables.where(Deliverable.project_id.in_(projets_expert))

    nb_actifs = session.scalar(requete_projets) or 0
    nb_livrables, nb_livres = session.execute(requete_livrables).one()
    return {
        "nb_projets_actifs": int(nb_actifs),
        "nb_livrables": int(nb_livrables or 0),
        "nb_livrables_livres": int(nb_livres or 0),
    }


# --------------------------------------------------------------------------- #
# 7.3 Graphes
# --------------------------------------------------------------------------- #
def avancement_par_projet(
    session: Session, user_id: int | None = None, project_id: int | None = None
) -> list[dict]:
    """Jours consommés par projet, face au budget du projet."""
    hpj = _heures_par_jour_courant(session)
    requete = (
        select(
            Project.id,
            Project.nom,
            Project.budget_jours,
            func.sum(_expr_jours(hpj)),
            func.count(Entry.id),
        )
        .join(Entry, Entry.project_id == Project.id, isouter=True)
        .group_by(Project.id, Project.nom, Project.budget_jours)
        .order_by(Project.nom)
    )
    if user_id is not None:
        requete = requete.where(Entry.user_id == user_id)
    if project_id is not None:
        requete = requete.where(Project.id == project_id)

    lignes = []
    for pid, nom, budget, consommes, nb in session.execute(requete):
        budget_dec = _dec(budget)
        consommes_dec = _dec(consommes)
        lignes.append(
            {
                "project_id": pid,
                "projet": nom,
                "budget_jours": budget_dec,
                "jours_consommes": consommes_dec,
                "jours_restants": budget_dec - consommes_dec,
                "pct": (
                    (consommes_dec / budget_dec * 100).quantize(CENT)
                    if budget_dec > 0
                    else (Decimal("100") if consommes_dec > 0 else Decimal("0"))
                ),
                "nb_entrees": int(nb or 0),
            }
        )
    return lignes


def facture_par_mois(session: Session, user_id: int | None = None) -> list[dict]:
    """Montants émis et payés par mois d'émission."""
    requete = (
        select(
            func.extract("year", Invoice.date_emission),
            func.extract("month", Invoice.date_emission),
            func.sum(Invoice.total_net),
            func.sum(case((Invoice.statut == StatutFacture.PAYEE, Invoice.total_net), else_=0)),
        )
        .where(Invoice.date_emission.is_not(None))
        .group_by(
            func.extract("year", Invoice.date_emission),
            func.extract("month", Invoice.date_emission),
        )
        .order_by(
            func.extract("year", Invoice.date_emission),
            func.extract("month", Invoice.date_emission),
        )
    )
    if user_id is not None:
        requete = requete.where(Invoice.user_id == user_id)
    return [
        {
            "annee": int(annee),
            "mois": int(mois),
            "periode": f"{int(annee):04d}-{int(mois):02d}",
            "montant_emis": _dec(emis),
            "montant_paye": _dec(paye),
        }
        for annee, mois, emis, paye in session.execute(requete)
    ]


def repartition_heures(
    session: Session,
    axe: str = "type_activite",
    user_id: int | None = None,
    debut: date | None = None,
    fin: date | None = None,
) -> list[dict]:
    """Répartition des heures par type d'activité, par projet ou par expert."""
    colonnes = {
        "type_activite": (Entry.type_activite, None),
        "projet": (Project.nom, Project),
        "expert": (User.nom, User),
    }
    if axe not in colonnes:
        raise ValueError(f"axe inconnu : {axe!r} (attendu : {', '.join(colonnes)})")
    colonne, jointure = colonnes[axe]

    hpj = _heures_par_jour_courant(session)
    requete = select(colonne, func.sum(_expr_heures()), func.sum(_expr_jours(hpj)))
    if jointure is Project:
        requete = requete.join(Project, Entry.project_id == Project.id)
    elif jointure is User:
        requete = requete.join(User, Entry.user_id == User.id)
    requete = _filtrer_entrees(requete, user_id, None, debut, fin)
    requete = requete.group_by(colonne).order_by(colonne)

    return [
        {"libelle": str(libelle), "heures": _dec(heures), "jours": _dec(jours)}
        for libelle, heures, jours in session.execute(requete)
    ]


def timeline_livrables(session: Session, user_id: int | None = None) -> list[dict]:
    """Livrables, leurs échéances et leurs statuts."""
    requete = (
        select(
            Deliverable.id,
            Deliverable.intitule,
            Deliverable.statut,
            Deliverable.echeance,
            Project.nom,
        )
        .join(Project, Deliverable.project_id == Project.id)
        .order_by(Deliverable.echeance.is_(None), Deliverable.echeance, Project.nom)
    )
    if user_id is not None:
        projets_expert = (
            select(Entry.project_id).where(Entry.user_id == user_id).distinct().scalar_subquery()
        )
        requete = requete.where(Deliverable.project_id.in_(projets_expert))
    return [
        {
            "deliverable_id": did,
            "intitule": intitule,
            "statut": str(statut),
            "echeance": echeance,
            "projet": projet,
        }
        for did, intitule, statut, echeance, projet in session.execute(requete)
    ]


def consommation_par_expert(session: Session, project_id: int | None = None) -> list[dict]:
    """Jours consommés par expert, face à la somme de ses allocations."""
    from core.models import Allocation

    hpj = _heures_par_jour_courant(session)
    requete_conso = select(Entry.user_id, func.sum(_expr_jours(hpj))).group_by(Entry.user_id)
    requete_alloc = select(Allocation.user_id, func.sum(Allocation.jours_alloues)).group_by(
        Allocation.user_id
    )
    if project_id is not None:
        requete_conso = requete_conso.where(Entry.project_id == project_id)
        requete_alloc = requete_alloc.where(Allocation.project_id == project_id)

    consommation = {uid: _dec(jours) for uid, jours in session.execute(requete_conso)}
    allocations = {uid: _dec(jours) for uid, jours in session.execute(requete_alloc)}
    noms = {u.id: u.nom for u in session.scalars(select(User))}

    lignes = []
    for uid in sorted(set(consommation) | set(allocations)):
        alloues = allocations.get(uid, Decimal("0"))
        consommes = consommation.get(uid, Decimal("0"))
        lignes.append(
            {
                "user_id": uid,
                "expert": noms.get(uid, f"#{uid}"),
                "jours_alloues": alloues,
                "jours_consommes": consommes,
                "jours_restants": alloues - consommes,
                "pct": (
                    (consommes / alloues * 100).quantize(CENT)
                    if alloues > 0
                    else (Decimal("100") if consommes > 0 else Decimal("0"))
                ),
            }
        )
    return sorted(lignes, key=lambda l: l["pct"], reverse=True)
