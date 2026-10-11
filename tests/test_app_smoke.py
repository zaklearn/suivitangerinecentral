"""L'application démarre, et la porte d'accès fait son travail.

Ces tests exécutent réellement `app.py` via le harnais de test de Streamlit :
une exception non rattrapée dans un écran les fait échouer.
"""
from __future__ import annotations

from pathlib import Path

import pytest

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest

DELAI = 60
APP = str(Path(__file__).resolve().parent.parent / "app.py")


@pytest.fixture()
def app(db, monkeypatch):
    """App lancée sur la base de test, cache de bootstrap vidé."""
    import streamlit as st

    st.cache_resource.clear()
    yield AppTest.from_file(APP, default_timeout=DELAI)
    st.cache_resource.clear()


def connecter(app: "AppTest", email: str, mot_de_passe: str) -> "AppTest":
    app.run()
    app.text_input[0].set_value(email)
    app.text_input[1].set_value(mot_de_passe)
    app.button[0].click().run()
    return app


def test_la_porte_bloque_sans_connexion(app):
    app.run()
    assert not app.exception
    # Seul le formulaire de connexion est rendu : aucune navigation.
    assert app.radio.values == []
    assert "Timesheet & Facturation" in [t.value for t in app.title]


def test_identifiants_invalides(app, jeu):
    connecter(app, "jane@tc.org", "mauvais")
    assert not app.exception
    assert any("Identifiants invalides" in e.value for e in app.error)
    assert app.radio.values == []


def test_expert_voit_ses_ecrans_et_pas_ceux_de_l_admin(app, jeu):
    connecter(app, "jane@tc.org", "janepass123")
    assert not app.exception
    ecrans = set(app.sidebar.radio[0].options)
    assert {"Dashboard", "Timesheet", "Facturation", "Mon compte"} <= ecrans
    assert "Configuration" not in ecrans
    assert "Utilisateurs" not in ecrans
    assert "Supervision" not in ecrans


def test_deputy_voit_la_supervision_et_pas_la_saisie(app, jeu):
    connecter(app, "deputy@tc.org", "deputypass123")
    assert not app.exception
    ecrans = set(app.sidebar.radio[0].options)
    assert {"Dashboard", "Supervision", "Mon compte"} <= ecrans
    assert "Timesheet" not in ecrans
    assert "Facturation" not in ecrans
    assert "Configuration" not in ecrans


def test_admin_voit_tout(app, jeu):
    connecter(app, "admin@tc.org", "adminpass123")
    assert not app.exception
    ecrans = set(app.sidebar.radio[0].options)
    assert {
        "Dashboard", "Timesheet", "Facturation", "Supervision",
        "Configuration", "Utilisateurs", "Intégrité", "Mon compte",
    } <= ecrans


@pytest.mark.parametrize(
    ("email", "mot_de_passe", "ecran"),
    [
        ("jane@tc.org", "janepass123", "Dashboard"),
        ("jane@tc.org", "janepass123", "Timesheet"),
        ("jane@tc.org", "janepass123", "Facturation"),
        ("jane@tc.org", "janepass123", "Mon compte"),
        ("deputy@tc.org", "deputypass123", "Supervision"),
        ("admin@tc.org", "adminpass123", "Configuration"),
        ("admin@tc.org", "adminpass123", "Utilisateurs"),
        ("admin@tc.org", "adminpass123", "Intégrité"),
    ],
)
def test_chaque_ecran_se_rend_sans_exception(app, jeu, entrees, email, mot_de_passe, ecran):
    connecter(app, email, mot_de_passe)
    assert not app.exception
    app.sidebar.radio[0].set_value(ecran).run()
    assert not app.exception, f"écran {ecran} : {app.exception}"


def test_mot_de_passe_reinitialise_bloque_la_navigation(app, jeu):
    """Tant que must_change_pwd est posé, aucun autre écran n'est accessible."""
    from core.auth import reinitialiser_mot_de_passe
    from core.db import get_session

    with get_session() as session:
        temporaire, erreurs = reinitialiser_mot_de_passe(session, jeu["admin"], jeu["expert"])
        assert not erreurs

    connecter(app, "jane@tc.org", temporaire)
    assert not app.exception
    assert app.sidebar.radio.values == []
    assert any("doit être changé" in w.value for w in app.warning)


def test_le_dashboard_affiche_les_donnees_de_l_expert(app, jeu, entrees):
    connecter(app, "jane@tc.org", "janepass123")
    app.sidebar.radio[0].set_value("Dashboard").run()
    assert not app.exception
    valeurs = {m.label: m.value for m in app.metric}
    assert valeurs["Entrées"] == "3"
    assert valeurs["Heures"] == "31.00"
