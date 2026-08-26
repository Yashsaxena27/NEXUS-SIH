from typing import Optional
from backend.app.normalization.base_adapter import BaseVendorAdapter
from backend.app.schemas.security_ir import (
    NormalizationResult,
    NormalizedConfig,
    ManagementConfig,
    SSHConfig,
    TelnetConfig,
    AuthenticationConfig,
    LoggingConfig,
    SyslogConfig,
    SNMPConfig,
    TimeConfig,
    NTPConfig
)

class JuniperAdapter(BaseVendorAdapter):
    VENDOR_NAME = "juniper"
    PLATFORM = "Junos"
    DEVICE_TYPE = "router"
    
    def detect(self, raw_config: str) -> Optional[float]:
        return 1.0 if "system {" in raw_config or "interfaces {" in raw_config else 0.0

    def normalize(self, raw_config: str, adaptive_rules: Optional[list] = None) -> NormalizationResult:
        evidence = []
        
        # Simple extraction for Juniper based on patterns
        def add_evidence(field, value, pattern, group=1):
            match = self._find_first_line(raw_config, pattern)
            if match:
                line_no, line_text = match
                val = self._extract_value(line_text, pattern, group)
                if val is not None:
                    evidence.append(self._make_evidence(field, val, source=f"line {line_no}", raw_evidence=line_text))
                    return val, line_text
            return None, None

        # This relies on simplified regex since full tree parsing isn't strictly requested and regex is fine
        hostname_val, _ = add_evidence("device.hostname", None, r"host-name\s+(\S+);")
        device = self._make_device_info(hostname=hostname_val)
        
        ssh_line = self._find_first_line(raw_config, r"ssh \{")
        ssh_enabled = bool(ssh_line)
        if ssh_line:
            evidence.append(self._make_evidence("management.ssh.enabled", True, f"line {ssh_line[0]}", ssh_line[1]))
            
        ssh_version_val, _ = add_evidence("management.ssh.version", None, r"protocol-version\s+v(\d+);")
        
        telnet_line = self._find_first_line(raw_config, r"\btelnet\b")
        telnet_enabled = bool(telnet_line)
        if telnet_line:
            evidence.append(self._make_evidence("management.telnet.enabled", True, f"line {telnet_line[0]}", telnet_line[1]))
            
        timeout_val, _ = add_evidence("management.session_timeout", None, r"idle-timeout\s+(\d+);")
        timeout_int = int(timeout_val) * 60 if timeout_val else None
        if timeout_val:
            evidence[-1].value = timeout_int
            
        banner_val, _ = add_evidence("management.login_banner", None, r"message\s+\"([^\"]+)\"")
        if not banner_val:
            banner_val, _ = add_evidence("management.login_banner", None, r"announcement\s+\"([^\"]+)\"")
            
        management = ManagementConfig(
            ssh=SSHConfig(enabled=ssh_enabled, version=int(ssh_version_val) if ssh_version_val else None),
            telnet=TelnetConfig(enabled=telnet_enabled),
            session_timeout=timeout_int,
            login_banner=banner_val
        )
        
        aaa_enabled = bool(self._find_first_line(raw_config, r"authentication-order") or self._find_first_line(raw_config, r"tacplus-server") or self._find_first_line(raw_config, r"login\s*\{"))
        if aaa_enabled:
            aaa_line = self._find_first_line(raw_config, r"authentication-order") or self._find_first_line(raw_config, r"tacplus-server") or self._find_first_line(raw_config, r"login\s*\{")
            evidence.append(self._make_evidence("authentication.aaa_enabled", True, f"line {aaa_line[0]}", aaa_line[1]))
            
        authentication = AuthenticationConfig(aaa_enabled=aaa_enabled)
        
        snmp_comm, _ = add_evidence("snmp.community_string", None, r"community\s+(\S+)\s*\{")
        snmp_default = snmp_comm in ['public', 'private']
        if snmp_comm:
            evidence.append(self._make_evidence("snmp.default_community", snmp_default, evidence[-1].source, evidence[-1].raw_evidence))
            
        snmp = SNMPConfig(community_string=snmp_comm, default_community=snmp_default)
        
        syslog_server, _ = add_evidence("logging.syslog.server", None, r"host\s+(\S+)\s*\{")
        syslog_enabled = bool(syslog_server)
        if syslog_server:
            evidence.append(self._make_evidence("logging.syslog.enabled", True, evidence[-1].source, evidence[-1].raw_evidence))
            
        logging = LoggingConfig(syslog=SyslogConfig(enabled=syslog_enabled, server=syslog_server))
        
        ntp_server, _ = add_evidence("time.ntp.servers", None, r"server\s+(\S+)")
        ntp_enabled = bool(ntp_server)
        if ntp_server:
            evidence[-1].value = [ntp_server]
            evidence.append(self._make_evidence("time.ntp.enabled", True, evidence[-1].source, evidence[-1].raw_evidence))
            
        time_cfg = TimeConfig(ntp=NTPConfig(enabled=ntp_enabled, servers=[ntp_server] if ntp_server else []))
        
        normalized = NormalizedConfig(
            device=device,
            management=management,
            authentication=authentication,
            logging=logging,
            snmp=snmp,
            time=time_cfg
        )
        
        self._apply_adaptive_rules(raw_config, normalized, evidence, adaptive_rules)
        return NormalizationResult(config=normalized, evidence=evidence, raw_config=raw_config)
