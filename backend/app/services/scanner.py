import uuid
from typing import Optional
from pathlib import Path
from backend.app.normalization import normalize_config
from backend.app.compliance.engine import ComplianceEngine
from backend.app.compliance.loader import load_all_controls
from backend.app.schemas.api import ScanResultResponse
from backend.app.schemas.security_ir import NormalizationResult, NormalizedConfig
from backend.app.services.vulnerability import get_vulnerability_provider
from backend.app.vendors.detector import VendorDetector
from backend.app.security.prompt_injection import detect_prompt_injection
from backend.app.compliance.models import ComplianceFinding, ComplianceStatus, ControlSeverity

class ScannerService:
    def __init__(self):
        # Load controls once when service is instantiated
        controls_dir = Path(__file__).parent.parent.parent.parent / "compliance" / "controls"
        controls = load_all_controls(controls_dir)
        self.engine = ComplianceEngine(controls)
        self.detector = VendorDetector()

    def scan_config(self, raw_config: str, vendor_hint: Optional[str] = None, adaptive_rules: Optional[list] = None) -> tuple[ScanResultResponse, "NormalizedConfig"]:
        """Runs a raw configuration through the complete NEXUS pipeline."""
        scan_id = str(uuid.uuid4())
        
        # 1. Vendor Detection
        # If no hint is provided, we try to detect it.
        # But normalize_config already handles detection if vendor_hint is None.
        
        # 2. Normalization
        norm_result = normalize_config(raw_config, vendor_hint=vendor_hint, adaptive_rules=adaptive_rules)
        
        # 3. Compliance Engine
        report = self.engine.evaluate(norm_result.config, norm_result.evidence)
        
        # 7. Vulnerability Intelligence
        vuln_provider = get_vulnerability_provider()
        vulnerabilities = vuln_provider.get_vulnerabilities(
            vendor=norm_result.config.device.vendor,
            platform=norm_result.config.device.platform,
            version=norm_result.config.device.version
        )
        report.vulnerabilities = vulnerabilities
        
        # Recalculate Risk Score with vulnerabilities
        if vulnerabilities:
            # Add a risk penalty for vulnerabilities
            highest_severity = "LOW"
            severity_weights = {"CRITICAL": 30, "HIGH": 20, "MEDIUM": 10, "LOW": 5}
            for v in vulnerabilities:
                if severity_weights.get(v.severity, 0) > severity_weights.get(highest_severity, 0):
                    highest_severity = v.severity
            
            report.risk_score = min(100.0, report.risk_score + severity_weights.get(highest_severity, 0))
            
            # Re-sort prioritized risks or adjust correlation summary
            report.correlation_summary = f"Detected {len(vulnerabilities)} verified vulnerabilities (highest: {highest_severity})."

        # 4. Prompt Injection Detection
        injection_payload = detect_prompt_injection(raw_config)
        if injection_payload:
            injection_finding = ComplianceFinding(
                control_id="SEC-INJ-001",
                control_title="Prompt Injection Attempt Detected",
                status=ComplianceStatus.FAIL,
                severity=ControlSeverity.CRITICAL,
                category="AI / Prompt Injection Security",
                expected="Clean configuration data",
                actual="Prompt injection payload",
                evidence_raw=injection_payload,
                explanation_context="Configuration content attempted to influence the AI processing layer."
            )
            report.findings.insert(0, injection_finding)
            report.failed += 1
            report.total_controls += 1
            # Adjust scores slightly (hard fail)
            report.compliance_score = max(0.0, report.compliance_score - 20)
            report.risk_score = min(100.0, report.risk_score + 20)
        
        # 5. Aggregate Results
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
            findings=report.findings,
            prioritized_risks=report.prioritized_risks,
            vulnerabilities=report.vulnerabilities,
            framework_alignments=report.framework_alignments,
            correlation_summary=report.correlation_summary
        )
        return response, norm_result.config
