from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DocumentVerification(Base):
    __tablename__ = "document_verifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    verification_result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    missing_information: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    verified_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )