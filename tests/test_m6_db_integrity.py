"""M6 — critères d'acceptation : bootstrap, snapshots, intégrité."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from core.entries_service import creer_entree
from core.enums import TypeActivite, Unite
from core.integrity import arrondi_money, calculer_consommation, verifier_integrite
from core.models import Config, Entry, Invoice


def test_bootstrap_idempotent(db):
    """Deux appels n'ajoutent ni config ni admin en double."""
    premier = db.bootstrap()
    second = db.bootstrap()
    assert premier["config_creee"] is False  # déjà créée par la fixture
    assert second["config_creee"] is False
    with db.get_session() as session:
        assert session.get(Config, 1) is not None


def test_health_check(db):
    assert db.health_check() is True


def test_entree_jour_fige_taux_et_heures_par_jour(db, jeu):
    """Une entrée en jours fige le TJM et la conversion jours → heures."""
    with db.get_session() as session:
        entree, erreurs = creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 1),
            Unite.JOUR, Decimal("2"), TypeActivite.FEDERAL,
        )
        assert not erreurs, erreurs
        assert entree.taux_applique == Decimal("800")
        assert entree.heures_par_jour_snap == Decimal("8")
        assert entree.montant == Decimal("1600.00")
        assert entree.heures_timesheet == Decimal("16")


def test_entree_heure_sans_snapshot_heures(db, jeu):
    with db.get_session() as session:
        entree, erreurs = creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 2),
            Unite.HEURE, Decimal("7.5"), TypeActivite.FEDERAL,
        )
        assert not erreurs, erreurs
        assert entree.taux_applique == Decimal("100")
        assert entree.heures_par_jour_snap is None
        assert entree.montant == Decimal("750.00")
        assert entree.heures_timesheet == Decimal("7.5")


def test_snapshots_survivent_au_changement_de_config(db, jeu):
    """Changer heures_par_jour et le TJM ne retouche aucune entrée existante."""
    from core.config_service import maj_parametres
    from core.auth import modifier_utilisateur

    with db.get_session() as session:
        entree, _ = creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 3),
            Unite.JOUR, Decimal("1"), TypeActivite.FEDERAL,
        )
        entry_id = entree.id

    with db.get_session() as session:
        maj_parametres(
            session, jeu["admin"], heures_par_jour=Decimal("6"),
            seuil_alerte_pct=80, seuil_critique_pct=95, prefixe_facture="TC",
        )
        modifier_utilisateur(
            session, jeu["admin"], jeu["expert"], tjm_jour=Decimal("1200")
        )

    with db.get_session() as session:
        entree = session.get(Entry, entry_id)
        assert entree.taux_applique == Decimal("800")
        assert entree.heures_par_jour_snap == Decimal("8")
        assert entree.montant == Decimal("800.00")
        assert entree.heures_timesheet == Decimal("8")


def test_integrite_detecte_et_repare_un_montant(db, jeu):
    """La règle 1 repère un montant incohérent et le recalcule."""
    with db.get_session() as session:
        entree, _ = creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 4),
            Unite.HEURE, Decimal("4"), TypeActivite.FEDERAL,
        )
        entry_id = entree.id

    with db.get_session() as session:
        session.get(Entry, entry_id).montant = Decimal("1.00")

    with db.get_session() as session:
        rapport = verifier_integrite(session, reparer=False)
        assert not rapport.ok
        assert any(a.regle == "1-montant" for a in rapport.anomalies)
        assert rapport.nb_reparees == 0

    with db.get_session() as session:
        rapport = verifier_integrite(session, reparer=True)
        assert rapport.nb_reparees >= 1

    with db.get_session() as session:
        assert session.get(Entry, entry_id).montant == Decimal("400.00")
        assert verifier_integrite(session).ok


def test_integrite_signale_un_total_de_facture_faux_sans_reparer(db, jeu, facture_emise):
    """Une facture émise est signalée, jamais réparée."""
    with db.get_session() as session:
        session.get(Invoice, facture_emise).total_net = Decimal("1.00")

    with db.get_session() as session:
        rapport = verifier_integrite(session, reparer=True)
        anomalies = [a for a in rapport.anomalies if a.regle == "4-totaux-facture"]
        assert anomalies
        assert all(not a.reparee for a in anomalies)
        assert session.get(Invoice, facture_emise).total_net == Decimal("1.00")


def test_invoice_labor_inchangee_apres_changement_de_tjm(db, jeu, facture_emise):
    """Le TJM peut changer : les lignes figées de la facture ne bougent pas."""
    from core.auth import modifier_utilisateur

    with db.get_session() as session:
        avant = [
            (l.item, Decimal(l.quantite), Decimal(l.taux), Decimal(l.montant))
            for l in session.get(Invoice, facture_emise).labor_lines
        ]
        assert avant

    with db.get_session() as session:
        modifier_utilisateur(session, jeu["admin"], jeu["expert"], tjm_heure=Decimal("999"))

    with db.get_session() as session:
        apres = [
            (l.item, Decimal(l.quantite), Decimal(l.taux), Decimal(l.montant))
            for l in session.get(Invoice, facture_emise).labor_lines
        ]
    assert apres == avant


def test_consommation_option_c(db, jeu):
    """Jours = quantité en jours + heures / heures_par_jour."""
    with db.get_session() as session:
        creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 5),
            Unite.JOUR, Decimal("2"), TypeActivite.FEDERAL,
        )
        creer_entree(
            session, jeu["expert"], jeu["expert"], jeu["projet"], date(2026, 10, 6),
            Unite.HEURE, Decimal("12"), TypeActivite.FEDERAL,
        )

    with db.get_session() as session:
        couples = calculer_consommation(session, user_id=jeu["expert"], project_id=jeu["projet"])
        assert len(couples) == 1
        couple = couples[0]
        # 2 jours + 12 h / 8 = 3,5 jours sur 20 alloués.
        assert couple.jours_consommes == Decimal("3.50")
        assert couple.jours_alloues == Decimal("20")
        assert couple.jours_restants == Decimal("16.50")
        assert couple.pct == Decimal("17.50")


def test_arrondi_money_half_up():
    assert arrondi_money(Decimal("1.005")) == Decimal("1.01")
    assert arrondi_money(Decimal("2.344")) == Decimal("2.34")
