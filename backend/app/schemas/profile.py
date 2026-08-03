import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator

from app.schemas.common import ORMModel

BLOOD_GROUPS = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
GENDERS = {"male", "female", "other", "prefer not to say"}


class EmergencyContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    relationship: str = Field(min_length=1, max_length=60)
    phone: str = Field(min_length=5, max_length=30)


class EmergencyContactOut(EmergencyContactIn, ORMModel):
    id: uuid.UUID


class MedicalProfileIn(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    date_of_birth: date | None = None
    gender: str | None = None
    blood_group: str | None = None
    allergies: str | None = Field(default=None, max_length=5000)
    conditions: str | None = Field(default=None, max_length=5000)
    medications: str | None = Field(default=None, max_length=5000)
    address: str | None = Field(default=None, max_length=2000)
    notes: str | None = Field(default=None, max_length=5000)
    contacts: list[EmergencyContactIn] = Field(default_factory=list, max_length=10)

    @model_validator(mode="after")
    def _validate_choices(self) -> "MedicalProfileIn":
        if self.blood_group and self.blood_group.upper() not in BLOOD_GROUPS:
            raise ValueError(f"blood_group must be one of {sorted(BLOOD_GROUPS)}")
        if self.gender and self.gender.lower() not in GENDERS:
            raise ValueError(f"gender must be one of {sorted(GENDERS)}")
        return self


class MedicalProfileOut(ORMModel):
    id: uuid.UUID
    carecode: str
    full_name: str
    date_of_birth: date | None
    gender: str | None
    blood_group: str | None
    allergies: str | None
    conditions: str | None
    medications: str | None
    address: str | None
    notes: str | None
    photo_url: str | None = None
    scan_count: int
    last_scanned_at: datetime | None
    contacts: list[EmergencyContactOut]
    public_url: str | None = None
    created_at: datetime
    updated_at: datetime


class PublicProfileOut(BaseModel):
    carecode: str
    full_name: str
    age: int | None
    gender: str | None
    blood_group: str | None
    allergies: str | None
    conditions: str | None
    medications: str | None
    address: str | None
    notes: str | None
    photo_url: str | None
    contacts: list[EmergencyContactOut]


class QRInfoOut(BaseModel):
    carecode: str
    public_url: str
    png_url: str
    svg_url: str
    scan_count: int
