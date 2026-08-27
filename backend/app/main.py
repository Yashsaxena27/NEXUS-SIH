from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.api.router import api_router
from backend.app.api.endpoints import scans, health, ai, adaptive, audit, settings as app_settings
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
    
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import RequestValidationError
    import traceback
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception):
        # Prevent stack trace leakage in production
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred.", "type": "server_error"}
        )
        
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "Input validation failed.", "errors": exc.errors()}
        )

    # Set up CORS
    cors_origins = [str(origin) for origin in settings.CORS_ORIGINS]
    if settings.FRONTEND_URL:
        cors_origins.append(settings.FRONTEND_URL)

    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    app.include_router(adaptive.router, prefix=f"{settings.API_V1_PREFIX}/adaptive", tags=["Adaptive Learning"])
    app.include_router(audit.router, prefix=f"{settings.API_V1_PREFIX}/audit", tags=["Audit"])
    app.include_router(app_settings.router, prefix=f"{settings.API_V1_PREFIX}/settings", tags=["Settings"])

    return app

app = create_app()
