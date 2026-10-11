"""Outils de remplissage de fichiers-modèles Excel (règle de fidélité n°5).

On ne reconstruit jamais un classeur : on ouvre le modèle d'origine et on y
écrit des valeurs. Les styles, polices, couleurs, bordures, fusions et largeurs
de colonnes restent ceux du modèle.

openpyxl déplace les hauteurs de ligne lors d'une insertion, mais **pas** les
plages fusionnées, les références de tableaux, la zone d'impression ni les
formules. Les fonctions ci-dessous comblent ces manques.
"""
from __future__ import annotations

import re
from collections.abc import Iterable
from copy import copy
from io import BytesIO
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def charger_modele(nom_fichier: str):
    """Ouvre un modèle depuis `templates/` — l'original n'est jamais écrit."""
    chemin = TEMPLATES_DIR / nom_fichier
    if not chemin.exists():
        raise FileNotFoundError(
            f"Modèle Excel absent : {chemin}. Les fichiers-modèles d'origine "
            "doivent rester dans templates/."
        )
    return load_workbook(chemin)


def vers_bytes(workbook) -> BytesIO:
    """Sérialise le classeur en mémoire, prêt pour `st.download_button`."""
    flux = BytesIO()
    workbook.save(flux)
    flux.seek(0)
    return flux


def copier_style(source: Cell, cible: Cell) -> None:
    """Recopie l'habillage d'une cellule (sans sa valeur)."""
    cible._style = copy(source._style)
    cible.number_format = source.number_format


def copier_style_ligne(
    ws: Worksheet, ligne_source: int, ligne_cible: int, col_min: int = 1, col_max: int | None = None
) -> None:
    """Recopie l'habillage d'une ligne entière sur une autre.

    Par défaut toute la largeur utilisée de la feuille, colonnes de marge
    comprises : ce sont elles qui portent le fond de page, et les omettre
    laisse des bandes blanches sur les lignes ajoutées.
    """
    if col_max is None:
        col_max = ws.max_column
    for col in range(col_min, col_max + 1):
        copier_style(ws.cell(row=ligne_source, column=col), ws.cell(row=ligne_cible, column=col))
    hauteur = ws.row_dimensions[ligne_source].height
    if hauteur:
        ws.row_dimensions[ligne_cible].height = hauteur


def decaler_fusions(ws: Worksheet, a_partir_de: int, nb_lignes: int) -> None:
    """Décale vers le bas les fusions situées à partir d'une ligne donnée.

    Les coordonnées des plages sont modifiées en place, sans passer par
    `unmerge_cells` / `merge_cells` : ces deux méthodes réécrivent les cellules
    de la plage, et effaceraient le contenu que `insert_rows` vient d'y
    déplacer.

    Une fusion qui enjambe la ligne d'insertion est étendue plutôt que
    déplacée, afin de ne pas couper un bloc en deux.
    """
    if nb_lignes <= 0:
        return
    for plage in list(ws.merged_cells.ranges):
        if plage.min_row >= a_partir_de:
            plage.shift(row_shift=nb_lignes)
        elif plage.max_row >= a_partir_de:
            plage.expand(down=nb_lignes)


def etendre_table(ws: Worksheet, nom_table: str, nb_lignes: int) -> None:
    """Étend la référence d'un tableau Excel de `nb_lignes` lignes."""
    if nb_lignes <= 0 or nom_table not in ws.tables:
        return
    table = ws.tables[nom_table]
    debut_col, debut_lig, fin_col, fin_lig = _bornes(table.ref)
    table.ref = _plage(debut_col, debut_lig, fin_col, fin_lig + nb_lignes)


def decaler_zone_impression(ws: Worksheet, a_partir_de: int, nb_lignes: int) -> None:
    """Étend la zone d'impression si l'insertion a lieu à l'intérieur."""
    if nb_lignes <= 0 or not ws.print_area:
        return
    nouvelles: list[str] = []
    for plage in ws.print_area if isinstance(ws.print_area, list) else [ws.print_area]:
        brute = plage.split("!")[-1].replace("$", "")
        try:
            debut_col, debut_lig, fin_col, fin_lig = _bornes(brute)
        except ValueError:
            nouvelles.append(plage)
            continue
        if fin_lig >= a_partir_de:
            fin_lig += nb_lignes
        nouvelles.append(
            f"${get_column_letter(debut_col)}${debut_lig}:"
            f"${get_column_letter(fin_col)}${fin_lig}"
        )
    ws.print_area = nouvelles


def inserer_lignes(
    ws: Worksheet,
    index: int,
    nb_lignes: int,
    ligne_modele: int,
    nom_table: str | None = None,
) -> None:
    """Insère `nb_lignes` lignes avant `index`, habillées comme `ligne_modele`.

    L'habillage est recopié sur toute la largeur de la feuille. Fusions,
    référence de tableau et zone d'impression sont ajustées. Les formules des
    blocs situés en dessous ne le sont pas : l'appelant les réécrit avec les
    nouveaux numéros de ligne.
    """
    if nb_lignes <= 0:
        return
    modele_apres_insertion = (
        ligne_modele + nb_lignes if ligne_modele >= index else ligne_modele
    )
    ws.insert_rows(index, nb_lignes)
    decaler_fusions(ws, index, nb_lignes)
    decaler_zone_impression(ws, index, nb_lignes)
    if nom_table:
        etendre_table(ws, nom_table, nb_lignes)
    largeur = ws.max_column
    for decalage in range(nb_lignes):
        copier_style_ligne(ws, modele_apres_insertion, index + decalage, 1, largeur)


def vider_cellules(ws: Worksheet, ligne: int, colonnes: Iterable[int]) -> None:
    """Vide les valeurs d'une ligne en conservant son habillage."""
    for col in colonnes:
        ws.cell(row=ligne, column=col).value = None


# --------------------------------------------------------------------------- #
# Utilitaires de plages
# --------------------------------------------------------------------------- #
_MOTIF_PLAGE = re.compile(r"^([A-Z]+)(\d+):([A-Z]+)(\d+)$")


def _bornes(plage: str) -> tuple[int, int, int, int]:
    """`"B15:G23"` → `(2, 15, 7, 23)`."""
    from openpyxl.utils import column_index_from_string

    correspondance = _MOTIF_PLAGE.match(plage.replace("$", "").upper())
    if correspondance is None:
        raise ValueError(f"plage non reconnue : {plage!r}")
    col_a, lig_a, col_b, lig_b = correspondance.groups()
    return (
        column_index_from_string(col_a),
        int(lig_a),
        column_index_from_string(col_b),
        int(lig_b),
    )


def _plage(debut_col: int, debut_lig: int, fin_col: int, fin_lig: int) -> str:
    return (
        f"{get_column_letter(debut_col)}{debut_lig}:"
        f"{get_column_letter(fin_col)}{fin_lig}"
    )
