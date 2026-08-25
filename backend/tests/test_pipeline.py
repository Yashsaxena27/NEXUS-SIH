"""
End-to-end integration tests for the full pipeline:
    Raw Config → Vendor Detection → Normalization → Compliance Engine → PASS/FAIL/UNKNOWN

Tests each vendor against sample configs and verifies:
    1. Vendor detection works
    2. Normalization produces correct schema
    3. Compliance engine produces correct PASS/FAIL/UNKNOWN
    4. Evidence is generated
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from backend.app.vendors.detector import VendorDetector
from backend.app.normalization import normalize_config
from backend.app.compliance.engine import ComplianceEngine
from backend.app.compliance.loader import load_all_controls
from backend.app.schemas.security_ir import NormalizationResult


# ─── Sample configs (inline, focused) ───────────────────────────────

CISCO_COMPLIANT = """
version 17.3
service timestamps debug datetime msec
service timestamps log datetime msec
hostname CISCO-RTR-01
!
aaa new-model
aaa authentication login default group tacacs+ local
!
ip ssh version 2
ip domain-name corp.example.com
!
no ip http server
no ip http secure-server
!
logging host 10.1.1.100
logging buffered 65536
!
snmp-server community S3cr3tStr1ng RO
!
ntp server 10.1.1.50
!
banner login ^C
*** WARNING: Authorized Access Only ***
^C
!
security passwords min-length 12
!
line con 0
 exec-timeout 5 0
line vty 0 4
 exec-timeout 5 0
 transport input ssh
 login authentication default
!
interface GigabitEthernet0/0
 ip address 10.0.0.1 255.255.255.0
 no shutdown
!
end
"""

CISCO_VIOLATIONS = """
version 15.1
hostname CISCO-BAD-01
!
ip ssh version 1
!
ip http server
!
snmp-server community public RO
!
line vty 0 4
 transport input telnet ssh
 exec-timeout 30 0
!
end
"""

JUNIPER_COMPLIANT = """
system {
    host-name JUNIPER-FW-01;
    services {
        ssh {
            protocol-version v2;
        }
    }
    login {
        class admin-class {
            idle-timeout 10;
        }
        message "Authorized Access Only";
    }
    syslog {
        host 10.1.1.100 {
            any informational;
        }
    }
    ntp {
        server 10.1.1.50;
    }
}
snmp {
    community MyS3cr3t {
        authorization read-only;
    }
}
"""

JUNIPER_VIOLATIONS = """
system {
    host-name JUNIPER-BAD-01;
    services {
        ssh;
        telnet;
    }
}
snmp {
    community public {
        authorization read-only;
    }
}
"""

FORTINET_COMPLIANT = """
config system global
    set hostname "FORTI-FW-01"
    set admintimeout 10
    set admin-sport 443
end
config log syslogd setting
    set status enable
    set server "10.1.1.100"
    set port 514
end
config system ntp
    set ntpsync enable
    set type custom
    config ntpserver
        edit 1
            set server "10.1.1.50"
        next
    end
end
config system snmp community
    edit 1
        set name "MyS3cr3t"
    next
end
"""

FORTINET_VIOLATIONS = """
config system global
    set hostname "FORTI-BAD-01"
    set admin-telnet enable
    set admintimeout 120
end
config system snmp community
    edit 1
        set name "public"
    next
end
"""

PALOALTO_COMPLIANT = """
set deviceconfig system hostname PA-FW-01
set deviceconfig system login-banner "Authorized Access Only"
set deviceconfig system service disable-telnet yes
set deviceconfig system service disable-http yes
set deviceconfig system idle-timeout 10
set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50
set shared log-settings syslog Syslog-Server server Syslog-Host server 10.1.1.100
set network interface ethernet ethernet1/1 layer3 ip 172.16.1.1/24
set rulebase security rules DEFAULT-DENY from any to any source any destination any action deny
"""

PALOALTO_VIOLATIONS = """
set deviceconfig system hostname PA-FW-BAD
set deviceconfig system idle-timeout 120
set network interface ethernet ethernet1/1 layer3 ip 172.16.1.1/24
set rulebase security rules ALLOW-ALL from any to any source any destination any action allow
"""


# ─── Fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def compliance_engine():
    controls_dir = Path(__file__).parent.parent.parent / "compliance" / "controls"
    controls = load_all_controls(controls_dir)
    return ComplianceEngine(controls)


# ─── Vendor Detection Tests ──────────────────────────────────────────

class TestVendorDetection:
    def test_detect_cisco(self):
        result = VendorDetector.detect_vendor(CISCO_COMPLIANT)
        assert result.vendor == "cisco"
        assert result.confidence > 0.5

    def test_detect_juniper(self):
        result = VendorDetector.detect_vendor(JUNIPER_COMPLIANT)
        assert result.vendor == "juniper"
        assert result.confidence > 0.5

    def test_detect_fortinet(self):
        result = VendorDetector.detect_vendor(FORTINET_COMPLIANT)
        assert result.vendor == "fortinet"
        assert result.confidence > 0.5

    def test_detect_paloalto(self):
        result = VendorDetector.detect_vendor(PALOALTO_COMPLIANT)
        assert result.vendor == "paloalto"
        assert result.confidence > 0.5

    def test_detect_unknown(self):
        result = VendorDetector.detect_vendor("this is not a network config")
        assert result.vendor == "unknown"


# ─── Normalization Tests ─────────────────────────────────────────────

class TestNormalization:
    def test_cisco_compliant_normalization(self):
        result = normalize_config(CISCO_COMPLIANT, vendor_hint="cisco")
        c = result.config
        assert c.device.vendor == "cisco"
        assert c.device.hostname == "CISCO-RTR-01"
        assert c.management.ssh.enabled is True
        assert c.management.ssh.version == 2
        assert c.management.telnet.enabled is False
        assert c.management.session_timeout == 300  # 5 min * 60
        assert c.authentication.aaa_enabled is True
        assert c.logging.syslog.enabled is True
        assert c.snmp.default_community is False
        assert c.time.ntp.enabled is True
        assert len(result.evidence) > 0

    def test_cisco_violations_normalization(self):
        result = normalize_config(CISCO_VIOLATIONS, vendor_hint="cisco")
        c = result.config
        assert c.management.telnet.enabled is True
        assert c.management.ssh.version == 1
        assert c.snmp.default_community is True

    def test_juniper_compliant_normalization(self):
        result = normalize_config(JUNIPER_COMPLIANT, vendor_hint="juniper")
        c = result.config
        assert c.device.vendor == "juniper"
        assert c.device.hostname == "JUNIPER-FW-01"
        assert c.management.ssh.enabled is True
        assert c.management.telnet.enabled is False
        assert c.logging.syslog.enabled is True
        assert c.time.ntp.enabled is True
        assert c.snmp.default_community is False

    def test_juniper_violations_normalization(self):
        result = normalize_config(JUNIPER_VIOLATIONS, vendor_hint="juniper")
        c = result.config
        assert c.management.telnet.enabled is True
        assert c.snmp.default_community is True

    def test_fortinet_compliant_normalization(self):
        result = normalize_config(FORTINET_COMPLIANT, vendor_hint="fortinet")
        c = result.config
        assert c.device.vendor == "fortinet"
        assert c.device.hostname is not None
        assert c.management.ssh.enabled is True  # Default for FortiOS
        assert c.management.telnet.enabled is False
        assert c.logging.syslog.enabled is True
        assert c.time.ntp.enabled is True
        assert c.snmp.default_community is False

    def test_fortinet_violations_normalization(self):
        result = normalize_config(FORTINET_VIOLATIONS, vendor_hint="fortinet")
        c = result.config
        assert c.management.telnet.enabled is True
        assert c.snmp.default_community is True

    def test_paloalto_compliant_normalization(self):
        result = normalize_config(PALOALTO_COMPLIANT, vendor_hint="paloalto")
        c = result.config
        assert c.device.vendor == "paloalto"
        assert c.device.hostname == "PA-FW-01"
        assert c.management.telnet.enabled is False
        assert c.management.session_timeout == 600  # 10 min * 60
        assert c.management.login_banner is not None
        assert c.logging.syslog.enabled is True
        assert c.time.ntp.enabled is True
        assert c.services.http_server_enabled is False

    def test_paloalto_violations_normalization(self):
        result = normalize_config(PALOALTO_VIOLATIONS, vendor_hint="paloalto")
        c = result.config
        assert c.management.telnet.enabled is True  # disable-telnet not set
        assert c.management.login_banner is None
        assert c.logging.syslog.enabled is False
        assert c.time.ntp.enabled is False

    def test_unknown_vendor_fallback(self):
        result = normalize_config("random text here", vendor_hint="unknown_vendor")
        assert result.config.device.vendor == "unknown"
        assert len(result.parse_errors) > 0


# ─── Full Pipeline Tests (Normalization + Compliance) ─────────────────

class TestFullPipeline:
    """
    Tests the complete pipeline:
        Config → Normalize → Compliance Engine → PASS/FAIL/UNKNOWN
    """

    def _find_finding(self, report, control_id):
        return next((f for f in report.findings if f.control_id == control_id), None)

    def test_cisco_compliant_pipeline(self, compliance_engine):
        result = normalize_config(CISCO_COMPLIANT, vendor_hint="cisco")
        report = compliance_engine.evaluate(result.config, result.evidence)

        assert report.device_vendor == "cisco"
        assert report.compliance_score > 50  # Should be high

        # Key controls should PASS
        telnet = self._find_finding(report, "NET-SSH-001")
        assert telnet.status.value == "PASS", f"Expected PASS for NET-SSH-001, got {telnet.status}"

        ssh_ver = self._find_finding(report, "NET-SSH-002")
        assert ssh_ver.status.value == "PASS"

        aaa = self._find_finding(report, "NET-AAA-001")
        assert aaa.status.value == "PASS"

        syslog = self._find_finding(report, "NET-LOG-001")
        assert syslog.status.value == "PASS"

        snmp = self._find_finding(report, "NET-SNMP-001")
        assert snmp.status.value == "PASS"

        ntp = self._find_finding(report, "NET-NTP-001")
        assert ntp.status.value == "PASS"

    def test_cisco_violations_pipeline(self, compliance_engine):
        result = normalize_config(CISCO_VIOLATIONS, vendor_hint="cisco")
        report = compliance_engine.evaluate(result.config, result.evidence)

        telnet = self._find_finding(report, "NET-SSH-001")
        assert telnet.status.value == "FAIL"

        ssh_ver = self._find_finding(report, "NET-SSH-002")
        assert ssh_ver.status.value == "FAIL"

        snmp = self._find_finding(report, "NET-SNMP-001")
        assert snmp.status.value == "FAIL"

    def test_juniper_compliant_pipeline(self, compliance_engine):
        result = normalize_config(JUNIPER_COMPLIANT, vendor_hint="juniper")
        report = compliance_engine.evaluate(result.config, result.evidence)

        telnet = self._find_finding(report, "NET-SSH-001")
        assert telnet.status.value == "PASS"

        syslog = self._find_finding(report, "NET-LOG-001")
        assert syslog.status.value == "PASS"

        ntp = self._find_finding(report, "NET-NTP-001")
        assert ntp.status.value == "PASS"

        snmp = self._find_finding(report, "NET-SNMP-001")
        assert snmp.status.value == "PASS"

    def test_fortinet_compliant_pipeline(self, compliance_engine):
        result = normalize_config(FORTINET_COMPLIANT, vendor_hint="fortinet")
        report = compliance_engine.evaluate(result.config, result.evidence)

        telnet = self._find_finding(report, "NET-SSH-001")
        assert telnet.status.value == "PASS"

        syslog = self._find_finding(report, "NET-LOG-001")
        assert syslog.status.value == "PASS"

        ntp = self._find_finding(report, "NET-NTP-001")
        assert ntp.status.value == "PASS"

    def test_paloalto_compliant_pipeline(self, compliance_engine):
        result = normalize_config(PALOALTO_COMPLIANT, vendor_hint="paloalto")
        report = compliance_engine.evaluate(result.config, result.evidence)

        telnet = self._find_finding(report, "NET-SSH-001")
        assert telnet.status.value == "PASS"

        syslog = self._find_finding(report, "NET-LOG-001")
        assert syslog.status.value == "PASS"

        ntp = self._find_finding(report, "NET-NTP-001")
        assert ntp.status.value == "PASS"

        http = self._find_finding(report, "NET-HTTP-001")
        assert http.status.value == "PASS"

        banner = self._find_finding(report, "NET-BAN-001")
        assert banner.status.value == "PASS"

    def test_paloalto_violations_pipeline(self, compliance_engine):
        result = normalize_config(PALOALTO_VIOLATIONS, vendor_hint="paloalto")
        report = compliance_engine.evaluate(result.config, result.evidence)

        telnet = self._find_finding(report, "NET-SSH-001")
        assert telnet.status.value == "FAIL"

        banner = self._find_finding(report, "NET-BAN-001")
        assert banner.status.value in ("FAIL", "UNKNOWN", "UNKNOWN_ABSENT")

        syslog = self._find_finding(report, "NET-LOG-001")
        assert syslog.status.value == "FAIL"

        ntp = self._find_finding(report, "NET-NTP-001")
        assert ntp.status.value == "FAIL"

    def test_findings_have_evidence(self, compliance_engine):
        result = normalize_config(CISCO_COMPLIANT, vendor_hint="cisco")
        report = compliance_engine.evaluate(result.config, result.evidence)

        for finding in report.findings:
            assert finding.control_id is not None
            assert finding.status is not None
            assert finding.severity is not None
            # Explanation context should be populated
            assert finding.explanation_context is not None

    def test_compliance_score_calculation(self, compliance_engine):
        # Compliant config should score higher
        compliant_result = normalize_config(CISCO_COMPLIANT, vendor_hint="cisco")
        compliant_report = compliance_engine.evaluate(compliant_result.config, compliant_result.evidence)

        violations_result = normalize_config(CISCO_VIOLATIONS, vendor_hint="cisco")
        violations_report = compliance_engine.evaluate(violations_result.config, violations_result.evidence)

        assert compliant_report.compliance_score > violations_report.compliance_score
