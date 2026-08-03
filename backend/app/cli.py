"""Admin CLI utilities.

Usage (from backend/, after running `alembic upgrade head`):
    python -m app.cli create-admin EMAIL "Full Name" PASSWORD

Promotes an existing user to admin, or creates one if the email is unknown.
"""
import argparse
import sys
import uuid

from app.core.database import SessionLocal
from app.core.security import hash_password, validate_password_strength
from app.models import MedicalProfile, User


def create_admin(email: str, full_name: str, password: str) -> None:
    strength = validate_password_strength(password)
    if strength:
        print(f"error: {strength}")
        sys.exit(1)

    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email.lower()).first()
        if user is None:
            user = User(email=email.lower(), full_name=full_name, password_hash=hash_password(password))
            db.add(user)
            db.flush()
            profile = MedicalProfile(user_id=user.id, carecode=str(uuid.uuid4()), full_name=full_name)
            db.add(profile)
        user.role = "admin"
        user.is_active = True
        db.commit()
        print(f"admin ready: {user.email} (role=admin)")


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create-admin", help="Create or promote an admin user")
    p.add_argument("email")
    p.add_argument("full_name")
    p.add_argument("password")
    args = parser.parse_args()
    create_admin(args.email, args.full_name, args.password)


if __name__ == "__main__":
    main()
