import pytest
from backend.app.llm.prompts import EXPLANATION_PROMPT

def test_explanation_prompt_structure():
    """Ensure the explanation prompt contains the required structural markers."""
    assert "### 1. Evidence" in EXPLANATION_PROMPT
    assert "### 2. Interpretation" in EXPLANATION_PROMPT
    assert "### 3. Recommendation" in EXPLANATION_PROMPT
    assert "### 4. Verification" in EXPLANATION_PROMPT

def test_prompt_formatting_args():
    """Ensure the prompt formatting arguments match the expected inputs."""
    # Attempt to format the prompt to ensure no KeyError on missing fields
    formatted = EXPLANATION_PROMPT.format(
        device_os="Cisco IOS",
        control_id="CIS-1.1",
        control_title="SSH Version 2",
        severity="HIGH",
        expected="2",
        actual="1",
        evidence="ip ssh version 1",
        context="Must use SSHv2",
        rag_knowledge="None",
        asset_criticality="HIGH",
        exposure_factor=1.5
    )
    assert "Cisco IOS" in formatted
    assert "CIS-1.1" in formatted
