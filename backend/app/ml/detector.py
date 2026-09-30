from pathlib import Path
from threading import Lock

import cv2
from ultralytics import YOLO

from app.core.config import settings
from app.ml.postprocessing import normalize_detection


class RoadDamageDetector:
    def __init__(self):
        self._model = None
        self._lock = Lock()

    def load(self) -> None:
        with self._lock:
            if self._model is not None:
                return

            if not settings.model_path.exists():
                raise FileNotFoundError(
                    f"Model weights were not found at: {settings.model_path}"
                )

            self._model = YOLO(str(settings.model_path))

    def is_available(self) -> bool:
        try:
            self.load()
            return True
        except Exception:
            return False

    def predict_and_save(
        self,
        image_path: Path,
        result_path: Path,
    ) -> list[dict]:
        self.load()

        results = self._model.predict(
            source=str(image_path),
            conf=settings.confidence_threshold,
            imgsz=settings.model_image_size,
            verbose=False,
        )

        if not results:
            raise RuntimeError("The model returned no inference result.")

        result = results[0]
        detections: list[dict] = []

        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())
                xyxy = [float(v) for v in box.xyxy[0].tolist()]

                detections.append(
                    normalize_detection(
                        class_id=class_id,
                        confidence=confidence,
                        xyxy=xyxy,
                    )
                )

        annotated = result.plot()
        result_path.parent.mkdir(parents=True, exist_ok=True)

        if not cv2.imwrite(str(result_path), annotated):
            raise RuntimeError("Failed to save the annotated result image.")

        return detections


detector = RoadDamageDetector()
