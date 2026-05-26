"""
SE — Black-box testing: exercise the app only through public HTTP (no internal imports).

We treat the Flask test client as an external client that does not know implementation details.
"""


def test_blackbox_homepage_status(client):
    response = client.get("/")
    assert response.status_code == 200


def test_blackbox_add_restaurant_via_http(client):
    response = client.post(
        "/restaurants/new",
        data={
            "name": "Black Box Cafe",
            "area": "Uptown",
            "service_type": "cafe",
            "food_types": "American",
            "occasions": "Casual",
            "dining_options": "Breakfast",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Black Box Cafe" in response.data


def test_blackbox_health_servlet_json(client):
    """Black-box call to the servlet-style JSON endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert "socket_probe" in payload
    assert "http_probe" in payload


def test_blackbox_browse_cookies_round_trip(client, sample_restaurant):
    client.set_cookie("tm_area", "Testville")
    client.set_cookie("tm_sort", "rating")
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data


def test_blackbox_default_sort_cookie_updates(client, sample_restaurant):
    client.set_cookie("tm_sort", "rating")
    client.get("/?area=&food_type=&sort=name&q=")
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Bistro" in response.data
