"""
Pydantic schemas for User operations.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ───────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    education: Optional[List[str]] = None


# ── Response Schemas ──────────────────────────────────────
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    skills: List[str] = []
    experience: str = ""
    education: List[str] = []
    resume_path: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
