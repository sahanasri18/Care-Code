import uuid
from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class HospitalIn(ORMModel):
    name: str = Field(min_length=2, max_length=200)
    address: str = Field(min_length=5, max_length=300)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=50)
    pincode: str | None = Field(default=None, max_length=10)
    phone: str | None = Field(default=None, max_length=30)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    departments: list[str] = Field(default_factory=list)


class HospitalOut(HospitalIn):
    id: uuid.UUID
    created_at: datetime


class HospitalNearbyOut(HospitalOut):
    distance_km: float = 0.0
