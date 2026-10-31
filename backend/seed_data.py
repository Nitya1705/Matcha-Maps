
from app.database import SessionLocal
from app.models import Cafe


sample_cafes = [
    {
        "name": "The Matcha Room",
        "city": "Delhi",
        "address": "Demo address, Delhi",
        "categories": ["matcha", "study-friendly"],
        "description": "A calm corner for matcha lovers.",
        "price_range": "₹₹",
        "rating": None,
    },
    {
        "name": "Bloom Cafe",
        "city": "Mumbai",
        "address": "Demo address, Mumbai",
        "categories": ["bakery", "date night"],
        "description": "A cozy cafe with pretty desserts.",
        "price_range": "₹₹",
        "rating": None,
    },
    {
        "name": "Little Leaf Coffee",
        "city": "Bengaluru",
        "address": "Demo address, Bengaluru",
        "categories": ["study-friendly", "coffee"],
        "description": "A peaceful spot to work and unwind.",
        "price_range": "₹",
        "rating": None,
    },
    {
        "name": "Sakura Matcha",
        "city": "Delhi",
        "address": "Demo address, Delhi",
        "categories": ["matcha", "date night"],
        "description": "A sample listing for matcha enthusiasts.",
        "price_range": "₹₹₹",
        "rating": None,
    },
]


def seed_database():
    db = SessionLocal()

    try:
        existing_count = db.query(Cafe).count()

        if existing_count > 0:
            print(
                f"Database already contains {existing_count} cafes."
            )
            print("No data was inserted. Avoiding duplicates.")
            return

        cafes = [
            Cafe(**cafe_data)
            for cafe_data in sample_cafes
        ]

        db.add_all(cafes)
        db.commit()

        print(f"Successfully inserted {len(cafes)} sample cafes!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
