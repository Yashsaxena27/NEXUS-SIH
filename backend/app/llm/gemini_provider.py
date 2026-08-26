import json
from typing import Any
from backend.app.core.config import settings
from backend.app.llm.provider import BaseLLMProvider
from backend.app.llm.prompts import EXPLANATION_PROMPT, REMEDIATION_PROMPT
from backend.app.llm.redactor import ConfigRedactor

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        if not genai:
            raise ImportError("google.generativeai package is not installed.")
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = settings.AI_MODEL

    async def generate_explanation(self, finding: Any, config_context: str, device_os: str, rag_knowledge: str = "", asset_criticality: str = "MEDIUM", exposure_factor: float = 1.0) -> str:
        # Redact the context to ensure no secrets are sent
        safe_context = ConfigRedactor.redact(config_context)
        
        prompt = EXPLANATION_PROMPT.format(
            device_os=device_os,
            control_id=finding.control_id,
            control_title=finding.control_title,
            severity=finding.severity.value,
            asset_criticality=asset_criticality,
            exposure_factor=exposure_factor,
            expected=finding.expected,
            actual=finding.actual,
            evidence=safe_context,
            context=finding.explanation_context or "None",
            rag_knowledge=rag_knowledge
        )

        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

    async def generate_remediation(self, finding: Any, device_os: str) -> str:
        prompt = REMEDIATION_PROMPT.format(
            device_os=device_os,
            control_id=finding.control_id,
            control_title=finding.control_title,
            expected=finding.expected,
            actual=finding.actual,
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Remediation guidance unavailable ({str(e)})."
            
    async def generate_chat_response(self, question: str, scan_context: str) -> str:
        prompt = (
            "You are NEXUS, a cybersecurity intelligence assistant.\n"
            "Answer the following user question strictly based on the provided Scan Context.\n"
            "If the answer is not in the context, say 'I don't have enough evidence in this scan to answer that reliably.'\n"
            "Do not hallucinate external vulnerabilities or findings.\n\n"
            f"=== SCAN CONTEXT ===\n{scan_context}\n====================\n\n"
            f"User Question: {question}"
        )
        
        try:
            # We are using generate_content, which is a sync call in the google-generativeai lib
            # but we run it in an async function. We could use asyncio.to_thread if it blocks too much.
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Chat is currently unavailable: {str(e)}"
