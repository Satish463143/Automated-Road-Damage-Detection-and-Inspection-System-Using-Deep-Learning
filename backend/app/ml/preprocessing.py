from pathlib import Path

from PIL import Image, ImageOps


def normalize_exif_orientation(image_path: Path) -> None:
    """
    Rewrites the uploaded image after applying its EXIF orientation.
    This avoids sideways phone images during inference and display.
    """
    with Image.open(image_path) as image:
        normalized = ImageOps.exif_transpose(image)
        if normalized.mode not in ("RGB", "L"):
            normalized = normalized.convert("RGB")
        normalized.save(image_path)
