
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_all_cafes():
    response = client.get("/api/cafes")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "cafes" in data
    assert data["total"] == len(data["cafes"])


def test_filter_cafes_by_city():
    response = client.get("/api/cafes?city=Delhi")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2

    for cafe in data["cafes"]:
        assert cafe["city"] == "Delhi"


def test_filter_cafes_by_category():
    response = client.get("/api/cafes?category=matcha")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2


def test_search_cafes():
    response = client.get("/api/cafes?search=coffee")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["cafes"][0]["name"] == "Little Leaf Coffee"


def test_sort_cafes_by_city():
    response = client.get("/api/cafes?sort_by=city")

    assert response.status_code == 200

    cafes = response.json()["cafes"]
    cities = [cafe["city"] for cafe in cafes]

    assert cities == sorted(cities, key=str.casefold)


def test_get_single_cafe():
    response = client.get("/api/cafes/1")

    assert response.status_code == 200
    assert response.json()["name"] == "The Matcha Room"


def test_cafe_not_found():
    response = client.get("/api/cafes/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Cafe not found"


def test_get_cities():
    response = client.get("/api/cities")

    assert response.status_code == 200
    assert response.json()["cities"] == [
        "Bengaluru",
        "Delhi",
        "Mumbai",
    ]


def test_get_categories():
    response = client.get("/api/categories")

    assert response.status_code == 200

    categories = response.json()["categories"]

    assert "matcha" in categories
    assert "coffee" in categories


def test_invalid_sort_parameter():
    response = client.get("/api/cafes?sort_by=rating")

    assert response.status_code == 422
