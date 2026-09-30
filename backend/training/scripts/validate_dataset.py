import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


VALID_CLASSES = {"D00", "D10", "D20", "D40"}
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


def find_image(images_dir: Path, stem: str) -> Path | None:
    for extension in IMAGE_EXTENSIONS:
        candidate = images_dir / f"{stem}{extension}"
        if candidate.exists():
            return candidate

    matches = [
        path
        for path in images_dir.rglob(f"{stem}.*")
        if path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return matches[0] if matches else None


def validate(images_dir: Path, annotations_dir: Path) -> None:
    errors = []
    checked = 0

    for xml_path in annotations_dir.rglob("*.xml"):
        checked += 1
        image_path = find_image(images_dir, xml_path.stem)

        if image_path is None:
            errors.append(f"Missing image for {xml_path}")
            continue

        try:
            with Image.open(image_path) as image:
                width, height = image.size
                image.verify()
        except Exception as exc:
            errors.append(f"Corrupt image {image_path}: {exc}")
            continue

        try:
            root = ET.parse(xml_path).getroot()
        except Exception as exc:
            errors.append(f"Invalid XML {xml_path}: {exc}")
            continue

        for obj in root.findall("object"):
            class_name = obj.findtext("name", default="").strip()

            if class_name not in VALID_CLASSES:
                continue

            bbox = obj.find("bndbox")

            try:
                xmin = float(bbox.findtext("xmin"))
                ymin = float(bbox.findtext("ymin"))
                xmax = float(bbox.findtext("xmax"))
                ymax = float(bbox.findtext("ymax"))
            except Exception:
                errors.append(f"Invalid bbox values in {xml_path}")
                continue

            if xmin >= xmax or ymin >= ymax:
                errors.append(f"Invalid bbox ordering in {xml_path}")

            if xmin < 0 or ymin < 0 or xmax > width or ymax > height:
                errors.append(f"Bbox outside image in {xml_path}")

    print(f"Annotation files checked: {checked}")
    print(f"Errors found: {len(errors)}")

    for error in errors[:100]:
        print("-", error)

    if len(errors) > 100:
        print(f"... plus {len(errors) - 100} more errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--annotations-dir", required=True, type=Path)
    args = parser.parse_args()

    validate(args.images_dir, args.annotations_dir)
