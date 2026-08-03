"""Lightweight in-memory sliding-window rate limiter (per-process).

Sufficient for a single Render web service. Switches off with RATE_LIMIT_ENABLED=false.
"""
import threading
import time
from collections import defaultdict, deque

from app.core.config import Settings

_lock = threading.Lock()
_buckets: dict[str, deque[float]] = defaultdict(deque)


def _prune(key: str, window: float, now: float) -> None:
    bucket = _buckets[key]
    while bucket and bucket[0] <= now - window:
        bucket.popleft()
    if not bucket:
        _buckets.pop(key, None)


def rate_limit(settings: Settings, key: str, limit: int, window_seconds: float) -> bool:
    """Record one hit for `key`. Return True if allowed, False if rate limited."""
    if not settings.rate_limit_enabled:
        return True
    now = time.monotonic()
    with _lock:
        _prune(key, window_seconds, now)
        bucket = _buckets[key]
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True
