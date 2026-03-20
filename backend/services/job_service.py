"""
Job service: CRUD operations for job listings.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import NotFoundException
from backend.models.job import Job
from backend.schemas.job import JobCreate, JobResponse


async def create_job(db: AsyncSession, job_data: JobCreate) -> JobResponse:
    """Create a new job listing."""
    job = Job(**job_data.model_dump())
    db.add(job)
    await db.flush()
    await db.refresh(job)
    return JobResponse.model_validate(job)


async def get_jobs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    location: Optional[str] = None,
    role: Optional[str] = None,
    experience_level: Optional[str] = None,
    posted_within_hours: Optional[int] = None,
) -> List[JobResponse]:
    """Get job listings with optional filters."""
    query = select(Job)

    if location:
        query = query.where(Job.location.ilike(f"%{location}%"))
    if role:
        query = query.where(Job.title.ilike(f"%{role}%"))
    if experience_level:
        query = query.where(Job.experience_level == experience_level)
    if posted_within_hours is not None:
        time_threshold = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=posted_within_hours)
        query = query.where(Job.created_at >= time_threshold)

    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    result = await db.execute(query)
    jobs = result.scalars().all()

    return [JobResponse.model_validate(job) for job in jobs]


async def get_job_by_id(db: AsyncSession, job_id: int) -> JobResponse:
    """Get a single job by ID."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise NotFoundException("Job")
    return JobResponse.model_validate(job)


async def get_all_jobs_raw(db: AsyncSession) -> List[Job]:
    """Get all job ORM objects (used internally by matching engine)."""
    result = await db.execute(select(Job))
    return list(result.scalars().all())
