import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api";

type Overview = {
  content_documents: number;
  media_assets: number;
  blog_posts_managed: number;
  last_publish_status: string | null;
};

type Props = { websiteId: string };

export default function OverviewPanel({ websiteId }: Props) {
  const [data, setData] = useState<Overview | null>(null);

  useEffect(() => {
    api<Overview>(`/api/v1/websites/${websiteId}/overview`).then(setData);
  }, [websiteId]);

  if (!data) return <p className="muted">Loading…</p>;

  return (
    <>
      <h1 style={{ marginTop: 0 }}>Dashboard</h1>
      <p className="muted">Welcome — edit your site like WordPress, then publish when ready.</p>
      <div className="grid" style={{ marginTop: "1.25rem" }}>
        <div className="card stat-card">
          <h3>Content docs</h3>
          <p style={{ fontSize: "1.75rem", margin: "0.25rem 0" }}>{data.content_documents}</p>
        </div>
        <div className="card stat-card">
          <h3>Media files</h3>
          <p style={{ fontSize: "1.75rem", margin: "0.25rem 0" }}>{data.media_assets}</p>
        </div>
        <div className="card stat-card">
          <h3>Blog posts (CMS)</h3>
          <p style={{ fontSize: "1.75rem", margin: "0.25rem 0" }}>{data.blog_posts_managed}</p>
        </div>
        <div className="card stat-card">
          <h3>Last publish</h3>
          <p style={{ margin: "0.35rem 0" }}>
            {data.last_publish_status ? (
              <span className={`badge ${data.last_publish_status === "succeeded" ? "success" : "warn"}`}>
                {data.last_publish_status}
              </span>
            ) : (
              "—"
            )}
          </p>
        </div>
      </div>
      <div className="card" style={{ marginTop: "1.25rem" }}>
        <h3>Quick actions</h3>
        <div className="save-bar" style={{ marginTop: "0.75rem" }}>
          <Link to={`/websites/${websiteId}/homepage`} className="btn">
            Edit homepage
          </Link>
          <Link to={`/websites/${websiteId}/blog`} className="btn secondary">
            Write blog post
          </Link>
          <Link to={`/websites/${websiteId}/publish`} className="btn secondary">
            Publish site
          </Link>
        </div>
      </div>
    </>
  );
}
