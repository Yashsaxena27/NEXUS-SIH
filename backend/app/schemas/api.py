from typing import Optional, List
from pydantic import BaseModel, Field
from backend.app.compliance.models import ComplianceFinding

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "0.1.0"

class ScanRequest(BaseModel):
    raw_config: str = Field(..., description="The raw configuration text to scan")
    vendor_hint: Optional[str] = Field(None, description="Optional vendor hint (e.g., 'cisco', 'juniper')")

class ScanResultResponse(BaseModel):
    scan_id: str = Field(..., description="Unique identifier for this scan")
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
