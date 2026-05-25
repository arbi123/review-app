"""Verified public image URLs (tested HTTP 200)."""

DEFAULT_RESTAURANT_IMAGE = (
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
    "?w=900&q=80&auto=format&fit=crop"
)

RESTAURANT_COVERS = {
    "Spice Garden": (
        "https://images.pexels.com/photos/357756/pexels-photo-357756.jpeg"
        "?auto=compress&cs=tinysrgb&w=900&h=600&fit=crop"
    ),
    "Island Flavours": (
        "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg"
        "?auto=compress&cs=tinysrgb&w=900&h=600&fit=crop"
    ),
    "Bella Italia": (
        "https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg"
        "?auto=compress&cs=tinysrgb&w=900&h=600&fit=crop"
    ),
    "Main Street Diner": (
        "https://images.unsplash.com/photo-1550547660-d9450f859349"
        "?w=900&q=80&auto=format&fit=crop"
    ),
    "Sunrise Cafe": (
        "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg"
        "?auto=compress&cs=tinysrgb&w=900&h=600&fit=crop"
    ),
    "Golden Dragon": (
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
        "?w=900&q=80&auto=format&fit=crop"
    ),
    "Jerk Pit Stop": (
        "https://images.pexels.com/photos/70497/pexels-photo-70497.jpeg"
        "?auto=compress&cs=tinysrgb&w=900&h=600&fit=crop"
    ),
    "La Mediterraneo": (
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5"
        "?w=900&q=80&auto=format&fit=crop"
    ),
    "BBQ Smokehouse": (
        "https://images.unsplash.com/photo-1544025162-d76694265947"
        "?w=900&q=80&auto=format&fit=crop"
    ),
    "The Green Bowl": (
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe"
        "?w=900&q=80&auto=format&fit=crop"
    ),
}

FOOD_TYPE_IMAGES = {
    "Asian": RESTAURANT_COVERS["Golden Dragon"],
    "Oriental": RESTAURANT_COVERS["Spice Garden"],
    "Caribbean": RESTAURANT_COVERS["Island Flavours"],
    "Italian": RESTAURANT_COVERS["Bella Italia"],
    "American": RESTAURANT_COVERS["Main Street Diner"],
    "Traditional": (
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
        "?w=900&q=80&auto=format&fit=crop"
    ),
    "Other": DEFAULT_RESTAURANT_IMAGE,
}

# One unique photo per seeded review (20 total — no duplicates)
REVIEW_PHOTOS_SEED = [
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80&auto=format&fit=crop",
    "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80&auto=format&fit=crop",
    "https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80&auto=format&fit=crop",
    "https://images.pexels.com/photos/2097090/pexels-photo-2097090.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/2135/pexels-photo-2135.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/2664215/pexels-photo-2664215.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/70497/pexels-photo-70497.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.pexels.com/photos/691114/pexels-photo-691114.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80&auto=format&fit=crop",
    "https://images.pexels.com/photos/725991/pexels-photo-725991.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
    "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&q=80&auto=format&fit=crop",
    "https://images.pexels.com/photos/5938/pexels-photo-5938.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop",
]
