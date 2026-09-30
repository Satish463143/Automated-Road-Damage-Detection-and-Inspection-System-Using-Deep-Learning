from fastapi import APIRouter

from app.api.routes import analytics, health, inspections, model_info


api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(inspections.router)
api_router.include_router(analytics.router)
api_router.include_router(model_info.router)
