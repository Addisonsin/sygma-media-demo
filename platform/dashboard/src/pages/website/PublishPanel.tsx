import { useEffect, useState } from "react";
import { api, getToken } from "../../api";

type Job = { id: string; status: string; build_path: string | null; error_message: string | null };
type Preview = { homepage_preview_url: string };

type Props = { websiteId: string; onToast: (m: string) => void };

export default function PublishPanel({ websiteId, onToast }: Props) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  function load() {
    api<Job[]>(`/api/v1/websites/${websiteId}/publish/jobs`).then(setJobs);
    api<Preview>(`/api/v1/websites/${websiteId}/preview/latest`)
      .then((p) => setPreviewUrl(p.homepage_preview_url))
      .catch(() => setPreviewUrl(null));
  }

  useEffect(() => {
    load();
  }, [websiteId]);

  async function run() {
    const job = await api<Job>(`/api/v1/websites/${websiteId}/publish`, { method: "POST" });
    onToast(job.status === "succeeded" ? "Build OK — check preview" : job.status);
    load();
  }

  function openPreview() {
    if (!previewUrl) return;
    const token = getToken();
    const q = token ? `?access_token=${encodeURIComponent(token)}` : "";
    window.open(`${previewUrl}${q}`, "_blank");
  }

  return (
    <>
      <h1 style={{ marginTop: 0 }}>Publish</h1>
      <PublishSteps />
      <div className="card">
        <p className="muted">Build copies the static site and patches published HTML. Does not deploy to Cloudflare until configured.</p>
        <button type="button" className="btn" onClick={run}>
          Run publish build
        </button>
        {previewUrl ? (
          <button type="button" className="btn secondary" style={{ marginLeft: "0.75rem" }} onClick={openPreview}>
            Preview homepage (auth required)
          </button>
        ) : null}
      </div>
      <h2 style={{ marginTop: "2rem" }}>History</h2>
      {jobs.map((j) => (
        <div key={j.id} className="card">
          <strong>{j.status}</strong>
          {j.build_path ? <p className="muted">{j.build_path}</p> : null}
          {j.error_message ? <p style={{ color: "var(--danger)" }}>{j.error_message}</p> : null}
        </div>
      ))}
    </>
  );
}

function PublishSteps() {
  return (
    <div className="grid" style={{ marginBottom: "1rem" }}>
      <PublishStep n={1} label="Edit & publish content in each section" />
      <PublishStep n={2} label="Run publish build below" />
      <PublishStep n={3} label="Preview, then deploy (when enabled)" />
    </div>
  );
}

function PublishStep({ n, label }: { n: number; label: string }) {
  return (
    <div className="card" style={{ marginBottom: 0 }}>
      <span className="badge">{n}</span> <span style={{ marginLeft: "0.35rem" }}>{label}</span>
    </div>
  );
}
