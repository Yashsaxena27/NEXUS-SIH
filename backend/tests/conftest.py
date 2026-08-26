import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.app.schemas.security_ir import (
    NormalizedConfig, DeviceInfo, ManagementConfig, TelnetConfig, SSHConfig, 
    AuthenticationConfig, PasswordPolicy
)
from backend.app.compliance.models import ComplianceControl, ControlRequirement, ControlOperator, ControlSeverity
from httpx import ASGITransport, AsyncClient
from backend.app.main import app
from backend.app.core.config import settings
from backend.app.security.auth import get_current_user

app.dependency_overrides[get_current_user] = lambda: "test_user"

import pytest_asyncio

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def compliant_config():
    return NormalizedConfig(
        device=DeviceInfo(vendor="cisco", platform="IOS-XE", device_type="router"),
        management=ManagementConfig(
            telnet=TelnetConfig(enabled=False),
            ssh=SSHConfig(enabled=True, version=2),
            session_timeout=300
        ),
        authentication=AuthenticationConfig(
            aaa_enabled=True,
            password_policy=PasswordPolicy(min_length=10)
        )
    )

@pytest.fixture
def non_compliant_config():
    return NormalizedConfig(
        device=DeviceInfo(vendor="cisco", platform="IOS-XE", device_type="router"),
        management=ManagementConfig(
            telnet=TelnetConfig(enabled=True),
            ssh=SSHConfig(enabled=False),
            session_timeout=3600
        ),
        authentication=AuthenticationConfig(
            aaa_enabled=False,
            password_policy=PasswordPolicy(min_length=4)
        )
    )

@pytest.fixture
def sample_controls():
    return [
        ComplianceControl(
            id="NET-SSH-001",
            title="Disable Insecure Telnet",
            severity=ControlSeverity.CRITICAL,
            requirement=ControlRequirement(
                field="management.telnet.enabled",
                operator=ControlOperator.EQUALS,
                value=False
            )
        )
    ]
