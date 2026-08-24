from typing import Any, Optional
from backend.app.schemas.security_ir import NormalizedConfig, PropertyEvidence
from backend.app.compliance.models import (
    ComplianceControl, ComplianceFinding, ComplianceStatus, ControlOperator, ComplianceReport
)
from backend.app.risk.scoring import calculate_compliance_score, calculate_risk_score

class ComplianceEngine:
    def __init__(self, controls: list[ComplianceControl]):
        self.controls = controls
    
    def evaluate(self, config: NormalizedConfig, evidence: list[PropertyEvidence] = None) -> ComplianceReport:
        '''Evaluate all controls against a normalized config.'''
        evidence = evidence or []
        findings = []
        passed = 0
        failed = 0
        unknown = 0
        
        for control in self.controls:
            finding = self.evaluate_control(control, config, evidence)
            findings.append(finding)
            if finding.status == ComplianceStatus.PASS:
                passed += 1
            elif finding.status == ComplianceStatus.FAIL:
                failed += 1
            else:
                unknown += 1
                
        compliance_score = calculate_compliance_score(findings)
        risk_score = calculate_risk_score(findings)
        
        return ComplianceReport(
            device_vendor=config.device.vendor,
            device_hostname=config.device.hostname,
            device_platform=config.device.platform,
            total_controls=len(self.controls),
            passed=passed,
            failed=failed,
            unknown=unknown,
            compliance_score=compliance_score,
            risk_score=risk_score,
            findings=findings
        )
    
    def evaluate_control(self, control: ComplianceControl, config: NormalizedConfig, evidence: list[PropertyEvidence] = None) -> ComplianceFinding:
        '''Evaluate a single control.'''
        evidence = evidence or []
        req = control.requirement
        actual, found = self._resolve_field(config, req.field)
        
        if not found or actual is None:
            if req.operator == ControlOperator.NOT_EXISTS:
                status = ComplianceStatus.PASS
            else:
                status = ComplianceStatus.UNKNOWN
        else:
            status = self._evaluate_operator(actual, req.operator, req.value, req.value_max)
            
        ev = next((e for e in evidence if e.field == req.field), None)
        evidence_source = ev.source if ev else None
        evidence_raw = ev.raw_evidence if ev else None
        confidence = ev.confidence if ev else 1.0
        
        explanation_context = f"Control {control.id} ({control.title}) requires {req.field} to be {req.value}, but actual value is {actual}."
        if control.description:
            explanation_context += f"\nDescription: {control.description}"
        if control.frameworks:
            explanation_context += f"\nFrameworks: {', '.join(control.frameworks)}"
        if ev and ev.source:
            explanation_context += f"\nEvidence from {ev.source}: '{ev.raw_evidence}'"
            
        return ComplianceFinding(
            control_id=control.id,
            control_title=control.title,
            status=status,
            severity=control.severity,
            category=control.category,
            frameworks=control.frameworks,
            expected=req.value,
            actual=actual,
            evidence_field=req.field,
            evidence_source=evidence_source,
            evidence_raw=evidence_raw,
            confidence=confidence,
            remediation_hint=control.remediation_hint,
            explanation_context=explanation_context
        )
    
    def _resolve_field(self, config: NormalizedConfig, field_path: str) -> tuple[Any, bool]:
        '''Navigate dot-path to get value. Returns (value, found).'''
        parts = field_path.split('.')
        current = config
        for part in parts:
            if isinstance(current, dict):
                if part in current:
                    current = current[part]
                else:
                    return None, False
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None, False
        return current, True
    
    def _evaluate_operator(self, actual, operator: ControlOperator, expected, expected_max=None) -> ComplianceStatus:
        '''Apply operator comparison. Return PASS/FAIL/UNKNOWN.'''
        try:
            if operator == ControlOperator.EQUALS:
                return ComplianceStatus.PASS if actual == expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.NOT_EQUALS:
                return ComplianceStatus.PASS if actual != expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.GREATER_THAN:
                return ComplianceStatus.PASS if actual > expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.LESS_THAN:
                return ComplianceStatus.PASS if actual < expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.GREATER_EQUAL:
                return ComplianceStatus.PASS if actual >= expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.LESS_EQUAL:
                return ComplianceStatus.PASS if actual <= expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.IN_RANGE:
                if expected is not None and expected_max is not None:
                    return ComplianceStatus.PASS if expected <= actual <= expected_max else ComplianceStatus.FAIL
                return ComplianceStatus.UNKNOWN
            elif operator == ControlOperator.EXISTS:
                if isinstance(actual, str) and not actual.strip():
                    return ComplianceStatus.FAIL
                return ComplianceStatus.PASS if actual is not None else ComplianceStatus.FAIL
            elif operator == ControlOperator.NOT_EXISTS:
                return ComplianceStatus.PASS if actual is None else ComplianceStatus.FAIL
            elif operator == ControlOperator.CONTAINS:
                return ComplianceStatus.PASS if expected in actual else ComplianceStatus.FAIL
            elif operator == ControlOperator.NOT_CONTAINS:
                return ComplianceStatus.PASS if expected not in actual else ComplianceStatus.FAIL
            elif operator == ControlOperator.IN_SET:
                return ComplianceStatus.PASS if actual in expected else ComplianceStatus.FAIL
            elif operator == ControlOperator.NOT_IN_SET:
                return ComplianceStatus.PASS if actual not in expected else ComplianceStatus.FAIL
            else:
                return ComplianceStatus.UNKNOWN
        except TypeError:
            return ComplianceStatus.UNKNOWN
