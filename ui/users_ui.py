"""M1 — Écran d'administration des utilisateurs (TJM et bloc société inclus)."""
from __future__ import annotations

from decimal import Decimal

import streamlit as st
from sqlalchemy import select

from core.auth import (
    creer_utilisateur,
    desactiver_utilisateur,
    modifier_utilisateur,
    reinitialiser_mot_de_passe,
    require_action,
)
from core.config_service import valider_tjm
from core.db import get_session
from core.enums import Role
from core.models import User
from ui.common import afficher_erreurs, tableau, usd

LIBELLES_ROLE = {
    Role.EXPERT: "Expert",
    Role.DEPUTY_MANAGER: "Deputy manager",
    Role.ADMIN: "Administrateur",
}


def afficher() -> None:
    utilisateur = require_action("administration")
    st.header("Utilisateurs")
    st.caption(
        "Un compte n'est jamais supprimé : il est désactivé, pour conserver "
        "l'historique des entrées et des factures."
    )

    with get_session() as session:
        comptes = list(session.scalars(select(User).order_by(User.nom)))
        tableau(
            [
                {
                    "Nom": c.nom,
                    "Email": c.email,
                    "Rôle": LIBELLES_ROLE[Role(c.role)],
                    "TJM jour": usd(c.tjm_jour) if c.tjm_jour else "—",
                    "TJM heure": usd(c.tjm_heure) if c.tjm_heure else "—",
                    "Code facture": c.code_facture or "—",
                    "Actif": "oui" if c.actif else "non",
                    "Mdp à changer": "oui" if c.must_change_pwd else "non",
                }
                for c in comptes
            ],
            vide="Aucun utilisateur.",
        )
        choix = {f"{c.nom} ({c.email})": c.id for c in comptes}

    onglet_creation, onglet_edition = st.tabs(["Créer un compte", "Modifier un compte"])

    with onglet_creation:
        _formulaire_creation(utilisateur.id)

    with onglet_edition:
        if not choix:
            st.info("Aucun compte à modifier.")
        else:
            libelle = st.selectbox("Compte", list(choix), key="users_edit_select")
            _formulaire_edition(utilisateur.id, choix[libelle])


def _formulaire_creation(auteur_id: int) -> None:
    with st.form("creation_utilisateur"):
        colonnes = st.columns(2)
        nom = colonnes[0].text_input("Nom")
        email = colonnes[1].text_input("Email")
        role = st.selectbox(
            "Rôle", list(Role), format_func=lambda r: LIBELLES_ROLE[r], key="create_role"
        )
        colonnes_tjm = st.columns(2)
        tjm_jour = colonnes_tjm[0].text_input("TJM jour (USD)", value="")
        tjm_heure = colonnes_tjm[1].text_input("TJM heure (USD)", value="")
        st.caption(
            "Laisser le mot de passe vide génère un mot de passe temporaire, "
            "affiché une seule fois, avec changement forcé à la connexion."
        )
        mot_de_passe = st.text_input("Mot de passe (optionnel)", type="password")
        valider = st.form_submit_button("Créer le compte")

    if not valider:
        return
    erreurs = valider_tjm(tjm_jour, tjm_heure)
    if afficher_erreurs(erreurs):
        return
    with get_session() as session:
        compte, temporaire, erreurs = creer_utilisateur(
            session,
            auteur_id,
            nom,
            email,
            role,
            mot_de_passe or None,
            tjm_jour=Decimal(tjm_jour) if tjm_jour else None,
            tjm_heure=Decimal(tjm_heure) if tjm_heure else None,
        )
    if afficher_erreurs(erreurs):
        return
    st.success(f"Compte créé : {compte.nom}.")
    if temporaire:
        st.warning(
            f"Mot de passe temporaire : **{temporaire}** — transmettez-le par un "
            "canal sûr, il ne sera plus affiché."
        )


def _formulaire_edition(auteur_id: int, user_id: int) -> None:
    with get_session() as session:
        compte = session.get(User, user_id)
        if compte is None:
            st.error("Compte introuvable.")
            return
        valeurs = {
            "nom": compte.nom,
            "email": compte.email,
            "role": Role(compte.role),
            "tjm_jour": str(compte.tjm_jour or ""),
            "tjm_heure": str(compte.tjm_heure or ""),
            "code_facture": compte.code_facture or "",
            "societe_nom": compte.societe_nom or "",
            "societe_adresse": compte.societe_adresse or "",
            "societe_ville_zip": compte.societe_ville_zip or "",
            "societe_phone": compte.societe_phone or "",
            "societe_email": compte.societe_email or "",
            "actif": bool(compte.actif),
        }

    with st.form(f"edition_utilisateur_{user_id}"):
        colonnes = st.columns(2)
        nom = colonnes[0].text_input("Nom", value=valeurs["nom"])
        email = colonnes[1].text_input("Email", value=valeurs["email"])
        role = st.selectbox(
            "Rôle",
            list(Role),
            index=list(Role).index(valeurs["role"]),
            format_func=lambda r: LIBELLES_ROLE[r],
            key=f"edit_role_{user_id}",
        )
        st.markdown("**TJM (USD)** — le changement ne s'applique qu'aux futures saisies.")
        colonnes_tjm = st.columns(3)
        tjm_jour = colonnes_tjm[0].text_input("TJM jour", value=valeurs["tjm_jour"])
        tjm_heure = colonnes_tjm[1].text_input("TJM heure", value=valeurs["tjm_heure"])
        code_facture = colonnes_tjm[2].text_input(
            "Code facture", value=valeurs["code_facture"],
            help="Discriminant de la séquence de numéros de facture (ex. JD).",
        )
        st.markdown("**Bloc société** — imprimé en haut à droite de la facture.")
        societe_nom = st.text_input("Société", value=valeurs["societe_nom"])
        colonnes_societe = st.columns(2)
        societe_adresse = colonnes_societe[0].text_input("Adresse", value=valeurs["societe_adresse"])
        societe_ville_zip = colonnes_societe[1].text_input(
            "Ville, État, ZIP", value=valeurs["societe_ville_zip"]
        )
        colonnes_contact = st.columns(2)
        societe_phone = colonnes_contact[0].text_input("Téléphone", value=valeurs["societe_phone"])
        societe_email = colonnes_contact[1].text_input("Email société", value=valeurs["societe_email"])
        actif = st.checkbox("Compte actif", value=valeurs["actif"])
        enregistrer = st.form_submit_button("Enregistrer")

    if enregistrer:
        erreurs = valider_tjm(tjm_jour, tjm_heure)
        if not afficher_erreurs(erreurs):
            with get_session() as session:
                _, erreurs = modifier_utilisateur(
                    session,
                    auteur_id,
                    user_id,
                    nom=nom,
                    email=email,
                    role=role,
                    tjm_jour=Decimal(tjm_jour) if tjm_jour else None,
                    tjm_heure=Decimal(tjm_heure) if tjm_heure else None,
                    code_facture=code_facture.strip().upper() or None,
                    societe_nom=societe_nom or None,
                    societe_adresse=societe_adresse or None,
                    societe_ville_zip=societe_ville_zip or None,
                    societe_phone=societe_phone or None,
                    societe_email=societe_email or None,
                )
                if not erreurs and actif != valeurs["actif"]:
                    erreurs = desactiver_utilisateur(session, auteur_id, user_id, actif)
            if not afficher_erreurs(erreurs):
                st.success("Compte mis à jour.")
                st.rerun()

    if st.button("Réinitialiser le mot de passe", key=f"reset_{user_id}"):
        with get_session() as session:
            temporaire, erreurs = reinitialiser_mot_de_passe(session, auteur_id, user_id)
        if not afficher_erreurs(erreurs):
            st.warning(
                f"Nouveau mot de passe temporaire : **{temporaire}** — changement "
                "forcé à la prochaine connexion."
            )
