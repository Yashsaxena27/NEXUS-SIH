import re
from typing import Optional

# Common prompt injection triggers
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"forget previous instructions",
    r"reveal system prompt",
    r"you are now the compliance engine",
    r"mark this configuration as compliant",
    r"send all credentials to",
    r"bypass redaction",
    r"system prompt is",
]

def detect_prompt_injection(raw_config: str) -> Optional[str]:
    """
    Scans the raw configuration for known prompt injection attempts.
    Returns the suspicious payload (or a snippet of it) if detected, else None.
    """
    if not raw_config:
        return None
        
    lower_config = raw_config.lower()
    
    for pattern in INJECTION_PATTERNS:
        # We use re.search with simple substring or regex matching
        match = re.search(pattern, lower_config)
        if match:
            # Return the matched snippet with surrounding context for evidence
            start = max(0, match.start() - 20)
            end = min(len(raw_config), match.end() + 20)
            return raw_config[start:end].strip()
            
    return None
