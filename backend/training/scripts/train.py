import argparse
from pathlib import Path

from ultralytics import YOLO


def train(
    data_yaml: Path,
    base_model: str,
    epochs: int,
    image_size: int,
    batch_size: int,
    project: str,
    name: str,
):
    model = YOLO(base_model)

    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=image_size,
        batch=batch_size,
        project=project,
        name=name,
        patience=15,
        pretrained=True,
        seed=42,
        plots=True,
    )

    print("Training finished.")
    print("Best weights are inside the run's weights/best.pt file.")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("training/configs/road_damage.yaml"),
    )
    parser.add_argument("--model", default="yolov8n.pt")
    parser.add_argument("--epochs", type=int, default=75)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--project", default="results/training")
    parser.add_argument("--name", default="road_damage_yolov8n")
    args = parser.parse_args()

    train(
        data_yaml=args.data,
        base_model=args.model,
        epochs=args.epochs,
        image_size=args.imgsz,
        batch_size=args.batch,
        project=args.project,
        name=args.name,
    )
