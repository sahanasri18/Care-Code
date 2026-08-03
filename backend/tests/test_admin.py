"""Admin module tests: role enforcement, hospital CRUD, privacy-safe stats.

Privacy-first: admin endpoints manage only application resources (hospitals,
analytics). There are no user-management endpoints — account and medical data
is strictly self-service.
"""
from sqlalchemy import select

from app.models import User

PASSWORD = "Str0ng!Pass"
ADMIN_PASSWORD = "Adm1n!Pass"


def _register(client, email="alex@example.com", password=PASSWORD):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Alex Morgan", "password": password},
    )


def _make_admin(client, db_session_factory, email="admin@carecode.io"):
    _register(client, email=email, password=ADMIN_PASSWORD)
    with db_session_factory() as db:
        user = db.scalar(select(User).where(User.email == email))
        user.role = "admin"
        db.commit()
    tokens = client.post(
        "/api/v1/auth/login", json={"email": email, "password": ADMIN_PASSWORD}
    ).json()["tokens"]
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def _user_headers(client, email="alex@example.com"):
    tokens = _register(client, email=email).json()["tokens"]
    return {"Authorization": f"Bearer {tokens['access_token']}"}


class TestRoleEnforcement:
    def test_non_admin_blocked(self, client):
        headers = _user_headers(client)
        for path in ["/api/v1/admin/hospitals", "/api/v1/admin/stats"]:
            assert client.get(path, headers=headers).status_code == 403, path

    def test_admin_allowed(self, client, db_session_factory):
        headers = _make_admin(client, db_session_factory)
        assert client.get("/api/v1/admin/hospitals", headers=headers).status_code == 200
        assert client.get("/api/v1/admin/stats", headers=headers).status_code == 200

    def test_anonymous_blocked(self, client):
        assert client.get("/api/v1/admin/stats").status_code == 401


class TestNoAdminUserManagement:
    """User accounts are self-service; admin user endpoints must not exist."""

    def test_user_list_endpoint_removed(self, client, db_session_factory):
        admin = _make_admin(client, db_session_factory)
        paths = client.get("/openapi.json").json()["paths"]
        assert "/api/v1/admin/users" not in paths
        assert "/api/v1/admin/users/{user_id}" not in paths

    def test_user_mutation_endpoints_removed(self, client, db_session_factory):
        admin = _make_admin(client, db_session_factory)
        paths = client.get("/openapi.json").json()["paths"]
        assert "/api/v1/admin/users/{user_id}" not in paths
        assert not any(
            "/api/v1/admin/users" in path and path != "/api/v1/admin/users"
            for path in paths
        )
        # the SPA fallback (not a JSON admin route) is what answers now
        resp = client.get("/api/v1/admin/users", headers=admin)
        assert resp.status_code == 200
        assert "CareCode" in resp.text

    def test_stats_never_expose_personal_data(self, client, db_session_factory):
        _user_headers(client, "alex@example.com")
        profile = client.get("/api/v1/users/me/profile", headers=_user_headers(client, "bob@example.com"))
        assert profile.status_code == 200
        admin = _make_admin(client, db_session_factory)
        body = client.get("/api/v1/admin/stats", headers=admin).json()
        assert "top_profiles" not in body
        serialized = str(body).lower()
        for forbidden in ["alex", "bob", "morgan", "carecode", "blood", "diabetes"]:
            assert forbidden not in serialized


class TestAdminHospitals:
    def test_create_update_delete(self, client, db_session_factory):
        admin = _make_admin(client, db_session_factory)
        data = {
            "name": "Test Hospital",
            "address": "1 Test Road",
            "city": "Test City",
            "state": "Tamil Nadu",
            "pincode": "600001",
            "phone": "+91 100",
            "latitude": 12.5,
            "longitude": 77.5,
            "departments": ["Emergency"],
        }
        created = client.post("/api/v1/admin/hospitals", json=data, headers=admin)
        assert created.status_code == 201
        hid = created.json()["id"]

        updated = client.put(
            f"/api/v1/admin/hospitals/{hid}",
            json={**data, "name": "Test Hospital 2"},
            headers=admin,
        )
        assert updated.status_code == 200
        assert updated.json()["name"] == "Test Hospital 2"

        deleted = client.delete(f"/api/v1/admin/hospitals/{hid}", headers=admin)
        assert deleted.status_code == 204
        assert client.get(f"/api/v1/hospitals/{hid}").status_code == 404

    def test_non_admin_cannot_create(self, client):
        headers = _user_headers(client)
        data = {
            "name": "X",
            "address": "1 X Road",
            "city": "X",
            "state": "X",
            "latitude": 1,
            "longitude": 1,
        }
        assert client.post("/api/v1/admin/hospitals", json=data, headers=headers).status_code == 403


class TestAdminStats:
    def test_stats_shape(self, client, db_session_factory):
        _user_headers(client, "alex@example.com")
        admin = _make_admin(client, db_session_factory)
        resp = client.get("/api/v1/admin/stats", headers=admin)
        assert resp.status_code == 200
        body = resp.json()
        assert body["total_users"] == 2  # alex + admin
        assert body["total_hospitals"] > 400
        assert isinstance(body["signups_per_day"], list)
        assert "top_profiles" not in body
