import uuid
from typing import Optional
from pathlib import Path
from backend.app.normalization import normalize_config
from backend.app.compliance.engine import ComplianceEngine
from backend.app.compliance.loader import load_all_controls
from backend.app.schemas.api import ScanResultResponse
from backend.app.vendors.detector import VendorDetector

class ScannerService:
    def __init__(self):
        # Load controls once when service is instantiated
        controls_dir = Path(__file__).parent.parent.parent.parent / "compliance" / "controls"
        controls = load_all_controls(controls_dir)
        self.engine = ComplianceEngine(controls)
        self.detector = VendorDetector()

    def scan_config(self, raw_config: str, vendor_hint: Optional[str] = None) -> tuple[ScanResultResponse, "NormalizedConfig"]:
        """Runs a raw configuration through the complete NEXUS pipeline."""
        scan_id = str(uuid.uuid4())
        
        # 1. Vendor Detection
        # If no hint is provided, we try to detect it.
        # But normalize_config already handles detection if vendor_hint is None.
        
        # 2. Normalization
        norm_result = normalize_config(raw_config, vendor_hint=vendor_hint)
        
        # 3. Compliance Engine
        report = self.engine.evaluate(norm_result.config, norm_result.evidence)
        
        # 4. Aggregate Results
        total = len(report.findings)
        passed = sum(1 for f in report.findings if f.status.value == "PASS")
        failed = sum(1 for f in report.findings if f.status.value == "FAIL")
        unknown = sum(1 for f in report.findings if f.status.value.startswith("UNKNOWN"))
        
        response = ScanResultResponse(
            scan_id=scan_id,
            vendor=report.device_vendor or "unknown",
            platform=norm_result.config.device.platform if norm_result.config.device else None,
            hostname=norm_result.config.device.hostname if norm_result.config.device else None,
            compliance_score=report.compliance_score,
            risk_score=report.risk_score,
            total_controls=total,
            passed_controls=passed,
            failed_controls=failed,
            unknown_controls=unknown,
            findings=report.findings
        )
        return response, norm_result.config
