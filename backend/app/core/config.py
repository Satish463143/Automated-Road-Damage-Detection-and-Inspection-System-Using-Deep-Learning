from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Road Damage Detection API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/road_damage_db"
    )

    model_path: Path = BASE_DIR / "models" / "weights" / "best.pt"
    model_metadata_path: Path = BASE_DIR / "models" / "metadata" / "model_info.json"

    upload_dir: Path = BASE_DIR / "storage" / "uploads"
    result_dir: Path = BASE_DIR / "storage" / "results"

    max_upload_size_mb: int = 10
    confidence_threshold: float = 0.25
    model_image_size: int = 640

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


settings = Settings()
