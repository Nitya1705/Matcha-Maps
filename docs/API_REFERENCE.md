
# Matcha Maps - Backend API Reference

## 1. Project Overview

Matcha Maps is a café discovery platform that helps users discover cafés across India based on location, categories, and preferences.

The backend is developed using:
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## 2. Base URL

Local development:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## 3. Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API welcome message |
| GET | /health | Check API health |
| GET | /api/cafes | Retrieve and filter cafés |
| GET | /api/cafes/{cafe_id} | Retrieve one café |
| GET | /api/cities | Retrieve available cities |
| GET | /api/categories | Retrieve available categories |

## 4. Café Listing

### GET /api/cafes

Returns all cafés or filtered café results.

Query parameters:

| Parameter | Type | Description |
|---|---|---|
| search | string | Search café name, city, description, or category |
| city | string | Filter by city |
| category | string | Filter by category |
| sort_by | string | Sort by name or city |

Example:

/api/cafes?city=Delhi

Response:

{
  "total": 2,
  "cafes": [
    {
      "id": 1,
      "name": "The Matcha Room",
      "city": "Delhi",
      "address": "Demo address, Delhi",
      "categories": ["matcha", "study-friendly"],
      "description": "A calm corner for matcha lovers.",
      "price_range": "₹₹",
      "rating": null
    }
  ]
}

## 5. Individual Café

### GET /api/cafes/{cafe_id}

Returns details of a specific café.

Example:

/api/cafes/1

Possible error:

404 Not Found

{
  "detail": "Cafe not found"
}

## 6. Cities

### GET /api/cities

Returns all unique cities available in the database.

Example response:

{
  "cities": ["Bengaluru", "Delhi", "Mumbai"]
}

## 7. Categories

### GET /api/categories

Returns all unique café categories.

Example response:

{
  "categories": [
    "bakery",
    "coffee",
    "date night",
    "matcha",
    "study-friendly"
  ]
}

## 8. Health Check

### GET /health

Checks whether the backend is running.

Response:

{
  "status": "healthy"
}

## 9. Status Codes

| Code | Meaning |
|---|---|
| 200 | Successful request |
| 404 | Café not found |
| 422 | Request validation error |
| 500 | Internal server error |

## 10. Running the Backend

Open PowerShell and navigate to the backend directory:

cd backend

Install dependencies:

pip install -r requirements.txt

Start the development server:

python -m uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

## 11. Frontend Integration

The React frontend can communicate with the backend using HTTP requests.

Base API URL:

http://127.0.0.1:8000

Example JavaScript request:

fetch("http://127.0.0.1:8000/api/cafes")
  .then(response => response.json())
  .then(data => console.log(data));

Note:
The backend currently contains sample café records.
