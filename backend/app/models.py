
from sqlalchemy import Column, Integer, String, Float, JSON

from app.database import Base


class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    address = Column(String(300), nullable=True)
    categories = Column(JSON, nullable=False, default=list)
    description = Column(String(500), nullable=True)
    price_range = Column(String(20), nullable=True)
    rating = Column(Float, nullable=True)
