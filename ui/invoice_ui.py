"""M5 — Écran de facturation : brouillon, émission, téléchargements."""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO

import streamlit as st

from core.auth import UtilisateurConnecte, require_action
from core.db import get_session
from core.enums import StatutFacture
from core.invoice_export import generer_facture
from core.invoice_service import (
    ajouter_odc,
    annuler_brouillon,
    attacher_entrees,
    creer_brouillon,
    definir_avance,
    detacher_entrees,
    emettre,
    entrees_facturables,
    lignes_labor_brouillon,
    lister_factures,
    marquer_payee,
    prochain_numero,
    supprimer_odc,
)
from core.models import Invoice
from ui.common import afficher_erreurs, nombre, tableau, telechargements, usd
from ui.timesheet_ui import expert_cible


def afficher() -> None:
    utilisateur = require_action("generer_documents")
    st.header("Facturation")
    user_id = expert_cible(utilisateur)
    if user_id is None:
        return

    onglets = st.tabs(["Brouillons", "Nouvelle facture", "Factures émises"])
    with onglets[0]:
        _brouillons(utilisateur, user_id)
    with onglets[1]:
        _nouvelle(utilisateur, user_id)
    with onglets[2]:
        _emises(utilisateur, user_id)


def _nouvelle(utilisateur: UtilisateurConnecte, user_id: int) -> None:
    aujourdhui = date.today()
    colonnes = st.columns(2)
    debut = colonnes[0].date_input(
        "Début de période", value=aujourdhui.replace(day=1), key="inv_debut"
    )
    fin = colonnes[1].date_input("Fin de période", value=aujourdhui, key="inv_fin")

    with get_session() as session:
        candidates = entrees_facturables(session, user_id, debut, fin)
        apercu = [
            {
                "id": e.id,
                "Date": e.date_entry,
                "Projet": e.project.nom,
                "Livrable / note": (
                    e.deliverable.intitule if e.deliverable else (e.note_livrable or "")
                ),
                "Quantité": float(e.quantite),
                "Unité": str(e.unite),
                "Taux": usd(e.taux_applique),
                "Montant": usd(e.montant),
            }
            for e in candidates
        ]
        numero_prevu = prochain_numero(session, user_id, (debut or aujourdhui).year)

    st.caption(
        "Seules apparaissent les entrées **facturables** et non encore rattachées "
        "à une facture. Une ligne LABOR est produite par entrée, sans regroupement."
    )
    tableau(apercu, vide="Aucune entrée facturable sur cette période.")
    if not candidates:
        return

    st.caption(f"Numéro qui serait attribué à l'émission : `{numero_prevu}`")
    choix = {
        f"#{e.id} — {e.date_entry} · {e.project.nom} · {e.quantite} {e.unite}": e.id
        for e in candidates
    }
    retenues = st.multiselect(
        "Entrées à facturer", list(choix), default=list(choix), key="inv_select"
    )
    avance = st.number_input("Avance (USD)", min_value=0.0, value=0.0, step=50.0, key="inv_avance")

    if st.button("Créer le brouillon", type="primary", key="inv_create"):
        if not retenues:
            st.error("Sélectionnez au moins une entrée.")
            return
        with get_session() as session:
            facture, erreurs = creer_brouillon(
                session, utilisateur.id, user_id, debut, fin,
                [choix[libelle] for libelle in retenues], Decimal(str(avance)),
            )
        if not afficher_erreurs(erreurs):
            st.success(f"Brouillon #{facture.id} créé.")
            st.rerun()


def _brouillons(utilisateur: UtilisateurConnecte, user_id: int) -> None:
    with get_session() as session:
        brouillons = lister_factures(session, user_id, StatutFacture.BROUILLON)
        resume = {
            f.id: {
                "labor": Decimal(f.sous_total_labor),
                "odc": Decimal(f.sous_total_odc),
                "avance": Decimal(f.avance),
                "net": Decimal(f.total_net),
                "periode": (f.periode_debut, f.periode_fin),
            }
            for f in brouillons
        }
    if not brouillons:
        st.info("Aucun brouillon.")
        return

    choix = {
        f"#{f.id} — {resume[f.id]['periode'][0]} → {resume[f.id]['periode'][1]} "
        f"({usd(resume[f.id]['net'])})": f.id
        for f in brouillons
    }
    libelle = st.selectbox("Brouillon", list(choix), key="brouillon_select")
    invoice_id = choix[libelle]

    with get_session() as session:
        lignes = lignes_labor_brouillon(session, invoice_id)
        facture = session.get(Invoice, invoice_id)
        odc = [
            {
                "id": o.id,
                "Item": o.item,
                "Projet": o.projet,
                "ODC": o.odc,
                "Units": float(o.units),
                "Unit cost": usd(o.unit_cost),
                "Montant": usd(o.montant),
            }
            for o in sorted(facture.odc_lines, key=lambda x: x.item)
        ]
        totaux = resume[invoice_id]

    st.subheader("LABOR")
    tableau(
        [
            {
                "Item": l["item"],
                "Date": l["date_entry"],
                "Projet": l["projet"],
                "Deliverables / Output": l["deliverable_output"],
                "Quantité": float(l["quantite"]),
                "Unité": l["unite"],
                "Rate": usd(l["taux"]),
                "Amount": usd(l["montant"]),
            }
            for l in lignes
        ],
        vide="Aucune entrée rattachée.",
    )

    st.subheader("Other Direct Costs")
    tableau(odc, vide="Aucune ligne ODC.")
    with st.expander("Ajouter une ligne ODC"):
        with st.form(f"odc_{invoice_id}"):
            colonnes = st.columns(4)
            projet = colonnes[0].text_input("Projet")
            libelle_odc = colonnes[1].text_input("ODC")
            units = colonnes[2].number_input("Units", min_value=0.0, value=1.0, step=1.0)
            unit_cost = colonnes[3].number_input("Unit cost (USD)", min_value=0.0, value=0.0, step=10.0)
            valider = st.form_submit_button("Ajouter")
        if valider:
            with get_session() as session:
                _, erreurs = ajouter_odc(
                    session, utilisateur.id, invoice_id, projet, libelle_odc,
                    Decimal(str(units)), Decimal(str(unit_cost)),
                )
            if not afficher_erreurs(erreurs):
                st.rerun()
    if odc:
        choix_odc = {f"#{o['id']} — {o['ODC']}": o["id"] for o in odc}
        colonnes_odc = st.columns([2, 1])
        cible = colonnes_odc[0].selectbox("Ligne ODC", list(choix_odc), key=f"odc_del_{invoice_id}")
        if colonnes_odc[1].button("Supprimer l'ODC", key=f"odc_del_btn_{invoice_id}"):
            with get_session() as session:
                erreurs = supprimer_odc(session, utilisateur.id, choix_odc[cible])
            if not afficher_erreurs(erreurs):
                st.rerun()

    st.subheader("Totaux")
    colonnes_totaux = st.columns(4)
    colonnes_totaux[0].metric("Sous-total LABOR", usd(totaux["labor"]))
    colonnes_totaux[1].metric("Sous-total ODC", usd(totaux["odc"]))
    colonnes_totaux[2].metric("Avance", usd(totaux["avance"]))
    colonnes_totaux[3].metric("Total net", usd(totaux["net"]))

    nouvelle_avance = st.number_input(
        "Avance (USD)", min_value=0.0, value=float(totaux["avance"]), step=50.0,
        key=f"avance_{invoice_id}",
    )
    if st.button("Mettre à jour l'avance", key=f"avance_btn_{invoice_id}"):
        with get_session() as session:
            erreurs = definir_avance(
                session, utilisateur.id, invoice_id, Decimal(str(nouvelle_avance))
            )
        if not afficher_erreurs(erreurs):
            st.rerun()

    if lignes:
        with st.expander("Détacher des entrées"):
            choix_lignes = {
                f"#{l['entry_id']} — {l['date_entry']} · {usd(l['montant'])}": l["entry_id"]
                for l in lignes
            }
            a_detacher = st.multiselect(
                "Entrées à détacher", list(choix_lignes), key=f"detach_{invoice_id}"
            )
            if st.button("Détacher", key=f"detach_btn_{invoice_id}") and a_detacher:
                with get_session() as session:
                    erreurs = detacher_entrees(
                        session, utilisateur.id, invoice_id,
                        [choix_lignes[libelle] for libelle in a_detacher],
                    )
                if not afficher_erreurs(erreurs):
                    st.rerun()

    st.divider()
    st.warning(
        "L'émission est **définitive** : numéro attribué, lignes figées, entrées "
        "verrouillées. Vérifiez les totaux avant de poursuivre."
    )
    colonnes_emission = st.columns(3)
    date_emission = colonnes_emission[0].date_input(
        "Date d'émission", value=date.today(), key=f"em_date_{invoice_id}"
    )
    date_echeance = colonnes_emission[1].date_input(
        "Échéance", value=date.today() + timedelta(days=30), key=f"em_ech_{invoice_id}"
    )
    confirmer = colonnes_emission[2].checkbox("Je confirme", key=f"em_ok_{invoice_id}")

    boutons = st.columns(2)
    if boutons[0].button("Émettre la facture", type="primary", key=f"em_btn_{invoice_id}"):
        if not confirmer:
            st.error("Cochez « Je confirme » pour émettre.")
        else:
            with get_session() as session:
                facture, erreurs = emettre(
                    session, utilisateur.id, invoice_id, date_emission, date_echeance
                )
            if not afficher_erreurs(erreurs):
                st.success(f"Facture émise : {facture.numero}")
                st.rerun()
    if boutons[1].button("Annuler le brouillon", key=f"cancel_{invoice_id}"):
        with get_session() as session:
            erreurs = annuler_brouillon(session, utilisateur.id, invoice_id)
        if not afficher_erreurs(erreurs):
            st.success("Brouillon annulé, entrées libérées.")
            st.rerun()

    if st.button("Aperçu Excel du brouillon", key=f"preview_{invoice_id}"):
        with get_session() as session:
            flux, nom = generer_facture(session, invoice_id)
        st.session_state[f"inv_preview_{invoice_id}"] = (flux.getvalue(), nom)
    apercu = st.session_state.get(f"inv_preview_{invoice_id}")
    if apercu:
        telechargements(BytesIO(apercu[0]), apercu[1], cle=f"prev_{invoice_id}")


def _emises(utilisateur: UtilisateurConnecte, user_id: int) -> None:
    with get_session() as session:
        factures = [
            f
            for f in lister_factures(session, user_id)
            if StatutFacture(f.statut) is not StatutFacture.BROUILLON
        ]
        lignes = [
            {
                "Numéro": f.numero,
                "Émission": f.date_emission,
                "Échéance": f.date_echeance,
                "Statut": str(f.statut),
                "LABOR": usd(f.sous_total_labor),
                "ODC": usd(f.sous_total_odc),
                "Avance": usd(f.avance),
                "Total net": usd(f.total_net),
            }
            for f in factures
        ]
        choix = {f"{f.numero} ({f.statut})": f.id for f in factures}

    tableau(lignes, vide="Aucune facture émise.")
    if not factures:
        return

    libelle = st.selectbox("Facture", list(choix), key="emise_select")
    invoice_id = choix[libelle]

    colonnes = st.columns(2)
    if colonnes[0].button("Générer les fichiers", key=f"gen_inv_{invoice_id}"):
        with get_session() as session:
            flux, nom = generer_facture(session, invoice_id)
        st.session_state[f"inv_files_{invoice_id}"] = (flux.getvalue(), nom)
    with get_session() as session:
        facture = session.get(Invoice, invoice_id)
        est_emise = StatutFacture(facture.statut) is StatutFacture.EMISE
    if est_emise and colonnes[1].button("Marquer payée", key=f"pay_{invoice_id}"):
        with get_session() as session:
            _, erreurs = marquer_payee(session, utilisateur.id, invoice_id)
        if not afficher_erreurs(erreurs):
            st.success("Facture marquée payée.")
            st.rerun()

    fichiers = st.session_state.get(f"inv_files_{invoice_id}")
    if fichiers:
        st.caption(
            "Le dépôt Tangerine demande la facture en PDF, accompagnée du PDF du "
            "timesheet et des reçus ODC."
        )
        telechargements(BytesIO(fichiers[0]), fichiers[1], cle=f"inv_{invoice_id}")
