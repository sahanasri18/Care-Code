"""Full forgot/reset password workflow tests (email captured via console backend)."""
from datetime import timedelta

from app.core.security import utcnow
from tests.conftest import extract_reset_token

PASSWORD = "Str0ng!Pass"


def _register(client, email="alex@example.com"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Alex Morgan", "password": PASSWORD},
    )


def _forgot(client, email="alex@example.com"):
    return client.post("/api/v1/auth/forgot-password", json={"email": email})


def _reset(client, token, password="New!Passw0rd"):
    return client.post("/api/v1/auth/reset-password", json={"token": token, "password": password})


class TestForgotPassword:
    def test_forgot_sends_email_with_reset_link(self, client, capture_emails):
        _register(client)
        resp = _forgot(client)
        assert resp.status_code == 200
        assert "If an account exists" in resp.json()["message"]

        assert len(capture_emails) == 1
        to, subject, html = capture_emails[0]
        assert to == "alex@example.com"
        assert "CareCode" in subject
        assert "Reset Password" in html
        assert "http://testserver/reset-password?token=" in html

    def test_forgot_unknown_email_returns_same_message(self, client, capture_emails):
        resp = _forgot(client, email="nobody@example.com")
        assert resp.status_code == 200
        assert "If an account exists" in resp.json()["message"]
        assert capture_emails == []

    def test_forgot_does_not_leak_existing_account(self, client, capture_emails):
        """Response must be byte-identical whether or not the account exists."""
        known = _forgot(client).json()
        unknown = _forgot(client, email="ghost@example.com").json()
        assert known == unknown

    def test_new_request_invalidates_previous_token(self, client, capture_emails):
        _register(client)
        _forgot(client)
        token1 = extract_reset_token(capture_emails[0][2])
        _forgot(client)
        token2 = extract_reset_token(capture_emails[1][2])
        assert token1 != token2
        # First token was invalidated when the second was requested.
        assert _reset(client, token1).status_code == 400
        assert _reset(client, token2).status_code == 200


class TestResetPassword:
    def test_full_flow_reset_and_login(self, client, capture_emails):
        _register(client)
        _forgot(client)
        token = extract_reset_token(capture_emails[0][2])

        resp = _reset(client, token)
        assert resp.status_code == 200

        # Old password is gone.
        assert client.post(
            "/api/v1/auth/login", json={"email": "alex@example.com", "password": PASSWORD}
        ).status_code == 401
        # New password works — the requirement: log in with the new password.
        resp = client.post(
            "/api/v1/auth/login", json={"email": "alex@example.com", "password": "New!Passw0rd"}
        )
        assert resp.status_code == 200
        assert resp.json()["tokens"]["access_token"]

    def test_token_is_single_use(self, client, capture_emails):
        _register(client)
        _forgot(client)
        token = extract_reset_token(capture_emails[0][2])

        assert _reset(client, token).status_code == 200
        assert _reset(client, token).status_code == 400

    def test_wrong_token_rejected(self, client, capture_emails):
        _register(client)
        _forgot(client)
        assert _reset(client, "forged-token-value").status_code == 400

    def test_expired_token_rejected(self, client, capture_emails, db_session_factory):
        _register(client)
        _forgot(client)
        token = extract_reset_token(capture_emails[0][2])

        from app.core.security import hash_reset_token
        from app.models import PasswordResetToken

        with db_session_factory() as db:
            record = db.query(PasswordResetToken).filter(
                PasswordResetToken.token_hash == hash_reset_token(token)
            ).first()
            record.expires_at = utcnow() - timedelta(minutes=1)
            db.commit()

        assert _reset(client, token).status_code == 400

    def test_reset_rejects_weak_password(self, client, capture_emails):
        _register(client)
        _forgot(client)
        token = extract_reset_token(capture_emails[0][2])
        resp = client.post(
            "/api/v1/auth/reset-password", json={"token": token, "password": "weak"}
        )
        assert resp.status_code in (400, 422)

    def test_reset_invalidates_old_sessions(self, client, capture_emails):
        _register(client)
        old_tokens = client.post(
            "/api/v1/auth/login", json={"email": "alex@example.com", "password": PASSWORD}
        ).json()["tokens"]
        _forgot(client)
        token = extract_reset_token(capture_emails[0][2])
        assert _reset(client, token).status_code == 200

        resp = client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {old_tokens['access_token']}"}
        )
        assert resp.status_code == 401
