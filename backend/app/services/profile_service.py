"""Profile upsert: replace contacts atomically, keep scan stats and carecode."""
import uuid

from sqlalchemy.orm import Session

from app.models import EmergencyContact, MedicalProfile, User
from app.schemas.profile import MedicalProfileIn


def get_or_create_profile(db: Session, user: User) -> MedicalProfile:
    if user.profile is None:
        profile = MedicalProfile(user_id=user.id, carecode=str(uuid.uuid4()), full_name=user.full_name)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return user.profile


def upsert_profile(db: Session, user: User, data: MedicalProfileIn) -> MedicalProfile:
    profile = get_or_create_profile(db, user)
    profile.full_name = data.full_name
    profile.date_of_birth = data.date_of_birth
    profile.gender = data.gender.lower() if data.gender else None
    profile.blood_group = data.blood_group.upper() if data.blood_group else None
    profile.allergies = data.allergies
    profile.conditions = data.conditions
    profile.medications = data.medications
    profile.address = data.address
    profile.notes = data.notes

    profile.contacts.clear()
    for c in data.contacts:
        profile.contacts.append(
            EmergencyContact(name=c.name.strip(), relationship=c.relationship.strip(), phone=c.phone.strip())
        )
    db.commit()
    db.refresh(profile)
    return profile
