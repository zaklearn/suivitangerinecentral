"""Hachage et vérification des mots de passe (M1).

bcrypt via passlib, coût 12. Aucun mot de passe en clair n'est stocké,
journalisé ou renvoyé. La comparaison passe par `CryptContext.verify`,
qui est à temps constant.
"""
from __future__ import annotations

import logging
import secrets
import string

from passlib.context import CryptContext

# passlib 1.7.x sonde `bcrypt.__about__`, absent depuis bcrypt 4.1 : l'échec est
# rattrapé en interne mais bruite les logs. On le tait, le backend fonctionne.
logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)

BCRYPT_ROUNDS = 12
LONGUEUR_MDP_MIN = 10

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=BCRYPT_ROUNDS
)


def hash_password(mot_de_passe: str) -> str:
    """Retourne le hash bcrypt d'un mot de passe."""
    if not mot_de_passe:
        raise ValueError("mot de passe vide")
    # bcrypt tronque silencieusement au-delà de 72 octets : on refuse plutôt
    # que d'accepter un mot de passe dont la fin ne compte pas.
    if len(mot_de_passe.encode("utf-8")) > 72:
        raise ValueError("mot de passe trop long (max 72 octets)")
    return pwd_context.hash(mot_de_passe)


def verify_password(mot_de_passe: str, hash_stocke: str | None) -> bool:
    """Vérifie un mot de passe contre son hash, à temps constant."""
    if not hash_stocke:
        return False
    try:
        return pwd_context.verify(mot_de_passe, hash_stocke)
    except ValueError:
        # Hash illisible ou tronqué en base : échec, sans détail à l'appelant.
        return False


def valider_robustesse(mot_de_passe: str) -> list[str]:
    """Liste les règles de robustesse non respectées (vide si conforme)."""
    erreurs: list[str] = []
    if len(mot_de_passe) < LONGUEUR_MDP_MIN:
        erreurs.append(f"au moins {LONGUEUR_MDP_MIN} caractères")
    if not any(c.isalpha() for c in mot_de_passe):
        erreurs.append("au moins une lettre")
    if not any(c.isdigit() for c in mot_de_passe):
        erreurs.append("au moins un chiffre")
    if len(mot_de_passe.encode("utf-8")) > 72:
        erreurs.append("72 octets au maximum")
    return erreurs


def generer_mot_de_passe_temporaire(longueur: int = 14) -> str:
    """Mot de passe temporaire conforme aux règles de robustesse."""
    alphabet = string.ascii_letters + string.digits
    while True:
        candidat = "".join(secrets.choice(alphabet) for _ in range(longueur))
        if not valider_robustesse(candidat):
            return candidat
