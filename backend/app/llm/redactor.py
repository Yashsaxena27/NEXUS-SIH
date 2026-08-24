import re

class ConfigRedactor:
    """Sanitizes raw configuration to remove secrets before sending to LLMs."""
    
    SECRET_PATTERNS = [
        # Passwords/Hashes
        (r"(password\s+\d+\s+)([a-zA-Z0-9\/\+\=]+)", r"\1<REDACTED_PASSWORD>"),
        (r"(secret\s+\d+\s+)([a-zA-Z0-9\/\+\=]+)", r"\1<REDACTED_SECRET>"),
        (r"(snmp-server community\s+)(\S+)", r"\1<REDACTED_COMMUNITY>"),
        (r"(snmp\s*{\s*community\s+)(\S+)", r"\1<REDACTED_COMMUNITY>"),
        (r"(set name\s+\")([^\"]+)(\")", r"\1<REDACTED_COMMUNITY>\3"),
        # Keys
        (r"(crypto key\s+\S+\s+)([a-zA-Z0-9\/\+\=\n]+)", r"\1<REDACTED_KEY>"),
        (r"(pre-shared-key\s+)(?:ascii-text|hexadecimal)\s+(\S+)", r"\1<REDACTED_PSK>"),
        # Hashes (e.g., enable secret 5 <hash>)
        (r"(enable secret\s+\d+\s+)(\S+)", r"\1<REDACTED_HASH>"),
    ]

    @classmethod
    def redact(cls, raw_config: str) -> str:
        """Applies regex patterns to redact sensitive information."""
        redacted = raw_config
        for pattern, replacement in cls.SECRET_PATTERNS:
            redacted = re.sub(pattern, replacement, redacted)
        return redacted
