from app.helpers import (
    resolve_image,
    restaurant_average_score,
    review_score_average,
)
from app.validation import validate_report, word_count


def test_review_score_average(sample_restaurant, app):
    from app import db
    from app.models import Review

    with app.app_context():
        review = Review(
            restaurant_id=sample_restaurant.id,
            avg_expense_per_head=20,
            food_quality=5,
            ambiance=3,
            service_quality=4,
            cleanliness=4,
            speed_of_service=4,
            value_for_money=4,
            overall_rating="average",
            report="Test report here.",
        )
        assert review_score_average(review) == 4.0


def test_restaurant_average_score(sample_restaurant, app):
    from app import db
    from app.models import Review

    with app.app_context():
        db.session.add(
            Review(
                restaurant_id=sample_restaurant.id,
                avg_expense_per_head=20,
                food_quality=4,
                ambiance=4,
                service_quality=4,
                cleanliness=4,
                speed_of_service=4,
                value_for_money=4,
                overall_rating="average",
                report="Nice place.",
            )
        )
        db.session.commit()
        sample_restaurant = db.session.get(
            type(sample_restaurant), sample_restaurant.id
        )
        assert restaurant_average_score(sample_restaurant) == 4.0


def test_resolve_image_url():
    assert resolve_image("https://example.com/img.jpg").startswith("https://")


def test_word_count_from_validation():
    assert word_count("one two three") == 3
    assert validate_report("short report") is None
