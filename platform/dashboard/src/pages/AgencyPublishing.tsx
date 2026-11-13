import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import Shell from "../components/Shell";

type Job = {
  id: string;
  status: string;
  website_name: string;
  website_slug: string;
  website_id: string;
  build_path: string | null;
  error_message: string | null;
  created_at: string;
};

type Props = { me: { email: string; role: string }; onLogout: () => void };

export default function AgencyPublishing({ me, onLogout }: Props) {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    api<Job[]>("/api/v1/agency/publish/jobs").then(setJobs).catch(console.error);
  }, []);

  return (
    <Shell
      title="Publishing"
      me={me}
      onLogout={onLogout}
      links={[
        { to: "/agency", label: "Clients" },
        { to: "/agency/publishing", label: "Publishing", active: true },
      ]}
    >
      <h1>Publishing monitor</h1>
      <p className="muted">Recent builds across all client websites.</p>
      {jobs.map((j) => (
        <div key={j.id} className="card">
          <strong>{j.website_name}</strong> — {j.status}
          <p className="muted">{new Date(j.created_at).toLocaleString()}</p>
          <Link to={`/websites/${j.website_id}`}>Open workspace</Link>
          {j.build_path ? <p className="muted">Build: {j.build_path}</p> : null}
          {j.error_message ? <p style={{ color: "var(--danger)" }}>{j.error_message}</p> : null}
        </div>
      ))}
    </Shell>
  );
}
