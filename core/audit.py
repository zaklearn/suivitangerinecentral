"""Journalisation des actions dans `audit_log`.

Toute écriture métier passe par `journaliser()`. Le détail est stocké en JSON :
il ne doit jamais contenir de mot de passe, en clair comme haché.
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from core.models import AuditLog

CHAMPS_INTERDITS = {"password", "mot_de_passe", "mdp", "hash_mdp", "hash", "secret"}


def _nettoyer(valeur: Any) -> Any:
    """Rend le détail sérialisable en JSON et retire tout secret."""
    if isinstance(valeur, dict):
        return {
            cle: ("***" if str(cle).lower() in CHAMPS_INTERDITS else _nettoyer(val))
            for cle, val in valeur.items()
        }
    if isinstance(valeur, (list, tuple)):
        return [_nettoyer(v) for v in valeur]
    if isinstance(valeur, Decimal):
        return str(valeur)
    if isinstance(valeur, (date, datetime)):
        return valeur.isoformat()
    if isinstance(valeur, (str, int, float, bool)) or valeur is None:
        return valeur
    return str(valeur)


def journaliser(
    session: Session,
    user_id: int | None,
    action: str,
    entity: str | None = None,
    entity_id: int | None = None,
    detail: dict | None = None,
) -> AuditLog:
    """Ajoute une ligne d'audit à la session courante (pas de commit ici)."""
    ligne = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        detail=_nettoyer(detail) if detail else None,
    )
    session.add(ligne)
    return ligne
