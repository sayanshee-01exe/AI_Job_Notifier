"""
Recommendation routes: personalized job matching + RAG queries.
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.schemas.job import JobMatch
from backend.services.recommendation_service import get_recommendations
from backend.rag.pipeline import ask_question

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/", response_model=list[JobMatch])
async def recommendations(
    top_k: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get personalized job recommendations based on your profile."""
    return await get_recommendations(db, current_user, top_k=top_k)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    answer: str


@router.post("/ask", response_model=AskResponse)
async def ask(
    request: AskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ask an AI-powered question about your job fit or resume."""
    user_profile = {
        "skills": current_user.skills or [],
        "experience": current_user.experience or "",
        "education": current_user.education or [],
    }
    answer = await ask_question(request.question, user_profile, db)
    return AskResponse(question=request.question, answer=answer)


class InteractionRequest(BaseModel):
    job_id: int
    action: str

@router.post("/interact")
async def interact(
    request: InteractionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record user interaction (click, apply, skip) for feedback loop."""
    from backend.models.user import UserInteraction
    interaction = UserInteraction(
        user_id=current_user.id,
        job_id=request.job_id,
        action=request.action
    )
    db.add(interaction)
    await db.commit()
    return {"status": "success", "message": f"Recorded {request.action}"}
