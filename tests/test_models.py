from app import db
from app.models import Restaurant, Review


def test_restaurant_json_fields(app, sample_restaurant):
    assert sample_restaurant.get_food_types() == ["Italian"]
    assert sample_restaurant.get_occasions() == ["Family meal"]
    assert sample_restaurant.get_dining_options() == ["Lunch", "Dinner"]


def test_review_cascade_delete(app, sample_restaurant):
    review = Review(
        restaurant_id=sample_restaurant.id,
        avg_expense_per_head=20.0,
        food_quality=4,
        ambiance=4,
        service_quality=4,
        cleanliness=4,
        speed_of_service=4,
        value_for_money=4,
        overall_rating="average",
        report="Decent place for a quick lunch.",
    )
    db.session.add(review)
    db.session.commit()

    db.session.delete(sample_restaurant)
    db.session.commit()
    assert Review.query.count() == 0


def test_restaurant_review_count(app, sample_restaurant):
    assert sample_restaurant.review_count == 0
