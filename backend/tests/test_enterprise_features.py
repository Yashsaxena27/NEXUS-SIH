import pytest
from httpx import AsyncClient
import csv
from io import StringIO
from backend.app.main import app
from backend.app.db.models import Base
from backend.app.db.session import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient

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

CISCO_CONFIG = """
version 17.3
hostname API-TEST-RTR
ip ssh version 2
!
line vty 0 4
 transport input ssh
"""

def test_enterprise_features():
    with TestClient(app) as client:
        # 1. Create a scan
        payload = {
            "raw_config": CISCO_CONFIG,
            "vendor_hint": "cisco"
        }
        response = client.post("/api/v1/scans/scan", json=payload)
        assert response.status_code == 200
        scan_id = response.json()["scan_id"]
        
        # 2. Test Attack Graph
        response = client.get(f"/api/v1/scans/{scan_id}/graph")
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) >= 2
        
        # 3. Test CSV Export
        response = client.get(f"/api/v1/scans/{scan_id}/export/csv")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content))
        rows = list(csv_reader)
        assert len(rows) > 1 
        assert "Scan ID" in rows[0]
        
        # 4. Test AI Chat
        response = client.post(
            "/api/v1/ai/chat",
            json={
                "scan_id": scan_id,
                "question": "What is the compliance score?"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert len(data["answer"]) > 0
