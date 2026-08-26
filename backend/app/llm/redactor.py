import re
from typing import List, Tuple

class ConfigRedactor:
    """Sanitizes raw configuration to remove secrets before sending to LLMs."""
    
    # List of (pattern, replacement) tuples
    # Note: Order matters. More specific patterns should be matched before generic ones.
    SECRET_PATTERNS: List[Tuple[re.Pattern, str]] = [
        # IPv4 Addresses
        # Matches valid IPv4 addresses, avoiding purely version numbers
        # We redact all IPv4 to be safe. We could optionally exclude loopbacks later.
        (re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'), r'<IP_REDACTED>'),
        
        # IPv6 Addresses
        (re.compile(r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b'), r'<IPV6_REDACTED>'),
        (re.compile(r'\b(?:[A-Fa-f0-9]{1,4}:)*:[A-Fa-f0-9]{1,4}(?::[A-Fa-f0-9]{1,4})*\b'), r'<IPV6_REDACTED>'),
        
        # MAC Addresses
        (re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b'), r'<MAC_REDACTED>'),
        (re.compile(r'\b(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}\b'), r'<MAC_REDACTED>'), # Cisco format

        # Cisco/Fortinet/Juniper Passwords & Hashes
        (re.compile(r'(password\s+(?:ENC\s+|\d+\s+)?)(\S+)', re.IGNORECASE), r'\1<PASSWORD_REDACTED>'),
        (re.compile(r'(secret\s+(?:\d+\s+)?)(\S+)', re.IGNORECASE), r'\1<SECRET_REDACTED>'),
        (re.compile(r'(root-authentication\s+encrypted-password\s+)(["\']?)([^"\'\s]+)(["\']?)', re.IGNORECASE), r'\1\2<PASSWORD_REDACTED>\4'),
        
        # SSH Keys (ssh-rsa, ssh-ed25519)
        (re.compile(r'(ssh-(?:rsa|ed25519|dss)\s+)([A-Za-z0-9+/=]+)', re.IGNORECASE), r'\1<KEY_REDACTED>'),
        
        # SNMP Communities
        (re.compile(r'(snmp-server\s+community\s+)(\S+)', re.IGNORECASE), r'\1<COMMUNITY_REDACTED>'),
        (re.compile(r'(snmp\s*{\s*community\s+)(\S+)', re.IGNORECASE), r'\1<COMMUNITY_REDACTED>'),
        (re.compile(r'(set\s+name\s+["\']?)([^"\'\s]+)(["\']?)', re.IGNORECASE), r'\1<COMMUNITY_REDACTED>\3'),

        # Cryptographic Keys (e.g., PSK, crypto keys)
        (re.compile(r'(crypto\s+key\s+\S+\s+)([a-zA-Z0-9\/\+\=]{20,})', re.IGNORECASE), r'\1<KEY_REDACTED>'),
        (re.compile(r'(pre-shared-key\s+(?:ascii-text|hexadecimal)\s+)(\S+)', re.IGNORECASE), r'\1<PSK_REDACTED>'),
        (re.compile(r'(set\s+psksecret\s+)(["\']?)([^"\'\s]+)(["\']?)', re.IGNORECASE), r'\1\2<PSK_REDACTED>\4'),
        
        # Generic Usernames (Optional: Could be aggressive, but requested by P0)
        # We look for explicit username declarations
        (re.compile(r'(username\s+)(\S+)', re.IGNORECASE), r'\1<USERNAME_REDACTED>'),
        (re.compile(r'(set\s+admin\s+)(\S+)', re.IGNORECASE), r'\1<USERNAME_REDACTED>'),

        # API Keys / Tokens (heuristic: strings that look like long base64/hex tokens typically following 'token' or 'key')
        (re.compile(r'(token\s+)([A-Za-z0-9\-_]{20,})', re.IGNORECASE), r'\1<TOKEN_REDACTED>'),
        (re.compile(r'(api-key\s+)([A-Za-z0-9\-_]{20,})', re.IGNORECASE), r'\1<API_KEY_REDACTED>'),
    ]

    @classmethod
    def redact(cls, raw_config: str) -> str:
        """Applies regex patterns to redact sensitive information."""
        redacted = raw_config
        for pattern, replacement in cls.SECRET_PATTERNS:
            redacted = pattern.sub(replacement, redacted)
        return redacted
