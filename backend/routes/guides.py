from typing import List
from fastapi import APIRouter, HTTPException
from models.guide import GuideResponse
from database import get_db

router = APIRouter(prefix="/api/guides", tags=["Plant Care Guides"])

def format_guide(doc: dict) -> dict:
    return {
        "id": str(doc.get("_id")),
        "title": doc.get("title"),
        "subtitle": doc.get("subtitle"),
        "category": doc.get("category"),
        "read_time": doc.get("read_time", "5 min read"),
        "image_url": doc.get("image_url"),
        "summary": doc.get("summary"),
        "content": doc.get("content")
    }

@router.get("", response_model=List[GuideResponse])
def get_all_guides():
    db = get_db()
    guides_col = db.get_collection("plant_guides")
    docs = guides_col.find()
    return [format_guide(d) for d in docs]

@router.get("/{guide_id}", response_model=GuideResponse)
def get_guide_by_id(guide_id: str):
    db = get_db()
    guides_col = db.get_collection("plant_guides")
    doc = guides_col.find_one({"_id": guide_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Guide not found")
    return format_guide(doc)
