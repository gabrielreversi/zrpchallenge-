import type { ReactNode } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { logout } from '../auth/fakeAuth';

export function AppShell({ children }: { children: ReactNode }) {
  const navigate = useNavigate();

  return (
    <div className="shell">
      <header className="topbar">
        <div className="topbar__brand">Curadoria</div>
        <nav className="topbar__tabs" aria-label="Principal">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'tab tab--active' : 'tab')}>
            Curadoria
          </NavLink>
          <NavLink
            to="/index"
            className={({ isActive }) => (isActive ? 'tab tab--active' : 'tab')}
          >
            Indexação
          </NavLink>
        </nav>
        <button
          type="button"
          className="btn btn--ghost"
          onClick={() => {
            logout();
            navigate('/login');
          }}
        >
          Sair
        </button>
      </header>
      <main className="shell__main">{children}</main>
    </div>
  );
}
