"""
Pydantic schemas for Job operations.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ── Request Schemas ───────────────────────────────────────
class JobCreate(BaseModel):
    title: str = Field(..., max_length=255)
    company: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    description: str
    skills_required: List[str] = []
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: str = "Full-time"
    source_url: Optional[str] = None


class JobFilter(BaseModel):
    location: Optional[str] = None
    role: Optional[str] = None
    experience_level: Optional[str] = None
    skills: Optional[List[str]] = None


# ── Response Schemas ──────────────────────────────────────
class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    skills_required: List[str] = []
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: str
    source_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class JobMatch(BaseModel):
    """A job with its computed match score for a user."""
    job: JobResponse
    match_score: float = Field(..., ge=0.0, le=1.0)
    skill_match_score: float = 0.0
    similarity_score: float = 0.0
    recency_score: float = 0.0
