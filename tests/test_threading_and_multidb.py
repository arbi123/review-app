"""
SE — Multi-threading and multi-database (optional) tests.
"""

import time

from app.background_stats import get_cached_stats, schedule_stats_refresh
from app.secondary_db import PageVisit


def test_multidb_page_visit_row(app):
    with app.app_context():
        from app import db

        record = PageVisit(path="/test")
        db.session.add(record)
        db.session.commit()
        assert PageVisit.query.filter_by(path="/test").count() == 1


def test_threading_stats_refresh_eventually_updates(app):
    schedule_stats_refresh(app)
    time.sleep(0.3)
    stats = get_cached_stats()
    assert "restaurant_count" in stats
    assert stats["refreshing"] is False
