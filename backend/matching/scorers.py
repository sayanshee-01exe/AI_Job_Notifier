"""
Individual scoring functions for job matching.
"""

import re
from typing import List, Set
from datetime import datetime, timezone

import numpy as np

from backend.vectorstore.embeddings import create_embedding


def calculate_skill_match(user_skills: List[str], job_skills: List[str]) -> float:
    """
    Calculate skill overlap score between user and job.

    Returns:
        Float between 0.0 and 1.0 representing the proportion of required
        skills that the user possesses.
    """
    if not job_skills:
        return 1.0  # No specific skills required = perfect match
    if not user_skills:
        return 0.0

    user_set: Set[str] = {s.lower().strip() for s in user_skills}
    job_set: Set[str] = {s.lower().strip() for s in job_skills}

    overlap = user_set & job_set
    return len(overlap) / len(job_set)


def calculate_semantic_similarity(user_text: str, job_text: str) -> float:
    """
    Calculate semantic similarity between user profile text and job description
    using sentence embeddings and cosine similarity.

    Returns:
        Float between 0.0 and 1.0.
    """
    if not user_text or not job_text:
        return 0.0

    try:
        user_embedding = create_embedding(user_text)
        job_embedding = create_embedding(job_text)

        # Cosine similarity (vectors are already normalized)
        similarity = float(np.dot(user_embedding, job_embedding))
        return max(0.0, min(1.0, similarity))
    except Exception:
        return 0.0


def calculate_experience_match(user_experience: str, job_experience_level: str) -> float:
    """
    Calculate experience match score.

    Extracts years of experience from user text and compares against
    job experience level requirements.

    Returns:
        Float between 0.0 and 1.0.
    """
    if not job_experience_level:
        return 1.0  # No specific level required

    # Extract years from user experience text
    user_years = _extract_years(user_experience)

    # Map job levels to expected year ranges
    level_map = {
        "intern": (0, 1),
        "entry": (0, 2),
        "junior": (0, 3),
        "mid": (2, 6),
        "mid-level": (2, 6),
        "senior": (5, 15),
        "lead": (7, 20),
        "principal": (10, 25),
        "staff": (8, 20),
        "director": (10, 30),
    }

    level_key = job_experience_level.lower().strip()
    if level_key in level_map:
        min_years, max_years = level_map[level_key]
        if user_years is None:
            return 0.5  # Unknown experience = neutral score
        if min_years <= user_years <= max_years:
            return 1.0
        elif user_years < min_years:
            return max(0.0, 1.0 - (min_years - user_years) * 0.2)
        else:
            return max(0.5, 1.0 - (user_years - max_years) * 0.05)

    return 0.5  # Unknown level = neutral


def calculate_recency_score(job_created_at: datetime) -> float:
    """Calculate recency score (1.0 for new, decaying over time)."""
    if not job_created_at:
        return 0.5
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    age_days = (now - job_created_at).days
    if age_days <= 1:
        return 1.0
    elif age_days <= 7:
        return 0.8
    elif age_days <= 14:
        return 0.6
    elif age_days <= 30:
        return 0.4
    else:
        return 0.2


def _extract_years(text: str) -> int | None:
    """Extract years of experience from text."""
    if not text:
        return None

    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # Count job entries (rough heuristic: each entry ≈ 2 years)
    job_indicators = len(re.findall(
        r'(?:20\d{2}|19\d{2})\s*[-–—]\s*(?:20\d{2}|19\d{2}|present|current)',
        text, re.IGNORECASE
    ))
    if job_indicators > 0:
        return job_indicators * 2

    return None
