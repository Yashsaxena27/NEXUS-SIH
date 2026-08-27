"""
Application configuration using Pydantic Settings.
Loads from environment variables and .env file.
"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Project
    PROJECT_NAME: str = "NEXUS — Network Security Compliance Auditor"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://nexus:nexus@localhost:5432/nexus"

    # File storage
    UPLOAD_DIR: str = str(Path(__file__).parent.parent.parent / "uploads")
    MAX_UPLOAD_SIZE_MB: int = 50

    # CORS (React frontend dev server)
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
    ]
    
    # Production Frontend URL for CORS
    FRONTEND_URL: Optional[str] = None

    # AI Provider (behind abstraction layer)
    AI_PROVIDER: str = "gemini"  # "gemini", "openai", "claude"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gemini-1.5-flash"

    # Compliance
    CONTROLS_DIR: str = str(
        Path(__file__).parent.parent.parent.parent / "compliance" / "controls"
    )

    # Dataset
    DATASET_DIR: str = str(
        Path(__file__).parent.parent.parent.parent / "dataset"
    )


settings = Settings()
