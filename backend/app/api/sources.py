from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.government_source import GovernmentSource


router = APIRouter(
    prefix="/sources",
    tags=["Government Sources"]
)


class SourceRequest(BaseModel):
    source_name: str
    url: str
    department: str | None = None
    source_type: str | None = None


@router.post("/")
async def add_source(
    request: SourceRequest,
    db: AsyncSession = Depends(get_db)
):
    source = GovernmentSource(
        source_name=request.source_name,
        url=request.url,
        department=request.department,
        source_type=request.source_type
    )

    db.add(source)
    await db.commit()
    await db.refresh(source)

    return {
        "message": "Government source added successfully",
        "source_id": source.id,
        "source_name": source.source_name,
        "url": source.url
    }