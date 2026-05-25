from app.constants import (
    DINING_OPTIONS,
    FOOD_TYPES,
    OCCASIONS,
    OVERALL_RATINGS,
    SCORE_MAX,
    SCORE_MIN,
    SERVICE_TYPES,
)


def word_count(text: str) -> int:
    return len(text.split())


def validate_report(text: str) -> str | None:
    if not text or not text.strip():
        return "Report is required."
    if word_count(text) > 100:
        return f"Report must be at most 100 words (you entered {word_count(text)})."
    return None


def _parse_score(value, field_name: str) -> tuple[int | None, str | None]:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return None, f"{field_name} must be a number between {SCORE_MIN} and {SCORE_MAX}."
    if score < SCORE_MIN or score > SCORE_MAX:
        return None, f"{field_name} must be between {SCORE_MIN} and {SCORE_MAX}."
    return score, None


def validate_review(data: dict) -> tuple[dict | None, list[str]]:
    errors = []
    cleaned = {}

    expense = data.get("avg_expense_per_head", "").strip()
    try:
        expense_val = float(expense)
        if expense_val <= 0:
            raise ValueError
        cleaned["avg_expense_per_head"] = expense_val
    except (ValueError, AttributeError):
        errors.append("Average expense per head must be a positive number.")

    score_fields = [
        ("food_quality", "Food quality"),
        ("ambiance", "Ambiance"),
        ("service_quality", "Service quality"),
        ("cleanliness", "Cleanliness"),
        ("speed_of_service", "Speed of service"),
        ("value_for_money", "Value for money"),
    ]
    for key, label in score_fields:
        score, err = _parse_score(data.get(key), label)
        if err:
            errors.append(err)
        else:
            cleaned[key] = score

    overall = (data.get("overall_rating") or "").strip().lower()
    if overall not in OVERALL_RATINGS:
        errors.append("Please select a valid overall rating.")
    else:
        cleaned["overall_rating"] = overall

    report_err = validate_report(data.get("report", ""))
    if report_err:
        errors.append(report_err)
    else:
        cleaned["report"] = data.get("report", "").strip()

    name = (data.get("reviewer_name") or "").strip()
    cleaned["reviewer_name"] = name or None

    if errors:
        return None, errors
    return cleaned, []


def validate_restaurant(data: dict) -> tuple[dict | None, list[str]]:
    errors = []
    cleaned = {}

    name = (data.get("name") or "").strip()
    area = (data.get("area") or "").strip()
    if not name:
        errors.append("Restaurant name is required.")
    if not area:
        errors.append("Area is required.")
    cleaned["name"] = name
    cleaned["area"] = area

    service_type = (data.get("service_type") or "").strip().lower()
    if service_type not in SERVICE_TYPES:
        errors.append("Please select a valid service type.")
    else:
        cleaned["service_type"] = service_type

    food_types = [v for v in data.getlist("food_types") if v in FOOD_TYPES]
    occasions = [v for v in data.getlist("occasions") if v in OCCASIONS]
    dining_options = [
        v for v in data.getlist("dining_options") if v in DINING_OPTIONS
    ]

    if not food_types:
        errors.append("Select at least one food type.")
    if not occasions:
        errors.append("Select at least one occasion.")
    if not dining_options:
        errors.append("Select at least one dining option.")

    cleaned["food_types"] = food_types
    cleaned["occasions"] = occasions
    cleaned["dining_options"] = dining_options
    cleaned["allergy_info_available"] = data.get("allergy_info_available") == "on"
    cleaned["description"] = (data.get("description") or "").strip() or None

    if errors:
        return None, errors
    return cleaned, []
