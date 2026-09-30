from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.constants import (
    INSPECTION_STATUS_COMPLETED,
    INSPECTION_STATUS_FAILED,
    INSPECTION_STATUS_PROCESSING,
)
from app.db.models.detection import Detection
from app.db.models.inspection import Inspection
from app.schemas.detection import DetectionResponse
from app.schemas.inspection import (
    InspectionDetailResponse,
    InspectionListResponse,
    InspectionSummaryResponse,
)
from app.services.image_service import validate_and_get_dimensions
from app.services.inference_service import inference_service
from app.services.model_service import model_service
from app.services.storage_service import (
    build_result_path,
    delete_file,
    media_url,
    relative_path,
    save_upload,
)
from app.ml.preprocessing import normalize_exif_orientation


class InspectionService:
    async def create(
        self,
        db: Session,
        upload: UploadFile,
    ) -> InspectionDetailResponse:
        original_filename = upload.filename or "image.jpg"
        saved_path = await save_upload(upload)

        try:
            normalize_exif_orientation(saved_path)
            image_width, image_height = validate_and_get_dimensions(saved_path)

            model_version = model_service.get_or_create_active(db)

            inspection = Inspection(
                original_filename=original_filename,
                stored_filename=saved_path.name,
                original_image_path=relative_path(saved_path),
                status=INSPECTION_STATUS_PROCESSING,
                image_width=image_width,
                image_height=image_height,
                model_version_id=model_version.id,
            )

            db.add(inspection)
            db.commit()
            db.refresh(inspection)

            result_path = build_result_path(saved_path)

            try:
                inference = await inference_service.run(
                    image_path=saved_path,
                    result_path=result_path,
                )

                inspection.result_image_path = relative_path(result_path)
                inspection.total_detections = inference["total_detections"]
                inspection.average_confidence = inference["average_confidence"]
                inspection.processing_time_ms = inference["processing_time_ms"]
                inspection.status = INSPECTION_STATUS_COMPLETED
                inspection.error_message = None

                for item in inference["detections"]:
                    db.add(
                        Detection(
                            inspection_id=inspection.id,
                            **item,
                        )
                    )

                db.commit()

            except Exception as exc:
                db.rollback()

                failed = db.get(Inspection, inspection.id)
                if failed is not None:
                    failed.status = INSPECTION_STATUS_FAILED
                    failed.error_message = str(exc)[:1000]
                    db.commit()

                raise

            stored = self._get_model(db, inspection.id)
            return self._to_detail(stored)

        except Exception:
            # Remove the upload only when validation failed before an inspection
            # record was created. Failed inference inspections are intentionally
            # kept so the dashboard can show their failure state.
            existing = None
            try:
                existing = db.scalar(
                    select(Inspection).where(
                        Inspection.original_image_path == relative_path(saved_path)
                    )
                )
            except Exception:
                db.rollback()

            if existing is None:
                delete_file(relative_path(saved_path))

            raise

    def get(
        self,
        db: Session,
        inspection_id: UUID,
    ) -> InspectionDetailResponse | None:
        inspection = self._get_model(db, inspection_id)
        if inspection is None:
            return None
        return self._to_detail(inspection)

    def list(
        self,
        db: Session,
        limit: int,
        offset: int,
    ) -> InspectionListResponse:
        total = db.scalar(select(func.count()).select_from(Inspection)) or 0

        inspections = db.scalars(
            select(Inspection)
            .options(selectinload(Inspection.model_version))
            .order_by(Inspection.created_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()

        return InspectionListResponse(
            total=total,
            limit=limit,
            offset=offset,
            items=[self._to_summary(item) for item in inspections],
        )

    def delete(
        self,
        db: Session,
        inspection_id: UUID,
    ) -> bool:
        inspection = db.scalar(
            select(Inspection)
            .options(selectinload(Inspection.detections))
            .where(Inspection.id == inspection_id)
        )

        if inspection is None:
            return False

        original_path = inspection.original_image_path
        result_path = inspection.result_image_path

        db.delete(inspection)
        db.commit()

        delete_file(original_path)
        delete_file(result_path)

        return True

    def _get_model(
        self,
        db: Session,
        inspection_id: UUID,
    ) -> Inspection | None:
        return db.scalar(
            select(Inspection)
            .options(
                selectinload(Inspection.detections),
                selectinload(Inspection.model_version),
            )
            .where(Inspection.id == inspection_id)
        )

    def _to_summary(
        self,
        inspection: Inspection,
    ) -> InspectionSummaryResponse:
        return InspectionSummaryResponse(
            id=inspection.id,
            original_filename=inspection.original_filename,
            original_image_url=media_url(
                inspection.original_image_path
            ) or "",
            result_image_url=media_url(
                inspection.result_image_path
            ),
            status=inspection.status,
            total_detections=inspection.total_detections,
            average_confidence=inspection.average_confidence,
            processing_time_ms=inspection.processing_time_ms,
            image_width=inspection.image_width,
            image_height=inspection.image_height,
            model_version=(
                inspection.model_version.version
                if inspection.model_version
                else None
            ),
            created_at=inspection.created_at,
        )

    def _to_detail(
        self,
        inspection: Inspection,
    ) -> InspectionDetailResponse:
        summary = self._to_summary(inspection)

        detections = [
            DetectionResponse.model_validate(item)
            for item in inspection.detections
        ]

        return InspectionDetailResponse(
            **summary.model_dump(),
            detections=detections,
        )


inspection_service = InspectionService()
