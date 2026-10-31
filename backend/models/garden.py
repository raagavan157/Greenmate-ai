from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GardenPlantCreate(BaseModel):
    plant_id: Optional[str] = None
    name: str = Field(..., min_length=2)
    scientific_name: Optional[str] = None
    category: Optional[str] = "Indoor Plants"
    nickname: Optional[str] = None
    location: Optional[str] = "Living Room"
    image_url: Optional[str] = None
    watering_interval_days: int = Field(default=5, ge=1, le=60)
    health_status: str = Field(default="Healthy")
    notes: Optional[str] = None
    sunlight: Optional[str] = "Medium Light"

class GardenPlantUpdate(BaseModel):
    nickname: Optional[str] = None
    location: Optional[str] = None
    watering_interval_days: Optional[int] = None
    health_status: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None

class GardenPlantResponse(BaseModel):
    id: str
    user_id: str
    plant_id: Optional[str] = None
    name: str
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    nickname: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    watering_interval_days: int
    health_status: str
    notes: Optional[str] = None
    sunlight: Optional[str] = None
    last_watered_at: Optional[str] = None
    next_watering_at: Optional[str] = None
    created_at: Optional[str] = None
