"""
Custom retriever for fetching relevant jobs and resume data from the vector store.
"""

import logging
from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.job import Job
from backend.vectorstore.embeddings import create_embedding
from backend.vectorstore.store import get_vector_store

logger = logging.getLogger("ai_job_notifier")


async def retrieve_relevant_jobs(
    query: str,
    db: AsyncSession,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant jobs for a given query using vector similarity.

    Falls back to keyword search if vector store is empty.
    """
    store = get_vector_store()

    if store.size > 0:
        # Vector-based retrieval
        query_embedding = create_embedding(query)
        results = store.search_similar(query_embedding, top_k=top_k)

        job_ids = [ext_id for ext_id, score in results]
        if job_ids:
            result = await db.execute(select(Job).where(Job.id.in_(job_ids)))
            jobs = result.scalars().all()
            return [_job_to_context(job) for job in jobs]

    # Fallback: keyword-based retrieval
    logger.info("Vector store empty, falling back to keyword search")
    query_words = query.lower().split()
    result = await db.execute(select(Job).limit(top_k * 2))
    jobs = list(result.scalars().all())

    # Simple relevance scoring by keyword overlap
    scored = []
    for job in jobs:
        job_text = f"{job.title} {job.description} {' '.join(job.skills_required or [])}".lower()
        score = sum(1 for w in query_words if w in job_text)
        scored.append((score, job))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [_job_to_context(job) for _, job in scored[:top_k]]


def _job_to_context(job: Job) -> Dict[str, Any]:
    """Convert a Job model to a context dict for the prompt."""
    return {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description[:500],  # Truncate for context window
        "skills_required": job.skills_required or [],
        "experience_level": job.experience_level or "Not specified",
    }


def format_job_context(jobs: List[Dict[str, Any]]) -> str:
    """Format job data into a string for the prompt template."""
    if not jobs:
        return "No relevant job listings found."

    parts = []
    for i, job in enumerate(jobs, 1):
        parts.append(
            f"### Job {i}: {job['title']} at {job['company']}\n"
            f"- **Location**: {job['location']}\n"
            f"- **Experience**: {job['experience_level']}\n"
            f"- **Required Skills**: {', '.join(job['skills_required'])}\n"
            f"- **Description**: {job['description']}\n"
        )
    return "\n".join(parts)
