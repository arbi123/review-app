import logging

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import func
from werkzeug.datastructures import ImmutableMultiDict

from app import db
from app.constants import (
    DINING_OPTIONS,
    FOOD_TYPES,
    OCCASIONS,
    OVERALL_RATINGS,
    SERVICE_TYPES,
)
from app.helpers import restaurant_average_expense, restaurant_average_score
from app.models import Restaurant, Review
from app.uploads import save_upload, validate_image_upload
from app.validation import validate_review, validate_restaurant

bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


def _enrich_restaurants(restaurants):
    for r in restaurants:
        r._avg_score = restaurant_average_score(r)
        r._avg_expense = restaurant_average_expense(r)
    return restaurants


@bp.route("/")
def index():
    area = request.args.get("area", "").strip()
    q = request.args.get("q", "").strip()
    food_type = request.args.get("food_type", "").strip()
    sort = request.args.get("sort", "name")

    query = Restaurant.query

    if area:
        query = query.filter(Restaurant.area == area)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Restaurant.name.ilike(like),
                Restaurant.area.ilike(like),
                Restaurant.description.ilike(like),
            )
        )
    if food_type:
        query = query.filter(Restaurant.food_types.contains(f'"{food_type}"'))

    restaurants = query.all()
    restaurants = _enrich_restaurants(restaurants)

    if sort == "rating":
        restaurants.sort(key=lambda r: r._avg_score or 0, reverse=True)
    elif sort == "reviews":
        restaurants.sort(key=lambda r: r.review_count, reverse=True)
    else:
        restaurants.sort(key=lambda r: r.name.lower())

    areas = [
        row[0]
        for row in db.session.query(Restaurant.area).distinct().order_by(Restaurant.area)
    ]
    total_reviews = db.session.query(func.count(Review.id)).scalar() or 0

    filters = []
    if q:
        filters.append(f"search='{q}'")
    if area:
        filters.append(f"area='{area}'")
    if food_type:
        filters.append(f"cuisine='{food_type}'")
    filter_text = ", ".join(filters) if filters else "no filters"

    logger.info(
        "Browse home: %d restaurants shown (sort=%s, %s). "
        "Database totals: %d restaurants, %d reviews.",
        len(restaurants),
        sort,
        filter_text,
        Restaurant.query.count(),
        total_reviews,
    )

    return render_template(
        "index.html",
        restaurants=restaurants,
        areas=areas,
        food_types=FOOD_TYPES,
        selected_area=area,
        search_query=q,
        selected_food=food_type,
        selected_sort=sort,
        total_reviews=total_reviews,
    )


@bp.route("/restaurants/<int:restaurant_id>")
def restaurant_detail(restaurant_id):
    restaurant = db.get_or_404(Restaurant, restaurant_id)
    reviews = (
        Review.query.filter_by(restaurant_id=restaurant_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    avg_score = restaurant_average_score(restaurant)
    avg_expense = restaurant_average_expense(restaurant)

    logger.info(
        "Viewing '%s' (id=%d, area=%s, service=%s): %d reviews, "
        "avg score=%s, avg expense=%s, allergy info=%s.",
        restaurant.name,
        restaurant.id,
        restaurant.area,
        restaurant.service_type,
        len(reviews),
        f"{avg_score:.1f}" if avg_score else "n/a",
        f"${avg_expense:.2f}" if avg_expense else "n/a",
        "yes" if restaurant.allergy_info_available else "no",
    )

    return render_template(
        "restaurant.html",
        restaurant=restaurant,
        reviews=reviews,
        avg_score=avg_score,
        avg_expense=avg_expense,
    )


@bp.route("/restaurants/<int:restaurant_id>/review", methods=["GET", "POST"])
def add_review(restaurant_id):
    restaurant = db.get_or_404(Restaurant, restaurant_id)
    if request.method == "POST":
        cleaned, errors = validate_review(request.form)
        img_err = validate_image_upload(request.files.get("photo"))
        if img_err:
            errors.append(img_err)
        if errors:
            logger.warning(
                "Review rejected for '%s' (id=%d): %s",
                restaurant.name,
                restaurant_id,
                "; ".join(errors),
            )
            for err in errors:
                flash(err, "danger")
            return render_template(
                "review_form.html",
                restaurant=restaurant,
                form=request.form,
                overall_ratings=OVERALL_RATINGS,
            )
        photo_path = save_upload(request.files.get("photo"), "reviews")
        review = Review(
            restaurant_id=restaurant_id,
            photo=photo_path,
            **cleaned,
        )
        db.session.add(review)
        db.session.commit()
        logger.info(
            "New review saved for '%s' by %s: overall=%s, expense=$%.2f, "
            "photo=%s, report length=%d words.",
            restaurant.name,
            cleaned.get("reviewer_name") or "Anonymous",
            cleaned["overall_rating"],
            cleaned["avg_expense_per_head"],
            "uploaded" if photo_path else "none",
            len(cleaned["report"].split()),
        )
        flash("Review submitted successfully.", "success")
        return redirect(url_for("main.restaurant_detail", restaurant_id=restaurant_id))

    logger.info("Review form opened for '%s' (id=%d).", restaurant.name, restaurant_id)
    return render_template(
        "review_form.html",
        restaurant=restaurant,
        form={},
        overall_ratings=OVERALL_RATINGS,
    )


@bp.route("/restaurants/new", methods=["GET", "POST"])
def add_restaurant():
    if request.method == "POST":
        cleaned, errors = validate_restaurant(request.form)
        img_err = validate_image_upload(request.files.get("cover_image"))
        if img_err:
            errors.append(img_err)
        if errors:
            logger.warning("Restaurant add rejected: %s", "; ".join(errors))
            for err in errors:
                flash(err, "danger")
            return render_template(
                "restaurant_form.html",
                form=request.form,
                food_types=FOOD_TYPES,
                occasions=OCCASIONS,
                dining_options=DINING_OPTIONS,
                service_types=SERVICE_TYPES,
            )
        cover_path = save_upload(request.files.get("cover_image"), "restaurants")
        restaurant = Restaurant(
            name=cleaned["name"],
            area=cleaned["area"],
            description=cleaned["description"],
            service_type=cleaned["service_type"],
            allergy_info_available=cleaned["allergy_info_available"],
            cover_image=cover_path,
        )
        restaurant.set_food_types(cleaned["food_types"])
        restaurant.set_occasions(cleaned["occasions"])
        restaurant.set_dining_options(cleaned["dining_options"])
        db.session.add(restaurant)
        db.session.commit()
        logger.info(
            "New restaurant added: '%s' in %s (%s). Cuisines: %s. Cover image: %s.",
            cleaned["name"],
            cleaned["area"],
            cleaned["service_type"],
            ", ".join(cleaned["food_types"]),
            "uploaded" if cover_path else "default",
        )
        flash("Restaurant added successfully.", "success")
        return redirect(url_for("main.restaurant_detail", restaurant_id=restaurant.id))

    logger.info("Add-restaurant form opened.")
    return render_template(
        "restaurant_form.html",
        form=ImmutableMultiDict(),
        food_types=FOOD_TYPES,
        occasions=OCCASIONS,
        dining_options=DINING_OPTIONS,
        service_types=SERVICE_TYPES,
    )
