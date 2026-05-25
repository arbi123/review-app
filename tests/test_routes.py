from app.models import Review


def test_index_empty(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No restaurants match" in response.data


def test_index_with_restaurant(client, sample_restaurant):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data


def test_index_area_filter(client, sample_restaurant):
    response = client.get("/?area=Testville")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data

    response = client.get("/?area=Nowhere")
    assert b"No restaurants match" in response.data


def test_index_search(client, sample_restaurant):
    response = client.get("/?q=Bistro")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data


def test_index_sort_rating(client, app, sample_restaurant):
    from app import db
    from app.models import Review

    with app.app_context():
        db.session.add(
            Review(
                restaurant_id=sample_restaurant.id,
                avg_expense_per_head=10,
                food_quality=5,
                ambiance=5,
                service_quality=5,
                cleanliness=5,
                speed_of_service=5,
                value_for_money=5,
                overall_rating="excellent",
                report="Amazing.",
            )
        )
        db.session.commit()

    response = client.get("/?sort=rating")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data


def test_restaurant_detail(client, sample_restaurant):
    response = client.get(f"/restaurants/{sample_restaurant.id}")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data
    assert b"Allergy" in response.data


def test_add_review_success(client, sample_restaurant, valid_review_data):
    response = client.post(
        f"/restaurants/{sample_restaurant.id}/review",
        data=valid_review_data,
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Review submitted successfully" in response.data
    assert b"A solid meal" in response.data
    assert Review.query.count() == 1


def test_add_review_rejects_long_report(client, sample_restaurant, valid_review_data):
    data = {**valid_review_data, "report": "word " * 101}
    response = client.post(
        f"/restaurants/{sample_restaurant.id}/review",
        data=data,
    )
    assert response.status_code == 200
    assert b"100 words" in response.data
    assert Review.query.count() == 0


def test_add_restaurant(client):
    response = client.post(
        "/restaurants/new",
        data={
            "name": "New Place",
            "area": "Uptown",
            "description": "A trendy new spot.",
            "service_type": "sit-down",
            "food_types": "Asian",
            "occasions": "Casual",
            "dining_options": "Lunch",
            "allergy_info_available": "on",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"New Place" in response.data
    assert b"Restaurant added successfully" in response.data
