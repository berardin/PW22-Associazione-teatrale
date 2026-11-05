import { useEffect } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router-dom";

function Logo() {
  return (
    <Link to="/" className="logo" aria-label="TeatrAmico, home">
      <span aria-hidden="true">Teatr</span>
      <span aria-hidden="true" className="logo-a">
        A
      </span>
      <span aria-hidden="true">mico</span>
    </Link>
  );
}

export default function Layout() {
  const { pathname, hash } = useLocation();
  const classe = ({ isActive }: { isActive: boolean }) =>
    isActive ? "attivo" : undefined;

  // Scorre al punto indicato dall'ancora; senza ancora torna in cima.
  useEffect(() => {
    if (hash) document.getElementById(hash.slice(1))?.scrollIntoView();
    else window.scrollTo(0, 0);
  }, [pathname, hash]);

  return (
    <div className="layout">
      <header className="header">
        <Logo />
        <nav className="nav" aria-label="Principale">
          <NavLink to="/corsi" className={classe}>
            Corsi
          </NavLink>
          <Link to="/#chi-siamo">Chi siamo</Link>
          <NavLink to="/iscrizione" className={classe}>
            Diventa socio
          </NavLink>
          <Link to="/#contatti">Contatti</Link>
          <NavLink to="/accesso" className="accedi">
            Accedi
          </NavLink>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer id="contatti" className="footer">
        <div className="riquadro">
          <strong>Sede</strong>
          <span>[Indirizzo della sede]</span>
        </div>
        <div className="riquadro">
          <strong>Info e contatti</strong>
          <span>[email] · [telefono]</span>
        </div>
        <div className="riquadro">
          <strong>Informazioni</strong>
          <Link to="/privacy">Informativa privacy</Link>
          <Link to="/statuto">Statuto</Link>
        </div>
      </footer>
    </div>
  );
}
