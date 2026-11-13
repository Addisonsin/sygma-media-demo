import { useEffect, useState } from "react";
import { api } from "../../api";

type Props = { websiteId: string; onToast: (m: string) => void };

export default function SettingsPanel({ websiteId, onToast }: Props) {
  const [business, setBusiness] = useState("");
  const [phoneDisplay, setPhoneDisplay] = useState("");
  const [phoneE164, setPhoneE164] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    api<{ payload?: Record<string, string> } | null>(
      `/api/v1/websites/${websiteId}/content/site_settings/default?status=draft`,
    )
      .then((rev) => {
        const p = rev?.payload ?? {};
        setBusiness(p.business_name ?? "");
        setPhoneDisplay(p.phone_display ?? "");
        setPhoneE164(p.phone_e164 ?? "");
        setWhatsapp(p.whatsapp_e164 ?? "");
        setEmail(p.email ?? "");
      })
      .catch(() => undefined);
  }, [websiteId]);

  async function save(publish: boolean) {
    await api(`/api/v1/websites/${websiteId}/content/save`, {
      method: "POST",
      body: JSON.stringify({
        doc_type: "site_settings",
        payload: {
          business_name: business,
          phone_display: phoneDisplay,
          phone_e164: phoneE164,
          whatsapp_e164: whatsapp,
          email,
        },
        publish,
      }),
    });
    onToast(publish ? "Contact settings published" : "Draft saved");
  }

  return (
    <div className="card" style={{ maxWidth: 640 }}>
      <p className="muted">Contact page JSON-LD and phone links (Phase 4 patch).</p>
      <div className="field">
        <label>Business name</label>
        <input value={business} onChange={(e) => setBusiness(e.target.value)} />
      </div>
      <div className="field">
        <label>Phone (display)</label>
        <input value={phoneDisplay} onChange={(e) => setPhoneDisplay(e.target.value)} />
      </div>
      <div className="field">
        <label>Phone E.164</label>
        <input value={phoneE164} onChange={(e) => setPhoneE164(e.target.value)} placeholder="+12125550147" />
      </div>
      <div className="field">
        <label>WhatsApp E.164</label>
        <input value={whatsapp} onChange={(e) => setWhatsapp(e.target.value)} />
      </div>
      <div className="field">
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div style={{ display: "flex", gap: "0.75rem" }}>
        <button type="button" className="btn secondary" onClick={() => save(false)}>
          Save draft
        </button>
        <button type="button" className="btn" onClick={() => save(true)}>
          Save & publish doc
        </button>
      </div>
    </div>
  );
}
