"""Update image URLs in an existing database without wiping reviews."""

from app import create_app, db
from app.images import RESTAURANT_COVERS, REVIEW_PHOTOS
from app.models import Restaurant, Review


def update_images():
    app = create_app()
    with app.app_context():
        for restaurant in Restaurant.query.all():
            url = RESTAURANT_COVERS.get(restaurant.name)
            if url:
                restaurant.cover_image = url

        for review in Review.query.all():
            if review.restaurant:
                url = REVIEW_PHOTOS.get(review.restaurant.name)
                if url:
                    review.photo = url

        db.session.commit()
        print("Updated restaurant and review image URLs.")


if __name__ == "__main__":
    update_images()
