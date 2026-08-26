import httpx
from typing import Any
from backend.app.llm.provider import BaseLLMProvider

class LocalLLMProvider(BaseLLMProvider):
    """
    Provider that connects to a local OpenAI-compatible inference server (e.g., Ollama, vLLM).
    Demonstrates sovereign deployment capability where no data leaves the organization.
    """
    def __init__(self, endpoint: str, model: str = "llama3"):
        self.endpoint = endpoint.rstrip('/')
        self.model = model
        
    async def _call_local_api(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}]
                }
                # Simple fallback: if endpoint doesn't have /v1/chat/completions, append it.
                url = self.endpoint
                if not url.endswith("/v1/chat/completions"):
                    url = f"{url}/v1/chat/completions"
                    
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "Empty response from local LLM.")
        except Exception as e:
            return f"[Local AI Unavailable] {str(e)}"

    async def generate_explanation(self, finding: Any, config_context: str, device_os: str, rag_knowledge: str = "", asset_criticality: str = "MEDIUM", exposure_factor: float = 1.0) -> str:
        prompt = (
            f"Explain the security risk for finding {finding.control_id} ({finding.title}) on {device_os}.\n"
            f"Context: {config_context}\n"
            f"Knowledge: {rag_knowledge}\n"
        )
        return await self._call_local_api(prompt)

    async def generate_remediation(self, finding: Any, device_os: str) -> str:
        prompt = f"Provide exact CLI remediation for {finding.title} on {device_os}."
        return await self._call_local_api(prompt)

    async def generate_chat_response(self, question: str, scan_context: str) -> str:
        prompt = (
            "You are NEXUS, a cybersecurity intelligence assistant.\n"
            "Answer the following user question strictly based on the provided Scan Context.\n"
            f"Context: {scan_context}\n\nQuestion: {question}"
        )
        return await self._call_local_api(prompt)
