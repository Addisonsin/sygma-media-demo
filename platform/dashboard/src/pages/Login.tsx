import { FormEvent, useState } from "react";
import { api } from "../api";

type Props = { onLogin: (token: string, role: string) => void };

export default function Login({ onLogin }: Props) {
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("ChangeMeNow!");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const res = await api<{ access_token: string; role: string }>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      onLogin(res.access_token, res.role);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "linear-gradient(160deg, #1d2327 0%, #2271b1 120%)" }}>
      <div className="card login-wrap" style={{ width: "100%", maxWidth: 420 }}>
        <div className="login-brand">
          <h1>Sygma CMS</h1>
          <p className="muted">Manage client websites — content, media, and publishing.</p>
        </div>
        <form onSubmit={submit}>
          <div className="field">
            <label>Email</label>
            <input value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="username" />
          </div>
          <div className="field">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
          </div>
          {error ? <p style={{ color: "var(--danger)" }}>{error}</p> : null}
          <button className="btn" disabled={busy} type="submit" style={{ width: "100%" }}>
            {busy ? "Signing in…" : "Log in"}
          </button>
        </form>
      </div>
    </div>
  );
}
