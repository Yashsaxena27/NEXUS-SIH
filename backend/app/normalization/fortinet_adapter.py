from typing import Optional
from backend.app.normalization.base_adapter import BaseVendorAdapter
from backend.app.schemas.security_ir import (
    NormalizationResult,
    NormalizedConfig,
    InterpretationMethod,
    ManagementConfig,
    SSHConfig,
    TelnetConfig,
    HttpAdminConfig,
    LoggingConfig,
    SyslogConfig,
    SNMPConfig,
    TimeConfig,
    NTPConfig,
    AuthenticationConfig,
    ServicesConfig,
)

class FortinetAdapter(BaseVendorAdapter):
    VENDOR_NAME = "fortinet"
    PLATFORM = "FortiOS"
    DEVICE_TYPE = "firewall"
    
    def detect(self, raw_config: str) -> Optional[float]:
        return 1.0 if "config system global" in raw_config or "config firewall policy" in raw_config else 0.0

    def normalize(self, raw_config: str, adaptive_rules: Optional[list] = None) -> NormalizationResult:
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

        hostname_val, _ = add_evidence("device.hostname", None, r"set hostname\s+\"?(.+?)\"?$")
        device = self._make_device_info(hostname=hostname_val)
        
        timeout_val, _ = add_evidence("management.session_timeout", None, r"set admintimeout\s+(\d+)")
        if not timeout_val:
            timeout_val, _ = add_evidence("management.session_timeout", None, r"set idle-timeout\s+(\d+)")
            
        timeout_sec = int(timeout_val) * 60 if timeout_val else None
        if timeout_val:
            evidence[-1].value = timeout_sec
            
        https_port, _ = add_evidence("management.http_admin.port", None, r"set admin-sport\s+(\d+)")
        
        snmp_comm, _ = add_evidence("snmp.community_string", None, r"set name\s+\"?([^\"\s]+)\"?")
        if snmp_comm:
            snmp_comm = snmp_comm.strip('"')
        snmp_default = snmp_comm in ['public', 'private'] if snmp_comm else False
        if snmp_comm:
            evidence.append(self._make_evidence("snmp.default_community", snmp_default, evidence[-1].source, evidence[-1].raw_evidence))
            
        snmp = SNMPConfig(community_string=snmp_comm, default_community=snmp_default)
        
        from backend.app.normalization.parsers.block_parser import KeywordBlockParser
        parser = KeywordBlockParser(raw_config)
        
        syslog_block = parser.get_block("log syslogd setting")
        syslog_enabled = False
        syslog_server = None
        
        if syslog_block:
            enable_line = syslog_block.get_command("set status enable")
            if enable_line:
                syslog_enabled = True
                evidence.append(self._make_evidence("logging.syslog.enabled", True, f"block {syslog_block.parent_line}", enable_line))
            
            server_line = syslog_block.get_command("set server")
            if server_line:
                syslog_server = self._extract_value(server_line, r"set server\s+\"?([^\s\"]+)\"?")
                evidence.append(self._make_evidence("logging.syslog.server", syslog_server, f"block {syslog_block.parent_line}", server_line))
                
        logging = LoggingConfig(syslog=SyslogConfig(enabled=syslog_enabled, server=syslog_server))
        
        ntp_enabled = bool(self._find_first_line(raw_config, r"set ntpsync enable"))
        if ntp_enabled:
            ntp_line = self._find_first_line(raw_config, r"set ntpsync enable")
            evidence.append(self._make_evidence("time.ntp.enabled", True, f"line {ntp_line[0]}", ntp_line[1]))
            
        time_cfg = TimeConfig(ntp=NTPConfig(enabled=ntp_enabled))
        
        # FortiOS defaults to SSH enabled on mgmt
        ssh_enabled = True
        ssh_version = 2
        evidence.append(self._make_evidence("management.ssh.enabled", True, None, None, method=InterpretationMethod.DEFAULT_ASSUMED))
        evidence.append(self._make_evidence("management.ssh.version", 2, None, None, method=InterpretationMethod.DEFAULT_ASSUMED))
        
        telnet_line = self._find_first_line(raw_config, r"set admin-telnet enable")
        telnet_enabled = bool(telnet_line)
        if telnet_line:
            evidence.append(self._make_evidence("management.telnet.enabled", True, f"line {telnet_line[0]}", telnet_line[1]))
            
        http_admin = bool(self._find_first_line(raw_config, r"set admin-server-cert") or self._find_first_line(raw_config, r"set admin-https-redirect"))
        if http_admin:
            http_line = self._find_first_line(raw_config, r"set admin-server-cert") or self._find_first_line(raw_config, r"set admin-https-redirect")
            evidence.append(self._make_evidence("management.http_admin.enabled", True, f"line {http_line[0]}", http_line[1]))
            
        # Authentication (FortiOS implicitly uses AAA for local/remote admin)
        aaa_enabled = True
        evidence.append(self._make_evidence("authentication.aaa_enabled", True, None, None, method=InterpretationMethod.DEFAULT_ASSUMED))
        authentication = AuthenticationConfig(aaa_enabled=aaa_enabled)

        # HTTP Server (Services)
        http_service = bool(self._find_first_line(raw_config, r"set admin-http enable") or self._find_first_line(raw_config, r"set admin-port 80") or self._find_first_line(raw_config, r"set admin-sport 80"))
        if http_service:
            http_svc_line = self._find_first_line(raw_config, r"set admin-http enable") or self._find_first_line(raw_config, r"set admin-port 80") or self._find_first_line(raw_config, r"set admin-sport 80")
            evidence.append(self._make_evidence("services.http_server_enabled", True, f"line {http_svc_line[0]}", http_svc_line[1]))
        services = ServicesConfig(http_server_enabled=http_service)

        management = ManagementConfig(
            ssh=SSHConfig(enabled=ssh_enabled, version=ssh_version),
            telnet=TelnetConfig(enabled=telnet_enabled),
            http_admin=HttpAdminConfig(enabled=http_admin),
            session_timeout=timeout_sec
        )
        
        normalized = NormalizedConfig(
            device=device,
            management=management,
            authentication=authentication,
            logging=logging,
            snmp=snmp,
            time=time_cfg,
            services=services
        )
        
        self._apply_adaptive_rules(raw_config, normalized, evidence, adaptive_rules)
        return NormalizationResult(config=normalized, evidence=evidence, raw_config=raw_config)
