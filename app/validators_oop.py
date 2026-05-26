"""
SE — Object-oriented design, interfaces (ABC), and inheritance.

Validators share a common interface and base class; restaurant/review validators specialize behavior.
"""

from abc import ABC, abstractmethod

from werkzeug.datastructures import ImmutableMultiDict

from app.constants import (
    DINING_OPTIONS,
    FOOD_TYPES,
    OCCASIONS,
    OVERALL_RATINGS,
    SCORE_MAX,
    SCORE_MIN,
    SERVICE_TYPES,
)
from app.report_rules import validate_report


class Validatable(ABC):
    """SE — Interface (ABC): contract that every form validator must implement."""

    @abstractmethod
    def validate(self, data) -> tuple[dict | None, list[str]]:
        """Return (cleaned_data, errors) — errors empty when valid."""


class BaseFormValidator(Validatable):
    """SE — Inheritance: shared helpers for subclasses."""

    def _parse_score(self, value, field_name: str) -> tuple[int | None, str | None]:
        try:
            score = int(value)
        except (TypeError, ValueError):
            return None, f"{field_name} must be a number between {SCORE_MIN} and {SCORE_MAX}."
        if score < SCORE_MIN or score > SCORE_MAX:
            return None, f"{field_name} must be between {SCORE_MIN} and {SCORE_MAX}."
        return score, None


class RestaurantFormValidator(BaseFormValidator):
    """SE — Inheritance: specializes BaseFormValidator for restaurant POST data."""

    def validate(self, data) -> tuple[dict | None, list[str]]:
        if not hasattr(data, "getlist"):
            data = ImmutableMultiDict(data)

        errors: list[str] = []
        name = (data.get("name") or "").strip()
        area = (data.get("area") or "").strip()
        if not name:
            errors.append("Restaurant name is required.")
        if not area:
            errors.append("Area is required.")

        service_type = (data.get("service_type") or "").strip().lower()
        if service_type not in SERVICE_TYPES:
            errors.append("Please select a valid service type.")

        food_types = [v for v in data.getlist("food_types") if v in FOOD_TYPES]
        occasions = [v for v in data.getlist("occasions") if v in OCCASIONS]
        dining_options = [v for v in data.getlist("dining_options") if v in DINING_OPTIONS]

        if not food_types:
            errors.append("Select at least one food type.")
        if not occasions:
            errors.append("Select at least one occasion.")
        if not dining_options:
            errors.append("Select at least one dining option.")

        if errors:
            return None, errors

        return {
            "name": name,
            "area": area,
            "service_type": service_type,
            "food_types": food_types,
            "occasions": occasions,
            "dining_options": dining_options,
            "allergy_info_available": data.get("allergy_info_available") == "on",
            "description": (data.get("description") or "").strip() or None,
        }, []


class ReviewFormValidator(BaseFormValidator):
    """SE — Inheritance: specializes BaseFormValidator for review POST data."""

    def validate(self, data) -> tuple[dict | None, list[str]]:
        errors: list[str] = []
        cleaned: dict = {}

        expense = (data.get("avg_expense_per_head") or "").strip()
        try:
            expense_val = float(expense)
            if expense_val <= 0:
                raise ValueError
            cleaned["avg_expense_per_head"] = expense_val
        except (ValueError, TypeError):
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
            score, err = self._parse_score(data.get(key), label)
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
            cleaned["report"] = (data.get("report") or "").strip()

        name = (data.get("reviewer_name") or "").strip()
        cleaned["reviewer_name"] = name or None

        if errors:
            return None, errors
        return cleaned, []
