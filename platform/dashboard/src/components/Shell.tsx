import { Link } from "react-router-dom";

type LinkItem = { to: string; label: string; active?: boolean };

type Props = {
  title: string;
  me: { email: string; role: string };
  onLogout: () => void;
  links: LinkItem[];
  children: React.ReactNode;
};

export default function Shell({ title, me, onLogout, links, children }: Props) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">Sygma Platform</div>
        <div className="muted" style={{ marginBottom: "1rem", fontSize: "0.85rem" }}>
          {me.role.replace(/_/g, " ")}
        </div>
        <nav className="nav">
          {links.map((l) => (
            <Link key={l.label} to={l.to} className={l.active ? "active" : undefined}>
              {l.label}
            </Link>
          ))}
        </nav>
        <button type="button" className="btn secondary" style={{ marginTop: "2rem", width: "100%" }} onClick={onLogout}>
          Sign out
        </button>
      </aside>
      <main className="main">
        <p className="muted" style={{ marginTop: 0 }}>
          {title}
        </p>
        {children}
      </main>
    </div>
  );
}
