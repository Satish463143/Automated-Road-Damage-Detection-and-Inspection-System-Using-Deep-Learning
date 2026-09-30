from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.detection import DetectionResponse


class InspectionSummaryResponse(BaseModel):
    id: UUID
    original_filename: str
    original_image_url: str
    result_image_url: str | None

    status: str
    total_detections: int
    average_confidence: float | None
    processing_time_ms: float | None

    image_width: int
    image_height: int

    model_version: str | None
    created_at: datetime


class InspectionDetailResponse(InspectionSummaryResponse):
    detections: list[DetectionResponse]


class InspectionListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[InspectionSummaryResponse]
