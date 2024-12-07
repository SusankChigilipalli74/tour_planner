from pydantic import BaseModel
from typing import List, Optional

class UserPreferences(BaseModel):
    interests: List[str]
    budget: float
    preferred_transportation: Optional[str]
    dietary_restrictions: Optional[List[str]]
    walking_preference: Optional[str]

class User(BaseModel):
    username: str
    email: str
    preferences: Optional[UserPreferences]

class Place(BaseModel):
    name: str
    category: str
    city: str
    price_range: str
    duration: int
    rating: float