from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GovernmentSource(Base):
    __tablename__ = "government_sources"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    source_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    department: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    source_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    last_updated: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )