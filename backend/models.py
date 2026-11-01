from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Persona(Base):
    """Anagrafica di chi presenta domanda di iscrizione o è socio."""

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
