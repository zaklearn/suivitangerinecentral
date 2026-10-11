"""M1 — Authentification et contrôle d'accès basé sur les rôles.

Deux niveaux volontairement séparés :

* les fonctions pures (`authentifier`, `peut`, `perimetre_user_id`, CRUD
  utilisateurs) ne connaissent pas Streamlit et sont testables seules ;
* le *gate* (`login_gate`, `logout_button`) manipule `st.session_state`.

Principe de cloisonnement : `perimetre_user_id()` renvoie l'identifiant sur
lequel **toute** requête entries/invoices doit être filtrée. Un `expert` ne
peut donc pas charger les données d'un autre, même en forçant l'interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.audit import journaliser
from core.db import get_session
from core.enums import Role
from core.models import User
from core.security import (
    generer_mot_de_passe_temporaire,
    hash_password,
    valider_robustesse,
    verify_password,
)

MESSAGE_ECHEC = "Identifiants invalides."
MAX_ECHECS = 5

# --------------------------------------------------------------------------- #
# Matrice de permissions
# --------------------------------------------------------------------------- #
#   saisie_entries        saisir / éditer ses entrées
#   generer_documents     générer son timesheet et ses factures
#   supervision           avancement global, jours consommés, alertes
#   administration        utilisateurs, TJM, projets, budgets, config
#   lecture_transversale  lire les données de tous les experts
MATRICE: dict[str, set[Role]] = {
    "saisie_entries": {Role.EXPERT, Role.ADMIN},
    "generer_documents": {Role.EXPERT, Role.ADMIN},
    "supervision": {Role.DEPUTY_MANAGER, Role.ADMIN},
    "administration": {Role.ADMIN},
    "lecture_transversale": {Role.DEPUTY_MANAGER, Role.ADMIN},
}


@dataclass(frozen=True)
class UtilisateurConnecte:
    """Identité en session — volontairement sans le hash du mot de passe."""

    id: int
    nom: str
    email: str
    role: Role
    must_change_pwd: bool = False

    @classmethod
    def depuis_user(cls, user: User) -> "UtilisateurConnecte":
        return cls(
            id=user.id,
            nom=user.nom,
            email=user.email,
            role=Role(user.role),
            must_change_pwd=bool(user.must_change_pwd),
        )


def peut(role: Role | str | None, action: str) -> bool:
    """`True` si le rôle autorise l'action (matrice ci-dessus)."""
    if role is None:
        return False
    if action not in MATRICE:
        raise KeyError(f"action inconnue dans la matrice de permissions : {action!r}")
    return Role(role) in MATRICE[action]


def perimetre_user_id(utilisateur: UtilisateurConnecte | None) -> int | None:
    """Filtre `user_id` à appliquer aux requêtes entries/invoices.

    * `expert` → son seul identifiant ;
    * `deputy_manager` / `admin` → `None`, c'est-à-dire aucun filtre (lecture
      transversale), le choix d'un expert se faisant explicitement par ailleurs.
    """
    if utilisateur is None:
        raise PermissionError("aucun utilisateur connecté")
    return utilisateur.id if utilisateur.role is Role.EXPERT else None


# --------------------------------------------------------------------------- #
# Authentification
# --------------------------------------------------------------------------- #
def authentifier(session: Session, email: str, mot_de_passe: str) -> UtilisateurConnecte | None:
    """Vérifie un couple email / mot de passe.

    Renvoie `None` dans tous les cas d'échec — email inconnu, compte désactivé
    ou mot de passe faux — afin de ne pas permettre l'énumération des comptes.
    """
    email_normalise = (email or "").strip().lower()
    user = session.scalars(select(User).where(User.email == email_normalise)).first()
    if user is None:
        # Vérification à vide : le temps de réponse ne révèle pas l'absence.
        verify_password(mot_de_passe or "", hash_password("placeholder-inexistant"))
        return None
    if not verify_password(mot_de_passe or "", user.hash_mdp):
        return None
    if not user.actif:
        return None
    journaliser(session, user.id, "login", "users", user.id)
    return UtilisateurConnecte.depuis_user(user)


def changer_mot_de_passe(
    session: Session, user_id: int, ancien: str, nouveau: str
) -> list[str]:
    """Change son propre mot de passe. Renvoie la liste des erreurs (vide = OK)."""
    user = session.get(User, user_id)
    if user is None:
        return ["Utilisateur inconnu."]
    if not verify_password(ancien, user.hash_mdp):
        return ["Mot de passe actuel incorrect."]
    manquants = valider_robustesse(nouveau)
    if manquants:
        return ["Le nouveau mot de passe doit comporter " + ", ".join(manquants) + "."]
    if verify_password(nouveau, user.hash_mdp):
        return ["Le nouveau mot de passe doit différer de l'ancien."]
    user.hash_mdp = hash_password(nouveau)
    user.must_change_pwd = False
    journaliser(session, user_id, "password_change", "users", user_id)
    return []


# --------------------------------------------------------------------------- #
# Gestion des utilisateurs (admin)
# --------------------------------------------------------------------------- #
def creer_utilisateur(
    session: Session,
    auteur_id: int | None,
    nom: str,
    email: str,
    role: Role | str,
    mot_de_passe: str | None = None,
    **champs: Any,
) -> tuple[User | None, str | None, list[str]]:
    """Crée un utilisateur. Renvoie `(user, mot_de_passe_temporaire, erreurs)`.

    Sans mot de passe fourni, un temporaire est généré et `must_change_pwd`
    est posé : il n'est renvoyé qu'une fois, à l'admin, et jamais stocké.
    """
    email_normalise = (email or "").strip().lower()
    erreurs: list[str] = []
    if not (nom or "").strip():
        erreurs.append("Le nom est obligatoire.")
    if "@" not in email_normalise:
        erreurs.append("Email invalide.")
    elif session.scalars(select(User).where(User.email == email_normalise)).first():
        erreurs.append("Cet email est déjà utilisé.")
    if mot_de_passe:
        erreurs.extend(
            f"Mot de passe : {regle}." for regle in valider_robustesse(mot_de_passe)
        )
    if erreurs:
        return None, None, erreurs

    temporaire = None if mot_de_passe else generer_mot_de_passe_temporaire()
    user = User(
        nom=nom.strip(),
        email=email_normalise,
        hash_mdp=hash_password(mot_de_passe or temporaire or ""),
        role=Role(role),
        must_change_pwd=temporaire is not None,
        actif=True,
        **champs,
    )
    session.add(user)
    session.flush()
    journaliser(
        session,
        auteur_id,
        "user_create",
        "users",
        user.id,
        {"email": email_normalise, "role": str(Role(role))},
    )
    return user, temporaire, []


def modifier_utilisateur(
    session: Session, auteur_id: int | None, user_id: int, **champs: Any
) -> tuple[User | None, list[str]]:
    """Modifie les champs d'un utilisateur (hors mot de passe)."""
    user = session.get(User, user_id)
    if user is None:
        return None, ["Utilisateur inconnu."]
    interdits = {"hash_mdp", "id", "created_at"}
    modifies: dict[str, Any] = {}
    for cle, valeur in champs.items():
        if cle in interdits or not hasattr(user, cle):
            continue
        if cle == "email":
            valeur = (valeur or "").strip().lower()
            doublon = session.scalars(
                select(User).where(User.email == valeur, User.id != user_id)
            ).first()
            if doublon:
                return None, ["Cet email est déjà utilisé."]
        if cle == "role":
            valeur = Role(valeur)
        if getattr(user, cle) != valeur:
            modifies[cle] = valeur
            setattr(user, cle, valeur)
    if modifies:
        session.flush()
        journaliser(session, auteur_id, "user_update", "users", user_id, modifies)
    return user, []


def desactiver_utilisateur(
    session: Session, auteur_id: int | None, user_id: int, actif: bool = False
) -> list[str]:
    """Désactive (ou réactive) un compte — on ne supprime jamais, pour l'historique."""
    user = session.get(User, user_id)
    if user is None:
        return ["Utilisateur inconnu."]
    if not actif and user.id == auteur_id:
        return ["Vous ne pouvez pas désactiver votre propre compte."]
    if not actif and Role(user.role) is Role.ADMIN:
        autres_admins = session.scalars(
            select(User).where(User.role == Role.ADMIN, User.actif == True, User.id != user_id)  # noqa: E712
        ).first()
        if autres_admins is None:
            return ["Impossible : ce compte est le dernier administrateur actif."]
    user.actif = actif
    journaliser(
        session,
        auteur_id,
        "user_activate" if actif else "user_deactivate",
        "users",
        user_id,
    )
    return []


def reinitialiser_mot_de_passe(
    session: Session, auteur_id: int | None, user_id: int
) -> tuple[str | None, list[str]]:
    """Génère un mot de passe temporaire et force son changement."""
    user = session.get(User, user_id)
    if user is None:
        return None, ["Utilisateur inconnu."]
    temporaire = generer_mot_de_passe_temporaire()
    user.hash_mdp = hash_password(temporaire)
    user.must_change_pwd = True
    journaliser(session, auteur_id, "password_reset", "users", user_id)
    return temporaire, []


# --------------------------------------------------------------------------- #
# Gate Streamlit
# --------------------------------------------------------------------------- #
def current_user() -> UtilisateurConnecte | None:
    """Utilisateur en session, ou `None`."""
    import streamlit as st

    return st.session_state.get("user")


def current_role() -> Role | None:
    utilisateur = current_user()
    return utilisateur.role if utilisateur else None


def require_role(*roles: Role | str) -> UtilisateurConnecte:
    """Interrompt le rendu si l'utilisateur n'a pas l'un des rôles attendus."""
    import streamlit as st

    utilisateur = current_user()
    attendus = {Role(r) for r in roles}
    if utilisateur is None or utilisateur.role not in attendus:
        st.error("Accès non autorisé.")
        st.stop()
    return utilisateur


def require_action(action: str) -> UtilisateurConnecte:
    """Variante de `require_role` fondée sur la matrice de permissions."""
    import streamlit as st

    utilisateur = current_user()
    if not peut(utilisateur.role if utilisateur else None, action):
        st.error("Accès non autorisé.")
        st.stop()
    assert utilisateur is not None
    return utilisateur


def can(action: str) -> bool:
    """`True` si l'utilisateur connecté peut réaliser l'action."""
    return peut(current_role(), action)


def login_gate() -> UtilisateurConnecte | None:
    """Affiche le formulaire de connexion tant que personne n'est connecté.

    Renvoie l'utilisateur connecté, ou `None` : dans ce cas l'appelant ne doit
    rendre aucun panneau.
    """
    import streamlit as st

    if st.session_state.get("user") is not None:
        return st.session_state["user"]

    st.title("Timesheet & Facturation")
    st.caption("Tangerine Central, LLC")

    echecs = st.session_state.get("echecs_login", 0)
    if echecs >= MAX_ECHECS:
        st.error(
            "Trop de tentatives échouées. Fermez l'onglet et reconnectez-vous "
            "dans quelques minutes."
        )
        return None

    with st.form("login"):
        email = st.text_input("Email")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        valider = st.form_submit_button("Se connecter")

    if valider:
        with get_session() as session:
            utilisateur = authentifier(session, email, mot_de_passe)
        if utilisateur is None:
            st.session_state["echecs_login"] = echecs + 1
            st.error(MESSAGE_ECHEC)
            return None
        st.session_state["user"] = utilisateur
        st.session_state["echecs_login"] = 0
        st.rerun()
    return None


def logout_button() -> None:
    """Bouton de déconnexion dans la barre latérale."""
    import streamlit as st

    if st.sidebar.button("Se déconnecter", use_container_width=True):
        for cle in list(st.session_state.keys()):
            del st.session_state[cle]
        st.rerun()
