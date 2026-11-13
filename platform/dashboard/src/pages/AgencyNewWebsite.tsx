import { FormEvent, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import Shell from "../components/Shell";

type Client = { id: string; name: string };
type Props = { me: { email: string; role: string }; onLogout: () => void };

export default function AgencyNewWebsite({ me, onLogout }: Props) {
  const [clients, setClients] = useState<Client[]>([]);
  const [clientId, setClientId] = useState("");
  const [slug, setSlug] = useState("");
  const [name, setName] = useState("");
  const [domain, setDomain] = useState("");
  const [staticRoot, setStaticRoot] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api<{ id: string; name: string }[]>("/api/v1/agency/clients").then((c) => {
      setClients(c);
      if (c[0]) setClientId(c[0].id);
    });
  }, []);

  async function submit(e: FormEvent) {
    e.preventDefault();
    try {
      await api("/api/v1/agency/websites", {
        method: "POST",
        body: JSON.stringify({
          client_id: clientId,
          slug,
          name,
          public_domain: domain || null,
          static_root: staticRoot,
        }),
      });
      navigate("/agency");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  }

  return (
    <Shell title="New website" me={me} onLogout={onLogout} links={[{ to: "/agency", label: "Clients" }]}>
      <h1>Register website</h1>
      <form className="card" style={{ maxWidth: 560 }} onSubmit={submit}>
        <div className="field">
          <label>Client</label>
          <select value={clientId} onChange={(e) => setClientId(e.target.value)} required>
            {clients.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Website name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="field">
          <label>Slug (URL key)</label>
          <input value={slug} onChange={(e) => setSlug(e.target.value)} pattern="[a-z0-9-]+" required />
        </div>
        <div className="field">
          <label>Public domain</label>
          <input value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="example.com" />
        </div>
        <div className="field">
          <label>Static site root (absolute path on server)</label>
          <input value={staticRoot} onChange={(e) => setStaticRoot(e.target.value)} required />
        </div>
        {error ? <p style={{ color: "var(--danger)" }}>{error}</p> : null}
        <button className="btn" type="submit">
          Register website
        </button>
        <Link to="/agency" className="muted" style={{ marginLeft: "1rem" }}>
          Cancel
        </Link>
      </form>
    </Shell>
  );
}
