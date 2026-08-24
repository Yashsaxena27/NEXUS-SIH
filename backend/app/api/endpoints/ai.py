from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from backend.app.llm.gemini_provider import GeminiProvider
from backend.app.llm.redactor import ConfigRedactor
from backend.app.compliance.models import ComplianceFinding

router = APIRouter()

class ExplainRequest(BaseModel):
    finding: ComplianceFinding
    device_platform: str
    raw_config_evidence: str

class ExplainResponse(BaseModel):
    explanation: str
    remediation: str

# In a real app we'd use Dependency Injection for the provider
def get_llm_provider() -> GeminiProvider:
    try:
        return GeminiProvider()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM Provider not available: {str(e)}")

@router.post("/explain", response_model=ExplainResponse, summary="Generate AI explanation and remediation")
async def explain_finding(
    request: ExplainRequest,
    provider: GeminiProvider = Depends(get_llm_provider)
):
    """
    Takes a deterministic compliance finding and generates a grounded explanation
    and secure remediation steps using the AI provider.
    """
    try:
        explanation = await provider.generate_explanation(
            finding=request.finding, 
            config_context=request.raw_config_evidence,
            device_os=request.device_platform
        )
        
        remediation = await provider.generate_remediation(
            finding=request.finding,
            device_os=request.device_platform
        )
        
        return ExplainResponse(
            explanation=explanation,
            remediation=remediation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/redact", summary="Test the config redactor")
async def test_redaction(config: dict):
    if "raw_config" not in config:
        raise HTTPException(status_code=400, detail="Missing raw_config")
    
    redacted = ConfigRedactor.redact(config["raw_config"])
    return {"redacted_config": redacted}
