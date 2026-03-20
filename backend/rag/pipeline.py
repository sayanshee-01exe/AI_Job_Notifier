"""
RAG (Retrieval-Augmented Generation) pipeline.

Uses LangChain with OpenAI to answer career-related questions
using retrieved job and resume context.
"""

import logging
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import get_settings
from backend.rag.prompts import select_prompt
from backend.rag.retriever import retrieve_relevant_jobs, format_job_context

logger = logging.getLogger("ai_job_notifier")
settings = get_settings()


async def ask_question(
    question: str,
    user_profile: Dict[str, Any],
    db: AsyncSession,
) -> str:
    """
    Answer a user's career-related question using RAG.

    1. Retrieve relevant jobs from the vector store / database.
    2. Build a prompt with user profile + job context.
    3. Generate an answer using the LLM.
    """
    # Step 1: Retrieve relevant context
    relevant_jobs = await retrieve_relevant_jobs(question, db, top_k=5)
    job_context = format_job_context(relevant_jobs)

    # Step 2: Select and fill prompt template
    prompt_template = select_prompt(question)
    prompt = prompt_template.format(
        role=user_profile.get("role") or "Not specified",
        skills=", ".join(user_profile.get("skills", [])) or "Not specified",
        experience=user_profile.get("experience", "Not specified") or "Not specified",
        education=", ".join(user_profile.get("education", [])) or "Not specified",
        preferred_location=user_profile.get("preferred_location") or "Not specified",
        job_context=job_context,
        question=question,
    )

    # Step 3: Generate answer using LLM
    try:
        answer = await _generate_with_llm(prompt)
    except Exception as e:
        logger.error("LLM generation failed: %s", str(e))
        answer = _generate_fallback_answer(question, user_profile, relevant_jobs)

    return answer


async def _generate_with_llm(prompt: str) -> str:
    """Generate an answer using Anthropic Claude via LangChain."""
    if not settings.ANTHROPIC_API_KEY:
        raise ValueError("Anthropic API key not configured")

    from langchain_anthropic import ChatAnthropic
    from langchain_core.messages import HumanMessage

    llm = ChatAnthropic(
        model_name="claude-3-opus-20240229",
        temperature=0.7,
        anthropic_api_key=settings.ANTHROPIC_API_KEY,
    )

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content

def _generate_fallback_answer(
    question: str,
    user_profile: Dict[str, Any],
    relevant_jobs: list,
) -> str:
    """Generate a basic answer without LLM when API key is missing or call fails."""
    skills = user_profile.get("skills", [])
    job_count = len(relevant_jobs)

    answer_parts = [
        f"Based on your profile with {len(skills)} skills and {job_count} relevant job listings found:\n"
    ]

    if relevant_jobs:
        answer_parts.append("**Relevant Jobs:**")
        for job in relevant_jobs[:3]:
            matching_skills = set(s.lower() for s in skills) & set(
                s.lower() for s in job.get("skills_required", [])
            )
            answer_parts.append(
                f"- **{job['title']}** at {job['company']} "
                f"({len(matching_skills)} skill matches)"
            )

    answer_parts.append(
        "\n*Note: For more detailed AI-powered analysis, please configure the Anthropic API key.*"
    )

    return "\n".join(answer_parts)
