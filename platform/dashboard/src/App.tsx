import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { api, getToken, setToken } from "./api";
import AgencyHome from "./pages/AgencyHome";
import AgencyInviteUser from "./pages/AgencyInviteUser";
import AgencyNewClient from "./pages/AgencyNewClient";
import AgencyNewWebsite from "./pages/AgencyNewWebsite";
import AgencyPublishing from "./pages/AgencyPublishing";
import ClientHome from "./pages/ClientHome";
import Login from "./pages/Login";
import WebsiteWorkspace from "./pages/WebsiteWorkspace";

type Me = { role: string; email: string };

export default function App() {
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setLoading(false);
      return;
    }
    api<Me>("/api/v1/auth/me")
      .then(setMe)
      .catch(() => setToken(null))
      .finally(() => setLoading(false));
  }, []);

  function onLogin(token: string, role: string) {
    setToken(token);
    setMe({ role, email: "" });
    navigate(role.startsWith("agency") ? "/agency" : "/client");
  }

  function logout() {
    setToken(null);
    setMe(null);
    navigate("/login");
  }

  if (loading) {
    return (
      <div className="login-wrap card">
        <p className="muted">Loading platform…</p>
      </div>
    );
  }

  const agency = me?.role.startsWith("agency") ? me : null;

  return (
    <Routes>
      <Route path="/login" element={me ? <Navigate to={agency ? "/agency" : "/client"} /> : <Login onLogin={onLogin} />} />
      <Route path="/agency" element={agency ? <AgencyHome me={me!} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="/agency/clients/new" element={agency ? <AgencyNewClient me={me!} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="/agency/websites/new" element={agency ? <AgencyNewWebsite me={me!} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="/agency/users/new" element={agency ? <AgencyInviteUser me={me!} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="/agency/publishing" element={agency ? <AgencyPublishing me={me!} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="/client" element={me && !agency ? <ClientHome me={me} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="/websites/:id" element={<Navigate to="overview" replace />} />
      <Route path="/websites/:id/:section" element={me ? <WebsiteWorkspace me={me} onLogout={logout} /> : <Navigate to="/login" />} />
      <Route path="*" element={<Navigate to={me ? (agency ? "/agency" : "/client") : "/login"} />} />
    </Routes>
  );
}
