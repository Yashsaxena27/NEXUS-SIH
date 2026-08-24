"""
NEXUS — Vendor-Neutral Security Intermediate Representation (IR)

This is the canonical schema that ALL vendor configurations normalize into.
The compliance engine operates exclusively on this representation.

Architecture principle:
    Cisco    ─┐
    Juniper  ─┤
    Fortinet ─┼─► NormalizedConfig ──► Compliance Engine ──► PASS/FAIL/UNKNOWN
    PaloAlto ─┤
    Unknown  ─┘

Each security-relevant property carries provenance metadata:
    - value: the extracted value
    - confidence: 0.0–1.0 (1.0 for deterministic, <1.0 for AI-inferred)
    - source: line number or section reference in the original config
    - method: how the value was extracted
    - raw_evidence: the raw config text that produced this value
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Interpretation method — how a property value was derived
# ---------------------------------------------------------------------------
class InterpretationMethod(str, Enum):
    DETERMINISTIC_PARSER = "deterministic_parser"
    REGEX_MATCH = "regex_match"
    LLM_INFERENCE = "llm_inference"
    HUMAN_CONFIRMED = "human_confirmed"
    DEFAULT_ASSUMED = "default_assumed"


# ---------------------------------------------------------------------------
# PropertyEvidence — provenance metadata for each normalized property
# ---------------------------------------------------------------------------
class PropertyEvidence(BaseModel):
    """Provenance metadata for a single normalized property."""
    field: str = Field(..., description="Dot-path to the property, e.g. 'management.ssh.version'")
    value: Any = Field(..., description="Extracted value")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Interpretation confidence")
    source: Optional[str] = Field(None, description="Source reference (e.g. 'line 182')")
    method: InterpretationMethod = Field(
        InterpretationMethod.DETERMINISTIC_PARSER,
        description="How this value was extracted",
    )
    raw_evidence: Optional[str] = Field(None, description="Raw config text that produced this value")


# ---------------------------------------------------------------------------
# UnknownCommand — commands the parser could not interpret
# ---------------------------------------------------------------------------
class UnknownCommand(BaseModel):
    """A configuration command the parser could not map to the normalized schema."""
    line_number: Optional[int] = None
    raw_text: str
    ai_hypothesis: Optional[str] = Field(None, description="AI's best guess at the semantic meaning")
    ai_confidence: float = Field(0.0, ge=0.0, le=1.0)
    suggested_property: Optional[str] = Field(None, description="Suggested IR field path")
    suggested_value: Optional[Any] = None


# ---------------------------------------------------------------------------
# Device info
# ---------------------------------------------------------------------------
class DeviceInfo(BaseModel):
    vendor: str = Field(..., description="Vendor name: cisco, juniper, fortinet, paloalto")
    platform: str = Field("", description="OS/platform: IOS-XE, Junos, FortiOS, PAN-OS")
    device_type: str = Field("", description="Device type: router, switch, firewall")
    version: Optional[str] = Field(None, description="Firmware/OS version")
    hostname: Optional[str] = Field(None, description="Device hostname")


# ---------------------------------------------------------------------------
# Management plane
# ---------------------------------------------------------------------------
class SSHConfig(BaseModel):
    enabled: bool = False
    version: Optional[int] = None  # 1 or 2

class TelnetConfig(BaseModel):
    enabled: bool = False

class HttpAdminConfig(BaseModel):
    enabled: bool = False
    https_only: Optional[bool] = None

class ManagementConfig(BaseModel):
    ssh: SSHConfig = Field(default_factory=SSHConfig)
    telnet: TelnetConfig = Field(default_factory=TelnetConfig)
    http_admin: HttpAdminConfig = Field(default_factory=HttpAdminConfig)
    session_timeout: Optional[int] = Field(None, description="Session timeout in seconds")
    login_banner: Optional[str] = Field(None, description="Login banner text")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
class PasswordPolicy(BaseModel):
    min_length: Optional[int] = None
    complexity_enabled: Optional[bool] = None

class AuthenticationConfig(BaseModel):
    aaa_enabled: bool = False
    method: Optional[str] = Field(None, description="Auth method: tacacs+, radius, local")
    local_fallback: Optional[bool] = None
    password_policy: PasswordPolicy = Field(default_factory=PasswordPolicy)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
class SyslogConfig(BaseModel):
    enabled: bool = False
    server: Optional[str] = None
    level: Optional[str] = None

class LoggingConfig(BaseModel):
    syslog: SyslogConfig = Field(default_factory=SyslogConfig)
    local_logging_enabled: bool = False
    buffer_size: Optional[int] = None


# ---------------------------------------------------------------------------
# SNMP
# ---------------------------------------------------------------------------
class SNMPConfig(BaseModel):
    version: Optional[str] = None  # "1", "2c", "3"
    community_string: Optional[str] = None
    default_community: bool = Field(
        False, description="True if community string is a well-known default (public/private)"
    )


# ---------------------------------------------------------------------------
# Time / NTP
# ---------------------------------------------------------------------------
class NTPConfig(BaseModel):
    enabled: bool = False
    servers: list[str] = Field(default_factory=list)
    authentication_enabled: Optional[bool] = None

class TimeConfig(BaseModel):
    ntp: NTPConfig = Field(default_factory=NTPConfig)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
class ServicesConfig(BaseModel):
    http_server_enabled: bool = False
    cdp_enabled: Optional[bool] = None
    lldp_enabled: Optional[bool] = None


# ---------------------------------------------------------------------------
# Access control
# ---------------------------------------------------------------------------
class AccessControlConfig(BaseModel):
    acl_enabled: Optional[bool] = None
    rules_count: Optional[int] = None


# ---------------------------------------------------------------------------
# NormalizedConfig — THE canonical vendor-neutral security representation
# ---------------------------------------------------------------------------
class NormalizedConfig(BaseModel):
    """
    The vendor-neutral security intermediate representation.

    All vendor-specific configurations are mapped into this common model.
    The compliance engine evaluates ONLY this model — never raw vendor syntax.
    """
    device: DeviceInfo
    management: ManagementConfig = Field(default_factory=ManagementConfig)
    authentication: AuthenticationConfig = Field(default_factory=AuthenticationConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    snmp: SNMPConfig = Field(default_factory=SNMPConfig)
    time: TimeConfig = Field(default_factory=TimeConfig)
    services: ServicesConfig = Field(default_factory=ServicesConfig)
    access_control: AccessControlConfig = Field(default_factory=AccessControlConfig)


# ---------------------------------------------------------------------------
# NormalizationResult — config + evidence + unknowns
# ---------------------------------------------------------------------------
class NormalizationResult(BaseModel):
    """Complete result of normalizing a vendor configuration."""
    config: NormalizedConfig
    evidence: list[PropertyEvidence] = Field(default_factory=list)
    unknown_commands: list[UnknownCommand] = Field(default_factory=list)
    raw_config: Optional[str] = Field(None, description="Original raw configuration text")
    parse_errors: list[str] = Field(default_factory=list)
