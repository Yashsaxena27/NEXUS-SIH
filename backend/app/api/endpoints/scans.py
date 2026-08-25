from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from backend.app.schemas.api import ScanRequest, ScanResultResponse, ScanSummaryResponse, ScanDetailResponse, FindingResponse
from backend.app.services.scanner import ScannerService
from backend.app.db.session import get_db
from backend.app.db.crud import save_scan_result, get_all_scans, get_scan_with_findings

router = APIRouter()

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
            
        result, norm_config = scanner.scan_config(request.raw_config, request.vendor_hint)
        await save_scan_result(db, result, norm_config)
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

    try:
        result, norm_config = scanner.scan_config(raw_config)
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
            expected=f.expected,
            actual=f.actual,
            evidence_field=f.evidence_json.get('evidence_field') if f.evidence_json else None,
            evidence_source=f.evidence_json.get('evidence_source') if f.evidence_json else None,
            evidence_raw=f.evidence_json.get('evidence_raw') if f.evidence_json else None,
            confidence=f.evidence_json.get('confidence', 1.0) if f.evidence_json else 1.0,
            remediation_hint=f.remediation_hint,
            explanation_context=f.explanation_context,
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
    )
