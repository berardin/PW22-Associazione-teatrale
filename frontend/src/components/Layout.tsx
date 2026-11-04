import { NavLink, Outlet } from "react-router-dom";

function Logo() {
  return (
    <NavLink to="/" className="logo" aria-label="TeatrAmico, home">
      <span aria-hidden="true">Teatr</span>
      <span aria-hidden="true" className="logo-a">
        A
      </span>
      <span aria-hidden="true">mico</span>
    </NavLink>
  );
}

export default function Layout() {
  const classe = ({ isActive }: { isActive: boolean }) =>
    isActive ? "attivo" : undefined;

  return (
    <div className="layout">
      <header className="header">
        <Logo />
        <nav className="nav" aria-label="Principale">
          <NavLink to="/corsi" className={classe}>
            Corsi
          </NavLink>
          <NavLink to="/#chi-siamo">Chi siamo</NavLink>
          <NavLink to="/iscrizione" className={classe}>
            Diventa socio
          </NavLink>
          <NavLink to="/accesso" className="accedi">
            Accedi
          </NavLink>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer className="footer">
        <strong>TeatrAmico</strong>
        <span>[Indirizzo della sede] · [email] · [telefono]</span>
        <span>Informativa privacy · Statuto</span>
      </footer>
    </div>
  );
}
