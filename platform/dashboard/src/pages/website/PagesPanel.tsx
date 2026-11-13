import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api";

type Page = { label: string; path: string; url: string; exists: boolean; editable: boolean };

type Props = { websiteId: string };

export default function PagesPanel({ websiteId }: Props) {
  const [pages, setPages] = useState<Page[]>([]);

  useEffect(() => {
    api<Page[]>(`/api/v1/websites/${websiteId}/pages`).then(setPages);
  }, [websiteId]);

  return (
    <>
      <h1 style={{ marginTop: 0 }}>Pages</h1>
      <p className="muted">All site routes — editable pages open in the content editor.</p>
      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <table className="table" style={{ margin: 0 }}>
          <thead>
            <tr>
              <th>Page</th>
              <th>URL</th>
              <th>File</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {pages.map((p) => (
              <tr key={p.path}>
                <td>
                  <strong>{p.label}</strong>
                </td>
                <td className="muted">{p.url}</td>
                <td>
                  {p.exists ? <span className="badge success">On disk</span> : <span className="badge warn">Missing</span>}
                </td>
                <td>
                  {p.label === "Home" ? (
                    <Link to={`/websites/${websiteId}/homepage`}>Edit</Link>
                  ) : p.label === "Contact" ? (
                    <Link to={`/websites/${websiteId}/settings`}>Edit</Link>
                  ) : (
                    <span className="muted">Soon</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
