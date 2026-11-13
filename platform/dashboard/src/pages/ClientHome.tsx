import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import Shell from "../components/Shell";

type Website = { id: string; name: string; slug: string; public_domain: string | null };
type Props = { me: { email: string; role: string }; onLogout: () => void };

export default function ClientHome({ me, onLogout }: Props) {
  const [sites, setSites] = useState<Website[]>([]);

  useEffect(() => {
    api<Website[]>("/api/v1/websites").then(setSites).catch(console.error);
  }, []);

  return (
    <Shell title="My website" me={me} onLogout={onLogout} links={[{ to: "/client", label: "Overview" }]}>
      <h1 style={{ marginTop: 0 }}>Your websites</h1>
      <p className="muted">Edit text, images, and pages — then preview and publish.</p>
      <div className="grid" style={{ marginTop: "1.5rem" }}>
        {sites.map((w) => (
          <Link key={w.id} to={`/websites/${w.id}/overview`} className="card" style={{ textDecoration: "none", color: "inherit" }}>
            <h3>{w.name}</h3>
            <p className="muted">{w.public_domain ?? w.slug}</p>
            <span className="badge">Open editor</span>
          </Link>
        ))}
      </div>
    </Shell>
  );
}
