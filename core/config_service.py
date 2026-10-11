"""M2 — Services de configuration : paramètres, projets, allocations, livrables.

Règle structurante : **rien ici ne recalcule les données passées.** Changer
`heures_par_jour` ou un TJM n'affecte que les saisies futures, puisque chaque
entrée porte ses propres snapshots (`taux_applique`, `heures_par_jour_snap`).
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.audit import journaliser
from core.db import get_config
from core.enums import StatutLivrable, StatutProjet
from core.models import Allocation, Config, Deliverable, Entry, Project, User


def _vers_decimal(valeur: Any, defaut: Decimal | None = None) -> Decimal | None:
    if valeur is None or valeur == "":
        return defaut
    try:
        return Decimal(str(valeur))
    except (InvalidOperation, ValueError):
        return None


# --------------------------------------------------------------------------- #
# 2.1 Paramètres généraux
# --------------------------------------------------------------------------- #
def valider_parametres(
    heures_par_jour: Any, seuil_alerte_pct: Any, seuil_critique_pct: Any
) -> list[str]:
    """Contrôle les paramètres généraux sans rien écrire."""
    erreurs: list[str] = []
    hpj = _vers_decimal(heures_par_jour)
    if hpj is None:
        erreurs.append("heures_par_jour : valeur numérique attendue.")
    elif hpj <= 0:
        erreurs.append("heures_par_jour doit être strictement positif.")
    elif hpj > 24:
        erreurs.append("heures_par_jour ne peut pas dépasser 24.")
    try:
        alerte, critique = int(seuil_alerte_pct), int(seuil_critique_pct)
    except (TypeError, ValueError):
        erreurs.append("Les seuils doivent être des entiers.")
        return erreurs
    if not 0 < alerte < critique <= 100:
        erreurs.append(
            "Les seuils doivent vérifier 0 < alerte < critique ≤ 100 "
            f"(reçu alerte={alerte}, critique={critique})."
        )
    return erreurs


def maj_parametres(
    session: Session, auteur_id: int | None, **champs: Any
) -> tuple[Config | None, list[str]]:
    """Met à jour `config` (ligne id=1). `devise` reste USD en v1."""
    config = get_config(session)
    propose = {
        "heures_par_jour": champs.get("heures_par_jour", config.heures_par_jour),
        "seuil_alerte_pct": champs.get("seuil_alerte_pct", config.seuil_alerte_pct),
        "seuil_critique_pct": champs.get("seuil_critique_pct", config.seuil_critique_pct),
    }
    erreurs = valider_parametres(**propose)
    prefixe = str(champs.get("prefixe_facture", config.prefixe_facture) or "").strip()
    if not prefixe:
        erreurs.append("Le préfixe de facture est obligatoire.")
    elif not all(c.isalnum() or c in "-_" for c in prefixe):
        erreurs.append("Le préfixe de facture n'accepte que lettres, chiffres, - et _.")
    if erreurs:
        return None, erreurs

    modifies: dict[str, Any] = {}
    valeurs = {
        "heures_par_jour": _vers_decimal(propose["heures_par_jour"]),
        "seuil_alerte_pct": int(propose["seuil_alerte_pct"]),
        "seuil_critique_pct": int(propose["seuil_critique_pct"]),
        "prefixe_facture": prefixe,
        "bill_to_nom": str(champs.get("bill_to_nom", config.bill_to_nom) or "").strip(),
        "bill_to_ville": str(champs.get("bill_to_ville", config.bill_to_ville) or "").strip(),
        "bill_to_email": str(champs.get("bill_to_email", config.bill_to_email) or "").strip(),
    }
    for cle, valeur in valeurs.items():
        if getattr(config, cle) != valeur:
            modifies[cle] = valeur
            setattr(config, cle, valeur)
    if modifies:
        session.flush()
        journaliser(session, auteur_id, "config_update", "config", 1, modifies)
    return config, []


# --------------------------------------------------------------------------- #
# 2.2 TJM & société par expert
# --------------------------------------------------------------------------- #
def valider_tjm(tjm_jour: Any, tjm_heure: Any) -> list[str]:
    erreurs: list[str] = []
    for libelle, valeur in (("tjm_jour", tjm_jour), ("tjm_heure", tjm_heure)):
        if valeur in (None, ""):
            continue
        montant = _vers_decimal(valeur)
        if montant is None:
            erreurs.append(f"{libelle} : valeur numérique attendue.")
        elif montant < 0:
            erreurs.append(f"{libelle} ne peut pas être négatif.")
    return erreurs


# --------------------------------------------------------------------------- #
# 2.3 Projets
# --------------------------------------------------------------------------- #
def valider_projet(
    nom: Any, budget_jours: Any, date_debut: date | None, date_fin: date | None
) -> list[str]:
    erreurs: list[str] = []
    if not str(nom or "").strip():
        erreurs.append("Le nom du projet est obligatoire.")
    budget = _vers_decimal(budget_jours, Decimal("0"))
    if budget is None:
        erreurs.append("budget_jours : valeur numérique attendue.")
    elif budget < 0:
        erreurs.append("budget_jours ne peut pas être négatif.")
    if date_debut and date_fin and date_fin < date_debut:
        erreurs.append("La date de fin doit être postérieure à la date de début.")
    return erreurs


def creer_projet(
    session: Session, auteur_id: int | None, **champs: Any
) -> tuple[Project | None, list[str]]:
    erreurs = valider_projet(
        champs.get("nom"),
        champs.get("budget_jours"),
        champs.get("date_debut"),
        champs.get("date_fin"),
    )
    if erreurs:
        return None, erreurs
    projet = Project(
        nom=str(champs["nom"]).strip(),
        numero=(str(champs.get("numero") or "").strip() or None),
        client=str(champs.get("client") or "Tangerine Central, LLC").strip(),
        budget_jours=_vers_decimal(champs.get("budget_jours"), Decimal("0")),
        statut=StatutProjet(champs.get("statut", StatutProjet.ACTIF)),
        date_debut=champs.get("date_debut"),
        date_fin=champs.get("date_fin"),
    )
    session.add(projet)
    session.flush()
    journaliser(
        session, auteur_id, "project_create", "projects", projet.id,
        {"nom": projet.nom, "numero": projet.numero},
    )
    return projet, []


def modifier_projet(
    session: Session, auteur_id: int | None, project_id: int, **champs: Any
) -> tuple[Project | None, list[str]]:
    projet = session.get(Project, project_id)
    if projet is None:
        return None, ["Projet inconnu."]
    fusion = {
        "nom": champs.get("nom", projet.nom),
        "budget_jours": champs.get("budget_jours", projet.budget_jours),
        "date_debut": champs.get("date_debut", projet.date_debut),
        "date_fin": champs.get("date_fin", projet.date_fin),
    }
    erreurs = valider_projet(**fusion)
    if erreurs:
        return None, erreurs

    nouveau_statut = champs.get("statut")
    if nouveau_statut is not None and StatutProjet(nouveau_statut) is StatutProjet.CLOS:
        avertissement = avertissement_cloture(session, project_id)
        if avertissement and not champs.get("forcer_cloture"):
            return None, [avertissement]

    modifies: dict[str, Any] = {}
    for cle in ("nom", "numero", "client", "budget_jours", "statut", "date_debut", "date_fin"):
        if cle not in champs:
            continue
        valeur = champs[cle]
        if cle in {"nom", "client"}:
            valeur = str(valeur or "").strip()
        elif cle == "numero":
            valeur = str(valeur or "").strip() or None
        elif cle == "budget_jours":
            valeur = _vers_decimal(valeur, Decimal("0"))
        elif cle == "statut":
            valeur = StatutProjet(valeur)
        if getattr(projet, cle) != valeur:
            modifies[cle] = valeur
            setattr(projet, cle, valeur)
    if modifies:
        session.flush()
        journaliser(session, auteur_id, "project_update", "projects", project_id, modifies)
    return projet, []


def avertissement_cloture(session: Session, project_id: int) -> str | None:
    """Message si le projet porte des entrées facturables non encore facturées."""
    nb = session.scalar(
        select(func.count())
        .select_from(Entry)
        .where(
            Entry.project_id == project_id,
            Entry.facturable.is_(True),
            Entry.invoice_id.is_(None),
        )
    )
    if nb:
        return (
            f"{nb} entrée(s) facturable(s) de ce projet ne sont pas encore facturées. "
            "Facturez-les ou cochez « clôturer malgré tout »."
        )
    return None


def projet_supprimable(session: Session, project_id: int) -> bool:
    """Un projet portant des entrées n'est jamais supprimé : il passe `clos`."""
    nb = session.scalar(
        select(func.count()).select_from(Entry).where(Entry.project_id == project_id)
    )
    return not nb


# --------------------------------------------------------------------------- #
# 2.3 Allocations
# --------------------------------------------------------------------------- #
def definir_allocation(
    session: Session, auteur_id: int | None, user_id: int, project_id: int, jours_alloues: Any
) -> tuple[Allocation | None, list[str]]:
    """Crée ou met à jour l'allocation d'un couple (expert, projet)."""
    jours = _vers_decimal(jours_alloues, Decimal("0"))
    if jours is None:
        return None, ["jours_alloues : valeur numérique attendue."]
    if jours < 0:
        return None, ["jours_alloues ne peut pas être négatif."]
    if session.get(User, user_id) is None:
        return None, ["Expert inconnu."]
    if session.get(Project, project_id) is None:
        return None, ["Projet inconnu."]

    allocation = session.scalars(
        select(Allocation).where(
            Allocation.user_id == user_id, Allocation.project_id == project_id
        )
    ).first()
    if allocation is None:
        allocation = Allocation(user_id=user_id, project_id=project_id, jours_alloues=jours)
        session.add(allocation)
        session.flush()
        action = "allocation_create"
    else:
        allocation.jours_alloues = jours
        session.flush()
        action = "allocation_update"
    journaliser(
        session, auteur_id, action, "allocations", allocation.id,
        {"user_id": user_id, "project_id": project_id, "jours_alloues": jours},
    )
    return allocation, []


def supprimer_allocation(
    session: Session, auteur_id: int | None, allocation_id: int
) -> list[str]:
    allocation = session.get(Allocation, allocation_id)
    if allocation is None:
        return ["Allocation inconnue."]
    nb = session.scalar(
        select(func.count())
        .select_from(Entry)
        .where(Entry.user_id == allocation.user_id, Entry.project_id == allocation.project_id)
    )
    if nb:
        return [
            f"{nb} entrée(s) existent pour ce couple : mettez l'allocation à 0 "
            "plutôt que de la supprimer."
        ]
    journaliser(
        session, auteur_id, "allocation_delete", "allocations", allocation_id,
        {"user_id": allocation.user_id, "project_id": allocation.project_id},
    )
    session.delete(allocation)
    return []


def projets_alloues(session: Session, user_id: int, actifs_seulement: bool = True) -> list[Project]:
    """Projets sur lesquels l'expert est alloué — base de la saisie (M3)."""
    requete = (
        select(Project)
        .join(Allocation, Allocation.project_id == Project.id)
        .where(Allocation.user_id == user_id)
        .order_by(Project.nom)
    )
    if actifs_seulement:
        requete = requete.where(Project.statut == StatutProjet.ACTIF)
    return list(session.scalars(requete))


# --------------------------------------------------------------------------- #
# 2.3 Livrables
# --------------------------------------------------------------------------- #
def creer_livrable(
    session: Session,
    auteur_id: int | None,
    project_id: int,
    intitule: str,
    statut: StatutLivrable | str = StatutLivrable.A_FAIRE,
    echeance: date | None = None,
) -> tuple[Deliverable | None, list[str]]:
    if session.get(Project, project_id) is None:
        return None, ["Projet inconnu."]
    if not str(intitule or "").strip():
        return None, ["L'intitulé du livrable est obligatoire."]
    livrable = Deliverable(
        project_id=project_id,
        intitule=str(intitule).strip(),
        statut=StatutLivrable(statut),
        echeance=echeance,
    )
    session.add(livrable)
    session.flush()
    journaliser(
        session, auteur_id, "deliverable_create", "deliverables", livrable.id,
        {"project_id": project_id, "intitule": livrable.intitule},
    )
    return livrable, []


def modifier_livrable(
    session: Session, auteur_id: int | None, deliverable_id: int, **champs: Any
) -> tuple[Deliverable | None, list[str]]:
    livrable = session.get(Deliverable, deliverable_id)
    if livrable is None:
        return None, ["Livrable inconnu."]
    modifies: dict[str, Any] = {}
    for cle in ("intitule", "statut", "echeance"):
        if cle not in champs:
            continue
        valeur = champs[cle]
        if cle == "intitule":
            valeur = str(valeur or "").strip()
            if not valeur:
                return None, ["L'intitulé du livrable est obligatoire."]
        elif cle == "statut":
            valeur = StatutLivrable(valeur)
        if getattr(livrable, cle) != valeur:
            modifies[cle] = valeur
            setattr(livrable, cle, valeur)
    if modifies:
        session.flush()
        journaliser(
            session, auteur_id, "deliverable_update", "deliverables", deliverable_id, modifies
        )
    return livrable, []


def supprimer_livrable(
    session: Session, auteur_id: int | None, deliverable_id: int
) -> list[str]:
    livrable = session.get(Deliverable, deliverable_id)
    if livrable is None:
        return ["Livrable inconnu."]
    nb = session.scalar(
        select(func.count()).select_from(Entry).where(Entry.deliverable_id == deliverable_id)
    )
    if nb:
        return [f"{nb} entrée(s) référencent ce livrable : il ne peut pas être supprimé."]
    journaliser(session, auteur_id, "deliverable_delete", "deliverables", deliverable_id)
    session.delete(livrable)
    return []


def livrables_projet(session: Session, project_id: int) -> list[Deliverable]:
    return list(
        session.scalars(
            select(Deliverable)
            .where(Deliverable.project_id == project_id)
            .order_by(Deliverable.echeance.is_(None), Deliverable.echeance, Deliverable.intitule)
        )
    )
