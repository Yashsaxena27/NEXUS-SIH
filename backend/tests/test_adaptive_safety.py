import pytest
from backend.app.normalization.cisco_adapter import CiscoAdapter
from backend.app.schemas.security_ir import NormalizedConfig
from backend.app.db.models import AdaptiveRule
import time

def test_adaptive_rule_no_redos():
    """
    Ensure that adaptive rules cannot cause ReDoS because they use substring matching, 
    not regex evaluation.
    """
    adapter = CiscoAdapter()
    
    # A pattern that would cause catastrophic backtracking if used in regex
    malicious_pattern = r"(a+)+b"
    
    rule = AdaptiveRule(
        vendor="cisco",
        raw_pattern=malicious_pattern,
        mapped_control="management.ssh.enabled",
        mapped_value_json=True
    )
    
    # Create a string that would trigger ReDoS if regex was used
    raw_config = "a" * 50 + "c"
    
    start = time.perf_counter()
    result = adapter.normalize(raw_config, adaptive_rules=[rule])
    end = time.perf_counter()
    
    assert end - start < 0.1  # Must be instant
    assert result.config.management.ssh.enabled is False  # Didn't match

def test_adaptive_rule_precedence():
    """
    Ensure that if multiple rules match, they are evaluated deterministically.
    """
    adapter = CiscoAdapter()
    
    rule1 = AdaptiveRule(
        vendor="cisco",
        raw_pattern="ip ssh version 2",
        mapped_control="management.ssh.enabled",
        mapped_value_json=True
    )
    
    rule2 = AdaptiveRule(
        vendor="cisco",
        raw_pattern="ip ssh version 2",
        mapped_control="management.ssh.enabled",
        mapped_value_json=False
    )
    
    raw_config = "ip ssh version 2"
    
    # Passing them in order 1 then 2, 2 should win.
    result = adapter.normalize(raw_config, adaptive_rules=[rule1, rule2])
    assert result.config.management.ssh.enabled is False
    
    # Evidence should record both adaptive rules + the base parser's extraction
    assert len(result.evidence) == 3
