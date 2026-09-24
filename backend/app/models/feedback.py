from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    guidance_id: Mapped[int | None] = mapped_column(
        ForeignKey("guidance_history.id"),
        nullable=True
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )