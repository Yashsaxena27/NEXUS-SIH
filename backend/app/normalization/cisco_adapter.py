from typing import Optional
from backend.app.normalization.base_adapter import BaseVendorAdapter
from backend.app.schemas.security_ir import (
    NormalizationResult,
    NormalizedConfig,
    ManagementConfig,
    SSHConfig,
    TelnetConfig,
    HttpAdminConfig,
    AuthenticationConfig,
    PasswordPolicy,
    LoggingConfig,
    SyslogConfig,
    SNMPConfig,
    TimeConfig,
    NTPConfig,
    ServicesConfig,
    AccessControlConfig
)

class CiscoAdapter(BaseVendorAdapter):
    VENDOR_NAME = "cisco"
    PLATFORM = "IOS-XE"
    DEVICE_TYPE = "router"
    
    def detect(self, raw_config: str) -> Optional[float]:
        # Delegate to the standalone detector logic via vendor hints typically.
        # This is a fallback implementation.
        return 1.0 if "version " in raw_config or "hostname " in raw_config else 0.0

    def normalize(self, raw_config: str, adaptive_rules: Optional[list] = None) -> NormalizationResult:
        evidence = []
        
        # Helper to extract and create evidence
        def add_evidence(field, value, pattern, group=1):
            match = self._find_first_line(raw_config, pattern)
            if match:
                line_no, line_text = match
                val = self._extract_value(line_text, pattern, group)
                if val is not None:
                    # Convert to required type later
                    evidence.append(self._make_evidence(field, val, source=f"line {line_no}", raw_evidence=line_text))
                    return val, line_text
            return None, None

        # Device info
        hostname_val, _ = add_evidence("device.hostname", None, r"^hostname\s+(\S+)")
        version_val, _ = add_evidence("device.version", None, r"^version\s+(\S+)")
        device = self._make_device_info(hostname=hostname_val, version=version_val)
        
        # Management (VTY Block)
        ssh_enabled = False
        ssh_version = None
        telnet_enabled = False
        
        from backend.app.normalization.parsers.block_parser import IndentBlockParser
        parser = IndentBlockParser(raw_config)
        vty_block = parser.get_block("line vty")
        
        if vty_block:
            # Check transport input inside VTY block
            ssh_line = vty_block.get_command("transport input")
            if ssh_line:
                if "ssh" in ssh_line or "all" in ssh_line:
                    ssh_enabled = True
                    evidence.append(self._make_evidence("management.ssh.enabled", True, f"line {vty_block.parent_line}", ssh_line))
                if "telnet" in ssh_line or "all" in ssh_line:
                    telnet_enabled = True
                    evidence.append(self._make_evidence("management.telnet.enabled", True, f"line {vty_block.parent_line}", ssh_line))
            
        ssh_ver_val, _ = add_evidence("management.ssh.version", None, r"^\s*ip\s+ssh\s+version\s+(\d+)")
        if ssh_ver_val:
            ssh_version = int(ssh_ver_val)
            # Update evidence to reflect int
            evidence[-1].value = ssh_version
            
        session_timeout = None
        timeout_match = self._find_first_line(raw_config, r"exec-timeout\s+(\d+)\s+(\d+)")
        if timeout_match:
            mins, secs = self._extract_value(timeout_match[1], r"exec-timeout\s+(\d+)\s+(\d+)", 1), self._extract_value(timeout_match[1], r"exec-timeout\s+(\d+)\s+(\d+)", 2)
            session_timeout = int(mins) * 60 + int(secs)
            evidence.append(self._make_evidence("management.session_timeout", session_timeout, f"line {timeout_match[0]}", timeout_match[1]))
            
        banner_val = None
        banner_match = self._find_first_line(raw_config, r"^banner login")
        if banner_match:
            line_no, line_text = banner_match
            import re
            m = re.search(r"^banner login\s+(\S+)\s+(.+?)\s+\1$", line_text)
            if m:
                banner_val = m.group(2)
            else:
                banner_val = line_text.replace("banner login", "").strip()
            evidence.append(self._make_evidence("management.login_banner", banner_val, f"line {line_no}", line_text))
        http_en_line = self._find_first_line(raw_config, r"^ip http server")
        http_dis_line = self._find_first_line(raw_config, r"^no ip http server")
        http_enabled = bool(http_en_line) and not bool(http_dis_line)
        if http_en_line:
            evidence.append(self._make_evidence("services.http_server_enabled", http_enabled, f"line {http_en_line[0]}", http_en_line[1]))
        elif http_dis_line:
            evidence.append(self._make_evidence("services.http_server_enabled", http_enabled, f"line {http_dis_line[0]}", http_dis_line[1]))

        management = ManagementConfig(
            ssh=SSHConfig(enabled=ssh_enabled, version=ssh_version),
            telnet=TelnetConfig(enabled=telnet_enabled),
            session_timeout=session_timeout,
            login_banner=banner_val
        )
        
        services = ServicesConfig(
            http_server_enabled=http_enabled
        )
        
        # Authentication
        aaa_enabled = bool(self._find_first_line(raw_config, r"^aaa new-model"))
        if aaa_enabled:
            aaa_line = self._find_first_line(raw_config, r"^aaa new-model")
            evidence.append(self._make_evidence("authentication.aaa_enabled", True, f"line {aaa_line[0]}", aaa_line[1]))
            
        auth_method, _ = add_evidence("authentication.method", None, r"^aaa authentication login \S+ group (\S+)")
        pass_len_val, _ = add_evidence("authentication.password_policy.min_length", None, r"^security passwords min-length (\d+)")
        
        authentication = AuthenticationConfig(
            aaa_enabled=aaa_enabled,
            method=auth_method,
            password_policy=PasswordPolicy(min_length=int(pass_len_val) if pass_len_val else None)
        )
        
        # Logging
        syslog_enabled = False
        syslog_server = None
        syslog_line = self._find_first_line(raw_config, r"^logging host (\S+)") or self._find_first_line(raw_config, r"^logging (\d+\.\d+\.\d+\.\d+)")
        if syslog_line:
            syslog_enabled = True
            syslog_server = self._extract_value(syslog_line[1], r"^logging host (\S+)") or self._extract_value(syslog_line[1], r"^logging (\d+\.\d+\.\d+\.\d+)")
            evidence.append(self._make_evidence("logging.syslog.enabled", True, f"line {syslog_line[0]}", syslog_line[1]))
            evidence.append(self._make_evidence("logging.syslog.server", syslog_server, f"line {syslog_line[0]}", syslog_line[1]))
            
        local_log_line = self._find_first_line(raw_config, r"^logging buffered")
        local_logging = bool(local_log_line)
        if local_log_line:
            evidence.append(self._make_evidence("logging.local_logging_enabled", True, f"line {local_log_line[0]}", local_log_line[1]))
            
        logging = LoggingConfig(
            syslog=SyslogConfig(enabled=syslog_enabled, server=syslog_server),
            local_logging_enabled=local_logging
        )
        
        # SNMP
        snmp_comm, _ = add_evidence("snmp.community_string", None, r"^snmp-server community (\S+)")
        snmp_default = snmp_comm in ['public', 'private']
        if snmp_comm:
            evidence[-1].value = snmp_comm
            evidence.append(self._make_evidence("snmp.default_community", snmp_default, evidence[-1].source, evidence[-1].raw_evidence))
            
        snmp = SNMPConfig(community_string=snmp_comm, default_community=snmp_default)
        
        # Time
        ntp_server, _ = add_evidence("time.ntp.servers", None, r"^ntp server (\S+)")
        ntp_enabled = bool(ntp_server)
        if ntp_server:
            # Fix evidence field for servers array
            evidence[-1].value = [ntp_server]
            evidence.append(self._make_evidence("time.ntp.enabled", True, evidence[-1].source, evidence[-1].raw_evidence))
            
        time_cfg = TimeConfig(ntp=NTPConfig(enabled=ntp_enabled, servers=[ntp_server] if ntp_server else []))
        
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
        
        return NormalizationResult(
            config=normalized,
            evidence=evidence,
            raw_config=raw_config
        )
