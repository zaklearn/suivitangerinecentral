"""M2 et M3 — configuration, allocations, saisie et verrouillage."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from core.config_service import (
    avertissement_cloture,
    creer_livrable,
    definir_allocation,
    maj_parametres,
    modifier_projet,
    projet_supprimable,
    projets_alloues,
    supprimer_allocation,
    valider_parametres,
    valider_projet,
    valider_tjm,
)
from core.entries_service import (
    calculer_totaux,
    creer_entree,
    dupliquer_entree,
    entree_verrouillee,
    lister_entrees,
    modifier_entree,
    supprimer_entree,
)
from core.enums import StatutProjet, TypeActivite, Unite
from core.models import Entry, User


# --------------------------------------------------------------------------- #
# M2
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("hpj", "alerte", "critique", "valide"),
    [
        (8, 80, 95, True),
        (7.5, 50, 100, True),
        (0, 80, 95, False),
        (25, 80, 95, False),
        (8, 95, 80, False),
        (8, 80, 101, False),
        (8, 80, 80, False),
    ],
)
def test_validation_parametres(db, hpj, alerte, critique, valide):
    assert (valider_parametres(hpj, alerte, critique) == []) is valide


def test_validation_tjm_et_projet(db):
    assert valider_tjm("800", "100") == []
    assert valider_tjm("-1", "100") != []
    assert valider_tjm("abc", None) != []
    assert valider_projet("P", 10, date(2026, 1, 1), date(2026, 12, 31)) == []
    assert valider_projet("", 10, None, None) != []
    assert valider_projet("P", -1, None, None) != []
    assert valider_projet("P", 10, date(2026, 12, 31), date(2026, 1, 1)) != []


def test_prefixe_facture_valide(db, jeu):
    with db.get_session() as session:
        _, erreurs = maj_parametres(
            session, jeu["admin"], seuil_alerte_pct=80, seuil_critique_pct=95,
            prefixe_facture="TC INVALID!",
        )
        assert erreurs


def test_allocation_rend_le_projet_disponible(db, jeu):
    with db.get_session() as session:
        disponibles = {p.id for p in projets_alloues(session, jeu["expert"])}
        assert disponibles == {jeu["projet"], jeu["projet_b"]}
        # John n'est alloué que sur le premier projet.
        assert {p.id for p in projets_alloues(session, jeu["autre"])} == {jeu["projet"]}


def test_allocation_unique_par_couple(db, jeu):
    with db.get_session() as session:
        allocation, erreurs = definir_allocation(
            session, jeu["admin"], jeu["expert"], jeu["projet"], Decimal("30")
        )
        assert not erreurs
        assert allocation.jours_alloues == Decimal("30")
        from core.models import Allocation
        from sqlalchemy import func, select

        nb = session.scalar(
            select(func.count()).select_from(Allocation).where(
                Allocation.user_id == jeu["expert"], Allocation.project_id == jeu["projet"]
            )
        )
        assert nb == 1


def test_allocation_non_supprimable_avec_entrees(db, jeu, entrees):
    from core.models import Allocation
    from sqlalchemy import select

    with db.get_session() as session:
        allocation = session.scalars(
            select(Allocation).where(
                Allocation.user_id == jeu["expert"], Allocation.project_id == jeu["projet"]
            )
        ).first()
        erreurs = supprimer_allocation(session, jeu["admin"], allocation.id)
        assert erreurs and "entrée" in erreurs[0]


def test_projet_avec_entrees_non_supprimable_mais_closable(db, jeu, entrees):
    with db.get_session() as session:
        assert projet_supprimable(session, jeu["projet"]) is False
        assert avertissement_cloture(session, jeu["projet"]) is not None
        _, erreurs = modifier_projet(
            session, jeu["admin"], jeu["projet"], statut=StatutProjet.CLOS
        )
        assert erreurs, "la clôture doit avertir tant que des entrées ne sont pas facturées"
        projet, erreurs = modifier_projet(
            session, jeu["admin"], jeu["projet"], statut=StatutProjet.CLOS,
            forcer_cloture=True,
        )
        assert not erreurs
        assert StatutProjet(projet.statut) is StatutProjet.CLOS


# --------------------------------------------------------------------------- #
# M3
# --------------------------------------------------------------------------- #
def test_projet_non_alloue_refuse(db, jeu):
    """Un expert ne peut saisir que sur un projet qui lui est alloué."""
    with db.get_session() as session:
        _, erreurs = creer_entree(
            session, jeu["autre"], jeu["autre"], jeu["projet_b"], date(2026, 10, 1),
            Unite.HEURE, Decimal("2"), TypeActivite.FEDERAL,
        )
        assert erreurs and "pas alloué" in erreurs[0]


def test_quantite_positive_obligatoire(db, jeu):
    with db.get_session() as session:
        for quantite in (Decimal("0"), Decimal("-1")):
            _, erreurs = creer_entree(
                session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 1),
                Unite.HEURE, quantite, TypeActivite.FEDERAL,
            )
            assert erreurs and "strictement positive" in erreurs[0]


def test_tjm_absent_bloque_la_saisie(db, jeu):
    from core.auth import modifier_utilisateur

    with db.get_session() as session:
        modifier_utilisateur(session, jeu["admin"], jeu["expert"], tjm_heure=None)
    with db.get_session() as session:
        _, erreurs = creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 1),
            Unite.HEURE, Decimal("2"), TypeActivite.FEDERAL,
        )
        assert erreurs and "définir le TJM" in erreurs[0]


def test_livrable_d_un_autre_projet_refuse(db, jeu):
    with db.get_session() as session:
        _, erreurs = creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet_b"], date(2026, 10, 1),
            Unite.HEURE, Decimal("2"), TypeActivite.FEDERAL,
            deliverable_id=jeu["livrable"],
        )
        assert erreurs and "n'appartient pas" in erreurs[0]


def test_edition_conserve_le_snapshot_sauf_demande(db, jeu, entrees):
    """Le taux figé n'est réécrit que si on le demande explicitement."""
    from core.auth import modifier_utilisateur

    entry_id = entrees[0]  # 7,5 h à 100 USD
    with db.get_session() as session:
        modifier_utilisateur(session, jeu["admin"], jeu["expert"], tjm_heure=Decimal("150"))

    with db.get_session() as session:
        entree, erreurs = modifier_entree(
            session, jeu["expert"], entry_id, quantite=Decimal("10")
        )
        assert not erreurs
        assert entree.taux_applique == Decimal("100")
        assert entree.montant == Decimal("1000.00")

    with db.get_session() as session:
        entree, erreurs = modifier_entree(
            session, jeu["expert"], entry_id, reappliquer_tjm=True
        )
        assert not erreurs
        assert entree.taux_applique == Decimal("150")
        assert entree.montant == Decimal("1500.00")


def test_changement_d_unite_reprend_le_tjm_et_le_snapshot(db, jeu, entrees):
    """Passer de l'heure au jour rend le taux horaire caduc : il est repris."""
    with db.get_session() as session:
        entree, erreurs = modifier_entree(
            session, jeu["expert"], entrees[0], unite=Unite.JOUR, quantite=Decimal("1")
        )
        assert not erreurs
        assert entree.taux_applique == Decimal("800")
        assert entree.heures_par_jour_snap == Decimal("8")
        assert entree.montant == Decimal("800.00")


def test_entree_facturee_ni_modifiable_ni_supprimable(db, jeu, facture_emise, entrees):
    with db.get_session() as session:
        entree = session.get(Entry, entrees[0])
        verrou = entree_verrouillee(session, entree)
        assert verrou and "détachez-la" in verrou

        _, erreurs = modifier_entree(session, jeu["expert"], entrees[0], quantite=Decimal("1"))
        assert erreurs and "détachez-la" in erreurs[0]

        erreurs = supprimer_entree(session, jeu["expert"], entrees[0])
        assert erreurs and "détachez-la" in erreurs[0]


def test_entree_en_brouillon_reste_modifiable(db, jeu, brouillon, entrees):
    """Rattachée à un brouillon, l'entrée reste modifiable et le total suit."""
    from core.models import Invoice

    with db.get_session() as session:
        entree = session.get(Entry, entrees[0])
        assert entree.invoice_id == brouillon
        assert entree_verrouillee(session, entree) is None

        _, erreurs = modifier_entree(
            session, jeu["expert"], entrees[0], quantite=Decimal("10")
        )
        assert not erreurs

    with db.get_session() as session:
        facture = session.get(Invoice, brouillon)
        # 10 h x 100 + 2 j x 800 + 7,5 h x 100 = 1000 + 1600 + 750
        assert facture.sous_total_labor == Decimal("3350.00")
        assert facture.total_net == Decimal("3100.00")  # moins l'avance de 250


def test_duplication(db, jeu, entrees):
    with db.get_session() as session:
        copie, erreurs = dupliquer_entree(
            session, jeu["expert"], entrees[0], date(2026, 11, 2)
        )
        assert not erreurs
        assert copie.id != entrees[0]
        assert copie.date_entry == date(2026, 11, 2)
        assert copie.quantite == Decimal("7.5")


def test_totaux_de_liste(db, jeu, entrees):
    with db.get_session() as session:
        liste = lister_entrees(session, user_id=jeu["expert"], annee=2026, mois=10)
        totaux = calculer_totaux(session, liste)
    # 7,5 h + 2 j (16 h) + 7,5 h = 31 h ; 31 / 8 = 3,875 jours
    assert totaux.nb_entrees == 3
    assert totaux.heures == Decimal("31.00")
    assert totaux.jours == Decimal("3.88")
    assert totaux.montant_facturable == Decimal("3100.00")
    assert totaux.montant_non_facturable == Decimal("0")


def test_filtre_par_mois_et_projet(db, jeu, entrees):
    with db.get_session() as session:
        creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet_b"], date(2026, 11, 5),
            Unite.HEURE, Decimal("4"), TypeActivite.BD,
        )
    with db.get_session() as session:
        assert len(lister_entrees(session, user_id=jeu["expert"], annee=2026, mois=10)) == 3
        assert len(lister_entrees(session, user_id=jeu["expert"], annee=2026, mois=11)) == 1
        assert (
            len(lister_entrees(session, user_id=jeu["expert"], project_id=jeu["projet_b"])) == 1
        )
