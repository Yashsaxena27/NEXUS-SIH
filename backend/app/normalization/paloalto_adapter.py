from typing import Optional
from backend.app.normalization.base_adapter import BaseVendorAdapter
from backend.app.schemas.security_ir import (
    NormalizationResult,
    NormalizedConfig,
    ManagementConfig,
    SSHConfig,
    TelnetConfig,
    HttpAdminConfig,
    LoggingConfig,
    SyslogConfig,
    TimeConfig,
    NTPConfig,
    ServicesConfig,
)

class PaloAltoAdapter(BaseVendorAdapter):
    VENDOR_NAME = "paloalto"
    PLATFORM = "PAN-OS"
    DEVICE_TYPE = "firewall"
    
    def detect(self, raw_config: str) -> Optional[float]:
        return 1.0 if "set deviceconfig" in raw_config or "set rulebase" in raw_config else 0.0

    def normalize(self, raw_config: str) -> NormalizationResult:
        evidence = []
        
        def add_evidence(field, value, pattern, group=1):
            match = self._find_first_line(raw_config, pattern)
            if match:
                line_no, line_text = match
                val = self._extract_value(line_text, pattern, group)
                if val is not None:
                    evidence.append(self._make_evidence(field, val, source=f"line {line_no}", raw_evidence=line_text))
                    return val, line_text
            return None, None

        hostname_val, _ = add_evidence("device.hostname", None, r"set deviceconfig system hostname\s+(\S+)")
        device = self._make_device_info(hostname=hostname_val)
        
        banner_val, _ = add_evidence("management.login_banner", None, r"set deviceconfig system login-banner\s+\"(.+)\"")
        
        telnet_disabled = bool(self._find_first_line(raw_config, r"set deviceconfig system service disable-telnet yes"))
        if telnet_disabled:
            telnet_line = self._find_first_line(raw_config, r"set deviceconfig system service disable-telnet yes")
            evidence.append(self._make_evidence("management.telnet.enabled", False, f"line {telnet_line[0]}", telnet_line[1]))
            # Imply SSH is primary
            evidence.append(self._make_evidence("management.ssh.enabled", True, f"line {telnet_line[0]}", telnet_line[1]))
        ssh_enabled = telnet_disabled
            
        http_disabled = bool(self._find_first_line(raw_config, r"set deviceconfig system service disable-http yes"))
        if http_disabled:
            http_line = self._find_first_line(raw_config, r"set deviceconfig system service disable-http yes")
            evidence.append(self._make_evidence("management.http_admin.enabled", False, f"line {http_line[0]}", http_line[1]))
            
        timeout_val, _ = add_evidence("management.session_timeout", None, r"set deviceconfig system idle-timeout\s+(\d+)")
        timeout_sec = int(timeout_val) * 60 if timeout_val else None
        if timeout_val:
            evidence[-1].value = timeout_sec
            
        management = ManagementConfig(
            ssh=SSHConfig(enabled=ssh_enabled),
            telnet=TelnetConfig(enabled=not telnet_disabled),
            http_admin=HttpAdminConfig(enabled=not http_disabled),
            session_timeout=timeout_sec,
            login_banner=banner_val
        )
        
        syslog_line = self._find_first_line(raw_config, r"set shared log-settings syslog")
        syslog_enabled = bool(syslog_line)
        if syslog_line:
            evidence.append(self._make_evidence("logging.syslog.enabled", True, f"line {syslog_line[0]}", syslog_line[1]))
            
        logging = LoggingConfig(syslog=SyslogConfig(enabled=syslog_enabled))
        
        ntp_line = self._find_first_line(raw_config, r"set deviceconfig system ntp-servers")
        ntp_enabled = bool(ntp_line)
        if ntp_line:
            evidence.append(self._make_evidence("time.ntp.enabled", True, f"line {ntp_line[0]}", ntp_line[1]))
            
        time_cfg = TimeConfig(ntp=NTPConfig(enabled=ntp_enabled))

        services = ServicesConfig(http_server_enabled=not http_disabled)
        
        normalized = NormalizedConfig(
            device=device,
            management=management,
            logging=logging,
            time=time_cfg,
            services=services,
        )
        
        return NormalizationResult(config=normalized, evidence=evidence, raw_config=raw_config)
