from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    class_id: int
    damage_code: str
    damage_name: str
    confidence: float

    x1: float
    y1: float
    x2: float
    y2: float

    bounding_box_width: float
    bounding_box_height: float
    bounding_box_area: float

    created_at: datetime
