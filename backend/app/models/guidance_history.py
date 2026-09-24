from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GuidanceHistory(Base):
    __tablename__ = "guidance_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    query_id: Mapped[int | None] = mapped_column(
        ForeignKey("query_history.id"),
        nullable=True
    )

    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    procedure: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    guidance: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )