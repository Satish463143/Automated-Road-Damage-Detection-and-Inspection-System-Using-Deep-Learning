from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    inspection_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("inspections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    damage_name: Mapped[str] = mapped_column(String(100), nullable=False)

    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    x1: Mapped[float] = mapped_column(Float, nullable=False)
    y1: Mapped[float] = mapped_column(Float, nullable=False)
    x2: Mapped[float] = mapped_column(Float, nullable=False)
    y2: Mapped[float] = mapped_column(Float, nullable=False)

    bounding_box_width: Mapped[float] = mapped_column(Float, nullable=False)
    bounding_box_height: Mapped[float] = mapped_column(Float, nullable=False)
    bounding_box_area: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    inspection = relationship(
        "Inspection",
        back_populates="detections",
    )
