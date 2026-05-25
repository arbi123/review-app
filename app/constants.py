from enum import Enum


class ServiceType(str, Enum):
    SIT_DOWN = "sit-down"
    FAST_FOOD = "fast food"
    FINE_DINING = "fine dining"
    BUFFET = "buffet"
    CAFE = "cafe"
    FOOD_TRUCK = "food truck"


class OverallRating(str, Enum):
    EXCELLENT = "excellent"
    VERY_GOOD = "very good"
    AVERAGE = "average"
    POOR = "poor"
    TERRIBLE = "terrible"


FOOD_TYPES = [
    "Asian",
    "Caribbean",
    "Oriental",
    "Italian",
    "American",
    "Traditional",
    "Other",
]

OCCASIONS = [
    "Family meal",
    "Kids meals",
    "Business lunch",
    "View/scenic",
    "Date night",
    "Celebration",
    "Casual",
]

DINING_OPTIONS = [
    "Breakfast",
    "Lunch",
    "Dinner",
    "Supper",
    "Take-out",
]

SERVICE_TYPES = [s.value for s in ServiceType]
OVERALL_RATINGS = [r.value for r in OverallRating]

SCORE_MIN = 1
SCORE_MAX = 5
