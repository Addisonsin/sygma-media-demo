import { useEffect, useState } from "react";
import { api, getToken } from "../../api";

type Props = { websiteId: string; onToast: (m: string) => void; onSaving?: (v: boolean) => void };

export default function HomepagePanel({ websiteId, onToast, onSaving }: Props) {
  const [line1, setLine1] = useState("");
  const [line2, setLine2] = useState("");
  const [metaTitle, setMetaTitle] = useState("");
  const [metaDesc, setMetaDesc] = useState("");
  const [previewSrc, setPreviewSrc] = useState<string | null>(null);

  useEffect(() => {
    api<{ payload?: { hero?: Record<string, string> } } | null>(
      `/api/v1/websites/${websiteId}/content/homepage/default?status=draft`,
    )
      .then((rev) => {
        if (rev?.payload?.hero) applyHero(rev.payload.hero);
        else
          api<{ payload?: { hero?: Record<string, string> } } | null>(
            `/api/v1/websites/${websiteId}/content/homepage/default?status=published`,
          ).then((pub) => {
            if (pub?.payload?.hero) applyHero(pub.payload.hero);
          });
      })
      .catch(() => undefined);
    const token = getToken();
    api<{ homepage_preview_url: string }>(`/api/v1/websites/${websiteId}/preview/latest`)
      .then((p) => setPreviewSrc(`${p.homepage_preview_url}?access_token=${encodeURIComponent(token || "")}`))
      .catch(() => setPreviewSrc(null));
  }, [websiteId]);

  function applyHero(h: Record<string, string>) {
    setLine1(h.line1 ?? "");
    setLine2(h.line2_emphasis ?? "");
    setMetaTitle(h.meta_title ?? "");
    setMetaDesc(h.meta_description ?? "");
  }

  async function save(publish: boolean) {
    onSaving?.(true);
    try {
      await api(`/api/v1/websites/${websiteId}/content/save`, {
        method: "POST",
        body: JSON.stringify({
          doc_type: "homepage",
          payload: { hero: { line1, line2_emphasis: line2, meta_title: metaTitle, meta_description: metaDesc } },
          publish,
        }),
      });
      onToast(publish ? "Published — run site publish to rebuild" : "Draft saved");
    } finally {
      onSaving?.(false);
    }
  }

  return (
    <>
      <h1 style={{ marginTop: 0 }}>Homepage</h1>
      <p className="muted">Hero headline and SEO — matches your live site markup.</p>
      <div className="editor-split">
        <div className="card">
          <FormFields>
            <div className="field">
              <label>Headline line 1</label>
              <input value={line1} onChange={(e) => setLine1(e.target.value)} />
            </div>
            <div className="field">
              <label>Headline line 2 (emphasis)</label>
              <input value={line2} onChange={(e) => setLine2(e.target.value)} />
            </div>
            <div className="field">
              <label>Browser title (SEO)</label>
              <input value={metaTitle} onChange={(e) => setMetaTitle(e.target.value)} />
            </div>
            <div className="field">
              <label>Meta description</label>
              <textarea rows={3} value={metaDesc} onChange={(e) => setMetaDesc(e.target.value)} />
            </div>
          </FormFields>
          <div className="save-bar">
            <button type="button" className="btn secondary" onClick={() => save(false)}>
              Save draft
            </button>
            <button type="button" className="btn" onClick={() => save(true)}>
              Publish changes
            </button>
          </div>
        </div>
        <div>
          <h3 style={{ margin: "0 0 0.5rem" }}>Live build preview</h3>
          <p className="muted">From last successful publish build.</p>
          <div className="preview-frame">
            {previewSrc ? <iframe title="Homepage preview" src={previewSrc} /> : <p className="muted" style={{ padding: "1rem" }}>Publish once to enable preview.</p>}
          </div>
        </div>
      </div>
    </>
  );
}

function FormFields({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>;
}
