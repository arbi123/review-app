"""
SE — White-box testing: tests know internal branches and call private helpers directly.
"""

import pytest

from app.validation import _parse_score, validate_report, validate_review
from app.validators_oop import RestaurantFormValidator, ReviewFormValidator


def test_whitebox_parse_score_boundary_low():
    score, err = _parse_score("1", "Food quality")
    assert score == 1
    assert err is None


def test_whitebox_parse_score_boundary_high():
    score, err = _parse_score("5", "Food quality")
    assert score == 5
    assert err is None


def test_whitebox_parse_score_below_min_branch():
    score, err = _parse_score("0", "Food quality")
    assert score is None
    assert "between" in err


def test_whitebox_parse_score_non_numeric_branch():
    score, err = _parse_score("abc", "Food quality")
    assert score is None
    assert "number" in err


def test_whitebox_validate_report_exactly_100_words():
    text = " ".join(["word"] * 100)
    assert validate_report(text) is None


def test_whitebox_review_validator_collects_multiple_errors(valid_review_data):
    data = {**valid_review_data, "avg_expense_per_head": "-1", "overall_rating": "nope"}
    cleaned, errors = ReviewFormValidator().validate(data)
    assert cleaned is None
    assert len(errors) >= 2


def test_whitebox_restaurant_validator_food_type_branch():
    from werkzeug.datastructures import ImmutableMultiDict

    cleaned, errors = RestaurantFormValidator().validate(
        ImmutableMultiDict(
            [("name", "X"), ("area", "Y"), ("service_type", "cafe")]
        )
    )
    assert cleaned is None
    assert any("food type" in e.lower() for e in errors)
