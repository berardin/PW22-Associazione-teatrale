import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function App() {
  const [stato, setStato] = useState("verifica in corso...");

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((r) => r.json())
      .then((dati) => setStato(`backend: ${dati.status}`))
      .catch(() => setStato("backend non raggiungibile"));
  }, []);

  return (
    <main>
      <h1>TeatrAmico</h1>
      <p>{stato}</p>
    </main>
  );
}

export default App;
