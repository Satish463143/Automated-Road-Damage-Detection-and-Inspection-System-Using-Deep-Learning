import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


CLASS_TO_ID = {
    "D00": 0,
    "D10": 1,
    "D20": 2,
    "D40": 3,
}

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


def find_image(images_dir: Path, stem: str) -> Path | None:
    for extension in IMAGE_EXTENSIONS:
        direct = images_dir / f"{stem}{extension}"
        if direct.exists():
            return direct

    matches = [
        path
        for path in images_dir.rglob(f"{stem}.*")
        if path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return matches[0] if matches else None


def voc_box_to_yolo(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    image_width: int,
    image_height: int,
) -> tuple[float, float, float, float]:
    x_center = ((xmin + xmax) / 2.0) / image_width
    y_center = ((ymin + ymax) / 2.0) / image_height
    width = (xmax - xmin) / image_width
    height = (ymax - ymin) / image_height

    return x_center, y_center, width, height


def convert(
    images_dir: Path,
    annotations_dir: Path,
    output_images: Path,
    output_labels: Path,
) -> None:
    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    for xml_path in annotations_dir.rglob("*.xml"):
        image_path = find_image(images_dir, xml_path.stem)

        if image_path is None:
            print(f"Missing image: {xml_path.stem}")
            skipped += 1
            continue

        root = ET.parse(xml_path).getroot()

        size = root.find("size")
        image_width = int(size.findtext("width", default="0"))
        image_height = int(size.findtext("height", default="0"))

        if image_width <= 0 or image_height <= 0:
            print(f"Invalid image size: {xml_path}")
            skipped += 1
            continue

        label_lines = []

        for obj in root.findall("object"):
            class_name = obj.findtext("name", default="").strip()

            if class_name not in CLASS_TO_ID:
                continue

            bbox = obj.find("bndbox")
            xmin = float(bbox.findtext("xmin"))
            ymin = float(bbox.findtext("ymin"))
            xmax = float(bbox.findtext("xmax"))
            ymax = float(bbox.findtext("ymax"))

            x, y, w, h = voc_box_to_yolo(
                xmin,
                ymin,
                xmax,
                ymax,
                image_width,
                image_height,
            )

            label_lines.append(
                f"{CLASS_TO_ID[class_name]} "
                f"{x:.6f} {y:.6f} {w:.6f} {h:.6f}"
            )

        destination_image = output_images / image_path.name
        destination_label = output_labels / f"{image_path.stem}.txt"

        shutil.copy2(image_path, destination_image)
        destination_label.write_text(
            "\n".join(label_lines),
            encoding="utf-8",
        )

        converted += 1

    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--annotations-dir", required=True, type=Path)
    parser.add_argument("--output-images", required=True, type=Path)
    parser.add_argument("--output-labels", required=True, type=Path)
    args = parser.parse_args()

    convert(
        images_dir=args.images_dir,
        annotations_dir=args.annotations_dir,
        output_images=args.output_images,
        output_labels=args.output_labels,
    )
