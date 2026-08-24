from fastapi import APIRouter
from backend.app.api.endpoints import scans, ai
from backend.app.schemas.api import HealthResponse

api_router = APIRouter()

@api_router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse()

api_router.include_router(scans.router, prefix="/scans", tags=["scans"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
