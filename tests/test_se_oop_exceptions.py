"""
SE — Intermediate testing for OOP (interface/inheritance) and custom exceptions.
"""

import pytest

from app.exceptions import TasteMapError, UploadError, ValidationError
from app.uploads import validate_image_upload
from app.validators_oop import (
    BaseFormValidator,
    RestaurantFormValidator,
    ReviewFormValidator,
    Validatable,
)


def test_oop_interface_contract():
    assert issubclass(RestaurantFormValidator, Validatable)
    assert issubclass(ReviewFormValidator, Validatable)
    assert issubclass(RestaurantFormValidator, BaseFormValidator)


def test_oop_restaurant_validator_success():
    cleaned, errors = RestaurantFormValidator().validate(
        {
            "name": "OOP Bistro",
            "area": "Code City",
            "service_type": "sit-down",
            "food_types": ["Italian"],
            "occasions": ["Casual"],
            "dining_options": ["Lunch"],
        }
    )
    assert errors == []
    assert cleaned["name"] == "OOP Bistro"


def test_exception_hierarchy():
    err = ValidationError("bad", field="name")
    assert isinstance(err, TasteMapError)
    assert err.field == "name"


def test_upload_exception_on_bad_extension():
    class FakeFile:
        filename = "menu.pdf"

    with pytest.raises(UploadError):
        validate_image_upload(FakeFile())
