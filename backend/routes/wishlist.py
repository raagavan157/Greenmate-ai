import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from utils.auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])

@router.get("")
def get_user_wishlist(user: dict = Depends(get_current_user)):
    db = get_db()
    wishlist_col = db.get_collection("wishlists")
    plants_col = db.get_collection("plants")
    user_id = str(user["_id"])

    wishes = wishlist_col.find({"user_id": user_id})
    plant_ids = [w.get("plant_id") for w in wishes]
    
    plants = []
    for pid in plant_ids:
        p = plants_col.find_one({"_id": pid})
        if p:
            plant_data = dict(p)
            plant_data["id"] = str(plant_data.pop("_id"))
            plant_data["is_wishlisted"] = True
            plants.append(plant_data)
            
    return plants

@router.post("", status_code=status.HTTP_201_CREATED)
def add_to_wishlist(payload: dict = Body(...), user: dict = Depends(get_current_user)):
    plant_id = payload.get("plant_id")
    if not plant_id:
        raise HTTPException(status_code=400, detail="plant_id is required.")

    db = get_db()
    wishlist_col = db.get_collection("wishlists")
    plants_col = db.get_collection("plants")
    user_id = str(user["_id"])

    # Verify plant exists
    plant = plants_col.find_one({"_id": plant_id})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    existing = wishlist_col.find_one({"user_id": user_id, "plant_id": plant_id})
    if not existing:
        wishlist_col.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "plant_id": plant_id,
            "created_at": datetime.utcnow().isoformat()
        })
    return {"message": "Added to wishlist", "plant_id": plant_id, "is_wishlisted": True}

@router.delete("/{plant_id}")
def remove_from_wishlist(plant_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    wishlist_col = db.get_collection("wishlists")
    user_id = str(user["_id"])

    res = wishlist_col.delete_one({"user_id": user_id, "plant_id": plant_id})
    return {"message": "Removed from wishlist", "plant_id": plant_id, "is_wishlisted": False}
