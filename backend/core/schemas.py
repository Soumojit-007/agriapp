from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


# ---------------- USER (for Auth) ----------------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserDB(BaseModel):
    id: str
    username: str
    password_hash: str


# ---------------- ASK MODEL ----------------

class AskIn(BaseModel):
    text: str = Field(..., description="User query text")
    lang: Optional[str] = Field(
        default=None,
        description="Language code (optional, auto-detected)"
    )


# ---------------- FERTILIZER RECOMMENDATION MODEL ----------------

class FertIn(BaseModel):
    crop: str = Field(..., description="Name of the crop")
    soil: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional soil parameters (e.g., pH, moisture, NPK ratios)"
    )
    symptoms: Optional[str] = Field(
        default=None,
        description="Visible crop symptoms, if any"
    )
    organicPreferred: bool = Field(
        default=False,
        description="Whether organic fertilizers are preferred"
    )
