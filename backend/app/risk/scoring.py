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

def calculate_risk_score(findings: list[ComplianceFinding], asset_criticality: str = 'MEDIUM', exposure_factor: float = 1.0) -> float:
    '''
    Calculate weighted risk score factoring in asset criticality and exposure.
    '''
    if not findings:
        return 0.0
        
    criticality_multiplier = {
        'HIGH': 1.5,
        'MEDIUM': 1.0,
        'LOW': 0.5
    }.get(asset_criticality.upper(), 1.0)
        
    risk_sum = 0.0
    for finding in findings:
        if finding.status == ComplianceStatus.FAIL:
            base_risk = SEVERITY_WEIGHTS.get(finding.severity.value, 0)
            risk_sum += base_risk * criticality_multiplier * exposure_factor
            
    return float(risk_sum)

def calculate_prioritized_risks(findings: list[ComplianceFinding]) -> tuple[list[dict], str]:
    '''
    Groups failed findings by severity and category, prioritizing CRITICAL and HIGH.
    Generates a correlation summary.
    '''
    prioritized = []
    failed_findings = [f for f in findings if f.status == ComplianceStatus.FAIL]
    
    # Sort by severity weight descending
    failed_findings.sort(key=lambda x: SEVERITY_WEIGHTS.get(x.severity.value, 0), reverse=True)
    
    categories_hit = set()
    for f in failed_findings:
        prioritized.append({
            "control_id": f.control_id,
            "title": f.control_title,
            "severity": f.severity.value,
            "category": f.category
        })
        categories_hit.add(f.category)
        
    correlation_summary = ""
    if len(failed_findings) > 0:
        correlation_summary = f"Detected {len(failed_findings)} compliance failures spanning {len(categories_hit)} categories."
        if 'Secure Management' in categories_hit and 'Authentication' in categories_hit:
            correlation_summary += " High risk correlation: Weak authentication combined with insecure management protocols detected."
            
    return prioritized, correlation_summary
