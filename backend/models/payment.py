from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class OrderInitiateRequest(BaseModel):
    plant_id: str
    quantity: int = Field(default=1, ge=1, le=10)
    shipping_name: str = Field(..., min_length=2)
    shipping_phone: str = Field(..., min_length=10)
    shipping_address: str = Field(..., min_length=5)
    shipping_city: str = Field(..., min_length=2)
    shipping_pincode: str = Field(..., min_length=4)
    payment_method: str = "PAYTM_UPI"  # PAYTM_UPI, PAYTM_WALLET, PAYTM_QR, PAYTM_CARD

class OrderInitiateResponse(BaseModel):
    order_id: str
    amount: float
    currency: str = "INR"
    plant_name: str
    plant_image: str
    quantity: int
    paytm_mid: str
    txn_token: str
    checksum: str
    paytm_env: str
    qr_payload: str
    paytm_params: Dict[str, Any]

class PaymentVerifyRequest(BaseModel):
    order_id: str
    paytm_txn_id: Optional[str] = None
    payment_method: Optional[str] = "PAYTM_UPI"
    checksum: Optional[str] = None
    simulate_status: Optional[str] = "TXN_SUCCESS"

class OrderTrackingTimeline(BaseModel):
    step: str
    label: str
    status: str  # completed, current, upcoming
    timestamp: Optional[str] = None

class OrderResponse(BaseModel):
    id: str
    order_id: str
    user_id: str
    plant_id: str
    plant_name: str
    plant_image: str
    unit_price: float
    quantity: int
    total_amount: float
    shipping_name: str
    shipping_phone: str
    shipping_address: str
    shipping_city: str
    shipping_pincode: str
    payment_status: str  # PENDING, PAID, FAILED, REFUNDED
    paytm_txn_id: Optional[str] = None
    payment_method: str
    tracking_status: str  # Order Placed, Confirmed, Botanical Inspection, Safely Packed, Shipped, Out for Delivery, Delivered
    estimated_delivery: str
    tracking_timeline: List[Dict[str, Any]]
    created_at: str
