"""Timesheet & Facturation — Tangerine Central, LLC.

Point d'entrée Streamlit : bootstrap de la base, porte d'accès (M1) puis
navigation restreinte par rôle. Aucun écran n'est rendu avant connexion, et
les panneaux non autorisés ne sont pas construits — pas seulement masqués.

Lancement : `streamlit run app.py`
"""
from __future__ import annotations

import streamlit as st

from core.auth import can, current_user, login_gate, logout_button
from core.db import bootstrap, health_check
from core.enums import Role
from ui import (
    account_ui,
    config_ui,
    dashboard_ui,
    integrity_ui,
    invoice_ui,
    supervision_ui,
    timesheet_ui,
    users_ui,
)

st.set_page_config(page_title="Timesheet & Facturation", page_icon="🍊", layout="wide")


@st.cache_resource(show_spinner="Initialisation de la base…")
def _initialiser() -> dict:
    """Crée les tables manquantes et sème la configuration. Une fois par process."""
    return bootstrap()


def main() -> None:
    try:
        rapport = _initialiser()
    except Exception as exc:  # noqa: BLE001 - message utilisateur
        st.error(
            "Connexion à la base impossible. Vérifiez la section `[mysql]` de "
            f".streamlit/secrets.toml.\n\nDétail : {exc}"
        )
        st.stop()

    utilisateur = login_gate()
    if utilisateur is None:
        if rapport.get("admin_cree"):
            st.info(
                f"Compte administrateur initial créé : **{rapport['admin_email']}**. "
                "Le mot de passe devra être changé à la première connexion."
            )
        return

    # Mot de passe réinitialisé par un admin : rien d'autre n'est accessible.
    if utilisateur.must_change_pwd:
        st.sidebar.write(f"**{utilisateur.nom}**")
        logout_button()
        account_ui.formulaire_mot_de_passe(force=True)
        return

    ecrans = _ecrans_autorises()
    st.sidebar.write(f"**{utilisateur.nom}**")
    st.sidebar.caption(f"{utilisateur.email} · {utilisateur.role}")
    choix = st.sidebar.radio("Navigation", list(ecrans), key="navigation")
    st.sidebar.divider()
    if not health_check():
        st.sidebar.error("Base de données injoignable.")
    logout_button()

    ecrans[choix]()


def _ecrans_autorises() -> dict:
    """Écrans accessibles au rôle courant, dans l'ordre d'usage."""
    utilisateur = current_user()
    ecrans: dict = {"Dashboard": dashboard_ui.afficher}
    if can("saisie_entries"):
        ecrans["Timesheet"] = timesheet_ui.afficher
    if can("generer_documents"):
        ecrans["Facturation"] = invoice_ui.afficher
    if can("supervision"):
        ecrans["Supervision"] = supervision_ui.afficher
    if can("administration"):
        ecrans["Configuration"] = config_ui.afficher
        ecrans["Utilisateurs"] = users_ui.afficher
        ecrans["Intégrité"] = integrity_ui.afficher
    ecrans["Mon compte"] = account_ui.afficher
    return ecrans


if __name__ == "__main__":
    main()
