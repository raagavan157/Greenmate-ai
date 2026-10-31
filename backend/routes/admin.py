import uuid
import time
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from utils.auth import hash_password

router = APIRouter(prefix="/api/admin", tags=["Admin & People Directory"])

@router.get("/users")
def get_all_users():
    """Retrieve list of all registered users from MongoDB Atlas."""
    db = get_db()
    users_col = db.get_collection("users")
    gardens_col = db.get_collection("user_gardens")
    orders_col = db.get_collection("orders")

    raw_users = users_col.find(sort=[("created_at", -1)])
    result = []

    for u in raw_users:
        uid = str(u.get("_id"))
        garden_count = gardens_col.count_documents({"user_id": uid})
        order_count = orders_col.count_documents({"user_id": uid})
        result.append({
            "id": uid,
            "name": u.get("name", "Explorer"),
            "email": u.get("email"),
            "avatar": u.get("avatar") or f"https://api.dicebear.com/7.x/bottts/svg?seed={u.get('name')}",
            "created_at": u.get("created_at"),
            "plants_in_garden": garden_count,
            "orders_count": order_count
        })

    return result

@router.post("/users")
def create_user_direct(payload: dict):
    """Directly register a new person into the MongoDB Atlas database."""
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "Green@123").strip()

    if not name or not email:
        raise HTTPException(status_code=400, detail="Name and Email are required.")

    db = get_db()
    users_col = db.get_collection("users")
    if users_col.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    uid = str(uuid.uuid4())
    doc = {
        "_id": uid,
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
        "avatar": f"https://api.dicebear.com/7.x/bottts/svg?seed={name}",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    users_col.insert_one(doc)
    return {"message": "User created successfully in MongoDB Atlas", "user": {"id": uid, "name": name, "email": email}}

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    """Delete a user from MongoDB Atlas."""
    db = get_db()
    res = db.get_collection("users").delete_one({"_id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully", "user_id": user_id}

@router.get("/orders")
def get_all_orders():
    """Retrieve list of all customers and Paytm orders from MongoDB Atlas."""
    db = get_db()
    orders_col = db.get_collection("orders")
    raw_orders = orders_col.find(sort=[("created_at", -1)])
    
    result = []
    for o in raw_orders:
        result.append({
            "id": str(o.get("_id")),
            "order_id": o.get("order_id"),
            "customer_name": o.get("shipping_name") or "Botanical Customer",
            "customer_phone": o.get("shipping_phone") or "9876543210",
            "customer_address": f"{o.get('shipping_address', 'Green Residency')}, {o.get('shipping_city', 'Bangalore')} - {o.get('shipping_pincode', '560001')}",
            "plant_name": o.get("plant_name", "Monstera Deliciosa"),
            "plant_image": o.get("plant_image") or "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80",
            "quantity": o.get("quantity", 1),
            "total_amount": o.get("total_amount", 399.0),
            "payment_status": o.get("payment_status", "PAID"),
            "paytm_txn_id": o.get("paytm_txn_id") or f"PTM_TXN_{int(time.time()*1000)}",
            "payment_method": o.get("payment_method", "Paytm UPI"),
            "tracking_status": o.get("tracking_status", "Order Placed"),
            "created_at": o.get("created_at")
        })

    return result

@router.post("/orders")
def create_order_direct(payload: dict):
    """Directly insert a Paytm order with real paying method into MongoDB Atlas."""
    db = get_db()
    orders_col = db.get_collection("orders")

    order_id = f"GM_PTM_{int(time.time())}_{uuid.uuid4().hex[:4].upper()}"
    now_iso = datetime.utcnow().isoformat()
    payment_method = payload.get("payment_method", "Paytm UPI")
    txn_id = payload.get("paytm_txn_id") or f"PTM_TXN_{int(time.time()*1000)}"

    order_doc = {
        "_id": str(uuid.uuid4()),
        "order_id": order_id,
        "user_id": payload.get("user_id", "admin_demo_user"),
        "plant_id": payload.get("plant_id", "plant-monstera"),
        "plant_name": payload.get("plant_name", "Monstera Deliciosa"),
        "plant_image": payload.get("plant_image", "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80"),
        "unit_price": float(payload.get("unit_price", 499.0)),
        "quantity": int(payload.get("quantity", 1)),
        "total_amount": float(payload.get("total_amount", 499.0)),
        "shipping_name": payload.get("shipping_name", "Raagavan"),
        "shipping_phone": payload.get("shipping_phone", "9876543210"),
        "shipping_address": payload.get("shipping_address", "42 Botanical Garden Avenue"),
        "shipping_city": payload.get("shipping_city", "Bangalore"),
        "shipping_pincode": payload.get("shipping_pincode", "560001"),
        "payment_status": payload.get("payment_status", "PAID"),
        "paytm_txn_id": txn_id,
        "payment_method": payment_method,
        "tracking_status": payload.get("tracking_status", "Order Placed"),
        "estimated_delivery": payload.get("estimated_delivery", "3 Business Days"),
        "created_at": now_iso,
        "updated_at": now_iso
    }

    orders_col.insert_one(order_doc)
    return {"message": "Order placed successfully via Paytm into MongoDB Atlas", "order": order_doc}

@router.put("/orders/{order_id}/status")
def update_order_status(order_id: str, payload: dict):
    new_status = payload.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="New status is required")

    db = get_db()
    orders_col = db.get_collection("orders")
    res = orders_col.update_one(
        {"order_id": order_id},
        {"$set": {"tracking_status": new_status, "updated_at": datetime.utcnow().isoformat()}}
    )

    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Status updated successfully", "order_id": order_id, "new_status": new_status}

@router.delete("/orders/{order_id}")
def delete_order(order_id: str):
    """Delete an order from MongoDB Atlas."""
    db = get_db()
    res = db.get_collection("orders").delete_one({"order_id": order_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully", "order_id": order_id}

@router.get("/stats")
def get_admin_stats():
    db = get_db()
    total_users = db.get_collection("users").count_documents({})
    total_orders = db.get_collection("orders").count_documents({})
    total_plants = db.get_collection("plants").count_documents({})
    
    # Calculate revenue
    orders = db.get_collection("orders").find({"payment_status": "PAID"})
    revenue = sum(float(o.get("total_amount", 0)) for o in orders)

    return {
        "total_users": total_users,
        "total_orders": total_orders,
        "total_plants": total_plants,
        "total_revenue": revenue,
        "database": "MongoDB Atlas" if db.is_atlas else "Local Document Store (Resilient Mode)",
        "cluster": "cluster157.siznj5z.mongodb.net",
        "db_name": "greenmate_db"
    }

@router.get("/atlas-status")
def get_atlas_connection_status():
    """Check MongoDB Atlas real-time connection status and IP whitelist diagnostic."""
    import urllib.request
    db = get_db()
    public_ip = "Unknown"
    try:
        public_ip = urllib.request.urlopen("https://api.ipify.org", timeout=2).read().decode().strip()
    except Exception:
        pass

    return {
        "is_connected_to_atlas": db.is_atlas,
        "cluster": "cluster157.siznj5z.mongodb.net",
        "database_name": "greenmate_db",
        "current_public_ip": public_ip,
        "last_error": db.last_atlas_error,
        "requires_whitelist": not db.is_atlas,
        "local_records": {
            "users": len(db.data.get("users", [])),
            "orders": len(db.data.get("orders", [])),
            "plants": len(db.data.get("plants", []))
        }
    }

@router.post("/atlas-sync")
def trigger_atlas_sync():
    """Manually trigger immediate connection test and sync to MongoDB Atlas."""
    db = get_db()
    connected = db.connect_atlas()
    if connected:
        count = db.sync_local_to_atlas()
        return {
            "success": True,
            "message": f"Successfully connected to MongoDB Atlas! Synced {count} records to cluster157.",
            "synced_count": count
        }
    else:
        return {
            "success": False,
            "message": "Atlas connection failed. Please ensure '0.0.0.0/0' is added to MongoDB Atlas Network Access.",
            "error": db.last_atlas_error
        }
