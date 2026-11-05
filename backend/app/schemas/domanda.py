from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

Testo100 = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class DomandaIn(BaseModel):
    nome: Testo100
    cognome: Testo100
    codice_fiscale: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, to_upper=True, pattern=r"^[A-Z0-9]{16}$"
        ),
    ]
    data_nascita: date
    email: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            max_length=255,
            pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        ),
    ]
    telefono: (
        Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)] | None
    ) = None
    indirizzo: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    cap: Annotated[str, StringConstraints(pattern=r"^\d{5}$")]
    citta: Testo100
    provincia: Annotated[
        str,
        StringConstraints(strip_whitespace=True, to_upper=True, pattern=r"^[A-Z]{2}$"),
    ]
    consenso_informativa: bool
    newsletter: bool = False
    foto: bool = False

    @field_validator("data_nascita")
    @classmethod
    def nascita_nel_passato(cls, v: date) -> date:
        if v >= date.today() or v.year < 1900:
            raise ValueError("data di nascita non valida")
        return v

    @field_validator("consenso_informativa")
    @classmethod
    def consenso_obbligatorio(cls, v: bool) -> bool:
        if not v:
            raise ValueError(
                "il consenso al trattamento per l'iscrizione è obbligatorio"
            )
        return v


class DomandaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stato: str
    data_presentazione: date
    scadenza_risposta: date
