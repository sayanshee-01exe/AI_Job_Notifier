"""
Pydantic schemas for resume parsing output.
"""

from typing import List, Optional

from pydantic import BaseModel


class ResumeData(BaseModel):
    """Structured data extracted from a resume."""
    skills: List[str] = []
    experience: str = ""
    education: List[str] = []
    raw_text: Optional[str] = None


class ResumeUploadResponse(BaseModel):
    """Response after successful resume upload and parsing."""
    message: str
    filename: str
    parsed_data: ResumeData
