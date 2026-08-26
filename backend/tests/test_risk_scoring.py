import pytest
from backend.app.risk.scoring import calculate_risk_score, calculate_compliance_score, calculate_prioritized_risks
from backend.app.compliance.models import ComplianceFinding, ComplianceStatus, ControlSeverity

def _make_finding(severity, status=ComplianceStatus.FAIL, category="General"):
    return ComplianceFinding(
        control_id="TEST-001",
        control_title="Test",
        status=status,
        severity=severity,
        expected=True,
        actual=False,
        evidence_field="test",
        evidence_source="test",
        evidence_raw="test",
        category=category
    )

def test_risk_scoring_boundary_conditions():
    findings_critical = [_make_finding(ControlSeverity.CRITICAL)]
    
    # Max risk case: Critical severity (10), High criticality (1.5), 1.5 exposure
    # 10 * 1.5 * 1.5 = 22.5
    score_max = calculate_risk_score(
        findings=findings_critical,
        asset_criticality="HIGH",
        exposure_factor=1.5
    )
    assert score_max == 22.5
    
    findings_low = [_make_finding(ControlSeverity.LOW)]
    # Min risk case: Low severity (1), Low criticality (0.5), 0.5 exposure
    # 1 * 0.5 * 0.5 = 0.25
    score_min = calculate_risk_score(
        findings=findings_low,
        asset_criticality="LOW",
        exposure_factor=0.5
    )
    assert score_min == 0.25
    
    # Fallback / Default case
    score_default = calculate_risk_score(
        findings=findings_low,
        asset_criticality="GARBAGE", # Defaults to 1.0
        exposure_factor=1.0
    )
    assert score_default == 1.0

def test_finding_correlation():
    f1 = _make_finding(ControlSeverity.CRITICAL, category="Secure Management")
    f2 = _make_finding(ControlSeverity.HIGH, category="Authentication")
    f3 = _make_finding(ControlSeverity.LOW, category="Logging")
    
    prioritized, summary = calculate_prioritized_risks([f1, f2, f3])
    
    # Check prioritization sorting (Critical -> High -> Low)
    assert prioritized[0]["severity"] == "CRITICAL"
    assert prioritized[1]["severity"] == "HIGH"
    assert prioritized[2]["severity"] == "LOW"
    
    # Check correlation logic
    assert "High risk correlation: Weak authentication combined with insecure management protocols detected." in summary
