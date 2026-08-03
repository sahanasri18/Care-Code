"""Account lifecycle: irreversible deletion with complete data cleanup.

Deletion removes (via ORM cascade):
- medical profile, emergency contacts, scan events
- password reset tokens, activity logs
- uploaded profile photo file
The user row itself is the cascade root; every user-derived row is deleted.
"""
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import verify_password
from app.models import ActivityLog, PasswordResetToken, User

NOT_AVAILABLE_DETAIL = "This CareCode profile is no longer available."


def _delete_photo_file(settings: Settings, user: User) -> None:
    if user.profile and user.profile.photo_filename:
        path = Path(settings.storage_dir) / "photos" / user.profile.photo_filename
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def delete_user(db: Session, user: User, settings: Settings, password: str | None = None) -> None:
    """Permanently delete a user and all personal data.

    `password` is required for self-deletion (defense in depth). Admin deletion passes None.
    """
    if password is not None:
        if password == "":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Password is required to delete your account")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect password")

    _delete_photo_file(settings, user)
    # Explicit child cleanup (works regardless of DB FK enforcement):
    # profile, contacts and scan events cascade via ORM relationships.
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
    db.query(ActivityLog).filter(ActivityLog.user_id == user.id).delete()
    db.delete(user)
    db.commit()


def ensure_profile_available(profile) -> bool:
    """A profile is publicly available only if its owner exists and is active."""
    return profile is not None and profile.user is not None and profile.user.is_active
