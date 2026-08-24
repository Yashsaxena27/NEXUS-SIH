from backend.app.compliance.models import ComplianceFinding, ComplianceStatus

SEVERITY_WEIGHTS = {
    'CRITICAL': 10,
    'HIGH': 5,
    'MEDIUM': 2,
    'LOW': 1,
    'INFORMATIONAL': 0,
}

def calculate_compliance_score(findings: list[ComplianceFinding]) -> float:
    '''Calculate 0-100 compliance score.'''
    if not findings:
        return 100.0
        
    penalty = 0
    for finding in findings:
        if finding.status == ComplianceStatus.FAIL:
            penalty += SEVERITY_WEIGHTS.get(finding.severity.value, 0)
            
    score = 100.0 - penalty
    return float(max(0.0, score))

def calculate_risk_score(findings: list[ComplianceFinding], asset_criticality: int = 5) -> float:
    '''Calculate weighted risk score.'''
    if not findings:
        return 0.0
        
    risk_sum = 0
    for finding in findings:
        if finding.status == ComplianceStatus.FAIL:
            risk_sum += SEVERITY_WEIGHTS.get(finding.severity.value, 0)
            
    return float(risk_sum * asset_criticality)
