"""
Resume service: file handling and NLP parsing integration.
"""

import os
import logging
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import get_settings
from backend.core.exceptions import ValidationException
from backend.models.user import User
from backend.nlp.parser import parse_resume
from backend.schemas.resume import ResumeData, ResumeUploadResponse

logger = logging.getLogger("ai_job_notifier")
settings = get_settings()

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


async def handle_resume_upload(
    db: AsyncSession, user: User, file: UploadFile
) -> ResumeUploadResponse:
    """Save uploaded resume, parse it with NLP, and update user profile."""

    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationException(f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXTENSIONS}")

    # Ensure upload directory exists
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    filename = f"user_{user.id}_{file.filename}"
    file_path = upload_dir / filename
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    logger.info("Saved resume for user %s: %s", user.id, file_path)

    # Parse resume with NLP
    parsed_data: ResumeData = parse_resume(str(file_path))

    # Update user profile
    user.skills = parsed_data.skills
    user.experience = parsed_data.experience
    user.education = parsed_data.education
    user.resume_path = str(file_path)
    db.add(user)
    await db.flush()

    return ResumeUploadResponse(
        message="Resume uploaded and parsed successfully",
        filename=filename,
        parsed_data=parsed_data,
    )
