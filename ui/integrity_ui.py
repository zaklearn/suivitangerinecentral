"""M6 — Écran de contrôle d'intégrité, réservé à l'administrateur."""
from __future__ import annotations

import streamlit as st

from core.auth import require_action
from core.db import get_session, health_check
from core.integrity import verifier_integrite
from ui.common import nombre, tableau


def afficher() -> None:
    require_action("administration")
    st.header("Intégrité des données")
    st.caption(
        "Les cinq règles du cahier des charges. Les lignes d'une facture déjà "
        "émise sont signalées mais jamais réparées : une facture est un document "
        "émis, pas une donnée de travail."
    )
    st.metric("Connexion base", "OK" if health_check() else "indisponible")

    reparer = st.checkbox(
        "Réparer les écarts réparables", value=False,
        help="Recalcule les montants et totaux des entrées et brouillons concernés.",
    )
    if not st.button("Lancer le contrôle", type="primary"):
        return

    with get_session() as session:
        rapport = verifier_integrite(session, reparer=reparer)

    colonnes = st.columns(4)
    colonnes[0].metric("Entrées", rapport.nb_entries)
    colonnes[1].metric("Factures", rapport.nb_invoices)
    colonnes[2].metric("Anomalies", len(rapport.anomalies))
    colonnes[3].metric("Réparées", rapport.nb_reparees)

    if rapport.ok:
        st.success("Aucune anomalie détectée.")
    else:
        for regle, anomalies in sorted(rapport.par_regle().items()):
            st.subheader(f"Règle {regle} — {len(anomalies)} anomalie(s)")
            tableau(
                [
                    {
                        "Entité": a.entite,
                        "id": a.entite_id,
                        "Message": a.message,
                        "Réparée": "oui" if a.reparee else "non",
                    }
                    for a in anomalies
                ]
            )

    st.subheader("Consommation par couple (règle 5, option C)")
    tableau(
        [
            {
                "Expert": c.user_nom,
                "Projet": c.project_nom,
                "Alloués": nombre(c.jours_alloues),
                "Consommés": nombre(c.jours_consommes),
                "Restants": nombre(c.jours_restants),
                "%": nombre(c.pct),
            }
            for c in rapport.consommation
        ],
        vide="Aucune consommation enregistrée.",
    )
