"""QR assets and public emergency page tests, incl. 410 behaviour."""
import io

from PIL import Image

PASSWORD = "Str0ng!Pass"
PROFILE = {
    "full_name": "Alex Morgan",
    "date_of_birth": "1992-04-17",
    "gender": "female",
    "blood_group": "O+",
    "allergies": "Penicillin",
    "conditions": "Type 1 Diabetes",
    "medications": "Insulin (daily)",
    "address": "12 Lake View Rd",
    "notes": "Carries glucagon kit",
    "contacts": [{"name": "Sam Morgan", "relationship": "Spouse", "phone": "+91 98765 43210"}],
}


def _setup(client, email="alex@example.com"):
    tokens = client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Alex Morgan", "password": PASSWORD},
    ).json()["tokens"]
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    profile = client.post("/api/v1/users/me/profile", json=PROFILE, headers=headers).json()
    return headers, profile["carecode"]


def _png_bytes():
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), color=(0, 0, 200)).save(buf, format="PNG")
    return buf.getvalue()


class TestQRImages:
    def test_download_png(self, client):
        _, code = _setup(client)
        resp = client.get(f"/api/v1/qr/{code}/image?format=png")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "image/png"
        assert resp.content[:8] == b"\x89PNG\r\n\x1a\n"

    def test_download_svg(self, client):
        _, code = _setup(client)
        resp = client.get(f"/api/v1/qr/{code}/image?format=svg")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "image/svg+xml"
        assert b"<svg" in resp.content

    def test_qr_image_unavailable_for_deleted_code(self, client):
        resp = client.get("/api/v1/qr/does-not-exist/image?format=png")
        assert resp.status_code == 410

    def test_printable_card_requires_owner(self, client):
        _, code = _setup(client)
        other = client.post(
            "/api/v1/auth/register",
            json={"email": "other@example.com", "full_name": "Other", "password": PASSWORD},
        ).json()["tokens"]["access_token"]
        resp = client.get(
            f"/api/v1/qr/{code}/card", headers={"Authorization": f"Bearer {other}"}
        )
        assert resp.status_code == 404
        resp = client.get(f"/api/v1/qr/{code}/card", headers={"Authorization": "Bearer invalid"})
        assert resp.status_code == 401


class TestPublicPage:
    def test_public_page_no_auth_required(self, client):
        _, code = _setup(client)
        resp = client.get(f"/api/v1/public/{code}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["full_name"] == "Alex Morgan"
        assert body["age"] is not None
        assert body["blood_group"] == "O+"
        assert body["contacts"][0]["phone"] == "+91 98765 43210"
        assert body["photo_url"] is None

    def test_scan_count_increments(self, client):
        headers, code = _setup(client)
        for _ in range(3):
            assert client.get(f"/api/v1/public/{code}").status_code == 200

        stats = client.get("/api/v1/analytics/me", headers=headers)
        assert stats.json()["total_scans"] == 3
        assert stats.json()["scans_last_30_days"] == 3

        qr = client.get("/api/v1/qr/me", headers=headers)
        assert qr.json()["scan_count"] == 3

    def test_public_unknown_code_410(self, client):
        resp = client.get("/api/v1/public/not-a-real-code")
        assert resp.status_code == 410
        assert "no longer available" in resp.json()["detail"]

    def test_regenerated_code_goes_410(self, client):
        headers, old_code = _setup(client)
        resp = client.post("/api/v1/users/me/regenerate-qr", headers=headers)
        assert resp.status_code == 200
        new_code = resp.json()["carecode"]
        assert new_code != old_code

        assert client.get(f"/api/v1/public/{old_code}").status_code == 410
        assert client.get(f"/api/v1/public/{new_code}").status_code == 200

    def test_deactivated_profile_goes_410(self, client, db_session_factory):
        headers, code = _setup(client)
        with db_session_factory() as db:
            from app.models import User

            user = db.query(User).filter(User.email == "alex@example.com").first()
            user.is_active = False
            db.commit()
        resp = client.get(f"/api/v1/public/{code}")
        assert resp.status_code == 410
        assert "no longer available" in resp.json()["detail"]

    def test_summary_download(self, client):
        _, code = _setup(client)
        resp = client.get(f"/api/v1/public/{code}/summary")
        assert resp.status_code == 200
        assert "EMERGENCY MEDICAL SUMMARY" in resp.text
        assert "Penicillin" in resp.text
        assert "Sam Morgan" in resp.text
        assert resp.headers["content-disposition"].startswith("attachment")

    def test_summary_unavailable_after_delete(self, client):
        headers, code = _setup(client)
        client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)
        assert client.get(f"/api/v1/public/{code}/summary").status_code == 410

    def test_photo_served_publicly_when_uploaded(self, client):
        headers, code = _setup(client)
        client.post(
            "/api/v1/users/me/profile/photo",
            files={"file": ("photo.png", _png_bytes(), "image/png")},
            headers=headers,
        )
        resp = client.get(f"/api/v1/public/{code}/photo")
        assert resp.status_code == 200
        assert resp.content[:8] == b"\x89PNG\r\n\x1a\n"
