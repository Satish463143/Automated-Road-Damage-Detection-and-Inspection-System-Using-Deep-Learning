from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import BASE_DIR, settings
from app.core.constants import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES


def ensure_storage_directories() -> None:
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.result_dir.mkdir(parents=True, exist_ok=True)


def relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(BASE_DIR.resolve()))
    except ValueError:
        return str(path.resolve())


def absolute_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return BASE_DIR / path


def generate_storage_name(original_filename: str) -> str:
    suffix = Path(original_filename).suffix.lower()
    return f"{uuid4().hex}{suffix}"


async def save_upload(upload: UploadFile) -> Path:
    ensure_storage_directories()

    original_name = upload.filename or "image.jpg"
    suffix = Path(original_name).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Only JPG, JPEG, and PNG images are allowed.")

    if upload.content_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Invalid image MIME type.")

    output_path = settings.upload_dir / generate_storage_name(original_name)
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    written = 0

    try:
        with output_path.open("wb") as destination:
            while chunk := await upload.read(1024 * 1024):
                written += len(chunk)
                if written > max_bytes:
                    raise ValueError(
                        f"Image exceeds the {settings.max_upload_size_mb} MB upload limit."
                    )
                destination.write(chunk)
    except Exception:
        output_path.unlink(missing_ok=True)
        raise
    finally:
        await upload.close()

    return output_path


def build_result_path(original_path: Path) -> Path:
    return settings.result_dir / f"{original_path.stem}_detected.jpg"


def media_url(path_value: str | None) -> str | None:
    if not path_value:
        return None

    path = absolute_path(path_value)

    if path.parent.resolve() == settings.upload_dir.resolve():
        return f"/media/uploads/{path.name}"

    if path.parent.resolve() == settings.result_dir.resolve():
        return f"/media/results/{path.name}"

    return None


def delete_file(path_value: str | None) -> None:
    if not path_value:
        return

    path = absolute_path(path_value)
    path.unlink(missing_ok=True)
