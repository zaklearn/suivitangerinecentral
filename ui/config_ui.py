"""M2 — Écrans de configuration, réservés à l'administrateur."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import streamlit as st
from sqlalchemy import select

from core.auth import require_action
from core.config_service import (
    avertissement_cloture,
    creer_livrable,
    creer_projet,
    definir_allocation,
    livrables_projet,
    maj_parametres,
    modifier_livrable,
    modifier_projet,
    supprimer_allocation,
)
from core.db import get_config, get_session
from core.enums import ModeNumerotation, Role, StatutLivrable, StatutProjet
from core.models import Allocation, Project, User
from ui.common import afficher_erreurs, nombre, tableau


def afficher() -> None:
    utilisateur = require_action("administration")
    st.header("Configuration")
    onglets = st.tabs(["Paramètres généraux", "Projets", "Allocations", "Livrables"])
    with onglets[0]:
        _parametres(utilisateur.id)
    with onglets[1]:
        _projets(utilisateur.id)
    with onglets[2]:
        _allocations(utilisateur.id)
    with onglets[3]:
        _livrables(utilisateur.id)


def _parametres(auteur_id: int) -> None:
    with get_session() as session:
        config = get_config(session)
        valeurs = {
            "heures_par_jour": float(config.heures_par_jour),
            "seuil_alerte_pct": int(config.seuil_alerte_pct),
            "seuil_critique_pct": int(config.seuil_critique_pct),
            "prefixe_facture": config.prefixe_facture,
            "mode_numerotation": ModeNumerotation(config.mode_numerotation),
            "bill_to_nom": config.bill_to_nom,
            "bill_to_ville": config.bill_to_ville,
            "bill_to_email": config.bill_to_email,
            "devise": config.devise,
        }

    st.info(
        "Modifier `heures par jour` ou un TJM ne recalcule **aucune** entrée "
        "existante : chaque entrée porte ses propres valeurs figées. Seules les "
        "nouvelles saisies sont concernées."
    )
    with st.form("parametres"):
        colonnes = st.columns(3)
        heures_par_jour = colonnes[0].number_input(
            "Heures par jour", min_value=0.5, max_value=24.0,
            value=valeurs["heures_par_jour"], step=0.5,
        )
        seuil_alerte = colonnes[1].number_input(
            "Seuil d'alerte (%)", min_value=1, max_value=99, value=valeurs["seuil_alerte_pct"]
        )
        seuil_critique = colonnes[2].number_input(
            "Seuil critique (%)", min_value=2, max_value=100, value=valeurs["seuil_critique_pct"]
        )
        st.text_input("Devise", value=valeurs["devise"], disabled=True, help="USD en v1.")

        st.markdown("**Numérotation des factures**")
        colonnes_num = st.columns(2)
        prefixe = colonnes_num[0].text_input("Préfixe", value=valeurs["prefixe_facture"])
        mode = colonnes_num[1].selectbox(
            "Mode",
            list(ModeNumerotation),
            index=list(ModeNumerotation).index(valeurs["mode_numerotation"]),
            format_func=lambda m: (
                "Par expert — {prefixe}-{code}-{année}-{seq}"
                if m is ModeNumerotation.PAR_EXPERT
                else "Globale — {prefixe}-{année}-{seq}"
            ),
        )
        st.caption(
            "Le mode « par expert » insère le code de l'expert : sans lui, deux "
            "experts obtiendraient le même numéro la même année."
        )

        st.markdown("**Bill To** (destinataire de la facture)")
        bill_to_nom = st.text_input("Nom", value=valeurs["bill_to_nom"])
        colonnes_bill = st.columns(2)
        bill_to_ville = colonnes_bill[0].text_input("Ville", value=valeurs["bill_to_ville"])
        bill_to_email = colonnes_bill[1].text_input("Email", value=valeurs["bill_to_email"])
        enregistrer = st.form_submit_button("Enregistrer")

    if not enregistrer:
        return
    with get_session() as session:
        config, erreurs = maj_parametres(
            session,
            auteur_id,
            heures_par_jour=Decimal(str(heures_par_jour)),
            seuil_alerte_pct=int(seuil_alerte),
            seuil_critique_pct=int(seuil_critique),
            prefixe_facture=prefixe,
            bill_to_nom=bill_to_nom,
            bill_to_ville=bill_to_ville,
            bill_to_email=bill_to_email,
        )
        if not erreurs:
            config.mode_numerotation = mode
    if not afficher_erreurs(erreurs):
        st.success("Paramètres enregistrés.")


def _projets(auteur_id: int) -> None:
    with get_session() as session:
        projets = list(session.scalars(select(Project).order_by(Project.nom)))
        tableau(
            [
                {
                    "Projet": p.nom,
                    "Numéro": p.numero or "—",
                    "Client": p.client,
                    "Budget (jours)": nombre(p.budget_jours),
                    "Statut": str(p.statut),
                    "Début": p.date_debut,
                    "Fin": p.date_fin,
                }
                for p in projets
            ],
            vide="Aucun projet.",
        )
        choix = {f"{p.nom} ({p.numero or 'sans numéro'})": p.id for p in projets}

    with st.expander("Créer un projet"):
        with st.form("creation_projet"):
            colonnes = st.columns(2)
            nom = colonnes[0].text_input("Nom du projet")
            numero = colonnes[1].text_input("Project/Proposal Number")
            colonnes_budget = st.columns(3)
            budget = colonnes_budget[0].number_input(
                "Budget (jours)", min_value=0.0, value=0.0, step=1.0
            )
            debut = colonnes_budget[1].date_input("Date de début", value=None)
            fin = colonnes_budget[2].date_input("Date de fin", value=None)
            valider = st.form_submit_button("Créer")
        if valider:
            with get_session() as session:
                _, erreurs = creer_projet(
                    session, auteur_id, nom=nom, numero=numero,
                    budget_jours=Decimal(str(budget)), date_debut=debut, date_fin=fin,
                )
            if not afficher_erreurs(erreurs):
                st.success("Projet créé.")
                st.rerun()

    if not choix:
        return
    with st.expander("Modifier un projet"):
        libelle = st.selectbox("Projet", list(choix), key="config_projet_edit")
        project_id = choix[libelle]
        with get_session() as session:
            projet = session.get(Project, project_id)
            valeurs = {
                "nom": projet.nom,
                "numero": projet.numero or "",
                "budget": float(projet.budget_jours or 0),
                "statut": StatutProjet(projet.statut),
                "debut": projet.date_debut,
                "fin": projet.date_fin,
            }
            avertissement = avertissement_cloture(session, project_id)

        with st.form(f"edition_projet_{project_id}"):
            colonnes = st.columns(2)
            nom = colonnes[0].text_input("Nom", value=valeurs["nom"])
            numero = colonnes[1].text_input("Numéro", value=valeurs["numero"])
            colonnes_b = st.columns(3)
            budget = colonnes_b[0].number_input(
                "Budget (jours)", min_value=0.0, value=valeurs["budget"], step=1.0
            )
            debut = colonnes_b[1].date_input("Début", value=valeurs["debut"])
            fin = colonnes_b[2].date_input("Fin", value=valeurs["fin"])
            statut = st.selectbox(
                "Statut", list(StatutProjet),
                index=list(StatutProjet).index(valeurs["statut"]),
                format_func=str,
            )
            if avertissement:
                st.warning(avertissement)
            forcer = st.checkbox("Clôturer malgré tout", value=False)
            enregistrer = st.form_submit_button("Enregistrer")

        if enregistrer:
            with get_session() as session:
                _, erreurs = modifier_projet(
                    session, auteur_id, project_id, nom=nom, numero=numero,
                    budget_jours=Decimal(str(budget)), date_debut=debut, date_fin=fin,
                    statut=statut, forcer_cloture=forcer,
                )
            if not afficher_erreurs(erreurs):
                st.success("Projet mis à jour.")
                st.rerun()


def _allocations(auteur_id: int) -> None:
    with get_session() as session:
        experts = list(
            session.scalars(
                select(User).where(User.role == Role.EXPERT).order_by(User.nom)
            )
        )
        projets = list(session.scalars(select(Project).order_by(Project.nom)))
        allocations = list(session.scalars(select(Allocation)))
        noms_experts = {u.id: u.nom for u in session.scalars(select(User))}
        noms_projets = {p.id: p.nom for p in projets}
        tableau(
            [
                {
                    "Expert": noms_experts.get(a.user_id, f"#{a.user_id}"),
                    "Projet": noms_projets.get(a.project_id, f"#{a.project_id}"),
                    "Jours alloués": nombre(a.jours_alloues),
                    "id": a.id,
                }
                for a in allocations
            ],
            vide="Aucune allocation : aucun expert ne peut encore saisir.",
        )
        choix_experts = {u.nom: u.id for u in experts}
        choix_projets = {p.nom: p.id for p in projets}
        choix_alloc = {
            f"{noms_experts.get(a.user_id)} / {noms_projets.get(a.project_id)}": a.id
            for a in allocations
        }

    if not choix_experts or not choix_projets:
        st.info("Créez au moins un expert et un projet pour définir des allocations.")
        return

    with st.form("allocation"):
        colonnes = st.columns(3)
        expert = colonnes[0].selectbox("Expert", list(choix_experts))
        projet = colonnes[1].selectbox("Projet", list(choix_projets))
        jours = colonnes[2].number_input("Jours alloués", min_value=0.0, value=0.0, step=1.0)
        valider = st.form_submit_button("Définir l'allocation")
    if valider:
        with get_session() as session:
            _, erreurs = definir_allocation(
                session, auteur_id, choix_experts[expert], choix_projets[projet],
                Decimal(str(jours)),
            )
        if not afficher_erreurs(erreurs):
            st.success("Allocation enregistrée.")
            st.rerun()

    if choix_alloc:
        libelle = st.selectbox("Allocation à supprimer", list(choix_alloc), key="alloc_del")
        if st.button("Supprimer l'allocation"):
            with get_session() as session:
                erreurs = supprimer_allocation(session, auteur_id, choix_alloc[libelle])
            if not afficher_erreurs(erreurs):
                st.success("Allocation supprimée.")
                st.rerun()


def _livrables(auteur_id: int) -> None:
    with get_session() as session:
        projets = list(session.scalars(select(Project).order_by(Project.nom)))
        choix_projets = {p.nom: p.id for p in projets}
    if not choix_projets:
        st.info("Créez un projet d'abord.")
        return

    libelle = st.selectbox("Projet", list(choix_projets), key="livrables_projet")
    project_id = choix_projets[libelle]
    with get_session() as session:
        livrables = livrables_projet(session, project_id)
        tableau(
            [
                {
                    "Livrable": d.intitule,
                    "Statut": str(d.statut),
                    "Échéance": d.echeance,
                    "id": d.id,
                }
                for d in livrables
            ],
            vide="Aucun livrable pour ce projet.",
        )
        choix_livrables = {d.intitule: d.id for d in livrables}

    with st.form(f"creation_livrable_{project_id}"):
        colonnes = st.columns(3)
        intitule = colonnes[0].text_input("Intitulé")
        statut = colonnes[1].selectbox("Statut", list(StatutLivrable), format_func=str)
        echeance = colonnes[2].date_input("Échéance", value=None)
        valider = st.form_submit_button("Ajouter le livrable")
    if valider:
        with get_session() as session:
            _, erreurs = creer_livrable(session, auteur_id, project_id, intitule, statut, echeance)
        if not afficher_erreurs(erreurs):
            st.success("Livrable ajouté.")
            st.rerun()

    if choix_livrables:
        with st.expander("Modifier un livrable"):
            cible = st.selectbox("Livrable", list(choix_livrables), key=f"liv_edit_{project_id}")
            deliverable_id = choix_livrables[cible]
            colonnes = st.columns(3)
            nouveau_statut = colonnes[0].selectbox(
                "Nouveau statut", list(StatutLivrable), format_func=str,
                key=f"liv_statut_{deliverable_id}",
            )
            nouvelle_echeance = colonnes[1].date_input(
                "Nouvelle échéance", value=None, key=f"liv_ech_{deliverable_id}"
            )
            if colonnes[2].button("Appliquer", key=f"liv_apply_{deliverable_id}"):
                champs = {"statut": nouveau_statut}
                if nouvelle_echeance:
                    champs["echeance"] = nouvelle_echeance
                with get_session() as session:
                    _, erreurs = modifier_livrable(session, auteur_id, deliverable_id, **champs)
                if not afficher_erreurs(erreurs):
                    st.success("Livrable mis à jour.")
                    st.rerun()
