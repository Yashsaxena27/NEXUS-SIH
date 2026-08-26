import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import engine
from backend.app.db.models import Base, AppSetting
from backend.app.api.endpoints.ai import explain_finding, ExplainRequest
from backend.app.compliance.models import ComplianceFinding, ComplianceStatus, ControlSeverity

# Mock provider
class MockProvider:
    async def generate_explanation(self, *args, **kwargs):
        return "AI Generated Explanation"
    async def generate_remediation(self, *args, **kwargs):
        return "AI Generated Remediation"
    async def generate_chat_response(self, *args, **kwargs):
        return "AI Generated Chat"

@pytest_asyncio.fixture
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    from backend.app.db.session import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_ai_kill_switch(test_db: AsyncSession):
    finding = ComplianceFinding(
        control_id="TEST-001",
        control_title="Test",
        status=ComplianceStatus.FAIL,
        severity=ControlSeverity.LOW,
        category="Test",
        expected="A",
        actual="B"
    )
    req = ExplainRequest(finding=finding, device_platform="cisco", raw_config_evidence="A")
    
    # By default, should use AI
    from backend.app.api.endpoints.ai import get_llm_provider
    provider = await get_llm_provider(test_db)
    
    res = await explain_finding(req, provider, test_db)
    
    # Turn OFF kill switch
    setting = AppSetting(key="ai_enabled", value="false")
    test_db.add(setting)
    await test_db.commit()
    
    # Should fallback to deterministic message
    provider_off = await get_llm_provider(test_db)
    res2 = await explain_finding(req, provider_off, test_db)
    assert "AI Explanation is temporarily unavailable" in res2.explanation or "AI Assistance: OFF" in res2.explanation or "disabled" in res2.explanation.lower()
    assert "remediation" in res2.remediation.lower() or "disabled" in res2.remediation.lower() or "documentation" in res2.remediation.lower()
