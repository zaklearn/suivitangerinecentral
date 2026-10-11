"""M6 — Connexion, sessions et bootstrap de la base MySQL (Aiven, SSL).

La configuration vient exclusivement de `st.secrets` en exécution Streamlit :

    [mysql]
    host = "..."
    port = 12345
    user = "avnadmin"
    password = "..."
    database = "defaultdb"
    ca_cert = \"\"\"-----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----\"\"\"

    [bootstrap_admin]
    nom = "Admin"
    email = "admin@example.org"
    password = "..."

Aucun secret n'est écrit en dur. Pour les tests et l'outillage hors Streamlit,
`APP_DATABASE_URL` permet de pointer une base locale (SQLite ou MySQL).
"""
from __future__ import annotations

import atexit
import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker

from core.enums import Role
from core.models import Base, Config, User
from core.security import hash_password

_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None
_ca_tmpfile: str | None = None


# --------------------------------------------------------------------------- #
# Secrets
# --------------------------------------------------------------------------- #
def _secrets() -> Any:
    """`st.secrets` si Streamlit est disponible et configuré, sinon None."""
    try:
        import streamlit as st
    except ModuleNotFoundError:  # pragma: no cover - Streamlit est une dépendance
        return None
    try:
        # Accès défensif : lève si aucun fichier secrets.toml n'existe.
        _ = st.secrets  # noqa: B018
        return st.secrets
    except Exception:
        return None


def _ecrire_ca(ca_cert: str) -> str:
    """Matérialise le certificat CA Aiven dans un fichier temporaire.

    PyMySQL attend un chemin, pas un contenu. Le fichier est créé avec les
    droits restreints du répertoire temporaire et supprimé à la sortie.
    """
    global _ca_tmpfile
    if _ca_tmpfile and Path(_ca_tmpfile).exists():
        return _ca_tmpfile
    fd, chemin = tempfile.mkstemp(prefix="aiven-ca-", suffix=".pem")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(ca_cert.strip() + "\n")
    os.chmod(chemin, 0o600)
    _ca_tmpfile = chemin
    atexit.register(lambda: Path(chemin).unlink(missing_ok=True))
    return chemin


def _url_et_connect_args() -> tuple[str, dict]:
    """Construit l'URL SQLAlchemy et les `connect_args` SSL."""
    url_env = os.environ.get("APP_DATABASE_URL")
    if url_env:
        return url_env, {}

    secrets = _secrets()
    section = None
    if secrets is not None:
        try:
            section = secrets["mysql"]
        except Exception:
            section = None
    if section is None:
        raise RuntimeError(
            "Configuration base absente : renseignez [mysql] dans "
            ".streamlit/secrets.toml (voir .streamlit/secrets.toml.example) "
            "ou la variable d'environnement APP_DATABASE_URL."
        )

    host = section["host"]
    port = int(section.get("port", 3306))
    user = section["user"]
    password = section["password"]
    database = section["database"]
    ca_cert = section.get("ca_cert")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    connect_args: dict = {}
    if ca_cert:
        # SSL obligatoire côté Aiven : on vérifie le certificat serveur.
        connect_args["ssl"] = {"ca": _ecrire_ca(ca_cert)}
    return url, connect_args


# --------------------------------------------------------------------------- #
# Engine / sessions
# --------------------------------------------------------------------------- #
def configure_engine(url: str, connect_args: dict | None = None) -> Engine:
    """Force l'engine (tests, scripts). Remplace l'engine courant."""
    global _engine, _SessionFactory
    kwargs: dict = {"pool_pre_ping": True, "future": True}
    if url.startswith("sqlite"):
        # Même connexion partagée pour une base mémoire pilotée par les tests.
        kwargs.pop("pool_pre_ping")
    _engine = create_engine(url, connect_args=connect_args or {}, **kwargs)
    _SessionFactory = sessionmaker(bind=_engine, expire_on_commit=False, future=True)
    return _engine


def get_engine() -> Engine:
    """Engine global, créé à la demande."""
    global _engine
    if _engine is None:
        url, connect_args = _url_et_connect_args()
        configure_engine(url, connect_args)
    assert _engine is not None
    return _engine


def reset_engine() -> None:
    """Oublie l'engine courant (tests)."""
    global _engine, _SessionFactory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionFactory = None


@contextmanager
def get_session() -> Iterator[Session]:
    """Session transactionnelle : commit en sortie normale, rollback sinon."""
    get_engine()
    assert _SessionFactory is not None
    session = _SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def health_check() -> bool:
    """`True` si la base répond."""
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# --------------------------------------------------------------------------- #
# Bootstrap
# --------------------------------------------------------------------------- #
def bootstrap() -> dict:
    """Crée les tables manquantes puis sème `config` et l'admin initial.

    Idempotent : deux appels successifs ne produisent aucun doublon et ne
    réécrivent aucune valeur existante.
    """
    engine = get_engine()
    Base.metadata.create_all(engine)

    rapport = {"config_creee": False, "admin_cree": False, "admin_email": None}
    with get_session() as session:
        if session.get(Config, 1) is None:
            session.add(Config(id=1))
            rapport["config_creee"] = True

        premier_user = session.scalars(select(User.id).limit(1)).first()
        if premier_user is None:
            graine = _graine_admin()
            if graine is not None:
                nom, email, mot_de_passe = graine
                session.add(
                    User(
                        nom=nom,
                        email=email,
                        hash_mdp=hash_password(mot_de_passe),
                        role=Role.ADMIN,
                        actif=True,
                        must_change_pwd=True,
                    )
                )
                rapport["admin_cree"] = True
                rapport["admin_email"] = email
    return rapport


def _graine_admin() -> tuple[str, str, str] | None:
    """Lit `st.secrets["bootstrap_admin"]`, sinon les variables d'environnement."""
    secrets = _secrets()
    section = None
    if secrets is not None:
        try:
            section = secrets["bootstrap_admin"]
        except Exception:
            section = None
    if section is not None:
        return (
            section.get("nom", "Administrateur"),
            section["email"],
            section["password"],
        )
    email = os.environ.get("BOOTSTRAP_ADMIN_EMAIL")
    mot_de_passe = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")
    if email and mot_de_passe:
        return os.environ.get("BOOTSTRAP_ADMIN_NOM", "Administrateur"), email, mot_de_passe
    return None


def get_config(session: Session) -> Config:
    """Ligne de configuration unique, créée au besoin."""
    config = session.get(Config, 1)
    if config is None:
        config = Config(id=1)
        session.add(config)
        session.flush()
    return config


def heures_par_jour(session: Session) -> Decimal:
    """Valeur courante de `config.heures_par_jour` (> 0 garantie)."""
    valeur = Decimal(get_config(session).heures_par_jour)
    return valeur if valeur > 0 else Decimal("8")
