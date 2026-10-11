"""Compte courant : changement de mot de passe par l'utilisateur lui-même."""
from __future__ import annotations

import streamlit as st

from core.auth import changer_mot_de_passe, current_user
from core.db import get_session
from core.security import LONGUEUR_MDP_MIN
from ui.common import afficher_erreurs


def afficher() -> None:
    utilisateur = current_user()
    if utilisateur is None:
        st.error("Accès non autorisé.")
        st.stop()
    st.header("Mon compte")
    st.write(f"**{utilisateur.nom}** — {utilisateur.email} · rôle : `{utilisateur.role}`")
    formulaire_mot_de_passe(force=False)


def formulaire_mot_de_passe(force: bool) -> None:
    """Formulaire de changement de mot de passe.

    `force=True` est utilisé par le gate quand `must_change_pwd` est posé :
    aucun autre écran n'est alors accessible.
    """
    utilisateur = current_user()
    if utilisateur is None:
        return
    if force:
        st.warning(
            "Votre mot de passe doit être changé avant d'accéder à l'application."
        )
    st.subheader("Changer mon mot de passe")
    st.caption(f"Au moins {LONGUEUR_MDP_MIN} caractères, dont une lettre et un chiffre.")
    with st.form("changement_mdp"):
        ancien = st.text_input("Mot de passe actuel", type="password")
        nouveau = st.text_input("Nouveau mot de passe", type="password")
        confirmation = st.text_input("Confirmation", type="password")
        valider = st.form_submit_button("Changer le mot de passe")

    if not valider:
        return
    if nouveau != confirmation:
        st.error("La confirmation ne correspond pas au nouveau mot de passe.")
        return
    with get_session() as session:
        erreurs = changer_mot_de_passe(session, utilisateur.id, ancien, nouveau)
    if afficher_erreurs(erreurs):
        return
    st.success("Mot de passe changé.")
    # L'identité en session porte must_change_pwd : on la rafraîchit.
    from dataclasses import replace

    st.session_state["user"] = replace(utilisateur, must_change_pwd=False)
    st.rerun()
