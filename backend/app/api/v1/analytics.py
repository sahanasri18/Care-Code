"""Per-user analytics: scan counts and recent activity."""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import ActivityLog, ScanEvent, User
from app.schemas.admin import ActivityOut, ScanStatsOut

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/me", response_model=ScanStatsOut)
def my_analytics(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = user.profile
    if profile is None:
        return ScanStatsOut(total_scans=0, scans_last_30_days=0, last_scanned_at=None)

    since = datetime.now(timezone.utc) - timedelta(days=30)
    recent = (
        db.query(ScanEvent.id)
        .filter(ScanEvent.profile_id == profile.id, ScanEvent.created_at >= since)
        .count()
    )
    return ScanStatsOut(
        total_scans=profile.scan_count,
        scans_last_30_days=recent,
        last_scanned_at=profile.last_scanned_at,
    )


@router.get("/me/activity", response_model=list[ActivityOut])
def my_activity(
    limit: int = 20,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(min(limit, 100))
        .all()
    )
    return [ActivityOut(action=r.action, detail=r.detail, created_at=r.created_at) for r in rows]
