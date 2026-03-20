"""
Job matching engine: combines multiple scores into a final ranking.

Final score = 0.5 * semantic_similarity + 0.3 * skill_match + 0.2 * experience_match
"""

import logging
from typing import Any, Dict, List

from backend.matching.scorers import (
    calculate_skill_match,
    calculate_semantic_similarity,
    calculate_experience_match,
    calculate_recency_score,
)
from backend.schemas.job import JobMatch, JobResponse

logger = logging.getLogger("ai_job_notifier")

# ── Scoring Weights ───────────────────────────────────────
WEIGHT_SIMILARITY = 0.5
WEIGHT_SKILL = 0.3
WEIGHT_RECENCY = 0.2


def compute_match_score(user_profile: Dict[str, Any], job) -> JobMatch:
    """
    Compute a composite match score between a user profile and a job.

    Args:
        user_profile: Dict with 'skills', 'experience', 'education' keys.
        job: SQLAlchemy Job model instance.

    Returns:
        JobMatch with individual and combined scores.
    """
    # Build user text for semantic comparison
    user_text = " ".join([
        " ".join(user_profile.get("skills", [])),
        user_profile.get("experience", ""),
        " ".join(user_profile.get("education", [])),
    ]).strip()

    # Build job text
    job_text = f"{job.title} {job.description} {' '.join(job.skills_required or [])}"

    # Calculate individual scores
    similarity_score = calculate_semantic_similarity(user_text, job_text)
    skill_score = calculate_skill_match(
        user_profile.get("skills", []),
        job.skills_required or [],
    )
    recency_score = calculate_recency_score(job.created_at)

    # Weighted combination
    final_score = (
        WEIGHT_SIMILARITY * similarity_score
        + WEIGHT_SKILL * skill_score
        + WEIGHT_RECENCY * recency_score
    )

    return JobMatch(
        job=JobResponse.model_validate(job),
        match_score=round(final_score, 4),
        skill_match_score=round(skill_score, 4),
        similarity_score=round(similarity_score, 4),
        recency_score=round(recency_score, 4),
    )


def rank_jobs_for_user(
    user_profile: Dict[str, Any],
    jobs: list,
    top_k: int = 10,
) -> List[JobMatch]:
    """
    Rank all jobs for a user and return the top-k matches.

    Args:
        user_profile: Dict with 'skills', 'experience', 'education'.
        jobs: List of SQLAlchemy Job model instances.
        top_k: Number of top matches to return.

    Returns:
        Sorted list of JobMatch objects (highest score first).
    """
    logger.info("Computing matches for %d jobs", len(jobs))

    matches = [compute_match_score(user_profile, job) for job in jobs]
    matches.sort(key=lambda m: m.match_score, reverse=True)

    return matches[:top_k]
