"""QR asset endpoints: image generation (PNG/SVG) and printable card."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.core.qr import generate_png, generate_svg, public_emergency_url
from app.models import MedicalProfile, User
from app.schemas.profile import QRInfoOut

router = APIRouter(prefix="/qr", tags=["qr"])


def _resolve_profile_by_code(db: Session, code: str) -> MedicalProfile:
    """Any missing code — deleted profile, regenerated QR — resolves to 410 Gone."""
    profile = db.query(MedicalProfile).filter(MedicalProfile.carecode == code).first()
    if profile is None or profile.user is None or not profile.user.is_active:
        raise HTTPException(
            status.HTTP_410_GONE,
            "This CareCode profile is no longer available. "
            "The owner has deleted or deactivated this emergency profile.",
        )
    return profile


@router.get("/me", response_model=QRInfoOut)
def my_qr(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if user.profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No medical profile yet")
    public_url = public_emergency_url(settings, user.profile.carecode)
    return QRInfoOut(
        carecode=user.profile.carecode,
        public_url=public_url,
        png_url=f"/api/v1/qr/{user.profile.carecode}/image?format=png",
        svg_url=f"/api/v1/qr/{user.profile.carecode}/image?format=svg",
        scan_count=user.profile.scan_count,
    )


@router.get("/{code}/image")
def qr_image(
    code: str,
    format: str = Query(default="png", pattern="^(png|svg)$"),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    _resolve_profile_by_code(db, code)
    if format == "svg":
        return Response(
            content=generate_svg(settings, code),
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"},
        )
    return Response(
        content=generate_png(settings, code),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/{code}/card", response_class=HTMLResponse)
def qr_card(
    code: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    profile = db.query(MedicalProfile).filter(MedicalProfile.carecode == code).first()
    if profile is None or profile.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "QR card not found")

    url = public_emergency_url(settings, code)
    png = generate_png(settings, code)
    import base64

    b64 = base64.b64encode(png).decode()
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>CareCode — Emergency Card</title>
<style>
  body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; padding: 40px; background:#fff; }}
  .card {{ width: 320px; border: 3px solid #E11D48; border-radius: 16px; padding: 20px; text-align: center; }}
  .logo {{ color:#0B5FFF; font-weight: bold; font-size: 18px; }}
  .name {{ font-size: 20px; font-weight: bold; margin: 8px 0; }}
  .info {{ color:#475569; font-size: 13px; margin-bottom: 12px; }}
  img {{ width: 200px; height: 200px; }}
  .url {{ font-size: 10px; color:#94a3b8; word-break: break-all; margin-top: 8px; }}
  @media print {{ body {{ padding: 0; }} }}
</style></head><body>
  <div class="card">
    <div class="logo">&#9671; CareCode</div>
    <div class="name">{profile.full_name}</div>
    <div class="info">{profile.blood_group or ''} {'·' if profile.blood_group and profile.date_of_birth else ''} {profile.date_of_birth.strftime('%d %b %Y') if profile.date_of_birth else ''}</div>
    <img src="data:image/png;base64,{b64}" alt="CareCode QR"/>
    <div class="info">In an emergency, scan this QR code.</div>
    <div class="url">{url}</div>
  </div>
  <script>window.onload = () => window.print();</script>
</body></html>"""
    return HTMLResponse(html)
