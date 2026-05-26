from app.constants import SCORE_MAX, SCORE_MIN
from app.report_rules import validate_report, word_count
from app.validators_oop import RestaurantFormValidator, ReviewFormValidator

# SE — OOP: validators implement Validatable interface via inheritance.
_restaurant_validator = RestaurantFormValidator()
_review_validator = ReviewFormValidator()


def _parse_score(value, field_name: str) -> tuple[int | None, str | None]:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return None, f"{field_name} must be a number between {SCORE_MIN} and {SCORE_MAX}."
    if score < SCORE_MIN or score > SCORE_MAX:
        return None, f"{field_name} must be between {SCORE_MIN} and {SCORE_MAX}."
    return score, None


def validate_review(data: dict) -> tuple[dict | None, list[str]]:
    # SE — OOP validator used when the review form is submitted (see add_review route).
    return _review_validator.validate(data)


def validate_restaurant(data: dict) -> tuple[dict | None, list[str]]:
    # SE — OOP validator used when the add-restaurant form is submitted.
    return _restaurant_validator.validate(data)
