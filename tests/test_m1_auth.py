"""M1 — critères d'acceptation : gate, cloisonnement, rôles, mots de passe."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from core.auth import (
    MATRICE,
    UtilisateurConnecte,
    authentifier,
    changer_mot_de_passe,
    creer_utilisateur,
    desactiver_utilisateur,
    peut,
    perimetre_user_id,
    reinitialiser_mot_de_passe,
)
from core.enums import Role
from core.models import AuditLog, User
from core.security import hash_password, verify_password
from sqlalchemy import select


def test_matrice_de_permissions(db):
    """La matrice reproduit exactement le tableau du cahier des charges."""
    attendu = {
        "saisie_entries": {Role.EXPERT, Role.ADMIN},
        "generer_documents": {Role.EXPERT, Role.ADMIN},
        "supervision": {Role.DEPUTY_MANAGER, Role.ADMIN},
        "administration": {Role.ADMIN},
        "lecture_transversale": {Role.DEPUTY_MANAGER, Role.ADMIN},
    }
    assert MATRICE == attendu
    assert peut(Role.DEPUTY_MANAGER, "saisie_entries") is False
    assert peut(Role.EXPERT, "administration") is False
    assert peut(None, "supervision") is False


def test_action_inconnue_leve(db):
    with pytest.raises(KeyError):
        peut(Role.ADMIN, "action_inexistante")


def test_mot_de_passe_stocke_hache(db, jeu):
    with db.get_session() as session:
        expert = session.get(User, jeu["expert"])
        assert expert.hash_mdp != "janepass123"
        assert expert.hash_mdp.startswith("$2b$12$")
        assert verify_password("janepass123", expert.hash_mdp)


def test_authentification_et_journalisation(db, jeu):
    with db.get_session() as session:
        utilisateur = authentifier(session, "jane@tc.org", "janepass123")
        assert utilisateur is not None
        assert utilisateur.role is Role.EXPERT
    with db.get_session() as session:
        logs = list(session.scalars(select(AuditLog).where(AuditLog.action == "login")))
        assert len(logs) == 1
        assert logs[0].user_id == jeu["expert"]


def test_authentification_insensible_a_la_casse_de_l_email(db, jeu):
    with db.get_session() as session:
        assert authentifier(session, "  JANE@TC.ORG ", "janepass123") is not None


@pytest.mark.parametrize(
    ("email", "mot_de_passe"),
    [
        ("jane@tc.org", "mauvais"),
        ("inconnu@tc.org", "janepass123"),
        ("jane@tc.org", ""),
    ],
)
def test_authentification_echoue_sans_distinction(db, jeu, email, mot_de_passe):
    """Aucun cas d'échec ne révèle si l'email existe."""
    with db.get_session() as session:
        assert authentifier(session, email, mot_de_passe) is None


def test_compte_desactive_ne_peut_plus_se_connecter(db, jeu):
    with db.get_session() as session:
        erreurs = desactiver_utilisateur(session, jeu["admin"], jeu["expert"])
        assert not erreurs
    with db.get_session() as session:
        assert authentifier(session, "jane@tc.org", "janepass123") is None


def test_dernier_admin_non_desactivable(db, jeu):
    with db.get_session() as session:
        erreurs = desactiver_utilisateur(session, jeu["expert"], jeu["admin"])
        assert erreurs and "dernier administrateur" in erreurs[0]


def test_admin_ne_se_desactive_pas_lui_meme(db, jeu):
    with db.get_session() as session:
        erreurs = desactiver_utilisateur(session, jeu["admin"], jeu["admin"])
        assert erreurs and "votre propre compte" in erreurs[0].lower()


def test_cloisonnement_perimetre(db, jeu):
    expert = UtilisateurConnecte(jeu["expert"], "Jane", "jane@tc.org", Role.EXPERT)
    deputy = UtilisateurConnecte(jeu["deputy"], "Deputy", "d@tc.org", Role.DEPUTY_MANAGER)
    admin = UtilisateurConnecte(jeu["admin"], "Admin", "a@tc.org", Role.ADMIN)
    assert perimetre_user_id(expert) == jeu["expert"]
    assert perimetre_user_id(deputy) is None
    assert perimetre_user_id(admin) is None
    with pytest.raises(PermissionError):
        perimetre_user_id(None)


def test_un_expert_ne_charge_que_ses_entrees(db, jeu, entrees):
    """Le filtre de cloisonnement s'applique au niveau de la requête."""
    from core.entries_service import creer_entree, lister_entrees
    from core.enums import TypeActivite, Unite

    with db.get_session() as session:
        creer_entree(
            session, jeu["autre"], jeu["autre"], jeu["projet"], date(2026, 10, 9),
            Unite.HEURE, Decimal("3"), TypeActivite.FEDERAL,
        )

    expert = UtilisateurConnecte(jeu["expert"], "Jane", "jane@tc.org", Role.EXPERT)
    with db.get_session() as session:
        siennes = lister_entrees(session, user_id=perimetre_user_id(expert))
        toutes = lister_entrees(session, user_id=None)
    assert {e.id for e in siennes} == set(entrees)
    assert len(toutes) == len(entrees) + 1


def test_reinitialisation_force_le_changement(db, jeu):
    with db.get_session() as session:
        temporaire, erreurs = reinitialiser_mot_de_passe(session, jeu["admin"], jeu["expert"])
        assert not erreurs
        assert temporaire
    with db.get_session() as session:
        expert = session.get(User, jeu["expert"])
        assert expert.must_change_pwd is True
        utilisateur = authentifier(session, "jane@tc.org", temporaire)
        assert utilisateur is not None
        assert utilisateur.must_change_pwd is True


def test_changement_de_mot_de_passe(db, jeu):
    with db.get_session() as session:
        assert changer_mot_de_passe(session, jeu["expert"], "faux", "nouveaupass1") == [
            "Mot de passe actuel incorrect."
        ]
        erreurs = changer_mot_de_passe(session, jeu["expert"], "janepass123", "court")
        assert erreurs and "10 caractères" in erreurs[0]
        erreurs = changer_mot_de_passe(session, jeu["expert"], "janepass123", "janepass123")
        assert erreurs and "différer" in erreurs[0]
        assert changer_mot_de_passe(session, jeu["expert"], "janepass123", "nouveaupass1") == []
    with db.get_session() as session:
        assert authentifier(session, "jane@tc.org", "nouveaupass1") is not None
        assert session.get(User, jeu["expert"]).must_change_pwd is False


def test_email_en_doublon_refuse(db, jeu):
    with db.get_session() as session:
        _, _, erreurs = creer_utilisateur(
            session, jeu["admin"], "Autre Jane", "JANE@tc.org", Role.EXPERT,
            mot_de_passe="autrepass123",
        )
        assert erreurs == ["Cet email est déjà utilisé."]


def test_mot_de_passe_trop_long_refuse(db):
    with pytest.raises(ValueError):
        hash_password("x" * 73)


def test_audit_ne_contient_aucun_secret(db, jeu):
    from core.audit import journaliser

    with db.get_session() as session:
        ligne = journaliser(
            session, jeu["admin"], "test", "users", jeu["expert"],
            {"email": "jane@tc.org", "password": "secret", "hash_mdp": "$2b$..."},
        )
        session.flush()
        assert ligne.detail["password"] == "***"
        assert ligne.detail["hash_mdp"] == "***"
        assert ligne.detail["email"] == "jane@tc.org"
