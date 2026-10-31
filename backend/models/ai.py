from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PlantIdentifyResponse(BaseModel):
    common_name: str
    scientific_name: str
    confidence: float
    category: str
    description: str
    sunlight: str
    watering: str
    soil_type: str
    temperature_range: str
    care_instructions: List[str]
    image_url: Optional[str] = None
    ai_source: str
    notice: Optional[str] = None

class DiseaseDiagnoseResponse(BaseModel):
    plant_name: Optional[str] = "Plant Specimen"
    disease_name: str
    confidence: float
    symptoms: List[str]
    causes: List[str]
    severity: str
    treatment: List[str]
    prevention: List[str]
    disclaimer: str = "This preliminary AI analysis is for educational and screening purposes and does not replace lab pathology."
    image_url: Optional[str] = None
    ai_source: str
    notice: Optional[str] = None

class CarePlanRequest(BaseModel):
    plant_species: str
    environment: str = "indoor"
    sunlight: str = "Medium Light"
    temperature: Optional[str] = "22°C - 26°C"
    watering_preference: Optional[str] = "Moderate"
    growth_stage: Optional[str] = "Mature"

class CarePlanResponse(BaseModel):
    plant_species: str
    environment: str
    daily_care: List[str]
    weekly_watering: Dict[str, Any]
    monthly_fertilizer: Dict[str, Any]
    seasonal_recommendations: Dict[str, str]
    custom_tips: List[str]
    ai_source: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    plant_context: Optional[str] = None
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str
    suggested_followups: Optional[List[str]] = []
    ai_source: str
