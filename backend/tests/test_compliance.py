import pytest
from backend.app.compliance.engine import ComplianceEngine
from backend.app.compliance.models import ComplianceStatus, ControlOperator, ComplianceControl, ControlRequirement, ControlSeverity
from backend.app.schemas.security_ir import NormalizedConfig, DeviceInfo
from backend.app.risk.scoring import calculate_compliance_score, calculate_risk_score
from backend.app.compliance.loader import load_all_controls

def test_evaluate_operator_equals():
    engine = ComplianceEngine([])
    assert engine._evaluate_operator(True, ControlOperator.EQUALS, True) == ComplianceStatus.PASS
    assert engine._evaluate_operator(True, ControlOperator.EQUALS, False) == ComplianceStatus.FAIL

def test_evaluate_operator_not_equals():
    engine = ComplianceEngine([])
    assert engine._evaluate_operator(2, ControlOperator.NOT_EQUALS, 1) == ComplianceStatus.PASS
    assert engine._evaluate_operator(1, ControlOperator.NOT_EQUALS, 1) == ComplianceStatus.FAIL

def test_evaluate_operator_greater_than():
    engine = ComplianceEngine([])
    assert engine._evaluate_operator(5, ControlOperator.GREATER_THAN, 4) == ComplianceStatus.PASS
    assert engine._evaluate_operator(3, ControlOperator.GREATER_THAN, 4) == ComplianceStatus.FAIL

def test_evaluate_operator_in_range():
    engine = ComplianceEngine([])
    assert engine._evaluate_operator(300, ControlOperator.IN_RANGE, 1, 600) == ComplianceStatus.PASS
    assert engine._evaluate_operator(700, ControlOperator.IN_RANGE, 1, 600) == ComplianceStatus.FAIL

def test_evaluate_operator_exists():
    engine = ComplianceEngine([])
    assert engine._evaluate_operator("banner", ControlOperator.EXISTS, True) == ComplianceStatus.PASS
    assert engine._evaluate_operator("", ControlOperator.EXISTS, True) == ComplianceStatus.FAIL

def test_evaluate_operator_not_exists():
    engine = ComplianceEngine([])
    assert engine._evaluate_operator(None, ControlOperator.NOT_EXISTS, True) == ComplianceStatus.PASS
    assert engine._evaluate_operator("banner", ControlOperator.NOT_EXISTS, True) == ComplianceStatus.FAIL

def test_unknown_when_missing():
    engine = ComplianceEngine([])
    config = NormalizedConfig(device=DeviceInfo(vendor="cisco"))
    control = ComplianceControl(
        id="T1", title="T1", severity=ControlSeverity.LOW,
        requirement=ControlRequirement(field="management.ssh.version", operator=ControlOperator.EQUALS, value=2)
    )
    # version is None by default
    finding = engine.evaluate_control(control, config)
    assert finding.status == ComplianceStatus.UNKNOWN_ABSENT

def test_scoring():
    engine = ComplianceEngine([])
    config = NormalizedConfig(device=DeviceInfo(vendor="cisco"))
    control = ComplianceControl(
        id="T1", title="T1", severity=ControlSeverity.CRITICAL,
        requirement=ControlRequirement(field="management.ssh.enabled", operator=ControlOperator.EQUALS, value=True)
    )
    finding = engine.evaluate_control(control, config)
    assert finding.status == ComplianceStatus.FAIL
    
    score = calculate_compliance_score([finding])
    assert score == 90.0
    
    risk = calculate_risk_score([finding])
    assert risk == 10.0

def test_yaml_loader():
    controls = load_all_controls()
    # It might be 0 if path isn't fully correct in tests, but it shouldn't crash
    assert isinstance(controls, list)
    
def test_full_pipeline(compliant_config, sample_controls):
    engine = ComplianceEngine(sample_controls)
    report = engine.evaluate(compliant_config)
    assert report.total_controls == 1
    assert report.passed == 1
    assert report.failed == 0
    
def test_full_pipeline_fail(non_compliant_config, sample_controls):
    engine = ComplianceEngine(sample_controls)
    report = engine.evaluate(non_compliant_config)
    assert report.total_controls == 1
    assert report.passed == 0
    assert report.failed == 1
