from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate_explanation(self, finding: Any, config_context: str, device_os: str) -> str:
        """
        Generate a grounded explanation for a compliance finding based on the config context.
        """
        pass

    @abstractmethod
    async def generate_remediation(self, finding: Any, device_os: str) -> str:
        """
        Generate remediation steps to fix the finding on the specified device OS.
        """
        pass
