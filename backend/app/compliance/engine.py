from typing import Any, Optional
from backend.app.schemas.security_ir import NormalizedConfig, PropertyEvidence
from backend.app.compliance.models import (
    ComplianceControl, ComplianceFinding, ComplianceStatus, ControlOperator, ComplianceReport, ExactRemediation
)
from backend.app.risk.scoring import calculate_compliance_score, calculate_risk_score, calculate_prioritized_risks
from backend.app.compliance.remediation import get_exact_remediation

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
        
        # Calculate framework alignments
        framework_alignments = {}
        framework_totals = {}
        framework_passed = {}
        
        for control in self.controls:
            for mapping in control.framework_mappings:
                fw = mapping.framework
                if fw not in framework_totals:
                    framework_totals[fw] = 0
                    framework_passed[fw] = 0
                framework_totals[fw] += 1
                
        for finding in findings:
            if finding.status == ComplianceStatus.PASS:
                for mapping in finding.framework_mappings:
                    fw = mapping.framework
                    framework_passed[fw] += 1
                    
        for fw, total in framework_totals.items():
            if total > 0:
                framework_alignments[fw] = round((framework_passed[fw] / total) * 100, 1)
        
        # We'll calculate risk score and prioritized risks later in the scanner once vulnerabilities are fetched.
        # But we can calculate a base risk score here.
        risk_score = calculate_risk_score(
            findings, 
            asset_criticality=config.device.asset_criticality,
            exposure_factor=config.device.exposure_factor
        )
        
        prioritized, correlation = calculate_prioritized_risks(findings)
        
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
            findings=findings,
            prioritized_risks=prioritized,
            framework_alignments=framework_alignments,
            vulnerabilities=[], # To be populated by scanner
            correlation_summary=correlation
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
                status = ComplianceStatus.UNKNOWN_ABSENT
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
            
        exact_remediation = None
        if status == ComplianceStatus.FAIL:
            exact_remediation = get_exact_remediation(control.id, config.device.vendor)
            
        return ComplianceFinding(
            control_id=control.id,
            control_title=control.title,
            status=status,
            severity=control.severity,
            category=control.category,
            frameworks=control.frameworks,
            framework_mappings=control.framework_mappings,
            expected=req.value,
            actual=actual,
            evidence_field=req.field,
            evidence_source=evidence_source,
            evidence_raw=evidence_raw,
            confidence=confidence,
            remediation_hint=control.remediation_hint,
            explanation_context=explanation_context,
            exact_remediation=exact_remediation
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
