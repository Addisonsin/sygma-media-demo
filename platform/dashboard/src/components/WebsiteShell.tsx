import { Link, NavLink } from "react-router-dom";
import { getToken } from "../api";

const NAV = [
  { key: "overview", label: "Dashboard", icon: "◫" },
  { key: "homepage", label: "Homepage", icon: "⌂" },
  { key: "pages", label: "Pages", icon: "☰" },
  { key: "blog", label: "Blog", icon: "✎" },
  { key: "settings", label: "Contact & SEO", icon: "⚙" },
  { key: "media", label: "Media", icon: "🖼" },
  { key: "publish", label: "Publish", icon: "↗" },
];

type Props = {
  websiteId: string;
  siteName: string;
  me: { role: string };
  onLogout: () => void;
  children: React.ReactNode;
  topRight?: React.ReactNode;
};

export default function WebsiteShell({ websiteId, siteName, me, onLogout, children, topRight }: Props) {
  const back = me.role.startsWith("agency") ? "/agency" : "/client";

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="brand">Sygma CMS</div>
        <div className="site-name">{siteName}</div>
        <nav className="app-nav">
          {NAV.map((item) => (
            <NavLink
              key={item.key}
              to={`/websites/${websiteId}/${item.key}`}
              className={({ isActive }) => (isActive ? "active" : undefined)}
            >
              <span aria-hidden="true">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div style={{ marginTop: "auto", padding: "1rem" }}>
          <Link to={back} style={{ color: "#a7aaad", fontSize: "0.85rem" }}>
            ← All sites
          </Link>
          <button type="button" className="btn secondary" style={{ width: "100%", marginTop: "0.75rem" }} onClick={onLogout}>
            Sign out
          </button>
        </div>
      </aside>
      <div className="app-main">
        <header className="app-topbar">
          <TitleBlock siteName={siteName} />
          <div className="save-bar">{topRight}</div>
        </header>
        <div className="app-content">{children}</div>
      </div>
    </div>
  );
}

function TitleBlock({ siteName }: { siteName: string }) {
  return (
    <div>
      <strong>{siteName}</strong>
      <div className="muted" style={{ fontSize: "0.8rem" }}>
        Content management
      </div>
    </div>
  );
}

export function mediaFileUrl(websiteId: string, assetId: string): string {
  const token = getToken();
  const q = token ? `?access_token=${encodeURIComponent(token)}` : "";
  return `/api/v1/websites/${websiteId}/media/${assetId}/file${q}`;
}
