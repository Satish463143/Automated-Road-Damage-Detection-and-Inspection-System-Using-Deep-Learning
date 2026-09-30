from pydantic import BaseModel


class DamageCount(BaseModel):
    damage_code: str
    damage_name: str
    count: int


class AnalyticsSummaryResponse(BaseModel):
    total_inspections: int
    completed_inspections: int
    failed_inspections: int
    total_detections: int
    average_confidence: float | None
    damage_distribution: list[DamageCount]


class DamageDistributionResponse(BaseModel):
    items: list[DamageCount]
