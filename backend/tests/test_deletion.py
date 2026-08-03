"""Account deletion workflow: irreversible, complete cleanup, QR stays invalid."""
import io

from PIL import Image
from sqlalchemy import select

from app.models import ActivityLog, MedicalProfile, PasswordResetToken, ScanEvent, User
from app.services.hospital_seed import SEED_HOSPITALS

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
    "notes": "Notes",
    "contacts": [{"name": "Sam Morgan", "relationship": "Spouse", "phone": "+91 98765 43210"}],
}


def _png_bytes():
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), color=(0, 200, 0)).save(buf, format="PNG")
    return buf.getvalue()


def _setup(client, email="alex@example.com"):
    tokens = client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Alex Morgan", "password": PASSWORD},
    ).json()["tokens"]
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    profile = client.post("/api/v1/users/me/profile", json=PROFILE, headers=headers).json()
    client.post(
        "/api/v1/users/me/profile/photo",
        files={"file": ("photo.png", _png_bytes(), "image/png")},
        headers=headers,
    )
    client.get(f"/api/v1/public/{profile['carecode']}")  # generate a scan event
    return tokens, headers, profile["carecode"]


def _row_counts(db):
    return {
        "users": db.scalar(select(func.count()).select_from(User)),
        "profiles": db.scalar(select(func.count()).select_from(MedicalProfile)),
        "scans": db.scalar(select(func.count()).select_from(ScanEvent)),
        "activity": db.scalar(select(func.count()).select_from(ActivityLog)),
        "reset_tokens": db.scalar(select(func.count()).select_from(PasswordResetToken)),
    }


from sqlalchemy import func  # noqa: E402


class TestDeleteAccount:
    def test_delete_requires_password(self, client):
        _, headers, _ = _setup(client)
        resp = client.delete("/api/v1/users/me?password=", headers=headers)
        assert resp.status_code == 400

    def test_delete_with_wrong_password(self, client):
        _, headers, _ = _setup(client)
        resp = client.delete("/api/v1/users/me?password=Wrong!Pass1", headers=headers)
        assert resp.status_code == 400

    def test_delete_removes_all_personal_data(self, client, db_session_factory):
        tokens, headers, code = _setup(client)
        resp = client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)
        assert resp.status_code == 204

        with db_session_factory() as db:
            counts = _row_counts(db)
            assert counts["users"] == 0
            assert counts["profiles"] == 0
            assert counts["scans"] == 0
            assert counts["activity"] == 0
            assert counts["reset_tokens"] == 0

    def test_delete_removes_photo_file(self, client, db_session_factory):
        tokens, headers, code = _setup(client)
        settings = __import__("app.core.config", fromlist=["get_settings"]).get_settings()
        with db_session_factory() as db:
            from app.models import MedicalProfile

            filename = db.scalar(select(MedicalProfile.photo_filename))
            photo_path = settings.storage_path / "photos" / filename
            assert photo_path.is_file()

        client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)
        assert not photo_path.exists()

    def test_old_qr_permanently_invalid_after_deletion(self, client):
        tokens, headers, code = _setup(client)
        client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)

        for path in (
            f"/api/v1/public/{code}",
            f"/api/v1/public/{code}/photo",
            f"/api/v1/public/{code}/summary",
            f"/api/v1/qr/{code}/image?format=png",
        ):
            resp = client.get(path)
            assert resp.status_code == 410, path
            assert "no longer available" in resp.json()["detail"]

    def test_tokens_invalid_after_deletion(self, client):
        tokens, headers, code = _setup(client)

        # Before deletion: access token works, refresh works, login works.
        assert client.get("/api/v1/users/me", headers=headers).status_code == 200
        assert (
            client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}).status_code == 200
        )
        assert client.post(
            "/api/v1/auth/login", json={"email": "alex@example.com", "password": PASSWORD}
        ).status_code == 200

        client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)

        # After deletion: everything is dead.
        assert client.get("/api/v1/users/me", headers=headers).status_code == 401
        assert (
            client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}).status_code == 401
        )
        assert client.post(
            "/api/v1/auth/login", json={"email": "alex@example.com", "password": PASSWORD}
        ).status_code == 401

    def test_deletion_is_irreversible(self, client):
        tokens, headers, code = _setup(client)
        client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)
        # Re-registering is a brand-new account; the old QR still must not work.
        _, headers2, code2 = _setup(client, email="alex@example.com")
        assert code2 != code
        assert client.get(f"/api/v1/public/{code}").status_code == 410

    def test_hospital_catalog_untouched_by_deletion(self, client, db_session_factory):
        _, headers, _ = _setup(client)
        client.delete(f"/api/v1/users/me?password={PASSWORD}", headers=headers)
        with db_session_factory() as db:
            from app.models import Hospital

            assert db.scalar(select(func.count()).select_from(Hospital)) == len(SEED_HOSPITALS)
