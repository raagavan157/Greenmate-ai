import os
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from models.ai import PlantIdentifyResponse, DiseaseDiagnoseResponse, CarePlanRequest, CarePlanResponse, ChatRequest, ChatResponse
from services.plant_ai import analyze_plant_image
from services.disease_ai import analyze_plant_disease
from services.care_ai import generate_personalized_care_plan
from services.chatbot_ai import generate_chat_response
from utils.auth import get_current_user_optional, get_current_user
from database import get_db
from config import settings

router = APIRouter(prefix="/api/ai", tags=["AI Features"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_and_save_upload(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".jpg"
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid image format. Allowed: JPG, PNG, WEBP.")
    
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = settings.UPLOAD_DIR / unique_name
    
    # Save file contents
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Image file exceeds 10MB limit.")
    
    with open(dest_path, "wb") as f:
        f.write(content)
        
    return str(dest_path), f"/uploads/{unique_name}"

@router.post("/identify", response_model=PlantIdentifyResponse)
def identify_plant(
    file: UploadFile = File(...),
    user: Optional[dict] = Depends(get_current_user_optional)
):
    local_path, rel_url = validate_and_save_upload(file)
    result = analyze_plant_image(local_path, filename=file.filename)
    result["image_url"] = rel_url

    # Persist identification record in MongoDB
    db = get_db()
    identifications_col = db.get_collection("plant_identifications")
    record = {
        "_id": str(uuid.uuid4()),
        "user_id": str(user["_id"]) if user else "guest",
        "common_name": result["common_name"],
        "scientific_name": result["scientific_name"],
        "confidence": result["confidence"],
        "image_url": rel_url,
        "category": result["category"],
        "ai_source": result["ai_source"],
        "created_at": datetime.utcnow().isoformat()
    }
    identifications_col.insert_one(record)

    return PlantIdentifyResponse(**result)

@router.post("/diagnose", response_model=DiseaseDiagnoseResponse)
def diagnose_disease(
    file: UploadFile = File(...),
    user: Optional[dict] = Depends(get_current_user_optional)
):
    local_path, rel_url = validate_and_save_upload(file)
    result = analyze_plant_disease(local_path, filename=file.filename)
    result["image_url"] = rel_url

    # Persist diagnosis record in MongoDB
    db = get_db()
    diagnoses_col = db.get_collection("plant_diagnoses")
    record = {
        "_id": str(uuid.uuid4()),
        "user_id": str(user["_id"]) if user else "guest",
        "plant_name": result.get("plant_name", "Specimen"),
        "disease_name": result["disease_name"],
        "confidence": result["confidence"],
        "severity": result["severity"],
        "image_url": rel_url,
        "ai_source": result["ai_source"],
        "created_at": datetime.utcnow().isoformat()
    }
    diagnoses_col.insert_one(record)

    return DiseaseDiagnoseResponse(**result)

@router.post("/care-plan", response_model=CarePlanResponse)
def get_care_plan(req: CarePlanRequest):
    result = generate_personalized_care_plan(req.dict())
    return CarePlanResponse(**result)

@router.post("/chat", response_model=ChatResponse)
def chat_ai(
    req: ChatRequest,
    user: Optional[dict] = Depends(get_current_user_optional)
):
    history_dicts = [{"role": h.role, "content": h.content} for h in (req.history or [])]
    result = generate_chat_response(
        message=req.message,
        plant_context=req.plant_context,
        history=history_dicts
    )

    # Persist chat history if user is authenticated
    if user:
        db = get_db()
        chat_col = db.get_collection("chat_history")
        turn = {
            "_id": str(uuid.uuid4()),
            "user_id": str(user["_id"]),
            "user_message": req.message,
            "assistant_reply": result["reply"],
            "plant_context": req.plant_context,
            "created_at": datetime.utcnow().isoformat()
        }
        chat_col.insert_one(turn)

    return ChatResponse(**result)

@router.get("/chat-history")
def get_chat_history(user: dict = Depends(get_current_user), limit: int = 20):
    db = get_db()
    chat_col = db.get_collection("chat_history")
    history = chat_col.find({"user_id": str(user["_id"])}, sort=[("created_at", -1)], limit=limit)
    return list(reversed(history))
