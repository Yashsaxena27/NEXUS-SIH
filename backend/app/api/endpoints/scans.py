from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from backend.app.core.logging import AuditLogger
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from backend.app.schemas.api import ScanRequest, ScanResultResponse, ScanSummaryResponse, ScanDetailResponse, FindingResponse, AttackGraphResponse, GraphNode, GraphEdge
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from backend.app.services.scanner import ScannerService
from backend.app.db.session import get_db
from backend.app.db.crud import save_scan_result, get_all_scans, get_scan_with_findings
from backend.app.security.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

# Dependency to get the scanner service
def get_scanner_service() -> ScannerService:
    return ScannerService()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@router.post("/scan", response_model=ScanResultResponse, summary="Scan a network configuration (raw text)")
async def scan_configuration(
    request: ScanRequest, 
    scanner: ScannerService = Depends(get_scanner_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Takes a raw network configuration string, detects the vendor, normalizes it, 
    evaluates it against deterministic compliance rules, and returns the result.
    """
    try:
        if not request.raw_config or not request.raw_config.strip():
            raise HTTPException(status_code=400, detail="raw_config cannot be empty")
            
        if len(request.raw_config) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Payload too large. Maximum size is 5MB.")
            
        for line in request.raw_config.splitlines():
            if len(line) > 10000:
                raise HTTPException(status_code=400, detail="Configuration contains excessively long lines.")
            
        from backend.app.db.models import AdaptiveRule
        from sqlalchemy.future import select
        rules_result = await db.execute(select(AdaptiveRule).where(AdaptiveRule.status == "APPROVED"))
        adaptive_rules = rules_result.scalars().all()
            
        AuditLogger.log_event("SCAN_STARTED", {"vendor_hint": request.vendor_hint})
        
        result, norm_config = scanner.scan_config(request.raw_config, request.vendor_hint, adaptive_rules)
        await save_scan_result(db, result, norm_config)
        
        AuditLogger.log_event("SCAN_COMPLETED", {"scan_id": result.scan_id, "vendor": result.vendor})
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal scanning error: {str(e)}")

@router.post("/upload", response_model=ScanResultResponse, summary="Upload and scan a config file")
async def upload_configuration(
    file: UploadFile = File(...),
    scanner: ScannerService = Depends(get_scanner_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a configuration file for scanning.
    Validates file size and empty contents.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB.")
        
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
    # Decode content safely
    try:
        raw_config = content.decode("utf-8")
    except UnicodeDecodeError:
        raw_config = content.decode("latin-1", errors="replace")
        
    if not raw_config.strip():
        raise HTTPException(status_code=400, detail="File contains no readable text.")
        
    # Prevent extremely long lines (ReDoS protection)
    for line in raw_config.splitlines():
        if len(line) > 10000:
            raise HTTPException(status_code=400, detail="Configuration contains excessively long lines.")

    try:
        from backend.app.db.models import AdaptiveRule
        from sqlalchemy.future import select
        rules_result = await db.execute(select(AdaptiveRule).where(AdaptiveRule.status == "APPROVED"))
        adaptive_rules = rules_result.scalars().all()
        
        result, norm_config = scanner.scan_config(raw_config, None, adaptive_rules)
        await save_scan_result(db, result, norm_config)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal scanning error: {str(e)}")


# === New Read Endpoints ===

@router.get("/", response_model=list[ScanSummaryResponse], summary="List all scans")
async def list_scans(db: AsyncSession = Depends(get_db)):
    """Get all scans ordered by most recent first."""
    scans = await get_all_scans(db)
    return [
        ScanSummaryResponse(
            scan_id=s.id,
            scan_name=s.scan_name,
            created_at=s.created_at.isoformat() if s.created_at else None,
            vendor=s.vendor,
            platform=s.platform,
            hostname=s.hostname,
            compliance_score=s.compliance_score,
            risk_score=s.risk_score,
            total_controls=s.total_controls,
            passed_controls=s.passed_controls,
            failed_controls=s.failed_controls,
            unknown_controls=s.unknown_controls,
            framework_alignments=s.framework_alignments_json or {}
        ) for s in scans
    ]

@router.get("/{scan_id}", response_model=ScanDetailResponse, summary="Get scan details")
async def get_scan(scan_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single scan with all its findings."""
    scan = await get_scan_with_findings(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    findings = []
    for f in scan.findings:
        findings.append(FindingResponse(
            control_id=f.control_id,
            title=f.title,
            status=f.status,
            severity=f.severity,
            category=f.category,
            frameworks=f.frameworks_json or [],
            framework_mappings=f.framework_mappings_json or [],
            expected=f.expected,
            actual=f.actual,
            evidence_field=f.evidence_json.get('evidence_field') if f.evidence_json else None,
            evidence_source=f.evidence_json.get('evidence_source') if f.evidence_json else None,
            evidence_raw=f.evidence_json.get('evidence_raw') if f.evidence_json else None,
            confidence=f.evidence_json.get('confidence', 1.0) if f.evidence_json else 1.0,
            remediation_hint=f.remediation_hint,
            explanation_context=f.explanation_context,
            exact_remediation=f.exact_remediation_json
        ))
    
    return ScanDetailResponse(
        scan_id=scan.id,
        scan_name=scan.scan_name,
        created_at=scan.created_at.isoformat() if scan.created_at else None,
        vendor=scan.vendor,
        platform=scan.platform,
        hostname=scan.hostname,
        compliance_score=scan.compliance_score,
        risk_score=scan.risk_score,
        total_controls=scan.total_controls,
        passed_controls=scan.passed_controls,
        failed_controls=scan.failed_controls,
        unknown_controls=scan.unknown_controls,
        findings=findings,
        vulnerabilities=scan.vulnerabilities_json or [],
        framework_alignments=scan.framework_alignments_json or {}
    )

@router.get("/{scan_id}/graph", response_model=AttackGraphResponse, summary="Get attack path graph")
async def get_scan_graph(scan_id: str, db: AsyncSession = Depends(get_db)):
    scan = await get_scan_with_findings(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    nodes = []
    edges = []
    
    # 1. Base Asset Node
    asset_id = scan.hostname or f"Device-{scan.vendor}"
    nodes.append(GraphNode(id=asset_id, label=asset_id, type="ASSET"))
    
    # 2. Internet / Exposure Node
    nodes.append(GraphNode(id="Internet", label="Internet", type="EXTERNAL"))
    edges.append(GraphEdge(source="Internet", target=asset_id, label="EXPOSED_TO"))
    
    # 3. Add vulnerabilities
    vulns = scan.vulnerabilities_json or []
    for v in vulns:
        cve_id = v.get("cve_id")
        if cve_id:
            nodes.append(GraphNode(id=cve_id, label=cve_id, type="VULNERABILITY", severity=v.get("severity")))
            edges.append(GraphEdge(source=asset_id, target=cve_id, label="HAS_VULNERABILITY"))
            
    # 4. Add high/critical findings and link them
    for f in scan.findings:
        if f.status == "FAIL" and f.severity in ["HIGH", "CRITICAL"]:
            nodes.append(GraphNode(id=f.control_id, label=f.title, type="FINDING", severity=f.severity))
            edges.append(GraphEdge(source=asset_id, target=f.control_id, label="HAS_FINDING"))
            
            # Create a correlated edge if vulnerability exists
            for v in vulns:
                cve_id = v.get("cve_id")
                if cve_id:
                    edges.append(GraphEdge(source=f.control_id, target=cve_id, label="CORRELATED_WITH"))

    return AttackGraphResponse(nodes=nodes, edges=edges)

@router.get("/{scan_id}/export/csv", summary="Export scan findings as CSV")
async def export_scan_csv(scan_id: str, db: AsyncSession = Depends(get_db)):
    scan = await get_scan_with_findings(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(["Scan ID", "Device", "Vendor", "Control ID", "Title", "Status", "Severity", "Category", "Frameworks", "Expected", "Actual", "Evidence Field"])
    
    # Data
    device_name = scan.hostname or f"{scan.vendor}-device"
    for f in scan.findings:
        frameworks = ", ".join(f.frameworks_json) if f.frameworks_json else ""
        evidence_field = f.evidence_json.get("evidence_field", "") if f.evidence_json else ""
        writer.writerow([
            scan.id,
            device_name,
            scan.vendor,
            f.control_id,
            f.title,
            f.status,
            f.severity,
            f.category or "",
            frameworks,
            f.expected or "",
            f.actual or "",
            evidence_field
        ])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=nexus_scan_{scan_id}.csv"}
    )
