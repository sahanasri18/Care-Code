"""Build the static hospital seed file shipped with the project.

Assembles records from scripts/seed_data/*.py and writes
backend/app/data/hospitals.json. Run from backend/:

    python -m scripts.build_hospital_seed
"""
import json
from collections import Counter
from pathlib import Path

from scripts.seed_data import east, north, south, tn, west

DEPT_SETS = {
    "DH": ["Emergency", "General Medicine", "General Surgery", "Pediatrics", "OBG"],
    "MC": ["Emergency", "General Medicine", "General Surgery", "Cardiology", "Neurology", "Pediatrics"],
    "PR": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology"],
    "PR2": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
    "PHC": ["General Medicine", "Maternity", "Pediatrics"],
    "EYE": ["Ophthalmology", "Emergency"],
    "CH": ["Pediatrics", "Emergency", "General Medicine"],
    "ONC": ["Oncology", "Emergency"],
    "ORTH": ["Orthopedics", "Emergency", "General Medicine"],
}

OUT = Path(__file__).resolve().parent.parent / "app" / "data" / "hospitals.json"


def expand(state: str, records: list) -> list[dict]:
    return [
        {
            "name": name,
            "address": address,
            "city": city,
            "state": state,
            "pincode": pincode,
            "phone": phone,
            "latitude": lat,
            "longitude": lng,
            "departments": DEPT_SETS[dept_key],
        }
        for name, address, city, pincode, phone, lat, lng, dept_key in records
    ]


def main() -> None:
    records = []
    for module in (tn, south, west, north, east):
        for state, state_records in module.STATES:
            records.extend(expand(state, state_records))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    by_state = Counter(r["state"] for r in records)
    print(f"wrote {OUT} — {len(records)} hospitals across {len(by_state)} states/UTs")
    for state, count in sorted(by_state.items(), key=lambda kv: -kv[1]):
        print(f"  {state}: {count}")


if __name__ == "__main__":
    main()
