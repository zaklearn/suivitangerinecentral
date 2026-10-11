"""Conversion xlsx → pdf par LibreOffice headless.

LibreOffice reproduit la mise en page du classeur (zone d'impression,
ajustement à la page) beaucoup plus fidèlement qu'une reconstruction, ce qui
est exactement ce qu'on cherche pour le dépôt Tangerine.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path

DELAI_MAX_S = 120


class ConversionPdfIndisponible(RuntimeError):
    """LibreOffice est absent de la machine."""


def libreoffice_disponible() -> bool:
    return binaire_libreoffice() is not None


def binaire_libreoffice() -> str | None:
    for nom in ("soffice", "libreoffice"):
        chemin = shutil.which(nom)
        if chemin:
            return chemin
    return None


def xlsx_vers_pdf(contenu_xlsx: BytesIO | bytes, nom_base: str = "document") -> BytesIO:
    """Convertit un classeur en PDF et renvoie le flux résultant."""
    binaire = binaire_libreoffice()
    if binaire is None:
        raise ConversionPdfIndisponible(
            "LibreOffice (soffice) est introuvable : la génération PDF est "
            "indisponible sur cette machine. Le téléchargement Excel reste "
            "possible."
        )

    octets = contenu_xlsx.getvalue() if isinstance(contenu_xlsx, BytesIO) else contenu_xlsx
    with tempfile.TemporaryDirectory(prefix="xlsx2pdf-") as repertoire:
        base = Path(repertoire)
        source = base / f"{nom_base}.xlsx"
        source.write_bytes(octets)
        # Profil utilisateur dédié : deux conversions simultanées ne se
        # disputent pas le même profil LibreOffice.
        profil = base / "profil"
        resultat = subprocess.run(
            [
                binaire,
                f"-env:UserInstallation=file://{profil}",
                "--headless",
                "--norestore",
                "--convert-to",
                "pdf:calc_pdf_Export",
                "--outdir",
                str(base),
                str(source),
            ],
            capture_output=True,
            text=True,
            timeout=DELAI_MAX_S,
            check=False,
        )
        produit = base / f"{nom_base}.pdf"
        if not produit.exists():
            raise RuntimeError(
                "La conversion PDF a échoué.\n"
                f"sortie : {resultat.stdout.strip()}\nerreur : {resultat.stderr.strip()}"
            )
        return BytesIO(produit.read_bytes())
