from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from backend.app.schemas.api import ScanRequest, ScanResultResponse
from backend.app.services.scanner import ScannerService
from backend.app.db.session import get_db
from backend.app.db.crud import save_scan_result

router = APIRouter()

# Dependency to get the scanner service (can be replaced with DI container later)
def get_scanner_service() -> ScannerService:
    return ScannerService()

@router.post("/scan", response_model=ScanResultResponse, summary="Scan a network configuration")
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
        
        # Save to database
        await save_scan_result(db, result, norm_config)
        
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Avoid leaking internal error details directly in production, but okay for MVP
        raise HTTPException(status_code=500, detail=f"Internal scanning error: {str(e)}")
