import { Link } from "react-router-dom";
import "./Home.css";

// Il motto dell'associazione: se è vuoto, la riga non viene mostrata.
const MOTTO = "";

const PASSAGGI = [
  {
    titolo: "Invia la domanda",
    testo: "Compili il modulo online e accetti l'informativa sulla privacy.",
  },
  {
    titolo: "Il direttivo delibera",
    testo:
      "I sette membri votano. Se la domanda è rigettata ricevi la motivazione.",
  },
  {
    titolo: "Ricevi tessera e accesso",
    testo: "Attivi il tuo account e puoi iscriverti ai corsi.",
  },
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="raggio raggio-sx" aria-hidden="true" />
        <div className="raggio raggio-dx" aria-hidden="true" />
        <div className="raggio raggio-centro" aria-hidden="true" />

        <svg
          className="onda"
          aria-hidden="true"
          viewBox="0 0 1280 200"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="oro-onda" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="#B8862B" />
              <stop offset="0.5" stopColor="#E3C26B" />
              <stop offset="1" stopColor="#B8862B" />
            </linearGradient>
          </defs>
          <path
            d="M0 150 C 340 60, 740 190, 1280 80 L1280 200 L0 200 Z"
            fill="#F6F0DF"
          />
          <path
            d="M0 136 C 340 46, 740 176, 1280 66"
            fill="none"
            stroke="#E3C26B"
            strokeWidth="2"
            strokeLinecap="round"
            opacity="0.55"
          />
          <path
            d="M0 150 C 340 60, 740 190, 1280 80"
            fill="none"
            stroke="url(#oro-onda)"
            strokeWidth="5"
            strokeLinecap="round"
          />
        </svg>

        <div className="hero-contenuto">
          <h1 aria-label="TeatrAmico" className="marchio">
            <span aria-hidden="true" className="marchio-lato">
              Teatr
            </span>
            <span aria-hidden="true" className="marchio-a">
              A
            </span>
            <span aria-hidden="true" className="marchio-lato">
              mico
            </span>
          </h1>
          <p className="sottotitolo">Associazione culturale di teatro</p>
          {MOTTO && <p className="motto">{MOTTO}</p>}
          <div className="azioni">
            <Link to="/iscrizione" className="btn btn-oro">
              Diventa socio
            </Link>
            <Link to="/corsi" className="btn btn-contorno">
              Scopri i corsi
            </Link>
          </div>
        </div>
      </section>

      <section id="soci" className="soci">
        <div className="soci-interno">
          <h2>Come si diventa soci</h2>
          <p className="soci-intro">
            Ai corsi si iscrivono i soci. L'ammissione è deliberata dal
            direttivo, che risponde entro 60 giorni.
          </p>
          <ol className="passaggi">
            {PASSAGGI.map((p, i) => (
              <li key={p.titolo}>
                <span className="numero" aria-hidden="true">
                  {i + 1}
                </span>
                <h3>{p.titolo}</h3>
                <p>{p.testo}</p>
              </li>
            ))}
          </ol>
          <div className="soci-azione">
            <Link to="/iscrizione" className="btn btn-oro">
              Diventa socio
            </Link>
          </div>
        </div>
      </section>

      <section id="chi-siamo" className="chi-siamo">
        <h2>Chi siamo</h2>
        <p>
          [Presentazione dell'associazione: storia, sede, attività, spettacoli.]
        </p>
      </section>
    </>
  );
}
