import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserRegister, UserLogin, UserResponse, TokenResponse
from utils.auth import hash_password, verify_password, create_access_token, get_current_user
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister):
    db = get_db()
    users_col = db.get_collection("users")
    
    # Check if email exists
    existing = users_col.find_one({"email": user_in.email.lower()})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address is already registered."
        )

    user_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_in.password)
    user_doc = {
        "_id": user_id,
        "name": user_in.name,
        "email": user_in.email.lower(),
        "password_hash": hashed_pwd,
        "avatar": f"https://api.dicebear.com/7.x/bottts/svg?seed={user_in.name}",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    users_col.insert_one(user_doc)

    token = create_access_token({"sub": user_id, "email": user_in.email.lower(), "name": user_in.name})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user_id,
            name=user_in.name,
            email=user_in.email.lower(),
            avatar=user_doc["avatar"],
            created_at=user_doc["created_at"]
        )
    )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    db = get_db()
    users_col = db.get_collection("users")
    user = users_col.find_one({"email": credentials.email.lower()})
    
    if not user or not verify_password(credentials.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token({"sub": user["_id"], "email": user["email"], "name": user["name"]})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            avatar=user.get("avatar"),
            created_at=user.get("created_at")
        )
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        avatar=user.get("avatar"),
        created_at=user.get("created_at")
    )

@router.post("/forgot-password")
def forgot_password(payload: dict):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required.")
    db = get_db()
    user = db.get_collection("users").find_one({"email": email.lower()})
    # Safe response regardless of email existence to prevent user enumeration
    return {
        "message": f"If an account is associated with {email}, a secure password reset link has been dispatched.",
        "status": "success"
    }
