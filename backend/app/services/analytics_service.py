from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.constants import (
    INSPECTION_STATUS_COMPLETED,
    INSPECTION_STATUS_FAILED,
)
from app.db.models.detection import Detection
from app.db.models.inspection import Inspection
from app.schemas.analytics import (
    AnalyticsSummaryResponse,
    DamageCount,
    DamageDistributionResponse,
)


class AnalyticsService:
    def _distribution(self, db: Session) -> list[DamageCount]:
        rows = db.execute(
            select(
                Detection.damage_code,
                Detection.damage_name,
                func.count(Detection.id),
            )
            .group_by(
                Detection.damage_code,
                Detection.damage_name,
            )
            .order_by(Detection.damage_code)
        ).all()

        return [
            DamageCount(
                damage_code=code,
                damage_name=name,
                count=count,
            )
            for code, name, count in rows
        ]

    def summary(self, db: Session) -> AnalyticsSummaryResponse:
        total_inspections = (
            db.scalar(select(func.count()).select_from(Inspection)) or 0
        )

        completed = (
            db.scalar(
                select(func.count())
                .select_from(Inspection)
                .where(Inspection.status == INSPECTION_STATUS_COMPLETED)
            )
            or 0
        )

        failed = (
            db.scalar(
                select(func.count())
                .select_from(Inspection)
                .where(Inspection.status == INSPECTION_STATUS_FAILED)
            )
            or 0
        )

        total_detections = (
            db.scalar(select(func.count()).select_from(Detection)) or 0
        )

        average_confidence = db.scalar(
            select(func.avg(Detection.confidence))
        )

        return AnalyticsSummaryResponse(
            total_inspections=total_inspections,
            completed_inspections=completed,
            failed_inspections=failed,
            total_detections=total_detections,
            average_confidence=(
                float(average_confidence)
                if average_confidence is not None
                else None
            ),
            damage_distribution=self._distribution(db),
        )

    def damage_distribution(
        self,
        db: Session,
    ) -> DamageDistributionResponse:
        return DamageDistributionResponse(
            items=self._distribution(db)
        )


analytics_service = AnalyticsService()
