from pathlib import Path
from time import perf_counter

from starlette.concurrency import run_in_threadpool

from app.ml.detector import detector


class ModelUnavailableError(RuntimeError):
    pass


class InferenceService:
    async def run(
        self,
        image_path: Path,
        result_path: Path,
    ) -> dict:
        if not detector.is_available():
            raise ModelUnavailableError(
                "The trained model is not available. "
                "Place best.pt in models/weights/best.pt first."
            )

        started = perf_counter()

        detections = await run_in_threadpool(
            detector.predict_and_save,
            image_path,
            result_path,
        )

        processing_time_ms = (perf_counter() - started) * 1000

        average_confidence = None
        if detections:
            average_confidence = sum(
                item["confidence"] for item in detections
            ) / len(detections)

        return {
            "detections": detections,
            "total_detections": len(detections),
            "average_confidence": average_confidence,
            "processing_time_ms": processing_time_ms,
        }


inference_service = InferenceService()
