from typing import Any
from backend.app.llm.provider import BaseLLMProvider

class DisabledProvider(BaseLLMProvider):
    """
    A null provider used when AI is disabled. 
    It ensures the deterministic engine runs without any AI dependencies.
    """
    
    async def generate_explanation(self, finding: Any, config_context: str, device_os: str, rag_knowledge: str = "", asset_criticality: str = "MEDIUM", exposure_factor: float = 1.0) -> str:
        return "AI Assistance: OFF. Deterministic rules remain fully operational."

    async def generate_remediation(self, finding: Any, device_os: str) -> str:
        return "AI Assistance: OFF. Please refer to deterministic remediation intelligence or standard vendor documentation."

    async def generate_chat_response(self, question: str, scan_context: str) -> str:
        return "AI Assistance: OFF\n\nStructured scan queries remain available. Natural-language generation is disabled."
