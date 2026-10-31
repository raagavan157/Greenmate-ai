from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CareScheduleCreate(BaseModel):
    garden_plant_id: str
    watering_interval_days: int = Field(..., ge=1, le=60)
    reminder_time: Optional[str] = "09:00"
    notifications_enabled: bool = True

class CareScheduleResponse(BaseModel):
    id: str
    user_id: str
    garden_plant_id: str
    plant_name: Optional[str] = None
    plant_image: Optional[str] = None
    watering_interval_days: int
    reminder_time: str
    notifications_enabled: bool
    last_watered_at: Optional[str] = None
    next_watering_at: Optional[str] = None
    is_overdue: bool = False

class WateringLogCreate(BaseModel):
    garden_plant_id: str
    notes: Optional[str] = None
    amount_ml: Optional[int] = 250

class WateringLogResponse(BaseModel):
    id: str
    user_id: str
    garden_plant_id: str
    plant_name: Optional[str] = None
    watered_at: str
    notes: Optional[str] = None
    amount_ml: Optional[int] = 250

class GrowthRecordCreate(BaseModel):
    garden_plant_id: str
    height_cm: Optional[float] = None
    new_leaves_count: Optional[int] = None
    health_notes: Optional[str] = None
    photo_url: Optional[str] = None

class GrowthRecordResponse(BaseModel):
    id: str
    user_id: str
    garden_plant_id: str
    plant_name: Optional[str] = None
    height_cm: Optional[float] = None
    new_leaves_count: Optional[int] = None
    health_notes: Optional[str] = None
    photo_url: Optional[str] = None
    recorded_at: str
