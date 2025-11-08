from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.database import db        # ✅ MongoDB
from core.auth import hash_password, verify_password, create_token
from core.logger import log_event   # ✅ Store logs in DB

router = APIRouter(prefix="/api", tags=["auth"])


# --- Request Schema (unchanged) ---
class AuthIn(BaseModel):
    username: str
    password: str


@router.post("/signup")
async def signup(payload: AuthIn):
    # ✅ Check if user already exists
    user = await db["users"].find_one({"username": payload.username})
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # ✅ Store new user
    new_user = {
        "username": payload.username,
        "password_hash": hash_password(payload.password)
    }
    await db["users"].insert_one(new_user)

    # ✅ Log event
    await log_event("users", {
        "username": payload.username,
        "action": "signup"
    })

    return {"result": "Signup successful ✅"}


@router.post("/login")
async def login(payload: AuthIn):
    # ✅ Fetch user
    user = await db["users"].find_one({"username": payload.username})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # ✅ Create token
    token = create_token({"sub": payload.username})

    # ✅ Log event
    await log_event("users", {
        "username": payload.username,
        "action": "login"
    })

    return {"result": {"token": token, "message": "Login successful ✅"}}
