import { Navigate, Outlet } from 'react-router-dom';
import { isAuthenticated } from '../auth/fakeAuth';

export function ProtectedRoute() {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
}
