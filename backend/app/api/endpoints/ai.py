from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from backend.app.llm.gemini_provider import GeminiProvider
from backend.app.llm.redactor import ConfigRedactor
from backend.app.compliance.models import ComplianceFinding
from backend.app.security.auth import get_current_user
from backend.app.rag.store import RAGStore
from backend.app.db.session import AsyncSessionLocal, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.db.models import AppSetting

router = APIRouter(dependencies=[Depends(get_current_user)])

class ExplainRequest(BaseModel):
    finding: ComplianceFinding
    device_platform: str
    raw_config_evidence: str
    asset_criticality: str = "MEDIUM"
    exposure_factor: float = 1.0

class ExplainResponse(BaseModel):
    explanation: str
    remediation: str

from backend.app.llm.provider import BaseLLMProvider
from backend.app.llm.local_provider import LocalLLMProvider
from backend.app.llm.disabled_provider import DisabledProvider

async def get_llm_provider(db: AsyncSession = Depends(get_db)) -> BaseLLMProvider:
    try:
        setting_provider = await db.execute(select(AppSetting).where(AppSetting.key == "ai_provider"))
        setting_provider = setting_provider.scalar_one_or_none()
        provider_type = setting_provider.value if setting_provider else "gemini"
        
        setting_enabled = await db.execute(select(AppSetting).where(AppSetting.key == "ai_enabled"))
        setting_enabled = setting_enabled.scalar_one_or_none()
        is_enabled = setting_enabled.value != "false" if setting_enabled else True
        
        if not is_enabled or provider_type == "disabled":
            return DisabledProvider()
            
        if provider_type == "local":
            setting_url = await db.execute(select(AppSetting).where(AppSetting.key == "local_ai_url"))
            setting_url = setting_url.scalar_one_or_none()
            url = setting_url.value if setting_url else "http://localhost:11434"
            return LocalLLMProvider(endpoint=url)
            
        return GeminiProvider()
    except Exception as e:
        # Fallback gracefully
        print(f"Error in LLM Provider setup: {e}")
        return DisabledProvider()

@router.post("/explain", response_model=ExplainResponse, summary="Generate AI explanation and remediation")
async def explain_finding(
    request: ExplainRequest,
    provider: BaseLLMProvider = Depends(get_llm_provider),
    db: AsyncSession = Depends(get_db)
):
    """
    Takes a deterministic compliance finding and generates a grounded explanation
    and secure remediation steps using the AI provider.
    """
    try:
        # Retrieve RAG Knowledge
        rag_knowledge_text = ""
        try:
            rag_store = RAGStore()
            query = f"{request.finding.control_title} {request.finding.actual} {request.device_platform}"
            async with AsyncSessionLocal() as db:
                docs = await rag_store.search(db, query, top_k=2)
                if docs:
                    rag_knowledge_text = "\n\n".join([f"Source: {d['authority']} ({d['source_id']})\n{d['text']}" for d in docs])
        except Exception as e:
            # Degrade gracefully if RAG fails
            print(f"RAG Retrieval failed: {e}")

        explanation = await provider.generate_explanation(
            finding=request.finding, 
            config_context=request.raw_config_evidence,
            device_os=request.device_platform,
            rag_knowledge=rag_knowledge_text,
            asset_criticality=request.asset_criticality,
            exposure_factor=request.exposure_factor
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
        # Fallback explanation if LLM completely fails
        return ExplainResponse(
            explanation=f"AI Explanation is temporarily unavailable. Deterministic violation detected for control: {request.finding.control_id}",
            remediation="Consult standard vendor documentation for remediation."
        )

class ChatRequest(BaseModel):
    scan_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse, summary="Scan-aware AI chat")
async def scan_chat(
    request: ChatRequest,
    provider: BaseLLMProvider = Depends(get_llm_provider),
    db: AsyncSession = Depends(get_db)
):
    from backend.app.db.crud import get_scan_with_findings
    
    if isinstance(provider, DisabledProvider):
        return ChatResponse(answer="AI Assistance: OFF\n\nStructured scan queries remain available. Natural-language generation is disabled.")
        
    scan = await get_scan_with_findings(db, request.scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    # Build bounded context
    context = f"Device: {scan.hostname} (Vendor: {scan.vendor})\n"
    context += f"Risk Score: {scan.risk_score} | Compliance: {scan.compliance_score}\n"
    if scan.vulnerabilities_json:
        context += "Vulnerabilities: " + ", ".join([v.get("cve_id", "") for v in scan.vulnerabilities_json]) + "\n"
    
    context += "Findings:\n"
    for f in scan.findings:
        if f.status == "FAIL":
            context += f"- [{f.severity}] {f.control_id}: {f.title} (Actual: {f.actual})\n"
            
    answer = await provider.generate_chat_response(request.question, context)
    return ChatResponse(answer=answer)

@router.post("/redact", summary="Test the config redactor")
async def test_redaction(config: dict):
    if "raw_config" not in config:
        raise HTTPException(status_code=400, detail="Missing raw_config")
    
    redacted = ConfigRedactor.redact(config["raw_config"])
    return {"redacted_config": redacted}
