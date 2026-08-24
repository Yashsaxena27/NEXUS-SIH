from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.api.router import api_router
from backend.app.core.config import settings
from backend.app.db.models import Base
from backend.app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="NEXUS AI-Driven Multi-Vendor Network Security Compliance Auditor",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan
    )

    # Set up CORS
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app

app = create_app()
