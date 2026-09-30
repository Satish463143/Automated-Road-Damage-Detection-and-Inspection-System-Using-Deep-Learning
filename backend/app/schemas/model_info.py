from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ModelInfoResponse(BaseModel):
    id: UUID
    model_name: str
    architecture: str
    version: str
    training_dataset: str
    image_size: int
    precision: float | None
    recall: float | None
    map50: float | None
    map50_95: float | None
    is_active: bool
    training_date: datetime | None
    classes: list[dict[str, str]]
