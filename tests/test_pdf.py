"""Conversion PDF — vérifie que LibreOffice recalcule bien les formules."""
from __future__ import annotations

import re
import shutil
import subprocess

import pytest

from core.pdf import libreoffice_disponible, xlsx_vers_pdf

besoin_libreoffice = pytest.mark.skipif(
    not libreoffice_disponible(), reason="LibreOffice (soffice) absent de la machine"
)
besoin_pdftotext = pytest.mark.skipif(
    shutil.which("pdftotext") is None, reason="pdftotext absent de la machine"
)


def texte_du_pdf(octets: bytes, tmp_path) -> str:
    chemin = tmp_path / "doc.pdf"
    chemin.write_bytes(octets)
    return subprocess.run(
        ["pdftotext", "-layout", str(chemin), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


@besoin_libreoffice
def test_timesheet_en_pdf(db, jeu, entrees, tmp_path):
    from core.timesheet_export import generer_timesheet

    with db.get_session() as session:
        flux, nom = generer_timesheet(session, jeu["expert"], 2026, 10)
    pdf = xlsx_vers_pdf(flux, nom.rsplit(".", 1)[0])
    assert pdf.getvalue().startswith(b"%PDF")


@besoin_libreoffice
@besoin_pdftotext
def test_le_pdf_du_timesheet_recalcule_le_total(db, jeu, entrees, tmp_path):
    from core.timesheet_export import generer_timesheet, total_heures_attendu

    with db.get_session() as session:
        flux, nom = generer_timesheet(session, jeu["expert"], 2026, 10)
        attendu = total_heures_attendu(session, jeu["expert"], 2026, 10)
    texte = texte_du_pdf(xlsx_vers_pdf(flux, "ts").getvalue(), tmp_path)
    assert "Jane Doe" in texte
    assert "October 2026" in texte
    assert "TOTAL HOURS" in texte
    # 31.00 est écrit « 31 » par Excel/LibreOffice au format General.
    assert re.search(rf"\b{int(attendu)}\b", texte)


@besoin_libreoffice
@besoin_pdftotext
def test_le_pdf_de_la_facture_porte_les_bons_totaux(db, jeu, brouillon, tmp_path):
    """Contrôle de bout en bout des trois correctifs du modèle."""
    from core.invoice_export import generer_facture
    from core.invoice_service import ajouter_odc, emettre

    with db.get_session() as session:
        ajouter_odc(
            session, jeu["expert"], brouillon, "Education Reform Study", "Airfare",
            3, "50",
        )
    with db.get_session() as session:
        facture, erreurs = emettre(session, jeu["expert"], brouillon)
        assert not erreurs, erreurs
    with db.get_session() as session:
        flux, nom = generer_facture(session, brouillon)
    texte = texte_du_pdf(xlsx_vers_pdf(flux, "inv").getvalue(), tmp_path)

    # Hours affiche la quantité réelle, pas son arrondi entier.
    assert "7.5" in texte
    # ODC : Amount = 3 x 50, et le sous-total ODC n'est pas celui du LABOR.
    assert "$150.00" in texte
    assert "$3,100.00" in texte  # sous-total LABOR
    # Total = 3 100 + 150 ; total net = 3 250 - 250 d'avance.
    assert "$3,250.00" in texte
    assert "$3,000.00" in texte
    assert "Thank you for your business!" in texte
