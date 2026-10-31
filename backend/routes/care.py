import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from models.care import (
    CareScheduleCreate, CareScheduleResponse,
    WateringLogCreate, WateringLogResponse,
    GrowthRecordCreate, GrowthRecordResponse
)
from utils.auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api", tags=["Plant Care & Schedules"])

@router.get("/care-schedules", response_model=List[CareScheduleResponse])
def get_care_schedules(user: dict = Depends(get_current_user)):
    db = get_db()
    schedules_col = db.get_collection("care_schedules")
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])
    
    docs = schedules_col.find({"user_id": user_id})
    result = []
    now = datetime.utcnow()

    for s in docs:
        garden_item = garden_col.find_one({"_id": s.get("garden_plant_id")})
        plant_name = s.get("plant_name") or (garden_item.get("name") if garden_item else "Plant")
        plant_img = s.get("plant_image") or (garden_item.get("image_url") if garden_item else None)
        
        last_watered = garden_item.get("last_watered_at") if garden_item else s.get("last_watered_at")
        interval = s.get("watering_interval_days", 5)
        next_watered = None
        is_overdue = False

        if last_watered:
            try:
                lw_dt = datetime.fromisoformat(last_watered)
                next_dt = lw_dt + timedelta(days=interval)
                next_watered = next_dt.isoformat()
                is_overdue = (now > next_dt)
            except Exception:
                pass

        result.append(CareScheduleResponse(
            id=str(s.get("_id")),
            user_id=user_id,
            garden_plant_id=s.get("garden_plant_id"),
            plant_name=plant_name,
            plant_image=plant_img,
            watering_interval_days=interval,
            reminder_time=s.get("reminder_time", "09:00"),
            notifications_enabled=s.get("notifications_enabled", True),
            last_watered_at=last_watered,
            next_watering_at=next_watered,
            is_overdue=is_overdue
        ))
    return result

@router.post("/care-schedules", response_model=CareScheduleResponse)
def set_care_schedule(req: CareScheduleCreate, user: dict = Depends(get_current_user)):
    db = get_db()
    schedules_col = db.get_collection("care_schedules")
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])

    garden_plant = garden_col.find_one({"_id": req.garden_plant_id, "user_id": user_id})
    if not garden_plant:
        raise HTTPException(status_code=404, detail="Garden plant not found")

    existing = schedules_col.find_one({"garden_plant_id": req.garden_plant_id, "user_id": user_id})
    now_iso = datetime.utcnow().isoformat()

    if existing:
        schedules_col.update_one(
            {"_id": existing["_id"]},
            {"$set": {
                "watering_interval_days": req.watering_interval_days,
                "reminder_time": req.reminder_time or "09:00",
                "notifications_enabled": req.notifications_enabled,
                "updated_at": now_iso
            }}
        )
        sched_id = existing["_id"]
    else:
        sched_id = str(uuid.uuid4())
        schedules_col.insert_one({
            "_id": sched_id,
            "user_id": user_id,
            "garden_plant_id": req.garden_plant_id,
            "plant_name": garden_plant["name"],
            "plant_image": garden_plant.get("image_url"),
            "watering_interval_days": req.watering_interval_days,
            "reminder_time": req.reminder_time or "09:00",
            "notifications_enabled": req.notifications_enabled,
            "last_watered_at": garden_plant.get("last_watered_at"),
            "created_at": now_iso
        })

    # Update plant interval in garden
    garden_col.update_one(
        {"_id": req.garden_plant_id},
        {"$set": {"watering_interval_days": req.watering_interval_days}}
    )

    return CareScheduleResponse(
        id=sched_id,
        user_id=user_id,
        garden_plant_id=req.garden_plant_id,
        plant_name=garden_plant["name"],
        plant_image=garden_plant.get("image_url"),
        watering_interval_days=req.watering_interval_days,
        reminder_time=req.reminder_time or "09:00",
        notifications_enabled=req.notifications_enabled,
        last_watered_at=garden_plant.get("last_watered_at"),
        is_overdue=False
    )

@router.post("/watering-logs", response_model=WateringLogResponse, status_code=status.HTTP_201_CREATED)
def record_watering(req: WateringLogCreate, user: dict = Depends(get_current_user)):
    db = get_db()
    logs_col = db.get_collection("watering_logs")
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])

    garden_plant = garden_col.find_one({"_id": req.garden_plant_id, "user_id": user_id})
    if not garden_plant:
        raise HTTPException(status_code=404, detail="Garden plant not found")

    now = datetime.utcnow()
    now_iso = now.isoformat()
    interval = garden_plant.get("watering_interval_days", 5)
    next_iso = (now + timedelta(days=interval)).isoformat()

    # Update garden plant's watering timestamp
    garden_col.update_one(
        {"_id": req.garden_plant_id},
        {"$set": {
            "last_watered_at": now_iso,
            "next_watering_at": next_iso
        }}
    )

    log_id = str(uuid.uuid4())
    log_doc = {
        "_id": log_id,
        "user_id": user_id,
        "garden_plant_id": req.garden_plant_id,
        "plant_name": garden_plant["name"],
        "watered_at": now_iso,
        "notes": req.notes,
        "amount_ml": req.amount_ml or 250
    }
    logs_col.insert_one(log_doc)

    return WateringLogResponse(
        id=log_id,
        user_id=user_id,
        garden_plant_id=req.garden_plant_id,
        plant_name=garden_plant["name"],
        watered_at=now_iso,
        notes=req.notes,
        amount_ml=req.amount_ml or 250
    )

@router.get("/watering-logs", response_model=List[WateringLogResponse])
def get_watering_logs(user: dict = Depends(get_current_user), limit: int = 20):
    db = get_db()
    logs_col = db.get_collection("watering_logs")
    user_id = str(user["_id"])
    docs = logs_col.find({"user_id": user_id}, sort=[("watered_at", -1)], limit=limit)
    
    return [
        WateringLogResponse(
            id=str(d["_id"]),
            user_id=user_id,
            garden_plant_id=d["garden_plant_id"],
            plant_name=d.get("plant_name", "Plant"),
            watered_at=d["watered_at"],
            notes=d.get("notes"),
            amount_ml=d.get("amount_ml", 250)
        )
        for d in docs
    ]

@router.post("/growth-records", response_model=GrowthRecordResponse, status_code=status.HTTP_201_CREATED)
def record_growth(req: GrowthRecordCreate, user: dict = Depends(get_current_user)):
    db = get_db()
    growth_col = db.get_collection("growth_records")
    garden_col = db.get_collection("user_gardens")
    user_id = str(user["_id"])

    garden_plant = garden_col.find_one({"_id": req.garden_plant_id, "user_id": user_id})
    if not garden_plant:
        raise HTTPException(status_code=404, detail="Garden plant not found")

    rec_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat()
    rec_doc = {
        "_id": rec_id,
        "user_id": user_id,
        "garden_plant_id": req.garden_plant_id,
        "plant_name": garden_plant["name"],
        "height_cm": req.height_cm,
        "new_leaves_count": req.new_leaves_count,
        "health_notes": req.health_notes,
        "photo_url": req.photo_url or garden_plant.get("image_url"),
        "recorded_at": now_iso
    }
    growth_col.insert_one(rec_doc)

    return GrowthRecordResponse(
        id=rec_id,
        user_id=user_id,
        garden_plant_id=req.garden_plant_id,
        plant_name=garden_plant["name"],
        height_cm=req.height_cm,
        new_leaves_count=req.new_leaves_count,
        health_notes=req.health_notes,
        photo_url=rec_doc["photo_url"],
        recorded_at=now_iso
    )

@router.get("/growth-records", response_model=List[GrowthRecordResponse])
def get_growth_records(user: dict = Depends(get_current_user), limit: int = 30):
    db = get_db()
    growth_col = db.get_collection("growth_records")
    user_id = str(user["_id"])
    docs = growth_col.find({"user_id": user_id}, sort=[("recorded_at", -1)], limit=limit)
    return [
        GrowthRecordResponse(
            id=str(d["_id"]),
            user_id=user_id,
            garden_plant_id=d["garden_plant_id"],
            plant_name=d.get("plant_name", "Plant"),
            height_cm=d.get("height_cm"),
            new_leaves_count=d.get("new_leaves_count"),
            health_notes=d.get("health_notes"),
            photo_url=d.get("photo_url"),
            recorded_at=d["recorded_at"]
        )
        for d in docs
    ]
