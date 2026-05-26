"""
SE — HTTP cookies: persist lightweight browse preferences on the client.
"""

from flask import Request, Response

COOKIE_SORT = "tm_sort"
COOKIE_AREA = "tm_area"
COOKIE_FOOD = "tm_food"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days

# Present when the user clicks "Apply filters" on the home page (even if values are defaults).
BROWSE_FILTER_KEYS = ("area", "food_type", "sort", "q")


def filters_explicitly_submitted(request: Request) -> bool:
    """True when the browse form was submitted, not a bare visit to /."""
    return any(key in request.args for key in BROWSE_FILTER_KEYS)


def apply_browse_preferences(
    request: Request, area: str, sort: str, food_type: str
) -> tuple[str, str, str]:
    """
    Restore area/sort/cuisine from cookies only on a bare GET /.
    When the filter form is submitted, keep query values (including first/default options).
    """
    if filters_explicitly_submitted(request):
        return area, sort or "name", food_type

    area = request.cookies.get(COOKIE_AREA, "")
    sort = request.cookies.get(COOKIE_SORT, "name")
    food_type = request.cookies.get(COOKIE_FOOD, "")
    return area, sort or "name", food_type


def _set_or_clear_cookie(response: Response, name: str, value: str) -> None:
    if value:
        response.set_cookie(
            name,
            value,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="Lax",
        )
    else:
        response.delete_cookie(name, path="/")


def remember_browse_preferences(
    response: Response,
    area: str,
    sort: str,
    food_type: str,
    *,
    save: bool,
) -> Response:
    """
    Write cookies after "Apply filters". Saves all choices, including
    Name sort, All areas, and All cuisines (clears stale cookies when empty).
    """
    if not save:
        return response

    response.set_cookie(
        COOKIE_SORT,
        sort or "name",
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="Lax",
    )
    _set_or_clear_cookie(response, COOKIE_AREA, area)
    _set_or_clear_cookie(response, COOKIE_FOOD, food_type)
    return response
