# app/models.py

from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    price: str
    availability: str
    rating: str
    disponibility: str
    category: str
    image: str
