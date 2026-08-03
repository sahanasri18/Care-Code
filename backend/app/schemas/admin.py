from datetime import datetime

from pydantic import BaseModel


class ActivityOut(BaseModel):
    action: str
    detail: dict | None
    created_at: datetime


class ScanStatsOut(BaseModel):
    total_scans: int
    scans_last_30_days: int
    last_scanned_at: datetime | None


class AdminStatsOut(BaseModel):
    """Aggregate platform analytics only — never per-user or medical data."""

    total_users: int
    active_users: int
    total_profiles: int
    total_scans: int
    total_hospitals: int
    signups_last_30_days: int
    scans_last_30_days: int
    signups_per_day: list[dict]
