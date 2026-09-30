from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.services.storage_service import ensure_storage_directories


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_storage_directories()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for road damage and pothole detection from images.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)

app.mount(
    "/media/uploads",
    StaticFiles(directory=str(settings.upload_dir)),
    name="uploads",
)

app.mount(
    "/media/results",
    StaticFiles(directory=str(settings.result_dir)),
    name="results",
)


@app.get("/", tags=["Root"])
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health",
    }
