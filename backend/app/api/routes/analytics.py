from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import (
    AnalyticsSummaryResponse,
    DamageDistributionResponse,
)
from app.services.analytics_service import analytics_service


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def summary(db: Session = Depends(get_db)):
    return analytics_service.summary(db)


@router.get(
    "/damage-distribution",
    response_model=DamageDistributionResponse,
)
def damage_distribution(db: Session = Depends(get_db)):
    return analytics_service.damage_distribution(db)
