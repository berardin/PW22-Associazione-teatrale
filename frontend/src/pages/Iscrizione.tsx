import { useState } from "react";
import type { FormEvent } from "react";
import "./Iscrizione.css";

type Dati = {
  nome: string;
  cognome: string;
  codiceFiscale: string;
  dataNascita: string;
  email: string;
  telefono: string;
  indirizzo: string;
  cap: string;
  citta: string;
  provincia: string;
  consensoInformativa: boolean;
  newsletter: boolean;
  foto: boolean;
};
type Errori = Partial<Record<keyof Dati, string>>;

const VUOTO: Dati = {
  nome: "",
  cognome: "",
  codiceFiscale: "",
  dataNascita: "",
  email: "",
  telefono: "",
  indirizzo: "",
  cap: "",
  citta: "",
  provincia: "",
  consensoInformativa: false,
  newsletter: false,
  foto: false,
};

const ETA_MINIMA = 18; // deve coincidere con l'età nel backend

function eta(nascita: string): number {
  const n = new Date(nascita);
  const o = new Date();
  let anni = o.getFullYear() - n.getFullYear();
  if (
    o.getMonth() < n.getMonth() ||
    (o.getMonth() === n.getMonth() && o.getDate() < n.getDate())
  )
    anni--;
  return anni;
}

// Validazione dati form
function valida(d: Dati): Errori {
  const e: Errori = {};
  const oggi = new Date().toISOString().slice(0, 10);
  if (!d.nome.trim()) e.nome = "Inserisci il nome.";
  if (!d.cognome.trim()) e.cognome = "Inserisci il cognome.";
  if (!/^[A-Z0-9]{16}$/.test(d.codiceFiscale.toUpperCase()))
    e.codiceFiscale = "Lunghezza codice fiscale non valida.";
  if (!d.dataNascita) e.dataNascita = "Inserisci la data di nascita.";
  else if (d.dataNascita >= oggi)
    e.dataNascita = "La data di nascita deve essere nel passato.";
  else if (eta(d.dataNascita) < ETA_MINIMA)
    e.dataNascita = `Per iscriversi serve avere almeno ${ETA_MINIMA} anni.`;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email))
    e.email = "Inserisci un indirizzo email valido.";
  if (!d.indirizzo.trim()) e.indirizzo = "Inserisci l'indirizzo.";
  if (!/^\d{5}$/.test(d.cap)) e.cap = "Il CAP ha 5 cifre.";
  if (!d.citta.trim()) e.citta = "Inserisci la città.";
  if (!/^[A-Za-z]{2}$/.test(d.provincia)) e.provincia = "Sigla di 2 lettere.";
  if (!d.consensoInformativa)
    e.consensoInformativa =
      "Per presentare la domanda devi accettare l'informativa.";
  return e;
}

type CampoProps = {
  id: keyof Dati;
  etichetta: string;
  valore: string;
  errore?: string;
  onChange: (id: keyof Dati, v: string) => void;
  tipo?: string;
  facoltativo?: boolean;
  maxLength?: number;
  maiuscolo?: boolean;
  larghezza?: string;
};

function Campo({
  id,
  etichetta,
  valore,
  errore,
  onChange,
  tipo = "text",
  facoltativo,
  maxLength,
  maiuscolo,
  larghezza,
}: CampoProps) {
  return (
    <div className="campo" style={{ flex: larghezza ?? "1 1 260px" }}>
      <label htmlFor={id}>
        {etichetta}{" "}
        {facoltativo && <span className="facoltativo">(facoltativo)</span>}
      </label>
      <input
        id={id}
        type={tipo}
        value={valore}
        maxLength={maxLength}
        className={maiuscolo ? "maiuscolo" : undefined}
        aria-invalid={errore ? true : undefined}
        aria-describedby={errore ? `${id}-errore` : undefined}
        onChange={(ev) => onChange(id, ev.target.value)}
      />
      {errore && (
        <span id={`${id}-errore`} className="errore" role="alert">
          {errore}
        </span>
      )}
    </div>
  );
}

export default function Iscrizione() {
  const [dati, setDati] = useState<Dati>(VUOTO);
  const [errori, setErrori] = useState<Errori>({});
  const [inviata, setInviata] = useState<Dati | null>(null);

  const cambia = (id: keyof Dati, v: string) =>
    setDati((d) => ({ ...d, [id]: v }));
  const spunta = (
    id: "consensoInformativa" | "newsletter" | "foto",
    v: boolean,
  ) => setDati((d) => ({ ...d, [id]: v }));

  function invia(ev: FormEvent) {
    ev.preventDefault();
    const e = valida(dati);
    setErrori(e);
    if (Object.keys(e).length === 0) setInviata(dati); // Invio a backend
  }

  const campo = (
    id: keyof Dati,
    etichetta: string,
    extra: Partial<CampoProps> = {},
  ) => (
    <Campo
      id={id}
      etichetta={etichetta}
      valore={dati[id] as string}
      errore={errori[id]}
      onChange={cambia}
      {...extra}
    />
  );

  return (
    <>
      <section className="fascia">
        <svg
          className="fascia-onda"
          aria-hidden="true"
          viewBox="0 0 1280 120"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="oro-fascia" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="#B8862B" />
              <stop offset="0.5" stopColor="#E3C26B" />
              <stop offset="1" stopColor="#B8862B" />
            </linearGradient>
          </defs>
          <path
            d="M0 88 C 340 28, 740 112, 1280 38 L1280 120 L0 120 Z"
            fill="#F6F0DF"
          />
          <path
            d="M0 88 C 340 28, 740 112, 1280 38"
            fill="none"
            stroke="url(#oro-fascia)"
            strokeWidth="5"
            strokeLinecap="round"
          />
        </svg>
        <div className="fascia-testo">
          <h1>Domanda di iscrizione</h1>
          <p>
            Compila il modulo per diventare socio. Il direttivo esaminerà la
            domanda e ti risponderà entro 60 giorni.
          </p>
        </div>
      </section>

      <div className="pagina-form">
        {inviata ? (
          <div className="esito" role="status">
            <h2>Dati pronti per l'invio</h2>
            <p>(Prova: l'invio al server arriva nei prossimi passi.)</p>
            <pre>{JSON.stringify(inviata, null, 2)}</pre>
            <button
              type="button"
              className="btn btn-verde"
              onClick={() => {
                setInviata(null);
                setDati(VUOTO);
              }}
            >
              Nuova domanda
            </button>
          </div>
        ) : (
          <form onSubmit={invia} noValidate>
            <fieldset>
              <legend>Dati personali</legend>
              <div className="riga">
                {campo("nome", "Nome")}
                {campo("cognome", "Cognome")}
              </div>
              <div className="riga">
                {campo("codiceFiscale", "Codice fiscale", {
                  maxLength: 16,
                  maiuscolo: true,
                })}
                {campo("dataNascita", "Data di nascita", { tipo: "date" })}
              </div>
              <div className="riga">
                {campo("email", "Email", { tipo: "email" })}
                {campo("telefono", "Telefono", {
                  tipo: "tel",
                  facoltativo: true,
                })}
              </div>
            </fieldset>

            <fieldset>
              <legend>Residenza</legend>
              <div className="riga">
                {campo("indirizzo", "Indirizzo e numero civico", {
                  larghezza: "1 1 100%",
                })}
              </div>
              <div className="riga">
                {campo("cap", "CAP", { maxLength: 5, larghezza: "1 1 120px" })}
                {campo("citta", "Città", { larghezza: "3 1 220px" })}
                {campo("provincia", "Provincia", {
                  maxLength: 2,
                  maiuscolo: true,
                  larghezza: "1 1 100px",
                })}
              </div>
            </fieldset>

            <fieldset>
              <legend>Privacy e consensi</legend>
              <div
                className="informativa"
                tabIndex={0}
                aria-label="Testo dell'informativa"
              >
                <strong>
                  Informativa sul trattamento dei dati personali · versione
                  [1.0]
                </strong>
                <br />
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. In
                sodales urna eu justo aliquam, ac suscipit risus faucibus. Etiam
                a tristique purus. Nunc volutpat eu nunc vitae interdum.
                Phasellus ipsum libero, volutpat vitae nulla non, vulputate
                auctor ante. Phasellus luctus felis velit, ut aliquet eros
                cursus vel. In porttitor, orci et fermentum tincidunt, mauris
                dui tristique neque, non convallis sapien libero ac quam. Duis a
                leo tellus. Nam vestibulum, nibh eget congue accumsan, nulla
                nibh faucibus tellus, id scelerisque arcu purus vitae urna.
                Vivamus vehicula, lorem id aliquet accumsan, sem lectus ornare
                dui, accumsan placerat mauris risus eget mi. Duis pulvinar purus
                dui.
              </div>
              <div className="spunta">
                <input
                  id="consensoInformativa"
                  type="checkbox"
                  checked={dati.consensoInformativa}
                  aria-invalid={errori.consensoInformativa ? true : undefined}
                  onChange={(ev) =>
                    spunta("consensoInformativa", ev.target.checked)
                  }
                />
                <label htmlFor="consensoInformativa">
                  Ho letto l'informativa e acconsento al trattamento dei miei
                  dati per la gestione della domanda di iscrizione.{" "}
                  <strong className="obbligatorio">Obbligatorio</strong>
                </label>
              </div>
              {errori.consensoInformativa && (
                <span className="errore" role="alert">
                  {errori.consensoInformativa}
                </span>
              )}
              <div className="spunta">
                <input
                  id="newsletter"
                  type="checkbox"
                  checked={dati.newsletter}
                  onChange={(ev) => spunta("newsletter", ev.target.checked)}
                />
                <label htmlFor="newsletter">
                  Desidero ricevere la newsletter di TeatrAmico.{" "}
                  <span className="facoltativo">Facoltativo</span>
                </label>
              </div>
              <div className="spunta">
                <input
                  id="foto"
                  type="checkbox"
                  checked={dati.foto}
                  onChange={(ev) => spunta("foto", ev.target.checked)}
                />
                <label htmlFor="foto">
                  Acconsento all'uso di foto e riprese degli eventi.{" "}
                  <span className="facoltativo">Facoltativo</span>
                </label>
              </div>
            </fieldset>

            <div className="invio">
              <p>
                Riceverai una conferma con la data entro cui il direttivo è
                tenuto a risponderti.
              </p>
              <button type="submit" className="btn btn-verde">
                Invia la domanda
              </button>
            </div>
          </form>
        )}
      </div>
    </>
  );
}
