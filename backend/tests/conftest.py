"""Test fixtures: isolated in-memory DB per test, console email capture."""
import os
import re
import tempfile
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# --- Must be set before any app import (settings are cached at import time) ---
_TMP = tempfile.mkdtemp(prefix="carecode-test-")
os.environ["ENVIRONMENT"] = "test"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["DATABASE_URL"] = f"sqlite:///{_TMP}/app.db"
os.environ["FRONTEND_URL"] = "http://localhost:5173"
os.environ["STORAGE_DIR"] = os.path.join(_TMP, "storage")
os.environ["SMTP_HOST"] = ""  # console backend
os.environ["PUBLIC_BASE_URL"] = "http://testserver"
os.environ["RATE_LIMIT_ENABLED"] = "false"

from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.services.hospital_seed import seed_hospitals  # noqa: E402

sent_emails: list[tuple[str, str, str]] = []


def _fake_send_email(settings, to: str, subject: str, html: str) -> bool:
    sent_emails.append((to, subject, html))
    return True


@pytest.fixture(autouse=True)
def capture_emails(monkeypatch):
    sent_emails.clear()
    monkeypatch.setattr("app.core.email.send_email", _fake_send_email)
    yield sent_emails
    sent_emails.clear()


@pytest.fixture
def test_db():
    """Fresh in-memory database per test, shared by client and direct DB access."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    yield sessionmaker(bind=test_engine, autoflush=False)


@pytest.fixture
def client(test_db) -> Generator[TestClient, None, None]:
    def override_get_db():
        db = test_db()
        try:
            seed_hospitals(db)
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def db_session_factory(test_db):
    return test_db



def extract_reset_token(email_html: str) -> str:
    match = re.search(r"reset-password\?token=([^\"&']+)", email_html)
    assert match, f"no reset token found in email: {email_html[:500]}"
    return match.group(1)
