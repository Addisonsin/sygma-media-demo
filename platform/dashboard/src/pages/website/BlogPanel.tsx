import { FormEvent, useEffect, useState } from "react";
import { api } from "../../api";
import RichTextEditor from "../../components/RichTextEditor";

type DocRow = { doc_key: string; title: string | null; has_draft: boolean; has_published: boolean };

type Props = { websiteId: string; onToast: (m: string) => void };

export default function BlogPanel({ websiteId, onToast }: Props) {
  const [posts, setPosts] = useState<DocRow[]>([]);
  const [slug, setSlug] = useState("");
  const [title, setTitle] = useState("");
  const [excerpt, setExcerpt] = useState("");
  const [body, setBody] = useState("<p></p>");
  const [seoTitle, setSeoTitle] = useState("");
  const [seoDesc, setSeoDesc] = useState("");

  function refreshList() {
    api<DocRow[]>(`/api/v1/websites/${websiteId}/content/documents?doc_type=blog_post`).then(setPosts);
  }

  useEffect(() => {
    refreshList();
  }, [websiteId]);

  function slugify(s: string) {
    return s
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
  }

  async function loadPost(docKey: string) {
    const rev = await api<{ payload: Record<string, string> } | null>(
      `/api/v1/websites/${websiteId}/content/blog_post/${docKey}?status=draft`,
    );
    let p = rev?.payload;
    if (!p) {
      const pub = await api<{ payload?: Record<string, string> } | null>(
        `/api/v1/websites/${websiteId}/content/blog_post/${docKey}?status=published`,
      );
      p = pub?.payload;
    }
    if (!p) return;
    setSlug(p.slug || docKey);
    setTitle(p.title || "");
    setExcerpt(p.excerpt || "");
    setBody(p.body_html || "<p></p>");
    setSeoTitle(p.seo_title || "");
    setSeoDesc(p.seo_description || "");
  }

  async function save(publish: boolean) {
    const key = slug || slugify(title);
    if (!key) {
      onToast("Add a title first");
      return;
    }
    await api(`/api/v1/websites/${websiteId}/content/save`, {
      method: "POST",
      body: JSON.stringify({
        doc_type: "blog_post",
        doc_key: key,
        publish,
        payload: {
          title,
          slug: key,
          excerpt,
          body_html: body,
          seo_title: seoTitle,
          seo_description: seoDesc,
          status: publish ? "published" : "draft",
        },
      }),
    });
    setSlug(key);
    onToast(publish ? "Post published in CMS" : "Draft saved");
    refreshList();
  }

  function newPost(e: FormEvent) {
    e.preventDefault();
    setSlug("");
    setTitle("");
    setExcerpt("");
    setBody("<p></p>");
    setSeoTitle("");
    setSeoDesc("");
  }

  return (
    <div className="editor-split">
      <div>
        <h1 style={{ marginTop: 0 }}>Blog</h1>
        <p className="muted">Rich editor — publish pipeline for live blog HTML comes next.</p>
        <form className="card" onSubmit={newPost}>
          <div className="field">
            <label>Title</label>
            <input value={title} onChange={(e) => setTitle(e.target.value)} onBlur={() => !slug && setSlug(slugify(title))} />
          </div>
          <div className="field">
            <label>Slug (URL)</label>
            <input value={slug} onChange={(e) => setSlug(slugify(e.target.value))} placeholder="my-post" />
          </div>
          <div className="field">
            <label>Excerpt</label>
            <textarea rows={2} value={excerpt} onChange={(e) => setExcerpt(e.target.value)} />
          </div>
          <BodyLabel />
          <RichTextEditor value={body} onChange={setBody} />
          <span style={{ display: "block", marginTop: "1rem" }}>
            <label>SEO title</label>
            <input value={seoTitle} onChange={(e) => setSeoTitle(e.target.value)} style={{ marginTop: "0.35rem" }} />
          </span>
          <span style={{ display: "block", marginTop: "0.75rem" }}>
            <label>Meta description</label>
            <textarea rows={2} value={seoDesc} onChange={(e) => setSeoDesc(e.target.value)} style={{ marginTop: "0.35rem" }} />
          </span>
          <div className="save-bar" style={{ marginTop: "1.25rem" }}>
            <button type="button" className="btn secondary" onClick={() => save(false)}>
              Save draft
            </button>
            <button type="button" className="btn" onClick={() => save(true)}>
              Publish
            </button>
          </div>
        </form>
      </div>
      <div className="card">
        <h3>Your posts</h3>
        {posts.length === 0 ? <p className="muted">No posts in CMS yet.</p> : null}
        <table className="table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Slug</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {posts.map((p) => (
              <tr key={p.doc_key} style={{ cursor: "pointer" }} onClick={() => loadPost(p.doc_key)}>
                <td>{p.title || p.doc_key}</td>
                <td className="muted">/blog/{p.doc_key}</td>
                <td>
                  {p.has_published ? <span className="badge success">Published</span> : null}
                  {p.has_draft ? <span className="badge warn">Draft</span> : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function BodyLabel() {
  return (
    <label style={{ display: "block", marginTop: "1rem", marginBottom: "0.35rem" }}>
      Body
    </label>
  );
}
