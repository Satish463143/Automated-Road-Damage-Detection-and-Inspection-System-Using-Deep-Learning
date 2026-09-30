from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ml.detector import detector


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check(db: Session = Depends(get_db)):
    database_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_ok = False

    model_ok = detector.is_available()

    overall = "healthy" if database_ok and model_ok else "degraded"

    return {
        "status": overall,
        "database": "connected" if database_ok else "unavailable",
        "model": "loaded" if model_ok else "unavailable",
    }
