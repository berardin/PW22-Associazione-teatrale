import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


# --- Enumerazioni ---
class StatoDomanda(str, enum.Enum):
    inviata = "inviata"
    in_delibera = "in_delibera"
    approvata = "approvata"
    rigettata = "rigettata"


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


class ConsensoPrivacy(Base):
    """Consenso privacy per la persona"""

    __tablename__ = "consenso_privacy"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"))
    tipo: Mapped[str] = mapped_column(String(50))
    versione_informativa: Mapped[str] = mapped_column(String(20))
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
