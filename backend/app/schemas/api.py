from typing import Optional, List
from pydantic import BaseModel, Field
from backend.app.compliance.models import ComplianceFinding, VulnerabilityRecord

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "0.1.0"
    database: str = "connected"
    ai_available: bool = False

class ScanRequest(BaseModel):
    raw_config: str = Field(..., description="The raw configuration text to scan")
    vendor_hint: Optional[str] = Field(None, description="Optional vendor hint (e.g., 'cisco', 'juniper')")

class ScanResultResponse(BaseModel):
    scan_id: str = Field(..., description="Unique identifier for this scan")
    scan_name: Optional[str] = Field(None, description="Optional name for this scan")
    vendor: str = Field(..., description="Detected vendor")
    platform: Optional[str] = Field(None, description="Detected platform")
    hostname: Optional[str] = Field(None, description="Extracted hostname")
    compliance_score: float = Field(..., description="Overall compliance score (0-100)")
    risk_score: float = Field(..., description="Overall risk score (0-100)")
    total_controls: int = Field(..., description="Total number of controls evaluated")
    passed_controls: int = Field(..., description="Number of passing controls")
    failed_controls: int = Field(..., description="Number of failing controls")
    unknown_controls: int = Field(..., description="Number of controls with unknown status")
    findings: List[ComplianceFinding] = Field(..., description="Detailed findings for each control")
    prioritized_risks: list[dict] = Field(default_factory=list, description="Findings grouped and ordered by risk")
    vulnerabilities: list[VulnerabilityRecord] = Field(default_factory=list, description="Vulnerability intelligence")
    framework_alignments: dict[str, float] = Field(default_factory=dict, description="Alignment score per framework")
    correlation_summary: Optional[str] = Field(None, description="Summary of correlated vulnerabilities")

class ScanSummaryResponse(BaseModel):
    scan_id: str
    scan_name: Optional[str] = None
    created_at: Optional[str] = None
    vendor: str
    platform: Optional[str] = None
    hostname: Optional[str] = None
    compliance_score: float
    risk_score: float
    total_controls: int
    passed_controls: int
    failed_controls: int
    unknown_controls: int
    framework_alignments: dict[str, float] = Field(default_factory=dict)

class FindingResponse(BaseModel):
    control_id: str
    title: str
    status: str
    severity: str
    category: Optional[str] = None
    frameworks: list[str] = Field(default_factory=list)
    framework_mappings: list[dict] = Field(default_factory=list)
    expected: Optional[str] = None
    actual: Optional[str] = None
    evidence_field: Optional[str] = None
    evidence_source: Optional[str] = None
    evidence_raw: Optional[str] = None
    confidence: float = 1.0
    remediation_hint: Optional[str] = None
    explanation_context: Optional[str] = None
    exact_remediation: Optional[dict] = None

class ScanDetailResponse(BaseModel):
    scan_id: str
    scan_name: Optional[str] = None
    created_at: Optional[str] = None
    vendor: str
    platform: Optional[str] = None
    hostname: Optional[str] = None
    compliance_score: float
    risk_score: float
    total_controls: int
    passed_controls: int
    failed_controls: int
    unknown_controls: int
    findings: List[FindingResponse] = Field(default_factory=list)
    prioritized_risks: list[dict] = Field(default_factory=list)
    vulnerabilities: list[dict] = Field(default_factory=list)
    framework_alignments: dict[str, float] = Field(default_factory=dict)
    correlation_summary: Optional[str] = None

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    severity: Optional[str] = None
    
class GraphEdge(BaseModel):
    source: str
    target: str
    label: str
    
class AttackGraphResponse(BaseModel):
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)
