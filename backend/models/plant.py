from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PlantBase(BaseModel):
    name: str = Field(..., min_length=2)
    scientific_name: str
    category: str
    difficulty: str = "Easy"
    sunlight: str
    watering: str
    watering_interval_days: int = 4
    price: Optional[float] = 399.0
    rating: Optional[float] = 4.8
    reviews_count: Optional[int] = 0
    image_url: str
    description: str
    soil_type: Optional[str] = None
    temperature_range: Optional[str] = None
    humidity: Optional[str] = None
    care_instructions: Optional[List[str]] = []

class PlantCreate(PlantBase):
    pass

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    sunlight: Optional[str] = None
    watering: Optional[str] = None
    watering_interval_days: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    soil_type: Optional[str] = None
    temperature_range: Optional[str] = None
    humidity: Optional[str] = None
    care_instructions: Optional[List[str]] = None

class PlantResponse(PlantBase):
    id: str
    created_at: Optional[str] = None
    is_wishlisted: Optional[bool] = False
