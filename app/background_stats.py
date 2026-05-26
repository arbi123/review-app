"""
SE — Multi-threading: refresh aggregate counters on a background worker thread.
"""

import logging
import threading
from typing import Any

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_stats: dict[str, Any] = {
    "restaurant_count": 0,
    "review_count": 0,
    "refreshing": False,
}


def get_cached_stats() -> dict[str, Any]:
    with _lock:
        return dict(_stats)


def schedule_stats_refresh(app) -> None:
    """Start a daemon thread so the HTTP request thread is not blocked."""

    def _worker():
        with app.app_context():
            from sqlalchemy import func

            from app import db
            from app.models import Restaurant, Review

            try:
                with _lock:
                    _stats["refreshing"] = True
                restaurant_count = Restaurant.query.count()
                review_count = db.session.query(func.count(Review.id)).scalar() or 0
                with _lock:
                    _stats["restaurant_count"] = restaurant_count
                    _stats["review_count"] = review_count
                logger.debug(
                    "Background stats refreshed: %d restaurants, %d reviews.",
                    restaurant_count,
                    review_count,
                )
            except Exception as exc:
                logger.exception("Background stats refresh failed: %s", exc)
            finally:
                with _lock:
                    _stats["refreshing"] = False

    threading.Thread(target=_worker, name="tastemap-stats", daemon=True).start()
