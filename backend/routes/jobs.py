"""
Job listing routes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db
from backend.schemas.job import JobCreate, JobResponse
from backend.services.job_service import get_jobs, get_job_by_id, create_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    location: Optional[str] = None,
    role: Optional[str] = None,
    experience_level: Optional[str] = None,
    posted_within_hours: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all jobs with optional filters."""
    return await get_jobs(
        db, 
        skip=skip, 
        limit=limit, 
        location=location, 
        role=role, 
        experience_level=experience_level,
        posted_within_hours=posted_within_hours
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single job by ID."""
    return await get_job_by_id(db, job_id)


@router.post("/", response_model=JobResponse, status_code=201)
async def add_job(job_data: JobCreate, db: AsyncSession = Depends(get_db)):
    """Create a new job listing (for scrapers/admin)."""
    return await create_job(db, job_data)
