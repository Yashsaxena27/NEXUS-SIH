from typing import Optional
from backend.app.compliance.models import ExactRemediation

# A simple registry for vendor-specific remediation templates.
# In a full production system, this could be loaded from YAML/JSON.

_REMEDIATION_DB: dict[str, dict[str, ExactRemediation]] = {
    "NET-SSH-001": {
        "cisco": ExactRemediation(
            problem_description="Telnet is an unencrypted protocol. Credentials and data are transmitted in plaintext.",
            remediation_explanation="Disable Telnet on all VTY lines and enforce SSH only.",
            vendor="cisco",
            vendor_cli="line vty 0 4\n transport input ssh\nno service telnet",
            human_approval_required=True,
            safe_guidance="Ensure SSH access is fully configured and tested before disabling Telnet to prevent being locked out."
        ),
        "juniper": ExactRemediation(
            problem_description="Telnet is an unencrypted protocol. Credentials and data are transmitted in plaintext.",
            remediation_explanation="Remove the telnet service from system services.",
            vendor="juniper",
            vendor_cli="delete system services telnet\ncommit",
            human_approval_required=True,
            safe_guidance="Ensure SSH access is fully configured and tested before disabling Telnet to prevent being locked out."
        )
    },
    "NET-SSH-002": {
        "cisco": ExactRemediation(
            problem_description="Legacy SSH versions (e.g., v1 or v1.99) are vulnerable to downgrade attacks and cryptographic flaws.",
            remediation_explanation="Enforce SSH version 2 globally.",
            vendor="cisco",
            vendor_cli="ip ssh version 2",
            human_approval_required=True,
            safe_guidance="Verify that all management clients support SSHv2 before enforcing."
        )
    },
    "NET-AUTH-001": {
        "cisco": ExactRemediation(
            problem_description="Local fallback authentication without a centralized AAA server reduces visibility and centralized control.",
            remediation_explanation="Configure AAA to use RADIUS/TACACS+ for authentication.",
            vendor="cisco",
            vendor_cli="aaa new-model\naaa authentication login default group radius local",
            human_approval_required=True,
            safe_guidance="Ensure the AAA server is reachable before committing this change."
        )
    }
}

def get_exact_remediation(control_id: str, vendor: str) -> Optional[ExactRemediation]:
    """Retrieve exact remediation intelligence for a specific control and vendor."""
    vendor = vendor.lower()
    if control_id in _REMEDIATION_DB and vendor in _REMEDIATION_DB[control_id]:
        return _REMEDIATION_DB[control_id][vendor]
    return None
