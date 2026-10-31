import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from models.garden import GardenPlantCreate, GardenPlantUpdate, GardenPlantResponse
from utils.auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/garden", tags=["Smart Garden"])

def format_garden_plant(doc: dict) -> dict:
    # Compute next watering date if last_watered_at exists
    last_watered = doc.get("last_watered_at")
    interval = doc.get("watering_interval_days", 5)
    next_watered = None
    if last_watered:
        try:
            dt = datetime.fromisoformat(last_watered)
            next_watered = (dt + timedelta(days=interval)).isoformat()
        except Exception:
            next_watered = None

    return {
        "id": str(doc.get("_id")),
        "user_id": str(doc.get("user_id")),
        "plant_id": doc.get("plant_id"),
        "name": doc.get("name"),
        "scientific_name": doc.get("scientific_name"),
        "category": doc.get("category", "Indoor Plants"),
        "nickname": doc.get("nickname"),
        "location": doc.get("location", "Living Room"),
        "image_url": doc.get("image_url"),
        "watering_interval_days": interval,
        "health_status": doc.get("health_status", "Healthy"),
        "notes": doc.get("notes"),
        "sunlight": doc.get("sunlight"),
        "last_watered_at": last_watered,
        "next_watering_at": next_watered or doc.get("next_watering_at"),
        "created_at": doc.get("created_at")
    }

@router.get("", response_model=List[GardenPlantResponse])
def get_user_garden(user: dict = Depends(get_current_user)):
    db = get_db()
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])
    docs = garden_col.find({"user_id": user_id})
    return [format_garden_plant(d) for d in docs]

@router.post("", response_model=GardenPlantResponse, status_code=status.HTTP_201_CREATED)
def add_to_garden(item_in: GardenPlantCreate, user: dict = Depends(get_current_user)):
    db = get_db()
    garden_col = db.get_collection("user_gardens")
    plants_col = db.get_collection("plants")
    
    plant_data = item_in.dict()
    # If plant_id is provided, merge catalog plant info if missing
    if item_in.plant_id:
        catalog_plant = plants_col.find_one({"_id": item_in.plant_id})
        if catalog_plant:
            if not plant_data.get("image_url"):
                plant_data["image_url"] = catalog_plant.get("image_url")
            if not plant_data.get("scientific_name"):
                plant_data["scientific_name"] = catalog_plant.get("scientific_name")
            if not plant_data.get("category"):
                plant_data["category"] = catalog_plant.get("category")
            if not plant_data.get("sunlight"):
                plant_data["sunlight"] = catalog_plant.get("sunlight")

    item_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat()
    plant_data["_id"] = item_id
    plant_data["user_id"] = str(user["_id"])
    plant_data["last_watered_at"] = now_iso
    plant_data["next_watering_at"] = (datetime.utcnow() + timedelta(days=item_in.watering_interval_days)).isoformat()
    plant_data["created_at"] = now_iso
    plant_data["updated_at"] = now_iso

    garden_col.insert_one(plant_data)

    # Automatically initialize a care schedule
    care_col = db.get_collection("care_schedules")
    care_doc = {
        "_id": str(uuid.uuid4()),
        "user_id": str(user["_id"]),
        "garden_plant_id": item_id,
        "plant_name": plant_data["name"],
        "plant_image": plant_data.get("image_url"),
        "watering_interval_days": item_in.watering_interval_days,
        "reminder_time": "09:00",
        "notifications_enabled": True,
        "last_watered_at": now_iso,
        "created_at": now_iso
    }
    care_col.insert_one(care_doc)

    return format_garden_plant(plant_data)

@router.put("/{plant_id}", response_model=GardenPlantResponse)
def update_garden_plant(plant_id: str, item_in: GardenPlantUpdate, user: dict = Depends(get_current_user)):
    db = get_db()
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])
    
    existing = garden_col.find_one({"_id": plant_id, "user_id": user_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Garden plant not found")

    update_fields = {k: v for k, v in item_in.dict(exclude_unset=True).items() if v is not None}
    update_fields["updated_at"] = datetime.utcnow().isoformat()
    
    garden_col.update_one({"_id": plant_id, "user_id": user_id}, {"$set": update_fields})
    updated = garden_col.find_one({"_id": plant_id, "user_id": user_id})
    return format_garden_plant(updated)

@router.delete("/{plant_id}")
def remove_from_garden(plant_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])
    
    res = garden_col.delete_one({"_id": plant_id, "user_id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Garden plant not found")

    # Clean up associated schedules and records
    db.get_collection("care_schedules").delete_one({"garden_plant_id": plant_id, "user_id": user_id})
    return {"message": "Plant removed from garden", "id": plant_id}
