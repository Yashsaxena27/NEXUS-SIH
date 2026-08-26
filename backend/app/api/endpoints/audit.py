from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import hashlib

from backend.app.db.session import get_db
from backend.app.db.models import ScanRecord
from backend.app.security.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

class AuditVerificationResponse(BaseModel):
    status: str  # "VERIFIED" or "TAMPER DETECTED"
    message: str
    tampered_scan_id: str | None = None

@router.get("/verify", response_model=AuditVerificationResponse, summary="Verify Tamper-Evident Audit Trail")
async def verify_audit_trail(db: AsyncSession = Depends(get_db)):
    """
    Sequentially recomputes the cryptographic hashes of all ScanRecords.
    Returns VERIFIED if the chain is fully intact.
    Returns TAMPER DETECTED if any payload or link in the chain is modified.
    """
    scans = await db.execute(select(ScanRecord).order_by(ScanRecord.created_at.asc()))
    scans = scans.scalars().all()
    
    if not scans:
        return AuditVerificationResponse(status="VERIFIED", message="Audit chain is empty.")
        
    expected_previous = "GENESIS"
    
    for scan in scans:
        # 1. Check link integrity
        if scan.previous_hash != expected_previous:
            return AuditVerificationResponse(
                status="TAMPER DETECTED",
                message=f"Broken hash chain link at scan {scan.id}",
                tampered_scan_id=scan.id
            )
            
        # 2. Check payload integrity
        canonical_payload = f"{scan.id}:{scan.compliance_score}:{scan.risk_score}:{expected_previous}"
        recomputed_hash = hashlib.sha256(canonical_payload.encode('utf-8')).hexdigest()
        
        if scan.current_hash != recomputed_hash:
            return AuditVerificationResponse(
                status="TAMPER DETECTED",
                message=f"Payload tampering detected at scan {scan.id}",
                tampered_scan_id=scan.id
            )
            
        expected_previous = scan.current_hash
        
    return AuditVerificationResponse(status="VERIFIED", message="All audit records successfully verified.")
