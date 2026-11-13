from __future__ import annotations

from app.config import settings


def _login(client, email: str | None = None, password: str | None = None) -> str:
    r = client.post(
        "/api/v1/auth/login",
        json={"email": email or settings.bootstrap_admin_email, "password": password or settings.bootstrap_admin_password},
    )
    assert r.status_code == 200
    return r.json()["access_token"]


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_agency_lists_sygma_website(client):
    token = _login(client)
    r = client.get("/api/v1/websites", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert any(w["slug"] == "sygma-media" for w in data)


def test_content_save_validates_schema(client):
    token = _login(client)
    websites = client.get("/api/v1/websites", headers={"Authorization": f"Bearer {token}"}).json()
    wid = websites[0]["id"]
    r = client.post(
        f"/api/v1/websites/{wid}/content/save",
        headers={"Authorization": f"Bearer {token}"},
        json={"doc_type": "homepage", "payload": {}, "publish": False},
    )
    assert r.status_code == 422


def test_content_save_draft(client):
    token = _login(client)
    wid = client.get("/api/v1/websites", headers={"Authorization": f"Bearer {token}"}).json()[0]["id"]
    payload = {"hero": {"line1": "Test Headline", "line2_emphasis": "Pilot CMS"}}
    r = client.post(
        f"/api/v1/websites/{wid}/content/save",
        headers={"Authorization": f"Bearer {token}"},
        json={"doc_type": "homepage", "payload": payload, "publish": False},
    )
    assert r.status_code == 200
    assert r.json()["payload"]["hero"]["line1"] == "Test Headline"


def test_tenant_isolation_without_membership(client):
    token = _login(client)
    wid = client.get("/api/v1/websites", headers={"Authorization": f"Bearer {token}"}).json()[0]["id"]

    # Create second client website
    clients = client.get("/api/v1/agency/clients", headers={"Authorization": f"Bearer {token}"}).json()
    agency_client_id = clients[0]["id"]
    w2_resp = client.post(
        "/api/v1/agency/websites",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_id": agency_client_id,
            "slug": "client-two",
            "name": "Client Two",
            "static_root": "/tmp/nonexistent",
        },
    )
    assert w2_resp.status_code == 200
    w2_id = w2_resp.json()["id"]

    # Client user with access only to first site
    client.post(
        "/api/v1/agency/users/client",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "owner@example.com",
            "password": "password1234",
            "role": "client_owner",
            "website_ids": [wid],
        },
    )
    client_token = _login(client, "owner@example.com", "password1234")
    blocked = client.get(
        f"/api/v1/websites/{w2_id}",
        headers={"Authorization": f"Bearer {client_token}"},
    )
    assert blocked.status_code == 403


def test_publish_build_only(client):
    token = _login(client)
    wid = client.get("/api/v1/websites", headers={"Authorization": f"Bearer {token}"}).json()[0]["id"]
    client.post(
        f"/api/v1/websites/{wid}/content/save",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "doc_type": "homepage",
            "payload": {"hero": {"line1": "Published", "line2_emphasis": "Live"}},
            "publish": True,
        },
    )
    job = client.post(
        f"/api/v1/websites/{wid}/publish",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert job.status_code == 200
    body = job.json()
    assert body["status"] in ("succeeded", "failed")
    if body["status"] == "succeeded":
        assert body["build_path"]
