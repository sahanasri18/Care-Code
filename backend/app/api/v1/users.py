"""User account & medical profile management."""
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.core.qr import public_emergency_url
from app.models import MedicalProfile, User
from app.schemas.auth import UserOut
from app.schemas.common import Message
from app.schemas.profile import MedicalProfileIn, MedicalProfileOut, QRInfoOut
from app.services.account import delete_user
from app.services.activity import log_activity
from app.services.profile_service import upsert_profile

router = APIRouter(prefix="/users/me", tags=["users"])

PHOTO_DIR = "photos"
ALLOWED_PHOTO_TYPES = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
MAX_PHOTO_BYTES = 5 * 1024 * 1024


def _profile_to_out(profile: MedicalProfile, settings: Settings) -> MedicalProfileOut:
    out = MedicalProfileOut.model_validate(profile)
    out.photo_url = f"/api/v1/public/{profile.carecode}/photo" if profile.photo_filename else None
    out.public_url = public_emergency_url(settings, profile.carecode)
    return out


@router.get("", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.get("/profile", response_model=MedicalProfileOut)
def get_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if user.profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No medical profile yet")
    return _profile_to_out(user.profile, settings)


@router.post("/profile", response_model=MedicalProfileOut)
def save_profile(
    data: MedicalProfileIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    profile = upsert_profile(db, user, data)
    log_activity(db, user, "profile_update", {"fields": len(data.model_dump())})
    db.commit()
    return _profile_to_out(profile, settings)


@router.post("/profile/photo", response_model=MedicalProfileOut)
async def upload_photo(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if file.content_type not in ALLOWED_PHOTO_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Photo must be JPEG, PNG or WebP")

    contents = await file.read()
    if len(contents) > MAX_PHOTO_BYTES:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Photo must be 5 MB or smaller")

    profile = user.profile
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No medical profile yet")

    # Remove previous photo file before replacing.
    if profile.photo_filename:
        (settings.storage_path / PHOTO_DIR / profile.photo_filename).unlink(missing_ok=True)

    filename = f"{uuid.uuid4().hex}.{ALLOWED_PHOTO_TYPES[file.content_type]}"
    photos_dir = settings.storage_path / PHOTO_DIR
    photos_dir.mkdir(parents=True, exist_ok=True)
    (photos_dir / filename).write_bytes(contents)

    profile.photo_filename = filename
    db.commit()
    log_activity(db, user, "photo_upload")
    db.commit()
    return _profile_to_out(profile, settings)


@router.delete("/profile/photo", response_model=MedicalProfileOut)
def remove_photo(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    profile = user.profile
    if profile is None or not profile.photo_filename:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No photo to remove")
    (settings.storage_path / PHOTO_DIR / profile.photo_filename).unlink(missing_ok=True)
    profile.photo_filename = None
    db.commit()
    log_activity(db, user, "photo_removed")
    db.commit()
    return _profile_to_out(profile, settings)


@router.post("/regenerate-qr", response_model=QRInfoOut)
def regenerate_qr(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    profile = user.profile
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No medical profile yet")

    old_code = profile.carecode
    profile.carecode = str(uuid.uuid4())
    db.commit()
    log_activity(db, user, "qr_regenerate", {"previous_code": old_code})
    db.commit()
    return _qr_info(profile, settings)


def _qr_info(profile: MedicalProfile, settings: Settings) -> QRInfoOut:
    public_url = public_emergency_url(settings, profile.carecode)
    return QRInfoOut(
        carecode=profile.carecode,
        public_url=public_url,
        png_url=f"/api/v1/qr/{profile.carecode}/image?format=png",
        svg_url=f"/api/v1/qr/{profile.carecode}/image?format=svg",
        scan_count=profile.scan_count,
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    password: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    delete_user(db, user, settings, password=password)
    return None
