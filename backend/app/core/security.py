"""Security primitives: password hashing, JWT, reset-token hashing."""
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import Settings, get_settings

ALGORITHM = "HS256"


# --------------------------------------------------------------------------
# Passwords
# --------------------------------------------------------------------------
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def validate_password_strength(password: str) -> str | None:
    """Return an error message if the password is weak, else None."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if len(password) > 128:
        return "Password must be at most 128 characters long."
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number."
    if not any(c in "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~" for c in password):
        return "Password must contain at least one special character."
    return None


# --------------------------------------------------------------------------
# JWT
# --------------------------------------------------------------------------
def _create_token(
    settings: Settings, subject: str, token_type: str, expires_delta: timedelta, token_version: int = 1
) -> tuple[str, str]:
    jti = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "jti": jti,
        "v": token_version,
        "iat": now,
        "exp": now + expires_delta,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
    return token, jti


def create_access_token(settings: Settings, user_id: str, token_version: int = 1) -> tuple[str, str]:
    return _create_token(
        settings, str(user_id), "access", timedelta(minutes=settings.access_token_expire_minutes), token_version
    )


def create_refresh_token(settings: Settings, user_id: str, token_version: int = 1) -> tuple[str, str]:
    return _create_token(
        settings, str(user_id), "refresh", timedelta(days=settings.refresh_token_expire_days), token_version
    )


def decode_token(settings: Settings, token: str) -> dict[str, Any]:
    """Decode and verify a JWT. Raises jwt.PyJWTError on any failure."""
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])


# --------------------------------------------------------------------------
# Reset tokens (opaque, hashed at rest)
# --------------------------------------------------------------------------
def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def hash_reset_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
