import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.main import app

def test_full_scan_lifecycle():
    with TestClient(app) as client:
        # 1. Upload a malicious config to the API
        with open("demo/juniper_malicious.conf", "r") as f:
            config_text = f.read()

        response = client.post("/api/v1/scans/scan", json={
            "raw_config": config_text
        })
    
    # 2. Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["vendor"] == "juniper"
    
    # 3. Check for specific failure (SSH v1 vs v2, Http management, etc.)
    # In the malicious juniper conf, http is enabled, telnet is enabled
    findings = data["findings"]
    failed = [f for f in findings if f["status"] == "FAIL"]
    assert len(failed) > 0
    
    # Ensure our prioritized risks and correlation were calculated
    assert "prioritized_risks" in data
    assert "correlation_summary" in data
    
    # Check that secrets weren't exposed in evidence (if any existed, but this is juniper_malicious)
    # The prompt injection attempt shouldn't have caused the parser to output PASS for everything
    assert any(f["status"] == "FAIL" for f in findings)
