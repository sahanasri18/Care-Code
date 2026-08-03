"""Authentication: register, login, refresh, logout, password recovery & change."""
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, revoke_jti
from app.core.config import Settings, get_settings
from app.core.email import password_reset_email
from app.core.rate_limit import rate_limit
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_reset_token,
    hash_password,
    hash_reset_token,
    utcnow,
    validate_password_strength,
    verify_password,
)
from app.core.database import get_db
from app.models import MedicalProfile, PasswordResetToken, RevokedToken, User
from app.schemas.auth import (
    AuthResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenPair,
    UserOut,
)
from app.schemas.common import Message
from app.services.activity import log_activity

router = APIRouter(prefix="/auth", tags=["auth"])

FORGOT_RESPONSE = "If an account exists with that email, a password reset link has been sent."


def _issue_tokens(settings: Settings, user: User) -> TokenPair:
    access, _ = create_access_token(settings, str(user.id), user.token_version)
    refresh, _ = create_refresh_token(settings, str(user.id), user.token_version)
    return TokenPair(access_token=access, refresh_token=refresh)


def _auth_response(user: User, settings: Settings) -> AuthResponse:
    return AuthResponse(user=UserOut.model_validate(user), tokens=_issue_tokens(settings, user))


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    strength_error = validate_password_strength(data.password)
    if strength_error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, strength_error)

    email = data.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")

    user = User(
        email=email,
        full_name=data.full_name.strip(),
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = MedicalProfile(user_id=user.id, carecode=str(uuid.uuid4()), full_name=user.full_name)
    db.add(profile)
    db.commit()

    log_activity(db, user, "register", {"method": "email"})
    db.commit()
    return _auth_response(user, settings)


@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limit(settings, f"login:{client_ip}", 10, 60):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many login attempts, try again later")

    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account has been deactivated")

    log_activity(db, user, "login")
    db.commit()
    return _auth_response(user, settings)


@router.post("/refresh", response_model=TokenPair)
def refresh(data: RefreshRequest, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    try:
        payload = decode_token(settings, data.refresh_token)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")
    if payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token type")
    if db.query(RevokedToken).filter(RevokedToken.jti == payload.get("jti")).first():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token has been revoked")

    user = db.get(User, uuid.UUID(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer exists")
    if payload.get("v", 0) != user.token_version:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session invalidated, please log in again")

    return _issue_tokens(settings, user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(data: LogoutRequest, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    try:
        payload = decode_token(settings, data.refresh_token)
        if payload.get("type") == "refresh":
            if not db.query(RevokedToken).filter(RevokedToken.jti == payload["jti"]).first():
                db.add(RevokedToken(jti=payload["jti"], expires_at=utcnow() + timedelta(seconds=10)))
                db.commit()
    except Exception:
        pass  # idempotent logout: always succeed
    return None


@router.post("/forgot-password", response_model=Message)
def forgot_password(
    data: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limit(settings, f"forgot:{client_ip}", 3, 3600):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many requests, try again later")

    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()

    # Uniform response prevents account enumeration.
    if user is None or not user.is_active:
        return Message(message=FORGOT_RESPONSE)

    # Invalidate any previously issued, unused tokens for this user (single-active-token policy).
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None)
    ).update({"used_at": utcnow()})

    raw_token = generate_reset_token()
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=hash_reset_token(raw_token),
            expires_at=utcnow() + timedelta(minutes=settings.reset_token_expire_minutes),
        )
    )
    db.commit()

    reset_url = f"{settings.public_url}/reset-password?token={raw_token}"
    password_reset_email(settings, user.email, reset_url)
    log_activity(db, user, "password_reset_requested")
    db.commit()
    return Message(message=FORGOT_RESPONSE)


@router.post("/reset-password", response_model=Message)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    strength_error = validate_password_strength(data.password)
    if strength_error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, strength_error)

    token_hash = hash_reset_token(data.token)
    record = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > utcnow(),
        )
        .first()
    )
    if record is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This reset link is invalid or has expired")

    user = db.get(User, record.user_id)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This reset link is invalid or has expired")

    user.password_hash = hash_password(data.password)
    user.token_version += 1
    record.used_at = utcnow()
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None)
    ).update({"used_at": utcnow()})
    db.commit()

    log_activity(db, user, "password_reset")
    db.commit()
    return Message(message="Your password has been reset. You can now log in with your new password.")


@router.post("/change-password", response_model=AuthResponse)
def change_password(
    data: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Current password is incorrect")
    strength_error = validate_password_strength(data.new_password)
    if strength_error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, strength_error)

    user.password_hash = hash_password(data.new_password)
    user.token_version += 1
    db.commit()

    log_activity(db, user, "password_change")
    db.commit()
    return _auth_response(user, settings)
