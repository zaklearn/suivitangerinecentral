"""M6 — Règles d'intégrité, en lecture (contrôle) ou avec réparation.

`verifier_integrite(session, reparer=False)` renvoie un rapport structuré.
Les cinq règles correspondent au §« Règles d'intégrité » du cahier des charges.
Aucune règle ne touche aux lignes figées d'une facture émise : si un écart
apparaît là, il est signalé mais jamais « réparé » — la facture est un
document émis, pas une donnée de travail.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.db import heures_par_jour as _heures_par_jour_courant
from core.db import get_config
from core.enums import StatutFacture, Unite
from core.models import Allocation, Entry, Invoice, Project, User

CENT = Decimal("0.01")


def arrondi_money(valeur: Decimal | float | int) -> Decimal:
    """Arrondi monétaire à 2 décimales (half-up, comme une facture papier)."""
    return Decimal(valeur).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class Anomalie:
    regle: str
    entite: str
    entite_id: int | None
    message: str
    reparee: bool = False


@dataclass
class ConsommationCouple:
    """Consommation d'un couple (expert, projet) — règle 5, option C."""

    user_id: int
    user_nom: str
    project_id: int
    project_nom: str
    jours_alloues: Decimal
    jours_consommes: Decimal

    @property
    def jours_restants(self) -> Decimal:
        return self.jours_alloues - self.jours_consommes

    @property
    def pct(self) -> Decimal:
        if self.jours_alloues <= 0:
            # Pas d'allocation : toute consommation est un dépassement.
            return Decimal("100") if self.jours_consommes > 0 else Decimal("0")
        return (self.jours_consommes / self.jours_alloues * Decimal("100")).quantize(CENT)

    def flags(self, seuil_alerte: int, seuil_critique: int) -> dict[str, bool]:
        pct = self.pct
        return {
            "alerte": pct >= Decimal(seuil_alerte),
            "critique": pct >= Decimal(seuil_critique),
            "epuise": self.jours_restants <= 0,
        }


@dataclass
class RapportIntegrite:
    anomalies: list[Anomalie] = field(default_factory=list)
    consommation: list[ConsommationCouple] = field(default_factory=list)
    nb_entries: int = 0
    nb_invoices: int = 0

    @property
    def ok(self) -> bool:
        return not self.anomalies

    @property
    def nb_reparees(self) -> int:
        return sum(1 for a in self.anomalies if a.reparee)

    def par_regle(self) -> dict[str, list[Anomalie]]:
        groupes: dict[str, list[Anomalie]] = {}
        for anomalie in self.anomalies:
            groupes.setdefault(anomalie.regle, []).append(anomalie)
        return groupes


def verifier_integrite(session: Session, reparer: bool = False) -> RapportIntegrite:
    """Applique les cinq règles d'intégrité et renvoie le rapport."""
    rapport = RapportIntegrite()
    _regle1_montants(session, rapport, reparer)
    _regle2_snapshot_heures(session, rapport, reparer)
    _regle3_entrees_facturees(session, rapport)
    _regle4_totaux_factures(session, rapport, reparer)
    rapport.consommation = calculer_consommation(session)
    rapport.nb_entries = session.scalar(select(func.count()).select_from(Entry)) or 0
    rapport.nb_invoices = session.scalar(select(func.count()).select_from(Invoice)) or 0
    return rapport


# --------------------------------------------------------------------------- #
# Règle 1 — montant = quantite x taux_applique
# --------------------------------------------------------------------------- #
def _regle1_montants(session: Session, rapport: RapportIntegrite, reparer: bool) -> None:
    for entry in session.scalars(select(Entry)):
        attendu = arrondi_money(Decimal(entry.quantite) * Decimal(entry.taux_applique))
        if arrondi_money(entry.montant) == attendu:
            continue
        reparable = reparer and entry.invoice_id is None
        if reparable:
            entry.montant = attendu
        rapport.anomalies.append(
            Anomalie(
                regle="1-montant",
                entite="entries",
                entite_id=entry.id,
                message=(
                    f"montant {entry.montant} ≠ {attendu} "
                    f"({entry.quantite} × {entry.taux_applique})"
                    + ("" if reparable else " — entrée facturée, non réparée")
                ),
                reparee=reparable,
            )
        )
    if reparer:
        session.flush()


# --------------------------------------------------------------------------- #
# Règle 2 — cohérence du snapshot heures/jour (option C)
# --------------------------------------------------------------------------- #
def _regle2_snapshot_heures(session: Session, rapport: RapportIntegrite, reparer: bool) -> None:
    defaut = _heures_par_jour_courant(session)
    for entry in session.scalars(select(Entry)):
        est_jour = Unite(entry.unite) is Unite.JOUR
        if est_jour and entry.heures_par_jour_snap is None:
            reparable = reparer and entry.invoice_id is None
            if reparable:
                # On ne peut pas retrouver la valeur d'origine : on applique la
                # valeur courante, en le signalant explicitement.
                entry.heures_par_jour_snap = defaut
            rapport.anomalies.append(
                Anomalie(
                    regle="2-snapshot-heures",
                    entite="entries",
                    entite_id=entry.id,
                    message=(
                        "unite=jour sans heures_par_jour_snap"
                        + (f" — rempli avec la valeur courante {defaut}" if reparable else "")
                    ),
                    reparee=reparable,
                )
            )
        elif not est_jour and entry.heures_par_jour_snap is not None:
            reparable = reparer and entry.invoice_id is None
            if reparable:
                entry.heures_par_jour_snap = None
            rapport.anomalies.append(
                Anomalie(
                    regle="2-snapshot-heures",
                    entite="entries",
                    entite_id=entry.id,
                    message="unite=heure avec heures_par_jour_snap renseigné"
                    + (" — vidé" if reparable else ""),
                    reparee=reparable,
                )
            )
    if reparer:
        session.flush()


# --------------------------------------------------------------------------- #
# Règle 3 — une entrée facturée pointe une facture existante et est facturable
# --------------------------------------------------------------------------- #
def _regle3_entrees_facturees(session: Session, rapport: RapportIntegrite) -> None:
    for entry in session.scalars(select(Entry).where(Entry.invoice_id.is_not(None))):
        facture = session.get(Invoice, entry.invoice_id)
        if facture is None:
            rapport.anomalies.append(
                Anomalie(
                    regle="3-entree-facturee",
                    entite="entries",
                    entite_id=entry.id,
                    message=f"invoice_id={entry.invoice_id} inexistante",
                )
            )
            continue
        if not entry.facturable:
            rapport.anomalies.append(
                Anomalie(
                    regle="3-entree-facturee",
                    entite="entries",
                    entite_id=entry.id,
                    message=f"rattachée à la facture {facture.id} mais facturable=0",
                )
            )
        if facture.user_id != entry.user_id:
            rapport.anomalies.append(
                Anomalie(
                    regle="3-entree-facturee",
                    entite="entries",
                    entite_id=entry.id,
                    message=(
                        f"entrée de l'expert {entry.user_id} rattachée à la facture "
                        f"{facture.id} de l'expert {facture.user_id}"
                    ),
                )
            )


# --------------------------------------------------------------------------- #
# Règle 4 — totaux des factures
# --------------------------------------------------------------------------- #
def _regle4_totaux_factures(session: Session, rapport: RapportIntegrite, reparer: bool) -> None:
    for facture in session.scalars(select(Invoice)):
        somme_labor = arrondi_money(sum((l.montant for l in facture.labor_lines), Decimal("0")))
        somme_odc = arrondi_money(sum((o.montant for o in facture.odc_lines), Decimal("0")))
        attendu_net = arrondi_money(somme_labor + somme_odc - Decimal(facture.avance))
        emise = StatutFacture(facture.statut) is not StatutFacture.BROUILLON
        reparable = reparer and not emise

        for champ, courant, attendu in (
            ("sous_total_labor", arrondi_money(facture.sous_total_labor), somme_labor),
            ("sous_total_odc", arrondi_money(facture.sous_total_odc), somme_odc),
            ("total_net", arrondi_money(facture.total_net), attendu_net),
        ):
            if courant == attendu:
                continue
            if reparable:
                setattr(facture, champ, attendu)
            rapport.anomalies.append(
                Anomalie(
                    regle="4-totaux-facture",
                    entite="invoices",
                    entite_id=facture.id,
                    message=f"{champ} {courant} ≠ {attendu}"
                    + ("" if reparable else " — facture émise, non réparée"),
                    reparee=reparable,
                )
            )
        for ligne in facture.labor_lines:
            attendu_ligne = arrondi_money(Decimal(ligne.quantite) * Decimal(ligne.taux))
            if arrondi_money(ligne.montant) != attendu_ligne:
                rapport.anomalies.append(
                    Anomalie(
                        regle="4-totaux-facture",
                        entite="invoice_labor",
                        entite_id=ligne.id,
                        message=f"montant {ligne.montant} ≠ {attendu_ligne}",
                    )
                )
        for ligne in facture.odc_lines:
            attendu_ligne = arrondi_money(Decimal(ligne.units) * Decimal(ligne.unit_cost))
            if arrondi_money(ligne.montant) != attendu_ligne:
                rapport.anomalies.append(
                    Anomalie(
                        regle="4-totaux-facture",
                        entite="invoice_odc",
                        entite_id=ligne.id,
                        message=f"montant {ligne.montant} ≠ {attendu_ligne}",
                    )
                )
        if Decimal(facture.avance) < 0:
            rapport.anomalies.append(
                Anomalie(
                    regle="4-totaux-facture",
                    entite="invoices",
                    entite_id=facture.id,
                    message=f"avance négative ({facture.avance})",
                )
            )
        elif Decimal(facture.avance) > somme_labor + somme_odc:
            rapport.anomalies.append(
                Anomalie(
                    regle="4-totaux-facture",
                    entite="invoices",
                    entite_id=facture.id,
                    message=(
                        f"avance {facture.avance} supérieure au total "
                        f"{somme_labor + somme_odc}"
                    ),
                )
            )
    if reparer:
        session.flush()


# --------------------------------------------------------------------------- #
# Règle 5 — consommation (option C)
# --------------------------------------------------------------------------- #
def jours_consommes_entry(entry: Entry, heures_par_jour: Decimal) -> Decimal:
    """Jours consommés par une entrée — option C.

    Une entrée en jours compte sa quantité telle quelle. Une entrée en heures
    est ramenée en jours avec `heures_par_jour` : la facturation, elle, ne fait
    jamais cette conversion.
    """
    if Unite(entry.unite) is Unite.JOUR:
        return Decimal(entry.quantite)
    diviseur = heures_par_jour if heures_par_jour > 0 else Decimal("8")
    return Decimal(entry.quantite) / diviseur


def calculer_consommation(
    session: Session, user_id: int | None = None, project_id: int | None = None
) -> list[ConsommationCouple]:
    """Consommation par couple (expert, projet), allocations incluses à 0.

    Les couples sans allocation mais avec des entrées sont renvoyés aussi :
    ce sont précisément les dépassements qu'il faut voir.
    """
    hpj = _heures_par_jour_courant(session)

    consommation: dict[tuple[int, int], Decimal] = {}
    requete = select(Entry)
    if user_id is not None:
        requete = requete.where(Entry.user_id == user_id)
    if project_id is not None:
        requete = requete.where(Entry.project_id == project_id)
    for entry in session.scalars(requete):
        cle = (entry.user_id, entry.project_id)
        consommation[cle] = consommation.get(cle, Decimal("0")) + jours_consommes_entry(entry, hpj)

    allocations: dict[tuple[int, int], Decimal] = {}
    requete_alloc = select(Allocation)
    if user_id is not None:
        requete_alloc = requete_alloc.where(Allocation.user_id == user_id)
    if project_id is not None:
        requete_alloc = requete_alloc.where(Allocation.project_id == project_id)
    for allocation in session.scalars(requete_alloc):
        allocations[(allocation.user_id, allocation.project_id)] = Decimal(
            allocation.jours_alloues
        )

    noms_users = {u.id: u.nom for u in session.scalars(select(User))}
    noms_projets = {p.id: p.nom for p in session.scalars(select(Project))}

    resultat: list[ConsommationCouple] = []
    for (uid, pid) in sorted(set(consommation) | set(allocations)):
        resultat.append(
            ConsommationCouple(
                user_id=uid,
                user_nom=noms_users.get(uid, f"#{uid}"),
                project_id=pid,
                project_nom=noms_projets.get(pid, f"#{pid}"),
                jours_alloues=allocations.get((uid, pid), Decimal("0")),
                jours_consommes=consommation.get((uid, pid), Decimal("0")).quantize(CENT),
            )
        )
    return resultat


def seuils(session: Session) -> tuple[int, int]:
    """`(seuil_alerte_pct, seuil_critique_pct)` depuis la config."""
    config = get_config(session)
    return int(config.seuil_alerte_pct), int(config.seuil_critique_pct)
