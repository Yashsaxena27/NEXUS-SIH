from fastapi import APIRouter
from backend.app.api.endpoints import scans, ai, adaptive, health
from backend.app.schemas.api import HealthResponse

api_router = APIRouter()

api_router.include_router(scans.router, prefix="/scans", tags=["scans"])
api_router.include_router(adaptive.router, prefix="/adaptive", tags=["adaptive"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(health.router, prefix="", tags=["health"])
