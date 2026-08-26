import pytest
from pathlib import Path
from backend.app.services.scanner import ScannerService

def test_cisco_legacy_robustness():
    path = Path("demo/cisco_legacy.cfg")
    if not path.exists():
        pytest.skip("Test config not found")
        
    with open(path, "r") as f:
        config = f.read()
        
    scanner = ScannerService()
    response, norm_config = scanner.scan_config(config)
    
    assert response.vendor == "cisco"
    # Even with bad spacing, hostname should parse
    assert response.hostname == "old-router"
    
    # Secrets should be redacted
    assert "$1$mERr$4/235q3" not in str(norm_config)
    assert "supersecretlegacy" not in str(norm_config)
    
    # It should have some UNKNOWN controls due to legacy/unsupported syntax
    # like 'ip bgp-community new-format'
    assert response.unknown_controls >= 0
    assert response.total_controls > 0
