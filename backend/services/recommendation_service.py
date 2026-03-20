"""
Recommendation service: orchestrates the matching engine for personalized job recommendations.
"""

import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from backend.matching.matcher import rank_jobs_for_user
from backend.models.user import User
from backend.schemas.job import JobMatch
from backend.services.job_service import get_all_jobs_raw

logger = logging.getLogger("ai_job_notifier")


async def get_recommendations(
    db: AsyncSession, user: User, top_k: int = 10
) -> List[JobMatch]:
    """Get top-k job recommendations for a user based on their profile."""
    if not user.skills and not user.experience:
        logger.warning("User %s has no profile data. Returning empty recommendations.", user.id)
        return []

    # Fetch user interactions
    from backend.models.user import UserInteraction
    from sqlalchemy import select
    res = await db.execute(select(UserInteraction).where(UserInteraction.user_id == user.id))
    interactions = res.scalars().all()
    ignore_job_ids = {i.job_id for i in interactions if i.action in ("skip", "apply")}

    # Fetch all jobs
    jobs = await get_all_jobs_raw(db)
    if not jobs:
        return []

    # Filter out ignored jobs
    if ignore_job_ids:
        jobs = [j for j in jobs if j.id not in ignore_job_ids]

    # Build user profile dict
    user_profile = {
        "skills": user.skills or [],
        "experience": user.experience or "",
        "education": user.education or [],
    }

    # Run matching engine
    ranked_matches = rank_jobs_for_user(user_profile, jobs, top_k=top_k)

    return ranked_matches
