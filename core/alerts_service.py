"""M8 — Supervision : consommation, seuils, alertes et demandes d'extras.

Lecture seule sur les données d'autrui : rien ici ne modifie une entrée ou une
facture. Les seules écritures sont la table `alerts` et le journal d'audit.

Le calcul de consommation est celui de la règle d'intégrité n°5 (option C), de
sorte que supervision, dashboard et contrôle d'intégrité donnent le même
chiffre.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.audit import journaliser
from core.db import get_config
from core.enums import NiveauAlerte, StatutAlerte
from core.integrity import ConsommationCouple, calculer_consommation, jours_consommes_entry
from core.models import Alert, Entry, Project, User

CENT = Decimal("0.01")

STATUT_OK = "OK"
STATUT_ALERTE = "Alerte"
STATUT_CRITIQUE = "Critique"
STATUT_EPUISE = "Épuisé"

# Ordre de criticité, du plus grave au plus bénin.
ORDRE_CRITICITE = {STATUT_EPUISE: 0, STATUT_CRITIQUE: 1, STATUT_ALERTE: 2, STATUT_OK: 3}

NIVEAU_PAR_STATUT = {
    STATUT_EPUISE: NiveauAlerte.EPUISE,
    STATUT_CRITIQUE: NiveauAlerte.CRITIQUE,
    STATUT_ALERTE: NiveauAlerte.ALERTE,
}


@dataclass
class LigneSupervision:
    """Une ligne du tableau de supervision : un couple (expert, projet)."""

    user_id: int
    expert: str
    project_id: int
    projet: str
    jours_alloues: Decimal
    jours_consommes: Decimal
    jours_restants: Decimal
    pct: Decimal
    statut: str

    @property
    def en_alerte(self) -> bool:
        return self.statut != STATUT_OK


def statut_couple(
    pct: Decimal, jours_restants: Decimal, seuil_alerte: int, seuil_critique: int
) -> str:
    """Statut d'un couple selon les seuils de la configuration.

    L'épuisement prime : un couple sans jour restant est épuisé, quel que soit
    son pourcentage (un projet sans allocation l'est d'emblée dès la première
    saisie).
    """
    if jours_restants <= 0:
        return STATUT_EPUISE
    if pct >= Decimal(seuil_critique):
        return STATUT_CRITIQUE
    if pct >= Decimal(seuil_alerte):
        return STATUT_ALERTE
    return STATUT_OK


def tableau_supervision(
    session: Session,
    user_id: int | None = None,
    project_id: int | None = None,
    debut: date | None = None,
    fin: date | None = None,
) -> list[LigneSupervision]:
    """Tableau trié par criticité décroissante, puis par pourcentage."""
    config = get_config(session)
    seuil_alerte = int(config.seuil_alerte_pct)
    seuil_critique = int(config.seuil_critique_pct)

    couples = calculer_consommation(session, user_id=user_id, project_id=project_id)
    if debut is not None or fin is not None:
        couples = _recalculer_sur_periode(session, couples, debut, fin)

    noms_experts = {u.id: u.nom for u in session.scalars(select(User))}
    lignes = [
        LigneSupervision(
            user_id=couple.user_id,
            expert=noms_experts.get(couple.user_id, couple.user_nom),
            project_id=couple.project_id,
            projet=couple.project_nom,
            jours_alloues=couple.jours_alloues,
            jours_consommes=couple.jours_consommes,
            jours_restants=couple.jours_restants,
            pct=couple.pct,
            statut=statut_couple(
                couple.pct, couple.jours_restants, seuil_alerte, seuil_critique
            ),
        )
        for couple in couples
    ]
    return sorted(lignes, key=lambda l: (ORDRE_CRITICITE[l.statut], -l.pct, l.expert))


def _recalculer_sur_periode(
    session: Session,
    couples: list[ConsommationCouple],
    debut: date | None,
    fin: date | None,
) -> list[ConsommationCouple]:
    """Restreint la consommation à une période, allocations inchangées.

    Une allocation n'est pas datée : elle reste la référence, seule la
    consommation est bornée.
    """
    hpj = Decimal(get_config(session).heures_par_jour)
    requete = select(Entry)
    if debut is not None:
        requete = requete.where(Entry.date_entry >= debut)
    if fin is not None:
        requete = requete.where(Entry.date_entry <= fin)

    consommation: dict[tuple[int, int], Decimal] = {}
    for entree in session.scalars(requete):
        cle = (entree.user_id, entree.project_id)
        consommation[cle] = consommation.get(cle, Decimal("0")) + jours_consommes_entry(
            entree, hpj
        )
    for couple in couples:
        couple.jours_consommes = consommation.get(
            (couple.user_id, couple.project_id), Decimal("0")
        ).quantize(CENT)
    return couples


def bandeau_alertes(session: Session) -> list[LigneSupervision]:
    """Couples en Alerte, Critique ou Épuisé, les plus graves d'abord."""
    return [ligne for ligne in tableau_supervision(session) if ligne.en_alerte]


# --------------------------------------------------------------------------- #
# Projection d'épuisement
# --------------------------------------------------------------------------- #
def date_projetee_epuisement(
    session: Session, user_id: int, project_id: int, fenetre_jours: int = 30
) -> date | None:
    """Extrapolation simple de la date d'épuisement, sur le rythme récent.

    Renvoie `None` s'il n'y a pas de rythme exploitable (aucune saisie dans la
    fenêtre), si l'allocation est déjà épuisée, ou si aucune allocation n'est
    définie.
    """
    couples = calculer_consommation(session, user_id=user_id, project_id=project_id)
    if not couples:
        return None
    couple = couples[0]
    if couple.jours_alloues <= 0 or couple.jours_restants <= 0:
        return None

    aujourdhui = date.today()
    depuis = aujourdhui - timedelta(days=fenetre_jours)
    hpj = Decimal(get_config(session).heures_par_jour)
    recentes = session.scalars(
        select(Entry).where(
            Entry.user_id == user_id,
            Entry.project_id == project_id,
            Entry.date_entry >= depuis,
        )
    )
    consommes_recents = sum((jours_consommes_entry(e, hpj) for e in recentes), Decimal("0"))
    if consommes_recents <= 0:
        return None

    rythme_par_jour = consommes_recents / Decimal(fenetre_jours)
    jours_avant_epuisement = int((couple.jours_restants / rythme_par_jour).to_integral_value())
    # Au-delà de ~5 ans la projection ne dit plus rien d'utile.
    if jours_avant_epuisement > 1825:
        return None
    return aujourdhui + timedelta(days=jours_avant_epuisement)


# --------------------------------------------------------------------------- #
# Alertes
# --------------------------------------------------------------------------- #
def generer_alertes(session: Session, auteur_id: int | None) -> list[Alert]:
    """Enregistre une alerte par couple ayant franchi un seuil.

    Idempotent au niveau du couple et du niveau : si une alerte ouverte de même
    niveau existe déjà, rien n'est ajouté — on ne réinonde pas la table à
    chaque ouverture de l'écran.
    """
    nouvelles: list[Alert] = []
    ouvertes = {
        (a.user_id, a.project_id, NiveauAlerte(a.niveau))
        for a in session.scalars(
            select(Alert).where(Alert.statut == StatutAlerte.OUVERTE)
        )
    }
    for ligne in bandeau_alertes(session):
        niveau = NIVEAU_PAR_STATUT[ligne.statut]
        if (ligne.user_id, ligne.project_id, niveau) in ouvertes:
            continue
        alerte = Alert(
            project_id=ligne.project_id,
            user_id=ligne.user_id,
            niveau=niveau,
            pct=ligne.pct,
            jours_restants=ligne.jours_restants,
            message=(
                f"{ligne.expert} / {ligne.projet} : {ligne.jours_consommes} jours "
                f"consommés sur {ligne.jours_alloues} alloués ({ligne.pct} %), "
                f"{ligne.jours_restants} restants — {ligne.statut}."
            ),
            statut=StatutAlerte.OUVERTE,
        )
        session.add(alerte)
        nouvelles.append(alerte)
    if nouvelles:
        session.flush()
        journaliser(
            session, auteur_id, "alerts_generate", "alerts", None,
            {"nb": len(nouvelles)},
        )
    return nouvelles


def marquer_alerte_traitee(
    session: Session, auteur_id: int | None, alert_id: int
) -> list[str]:
    alerte = session.get(Alert, alert_id)
    if alerte is None:
        return ["Alerte inconnue."]
    alerte.statut = StatutAlerte.TRAITEE
    session.flush()
    journaliser(session, auteur_id, "alert_handled", "alerts", alert_id)
    return []


def lister_alertes(
    session: Session, statut: StatutAlerte | str | None = StatutAlerte.OUVERTE
) -> list[Alert]:
    requete = select(Alert).order_by(Alert.created_at.desc(), Alert.id.desc())
    if statut is not None:
        requete = requete.where(Alert.statut == StatutAlerte(statut))
    return list(session.scalars(requete))


def depassement_a_signaler(session: Session, user_id: int, project_id: int) -> str | None:
    """Message de dépassement à afficher à la saisie, le cas échéant (M8 §8.2)."""
    couples = calculer_consommation(session, user_id=user_id, project_id=project_id)
    if not couples:
        return None
    couple = couples[0]
    if couple.jours_alloues <= 0:
        return (
            "Aucune allocation définie pour ce couple expert / projet : "
            "toute saisie est en dépassement."
        )
    if couple.jours_restants <= 0:
        return (
            f"Allocation épuisée : {couple.jours_consommes} jours consommés sur "
            f"{couple.jours_alloues} alloués. Les saisies suivantes sont en "
            "dépassement."
        )
    return None


# --------------------------------------------------------------------------- #
# 8.4 Demande d'extras — brouillon uniquement, aucun envoi
# --------------------------------------------------------------------------- #
def brouillon_demande_extras(
    session: Session,
    auteur_id: int | None,
    user_id: int,
    project_id: int,
    jours_demandes: Decimal | float | str,
    justification: str,
) -> tuple[str, list[str]]:
    """Rédige le texte d'une demande d'extras. Rien n'est envoyé.

    Conforme au principe « rien d'irréversible sans action explicite » : la
    sortie est un texte à relire, copier et envoyer soi-même.
    """
    expert = session.get(User, user_id)
    projet = session.get(Project, project_id)
    if expert is None:
        return "", ["Expert inconnu."]
    if projet is None:
        return "", ["Projet inconnu."]
    try:
        jours = Decimal(str(jours_demandes))
    except Exception:
        return "", ["Le nombre de jours demandés doit être numérique."]
    if jours <= 0:
        return "", ["Le nombre de jours demandés doit être strictement positif."]
    if not str(justification or "").strip():
        return "", ["La justification est obligatoire."]

    couples = calculer_consommation(session, user_id=user_id, project_id=project_id)
    couple = couples[0] if couples else None
    alloues = couple.jours_alloues if couple else Decimal("0")
    consommes = couple.jours_consommes if couple else Decimal("0")
    restants = couple.jours_restants if couple else Decimal("0")
    projection = date_projetee_epuisement(session, user_id, project_id)

    texte = f"""Objet : demande de jours supplémentaires — {projet.nom} ({expert.nom})

Projet          : {projet.nom}{f" (n° {projet.numero})" if projet.numero else ""}
Expert          : {expert.nom}
Jours alloués   : {alloues}
Jours consommés : {consommes} ({couple.pct if couple else 0} %)
Jours restants  : {restants}
{f"Épuisement projeté : {projection.isoformat()}" if projection else "Épuisement projeté : non estimable sur le rythme récent"}

Jours supplémentaires demandés : {jours}

Justification :
{justification.strip()}

Demande à relire et à transmettre manuellement — ce brouillon n'a pas été envoyé.
"""
    journaliser(
        session, auteur_id, "extras_request_draft", "projects", project_id,
        {"user_id": user_id, "jours_demandes": jours},
    )
    return texte, []


def exporter_vue_xlsx(lignes: list[LigneSupervision]) -> BytesIO:
    """Export de la vue de supervision. Classeur simple, sans modèle imposé."""
    from openpyxl import Workbook
    from openpyxl.styles import Font

    workbook = Workbook()
    ws = workbook.active
    ws.title = "Supervision"
    entetes = [
        "Expert", "Projet", "Jours alloués", "Jours consommés",
        "Jours restants", "%", "Statut",
    ]
    ws.append(entetes)
    for cellule in ws[1]:
        cellule.font = Font(bold=True)
    for ligne in lignes:
        ws.append(
            [
                ligne.expert,
                ligne.projet,
                float(ligne.jours_alloues),
                float(ligne.jours_consommes),
                float(ligne.jours_restants),
                float(ligne.pct),
                ligne.statut,
            ]
        )
    for index, largeur in enumerate([26, 34, 14, 16, 14, 8, 12], start=1):
        ws.column_dimensions[ws.cell(row=1, column=index).column_letter].width = largeur
    ws.freeze_panes = "A2"

    flux = BytesIO()
    workbook.save(flux)
    flux.seek(0)
    return flux
