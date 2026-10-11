"""M3 + M4 — Saisie des entrées et génération du timesheet."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import streamlit as st
from sqlalchemy import select

from core.alerts_service import depassement_a_signaler
from core.auth import UtilisateurConnecte, current_user, require_action
from core.config_service import livrables_projet, projets_alloues
from core.db import get_session
from core.entries_service import (
    apercu_entree,
    calculer_totaux,
    creer_entree,
    dupliquer_entree,
    entree_verrouillee,
    lister_entrees,
    modifier_entree,
    supprimer_entree,
    valider_entree,
)
from core.enums import Role, TypeActivite, Unite
from core.models import Entry, Invoice, User
from core.timesheet_export import generer_timesheet, total_heures_attendu
from ui.common import afficher_erreurs, nombre, selecteur_mois, tableau, telechargements, usd

LIBELLES_ACTIVITE = {
    TypeActivite.FEDERAL: "Federal",
    TypeActivite.NON_FEDERAL: "Non-federal",
    TypeActivite.ADMIN: "Company/administrative",
    TypeActivite.BD: "Proposal / business development",
}


def expert_cible(utilisateur: UtilisateurConnecte) -> int | None:
    """Expert pour lequel on saisit : soi-même, ou un expert choisi par l'admin."""
    if utilisateur.role is not Role.ADMIN:
        return utilisateur.id
    with get_session() as session:
        experts = list(
            session.scalars(
                select(User)
                .where(User.role == Role.EXPERT, User.actif.is_(True))
                .order_by(User.nom)
            )
        )
        choix = {f"{u.nom} ({u.email})": u.id for u in experts}
    if not choix:
        st.warning("Aucun expert actif : créez un compte expert dans Utilisateurs.")
        return None
    libelle = st.selectbox(
        "Saisir pour l'expert", list(choix), key="timesheet_expert",
        help="En tant qu'administrateur, vous saisissez pour le compte d'un expert ; "
             "l'action est journalisée.",
    )
    return choix[libelle]


def afficher() -> None:
    utilisateur = require_action("saisie_entries")
    st.header("Timesheet")
    user_id = expert_cible(utilisateur)
    if user_id is None:
        return

    onglets = st.tabs(["Saisir une entrée", "Mes entrées", "Générer le timesheet"])
    with onglets[0]:
        _saisie(utilisateur, user_id)
    with onglets[1]:
        _liste(utilisateur, user_id)
    with onglets[2]:
        _generation(user_id)


def _saisie(utilisateur: UtilisateurConnecte, user_id: int) -> None:
    with get_session() as session:
        projets = projets_alloues(session, user_id)
        choix_projets = {f"{p.nom} ({p.numero or 'sans numéro'})": p.id for p in projets}
    if not choix_projets:
        st.warning(
            "Aucun projet alloué à cet expert : l'administrateur doit créer une "
            "allocation (Configuration → Allocations)."
        )
        return

    libelle_projet = st.selectbox("Projet", list(choix_projets), key="saisie_projet")
    project_id = choix_projets[libelle_projet]

    with get_session() as session:
        livrables = livrables_projet(session, project_id)
        choix_livrables = {"— aucun —": None} | {d.intitule: d.id for d in livrables}
        avertissement = depassement_a_signaler(session, user_id, project_id)
    if avertissement:
        st.warning(avertissement)

    colonnes = st.columns(3)
    date_entry = colonnes[0].date_input("Date", value=date.today(), key="saisie_date")
    unite = colonnes[1].selectbox("Unité", list(Unite), format_func=str, key="saisie_unite")
    quantite = colonnes[2].number_input(
        "Quantité", min_value=0.0, value=1.0, step=0.5, key="saisie_quantite"
    )

    colonnes_detail = st.columns(2)
    libelle_livrable = colonnes_detail[0].selectbox(
        "Livrable", list(choix_livrables), key="saisie_livrable"
    )
    type_activite = colonnes_detail[1].selectbox(
        "Type d'activité", list(TypeActivite),
        format_func=lambda t: LIBELLES_ACTIVITE[t], key="saisie_type",
    )
    note = st.text_area(
        "Notes / Activities / Deliverables", key="saisie_note",
        help="Reporté tel quel dans la colonne E du timesheet.",
    )
    facturable = st.checkbox("Facturable", value=True, key="saisie_facturable")

    # Aperçu en direct, avant toute écriture.
    with get_session() as session:
        erreurs, taux = valider_entree(
            session, user_id, project_id, unite, quantite, choix_livrables[libelle_livrable]
        )
        apercu = apercu_entree(session, unite, quantite, taux)
    colonnes_apercu = st.columns(3)
    colonnes_apercu[0].metric("Taux appliqué", usd(taux) if taux else "—")
    colonnes_apercu[1].metric("Montant", usd(apercu["montant"]))
    colonnes_apercu[2].metric("Heures timesheet", nombre(apercu["heures_timesheet"]))
    if erreurs:
        for erreur in erreurs:
            st.caption(f"⚠️ {erreur}")

    if st.button("Enregistrer l'entrée", type="primary", key="saisie_submit"):
        with get_session() as session:
            _, erreurs = creer_entree(
                session,
                utilisateur.id,
                user_id=user_id,
                project_id=project_id,
                date_entry=date_entry,
                unite=unite,
                quantite=Decimal(str(quantite)),
                type_activite=type_activite,
                deliverable_id=choix_livrables[libelle_livrable],
                note_livrable=note,
                facturable=facturable,
            )
        if not afficher_erreurs(erreurs):
            st.success("Entrée enregistrée.")
            st.rerun()


def _liste(utilisateur: UtilisateurConnecte, user_id: int) -> None:
    colonnes = st.columns([1, 1, 2])
    with colonnes[0]:
        annee, mois = selecteur_mois("liste")
    with get_session() as session:
        projets = projets_alloues(session, user_id, actifs_seulement=False)
        choix_projets = {"— tous —": None} | {p.nom: p.id for p in projets}
    libelle_projet = colonnes[2].selectbox("Projet", list(choix_projets), key="liste_projet")

    with get_session() as session:
        entrees = lister_entrees(
            session, user_id=user_id, annee=annee, mois=mois,
            project_id=choix_projets[libelle_projet],
        )
        totaux = calculer_totaux(session, entrees)
        lignes = []
        for entree in entrees:
            facture = (
                session.get(Invoice, entree.invoice_id) if entree.invoice_id else None
            )
            lignes.append(
                {
                    "id": entree.id,
                    "Date": entree.date_entry,
                    "Projet": entree.project.nom,
                    "Unité": str(entree.unite),
                    "Quantité": float(entree.quantite),
                    "Taux": usd(entree.taux_applique),
                    "Montant": usd(entree.montant),
                    "Heures (équiv.)": float(entree.heures_timesheet),
                    "Type": str(entree.type_activite),
                    "Facturable": "oui" if entree.facturable else "non",
                    "Facture": (
                        (facture.numero or f"brouillon #{facture.id}") if facture else "—"
                    ),
                }
            )
        verrous = {e.id: entree_verrouillee(session, e) for e in entrees}

    tableau(lignes, vide="Aucune entrée pour ce mois.")
    colonnes_totaux = st.columns(5)
    colonnes_totaux[0].metric("Entrées", totaux.nb_entrees)
    colonnes_totaux[1].metric("Heures", nombre(totaux.heures))
    colonnes_totaux[2].metric("Jours (équiv.)", nombre(totaux.jours))
    colonnes_totaux[3].metric("Facturable", usd(totaux.montant_facturable))
    colonnes_totaux[4].metric("Non facturable", usd(totaux.montant_non_facturable))

    if not entrees:
        return
    with st.expander("Modifier, dupliquer ou supprimer une entrée"):
        choix = {
            f"#{e.id} — {e.date_entry} · {e.project.nom} · {e.quantite} {e.unite}": e.id
            for e in entrees
        }
        libelle = st.selectbox("Entrée", list(choix), key="liste_edit_select")
        entry_id = choix[libelle]
        if verrous.get(entry_id):
            st.warning(verrous[entry_id])
            return
        _edition_entree(utilisateur, entry_id)


def _edition_entree(utilisateur: UtilisateurConnecte, entry_id: int) -> None:
    with get_session() as session:
        entree = session.get(Entry, entry_id)
        if entree is None:
            st.error("Entrée introuvable.")
            return
        valeurs = {
            "date_entry": entree.date_entry,
            "unite": Unite(entree.unite),
            "quantite": float(entree.quantite),
            "note": entree.note_livrable or "",
            "type_activite": TypeActivite(entree.type_activite),
            "facturable": bool(entree.facturable),
            "taux": entree.taux_applique,
        }

    colonnes = st.columns(3)
    date_entry = colonnes[0].date_input("Date", value=valeurs["date_entry"], key=f"e_date_{entry_id}")
    unite = colonnes[1].selectbox(
        "Unité", list(Unite), index=list(Unite).index(valeurs["unite"]),
        format_func=str, key=f"e_unite_{entry_id}",
    )
    quantite = colonnes[2].number_input(
        "Quantité", min_value=0.0, value=valeurs["quantite"], step=0.5, key=f"e_qte_{entry_id}"
    )
    note = st.text_area("Notes / Activities / Deliverables", value=valeurs["note"], key=f"e_note_{entry_id}")
    colonnes_detail = st.columns(3)
    type_activite = colonnes_detail[0].selectbox(
        "Type d'activité", list(TypeActivite),
        index=list(TypeActivite).index(valeurs["type_activite"]),
        format_func=lambda t: LIBELLES_ACTIVITE[t], key=f"e_type_{entry_id}",
    )
    facturable = colonnes_detail[1].checkbox(
        "Facturable", value=valeurs["facturable"], key=f"e_fact_{entry_id}"
    )
    reappliquer = colonnes_detail[2].checkbox(
        "Réappliquer le TJM actuel", value=False, key=f"e_tjm_{entry_id}",
        help=f"Taux figé actuellement : {usd(valeurs['taux'])}. Sans cette case, "
             "le snapshot d'origine est conservé.",
    )

    boutons = st.columns(3)
    if boutons[0].button("Enregistrer", key=f"e_save_{entry_id}"):
        with get_session() as session:
            _, erreurs = modifier_entree(
                session, utilisateur.id, entry_id, reappliquer_tjm=reappliquer,
                date_entry=date_entry, unite=unite, quantite=Decimal(str(quantite)),
                note_livrable=note, type_activite=type_activite, facturable=facturable,
            )
        if not afficher_erreurs(erreurs):
            st.success("Entrée modifiée.")
            st.rerun()
    if boutons[1].button("Dupliquer", key=f"e_dup_{entry_id}"):
        with get_session() as session:
            _, erreurs = dupliquer_entree(session, utilisateur.id, entry_id, date.today())
        if not afficher_erreurs(erreurs):
            st.success("Entrée dupliquée à aujourd'hui.")
            st.rerun()
    if boutons[2].button("Supprimer", key=f"e_del_{entry_id}"):
        with get_session() as session:
            erreurs = supprimer_entree(session, utilisateur.id, entry_id)
        if not afficher_erreurs(erreurs):
            st.success("Entrée supprimée.")
            st.rerun()


def _generation(user_id: int) -> None:
    st.caption(
        "Le timesheet reporte **toute** l'activité du mois — federal, non-federal, "
        "administratif et business development, facturable ou non : c'est un "
        "*effort record*."
    )
    annee, mois = selecteur_mois("gen")
    with get_session() as session:
        attendu = total_heures_attendu(session, user_id, annee, mois)
        nb = len(lister_entrees(session, user_id=user_id, annee=annee, mois=mois))
    colonnes = st.columns(2)
    colonnes[0].metric("Entrées du mois", nb)
    colonnes[1].metric("Total heures attendu", nombre(attendu))

    if nb == 0:
        st.info("Aucune entrée pour ce mois : rien à générer.")
        return
    if st.button("Générer le timesheet", type="primary", key="gen_submit"):
        with get_session() as session:
            flux, nom = generer_timesheet(session, user_id, annee, mois)
        st.session_state["timesheet_flux"] = flux.getvalue()
        st.session_state["timesheet_nom"] = nom

    if st.session_state.get("timesheet_flux"):
        from io import BytesIO

        telechargements(
            BytesIO(st.session_state["timesheet_flux"]),
            st.session_state["timesheet_nom"],
            proposer_pdf=True,
            cle="timesheet",
        )
