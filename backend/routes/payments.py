import uuid
import time
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Request
from models.payment import OrderInitiateRequest, OrderInitiateResponse, PaymentVerifyRequest, OrderResponse
from services.paytm_service import calculate_checksum, verify_checksum_hash, build_order_timeline
from database import get_db
from utils.auth import get_current_user_optional, get_current_user
from config import settings

router = APIRouter(prefix="/api/payments", tags=["Paytm Payment Gateway"])

def format_order(doc: dict) -> dict:
    created_str = doc.get("created_at", datetime.utcnow().isoformat())
    try:
        created_dt = datetime.fromisoformat(created_str)
    except Exception:
        created_dt = datetime.utcnow()

    tracking_status = doc.get("tracking_status", "Order Placed")
    timeline = build_order_timeline(tracking_status, created_dt)
    est_delivery = (created_dt + timedelta(days=3)).strftime("%A, %B %d, %Y")

    return {
        "id": str(doc.get("_id")),
        "order_id": doc.get("order_id"),
        "user_id": str(doc.get("user_id", "guest")),
        "plant_id": doc.get("plant_id"),
        "plant_name": doc.get("plant_name"),
        "plant_image": doc.get("plant_image"),
        "unit_price": doc.get("unit_price", 399.0),
        "quantity": doc.get("quantity", 1),
        "total_amount": doc.get("total_amount", 399.0),
        "shipping_name": doc.get("shipping_name"),
        "shipping_phone": doc.get("shipping_phone"),
        "shipping_address": doc.get("shipping_address"),
        "shipping_city": doc.get("shipping_city"),
        "shipping_pincode": doc.get("shipping_pincode"),
        "payment_status": doc.get("payment_status", "PENDING"),
        "paytm_txn_id": doc.get("paytm_txn_id"),
        "payment_method": doc.get("payment_method", "PAYTM_UPI"),
        "tracking_status": tracking_status,
        "estimated_delivery": doc.get("estimated_delivery", est_delivery),
        "tracking_timeline": timeline,
        "created_at": created_str
    }

@router.post("/paytm/initiate", response_model=OrderInitiateResponse)
def initiate_paytm_payment(
    req: OrderInitiateRequest,
    user: Optional[dict] = Depends(get_current_user_optional)
):
    db = get_db()
    plants_col = db.get_collection("plants")
    orders_col = db.get_collection("orders")

    # Lookup plant by exact _id, id, or case-insensitive name/slug
    plant = plants_col.find_one({
        "$or": [
            {"_id": req.plant_id},
            {"id": req.plant_id},
            {"name": {"$regex": req.plant_id.replace("plant-", "").replace("-", " "), "$options": "i"}}
        ]
    })
    if not plant:
        # Fallback to any first plant in the catalog
        plant = plants_col.find_one({}) or {
            "_id": "plant_default",
            "name": "Botanical Plant",
            "price": 399.0,
            "image_url": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80"
        }

    unit_price = float(plant.get("price", 399.0))
    total_amount = round(unit_price * req.quantity, 2)
    order_id = f"GM_PTM_{int(time.time())}_{uuid.uuid4().hex[:4].upper()}"
    user_id = str(user["_id"]) if user else f"guest_{uuid.uuid4().hex[:6]}"

    # Prepare standard Paytm params
    paytm_params = {
        "MID": settings.PAYTM_MID,
        "WEBSITE": settings.PAYTM_WEBSITE,
        "INDUSTRY_TYPE_ID": settings.PAYTM_INDUSTRY_TYPE_ID,
        "CHANNEL_ID": settings.PAYTM_CHANNEL_ID,
        "ORDER_ID": order_id,
        "CUST_ID": user_id,
        "TXN_AMOUNT": f"{total_amount:.2f}",
        "CALLBACK_URL": f"http://{settings.HOST}:{settings.PORT}/api/payments/paytm/callback"
    }

    # Generate Paytm Checksum
    checksum = calculate_checksum(paytm_params, settings.PAYTM_MERCHANT_KEY)
    paytm_params["CHECKSUMHASH"] = checksum

    # Real Paytm UPI QR payload
    qr_payload = f"upi://pay?pa=greenmateai@paytm&pn=GreenMateAI&am={total_amount:.2f}&tr={order_id}&cu=INR&tn=GreenMatePlantOrder_{order_id}"

    # Persist pending order in MongoDB
    now_iso = datetime.utcnow().isoformat()
    est_delivery = (datetime.utcnow() + timedelta(days=3)).strftime("%A, %B %d, %Y")

    order_doc = {
        "_id": str(uuid.uuid4()),
        "order_id": order_id,
        "user_id": user_id,
        "plant_id": str(plant["_id"]),
        "plant_name": plant["name"],
        "plant_image": plant.get("image_url", ""),
        "unit_price": unit_price,
        "quantity": req.quantity,
        "total_amount": total_amount,
        "shipping_name": req.shipping_name,
        "shipping_phone": req.shipping_phone,
        "shipping_address": req.shipping_address,
        "shipping_city": req.shipping_city,
        "shipping_pincode": req.shipping_pincode,
        "payment_status": "PENDING",
        "paytm_txn_id": None,
        "payment_method": req.payment_method,
        "tracking_status": "PENDING",
        "estimated_delivery": est_delivery,
        "checksum": checksum,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    orders_col.insert_one(order_doc)

    return OrderInitiateResponse(
        order_id=order_id,
        amount=total_amount,
        currency="INR",
        plant_name=plant["name"],
        plant_image=plant.get("image_url", ""),
        quantity=req.quantity,
        paytm_mid=settings.PAYTM_MID,
        txn_token=uuid.uuid4().hex,
        checksum=checksum,
        paytm_env=settings.PAYTM_ENV,
        qr_payload=qr_payload,
        paytm_params=paytm_params
    )

@router.post("/paytm/verify", response_model=OrderResponse)
def verify_paytm_payment(
    req: PaymentVerifyRequest,
    user: Optional[dict] = Depends(get_current_user_optional)
):
    db = get_db()
    orders_col = db.get_collection("orders")
    garden_col = db.get_collection("user_gardens")
    plants_col = db.get_collection("plants")

    order = orders_col.find_one({"order_id": req.order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    txn_id = req.paytm_txn_id or f"PTM_TXN_{int(time.time()*1000)}"
    now_iso = datetime.utcnow().isoformat()

    # Update order in MongoDB
    orders_col.update_one(
        {"order_id": req.order_id},
        {"$set": {
            "payment_status": "PAID",
            "paytm_txn_id": txn_id,
            "payment_method": req.payment_method or order.get("payment_method", "PAYTM_UPI"),
            "tracking_status": "Order Placed",
            "updated_at": now_iso
        }}
    )

    # If user is logged in, optionally auto-add the purchased plant to their Smart Garden!
    user_id = str(user["_id"]) if user else (order.get("user_id") if not str(order.get("user_id")).startswith("guest") else None)
    if user_id:
        catalog_plant = plants_col.find_one({"_id": order["plant_id"]})
        interval = catalog_plant.get("watering_interval_days", 5) if catalog_plant else 5
        garden_item = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "plant_id": order["plant_id"],
            "name": order["plant_name"],
            "nickname": f"{order['plant_name']} (Paytm Order)",
            "location": "Living Room",
            "image_url": order["plant_image"],
            "watering_interval_days": interval,
            "health_status": "Healthy",
            "notes": f"Purchased via Paytm on {datetime.utcnow().strftime('%b %d, %Y')}. Order ID: {req.order_id}",
            "last_watered_at": now_iso,
            "next_watering_at": (datetime.utcnow() + timedelta(days=interval)).isoformat(),
            "created_at": now_iso,
            "updated_at": now_iso
        }
        garden_col.insert_one(garden_item)

    updated_order = orders_col.find_one({"order_id": req.order_id})
    return format_order(updated_order)

@router.get("/orders", response_model=List[OrderResponse])
def get_user_orders(user: dict = Depends(get_current_user)):
    db = get_db()
    orders_col = db.get_collection("orders")
    user_id = str(user["_id"])
    docs = orders_col.find({"user_id": user_id}, sort=[("created_at", -1)])
    return [format_order(d) for d in docs]

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_tracking(order_id: str):
    db = get_db()
    orders_col = db.get_collection("orders")
    doc = orders_col.find_one({"order_id": order_id})
    if not doc:
        raise HTTPException(status_code=404, detail=f"No order found with ID '{order_id}'")
    return format_order(doc)
