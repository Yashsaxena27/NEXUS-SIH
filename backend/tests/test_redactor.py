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

