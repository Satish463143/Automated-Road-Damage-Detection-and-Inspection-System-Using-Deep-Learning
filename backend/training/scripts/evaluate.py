import argparse
import json
from pathlib import Path

from ultralytics import YOLO


def evaluate(
    weights: Path,
    data_yaml: Path,
    image_size: int,
    output_json: Path,
) -> None:
    model = YOLO(str(weights))

    metrics = model.val(
        data=str(data_yaml),
        split="test",
        imgsz=image_size,
        plots=True,
    )

    result = {
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2))
    print(f"Saved metrics to: {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights",
        type=Path,
        default=Path("models/weights/best.pt"),
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("training/configs/road_damage.yaml"),
    )
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/evaluation/metrics.json"),
    )
    args = parser.parse_args()

    evaluate(
        weights=args.weights,
        data_yaml=args.data,
        image_size=args.imgsz,
        output_json=args.output,
    )
