"""Énumérations partagées — les valeurs stockées en base sont les `value`."""
from __future__ import annotations

import enum


class StrEnum(str, enum.Enum):
    """Enum dont la valeur stockée en base est la chaîne."""

    def __str__(self) -> str:  # pragma: no cover - confort d'affichage
        return self.value


class Role(StrEnum):
    EXPERT = "expert"
    DEPUTY_MANAGER = "deputy_manager"
    ADMIN = "admin"


class Unite(StrEnum):
    JOUR = "jour"
    HEURE = "heure"


class TypeActivite(StrEnum):
    FEDERAL = "federal"
    NON_FEDERAL = "non_federal"
    ADMIN = "admin"
    BD = "bd"


class StatutProjet(StrEnum):
    ACTIF = "actif"
    SUSPENDU = "suspendu"
    CLOS = "clos"


class StatutLivrable(StrEnum):
    A_FAIRE = "a_faire"
    EN_COURS = "en_cours"
    LIVRE = "livre"


class StatutFacture(StrEnum):
    BROUILLON = "brouillon"
    EMISE = "emise"
    PAYEE = "payee"


class NiveauAlerte(StrEnum):
    ALERTE = "alerte"
    CRITIQUE = "critique"
    EPUISE = "epuise"


class StatutAlerte(StrEnum):
    OUVERTE = "ouverte"
    TRAITEE = "traitee"


class ModeNumerotation(StrEnum):
    """Forme du numéro de facture (M2 §2.4 / M5 §5.4).

    PAR_EXPERT  -> {prefixe}-{code_expert}-{AAAA}-{seq:03d}, une séquence par
                   expert et par année. Le code expert est indispensable :
                   sans lui, deux experts obtiennent le même numéro la même
                   année et la contrainte d'unicité de `invoices.numero` saute.
    GLOBALE     -> {prefixe}-{AAAA}-{seq:03d}, une seule séquence pour tous.
    """

    PAR_EXPERT = "par_expert"
    GLOBALE = "globale"
