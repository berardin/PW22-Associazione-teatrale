import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


# --- Enumerazioni ---
class StatoDomanda(str, enum.Enum):
    inviata = "inviata"
    in_delibera = "in_delibera"
    approvata = "approvata"
    rigettata = "rigettata"


class StatoSocio(str, enum.Enum):
    attivo = "attivo"
    sospeso = "sospeso"
    cessato = "cessato"


class Carica(str, enum.Enum):
    presidente = "presidente"
    vicepresidente = "vicepresidente"
    consigliere = "consigliere"


class Voto(str, enum.Enum):
    favorevole = "favorevole"
    contrario = "contrario"
    astenuto = "astenuto"


class EsitoDelibera(str, enum.Enum):
    approvata = "approvata"
    rigettata = "rigettata"


class CausalePagamento(str, enum.Enum):
    quota_associativa = "quota_associativa"
    corso = "corso"  # Nel caso facciamo un secondo processo


class Persona(Base):
    """Anagrafica di chi presenta domanda di iscrizione o è socio"""

    __tablename__ = "persona"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    cognome: Mapped[str] = mapped_column(String(100))
    codice_fiscale: Mapped[str] = mapped_column(String(16), unique=True)
    data_nascita: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(30))
    indirizzo: Mapped[str] = mapped_column(String(200))
    cap: Mapped[str] = mapped_column(String(5))
    citta: Mapped[str] = mapped_column(String(100))
    provincia: Mapped[str] = mapped_column(String(2))


class InformativaPrivacy(Base):
    """Versione dell'informativa privacy; quella in vigore è la più recente."""

    __tablename__ = "informativa_privacy"

    id: Mapped[int] = mapped_column(primary_key=True)
    versione: Mapped[str] = mapped_column(String(20), unique=True)
    testo: Mapped[str] = mapped_column(Text)
    in_vigore_dal: Mapped[date] = mapped_column(Date)


class Statuto(Base):
    """Versione dello statuto; quella in vigore è la più recente."""

    __tablename__ = "statuto"

    id: Mapped[int] = mapped_column(primary_key=True)
    versione: Mapped[str] = mapped_column(String(20), unique=True)
    testo: Mapped[str] = mapped_column(Text)
    in_vigore_dal: Mapped[date] = mapped_column(Date)


class ConsensoPrivacy(Base):
    """Consenso espresso da una persona su una versione dell'informativa."""

    __tablename__ = "consenso_privacy"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), index=True)
    informativa_id: Mapped[int] = mapped_column(ForeignKey("informativa_privacy.id"))
    tipo: Mapped[str] = mapped_column(String(50))
    accettato: Mapped[bool] = mapped_column(Boolean)
    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class DomandaIscrizione(Base):
    __tablename__ = "domanda_iscrizione"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"))
    data_presentazione: Mapped[date] = mapped_column(Date, default=date.today)
    scadenza_risposta: Mapped[date] = mapped_column(Date)
    stato: Mapped[StatoDomanda] = mapped_column(
        Enum(
            StatoDomanda, native_enum=False, length=20
        ),  # native_enum=False per problema con DB
        default=StatoDomanda.inviata,
    )


class Utente(Base):
    """Account di accesso alla piattaforma; creato all'ammissione del socio."""

    __tablename__ = "utente"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    token_attivazione_hash: Mapped[str | None] = mapped_column(String(255))
    token_scadenza: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    attivo: Mapped[bool] = mapped_column(Boolean, default=True)
    creato_il: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Socio(Base):
    """Persona ammessa all'associazione (libro soci)."""

    __tablename__ = "socio"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), unique=True)
    domanda_id: Mapped[int | None] = mapped_column(
        ForeignKey("domanda_iscrizione.id"), unique=True
    )
    numero_tessera: Mapped[str] = mapped_column(String(20), unique=True)
    stato: Mapped[StatoSocio] = mapped_column(
        Enum(StatoSocio, native_enum=False, length=20),
        default=StatoSocio.attivo,
    )
    data_ammissione: Mapped[date] = mapped_column(Date)
    data_scadenza: Mapped[date] = mapped_column(Date)


class MembroDirettivo(Base):
    """Mandato di un membro del direttivo; attivo se data_fine è nulla."""

    __tablename__ = "membro_direttivo"

    id: Mapped[int] = mapped_column(primary_key=True)
    utente_id: Mapped[int] = mapped_column(ForeignKey("utente.id"), index=True)
    carica: Mapped[Carica] = mapped_column(Enum(Carica, native_enum=False, length=20))
    data_inizio: Mapped[date] = mapped_column(Date)
    data_fine: Mapped[date | None] = mapped_column(Date)


class Delibera(Base):
    """Delibera del direttivo su una domanda di iscrizione."""

    __tablename__ = "delibera"

    id: Mapped[int] = mapped_column(primary_key=True)
    domanda_id: Mapped[int] = mapped_column(
        ForeignKey("domanda_iscrizione.id"), unique=True
    )
    aperta_il: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    chiusa_il: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    esito: Mapped[EsitoDelibera | None] = mapped_column(
        Enum(EsitoDelibera, native_enum=False, length=20)
    )
    motivazione: Mapped[str | None] = mapped_column(Text)


class VotoDelibera(Base):
    """Voto espresso da un membro del direttivo in una delibera."""

    __tablename__ = "voto_delibera"
    __table_args__ = (UniqueConstraint("delibera_id", "membro_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    delibera_id: Mapped[int] = mapped_column(ForeignKey("delibera.id"))
    membro_id: Mapped[int] = mapped_column(ForeignKey("membro_direttivo.id"))
    voto: Mapped[Voto] = mapped_column(Enum(Voto, native_enum=False, length=20))
    votato_il: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Pagamento(Base):
    """Pagamento registrato da un socio (quota associativa o corso)."""

    __tablename__ = "pagamento"

    id: Mapped[int] = mapped_column(primary_key=True)
    socio_id: Mapped[int] = mapped_column(ForeignKey("socio.id"), index=True)
    causale: Mapped[CausalePagamento] = mapped_column(
        Enum(CausalePagamento, native_enum=False, length=30)
    )
    importo: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    pagato_il: Mapped[date] = mapped_column(Date, default=date.today)
    metodo: Mapped[str] = mapped_column(String(30))
    anno_associativo: Mapped[int | None]


class AuditLog(Base):
    """Registro delle azioni rilevanti"""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    utente_id: Mapped[int | None] = mapped_column(ForeignKey("utente.id"), index=True)
    azione: Mapped[str] = mapped_column(String(100))
    entita: Mapped[str] = mapped_column(String(50))
    entita_id: Mapped[int | None]
    dettaglio: Mapped[dict | None] = mapped_column(JSONB)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
