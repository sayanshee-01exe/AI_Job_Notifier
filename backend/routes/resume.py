"""
Resume upload route.
"""

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.schemas.resume import ResumeUploadResponse
from backend.services.resume_service import handle_resume_upload

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a resume (PDF/DOCX) for NLP parsing and profile update."""
    return await handle_resume_upload(db, current_user, file)
