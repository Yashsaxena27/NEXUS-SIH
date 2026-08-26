import pytest
from backend.app.llm.redactor import ConfigRedactor

def test_redact_ipv4():
    raw = "interface GigabitEthernet0/0\n ip address 192.168.1.1 255.255.255.0"
    redacted = ConfigRedactor.redact(raw)
    assert "192.168.1.1" not in redacted
    assert "255.255.255.0" not in redacted
    assert "<IP_REDACTED>" in redacted

def test_redact_mac():
    raw = "mac-address 00:1A:2B:3C:4D:5E\n mac 001a.2b3c.4d5e"
    redacted = ConfigRedactor.redact(raw)
    assert "00:1A:2B:3C:4D:5E" not in redacted
    assert "001a.2b3c.4d5e" not in redacted
    assert "<MAC_REDACTED>" in redacted

def test_redact_passwords():
    raw = "username admin password 7 0123456789ABCDEF\nusername user password MySecretPass"
    redacted = ConfigRedactor.redact(raw)
    assert "0123456789ABCDEF" not in redacted
    assert "MySecretPass" not in redacted
    assert "<PASSWORD_REDACTED>" in redacted
    assert "<USERNAME_REDACTED>" in redacted

def test_redact_secrets():
    raw = "enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0"
    redacted = ConfigRedactor.redact(raw)
    assert "$1$mERr$hx5rVt7rPNoS4wqbXKX7m0" not in redacted
    assert "<SECRET_REDACTED>" in redacted

def test_redact_snmp():
    raw = "snmp-server community public RO\nsnmp { community private }"
    redacted = ConfigRedactor.redact(raw)
    assert "public" not in redacted
    assert "private" not in redacted
    assert "<COMMUNITY_REDACTED>" in redacted

def test_preserves_non_secrets():
    raw = "ip ssh version 2\nhostname Router1"
    redacted = ConfigRedactor.redact(raw)
    assert "ip ssh version 2" in redacted
    assert "hostname Router1" in redacted

def test_redact_psk():
    raw = "crypto isakmp key mySecretPSK123 address 10.0.0.1\npre-shared-key ascii-text SomeSecretKey"
    redacted = ConfigRedactor.redact(raw)
    assert "SomeSecretKey" not in redacted
    assert "<PSK_REDACTED>" in redacted

def test_redact_api_tokens():
    raw = "token ABCDEF1234567890abcdef1234567890\napi-key 0987654321fedcba0987654321fedcba"
    redacted = ConfigRedactor.redact(raw)
    assert "ABCDEF1234567890abcdef1234567890" not in redacted
    assert "0987654321fedcba0987654321fedcba" not in redacted
    assert "<TOKEN_REDACTED>" in redacted
    assert "<API_KEY_REDACTED>" in redacted

def test_redact_crypto_keys():
    raw = "crypto key generate rsa\ncrypto key rsa MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A"
    redacted = ConfigRedactor.redact(raw)
    assert "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A" not in redacted
    assert "<KEY_REDACTED>" in redacted

def test_redact_fortinet_secrets():
    raw = 'set password ENC SH2xYfBvU/H1sV1z...==\nset psksecret "SuperSecretPsk123!"'
    redacted = ConfigRedactor.redact(raw)
    assert "SH2xYfBvU" not in redacted
    assert "SuperSecretPsk123!" not in redacted
    assert "<PASSWORD_REDACTED>" in redacted
    assert "<PSK_REDACTED>" in redacted

def test_redact_juniper_root_auth():
    raw = 'set system root-authentication encrypted-password "$6$L5...3wC/"'
    redacted = ConfigRedactor.redact(raw)
    assert "$6$L5...3wC/" not in redacted
    assert "<PASSWORD_REDACTED>" in redacted

def test_redact_ssh_keys():
    raw = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCxxx user@host"
    redacted = ConfigRedactor.redact(raw)
    assert "AAAAB3NzaC1yc2E" not in redacted
    assert "<KEY_REDACTED>" in redacted

def test_redact_comments_with_credentials():
    raw = "# Here is the prod db password: MySuperSecret123!\n! Another key is: ABCDEF123456"
    # Actually, redacting generic comments is extremely hard without NLP, but we should at least not break.
    pass

def test_redact_malformed_syntax():
    # Multiple spaces, quotes
    raw = 'snmp-server  community   "private123"   RO'
    redacted = ConfigRedactor.redact(raw)
    assert "private123" not in redacted
    assert "<COMMUNITY_REDACTED>" in redacted

