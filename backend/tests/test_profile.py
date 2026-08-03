"""Medical profile module tests: upsert, contacts, validation, photo upload."""
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
    "address": "12 Lake View Rd, Bengaluru",
    "notes": "Carries glucagon kit",
    "contacts": [
        {"name": "Sam Morgan", "relationship": "Spouse", "phone": "+91 98765 43210"},
        {"name": "Dr. Lee", "relationship": "Physician", "phone": "+91 91234 56789"},
    ],
}


def _register(client, email="alex@example.com"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Alex Morgan", "password": PASSWORD},
    ).json()


def _auth(client, email="alex@example.com"):
    return {"Authorization": f"Bearer {_register(client, email)['tokens']['access_token']}"}


def _save(client, headers, data):
    return client.post("/api/v1/users/me/profile", json=data, headers=headers)


class TestProfileSave:
    def test_create_profile(self, client):
        resp = _save(client, _auth(client), PROFILE)
        assert resp.status_code == 200
        body = resp.json()
        assert body["full_name"] == "Alex Morgan"
        assert body["blood_group"] == "O+"
        assert body["scan_count"] == 0
        assert body["public_url"].startswith("http://testserver/e/")
        assert len(body["contacts"]) == 2

    def test_upsert_replaces_contacts(self, client):
        headers = _auth(client)
        _save(client, headers, PROFILE)
        updated = {**PROFILE, "full_name": "Alex M. Morgan", "contacts": PROFILE["contacts"][:1]}
        resp = _save(client, headers, updated)
        assert resp.status_code == 200
        assert resp.json()["full_name"] == "Alex M. Morgan"
        assert len(resp.json()["contacts"]) == 1

    def test_carecode_stable_across_updates(self, client):
        headers = _auth(client)
        code1 = _save(client, headers, PROFILE).json()["carecode"]
        code2 = _save(client, headers, {**PROFILE, "notes": "changed"}).json()["carecode"]
        assert code1 == code2

    def test_scan_stats_preserved_on_update(self, client):
        headers = _auth(client)
        profile = _save(client, headers, PROFILE).json()
        code = profile["carecode"]
        client.get(f"/api/v1/public/{code}")  # one scan
        updated = _save(client, headers, {**PROFILE, "notes": "x"}).json()
        assert updated["scan_count"] == 1

    def test_blood_group_validation(self, client):
        resp = _save(client, _auth(client), {**PROFILE, "blood_group": "ZZ"})
        assert resp.status_code == 422

    def test_gender_validation(self, client):
        resp = _save(client, _auth(client), {**PROFILE, "gender": "alien"})
        assert resp.status_code == 422

    def test_empty_optional_fields(self, client):
        minimal = {"full_name": "Bob", "contacts": []}
        resp = _save(client, _auth(client, "bob@example.com"), minimal)
        assert resp.status_code == 200
        body = resp.json()
        assert body["blood_group"] is None
        assert body["allergies"] is None

    def test_another_user_cannot_see_my_profile(self, client):
        alex = _auth(client)
        other = _auth(client, "other@example.com")
        alex_profile = _save(client, alex, PROFILE).json()
        other_profile = client.get("/api/v1/users/me/profile", headers=other).json()
        assert alex_profile["carecode"] != other_profile["carecode"]
        assert other_profile["full_name"] == "Alex Morgan"  # own profile, default name


class TestPhotoUpload:
    def _png_bytes(self) -> bytes:
        buf = io.BytesIO()
        Image.new("RGB", (10, 10), color=(200, 0, 0)).save(buf, format="PNG")
        return buf.getvalue()

    def test_upload_photo(self, client, db_session_factory):
        headers = _auth(client)
        _save(client, headers, PROFILE)
        resp = client.post(
            "/api/v1/users/me/profile/photo",
            files={"file": ("photo.png", self._png_bytes(), "image/png")},
            headers=headers,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["photo_url"] == f"/api/v1/public/{body['carecode']}/photo"

        with db_session_factory() as db:
            from app.models import MedicalProfile

            profile = db.query(MedicalProfile).first()
            path = __import__("app.core.config", fromlist=["get_settings"]).get_settings().storage_path / "photos" / profile.photo_filename
            assert path.is_file()

    def test_upload_rejects_non_image(self, client):
        headers = _auth(client)
        _save(client, headers, PROFILE)
        resp = client.post(
            "/api/v1/users/me/profile/photo",
            files={"file": ("evil.txt", b"not an image", "text/plain")},
            headers=headers,
        )
        assert resp.status_code == 400

    def test_remove_photo(self, client, db_session_factory):
        headers = _auth(client)
        _save(client, headers, PROFILE)
        client.post(
            "/api/v1/users/me/profile/photo",
            files={"file": ("photo.png", self._png_bytes(), "image/png")},
            headers=headers,
        )
        resp = client.delete("/api/v1/users/me/profile/photo", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["photo_url"] is None
