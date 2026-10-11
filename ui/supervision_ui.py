"""M8 — Écran de supervision du deputy manager (et de l'admin)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import streamlit as st
from sqlalchemy import select

from core.alerts_service import (
    STATUT_OK,
    brouillon_demande_extras,
    date_projetee_epuisement,
    exporter_vue_xlsx,
    generer_alertes,
    lister_alertes,
    marquer_alerte_traitee,
    tableau_supervision,
)
from core.auth import require_action
from core.db import get_session
from core.entries_service import lister_entrees
from core.enums import StatutAlerte
from core.models import Project, User
from ui.common import MIME_XLSX, afficher_erreurs, badge_statut, nombre, tableau, usd


def afficher() -> None:
    utilisateur = require_action("supervision")
    st.header("Supervision")
    st.caption(
        "Vue globale en lecture seule : aucune entrée ni facture d'un expert "
        "n'est modifiable depuis cet écran."
    )

    colonnes = st.columns(4)
    with get_session() as session:
        experts = {"— tous —": None} | {
            u.nom: u.id for u in session.scalars(select(User).order_by(User.nom))
        }
        projets = {"— tous —": None} | {
            p.nom: p.id for p in session.scalars(select(Project).order_by(Project.nom))
        }
    expert = colonnes[0].selectbox("Expert", list(experts), key="sup_expert")
    projet = colonnes[1].selectbox("Projet", list(projets), key="sup_projet")
    debut = colonnes[2].date_input("Du", value=None, key="sup_debut")
    fin = colonnes[3].date_input("Au", value=None, key="sup_fin")

    with get_session() as session:
        lignes = tableau_supervision(
            session, experts[expert], projets[projet], debut or None, fin or None
        )

    alertes = [ligne for ligne in lignes if ligne.statut != STATUT_OK]
    if alertes:
        st.markdown("#### Couples à surveiller")
        st.markdown(
            " &nbsp;|&nbsp; ".join(
                f"{badge_statut(l.statut)} {l.expert} / {l.projet} ({nombre(l.pct)} %)"
                for l in alertes
            ),
            unsafe_allow_html=True,
        )
    else:
        st.success("Aucun couple expert / projet au-delà du seuil d'alerte.")

    tableau(
        [
            {
                "Expert": l.expert,
                "Projet": l.projet,
                "Alloué": nombre(l.jours_alloues),
                "Consommé": nombre(l.jours_consommes),
                "Restant": nombre(l.jours_restants),
                "%": nombre(l.pct),
                "Statut": l.statut,
            }
            for l in lignes
        ],
        vide="Aucune consommation enregistrée.",
    )

    boutons = st.columns(3)
    if lignes:
        boutons[0].download_button(
            "Exporter la vue (.xlsx)",
            data=exporter_vue_xlsx(lignes).getvalue(),
            file_name=f"Supervision_{date.today().isoformat()}.xlsx",
            mime=MIME_XLSX,
            use_container_width=True,
        )
    if boutons[1].button("Enregistrer les alertes", use_container_width=True):
        with get_session() as session:
            nouvelles = generer_alertes(session, utilisateur.id)
        st.success(
            f"{len(nouvelles)} alerte(s) enregistrée(s)."
            if nouvelles
            else "Aucune nouvelle alerte : les franchissements en cours sont déjà consignés."
        )

    st.divider()
    onglets = st.tabs(["Détail d'un couple", "Demande d'extras", "Alertes enregistrées"])
    with onglets[0]:
        _detail(lignes)
    with onglets[1]:
        _demande_extras(utilisateur.id, lignes)
    with onglets[2]:
        _alertes(utilisateur.id)


def _detail(lignes: list) -> None:
    if not lignes:
        st.info("Aucun couple à détailler.")
        return
    choix = {f"{l.expert} / {l.projet}": (l.user_id, l.project_id) for l in lignes}
    libelle = st.selectbox("Couple", list(choix), key="sup_detail")
    user_id, project_id = choix[libelle]

    with get_session() as session:
        entrees = lister_entrees(session, user_id=user_id, project_id=project_id)
        projection = date_projetee_epuisement(session, user_id, project_id)
        detail = [
            {
                "Date": e.date_entry,
                "Unité": str(e.unite),
                "Quantité": float(e.quantite),
                "Heures (équiv.)": float(e.heures_timesheet),
                "Montant": usd(e.montant),
                "Type": str(e.type_activite),
                "Note": e.note_livrable or "",
            }
            for e in entrees
        ]

    if projection:
        st.metric("Épuisement projeté", projection.isoformat())
        st.caption("Extrapolation du rythme des 30 derniers jours — indicatif.")
    else:
        st.caption(
            "Épuisement projeté non estimable : pas de saisie récente, allocation "
            "absente, ou allocation déjà épuisée."
        )

    if detail:
        import pandas as pd

        cumul = pd.DataFrame(detail)[["Date", "Heures (équiv.)"]].copy()
        cumul = cumul.groupby("Date", as_index=False).sum()
        cumul["Heures cumulées"] = cumul["Heures (équiv.)"].cumsum()
        st.line_chart(cumul.set_index("Date")["Heures cumulées"])
    tableau(detail, vide="Aucune entrée pour ce couple.")


def _demande_extras(auteur_id: int, lignes: list) -> None:
    st.caption(
        "La demande est produite en **brouillon** : rien n'est envoyé. "
        "Relisez, copiez, transmettez vous-même."
    )
    if not lignes:
        st.info("Aucun couple disponible.")
        return
    choix = {f"{l.expert} / {l.projet}": (l.user_id, l.project_id) for l in lignes}
    libelle = st.selectbox("Couple concerné", list(choix), key="extras_couple")
    user_id, project_id = choix[libelle]
    jours = st.number_input(
        "Jours supplémentaires demandés", min_value=0.5, value=5.0, step=0.5, key="extras_jours"
    )
    justification = st.text_area("Justification", key="extras_just")

    if st.button("Produire le brouillon", key="extras_btn"):
        with get_session() as session:
            texte, erreurs = brouillon_demande_extras(
                session, auteur_id, user_id, project_id, Decimal(str(jours)), justification
            )
        if not afficher_erreurs(erreurs):
            st.session_state["extras_texte"] = texte

    if st.session_state.get("extras_texte"):
        st.text_area("Brouillon", value=st.session_state["extras_texte"], height=360)
        st.download_button(
            "Télécharger le brouillon (.txt)",
            data=st.session_state["extras_texte"].encode("utf-8"),
            file_name=f"Demande_extras_{date.today().isoformat()}.txt",
            mime="text/plain",
        )


def _alertes(auteur_id: int) -> None:
    statut = st.radio(
        "Statut", [StatutAlerte.OUVERTE, StatutAlerte.TRAITEE], format_func=str,
        horizontal=True, key="alertes_statut",
    )
    with get_session() as session:
        alertes = lister_alertes(session, statut)
        noms_experts = {u.id: u.nom for u in session.scalars(select(User))}
        noms_projets = {p.id: p.nom for p in session.scalars(select(Project))}
        lignes = [
            {
                "id": a.id,
                "Date": a.created_at,
                "Niveau": str(a.niveau),
                "Expert": noms_experts.get(a.user_id, f"#{a.user_id}"),
                "Projet": noms_projets.get(a.project_id, f"#{a.project_id}"),
                "%": nombre(a.pct),
                "Restants": nombre(a.jours_restants),
                "Message": a.message,
            }
            for a in alertes
        ]
    tableau(lignes, vide="Aucune alerte dans ce statut.")

    if statut is StatutAlerte.OUVERTE and lignes:
        choix = {f"#{l['id']} — {l['Expert']} / {l['Projet']} ({l['Niveau']})": l["id"] for l in lignes}
        libelle = st.selectbox("Alerte à clore", list(choix), key="alerte_close")
        if st.button("Marquer traitée", key="alerte_close_btn"):
            with get_session() as session:
                erreurs = marquer_alerte_traitee(session, auteur_id, choix[libelle])
            if not afficher_erreurs(erreurs):
                st.rerun()
