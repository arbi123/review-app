from flask import url_for

from app.images import DEFAULT_RESTAURANT_IMAGE, FOOD_TYPE_IMAGES

SCORE_LABELS = [
    ("food_quality", "Food"),
    ("ambiance", "Ambiance"),
    ("service_quality", "Service"),
    ("cleanliness", "Cleanliness"),
    ("speed_of_service", "Speed"),
    ("value_for_money", "Value"),
]

def resolve_image(path: str | None, fallback: str | None = None) -> str:
    if not path:
        return fallback or DEFAULT_RESTAURANT_IMAGE
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return url_for("static", filename=path)


def restaurant_fallback_image(restaurant) -> str:
    from app.images import RESTAURANT_COVERS

    cover = RESTAURANT_COVERS.get(restaurant.name)
    if cover:
        return cover
    for food in restaurant.get_food_types():
        if food in FOOD_TYPE_IMAGES:
            return FOOD_TYPE_IMAGES[food]
    return DEFAULT_RESTAURANT_IMAGE


def review_score_average(review) -> float:
    scores = [
        review.food_quality,
        review.ambiance,
        review.service_quality,
        review.cleanliness,
        review.speed_of_service,
        review.value_for_money,
    ]
    return sum(scores) / len(scores)


def restaurant_average_score(restaurant) -> float | None:
    if not restaurant.reviews:
        return None
    return sum(review_score_average(r) for r in restaurant.reviews) / len(restaurant.reviews)


def restaurant_average_expense(restaurant) -> float | None:
    if not restaurant.reviews:
        return None
    return sum(r.avg_expense_per_head for r in restaurant.reviews) / len(restaurant.reviews)


def stars_html(score: float, max_stars: int = 5) -> str:
    full = int(round(score))
    full = max(0, min(full, max_stars))
    return "★" * full + "☆" * (max_stars - full)
