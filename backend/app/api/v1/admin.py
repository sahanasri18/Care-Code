"""Admin-only endpoints: hospital CRUD and platform analytics.

Privacy-first: admins manage only application resources. User accounts and
medical profiles are strictly self-service (Account Settings) and no admin
endpoint exposes them.
"""
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models import Hospital, MedicalProfile, ScanEvent, User
from app.schemas.admin import AdminStatsOut
from app.schemas.hospital import HospitalIn, HospitalOut
from app.schemas.pagination import Paginated, PaginationParams, paginate

router = APIRouter(prefix="/admin", tags=["admin"])


# --------------------------------------------------------------------------
# Hospitals
# --------------------------------------------------------------------------
@router.get("/hospitals", response_model=Paginated)
def admin_list_hospitals(
    q: str | None = Query(default=None, max_length=100),
    params: PaginationParams = Depends(),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Hospital)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            Hospital.name.ilike(like)
            | Hospital.city.ilike(like)
            | Hospital.state.ilike(like)
            | Hospital.address.ilike(like)
        )
    total = query.count()
    hospitals = (
        query.order_by(Hospital.name).offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    )
    return paginate(total, [HospitalOut.model_validate(h) for h in hospitals], params)


@router.post("/hospitals", response_model=HospitalOut, status_code=status.HTTP_201_CREATED)
def admin_create_hospital(
    data: HospitalIn,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    hospital = Hospital(**data.model_dump())
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital


@router.put("/hospitals/{hospital_id}", response_model=HospitalOut)
def admin_update_hospital(
    hospital_id: uuid.UUID,
    data: HospitalIn,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    hospital = db.get(Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Hospital not found")
    for key, value in data.model_dump().items():
        setattr(hospital, key, value)
    db.commit()
    db.refresh(hospital)
    return hospital


@router.delete("/hospitals/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_hospital(
    hospital_id: uuid.UUID,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    hospital = db.get(Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Hospital not found")
    db.delete(hospital)
    db.commit()
    return None


# --------------------------------------------------------------------------
# Stats
# --------------------------------------------------------------------------
@router.get("/stats", response_model=AdminStatsOut)
def admin_stats(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    since_30 = datetime.now(timezone.utc) - timedelta(days=30)

    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active.is_(True)).count()
    total_profiles = db.query(MedicalProfile).count()
    total_scans = db.query(func.sum(MedicalProfile.scan_count)).scalar() or 0
    total_hospitals = db.query(Hospital).count()
    signups_30 = db.query(User).filter(User.created_at >= since_30).count()
    scans_30 = db.query(ScanEvent).filter(ScanEvent.created_at >= since_30).count()

    signups_per_day = [
        {"date": str(d[0]), "count": d[1]}
        for d in db.query(func.date(User.created_at), func.count(User.id))
        .filter(User.created_at >= since_30)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
        .all()
    ]

    return AdminStatsOut(
        total_users=total_users,
        active_users=active_users,
        total_profiles=total_profiles,
        total_scans=total_scans,
        total_hospitals=total_hospitals,
        signups_last_30_days=signups_30,
        scans_last_30_days=scans_30,
        signups_per_day=signups_per_day,
    )
