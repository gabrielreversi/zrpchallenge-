import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../auth/fakeAuth';

export function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    login(username, password);
    navigate('/');
  }

  return (
    <div className="page page--center">
      <form className="login-card" onSubmit={handleSubmit}>
        <p className="eyebrow">Consultoria</p>
        <h1 className="display">Curadoria de talentos</h1>
        <p className="lede">Acesso interno — use qualquer usuário e senha.</p>
        <label className="field">
          <span>Usuário</span>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
        </label>
        <label className="field">
          <span>Senha</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />
        </label>
        <button type="submit" className="btn btn--primary">
          Entrar
        </button>
      </form>
    </div>
  );
}
