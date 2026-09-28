import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { IndexPage } from './pages/IndexPage';
import { LoginPage } from './pages/LoginPage';
import { MatchPage } from './pages/MatchPage';
import { isAuthenticated } from './auth/fakeAuth';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated() ? <Navigate to="/" replace /> : <LoginPage />
          }
        />
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<MatchPage />} />
          <Route path="/index" element={<IndexPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
