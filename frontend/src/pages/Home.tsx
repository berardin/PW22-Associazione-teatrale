import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [stato, setStato] = useState("verifica in corso...");

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((r) => r.json())
      .then((dati) => setStato(`backend: ${dati.status}`))
      .catch(() => setStato("backend non raggiungibile"));
  }, []);

  return (
    <section style={{ padding: "48px" }}>
      <h1>Home</h1>
      <p>{stato}</p>
    </section>
  );
}
