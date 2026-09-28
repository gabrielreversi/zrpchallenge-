const AUTH_KEY = 'curadoria_auth';

export function isAuthenticated(): boolean {
  return sessionStorage.getItem(AUTH_KEY) === 'true';
}

export function login(_username: string, _password: string): void {
  sessionStorage.setItem(AUTH_KEY, 'true');
}

export function logout(): void {
  sessionStorage.removeItem(AUTH_KEY);
}
