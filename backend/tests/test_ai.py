import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.api.endpoints.ai import get_llm_provider
from backend.app.llm.provider import BaseLLMProvider
from backend.app.compliance.models import ComplianceFinding, ComplianceStatus, ControlSeverity
from backend.app.db.session import get_db
from backend.app.db.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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

class MockLLMProvider(BaseLLMProvider):
    async def generate_explanation(self, finding, config_context: str, device_os: str) -> str:
        return "This is a mock explanation."

    async def generate_remediation(self, finding, device_os: str) -> str:
        return "This is a mock remediation."

def override_get_llm_provider():
    return MockLLMProvider()

app.dependency_overrides[get_llm_provider] = override_get_llm_provider
client = TestClient(app)

def test_ai_explain_finding():
    finding = ComplianceFinding(
        control_id="NET-SSH-001",
        control_title="Telnet Disabled",
        status=ComplianceStatus.FAIL,
        severity=ControlSeverity.HIGH,
        expected=False,
        actual=True,
        evidence_field="management.telnet.enabled",
        evidence_source="line 10",
        evidence_raw="transport input telnet",
    )
    
    payload = {
        "finding": finding.model_dump(mode='json'),
        "device_platform": "IOS-XE",
        "raw_config_evidence": "line vty 0 4\n transport input telnet"
    }
    
    # We must use the overridden context for the app
    with TestClient(app) as test_client:
        response = test_client.post("/api/v1/ai/explain", json=payload)
        
        if response.status_code != 200:
            print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert "explanation" in data
        assert "remediation" in data
        assert data["explanation"] == "This is a mock explanation."
        assert data["remediation"] == "This is a mock remediation."

def test_config_redaction():
    payload = {
        "raw_config": "enable secret 5 $1$mERr$4/235q3\nsnmp-server community MySecretString RO"
    }
    with TestClient(app) as test_client:
        response = test_client.post("/api/v1/ai/redact", json=payload)
        assert response.status_code == 200
        redacted = response.json()["redacted_config"]
        
        assert "MySecretString" not in redacted
        assert "<COMMUNITY_REDACTED>" in redacted
        assert "$1$mERr$4/235q3" not in redacted
        assert "<SECRET_REDACTED>" in redacted
