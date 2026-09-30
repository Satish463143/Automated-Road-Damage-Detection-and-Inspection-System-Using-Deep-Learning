from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.inspection import (
    InspectionDetailResponse,
    InspectionListResponse,
)
from app.services.inspection_service import inspection_service
from app.services.inference_service import ModelUnavailableError


router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.post("", response_model=InspectionDetailResponse, status_code=201)
async def create_inspection(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        return await inspection_service.create(db=db, upload=file)
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Inspection failed: {exc}",
        ) from exc


@router.get("", response_model=InspectionListResponse)
def list_inspections(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return inspection_service.list(db=db, limit=limit, offset=offset)


@router.get("/{inspection_id}", response_model=InspectionDetailResponse)
def get_inspection(
    inspection_id: UUID,
    db: Session = Depends(get_db),
):
    inspection = inspection_service.get(db=db, inspection_id=inspection_id)
    if inspection is None:
        raise HTTPException(status_code=404, detail="Inspection not found.")
    return inspection


@router.delete("/{inspection_id}", status_code=204)
def delete_inspection(
    inspection_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = inspection_service.delete(db=db, inspection_id=inspection_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inspection not found.")
    return Response(status_code=204)
