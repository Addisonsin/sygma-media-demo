import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import Shell from "../components/Shell";

type Website = { id: string; name: string; slug: string; public_domain: string | null };
type Client = { id: string; name: string; websites: Website[] };

type Props = { me: { email: string; role: string }; onLogout: () => void };

export default function AgencyHome({ me, onLogout }: Props) {
  const [clients, setClients] = useState<Client[]>([]);

  useEffect(() => {
    api<Client[]>("/api/v1/agency/clients").then(setClients).catch(console.error);
  }, []);

  return (
    <Shell
      title="Agency"
      me={me}
      onLogout={onLogout}
      links={[
        { to: "/agency", label: "Clients", active: true },
        { to: "/agency/publishing", label: "Publishing" },
      ]}
    >
      <h1 style={{ marginTop: 0 }}>Agency dashboard</h1>
      <p className="muted">Register clients, open a site workspace, or edit on their behalf.</p>
      <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", margin: "1rem 0 1.5rem" }}>
        <Link to="/agency/clients/new" className="btn">
          Add client
        </Link>
        <Link to="/agency/websites/new" className="btn secondary">
          Register website
        </Link>
        <Link to="/agency/users/new" className="btn secondary">
          Invite client user
        </Link>
      </div>
      <div className="grid" style={{ marginTop: "1.5rem" }}>
        {clients.map((c) => (
          <ClientCard key={c.id} client={c} />
        ))}
      </div>
    </Shell>
  );
}

function ClientCard({ client }: { client: Client }) {
  return (
    <div className="card">
      <h3>{client.name}</h3>
      <p className="muted">{client.websites.length} website(s)</p>
      {client.websites.map((w) => (
        <p key={w.id}>
          <Link to={`/websites/${w.id}/overview`}>{w.name}</Link>
          {w.public_domain ? <span className="muted"> · {w.public_domain}</span> : null}
        </p>
      ))}
    </div>
  );
}
