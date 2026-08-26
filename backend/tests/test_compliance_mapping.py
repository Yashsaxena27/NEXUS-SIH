import pytest
from pathlib import Path
from backend.app.compliance.loader import load_all_controls
from backend.app.compliance.engine import ComplianceEngine
from backend.app.schemas.security_ir import NormalizedConfig, DeviceInfo
from backend.app.compliance.models import ComplianceStatus

def test_framework_mappings_loaded():
    controls_dir = Path(__file__).parent.parent.parent / "compliance" / "controls"
    controls = load_all_controls(controls_dir)
    
    # Verify that at least one control has framework mappings
    has_mappings = any(len(c.framework_mappings) > 0 for c in controls)
    assert has_mappings, "No framework mappings found in loaded controls"

def test_framework_alignments_calculated():
    controls_dir = Path(__file__).parent.parent.parent / "compliance" / "controls"
    controls = load_all_controls(controls_dir)
    engine = ComplianceEngine(controls)
    
    # Mock config that should pass some controls
    config = NormalizedConfig(
        device=DeviceInfo(vendor="cisco", hostname="router1", platform="ios", version="15.2"),
        authentication={"ssh": {"enabled": True, "version": "2"}},
        logging={"syslog_servers": ["10.0.0.1"]}
    )
    
    report = engine.evaluate(config)
    
    # Check that framework alignments are calculated and present
    assert report.framework_alignments is not None
    assert isinstance(report.framework_alignments, dict)
    assert len(report.framework_alignments) > 0
    
    # Ensure some score is calculated
    assert any(score > 0 for score in report.framework_alignments.values())
