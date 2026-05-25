"""Populate the database with sample restaurants and reviews."""

import logging

from app import create_app, db
from app.images import RESTAURANT_COVERS, REVIEW_PHOTOS_SEED
from app.models import Restaurant, Review

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | seed | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("seed")

SAMPLE_RESTAURANTS = [
    {
        "name": "Spice Garden",
        "area": "Downtown Kingston",
        "description": "Modern Asian fusion with bold spices and a relaxed dining room.",
        "service_type": "sit-down",
        "food_types": ["Asian", "Oriental"],
        "occasions": ["Family meal", "Business lunch"],
        "dining_options": ["Lunch", "Dinner"],
        "allergy_info_available": True,
    },
    {
        "name": "Island Flavours",
        "area": "Downtown Kingston",
        "description": "Colourful Caribbean buffet — lively, casual, and great for groups.",
        "service_type": "buffet",
        "food_types": ["Caribbean", "Traditional"],
        "occasions": ["Family meal", "Celebration", "Casual"],
        "dining_options": ["Lunch", "Dinner", "Take-out"],
        "allergy_info_available": False,
    },
    {
        "name": "Bella Italia",
        "area": "Harbour Bay",
        "description": "Fine Italian dining with harbour views and handmade pasta.",
        "service_type": "fine dining",
        "food_types": ["Italian"],
        "occasions": ["Date night", "Business lunch", "View/scenic"],
        "dining_options": ["Dinner", "Supper"],
        "allergy_info_available": True,
    },
    {
        "name": "Main Street Diner",
        "area": "Harbour Bay",
        "description": "Classic American diner — burgers, shakes, and all-day breakfast.",
        "service_type": "fast food",
        "food_types": ["American"],
        "occasions": ["Kids meals", "Casual"],
        "dining_options": ["Breakfast", "Lunch", "Take-out"],
        "allergy_info_available": False,
    },
    {
        "name": "Sunrise Cafe",
        "area": "Old Town",
        "description": "Cosy cafe for morning coffee, pastries, and light lunches.",
        "service_type": "cafe",
        "food_types": ["American", "Traditional"],
        "occasions": ["Business lunch", "Casual"],
        "dining_options": ["Breakfast", "Lunch"],
        "allergy_info_available": True,
    },
    {
        "name": "Golden Dragon",
        "area": "Downtown Kingston",
        "description": "Classic Cantonese dishes, dim sum weekends, and quick lunch combos.",
        "service_type": "sit-down",
        "food_types": ["Asian", "Oriental"],
        "occasions": ["Family meal", "Business lunch", "Casual"],
        "dining_options": ["Lunch", "Dinner", "Take-out"],
        "allergy_info_available": True,
    },
    {
        "name": "Jerk Pit Stop",
        "area": "Old Town",
        "description": "Street-style jerk chicken, festival, and ice-cold drinks on the patio.",
        "service_type": "food truck",
        "food_types": ["Caribbean", "Traditional"],
        "occasions": ["Casual", "Celebration"],
        "dining_options": ["Lunch", "Dinner", "Take-out"],
        "allergy_info_available": False,
    },
    {
        "name": "La Mediterraneo",
        "area": "Harbour Bay",
        "description": "Shared plates, grilled seafood, and olive oil cakes by the waterfront.",
        "service_type": "sit-down",
        "food_types": ["Italian", "Oriental"],
        "occasions": ["Date night", "View/scenic", "Celebration"],
        "dining_options": ["Lunch", "Dinner", "Supper"],
        "allergy_info_available": True,
    },
    {
        "name": "BBQ Smokehouse",
        "area": "Old Town",
        "description": "Slow-smoked ribs, brisket plates, and house pickles in a rustic barn setting.",
        "service_type": "sit-down",
        "food_types": ["American", "Traditional"],
        "occasions": ["Family meal", "Casual", "Celebration"],
        "dining_options": ["Lunch", "Dinner"],
        "allergy_info_available": False,
    },
    {
        "name": "The Green Bowl",
        "area": "Downtown Kingston",
        "description": "Farm-to-table salads, grain bowls, and fresh juices with vegan options.",
        "service_type": "cafe",
        "food_types": ["Traditional", "Other"],
        "occasions": ["Business lunch", "Casual", "Kids meals"],
        "dining_options": ["Breakfast", "Lunch", "Take-out"],
        "allergy_info_available": True,
    },
]

SAMPLE_REVIEWS = [
    {
        "restaurant_name": "Spice Garden",
        "reviewer_name": "Alex M.",
        "avg_expense_per_head": 28.50,
        "food_quality": 5, "ambiance": 4, "service_quality": 4,
        "cleanliness": 5, "speed_of_service": 3, "value_for_money": 4,
        "overall_rating": "very good",
        "report": (
            "Wonderful Asian fusion with fresh ingredients and balanced heat in every dish. "
            "Staff explained allergy options clearly at the table. Service slowed slightly during "
            "the Friday rush, but the relaxed dining room and excellent flavours made the wait worthwhile."
        ),
    },
    {
        "restaurant_name": "Spice Garden",
        "reviewer_name": "Priya S.",
        "avg_expense_per_head": 32.00,
        "food_quality": 4, "ambiance": 5, "service_quality": 5,
        "cleanliness": 5, "speed_of_service": 4, "value_for_money": 4,
        "overall_rating": "excellent",
        "report": (
            "Beautiful presentation on the curry noodles and attentive service throughout the evening. "
            "The dining room feels intimate without being cramped. Ideal for a date night; we will "
            "return to try the chef's tasting menu next month."
        ),
    },
    {
        "restaurant_name": "Island Flavours",
        "reviewer_name": "Jordan K.",
        "avg_expense_per_head": 18.00,
        "food_quality": 4, "ambiance": 3, "service_quality": 3,
        "cleanliness": 4, "speed_of_service": 5, "value_for_money": 5,
        "overall_rating": "excellent",
        "report": (
            "Authentic Caribbean buffet at a price that suits family outings. Roti, stew, and "
            "grilled fish all tasted homemade. No allergy cards on tables—ask staff directly. "
            "Lively music and a casual vibe kept the mood upbeat all evening."
        ),
    },
    {
        "restaurant_name": "Island Flavours",
        "reviewer_name": "Marcus T.",
        "avg_expense_per_head": 16.50,
        "food_quality": 3, "ambiance": 4, "service_quality": 4,
        "cleanliness": 3, "speed_of_service": 4, "value_for_money": 5,
        "overall_rating": "very good",
        "report": (
            "Generous portions and friendly staff refilling drinks without being asked. The dessert "
            "station could be fresher late in service. Still one of the best-value lunches downtown "
            "when you want variety without ordering a la carte."
        ),
    },
    {
        "restaurant_name": "Bella Italia",
        "reviewer_name": "Sam T.",
        "avg_expense_per_head": 55.00,
        "food_quality": 5, "ambiance": 5, "service_quality": 5,
        "cleanliness": 5, "speed_of_service": 4, "value_for_money": 3,
        "overall_rating": "very good",
        "report": (
            "Elegant harbour views paired with handmade pasta and a wine list that impressed our table. "
            "Impeccable service and spotless linens throughout. Premium pricing, yet ideal for business "
            "lunches and milestone celebrations when presentation matters."
        ),
    },
    {
        "restaurant_name": "Bella Italia",
        "reviewer_name": "Elena R.",
        "avg_expense_per_head": 48.00,
        "food_quality": 4, "ambiance": 4, "service_quality": 4,
        "cleanliness": 5, "speed_of_service": 3, "value_for_money": 3,
        "overall_rating": "average",
        "report": (
            "Solid pasta and risotto, though we waited twenty minutes past our reservation time. "
            "Once seated, the sommelier guided us well through Italian whites. Good allergy chart "
            "provided; kitchen accommodated a nut-free request without fuss."
        ),
    },
    {
        "restaurant_name": "Main Street Diner",
        "reviewer_name": "Chris P.",
        "avg_expense_per_head": 14.00,
        "food_quality": 4, "ambiance": 3, "service_quality": 4,
        "cleanliness": 4, "speed_of_service": 5, "value_for_money": 5,
        "overall_rating": "excellent",
        "report": (
            "Best burgers in town and thick milkshakes the kids finished before the mains arrived. "
            "Fast, friendly counter service and booths that feel authentically retro. Easy on the "
            "wallet for a Saturday family brunch with refills on coffee."
        ),
    },
    {
        "restaurant_name": "Main Street Diner",
        "reviewer_name": "Dana W.",
        "avg_expense_per_head": 12.50,
        "food_quality": 3, "ambiance": 3, "service_quality": 3,
        "cleanliness": 4, "speed_of_service": 4, "value_for_money": 4,
        "overall_rating": "very good",
        "report": (
            "Reliable breakfast spot before work. Coffee refills are generous and the staff remember "
            "regular orders. Pancakes could arrive hotter on busy mornings. No formal allergy menu, "
            "but the manager listed ingredients when we asked about gluten."
        ),
    },
    {
        "restaurant_name": "Sunrise Cafe",
        "reviewer_name": "Nina L.",
        "avg_expense_per_head": 11.00,
        "food_quality": 4, "ambiance": 4, "service_quality": 4,
        "cleanliness": 5, "speed_of_service": 4, "value_for_money": 5,
        "overall_rating": "excellent",
        "report": (
            "Perfect latte art and flaky croissants in a bright corner with plug points for laptops. "
            "Quiet enough for remote work until mid-morning. Allergy information is printed on the "
            "pastry case labels, which builds trust for sensitive diners."
        ),
    },
    {
        "restaurant_name": "Sunrise Cafe",
        "reviewer_name": "Omar H.",
        "avg_expense_per_head": 9.50,
        "food_quality": 3, "ambiance": 3, "service_quality": 3,
        "cleanliness": 4, "speed_of_service": 3, "value_for_money": 4,
        "overall_rating": "average",
        "report": (
            "Sandwiches are tasty but seating fills quickly at lunch. Waited outside ten minutes "
            "for a two-top. Staff offered an allergy binder upon request, listing nuts and dairy in "
            "each filling. Fair prices for the neighbourhood cafe scene."
        ),
    },
    {
        "restaurant_name": "Golden Dragon",
        "reviewer_name": "Wei C.",
        "avg_expense_per_head": 22.00,
        "food_quality": 5, "ambiance": 3, "service_quality": 4,
        "cleanliness": 4, "speed_of_service": 5, "value_for_money": 5,
        "overall_rating": "excellent",
        "report": (
            "Dim sum on Sundays is outstanding—har gow, siu mai, and custard buns all arrive steaming. "
            "Quick lunch combos suit office workers nearby. Very fair prices for portion size and "
            "consistent quality visit after visit."
        ),
    },
    {
        "restaurant_name": "Golden Dragon",
        "reviewer_name": "Lisa F.",
        "avg_expense_per_head": 26.00,
        "food_quality": 4, "ambiance": 4, "service_quality": 3,
        "cleanliness": 4, "speed_of_service": 3, "value_for_money": 4,
        "overall_rating": "very good",
        "report": (
            "Crispy duck and hot pot were highlights of our group dinner. Noise rises when the "
            "main room fills, so book an early table. Servers know the menu well and flagged "
            "shellfish in the shared broth without prompting."
        ),
    },
    {
        "restaurant_name": "Jerk Pit Stop",
        "reviewer_name": "Andre B.",
        "avg_expense_per_head": 13.00,
        "food_quality": 5, "ambiance": 4, "service_quality": 4,
        "cleanliness": 3, "speed_of_service": 5, "value_for_money": 5,
        "overall_rating": "excellent",
        "report": (
            "Smoky jerk chicken with heat that builds slowly and festival bread that soaks up the gravy. "
            "Casual patio with cold drinks and a street-food energy. No allergy info posted—ask at "
            "the counter before ordering sides with hidden dairy."
        ),
    },
    {
        "restaurant_name": "Jerk Pit Stop",
        "reviewer_name": "Kayla J.",
        "avg_expense_per_head": 11.00,
        "food_quality": 4, "ambiance": 3, "service_quality": 3,
        "cleanliness": 3, "speed_of_service": 4, "value_for_money": 5,
        "overall_rating": "very good",
        "report": (
            "Plantains and festival are addictive alongside the half-chicken plate. Paper plates "
            "keep service fast for the lunch queue. Flavour beats presentation every time, and "
            "take-out boxes travel well for park picnics nearby."
        ),
    },
    {
        "restaurant_name": "La Mediterraneo",
        "reviewer_name": "Sophie M.",
        "avg_expense_per_head": 42.00,
        "food_quality": 5, "ambiance": 5, "service_quality": 4,
        "cleanliness": 5, "speed_of_service": 3, "value_for_money": 4,
        "overall_rating": "excellent",
        "report": (
            "Sunset views over the harbour while sharing grilled octopus and mezze boards. Olive oil "
            "cake finished the meal on a sweet note. Romantic setting with attentive but unhurried "
            "service—worth the splurge for anniversaries."
        ),
    },
    {
        "restaurant_name": "La Mediterraneo",
        "reviewer_name": "Tom G.",
        "avg_expense_per_head": 38.00,
        "food_quality": 4, "ambiance": 4, "service_quality": 3,
        "cleanliness": 4, "speed_of_service": 2, "value_for_money": 3,
        "overall_rating": "average",
        "report": (
            "Food quality stayed strong on a busy Friday, but courses arrived unevenly spaced. "
            "Wine pairings were well explained. Printed allergy chart covered seafood and nuts; "
            "kitchen adjusted a starter for our coeliac guest promptly."
        ),
    },
    {
        "restaurant_name": "BBQ Smokehouse",
        "reviewer_name": "Jake R.",
        "avg_expense_per_head": 24.00,
        "food_quality": 5, "ambiance": 4, "service_quality": 4,
        "cleanliness": 4, "speed_of_service": 4, "value_for_money": 4,
        "overall_rating": "very good",
        "report": (
            "Brisket melts off the bone and house pickles cut through the richness. Rustic barn "
            "decor suits group celebrations. Come hungry and share the rib platter with cornbread "
            "on the side—portions are built for sharing."
        ),
    },
    {
        "restaurant_name": "BBQ Smokehouse",
        "reviewer_name": "Megan S.",
        "avg_expense_per_head": 20.00,
        "food_quality": 3, "ambiance": 3, "service_quality": 3,
        "cleanliness": 3, "speed_of_service": 4, "value_for_money": 4,
        "overall_rating": "average",
        "report": (
            "Main proteins impressed more than the side dishes, which tasted under-seasoned. Still "
            "a fun group spot with long communal tables. No allergy guidance available; staff guessed "
            "ingredients for sauces when we asked about mustard."
        ),
    },
    {
        "restaurant_name": "The Green Bowl",
        "reviewer_name": "Hannah K.",
        "avg_expense_per_head": 15.00,
        "food_quality": 4, "ambiance": 4, "service_quality": 5,
        "cleanliness": 5, "speed_of_service": 4, "value_for_money": 4,
        "overall_rating": "very good",
        "report": (
            "Fresh grain bowls with labelled allergens on the menu board. Vegan options taste vibrant, "
            "not afterthoughts. Counter staff answered questions about nuts and soy patiently. "
            "Juice bar blends are a refreshing add-on after lunch."
        ),
    },
    {
        "restaurant_name": "The Green Bowl",
        "reviewer_name": "Ryan D.",
        "avg_expense_per_head": 13.50,
        "food_quality": 3, "ambiance": 3, "service_quality": 4,
        "cleanliness": 5, "speed_of_service": 5, "value_for_money": 5,
        "overall_rating": "very good",
        "report": (
            "Quick healthy lunch with crisp greens and proteins that do not swim in dressing. "
            "Portions are modest yet fairly priced. Ideal takeaway for office workers; online "
            "ordering queue moved fast at peak hour today."
        ),
    },
]


def seed():
    app = create_app()
    with app.app_context():
        log.info("Resetting database and loading sample data...")
        db.drop_all()
        db.create_all()

        name_to_id = {}
        for data in SAMPLE_RESTAURANTS:
            restaurant = Restaurant(
                name=data["name"],
                area=data["area"],
                description=data.get("description"),
                service_type=data["service_type"],
                allergy_info_available=data["allergy_info_available"],
                cover_image=RESTAURANT_COVERS.get(data["name"]),
            )
            restaurant.set_food_types(data["food_types"])
            restaurant.set_occasions(data["occasions"])
            restaurant.set_dining_options(data["dining_options"])
            db.session.add(restaurant)
            db.session.flush()
            name_to_id[data["name"]] = restaurant.id
            log.info(
                "Restaurant: %s | %s | %s | cuisines=%s",
                data["name"],
                data["area"],
                data["service_type"],
                ", ".join(data["food_types"]),
            )

        if len(SAMPLE_REVIEWS) != len(REVIEW_PHOTOS_SEED):
            raise ValueError(
                f"Need {len(SAMPLE_REVIEWS)} unique review photos, "
                f"got {len(REVIEW_PHOTOS_SEED)}"
            )

        for idx, data in enumerate(SAMPLE_REVIEWS):
            photo = REVIEW_PHOTOS_SEED[idx]
            review = Review(
                restaurant_id=name_to_id[data["restaurant_name"]],
                reviewer_name=data["reviewer_name"],
                avg_expense_per_head=data["avg_expense_per_head"],
                food_quality=data["food_quality"],
                ambiance=data["ambiance"],
                service_quality=data["service_quality"],
                cleanliness=data["cleanliness"],
                speed_of_service=data["speed_of_service"],
                value_for_money=data["value_for_money"],
                overall_rating=data["overall_rating"],
                report=data["report"],
                photo=photo,
            )
            db.session.add(review)
            log.info(
                "Review #%d: %s by %s | %s | $%.2f | photo slot %d",
                idx + 1,
                data["restaurant_name"],
                data["reviewer_name"],
                data["overall_rating"],
                data["avg_expense_per_head"],
                idx + 1,
            )

        db.session.commit()
        log.info(
            "Done — %d restaurants, %d reviews, %d unique review photos.",
            len(SAMPLE_RESTAURANTS),
            len(SAMPLE_REVIEWS),
            len(set(REVIEW_PHOTOS_SEED)),
        )


if __name__ == "__main__":
    seed()
