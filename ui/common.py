"""Fonctions d'affichage partagées par les écrans Streamlit."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from io import BytesIO
from typing import Iterable

import pandas as pd
import streamlit as st

from core.pdf import ConversionPdfIndisponible, xlsx_vers_pdf

MIME_XLSX = "application/vnd.openpyxlformats-officedocument.spreadsheetml.sheet"
MIME_PDF = "application/pdf"

COULEURS_STATUT = {
    "OK": "#2E7D32",
    "Alerte": "#E8833A",
    "Critique": "#C62828",
    "Épuisé": "#7B1010",
}


def usd(montant: Decimal | float | int | None) -> str:
    """Formate un montant en USD : `$1,234.50`."""
    if montant is None:
        return "—"
    return f"${Decimal(str(montant)):,.2f}"


def nombre(valeur: Decimal | float | int | None, decimales: int = 2) -> str:
    if valeur is None:
        return "—"
    return f"{Decimal(str(valeur)):,.{decimales}f}"


def afficher_erreurs(erreurs: Iterable[str]) -> bool:
    """Affiche une liste d'erreurs. Renvoie `True` s'il y en avait."""
    erreurs = list(erreurs)
    for erreur in erreurs:
        st.error(erreur)
    return bool(erreurs)


def tableau(donnees: list[dict], vide: str = "Aucune donnée.") -> None:
    """Affiche un tableau, ou un message si la liste est vide."""
    if not donnees:
        st.info(vide)
        return
    st.dataframe(pd.DataFrame(donnees), use_container_width=True, hide_index=True)


def telechargements(
    flux_xlsx: BytesIO,
    nom_xlsx: str,
    proposer_pdf: bool = True,
    cle: str = "dl",
) -> None:
    """Boutons de téléchargement Excel et, si demandé, PDF."""
    octets = flux_xlsx.getvalue()
    colonnes = st.columns(2 if proposer_pdf else 1)
    colonnes[0].download_button(
        "Télécharger l'Excel",
        data=octets,
        file_name=nom_xlsx,
        mime=MIME_XLSX,
        key=f"{cle}_xlsx",
        use_container_width=True,
    )
    if not proposer_pdf:
        return
    nom_pdf = nom_xlsx.rsplit(".", 1)[0] + ".pdf"
    if colonnes[1].button("Préparer le PDF", key=f"{cle}_pdf_btn", use_container_width=True):
        try:
            with st.spinner("Conversion PDF par LibreOffice…"):
                st.session_state[f"{cle}_pdf"] = xlsx_vers_pdf(octets, nom_pdf[:-4]).getvalue()
        except ConversionPdfIndisponible as exc:
            st.warning(str(exc))
        except Exception as exc:  # noqa: BLE001 - message utilisateur
            st.error(f"Conversion PDF impossible : {exc}")
    if st.session_state.get(f"{cle}_pdf"):
        st.download_button(
            "Télécharger le PDF",
            data=st.session_state[f"{cle}_pdf"],
            file_name=nom_pdf,
            mime=MIME_PDF,
            key=f"{cle}_pdf_dl",
            use_container_width=True,
        )


def selecteur_mois(cle: str, defaut: date | None = None) -> tuple[int, int]:
    """Sélecteur année / mois, mois courant par défaut."""
    reference = defaut or date.today()
    colonnes = st.columns(2)
    annee = colonnes[0].number_input(
        "Année", min_value=2020, max_value=2100, value=reference.year, step=1, key=f"{cle}_annee"
    )
    mois = colonnes[1].selectbox(
        "Mois",
        list(range(1, 13)),
        index=reference.month - 1,
        format_func=lambda m: f"{m:02d}",
        key=f"{cle}_mois",
    )
    return int(annee), int(mois)


def badge_statut(statut: str) -> str:
    """Pastille colorée doublée du libellé — la couleur seule ne porte pas le sens."""
    couleur = COULEURS_STATUT.get(statut, "#555555")
    return f"<span style='color:{couleur};font-weight:600'>● {statut}</span>"
