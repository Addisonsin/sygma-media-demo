import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import Shell from "../components/Shell";

type Props = { me: { email: string; role: string }; onLogout: () => void };

export default function AgencyNewClient({ me, onLogout }: Props) {
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function submit(e: FormEvent) {
    e.preventDefault();
    try {
      await api("/api/v1/agency/clients", { method: "POST", body: JSON.stringify({ name }) });
      navigate("/agency");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  }

  return (
    <Shell title="New client" me={me} onLogout={onLogout} links={[{ to: "/agency", label: "Clients" }]}>
      <h1>Add client</h1>
      <form className="card" style={{ maxWidth: 480 }} onSubmit={submit}>
        <div className="field">
          <label>Client name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        {error ? <p style={{ color: "var(--danger)" }}>{error}</p> : null}
        <button className="btn" type="submit">
          Create client
        </button>
        <Link to="/agency" className="muted" style={{ marginLeft: "1rem" }}>
          Cancel
        </Link>
      </form>
    </Shell>
  );
}
