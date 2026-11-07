// Lib per le chiamate API al Backend.
export const API_URL: string =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000";

// Errore: stato HTTP (0 se il server non risponde) e
// dettaglio restituito da FastAPI (stringa per 4xx, lista di errori per 422).
export class ErroreApi extends Error {
  stato: number;
  dettaglio: unknown;

  constructor(stato: number, dettaglio: unknown, messaggio: string) {
    super(messaggio);
    this.name = "ErroreApi";
    this.stato = stato;
    this.dettaglio = dettaglio;
  }
}

// Documento versionato (informativa privacy, statuto).
export type Documento = {
  versione: string;
  testo: string;
  in_vigore_dal: string; // aaaa-mm-gg
};

// Risposta di POST /domande.
export type DomandaCreata = {
  id: number;
  stato: string;
  data_presentazione: string; // aaaa-mm-gg
  scadenza_risposta: string; // aaaa-mm-gg
};

export async function chiama<T>(
  percorso: string,
  opzioni: RequestInit = {},
): Promise<T> {
  let risposta: Response;
  try {
    risposta = await fetch(API_URL + percorso, {
      ...opzioni,
      headers: { "Content-Type": "application/json", ...opzioni.headers },
    });
  } catch {
    throw new ErroreApi(0, null, "Il server non risponde.");
  }

  const corpo = await risposta.json().catch(() => null);
  if (!risposta.ok) {
    const dettaglio = corpo?.detail ?? null;
    const messaggio =
      typeof dettaglio === "string" ? dettaglio : `Errore ${risposta.status}`;
    throw new ErroreApi(risposta.status, dettaglio, messaggio);
  }
  return corpo as T;
}
