
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cafe
from app.schemas import (
    CafeResponse,
    CafeListResponse,
    CityListResponse,
    CategoryListResponse,
)

app = FastAPI(
    title="Matcha Maps API",
    description="Discover aesthetic cafes across India.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def cafe_to_dict(cafe: Cafe):
    return {
        "id": cafe.id,
        "name": cafe.name,
        "city": cafe.city,
        "address": cafe.address,
        "categories": cafe.categories or [],
        "description": cafe.description or "",
        "price_range": cafe.price_range,
        "rating": cafe.rating,
    }


@app.get("/")
def home():
    return {
        "message": "Welcome to Matcha Maps API!",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/cafes", response_model=CafeListResponse)
def get_cafes(
    search: str | None = Query(default=None, min_length=1),
    city: str | None = None,
    category: str | None = None,
    sort_by: str = Query(default="name", pattern="^(name|city)$"),
    db: Session = Depends(get_db),
):
    results = [
        cafe_to_dict(cafe)
        for cafe in db.query(Cafe).all()
    ]

    if search:
        keyword = search.strip().casefold()
        results = [
            cafe for cafe in results
            if keyword in cafe["name"].casefold()
            or keyword in cafe["city"].casefold()
            or keyword in cafe["description"].casefold()
            or any(
                keyword in tag.casefold()
                for tag in cafe["categories"]
            )
        ]

    if city:
        results = [
            cafe for cafe in results
            if cafe["city"].casefold() == city.strip().casefold()
        ]

    if category:
        results = [
            cafe for cafe in results
            if category.strip().casefold()
            in [tag.casefold() for tag in cafe["categories"]]
        ]

    results.sort(
        key=lambda cafe: (cafe[sort_by] or "").casefold()
    )

    return {
        "total": len(results),
        "cafes": results,
    }


@app.get("/api/cafes/{cafe_id}", response_model=CafeResponse)
def get_cafe(
    cafe_id: int,
    db: Session = Depends(get_db),
):
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id).first()

    if cafe is None:
        raise HTTPException(
            status_code=404,
            detail="Cafe not found",
        )

    return cafe_to_dict(cafe)


@app.get("/api/cities", response_model=CityListResponse)
def get_cities(db: Session = Depends(get_db)):
    cities = {
        city
        for (city,) in db.query(Cafe.city).distinct().all()
        if city
    }

    return {"cities": sorted(cities)}


@app.get("/api/categories", response_model=CategoryListResponse)
def get_categories(db: Session = Depends(get_db)):
    categories = {
        category
        for (category_list,) in db.query(Cafe.categories).all()
        for category in (category_list or [])
    }

    return {"categories": sorted(categories)}
