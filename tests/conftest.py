import pytest

from app import create_app, db
from app.models import Restaurant, Review


@pytest.fixture
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
        }
    )
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_restaurant(app):
    restaurant = Restaurant(
        name="Test Bistro",
        area="Testville",
        service_type="sit-down",
        allergy_info_available=True,
    )
    restaurant.set_food_types(["Italian"])
    restaurant.set_occasions(["Family meal"])
    restaurant.set_dining_options(["Lunch", "Dinner"])
    db.session.add(restaurant)
    db.session.commit()
    return restaurant


@pytest.fixture
def valid_review_data():
    return {
        "reviewer_name": "Tester",
        "avg_expense_per_head": "25.00",
        "food_quality": "4",
        "ambiance": "4",
        "service_quality": "3",
        "cleanliness": "5",
        "speed_of_service": "3",
        "value_for_money": "4",
        "overall_rating": "very good",
        "report": "A solid meal with friendly staff and clean surroundings.",
    }
