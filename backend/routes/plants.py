import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status, Depends
from models.plant import PlantCreate, PlantUpdate, PlantResponse
from database import get_db
from utils.auth import get_current_user_optional, get_current_user

router = APIRouter(prefix="/api/plants", tags=["Plants"])

def format_plant(doc: dict, is_wishlisted: bool = False) -> dict:
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "scientific_name": doc.get("scientific_name"),
        "category": doc.get("category"),
        "difficulty": doc.get("difficulty", "Easy"),
        "sunlight": doc.get("sunlight"),
        "watering": doc.get("watering"),
        "watering_interval_days": doc.get("watering_interval_days", 4),
        "price": doc.get("price", 399.0),
        "rating": doc.get("rating", 4.8),
        "reviews_count": doc.get("reviews_count", 0),
        "image_url": doc.get("image_url"),
        "description": doc.get("description"),
        "soil_type": doc.get("soil_type"),
        "temperature_range": doc.get("temperature_range"),
        "humidity": doc.get("humidity"),
        "care_instructions": doc.get("care_instructions", []),
        "created_at": doc.get("created_at"),
        "is_wishlisted": is_wishlisted
    }

@router.get("", response_model=List[PlantResponse])
def get_plants(
    category: Optional[str] = Query(None, description="Filter by botanical category"),
    search: Optional[str] = Query(None, description="Search by name, scientific name or keyword"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    sunlight: Optional[str] = Query(None, description="Filter by sunlight requirement"),
    limit: int = Query(50, ge=1, le=100),
    user: Optional[dict] = Depends(get_current_user_optional)
):
    db = get_db()
    plants_col = db.get_collection("plants")
    query = {}

    if category and category.lower() != "all":
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    if difficulty and difficulty.lower() != "all":
        query["difficulty"] = {"$regex": f"^{difficulty}$", "$options": "i"}

    if sunlight and sunlight.lower() != "all":
        query["sunlight"] = {"$regex": sunlight, "$options": "i"}

    if search and search.strip():
        s = search.strip()
        query["$or"] = [
            {"name": {"$regex": s, "$options": "i"}},
            {"scientific_name": {"$regex": s, "$options": "i"}},
            {"description": {"$regex": s, "$options": "i"}},
            {"category": {"$regex": s, "$options": "i"}}
        ]

    try:
        docs = plants_col.find(query, limit=limit)
    except Exception:
        docs = db.get_local_collection("plants").find(query, limit=limit)

    # Check user wishlist
    wishlisted_ids = set()
    if user:
        try:
            wishlist_col = db.get_collection("wishlists")
            user_wishes = wishlist_col.find({"user_id": str(user["_id"])})
            wishlisted_ids = {w.get("plant_id") for w in user_wishes}
        except Exception:
            pass

    return [format_plant(doc, is_wishlisted=str(doc.get("_id")) in wishlisted_ids) for doc in docs]

@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant_by_id(plant_id: str, user: Optional[dict] = Depends(get_current_user_optional)):
    db = get_db()
    plants_col = db.get_collection("plants")
    doc = None
    try:
        doc = plants_col.find_one({"$or": [{"_id": plant_id}, {"id": plant_id}]}) or plants_col.find_one({"_id": plant_id})
    except Exception:
        doc = db.get_local_collection("plants").find_one({"_id": plant_id})

    if not doc:
        doc = db.get_local_collection("plants").find_one({"_id": plant_id})

    if not doc:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not doc:
        raise HTTPException(status_code=404, detail="Plant not found")

    is_wishlisted = False
    if user:
        wishlist_col = db.get_collection("wishlists")
        is_wishlisted = bool(wishlist_col.find_one({"user_id": str(user["_id"]), "plant_id": plant_id}))

    return format_plant(doc, is_wishlisted=is_wishlisted)

@router.post("", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_plant(plant_in: PlantCreate, user: dict = Depends(get_current_user)):
    db = get_db()
    plants_col = db.get_collection("plants")
    
    plant_doc = plant_in.dict()
    plant_doc["_id"] = f"plant_{uuid.uuid4().hex[:8]}"
    plant_doc["created_at"] = datetime.utcnow().isoformat()
    plant_doc["updated_at"] = datetime.utcnow().isoformat()
    
    plants_col.insert_one(plant_doc)
    return format_plant(plant_doc, False)

@router.put("/{plant_id}", response_model=PlantResponse)
def update_plant(plant_id: str, plant_in: PlantUpdate, user: dict = Depends(get_current_user)):
    db = get_db()
    plants_col = db.get_collection("plants")
    existing = plants_col.find_one({"_id": plant_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Plant not found")

    update_data = {k: v for k, v in plant_in.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    plants_col.update_one({"_id": plant_id}, {"$set": update_data})
    updated = plants_col.find_one({"_id": plant_id})
    return format_plant(updated, False)

@router.delete("/{plant_id}")
def delete_plant(plant_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    plants_col = db.get_collection("plants")
    result = plants_col.delete_one({"_id": plant_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"message": "Plant deleted successfully", "id": plant_id}
