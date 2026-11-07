"""Creazione automatica dati per la demo"""

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select

from app.core.config import parametri
from app.core.security import hash_password
from app.db import SessionLocal
from app.models import (
    Carica,
    ConsensoPrivacy,
    Delibera,
    DomandaIscrizione,
    EsitoDelibera,
    InformativaPrivacy,
    Statuto,
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

TESTO_STATUTO = """STATUTO DELL'ASSOCIAZIONE TEATRAMICO

Art. 1 – Lorem ipsum
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua, sede in Lorem Civitas, via Ipsum n. 1.

Art. 2 – Dolor sit amet
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse.

Art. 3 – Consectetur adipiscing
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum:
a) Curabitur pretium tincidunt lacus, nulla gravida orci a odio;
b) Nullam varius, turpis et commodo pharetra, est eros bibendum elit;
c) Integer in mauris eu nibh euismod gravida.

Art. 4 – Sed do eiusmod
Praesent dapibus, neque id cursus faucibus, tortor neque egestas augue, eu vulputate magna eros eu erat. Aliquam erat volutpat, nam dui mi, tincidunt quis.

Art. 5 – Tempor incididunt
Phasellus ultrices nulla quis nibh. Quisque a lectus. Donec consectetuer ligula vulputate sem tristique cursus. Nam nulla quam, gravida non, commodo a, sodales sit amet.

Art. 6 – Labore et dolore
Organa lorem sunt:
a) Assemblea Ipsum;
b) Consilium Dolor;
c) Praeses Amet.

Art. 7 – Magna aliqua
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae. Fusce id purus, ut varius tincidunt libero, mauris sit amet magna.

Art. 8 – Ut enim ad minim
Morbi in sem quis dui placerat ornare. Pellentesque odio nisi, euismod in, pharetra a, ultricies in, diam. Sed arcu, cras consequat.

Art. 9 – Disposizioni finali
Mauris eleifend leo quis libero tristique, pro omnibus non expressis lorem ipsum dolor sit amet.
"""

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
        data_scadenza=aggiungi_mesi(ammissione, parametri.durata_quota_mesi),
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


def nuova_domanda(db, persona, stato, giorni_fa, informativa, statuto):
    presentata = OGGI - timedelta(days=giorni_fa)
    d = DomandaIscrizione(
        persona_id=persona.id,
        data_presentazione=presentata,
        scadenza_risposta=presentata
        + timedelta(days=parametri.scadenza_risposta_giorni),
        stato=stato,
        statuto_id=statuto.id,
        statuto_accettato_il=datetime.now(timezone.utc),
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

        # Statuto
        stat = Statuto(
            versione="1.0", in_vigore_dal=date(2026, 1, 1), testo=TESTO_STATUTO
        )
        db.add(stat)
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
        d = nuova_domanda(db, p, StatoDomanda.approvata, 70, inf, stat)
        nuovo_utente(db, p, "giulia.bianchi", PASSWORD_DEMO)
        nuovo_socio(db, p, "T-0008", OGGI - timedelta(days=50), domanda_id=d.id)

        # Domande ancora aperte
        nuova_domanda(
            db,
            nuova_persona(db, "Luca", "Ferrari", date(1988, 7, 2)),
            StatoDomanda.inviata,
            50,
            inf,
            stat,
        )
        nuova_domanda(
            db,
            nuova_persona(db, "Elena", "Conti", date(1999, 11, 21)),
            StatoDomanda.inviata,
            3,
            inf,
            stat,
        )

        # Domanda in delibera con 3 voti su 7
        d = nuova_domanda(
            db,
            nuova_persona(db, "Paolo", "Greco", date(1985, 2, 9)),
            StatoDomanda.in_delibera,
            20,
            inf,
            stat,
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
            stat,
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
