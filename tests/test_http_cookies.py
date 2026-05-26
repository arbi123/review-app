"""Tests for browse filter cookie read/write behavior."""

from app.http_cookies import (
    COOKIE_AREA,
    COOKIE_FOOD,
    COOKIE_SORT,
    apply_browse_preferences,
    remember_browse_preferences,
)


class FakeRequest:
    def __init__(self, args=None, cookies=None):
        self.args = args or {}
        self.cookies = cookies or {}


class FakeResponse:
    def __init__(self):
        self.cookies = {}

    def set_cookie(self, key, value, **kwargs):
        self.cookies[key] = value

    def delete_cookie(self, key, path="/"):
        self.cookies.pop(key, None)


def test_apply_restores_from_cookies_on_bare_visit():
    req = FakeRequest(cookies={COOKIE_SORT: "rating", COOKIE_AREA: "Uptown", COOKIE_FOOD: "Asian"})
    area, sort, food = apply_browse_preferences(req, "", "name", "")
    assert area == "Uptown"
    assert sort == "rating"
    assert food == "Asian"


def test_apply_keeps_query_when_form_submitted_with_defaults():
    req = FakeRequest(args={"area": "", "food_type": "", "sort": "name", "q": ""})
    area, sort, food = apply_browse_preferences(req, "", "name", "")
    assert area == ""
    assert sort == "name"
    assert food == ""


def test_remember_saves_first_sort_option_and_clears_area_food():
    resp = FakeResponse()
    remember_browse_preferences(
        resp, area="", sort="name", food_type="", save=True
    )
    assert resp.cookies[COOKIE_SORT] == "name"
    assert COOKIE_AREA not in resp.cookies
    assert COOKIE_FOOD not in resp.cookies


def test_remember_saves_cuisine_cookie(client, sample_restaurant):
    response = client.get("/?area=&food_type=Italian&sort=name&q=")
    assert response.status_code == 200
    cookies = response.headers.getlist("Set-Cookie")
    assert any("tm_food=Italian" in c for c in cookies)

    response2 = client.get("/")
    assert b"Test Bistro" in response2.data
