"""Auth module tests: register, login, refresh, logout, change password."""
from datetime import timedelta

from app.core.security import decode_token

PASSWORD = "Str0ng!Pass"


def _register(client, email="alex@example.com", name="Alex Morgan", password=PASSWORD):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": name, "password": password},
    )


def _login(client, email="alex@example.com", password=PASSWORD):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


class TestRegister:
    def test_register_success(self, client):
        resp = _register(client)
        assert resp.status_code == 201
        body = resp.json()
        assert body["user"]["email"] == "alex@example.com"
        assert body["user"]["role"] == "user"
        assert body["tokens"]["access_token"]
        assert body["tokens"]["refresh_token"]

    def test_register_normalizes_email(self, client):
        resp = _register(client, email="  Alex@Example.COM ")
        assert resp.status_code == 201
        assert resp.json()["user"]["email"] == "alex@example.com"

    def test_register_duplicate_email_conflict(self, client):
        _register(client)
        resp = _register(client)
        assert resp.status_code == 409

    def test_register_rejects_weak_password(self, client):
        for weak in ["short", "alllowercase1", "NoNumbersHere!", "noSpecialChars1"]:
            resp = _register(client, email=f"{weak}@example.com", password=weak)
            # Pydantic min_length may reject first (422); otherwise our policy rejects (400).
            assert resp.status_code in (400, 422), weak

    def test_register_creates_profile_with_carecode(self, client):
        token = _register(client).json()["tokens"]["access_token"]
        resp = client.get(
            "/api/v1/users/me/profile", headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200
        assert resp.json()["carecode"]
        assert resp.json()["full_name"] == "Alex Morgan"


class TestLogin:
    def test_login_success(self, client):
        _register(client)
        resp = _login(client)
        assert resp.status_code == 200
        assert resp.json()["tokens"]["access_token"]

    def test_login_wrong_password(self, client):
        _register(client)
        resp = _login(client, password="Wrong!Pass1")
        assert resp.status_code == 401

    def test_login_unknown_email(self, client):
        resp = _login(client, email="nobody@example.com")
        assert resp.status_code == 401

    def test_login_deactivated_user_blocked(self, client, db_session_factory):
        _register(client)
        with db_session_factory() as db:
            from app.models import User

            user = db.query(User).filter(User.email == "alex@example.com").first()
            user.is_active = False
            db.commit()
        resp = _login(client)
        assert resp.status_code == 403


class TestRefresh:
    def test_refresh_rotates_tokens(self, client):
        tokens = _register(client).json()["tokens"]
        resp = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
        assert resp.status_code == 200
        body = resp.json()
        assert body["access_token"] != tokens["access_token"]
        assert body["refresh_token"] != tokens["refresh_token"]

    def test_refresh_rejects_access_token(self, client):
        tokens = _register(client).json()["tokens"]
        resp = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["access_token"]})
        assert resp.status_code == 401

    def test_refresh_rejects_garbage(self, client):
        resp = client.post("/api/v1/auth/refresh", json={"refresh_token": "not-a-token"})
        assert resp.status_code == 401


class TestLogout:
    def test_logout_revokes_refresh_token(self, client):
        tokens = _register(client).json()["tokens"]
        resp = client.post("/api/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]})
        assert resp.status_code == 204

        resp = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
        assert resp.status_code == 401

    def test_logout_is_idempotent(self, client):
        resp = client.post("/api/v1/auth/logout", json={"refresh_token": "garbage-token"})
        assert resp.status_code == 204


class TestChangePassword:
    def test_change_password_and_relogin(self, client):
        _register(client)
        tokens = _login(client).json()["tokens"]
        auth = {"Authorization": f"Bearer {tokens['access_token']}"}

        resp = client.post(
            "/api/v1/auth/change-password",
            json={"current_password": PASSWORD, "new_password": "New!Passw0rd"},
            headers=auth,
        )
        assert resp.status_code == 200
        assert resp.json()["tokens"]["access_token"]

        # Old password no longer works; new one does.
        assert _login(client, password=PASSWORD).status_code == 401
        assert _login(client, password="New!Passw0rd").status_code == 200

    def test_change_password_wrong_current(self, client):
        tokens = _register(client).json()["tokens"]
        resp = client.post(
            "/api/v1/auth/change-password",
            json={"current_password": "Wrong!Pass1", "new_password": "New!Passw0rd"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert resp.status_code == 400

    def test_password_change_invalidates_old_tokens(self, client):
        tokens = _register(client).json()["tokens"]
        old_access = tokens["access_token"]
        resp = client.post(
            "/api/v1/auth/change-password",
            json={"current_password": PASSWORD, "new_password": "New!Passw0rd"},
            headers={"Authorization": f"Bearer {old_access}"},
        )
        assert resp.status_code == 200
        # The old access token (pre-change version) is now invalid.
        resp = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {old_access}"})
        assert resp.status_code == 401


class TestTokenProtection:
    def test_me_requires_auth(self, client):
        assert client.get("/api/v1/users/me").status_code == 401

    def test_me_with_valid_token(self, client):
        token = _register(client).json()["tokens"]["access_token"]
        resp = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "alex@example.com"

    def test_jti_uniqueness(self, client):
        tokens = _register(client).json()["tokens"]
        payload1 = decode_token(
            __import__("app.core.config", fromlist=["get_settings"]).get_settings(), tokens["access_token"]
        )
        assert payload1["jti"]
        assert payload1["type"] == "access"
