import hashlib
import hmac
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from config import settings

logger = logging.getLogger("greenmate.paytm")

def calculate_checksum(params: Dict[str, Any], key: str) -> str:
    """Generate SHA256 HMAC checksum matching Paytm payment protocol."""
    sorted_keys = sorted(params.keys())
    data_str = "|".join(f"{k}={params[k]}" for k in sorted_keys if k != "CHECKSUMHASH")
    hashed = hmac.new(key.encode("utf-8"), data_str.encode("utf-8"), hashlib.sha256).hexdigest()
    return hashed

def verify_checksum_hash(params: Dict[str, Any], key: str, checksum: str) -> bool:
    expected = calculate_checksum(params, key)
    return hmac.compare_digest(expected, checksum)

def build_order_timeline(current_status: str, created_dt: datetime) -> list:
    steps = [
        {"step": "PLACED", "label": "Order Placed with Paytm", "desc": "Payment verified and order accepted", "offset_hours": 0},
        {"step": "INSPECTION", "label": "Botanical Health Inspection", "desc": "Certified botanist verifies foliage & root health", "offset_hours": 4},
        {"step": "PACKED", "label": "Eco-Friendly Botanical Packaging", "desc": "Moisture-retaining coco wrap with ventilated container", "offset_hours": 12},
        {"step": "DISPATCHED", "label": "Dispatched via Plant Express", "desc": "Assigned tracking with temperature-controlled transit", "offset_hours": 24},
        {"step": "OUT_FOR_DELIVERY", "label": "Out for Delivery", "desc": "Courier rider delivering to doorstep", "offset_hours": 48},
        {"step": "DELIVERED", "label": "Delivered to Sanctuary", "desc": "Unboxing instructions & care plan activated", "offset_hours": 60}
    ]

    status_ranks = {
        "PENDING": -1,
        "PLACED": 0,
        "Order Placed": 0,
        "INSPECTION": 1,
        "Botanical Inspection": 1,
        "PACKED": 2,
        "Safely Packed": 2,
        "DISPATCHED": 3,
        "Dispatched": 3,
        "OUT_FOR_DELIVERY": 4,
        "Out for Delivery": 4,
        "DELIVERED": 5,
        "Delivered": 5
    }

    current_rank = status_ranks.get(current_status, 0)
    timeline = []
    
    for i, s in enumerate(steps):
        target_time = created_dt + timedelta(hours=s["offset_hours"])
        if i < current_rank:
            st = "completed"
            ts = target_time.strftime("%b %d, %I:%M %p")
        elif i == current_rank:
            st = "current"
            ts = target_time.strftime("%b %d, %I:%M %p")
        else:
            st = "upcoming"
            ts = f"Est. {target_time.strftime('%b %d, %I:%M %p')}"

        timeline.append({
            "step": s["step"],
            "label": s["label"],
            "desc": s["desc"],
            "status": st,
            "timestamp": ts
        })

    return timeline
