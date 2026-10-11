"""M7 — Dashboard animé, à périmètre adapté au rôle."""
from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import select

from core.auth import UtilisateurConnecte, current_user
from core.db import get_config, get_session
from core.enums import Role
from core.metrics_service import (
    avancement_par_projet,
    consommation_par_expert,
    facture_par_mois,
    kpis_factures,
    kpis_projets,
    kpis_taches,
    repartition_heures,
    timeline_livrables,
)
from core.models import Project, User
from ui.common import COULEURS_STATUT, nombre, tableau, usd

GABARIT = "plotly_white"
TRANSITION = {"transition": {"duration": 600, "easing": "cubic-in-out"}}


def afficher() -> None:
    utilisateur = current_user()
    if utilisateur is None:
        st.error("Accès non autorisé.")
        st.stop()
    st.header("Dashboard")

    transversal = utilisateur.role in (Role.DEPUTY_MANAGER, Role.ADMIN)
    user_id, project_id, debut, fin = _filtres(utilisateur, transversal)

    with get_session() as session:
        taches = kpis_taches(session, user_id, project_id, debut, fin)
        factures = kpis_factures(session, user_id, debut, fin)
        projets = kpis_projets(session, user_id)
        avancement = avancement_par_projet(session, user_id, project_id)
        mensuel = facture_par_mois(session, user_id)
        par_activite = repartition_heures(session, "type_activite", user_id, debut, fin)
        par_projet = repartition_heures(session, "projet", user_id, debut, fin)
        livrables = timeline_livrables(session, user_id)
        par_expert = consommation_par_expert(session, project_id) if transversal else []
        config = get_config(session)
        seuil_alerte = int(config.seuil_alerte_pct)
        seuil_critique = int(config.seuil_critique_pct)

    _kpis(taches, factures, projets, avancement)
    st.divider()

    colonnes = st.columns(2)
    with colonnes[0]:
        _graphe_avancement(avancement, seuil_alerte, seuil_critique)
    with colonnes[1]:
        _graphe_facture_mensuelle(mensuel)

    colonnes_repartition = st.columns(2)
    with colonnes_repartition[0]:
        _graphe_repartition(par_activite, "Heures par type d'activité")
    with colonnes_repartition[1]:
        _graphe_repartition(par_projet, "Heures par projet", donut=True)

    _timeline_livrables(livrables)
    if transversal:
        _graphe_experts(par_expert, seuil_alerte, seuil_critique)


def _filtres(
    utilisateur: UtilisateurConnecte, transversal: bool
) -> tuple[int | None, int | None, date, date]:
    aujourdhui = date.today()
    colonnes = st.columns(4)
    debut = colonnes[0].date_input(
        "Du", value=aujourdhui.replace(month=1, day=1), key="dash_debut"
    )
    fin = colonnes[1].date_input("Au", value=aujourdhui, key="dash_fin")

    with get_session() as session:
        projets = {"— tous —": None} | {
            p.nom: p.id for p in session.scalars(select(Project).order_by(Project.nom))
        }
        if transversal:
            experts = {"— tous —": None} | {
                u.nom: u.id
                for u in session.scalars(select(User).order_by(User.nom))
            }
        else:
            experts = {}

    projet = colonnes[2].selectbox("Projet", list(projets), key="dash_projet")
    if transversal:
        expert = colonnes[3].selectbox("Expert", list(experts), key="dash_expert")
        user_id = experts[expert]
    else:
        colonnes[3].caption("Périmètre : vos données.")
        user_id = utilisateur.id
    return user_id, projets[projet], debut, fin


def _kpis(taches: dict, factures: dict, projets: dict, avancement: list[dict]) -> None:
    colonnes = st.columns(4)
    colonnes[0].metric("Entrées", taches["nb_entrees"])
    colonnes[1].metric("Heures", nombre(taches["heures"]))
    colonnes[2].metric("Jours (équiv.)", nombre(taches["jours"]))
    total_alloue = sum((l["budget_jours"] for l in avancement), start=0)
    total_consomme = sum((l["jours_consommes"] for l in avancement), start=0)
    pct = (total_consomme / total_alloue * 100) if total_alloue else 0
    colonnes[3].metric("Avancement global", f"{float(pct):.1f} %")

    colonnes_factures = st.columns(4)
    colonnes_factures[0].metric("Facturé", usd(factures["montant_facture"]))
    colonnes_factures[1].metric("Payé", usd(factures["montant_paye"]))
    colonnes_factures[2].metric("En attente", usd(factures["montant_en_attente"]))
    colonnes_factures[3].metric(
        "Livrables livrés", f"{projets['nb_livrables_livres']} / {projets['nb_livrables']}"
    )

    par_statut = factures["par_statut"]
    st.caption(
        " · ".join(
            f"{statut} : {valeurs['nb']} ({usd(valeurs['montant'])})"
            for statut, valeurs in par_statut.items()
        )
        + f" · projets actifs : {projets['nb_projets_actifs']}"
    )


def _couleur_pct(pct: float, seuil_alerte: int, seuil_critique: int) -> str:
    if pct >= seuil_critique:
        return COULEURS_STATUT["Critique"]
    if pct >= seuil_alerte:
        return COULEURS_STATUT["Alerte"]
    return COULEURS_STATUT["OK"]


def _graphe_avancement(lignes: list[dict], seuil_alerte: int, seuil_critique: int) -> None:
    st.subheader("Avancement par projet")
    if not lignes:
        st.info("Aucun projet à afficher.")
        return
    donnees = pd.DataFrame(
        [
            {
                "Projet": l["projet"],
                "Consommés": float(l["jours_consommes"]),
                "Budget": float(l["budget_jours"]),
                "pct": float(l["pct"]),
            }
            for l in lignes
        ]
    )
    figure = go.Figure()
    figure.add_bar(
        x=donnees["Projet"], y=donnees["Budget"], name="Budget (jours)",
        marker_color="#D8D8D8", hovertemplate="%{x}<br>Budget : %{y} j<extra></extra>",
    )
    figure.add_bar(
        x=donnees["Projet"],
        y=donnees["Consommés"],
        name="Consommés (jours)",
        marker_color=[
            _couleur_pct(pct, seuil_alerte, seuil_critique) for pct in donnees["pct"]
        ],
        text=[f"{pct:.0f} %" for pct in donnees["pct"]],
        textposition="outside",
        hovertemplate="%{x}<br>Consommés : %{y} j<extra></extra>",
    )
    figure.update_layout(
        barmode="overlay", template=GABARIT, height=380,
        yaxis_title="Jours", legend_title_text="",
        margin={"t": 30, "b": 10}, **TRANSITION,
    )
    st.plotly_chart(figure, use_container_width=True)
    st.caption(
        f"Vert sous {seuil_alerte} %, orange de {seuil_alerte} à {seuil_critique} %, "
        f"rouge au-delà — le pourcentage est écrit sur chaque barre."
    )


def _graphe_facture_mensuelle(lignes: list[dict]) -> None:
    st.subheader("Facturé par mois")
    if not lignes:
        st.info("Aucune facture émise.")
        return
    donnees = pd.DataFrame(
        [
            {
                "Mois": l["periode"],
                "Émis": float(l["montant_emis"]),
                "Payé": float(l["montant_paye"]),
            }
            for l in lignes
        ]
    )
    figure = go.Figure()
    figure.add_bar(x=donnees["Mois"], y=donnees["Émis"], name="Émis", marker_color="#E8833A")
    figure.add_scatter(
        x=donnees["Mois"], y=donnees["Payé"], name="Payé", mode="lines+markers",
        line={"color": "#2E7D32", "width": 3},
    )
    figure.update_layout(
        template=GABARIT, height=380, yaxis_title="USD",
        margin={"t": 30, "b": 10}, **TRANSITION,
    )
    st.plotly_chart(figure, use_container_width=True)


def _graphe_repartition(lignes: list[dict], titre: str, donut: bool = False) -> None:
    st.subheader(titre)
    if not lignes:
        st.info("Aucune heure saisie sur la période.")
        return
    donnees = pd.DataFrame(
        [{"Libellé": l["libelle"], "Heures": float(l["heures"])} for l in lignes]
    )
    if donut:
        figure = px.pie(
            donnees, names="Libellé", values="Heures", hole=0.55, template=GABARIT
        )
        figure.update_traces(textposition="inside", textinfo="label+percent")
    else:
        figure = px.bar(
            donnees, x="Libellé", y="Heures", text="Heures", template=GABARIT,
            color="Libellé",
        )
        figure.update_traces(textposition="outside")
    figure.update_layout(height=380, margin={"t": 30, "b": 10}, showlegend=donut, **TRANSITION)
    st.plotly_chart(figure, use_container_width=True)


def _timeline_livrables(lignes: list[dict]) -> None:
    st.subheader("Livrables : échéances et statuts")
    datees = [l for l in lignes if l["echeance"]]
    if not datees:
        tableau(
            [
                {"Projet": l["projet"], "Livrable": l["intitule"], "Statut": l["statut"]}
                for l in lignes
            ],
            vide="Aucun livrable.",
        )
        if lignes:
            st.caption("Aucune échéance renseignée : pas de frise possible.")
        return

    couleurs = {"a_faire": "#9E9E9E", "en_cours": "#E8833A", "livre": "#2E7D32"}
    donnees = pd.DataFrame(
        [
            {
                "Livrable": f"{l['projet']} — {l['intitule']}",
                "Début": l["echeance"] - timedelta(days=7),
                "Échéance": l["echeance"],
                "Statut": l["statut"],
            }
            for l in datees
        ]
    )
    figure = px.timeline(
        donnees, x_start="Début", x_end="Échéance", y="Livrable", color="Statut",
        color_discrete_map=couleurs, template=GABARIT,
    )
    figure.update_yaxes(autorange="reversed")
    figure.update_layout(height=max(260, 42 * len(donnees)), margin={"t": 30}, **TRANSITION)
    st.plotly_chart(figure, use_container_width=True)
    st.caption("Chaque barre couvre la semaine précédant l'échéance du livrable.")


def _graphe_experts(lignes: list[dict], seuil_alerte: int, seuil_critique: int) -> None:
    st.subheader("Consommation par expert")
    if not lignes:
        st.info("Aucune consommation enregistrée.")
        return
    donnees = pd.DataFrame(
        [
            {
                "Expert": l["expert"],
                "Consommés": float(l["jours_consommes"]),
                "Restants": max(0.0, float(l["jours_restants"])),
                "pct": float(l["pct"]),
            }
            for l in lignes
        ]
    )
    figure = go.Figure()
    figure.add_bar(
        y=donnees["Expert"], x=donnees["Consommés"], name="Consommés",
        orientation="h",
        marker_color=[
            _couleur_pct(pct, seuil_alerte, seuil_critique) for pct in donnees["pct"]
        ],
    )
    figure.add_bar(
        y=donnees["Expert"], x=donnees["Restants"], name="Restants",
        orientation="h", marker_color="#D8D8D8",
    )
    figure.update_layout(
        barmode="stack", template=GABARIT, height=max(280, 44 * len(donnees)),
        xaxis_title="Jours", margin={"t": 30}, **TRANSITION,
    )
    figure.add_vline(
        x=0, line_width=0,
    )
    st.plotly_chart(figure, use_container_width=True)
    tableau(
        [
            {
                "Expert": l["expert"],
                "Alloués": nombre(l["jours_alloues"]),
                "Consommés": nombre(l["jours_consommes"]),
                "Restants": nombre(l["jours_restants"]),
                "%": nombre(l["pct"]),
            }
            for l in lignes
        ]
    )
