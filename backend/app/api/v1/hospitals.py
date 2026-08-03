"""Hospital directory: list, search, nearby (haversine), details."""
import math
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Hospital
from app.schemas.hospital import HospitalNearbyOut, HospitalOut
from app.schemas.pagination import PaginationParams, Paginated, paginate

router = APIRouter(prefix="/hospitals", tags=["hospitals"])

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = p2 - p1
    dlon = math.radians(lon2) - math.radians(lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


@router.get("", response_model=Paginated)
def list_hospitals(
    q: str | None = Query(default=None, max_length=100),
    city: str | None = Query(default=None, max_length=100),
    state: str | None = Query(default=None, max_length=50),
    params: PaginationParams = Depends(),
    db: Session = Depends(get_db),
):
    query = db.query(Hospital)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Hospital.name.ilike(like),
                Hospital.city.ilike(like),
                Hospital.state.ilike(like),
                Hospital.address.ilike(like),
            )
        )
    if city:
        query = query.filter(Hospital.city.ilike(f"%{city.strip()}%"))
    if state:
        query = query.filter(Hospital.state.ilike(f"%{state.strip()}%"))

    total = query.count()
    items = query.order_by(Hospital.name).offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    return paginate(total, [HospitalOut.model_validate(h) for h in items], params)


@router.get("/cities")
def list_cities(db: Session = Depends(get_db)):
    rows = db.query(Hospital.city).distinct().order_by(Hospital.city).all()
    return {"cities": [r[0] for r in rows]}


@router.get("/states")
def list_states(db: Session = Depends(get_db)):
    rows = db.query(Hospital.state).distinct().order_by(Hospital.state).all()
    return {"states": [r[0] for r in rows]}


@router.get("/nearby", response_model=list[HospitalNearbyOut])
def nearby_hospitals(
    lat: float = Query(ge=-90, le=90),
    lng: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=25, ge=1, le=500),
    db: Session = Depends(get_db),
):
    hospitals = db.query(Hospital).all()
    results = []
    for h in hospitals:
        distance = haversine_km(lat, lng, h.latitude, h.longitude)
        if distance <= radius_km:
            out = HospitalNearbyOut.model_validate(h)
            out.distance_km = round(distance, 1)
            results.append(out)
    results.sort(key=lambda x: x.distance_km)
    return results[:50]


@router.get("/{hospital_id}", response_model=HospitalOut)
def hospital_detail(hospital_id: uuid.UUID, db: Session = Depends(get_db)):
    hospital = db.get(Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Hospital not found")
    return hospital
