from fastapi import APIRouter
from pydantic import BaseModel
import time

router = APIRouter()

start_time = time.time()

class HealthCheckResponse(BaseModel):
    status: str
    uptime_seconds: float
    version: str
    database: str = "ok"
    ai_available: bool = True

@router.get("/health", response_model=HealthCheckResponse, summary="System Healthcheck")
async def health_check():
    """
    Returns the system health status, uptime, and version.
    """
    return HealthCheckResponse(
        status="healthy",
        uptime_seconds=time.time() - start_time,
        version="0.1.0",
        database="ok",
        ai_available=True
    )
