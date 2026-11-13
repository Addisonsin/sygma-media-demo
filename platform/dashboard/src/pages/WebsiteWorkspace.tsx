import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api";
import WebsiteShell from "../components/WebsiteShell";
import OverviewPanel from "./website/OverviewPanel";
import HomepagePanel from "./website/HomepagePanel";
import SettingsPanel from "./website/SettingsPanel";
import MediaPanel from "./website/MediaPanel";
import PagesPanel from "./website/PagesPanel";
import PublishPanel from "./website/PublishPanel";
import BlogPanel from "./website/BlogPanel";

type Props = { me: { role: string; email: string }; onLogout: () => void };

export default function WebsiteWorkspace({ me, onLogout }: Props) {
  const { id, section } = useParams();
  const tab = section ?? "overview";
  const [name, setName] = useState("Website");
  const [toast, setToast] = useState("");

  useEffect(() => {
    if (!id) return;
    api<{ name: string }>(`/api/v1/websites/${id}`).then((w) => setName(w.name));
  }, [id]);

  if (!id) return null;

  function onToast(m: string) {
    setToast(m);
    setTimeout(() => setToast(""), 3500);
  }

  return (
    <WebsiteShell websiteId={id} siteName={name} me={me} onLogout={onLogout}>
      {tab === "overview" && <OverviewPanel websiteId={id} />}
      {tab === "homepage" && <HomepagePanel websiteId={id} onToast={onToast} />}
      {tab === "settings" && <SettingsPanel websiteId={id} onToast={onToast} />}
      {tab === "media" && <MediaPanel websiteId={id} onToast={onToast} />}
      {tab === "pages" && <PagesPanel websiteId={id} />}
      {tab === "blog" && <BlogPanel websiteId={id} onToast={onToast} />}
      {tab === "publish" && <PublishPanel websiteId={id} onToast={onToast} />}
      {toast ? <div className="toast">{toast}</div> : null}
    </WebsiteShell>
  );
}
