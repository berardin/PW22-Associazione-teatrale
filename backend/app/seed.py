"""Creazione automatica dati per la demo"""

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select

from app.core.config import statuto
from app.core.security import hash_password
from app.db import SessionLocal
from app.models import (
    Carica,
    ConsensoPrivacy,
    Delibera,
    DomandaIscrizione,
    EsitoDelibera,
    InformativaPrivacy,
    MembroDirettivo,
    Pagamento,
    Persona,
    Socio,
    StatoDomanda,
    StatoSocio,
    Utente,
    Voto,
    VotoDelibera,
    CausalePagamento,
)

PASSWORD_DEMO = "TeatramicoDemo-2026!"
PASSWORD_ADMIN = "TeatramicoAdmin-2026!"

OGGI = date.today()
_contatore = 0


def aggiungi_mesi(d: date, mesi: int) -> date:
    m = d.month - 1 + mesi
    anno, mese = d.year + m // 12, m % 12 + 1
    ultimo = [
        31,
        29 if anno % 4 == 0 and (anno % 100 or anno % 400 == 0) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ][mese - 1]
    return date(anno, mese, min(d.day, ultimo))


def nuova_persona(
    db, nome, cognome, nascita, citta="Mola di Bari", prov="BA", cap="70042"
):
    global _contatore
    _contatore += 1
    p = Persona(
        nome=nome,
        cognome=cognome,
        codice_fiscale=f"DEMOCF{_contatore:010d}",
        data_nascita=nascita,
        email=f"{nome}.{cognome}@example.it".lower(),
        telefono=None,
        indirizzo="Via Demo 1",
        cap=cap,
        citta=citta,
        provincia=prov,
    )
    db.add(p)
    db.flush()
    return p


def nuovo_utente(db, persona, username, password, is_admin=False):
    u = Utente(
        persona_id=persona.id,
        username=username,
        password_hash=hash_password(password),
        is_admin=is_admin,
        attivo=True,
    )
    db.add(u)
    db.flush()
    return u


def nuovo_socio(db, persona, tessera, ammissione, domanda_id=None):
    s = Socio(
        persona_id=persona.id,
        domanda_id=domanda_id,
        numero_tessera=tessera,
        stato=StatoSocio.attivo,
        data_ammissione=ammissione,
        data_scadenza=aggiungi_mesi(ammissione, statuto.durata_quota_mesi),
    )
    db.add(s)
    db.flush()
    db.add(
        Pagamento(
            socio_id=s.id,
            causale=CausalePagamento.quota_associativa,
            importo=20,
            pagato_il=ammissione,
            metodo="bonifico",
            anno_associativo=ammissione.year,
        )
    )
    return s


def nuova_domanda(db, persona, stato, giorni_fa, informativa):
    presentata = OGGI - timedelta(days=giorni_fa)
    d = DomandaIscrizione(
        persona_id=persona.id,
        data_presentazione=presentata,
        scadenza_risposta=presentata + timedelta(days=statuto.scadenza_risposta_giorni),
        stato=stato,
    )
    db.add(d)
    db.flush()
    db.add(
        ConsensoPrivacy(
            persona_id=persona.id,
            informativa_id=informativa.id,
            tipo="trattamento_iscrizione",
            accettato=True,
        )
    )
    return d


def esegui():
    with SessionLocal() as db:
        if db.scalar(select(Utente).where(Utente.username == "admin")):
            print("Seed già eseguito: nessuna modifica.")
            return

        # Informativa
        inf = InformativaPrivacy(
            versione="1.0",
            in_vigore_dal=date(2026, 1, 1),
            testo="[Testo dell'informativa sul trattamento dei dati]",
        )
        db.add(inf)
        db.flush()

        # Admin tecnico (non socio, non direttivo)
        p_admin = nuova_persona(db, "Admin", "Tecnico", date(1990, 1, 1))
        nuovo_utente(db, p_admin, "admin", PASSWORD_ADMIN, is_admin=True)

        # Fondatori: utente + socio + mandato
        # Per questione di ononimia, lo username è il nome e cognome in minuscolo senza spazi
        fondatori = [
            ("Marta", "Rossi", "marta.rossi", Carica.presidente, True),
            ("Carlo", "Neri", "carlo.neri", Carica.vicepresidente, False),
            ("Anna", "Riva", "anna.riva", Carica.consigliere, False),
            ("Sergio", "Villa", "sergio.villa", Carica.consigliere, False),
            ("Paola", "Longo", "paola.longo", Carica.consigliere, False),
            ("Franco", "Gatti", "franco.gatti", Carica.consigliere, False),
            ("Lucia", "Fontana", "lucia.fontana", Carica.consigliere, False),
        ]
        inizio = OGGI - timedelta(days=730)
        membri = []
        for i, (nome, cognome, user, carica, admin) in enumerate(fondatori, start=1):
            p = nuova_persona(db, nome, cognome, date(1975 + i, 5, 10))
            u = nuovo_utente(db, p, user, PASSWORD_DEMO, is_admin=admin)
            s = nuovo_socio(db, p, f"T-{i:04d}", inizio)
            s.data_scadenza = OGGI + timedelta(days=180)  # quota in regola
            m = MembroDirettivo(utente_id=u.id, carica=carica, data_inizio=inizio)
            db.add(m)
            db.flush()
            membri.append(m)

        # Socio ammesso da poco (domanda approvata, voto in assemblea tra ~40 giorni)
        p = nuova_persona(db, "Giulia", "Bianchi", date(1994, 3, 14))
        d = nuova_domanda(db, p, StatoDomanda.approvata, 70, inf)
        nuovo_utente(db, p, "giulia.bianchi", PASSWORD_DEMO)
        nuovo_socio(db, p, "T-0008", OGGI - timedelta(days=50), domanda_id=d.id)

        # Domande ancora aperte
        nuova_domanda(
            db,
            nuova_persona(db, "Luca", "Ferrari", date(1988, 7, 2)),
            StatoDomanda.inviata,
            50,
            inf,
        )
        nuova_domanda(
            db,
            nuova_persona(db, "Elena", "Conti", date(1999, 11, 21)),
            StatoDomanda.inviata,
            3,
            inf,
        )

        # Domanda in delibera con 3 voti su 7
        d = nuova_domanda(
            db,
            nuova_persona(db, "Paolo", "Greco", date(1985, 2, 9)),
            StatoDomanda.in_delibera,
            20,
            inf,
        )
        delibera = Delibera(domanda_id=d.id)
        db.add(delibera)
        db.flush()
        for m, v in zip(membri[:3], [Voto.favorevole, Voto.favorevole, Voto.contrario]):
            db.add(VotoDelibera(delibera_id=delibera.id, membro_id=m.id, voto=v))

        # Domanda rigettata con delibera chiusa
        d = nuova_domanda(
            db,
            nuova_persona(db, "Sara", "Moretti", date(1992, 6, 30)),
            StatoDomanda.rigettata,
            45,
            inf,
        )
        delibera = Delibera(
            domanda_id=d.id,
            chiusa_il=datetime.now(timezone.utc),
            esito=EsitoDelibera.rigettata,
            motivazione="[Motivazione di esempio del rigetto]",
        )
        db.add(delibera)
        db.flush()
        for m, v in zip(membri[:4], [Voto.contrario] * 3 + [Voto.favorevole]):
            db.add(VotoDelibera(delibera_id=delibera.id, membro_id=m.id, voto=v))

        db.commit()
        print("Seed completato.")


if __name__ == "__main__":
    esegui()
