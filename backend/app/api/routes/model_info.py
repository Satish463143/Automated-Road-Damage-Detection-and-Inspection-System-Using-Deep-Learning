from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.model_info import ModelInfoResponse
from app.services.model_service import model_service


router = APIRouter(prefix="/model", tags=["Model"])


@router.get("", response_model=ModelInfoResponse)
def get_model_info(db: Session = Depends(get_db)):
    model = model_service.get_active(db)
    if model is None:
        raise HTTPException(status_code=404, detail="Model information not found.")
    return model_service.to_response(model)
