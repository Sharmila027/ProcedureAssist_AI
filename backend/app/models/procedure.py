from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Procedure(Base):
    __tablename__ = "procedures"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    service_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    department: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    sla_days: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    can_required: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True
    )

    validity: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    file_rules: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    target_demographic: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    govt_fee: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    esevai_fee: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    access_sources: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    tracker_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    first_appellate_authority: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    workflow: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )