from pathlib import Path


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def safe_stem(filename: str) -> str:
    return Path(filename).stem.strip().replace(" ", "_")
