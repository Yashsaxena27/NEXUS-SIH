import pytest
from backend.app.compliance.remediation import get_exact_remediation
from backend.app.services.scanner import ScannerService
from backend.app.compliance.models import ComplianceStatus

def test_remediation_retrieval():
    remediation = get_exact_remediation("NET-SSH-001", "cisco")
    assert remediation is not None
    assert remediation.vendor == "cisco"
    assert "transport input ssh" in remediation.vendor_cli
    
    # Non-existent control
    assert get_exact_remediation("NOT-A-CONTROL", "cisco") is None
    
    # Non-existent vendor for a valid control
    assert get_exact_remediation("NET-SSH-001", "unknown_vendor") is None

def test_remediation_attached_on_fail():
    scanner = ScannerService()
    # A config that fails NET-SSH-001 (telnet enabled)
    raw_config = """
    hostname Router1
    !
    line vty 0 4
     transport input all
    """
    
    result, _ = scanner.scan_config(raw_config, vendor_hint="cisco")
    
    finding = next(f for f in result.findings if f.control_id == "NET-SSH-001")
    assert finding.status == ComplianceStatus.FAIL
    assert finding.exact_remediation is not None
    assert finding.exact_remediation.vendor == "cisco"
    assert "transport input ssh" in finding.exact_remediation.vendor_cli

def test_remediation_not_attached_on_pass():
    scanner = ScannerService()
    # A config that passes NET-SSH-001
    raw_config = """
    hostname Router1
    !
    line vty 0 4
     transport input ssh
    """
    
    result, _ = scanner.scan_config(raw_config, vendor_hint="cisco")
    
    finding = next(f for f in result.findings if f.control_id == "NET-SSH-001")
    assert finding.status == ComplianceStatus.PASS
    assert finding.exact_remediation is None
