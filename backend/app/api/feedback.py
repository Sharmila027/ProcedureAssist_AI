from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.feedback import Feedback


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


class FeedbackRequest(BaseModel):
    guidance_id: int
    rating: int = Field(
        ge=1,
        le=5
    )
    comment: str | None = None
    language: str = "en"


@router.post("/")
async def submit_feedback(
    request: FeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    feedback = Feedback(
        guidance_id=request.guidance_id,
        rating=request.rating,
        comment=request.comment,
        language=request.language
    )

    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.id,
        "rating": feedback.rating
    }