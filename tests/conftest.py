import sys

import pytest

from app import create_app, db
from app.models import Restaurant, Review


def pytest_sessionstart(session):
    """Visible in GitHub Actions when pytest runs with -s."""
    print("\n" + "=" * 60, flush=True)
    print("TasteMap - starting test session", flush=True)
    print("=" * 60 + "\n", flush=True)


def pytest_runtest_logstart(nodeid, location):
    file_path, line_no, test_name = location
    print(f"[TEST START] {test_name} ({file_path}:{line_no})", flush=True)
    print(f"             nodeid: {nodeid}", flush=True)


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    label = report.outcome.upper()
    print(f"[TEST {label}] {report.nodeid}", flush=True)
    if report.outcome == "failed" and report.longrepr:
        print(f"             reason: {report.longreprtext.splitlines()[0]}", flush=True)
    sys.stdout.flush()


def pytest_sessionfinish(session, exitstatus):
    print("\n" + "=" * 60, flush=True)
    print(f"TasteMap - test session finished (exit status {exitstatus})", flush=True)
    print("=" * 60 + "\n", flush=True)


@pytest.fixture
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_BINDS": {"analytics": "sqlite:///:memory:"},
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
