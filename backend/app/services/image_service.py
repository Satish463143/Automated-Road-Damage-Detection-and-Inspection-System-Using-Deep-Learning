from pathlib import Path

from PIL import Image, UnidentifiedImageError


def validate_and_get_dimensions(image_path: Path) -> tuple[int, int]:
    try:
        with Image.open(image_path) as image:
            image.verify()

        with Image.open(image_path) as image:
            width, height = image.size

        if width <= 0 or height <= 0:
            raise ValueError("Image dimensions are invalid.")

        return width, height

    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Uploaded file is not a valid image.") from exc
