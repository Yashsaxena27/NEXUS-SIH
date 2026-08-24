from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.api import ScanResultResponse
from backend.app.db.models import ScanRecord, FindingRecord
from backend.app.schemas.security_ir import NormalizedConfig

async def save_scan_result(db: AsyncSession, scan_result: ScanResultResponse, normalized_config: NormalizedConfig = None):
    """Saves a ScanResultResponse and its findings to the database."""
    
    scan_record = ScanRecord(
        id=scan_result.scan_id,
        vendor=scan_result.vendor,
        platform=scan_result.platform,
        hostname=scan_result.hostname,
        compliance_score=scan_result.compliance_score,
        risk_score=scan_result.risk_score,
        total_controls=scan_result.total_controls,
        passed_controls=scan_result.passed_controls,
        failed_controls=scan_result.failed_controls,
        unknown_controls=scan_result.unknown_controls,
        normalized_config_json=normalized_config.model_dump() if normalized_config else None
    )
    
    db.add(scan_record)
    
    for finding in scan_result.findings:
        finding_record = FindingRecord(
            scan_id=scan_result.scan_id,
            control_id=finding.control_id,
            title=finding.control_title,
            status=finding.status.value,
            severity=finding.severity.value,
            evidence_json={
                "evidence_field": finding.evidence_field,
                "evidence_source": finding.evidence_source,
                "evidence_raw": finding.evidence_raw,
                "confidence": finding.confidence
            },
            explanation_context=finding.explanation_context
        )
        db.add(finding_record)
        
    await db.commit()
    return scan_record
