"""
SE — Multi-database (optional): analytics bind separate from the main reviews database.
"""

from datetime import datetime, timezone

from app import db


class PageVisit(db.Model):
    """Stored in the 'analytics' SQLAlchemy bind — not the primary reviews.db."""

    __bind_key__ = "analytics"
    __tablename__ = "page_visits"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)
    visited_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


def record_page_visit(path: str) -> None:
    """Persist a lightweight analytics row to the secondary database."""
    visit = PageVisit(path=path[:200])
    db.session.add(visit)
    db.session.commit()
