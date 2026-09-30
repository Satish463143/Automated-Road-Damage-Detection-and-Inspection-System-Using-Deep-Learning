from app.core.constants import DAMAGE_CLASS_MAP


def normalize_detection(
    class_id: int,
    confidence: float,
    xyxy: list[float],
) -> dict:
    x1, y1, x2, y2 = xyxy

    width = max(0.0, x2 - x1)
    height = max(0.0, y2 - y1)

    class_info = DAMAGE_CLASS_MAP.get(
        class_id,
        {
            "code": f"CLASS_{class_id}",
            "name": f"Class {class_id}",
        },
    )

    return {
        "class_id": class_id,
        "damage_code": class_info["code"],
        "damage_name": class_info["name"],
        "confidence": confidence,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "bounding_box_width": width,
        "bounding_box_height": height,
        "bounding_box_area": width * height,
    }
