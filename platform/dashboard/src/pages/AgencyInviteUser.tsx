import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import Shell from "../components/Shell";

type Website = { id: string; name: string };
type Props = { me: { email: string; role: string }; onLogout: () => void };

export default function AgencyInviteUser({ me, onLogout }: Props) {
  const [sites, setSites] = useState<Website[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("client_owner");
  const [msg, setMsg] = useState("");

  useEffect(() => {
    api<Website[]>("/api/v1/websites").then(setSites);
  }, []);

  function toggle(id: string) {
    setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  }

  async function submit(e: FormEvent) {
    e.preventDefault();
    try {
      await api("/api/v1/agency/users/client", {
        method: "POST",
        body: JSON.stringify({ email, password, role, website_ids: selected, can_publish: true }),
      });
      setMsg(`Created ${email}`);
    } catch (err) {
      setMsg(err instanceof Error ? err.message : "Failed");
    }
  }

  return (
    <Shell title="Invite client user" me={me} onLogout={onLogout} links={[{ to: "/agency", label: "Clients" }]}>
      <h1>Client account</h1>
      <form className="card" style={{ maxWidth: 560 }} onSubmit={submit}>
        <div className="field">
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="field">
          <label>Temporary password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={10} required />
        </div>
        <div className="field">
          <label>Role</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="client_owner">Owner</option>
            <option value="client_editor">Editor</option>
          </select>
        </div>
        <div className="field">
          <label>Website access</label>
          {sites.map((w) => (
            <label key={w.id} style={{ display: "flex", gap: "0.5rem", marginBottom: "0.35rem" }}>
              <input type="checkbox" checked={selected.includes(w.id)} onChange={() => toggle(w.id)} />
              {w.name}
            </label>
          ))}
        </div>
        <button className="btn" type="submit" disabled={!selected.length}>
          Create user
        </button>
        <Link to="/agency" className="muted" style={{ marginLeft: "1rem" }}>
          Back
        </Link>
      </form>
      {msg ? <p className="toast" style={{ position: "static", marginTop: "1rem" }}>{msg}</p> : null}
    </Shell>
  );
}
