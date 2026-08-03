"""Hospital catalog seed data — loaded from the static file shipped with the project.

Source of truth: app/data/hospitals.json (regenerate with
`python -m scripts.build_hospital_seed` from scripts/seed_data/).
"""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import Hospital

SEED_FILE = Path(__file__).resolve().parent.parent / "data" / "hospitals.json"

SEED_HOSPITALS: list[dict] = json.loads(SEED_FILE.read_text(encoding="utf-8"))


def seed_hospitals(db: Session) -> int:
    if db.query(Hospital.id).first() is not None:
        return 0
    count = 0
    for record in SEED_HOSPITALS:
        db.add(Hospital(**record))
        count += 1
    db.commit()
    return count
