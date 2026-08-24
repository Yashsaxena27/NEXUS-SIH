import json
from typing import Any
from backend.app.core.config import settings
from backend.app.llm.provider import BaseLLMProvider
from backend.app.llm.prompts import EXPLANATION_PROMPT, REMEDIATION_PROMPT
from backend.app.llm.redactor import ConfigRedactor

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        if not genai:
            raise ImportError("google-genai package is not installed.")
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.AI_MODEL

    async def generate_explanation(self, finding: Any, config_context: str, device_os: str) -> str:
        # Redact the context to ensure no secrets are sent
        safe_context = ConfigRedactor.redact(config_context)
        
        prompt = EXPLANATION_PROMPT.format(
            device_os=device_os,
            control_id=finding.control_id,
            control_title=finding.control_title,
            severity=finding.severity.value,
            expected=finding.expected,
            actual=finding.actual,
            evidence=safe_context,
            context=finding.explanation_context or "None"
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    async def generate_remediation(self, finding: Any, device_os: str) -> str:
        prompt = REMEDIATION_PROMPT.format(
            device_os=device_os,
            control_id=finding.control_id,
            control_title=finding.control_title,
            expected=finding.expected,
            actual=finding.actual,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text
