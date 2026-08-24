import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class ScanRecord(Base):
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    vendor = Column(String, nullable=False)
    platform = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    
    compliance_score = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    
    total_controls = Column(Integer, nullable=False)
    passed_controls = Column(Integer, nullable=False)
    failed_controls = Column(Integer, nullable=False)
    unknown_controls = Column(Integer, nullable=False)
    
    # Store the entire normalized IR as JSON for future reference
    normalized_config_json = Column(JSON, nullable=True)
    
    findings = relationship("FindingRecord", back_populates="scan", cascade="all, delete-orphan")

class FindingRecord(Base):
    __tablename__ = "findings"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    
    control_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)  # PASS, FAIL, UNKNOWN
    severity = Column(String, nullable=False)
    
    # Store evidence and context
    evidence_json = Column(JSON, nullable=True)
    explanation_context = Column(String, nullable=True)
    
    scan = relationship("ScanRecord", back_populates="findings")
