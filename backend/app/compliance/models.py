"""
Compliance engine models — control definitions and evaluation results.

Controls are defined as DATA (YAML/JSON), not scattered code.
The engine evaluates NormalizedConfig against controls and produces
PASS / FAIL / UNKNOWN with evidence.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ComplianceStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    UNKNOWN_ABSENT = "UNKNOWN_ABSENT"
    UNKNOWN_PARSE_ERROR = "UNKNOWN_PARSE_ERROR"


class ControlSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class ControlOperator(str, Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    IN_RANGE = "IN_RANGE"
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT_EXISTS"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"
    IN_SET = "IN_SET"
    NOT_IN_SET = "NOT_IN_SET"


class ControlRequirement(BaseModel):
    """A single check within a compliance control."""
    field: str = Field(..., description="Dot-path into NormalizedConfig, e.g. 'management.ssh.version'")
    operator: ControlOperator
    value: Any = Field(..., description="Expected value for the check")
    value_max: Optional[Any] = Field(None, description="Upper bound for IN_RANGE operator")


class ComplianceControl(BaseModel):
    """
    A compliance control definition.

    Controls are data — loaded from YAML files, not hard-coded.
    """
    id: str = Field(..., description="Unique control ID, e.g. 'NET-SSH-001'")
    title: str
    description: Optional[str] = None
    severity: ControlSeverity
    category: str = Field("", description="Category, e.g. 'Secure Management'")
    frameworks: list[str] = Field(default_factory=list, description="e.g. ['CIS', 'NIST AC-17']")
    requirement: ControlRequirement
    remediation_hint: Optional[str] = Field(None, description="Brief remediation guidance")


class ComplianceFinding(BaseModel):
    """Result of evaluating a single control against a normalized config."""
    control_id: str
    control_title: str
    status: ComplianceStatus
    severity: ControlSeverity
    category: str = ""
    frameworks: list[str] = Field(default_factory=list)
    expected: Any = Field(None, description="What the control requires")
    actual: Any = Field(None, description="What was found in the config")
    evidence_field: str = Field("", description="Which IR field was checked")
    evidence_source: Optional[str] = Field(None, description="Source line/section")
    evidence_raw: Optional[str] = Field(None, description="Raw config evidence")
    confidence: float = Field(1.0, description="Confidence in the evidence")
    remediation_hint: Optional[str] = None
    explanation_context: Optional[str] = Field(
        None, description="Pre-built context string for AI explanation"
    )


class ComplianceReport(BaseModel):
    """Complete compliance evaluation for a single device."""
    device_vendor: str
    device_hostname: Optional[str] = None
    device_platform: str = ""
    total_controls: int = 0
    passed: int = 0
    failed: int = 0
    unknown: int = 0
    compliance_score: float = Field(0.0, description="0-100 compliance percentage")
    risk_score: float = Field(0.0, description="Weighted risk score")
    findings: list[ComplianceFinding] = Field(default_factory=list)
