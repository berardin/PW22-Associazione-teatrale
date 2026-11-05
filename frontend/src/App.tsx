import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Vuota from "./pages/Vuota";
import Iscrizione from "./pages/Iscrizione";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<Vuota />} />
        <Route path="/iscrizione" element={<Iscrizione />} />
      </Route>
    </Routes>
  );
}
