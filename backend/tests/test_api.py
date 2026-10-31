
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Cafe


# Create a separate temporary SQLite database.
@pytest.fixture
def client():

    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    # Create temporary database tables.
    Base.metadata.create_all(bind=test_engine)

    # Override the application's database dependency.
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Insert temporary test cafés.
    db = TestingSessionLocal()

    try:
        test_cafes = [
            Cafe(
                id=1,
                name="The Matcha Room",
                city="Delhi",
                address="Test address, Delhi",
                categories=["matcha", "study-friendly"],
                description="A calm corner for matcha lovers.",
                price_range="₹₹",
                rating=4.5,
            ),
            Cafe(
                id=2,
                name="Bloom Cafe",
                city="Mumbai",
                address="Test address, Mumbai",
                categories=["bakery", "date night"],
                description="A beautiful bakery cafe.",
                price_range="₹₹",
                rating=4.2,
            ),
            Cafe(
                id=3,
                name="Little Leaf Coffee",
                city="Bengaluru",
                address="Test address, Bengaluru",
                categories=["study-friendly", "coffee"],
                description="A peaceful place to enjoy coffee.",
                price_range="₹",
                rating=4.3,
            ),
            Cafe(
                id=4,
                name="Sakura Matcha",
                city="Delhi",
                address="Test address, Delhi",
                categories=["matcha", "date night"],
                description="Japanese-inspired matcha cafe.",
                price_range="₹₹₹",
                rating=4.7,
            ),
        ]

        db.add_all(test_cafes)
        db.commit()

    finally:
        db.close()

    # Provide a test client.
    with TestClient(app) as test_client:
        yield test_client

    # Clean up after each test.
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_all_cafes(client):
    response = client.get("/api/cafes")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 4
    assert len(data["cafes"]) == 4


def test_filter_cafes_by_city(client):
    response = client.get("/api/cafes?city=Delhi")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2

    for cafe in data["cafes"]:
        assert cafe["city"] == "Delhi"


def test_filter_cafes_by_category(client):
    response = client.get("/api/cafes?category=matcha")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2


def test_search_cafes(client):
    response = client.get("/api/cafes?search=coffee")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["cafes"][0]["name"] == "Little Leaf Coffee"


def test_sort_cafes_by_city(client):
    response = client.get("/api/cafes?sort_by=city")

    assert response.status_code == 200

    cafes = response.json()["cafes"]
    cities = [cafe["city"] for cafe in cafes]

    assert cities == sorted(cities, key=str.casefold)


def test_get_single_cafe(client):
    response = client.get("/api/cafes/1")

    assert response.status_code == 200
    assert response.json()["name"] == "The Matcha Room"


def test_cafe_not_found(client):
    response = client.get("/api/cafes/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Cafe not found"


def test_get_cities(client):
    response = client.get("/api/cities")

    assert response.status_code == 200
    assert response.json()["cities"] == [
        "Bengaluru",
        "Delhi",
        "Mumbai",
    ]


def test_get_categories(client):
    response = client.get("/api/categories")

    assert response.status_code == 200

    categories = response.json()["categories"]

    assert "matcha" in categories
    assert "coffee" in categories


def test_invalid_sort_parameter(client):
    response = client.get("/api/cafes?sort_by=rating")

    assert response.status_code == 422
