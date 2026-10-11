"""M6 — Modèle de données (ORM SQLAlchemy 2.x).

Toutes les montants sont en USD. Les `Numeric` sont manipulés en `Decimal`
côté Python : aucun calcul monétaire ne passe par un float.

Règles structurantes rappelées ici car elles conditionnent le schéma :
  * `entries.taux_applique` est un **snapshot** du TJM de l'expert à la saisie ;
    modifier `users.tjm_*` ensuite ne touche aucune entrée existante.
  * `entries.heures_par_jour_snap` fige la conversion jours -> heures
    (option C) et n'est renseigné que pour `unite = jour`.
  * `invoice_labor` / `invoice_odc` sont des copies figées à l'émission :
    elles ne référencent pas les entrées, elles les recopient.
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    CHAR,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.enums import (
    ModeNumerotation,
    NiveauAlerte,
    Role,
    StatutAlerte,
    StatutFacture,
    StatutLivrable,
    StatutProjet,
    TypeActivite,
    Unite,
)

# Précisions décimales : montants sur 2 décimales, quantités sur 2 décimales.
MONEY = Numeric(14, 2)
QTY = Numeric(10, 2)
PCT = Numeric(6, 2)


def _enum(python_enum, name: str) -> SAEnum:
    """ENUM MySQL natif portant les *valeurs* (pas les noms) de l'enum Python."""
    return SAEnum(
        python_enum,
        name=name,
        values_callable=lambda e: [m.value for m in e],
        validate_strings=True,
    )


class Base(DeclarativeBase):
    pass


class Config(Base):
    """Paramètres généraux — ligne unique `id = 1` (M2)."""

    __tablename__ = "config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    heures_par_jour: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=Decimal("8")
    )
    devise: Mapped[str] = mapped_column(CHAR(3), nullable=False, default="USD")
    seuil_alerte_pct: Mapped[int] = mapped_column(Integer, nullable=False, default=80)
    seuil_critique_pct: Mapped[int] = mapped_column(Integer, nullable=False, default=95)
    bill_to_nom: Mapped[str] = mapped_column(
        String(255), nullable=False, default="Tangerine Central, LLC"
    )
    bill_to_ville: Mapped[str] = mapped_column(
        String(255), nullable=False, default="Durham, NC, USA"
    )
    bill_to_email: Mapped[str] = mapped_column(
        String(255), nullable=False, default="carmen@tangerinecentral.org"
    )
    prefixe_facture: Mapped[str] = mapped_column(String(16), nullable=False, default="TC")
    mode_numerotation: Mapped[ModeNumerotation] = mapped_column(
        _enum(ModeNumerotation, "mode_numerotation_enum"),
        nullable=False,
        default=ModeNumerotation.PAR_EXPERT,
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hash_mdp: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(_enum(Role, "role_enum"), nullable=False)
    tjm_jour: Mapped[Decimal | None] = mapped_column(MONEY, nullable=True)
    tjm_heure: Mapped[Decimal | None] = mapped_column(MONEY, nullable=True)
    # Bloc société de l'expert, imprimé en haut à droite de la facture.
    societe_nom: Mapped[str | None] = mapped_column(String(255), nullable=True)
    societe_adresse: Mapped[str | None] = mapped_column(String(255), nullable=True)
    societe_ville_zip: Mapped[str | None] = mapped_column(String(255), nullable=True)
    societe_phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    societe_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Discriminant de la séquence de factures propre à l'expert (ex. « JD »).
    code_facture: Mapped[str | None] = mapped_column(String(8), nullable=True, unique=True)
    actif: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    must_change_pwd: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    allocations: Mapped[list["Allocation"]] = relationship(back_populates="user")

    def tjm_pour(self, unite: Unite) -> Decimal | None:
        """TJM applicable à l'unité — base du snapshot `taux_applique` (M3)."""
        return self.tjm_jour if Unite(unite) is Unite.JOUR else self.tjm_heure


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str | None] = mapped_column(String(64), nullable=True)
    client: Mapped[str] = mapped_column(
        String(255), nullable=False, default="Tangerine Central, LLC"
    )
    budget_jours: Mapped[Decimal | None] = mapped_column(QTY, nullable=True)
    statut: Mapped[StatutProjet] = mapped_column(
        _enum(StatutProjet, "statut_projet_enum"),
        nullable=False,
        default=StatutProjet.ACTIF,
    )
    date_debut: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    allocations: Mapped[list["Allocation"]] = relationship(back_populates="project")
    deliverables: Mapped[list["Deliverable"]] = relationship(back_populates="project")


class Allocation(Base):
    __tablename__ = "allocations"
    __table_args__ = (UniqueConstraint("user_id", "project_id", name="uq_alloc_user_project"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    jours_alloues: Mapped[Decimal] = mapped_column(QTY, nullable=False, default=Decimal("0"))

    user: Mapped[User] = relationship(back_populates="allocations")
    project: Mapped[Project] = relationship(back_populates="allocations")


class Deliverable(Base):
    __tablename__ = "deliverables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    intitule: Mapped[str] = mapped_column(String(255), nullable=False)
    statut: Mapped[StatutLivrable] = mapped_column(
        _enum(StatutLivrable, "statut_livrable_enum"),
        nullable=False,
        default=StatutLivrable.A_FAIRE,
    )
    echeance: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    project: Mapped[Project] = relationship(back_populates="deliverables")


class Entry(Base):
    """Une ligne de timesheet : la brique de base de toute l'app."""

    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    deliverable_id: Mapped[int | None] = mapped_column(
        ForeignKey("deliverables.id"), nullable=True
    )
    date_entry: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    unite: Mapped[Unite] = mapped_column(_enum(Unite, "unite_enum"), nullable=False)
    quantite: Mapped[Decimal] = mapped_column(QTY, nullable=False)
    taux_applique: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    montant: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    heures_par_jour_snap: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    note_livrable: Mapped[str | None] = mapped_column(Text, nullable=True)
    type_activite: Mapped[TypeActivite] = mapped_column(
        _enum(TypeActivite, "type_activite_enum"), nullable=False
    )
    facturable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    invoice_id: Mapped[int | None] = mapped_column(
        ForeignKey("invoices.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship()
    project: Mapped[Project] = relationship()
    deliverable: Mapped[Deliverable | None] = relationship()
    invoice: Mapped["Invoice | None"] = relationship(back_populates="entries")

    @property
    def heures_timesheet(self) -> Decimal:
        """Heures affichées au timesheet — option C, via le snapshot figé.

        Dérivé, jamais stocké : `quantite` si l'unité est l'heure, sinon
        `quantite x heures_par_jour_snap`. Sans impact sur la facturation.
        """
        if Unite(self.unite) is Unite.HEURE:
            return Decimal(self.quantite)
        facteur = self.heures_par_jour_snap
        if facteur is None:
            raise ValueError(
                f"entrée {self.id}: unite=jour sans heures_par_jour_snap (intégrité M6 §2)"
            )
        return Decimal(self.quantite) * Decimal(facteur)


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    # NULL tant que la facture est en brouillon : le numéro n'est attribué
    # qu'à l'émission (séquence par expert et par année, M5 §5.4).
    numero: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True)
    date_emission: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_echeance: Mapped[date | None] = mapped_column(Date, nullable=True)
    statut: Mapped[StatutFacture] = mapped_column(
        _enum(StatutFacture, "statut_facture_enum"),
        nullable=False,
        default=StatutFacture.BROUILLON,
    )
    sous_total_labor: Mapped[Decimal] = mapped_column(MONEY, nullable=False, default=Decimal("0"))
    sous_total_odc: Mapped[Decimal] = mapped_column(MONEY, nullable=False, default=Decimal("0"))
    avance: Mapped[Decimal] = mapped_column(MONEY, nullable=False, default=Decimal("0"))
    total_net: Mapped[Decimal] = mapped_column(MONEY, nullable=False, default=Decimal("0"))
    periode_debut: Mapped[date | None] = mapped_column(Date, nullable=True)
    periode_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship()
    entries: Mapped[list[Entry]] = relationship(back_populates="invoice")
    labor_lines: Mapped[list["InvoiceLabor"]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan", order_by="InvoiceLabor.item"
    )
    odc_lines: Mapped[list["InvoiceOdc"]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan", order_by="InvoiceOdc.item"
    )


class InvoiceLabor(Base):
    """Snapshot figé d'une ligne LABOR — immuable après émission."""

    __tablename__ = "invoice_labor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False, index=True)
    item: Mapped[int] = mapped_column(Integer, nullable=False)
    projet: Mapped[str] = mapped_column(String(255), nullable=False)
    deliverable_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantite: Mapped[Decimal] = mapped_column(QTY, nullable=False)
    taux: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    montant: Mapped[Decimal] = mapped_column(MONEY, nullable=False)

    invoice: Mapped[Invoice] = relationship(back_populates="labor_lines")


class InvoiceOdc(Base):
    """Snapshot figé d'une ligne ODC (Other Direct Costs)."""

    __tablename__ = "invoice_odc"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False, index=True)
    item: Mapped[int] = mapped_column(Integer, nullable=False)
    projet: Mapped[str] = mapped_column(String(255), nullable=False)
    odc: Mapped[str] = mapped_column(String(255), nullable=False)
    units: Mapped[Decimal] = mapped_column(QTY, nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    montant: Mapped[Decimal] = mapped_column(MONEY, nullable=False)

    invoice: Mapped[Invoice] = relationship(back_populates="odc_lines")


class Alert(Base):
    """M8 — franchissement de seuil sur un couple (expert, projet)."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    niveau: Mapped[NiveauAlerte] = mapped_column(
        _enum(NiveauAlerte, "niveau_alerte_enum"), nullable=False
    )
    pct: Mapped[Decimal] = mapped_column(PCT, nullable=False)
    jours_restants: Mapped[Decimal] = mapped_column(QTY, nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    statut: Mapped[StatutAlerte] = mapped_column(
        _enum(StatutAlerte, "statut_alerte_enum"), nullable=False, default=StatutAlerte.OUVERTE
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    project: Mapped[Project] = relationship()
    user: Mapped[User] = relationship()


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity: Mapped[str | None] = mapped_column(String(64), nullable=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    detail: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
