import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import DAMAGE_CLASS_MAP
from app.db.models.model_version import ModelVersion
from app.schemas.model_info import ModelInfoResponse
from app.services.storage_service import relative_path


class ModelService:
    def _read_metadata(self) -> dict:
        if not settings.model_metadata_path.exists():
            return {
                "model_name": "Road Damage Detector",
                "architecture": "YOLO",
                "version": "v1.0",
                "training_dataset": "RDD2022",
                "image_size": settings.model_image_size,
                "precision": None,
                "recall": None,
                "map50": None,
                "map50_95": None,
                "training_date": None,
            }

        with settings.model_metadata_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_or_create_active(self, db: Session) -> ModelVersion:
        metadata = self._read_metadata()
        version = metadata.get("version", "v1.0")

        existing = db.scalar(
            select(ModelVersion).where(ModelVersion.version == version)
        )
        if existing:
            if not existing.is_active:
                db.execute(update(ModelVersion).values(is_active=False))
                existing.is_active = True
                db.commit()
                db.refresh(existing)
            return existing

        db.execute(update(ModelVersion).values(is_active=False))

        training_date = metadata.get("training_date")
        parsed_training_date = None
        if training_date:
            parsed_training_date = datetime.fromisoformat(
                training_date.replace("Z", "+00:00")
            )

        model = ModelVersion(
            model_name=metadata.get("model_name", "Road Damage Detector"),
            architecture=metadata.get("architecture", "YOLO"),
            version=version,
            weights_path=relative_path(settings.model_path),
            training_dataset=metadata.get("training_dataset", "RDD2022"),
            image_size=int(
                metadata.get("image_size", settings.model_image_size)
            ),
            precision=metadata.get("precision"),
            recall=metadata.get("recall"),
            map50=metadata.get("map50"),
            map50_95=metadata.get("map50_95"),
            is_active=True,
            training_date=parsed_training_date,
        )

        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    def get_active(self, db: Session) -> ModelVersion | None:
        model = db.scalar(
            select(ModelVersion)
            .where(ModelVersion.is_active.is_(True))
            .order_by(ModelVersion.created_at.desc())
        )

        if model is None:
            model = self.get_or_create_active(db)

        return model

    def to_response(self, model: ModelVersion) -> ModelInfoResponse:
        classes = [
            {
                "code": info["code"],
                "name": info["name"],
            }
            for _, info in sorted(DAMAGE_CLASS_MAP.items())
        ]

        return ModelInfoResponse(
            id=model.id,
            model_name=model.model_name,
            architecture=model.architecture,
            version=model.version,
            training_dataset=model.training_dataset,
            image_size=model.image_size,
            precision=model.precision,
            recall=model.recall,
            map50=model.map50,
            map50_95=model.map50_95,
            is_active=model.is_active,
            training_date=model.training_date,
            classes=classes,
        )


model_service = ModelService()
