from datetime import date, timedelta

from sqlalchemy import desc, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import parametri
from app.models import (
    AuditLog,
    ConsensoPrivacy,
    DomandaIscrizione,
    InformativaPrivacy,
    Persona,
    Socio,
    StatoDomanda,
    StatoSocio,
)
from app.schemas.domanda import DomandaIn


class DomandaEsistente(Exception):
    """Esiste già una domanda aperta, o la persona è già socia."""


class InformativaMancante(Exception):
    """Nessuna informativa in vigore: configurazione errata."""


def _informativa_in_vigore(db: Session) -> InformativaPrivacy:
    inf = db.scalar(
        select(InformativaPrivacy)
        .where(InformativaPrivacy.in_vigore_dal <= date.today())
        .order_by(desc(InformativaPrivacy.in_vigore_dal))
        .limit(1)
    )
    if inf is None:
        raise InformativaMancante("Nessuna informativa privacy in vigore")
    return inf


def presenta_domanda(db: Session, dati: DomandaIn) -> DomandaIscrizione:
    informativa = _informativa_in_vigore(db)

    trovate = db.scalars(
        select(Persona).where(
            or_(
                Persona.codice_fiscale == dati.codice_fiscale,
                Persona.email == dati.email,
            )
        )
    ).all()
    if len(trovate) > 1:
        raise DomandaEsistente("Codice fiscale o email risultano già registrati")

    persona = trovate[0] if trovate else None
    if persona is not None:
        socio = db.scalar(select(Socio).where(Socio.persona_id == persona.id))
        if socio is not None and socio.stato != StatoSocio.cessato:
            raise DomandaEsistente("Risulta già un socio con questi dati")
        aperta = db.scalar(
            select(DomandaIscrizione).where(
                DomandaIscrizione.persona_id == persona.id,
                DomandaIscrizione.stato.in_(
                    [StatoDomanda.inviata, StatoDomanda.in_delibera]
                ),
            )
        )
        if aperta is not None:
            giorni = (aperta.scadenza_risposta - date.today()).days
            if giorni >= 0:
                msg = (
                    f"Risulta già una domanda in corso per questi dati: il direttivo risponde "
                    f"entro il {aperta.scadenza_risposta:%d/%m/%Y} (tra {giorni} giorni al massimo)."
                )
            else:
                msg = (
                    f"Risulta già una domanda in corso per questi dati: il termine per la risposta "
                    f"({aperta.scadenza_risposta:%d/%m/%Y}) è scaduto."
                )
            raise DomandaEsistente(msg)
    else:
        persona = Persona(codice_fiscale=dati.codice_fiscale)
        db.add(persona)

    persona.nome, persona.cognome = dati.nome, dati.cognome
    persona.data_nascita, persona.email, persona.telefono = (
        dati.data_nascita,
        dati.email,
        dati.telefono,
    )
    persona.indirizzo, persona.cap = dati.indirizzo, dati.cap
    persona.citta, persona.provincia = dati.citta, dati.provincia

    try:
        db.flush()  # assegna l'id

        oggi = date.today()
        domanda = DomandaIscrizione(
            persona_id=persona.id,
            data_presentazione=oggi,
            scadenza_risposta=oggi + timedelta(days=parametri.scadenza_risposta_giorni),
            stato=StatoDomanda.inviata,
        )
        db.add(domanda)

        for tipo, accettato in [
            ("trattamento_iscrizione", True),
            ("newsletter", dati.newsletter),
            ("foto", dati.foto),
        ]:
            db.add(
                ConsensoPrivacy(
                    persona_id=persona.id,
                    informativa_id=informativa.id,
                    tipo=tipo,
                    accettato=accettato,
                )
            )
        db.flush()

        # Nel log solo identificativi, non dati personali
        db.add(
            AuditLog(
                utente_id=None,
                azione="domanda_presentata",
                entita="domanda_iscrizione",
                entita_id=domanda.id,
                dettaglio={"persona_id": persona.id, "informativa_id": informativa.id},
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DomandaEsistente("Codice fiscale o email risultano già registrati")

    db.refresh(domanda)
    return domanda
