import pytest
from pathlib import Path
from backend.app.normalization import normalize_config

FIXTURES_DIR = Path(__file__).parent.parent.parent / "evaluation" / "fixtures"

def test_cisco_edge_case_1():
    with open(FIXTURES_DIR / "cisco" / "edge_cases" / "cisco_edge_1.txt", "r") as f:
        raw = f.read()
    
    result = normalize_config(raw, vendor_hint="cisco")
    c = result.config
    
    # Check that unusual spacing was handled
    assert c.device.hostname == "CISCO-EDGE-1"
    assert c.management.ssh.version == 2
    assert c.management.telnet.enabled is True # transport input ssh telnet
    assert c.management.session_timeout == 0 # exec-timeout 0 0

def test_juniper_edge_case_1():
    with open(FIXTURES_DIR / "juniper" / "edge_cases" / "juniper_edge_1.txt", "r") as f:
        raw = f.read()
        
    result = normalize_config(raw, vendor_hint="juniper")
    c = result.config
    
    # Nested braces on one line and comments
    assert c.device.hostname == "JUNIPER-EDGE-1"
    assert c.management.ssh.version == 2
    assert c.management.telnet.enabled is True
    assert c.management.session_timeout == 1800 # idle-timeout 30 (30 * 60)
    assert c.snmp.default_community is True # community public

def test_fortinet_edge_case_1():
    with open(FIXTURES_DIR / "fortinet" / "edge_cases" / "forti_edge_1.txt", "r") as f:
        raw = f.read()
        
    result = normalize_config(raw, vendor_hint="fortinet")
    c = result.config
    
    assert c.device.hostname == "FORTI-EDGE"
    assert c.management.session_timeout == 0
    assert c.logging.syslog.enabled is False
    assert c.snmp.default_community is True

def test_paloalto_edge_case_1():
    with open(FIXTURES_DIR / "paloalto" / "edge_cases" / "pa_edge_1.txt", "r") as f:
        raw = f.read()
        
    result = normalize_config(raw, vendor_hint="paloalto")
    c = result.config
    
    assert c.device.hostname == "PA-EDGE-1"
    assert c.management.telnet.enabled is True # disable-telnet no
    assert c.services.http_server_enabled is True # disable-http no
    assert c.management.login_banner == ""
