
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CafeResponse(BaseModel):
    id: int
    name: str
    city: str
    address: Optional[str] = None
    categories: list[str] = Field(default_factory=list)
    description: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class CafeListResponse(BaseModel):
    total: int
    cafes: list[CafeResponse]


class CityListResponse(BaseModel):
    cities: list[str]


class CategoryListResponse(BaseModel):
    categories: list[str]
