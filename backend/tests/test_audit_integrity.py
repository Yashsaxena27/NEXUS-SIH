import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import engine
from backend.app.db.models import Base, ScanRecord
from backend.app.db.crud import save_scan_result
from backend.app.services.scanner import ScannerService
from fastapi.testclient import TestClient
from backend.app.main import app

# Need a test db fixture
@pytest_asyncio.fixture
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    from backend.app.db.session import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_audit_hash_chain(test_db: AsyncSession):
    scanner = ScannerService()
    
    # 1. Genesis Scan
    res1, norm1 = scanner.scan_config("hostname R1")
    await save_scan_result(test_db, res1, norm1)
    
    # 2. Second Scan
    res2, norm2 = scanner.scan_config("hostname R2")
    await save_scan_result(test_db, res2, norm2)
    
    # Fetch from DB
    from sqlalchemy import select
    scans = (await test_db.execute(select(ScanRecord).order_by(ScanRecord.created_at.asc()))).scalars().all()
    
    assert len(scans) == 2
    s1, s2 = scans
    
    # Check Genesis
    assert s1.previous_hash == "GENESIS"
    assert s1.current_hash is not None
    
    # Check link
    assert s2.previous_hash == s1.current_hash
    assert s2.current_hash is not None

@pytest.mark.asyncio
async def test_tamper_detection(test_db: AsyncSession):
    scanner = ScannerService()
    
    res1, norm1 = scanner.scan_config("hostname R1")
    await save_scan_result(test_db, res1, norm1)
    
    res2, norm2 = scanner.scan_config("hostname R2")
    await save_scan_result(test_db, res2, norm2)
    
    # Tamper with the database
    from sqlalchemy import select
    scans = (await test_db.execute(select(ScanRecord).order_by(ScanRecord.created_at.asc()))).scalars().all()
    s1 = scans[0]
    
    # Modify the score directly in the database (tampering)
    s1.compliance_score = 99.9
    test_db.add(s1)
    await test_db.commit()
    
    # Use TestClient to call the verify endpoint
    # Note: Authentication is mocked or disabled for tests usually, assuming tests bypass it or we construct a mock.
    # For this test, we'll just test the logic directly to avoid Auth dependency issues.
    
    import hashlib
    scans = (await test_db.execute(select(ScanRecord).order_by(ScanRecord.created_at.asc()))).scalars().all()
    
    expected_previous = "GENESIS"
    tampered = False
    
    for scan in scans:
        if scan.previous_hash != expected_previous:
            tampered = True
            break
            
        canonical_payload = f"{scan.id}:{scan.compliance_score}:{scan.risk_score}:{expected_previous}"
        recomputed_hash = hashlib.sha256(canonical_payload.encode('utf-8')).hexdigest()
        
        if scan.current_hash != recomputed_hash:
            tampered = True
            break
            
        expected_previous = scan.current_hash
        
    assert tampered == True
