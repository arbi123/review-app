import json
from datetime import datetime, timezone

from app import db
from app.helpers import restaurant_average_score, review_score_average


class TimestampMixin:
    """SE — Inheritance (mixin): shared created_at column for concrete models."""

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_type = db.Column(db.String(50), nullable=False)
    food_types = db.Column(db.Text, nullable=False, default="[]")
    occasions = db.Column(db.Text, nullable=False, default="[]")
    dining_options = db.Column(db.Text, nullable=False, default="[]")
    allergy_info_available = db.Column(db.Boolean, nullable=False, default=False)
    cover_image = db.Column(db.String(500), nullable=True)
    reviews = db.relationship(
        "Review", backref="restaurant", lazy=True, cascade="all, delete-orphan"
    )

    def get_food_types(self):
        return json.loads(self.food_types)

    def set_food_types(self, values):
        self.food_types = json.dumps(values)

    def get_occasions(self):
        return json.loads(self.occasions)

    def set_occasions(self, values):
        self.occasions = json.dumps(values)

    def get_dining_options(self):
        return json.loads(self.dining_options)

    def set_dining_options(self, values):
        self.dining_options = json.dumps(values)

    @property
    def review_count(self):
        return len(self.reviews)

    @property
    def average_score(self):
        return restaurant_average_score(self)


class Review(TimestampMixin, db.Model):
    """SE — Inheritance: Review inherits TimestampMixin.created_at."""

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurants.id"), nullable=False
    )
    reviewer_name = db.Column(db.String(80), nullable=True)
    avg_expense_per_head = db.Column(db.Float, nullable=False)
    food_quality = db.Column(db.Integer, nullable=False)
    ambiance = db.Column(db.Integer, nullable=False)
    service_quality = db.Column(db.Integer, nullable=False)
    cleanliness = db.Column(db.Integer, nullable=False)
    speed_of_service = db.Column(db.Integer, nullable=False)
    value_for_money = db.Column(db.Integer, nullable=False)
    overall_rating = db.Column(db.String(20), nullable=False)
    report = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(500), nullable=True)

    @property
    def average_score(self):
        return review_score_average(self)
