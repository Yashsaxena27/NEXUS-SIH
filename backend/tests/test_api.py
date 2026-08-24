import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.app.main import app
from backend.app.db.session import get_db
from backend.app.db.models import Base

from contextlib import asynccontextmanager

# Setup in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@asynccontextmanager
async def override_lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app.router.lifespan_context = override_lifespan

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

CISCO_CONFIG = """
version 17.3
hostname API-TEST-RTR
ip ssh version 2
!
line vty 0 4
 transport input ssh
"""

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_scan_config_success():
    payload = {
        "raw_config": CISCO_CONFIG,
        "vendor_hint": "cisco"
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/scans/scan", json=payload)
        if response.status_code != 200:
            print(response.json())
        assert response.status_code == 200
        
        data = response.json()
        assert "scan_id" in data
        assert data["vendor"] == "cisco"
        assert data["hostname"] == "API-TEST-RTR"
        assert data["total_controls"] > 0
        assert "findings" in data
        assert len(data["findings"]) == data["total_controls"]

def test_scan_config_empty():
    payload = {
        "raw_config": "   ",
        "vendor_hint": None
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/scans/scan", json=payload)
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

def test_scan_config_unknown_vendor():
    # If the config is nonsense and no hint is given, detector will say 'unknown'
    # The normalizer will return an empty/unknown config, and compliance will run against it (yielding UNKNOWN)
    payload = {
        "raw_config": "this is a text file with no networking concepts",
        "vendor_hint": None
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/scans/scan", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["vendor"] == "unknown"
        assert data["unknown_controls"] > 0

def test_scan_config_invalid_schema():
    payload = {
        "wrong_field": "test"
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/scans/scan", json=payload)
        assert response.status_code == 422 # Validation Error
