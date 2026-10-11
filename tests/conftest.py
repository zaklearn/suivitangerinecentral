"""Fixtures communes : base SQLite jetable et jeu de données minimal.

Les tests tournent sur SQLite plutôt que sur MySQL pour rester exécutables
sans service externe. Le code de production ne contient aucune branche
spécifique à SQLite : seule l'URL change.
"""
from __future__ import annotations

import os
from datetime import date
from decimal import Decimal

import pytest


@pytest.fixture()
def db(tmp_path, monkeypatch):
    """Base vierge, amorcée, pour un test."""
    chemin = tmp_path / "test.db"
    monkeypatch.setenv("APP_DATABASE_URL", f"sqlite:///{chemin}")

    from core import db as module_db

    module_db.reset_engine()
    module_db.bootstrap()
    yield module_db
    module_db.reset_engine()


@pytest.fixture()
def session(db):
    """Session ouverte sur la base de test, commitée en sortie."""
    with db.get_session() as session:
        yield session


@pytest.fixture()
def jeu(db):
    """Un admin, deux experts, un deputy, deux projets, des allocations.

    Renvoie un dictionnaire d'identifiants, pour éviter de faire voyager des
    objets ORM entre sessions.
    """
    from core.auth import creer_utilisateur
    from core.config_service import creer_livrable, creer_projet, definir_allocation
    from core.enums import Role

    ids: dict = {}
    with db.get_session() as session:
        admin, _, erreurs = creer_utilisateur(
            session, None, "Admin Root", "admin@tc.org", Role.ADMIN,
            mot_de_passe="adminpass123",
        )
        assert not erreurs, erreurs
        expert, _, erreurs = creer_utilisateur(
            session, admin.id, "Jane Doe", "jane@tc.org", Role.EXPERT,
            mot_de_passe="janepass123",
            tjm_jour=Decimal("800"), tjm_heure=Decimal("100"),
            societe_nom="Doe Consulting LLC", societe_adresse="12 Elm Street",
            societe_ville_zip="Raleigh, NC 27601", societe_phone="+1 919 555 0101",
            societe_email="jane@doeconsulting.com",
        )
        assert not erreurs, erreurs
        autre, _, erreurs = creer_utilisateur(
            session, admin.id, "John Roe", "john@tc.org", Role.EXPERT,
            mot_de_passe="johnpass123",
            tjm_jour=Decimal("600"), tjm_heure=Decimal("75"),
        )
        assert not erreurs, erreurs
        deputy, _, erreurs = creer_utilisateur(
            session, admin.id, "Deputy Manager", "deputy@tc.org", Role.DEPUTY_MANAGER,
            mot_de_passe="deputypass123",
        )
        assert not erreurs, erreurs

        projet, erreurs = creer_projet(
            session, admin.id, nom="Education Reform Study", numero="TC-2026-01",
            budget_jours=Decimal("50"), date_debut=date(2026, 1, 1),
            date_fin=date(2026, 12, 31),
        )
        assert not erreurs, erreurs
        projet_b, erreurs = creer_projet(
            session, admin.id, nom="Proposal: Literacy Baseline", numero="PROP-77",
            budget_jours=Decimal("10"),
        )
        assert not erreurs, erreurs
        livrable, erreurs = creer_livrable(
            session, admin.id, projet.id, "Inception report", echeance=date(2026, 11, 30)
        )
        assert not erreurs, erreurs

        definir_allocation(session, admin.id, expert.id, projet.id, Decimal("20"))
        definir_allocation(session, admin.id, expert.id, projet_b.id, Decimal("4"))
        definir_allocation(session, admin.id, autre.id, projet.id, Decimal("10"))

        ids = {
            "admin": admin.id,
            "expert": expert.id,
            "autre": autre.id,
            "deputy": deputy.id,
            "projet": projet.id,
            "projet_b": projet_b.id,
            "livrable": livrable.id,
        }
    return ids


@pytest.fixture()
def entrees(db, jeu):
    """Trois entrées facturables de l'expert : 7,5 h · 2 j · 7,5 h."""
    from core.entries_service import creer_entree
    from core.enums import TypeActivite, Unite

    ids = []
    with db.get_session() as session:
        for index, (unite, quantite) in enumerate(
            [(Unite.HEURE, "7.5"), (Unite.JOUR, "2"), (Unite.HEURE, "7.5")]
        ):
            entree, erreurs = creer_entree(
                session,
                jeu["expert"],
                user_id=jeu["expert"],
                project_id=jeu["projet"],
                date_entry=date(2026, 10, index + 1),
                unite=unite,
                quantite=Decimal(quantite),
                type_activite=TypeActivite.FEDERAL,
                deliverable_id=jeu["livrable"] if index == 0 else None,
                note_livrable=f"Draft chapter {index + 1}",
            )
            assert not erreurs, erreurs
            ids.append(entree.id)
    return ids


@pytest.fixture()
def brouillon(db, jeu, entrees):
    """Un brouillon de facture portant les trois entrées, avance de 250 USD."""
    from core.invoice_service import creer_brouillon

    with db.get_session() as session:
        facture, erreurs = creer_brouillon(
            session, jeu["expert"], jeu["expert"], date(2026, 10, 1), date(2026, 10, 31),
            entrees, Decimal("250"),
        )
        assert not erreurs, erreurs
        return facture.id


@pytest.fixture()
def facture_emise(db, jeu, brouillon):
    """La facture précédente, émise le 31 octobre 2026."""
    from core.invoice_service import emettre

    with db.get_session() as session:
        facture, erreurs = emettre(session, jeu["expert"], brouillon, date(2026, 10, 31))
        assert not erreurs, erreurs
        return facture.id
