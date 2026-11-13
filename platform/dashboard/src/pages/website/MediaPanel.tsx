import { FormEvent, useEffect, useState } from "react";
import { api, getToken } from "../../api";
import { mediaFileUrl } from "../../components/WebsiteShell";

type Asset = {
  id: string;
  logical_key: string;
  mime_type: string;
  size_bytes: number;
  alt_text: string | null;
};

type Props = { websiteId: string; onToast: (m: string) => void };

export default function MediaPanel({ websiteId, onToast }: Props) {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [key, setKey] = useState("uploads/hero");
  const [alt, setAlt] = useState("");
  const [drag, setDrag] = useState(false);

  function refresh() {
    api<Asset[]>(`/api/v1/websites/${websiteId}/media`).then(setAssets).catch(console.error);
  }

  useEffect(() => {
    refresh();
  }, [websiteId]);

  async function uploadFile(file: File) {
    const fd = new FormData();
    fd.set("logical_key", key);
    fd.set("file", file);
    if (alt) fd.set("alt_text", alt);
    const token = getToken();
    const res = await fetch(`/api/v1/websites/${websiteId}/media/upload`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: fd,
    });
    if (!res.ok) throw new Error(await res.text());
    onToast("Uploaded");
    refresh();
  }

  async function upload(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const input = e.currentTarget.querySelector<HTMLInputElement>('input[type="file"]');
    if (input?.files?.[0]) await uploadFile(input.files[0]);
    e.currentTarget.reset();
  }

  return (
    <>
      <h1 style={{ marginTop: 0 }}>Media library</h1>
      <p className="muted">Upload images like WordPress — stored per website.</p>
      <form className="card" onSubmit={upload}>
        <DropZone drag={drag} onDrag={() => setDrag(true)} onLeave={() => setDrag(false)}>
          <div className="field">
            <label>Folder / key</label>
            <input value={key} onChange={(e) => setKey(e.target.value)} required />
          </div>
          <div className="field">
            <label>Alt text</label>
            <input value={alt} onChange={(e) => setAlt(e.target.value)} />
          </div>
          <input type="file" name="file" accept="image/*" required />
          <button className="btn" type="submit" style={{ marginTop: "0.75rem" }}>
            Upload
          </button>
        </DropZone>
      </form>
      <div className="media-grid" style={{ marginTop: "1.25rem" }}>
        {assets.map((a) => (
          <Button key={a.id} asset={a} websiteId={websiteId} />
        ))}
      </div>
      {assets.length === 0 ? <p className="muted">No media yet.</p> : null}
    </>
  );
}

function DropZone({
  children,
  drag,
  onDrag,
  onLeave,
}: {
  children: React.ReactNode;
  drag: boolean;
  onDrag: () => void;
  onLeave: () => void;
}) {
  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        onDrag();
      }}
      onDragLeave={onLeave}
      style={{
        border: drag ? "2px dashed var(--primary)" : "2px dashed transparent",
        borderRadius: 8,
        padding: drag ? "0.5rem" : 0,
      }}
    >
      {children}
    </div>
  );
}

function Button({ asset, websiteId }: { asset: Asset; websiteId: string }) {
  const src = asset.mime_type.startsWith("image/") ? mediaFileUrl(websiteId, asset.id) : undefined;
  return (
    <article className="media-thumb">
      {src ? <img src={src} alt={asset.alt_text || asset.logical_key} /> : <FilePlaceholder />}
      <div className="meta">
        <strong style={{ fontSize: "0.8rem" }}>{asset.logical_key}</strong>
        <div className="muted">{Math.round(asset.size_bytes / 1024)} KB</div>
      </div>
    </article>
  );
}

function FilePlaceholder() {
  return <div className="muted" style={{ padding: "2rem", textAlign: "center" }}>File</div>;
}
