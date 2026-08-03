"""Business services shared across routers."""
from app.models.activity import ActivityLog
from app.models.user import User
from sqlalchemy.orm import Session


def log_activity(db: Session, user: User, action: str, detail: dict | None = None) -> None:
    db.add(ActivityLog(user_id=user.id, action=action, detail=detail))
