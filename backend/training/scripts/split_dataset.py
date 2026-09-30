import argparse
import random
import shutil
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def copy_pair(
    image_path: Path,
    labels_dir: Path,
    destination_images: Path,
    destination_labels: Path,
) -> None:
    destination_images.mkdir(parents=True, exist_ok=True)
    destination_labels.mkdir(parents=True, exist_ok=True)

    label_path = labels_dir / f"{image_path.stem}.txt"

    shutil.copy2(image_path, destination_images / image_path.name)

    if label_path.exists():
        shutil.copy2(label_path, destination_labels / label_path.name)
    else:
        (destination_labels / f"{image_path.stem}.txt").write_text(
            "",
            encoding="utf-8",
        )


def split(
    images_dir: Path,
    labels_dir: Path,
    output_dir: Path,
    train_ratio: float,
    val_ratio: float,
    seed: int,
) -> None:
    images = [
        path
        for path in images_dir.iterdir()
        if path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    random.Random(seed).shuffle(images)

    total = len(images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:],
    }

    for split_name, split_images in splits.items():
        for image_path in split_images:
            copy_pair(
                image_path=image_path,
                labels_dir=labels_dir,
                destination_images=output_dir / "images" / split_name,
                destination_labels=output_dir / "labels" / split_name,
            )

        print(f"{split_name}: {len(split_images)} images")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--labels-dir", required=True, type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
    )
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.train_ratio + args.val_ratio >= 1:
        raise ValueError("train-ratio + val-ratio must be below 1.")

    split(
        images_dir=args.images_dir,
        labels_dir=args.labels_dir,
        output_dir=args.output_dir,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )
