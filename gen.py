import os
import json

base_dir = r"c:\Users\saxen\Documents\antigravity\beautiful-mendel"

directories = [
    "dataset/samples/cisco",
    "dataset/samples/juniper",
    "dataset/samples/fortinet",
    "dataset/samples/paloalto",
    "dataset/samples/unknown",
    "dataset/ground_truth"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# Cisco Generator
cisco_template = """!
version 17.3
service timestamps debug datetime msec
service timestamps log datetime msec
service password-encryption
!
hostname {hostname}
!
{aaa_config}
!
{banner_config}
!
interface GigabitEthernet0/0
 description Management Interface
 ip address 10.1.1.10 255.255.255.0
!
interface GigabitEthernet0/1
 description WAN
 ip address 203.0.113.2 255.255.255.252
!
router bgp 65000
 network 192.168.1.0
!
{http_config}
!
{ssh_config}
!
{logging_config}
!
{snmp_config}
!
{ntp_config}
!
line vty 0 4
 {timeout_config}
 {transport_config}
!
end
"""

cisco_samples = [
    {"name": "cisco_compliant_01.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-01"},
    {"name": "cisco_compliant_02.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community diffComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-02"},
    {"name": "cisco_telnet_violation.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input all", "hostname": "RTR-03"},
    {"name": "cisco_sshv1_violation.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 1", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-04"},
    {"name": "cisco_snmp_default.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community public RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-05"},
    {"name": "cisco_no_aaa.cfg", "aaa_config": "! no aaa config", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-06"},
    {"name": "cisco_no_syslog.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "! no syslog", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-07"},
    {"name": "cisco_multi_violation_01.cfg", "aaa_config": "! no aaa", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "! no syslog", "snmp_config": "snmp-server community public RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-08"},
    {"name": "cisco_multi_violation_02.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "! no banner", "http_config": "ip http server", "ssh_config": "ip ssh version 1", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 0 0", "transport_config": "transport input ssh", "hostname": "RTR-09"},
    {"name": "cisco_noisy_01.cfg", "aaa_config": "aaa new-model\naaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-10\n!\ninterface Loopback0\n ip address 1.1.1.1 255.255.255.255\n!\n! random noisy block\n"},
    {"name": "cisco_format_variant.cfg", "aaa_config": "aaa new-model\n aaa authentication login default local", "banner_config": "banner login ^C Authorized Access Only ^C", "http_config": "no ip http server", "ssh_config": "ip ssh version 2", "logging_config": "logging host 10.1.1.100", "snmp_config": "snmp-server community secureComm RO", "ntp_config": "ntp server 10.1.1.50", "timeout_config": "exec-timeout 10 0", "transport_config": "transport input ssh", "hostname": "RTR-11"},
    {"name": "cisco_many_violations.cfg", "aaa_config": "! no aaa", "banner_config": "! no banner", "http_config": "ip http server", "ssh_config": "ip ssh version 1", "logging_config": "! no syslog", "snmp_config": "snmp-server community public RW", "ntp_config": "! no ntp", "timeout_config": "exec-timeout 0 0", "transport_config": "transport input telnet", "hostname": "RTR-12"}
]

for sample in cisco_samples:
    content = cisco_template.format(**sample)
    with open(os.path.join(base_dir, "dataset/samples/cisco", sample["name"]), "w") as f:
        f.write(content)

cisco_gt = {
    "vendor": "cisco",
    "samples": []
}

def build_compliance(sample_name, overrides=None):
    if overrides is None: overrides = {}
    base = {
        "NET-SSH-001": "PASS",
        "NET-SSH-002": "PASS",
        "NET-SSH-003": "PASS",
        "NET-AAA-001": "PASS",
        "NET-LOG-001": "PASS",
        "NET-NTP-001": "PASS",
        "NET-SNMP-001": "PASS",
        "NET-HTTP-001": "PASS",
        "NET-BAN-001": "PASS"
    }
    base.update(overrides)
    return base

def build_normalized(sample_name, overrides=None):
    if overrides is None: overrides = {}
    base = {
        "management.ssh.enabled": True,
        "management.ssh.version": 2,
        "management.telnet.enabled": False,
        "management.session_timeout": 600,
        "authentication.aaa_enabled": True,
        "logging.syslog.enabled": True,
        "logging.syslog.server": "10.1.1.100",
        "snmp.default_community": False,
        "time.ntp.enabled": True,
        "services.http_server_enabled": False,
        "management.login_banner": "Authorized Access Only"
    }
    base.update(overrides)
    return base

for s in cisco_samples:
    norm_overrides = {}
    comp_overrides = {}
    
    if "telnet_violation" in s["name"]:
        norm_overrides["management.telnet.enabled"] = True
        comp_overrides["NET-SSH-001"] = "FAIL"
    elif "sshv1_violation" in s["name"]:
        norm_overrides["management.ssh.version"] = 1
        comp_overrides["NET-SSH-002"] = "FAIL"
    elif "snmp_default" in s["name"]:
        norm_overrides["snmp.default_community"] = True
        comp_overrides["NET-SNMP-001"] = "FAIL"
    elif "no_aaa" in s["name"]:
        norm_overrides["authentication.aaa_enabled"] = False
        comp_overrides["NET-AAA-001"] = "FAIL"
    elif "no_syslog" in s["name"]:
        norm_overrides["logging.syslog.enabled"] = False
        comp_overrides["NET-LOG-001"] = "FAIL"
    elif "multi_violation_01" in s["name"]:
        norm_overrides["authentication.aaa_enabled"] = False
        norm_overrides["logging.syslog.enabled"] = False
        norm_overrides["snmp.default_community"] = True
        comp_overrides["NET-AAA-001"] = "FAIL"
        comp_overrides["NET-LOG-001"] = "FAIL"
        comp_overrides["NET-SNMP-001"] = "FAIL"
    elif "multi_violation_02" in s["name"]:
        norm_overrides["services.http_server_enabled"] = True
        norm_overrides["management.ssh.version"] = 1
        norm_overrides["management.login_banner"] = ""
        norm_overrides["management.session_timeout"] = 0
        comp_overrides["NET-HTTP-001"] = "FAIL"
        comp_overrides["NET-SSH-002"] = "FAIL"
        comp_overrides["NET-BAN-001"] = "FAIL"
        comp_overrides["NET-SSH-003"] = "FAIL"
    elif "many_violations" in s["name"]:
        norm_overrides = {
            "management.telnet.enabled": True,
            "management.ssh.version": 1,
            "management.session_timeout": 0,
            "authentication.aaa_enabled": False,
            "logging.syslog.enabled": False,
            "time.ntp.enabled": False,
            "snmp.default_community": True,
            "services.http_server_enabled": True,
            "management.login_banner": ""
        }
        comp_overrides = {k: "FAIL" for k in build_compliance("")}
        
    cisco_gt["samples"].append({
        "filename": s["name"],
        "expected_vendor_detection": "cisco",
        "expected_platform": "IOS-XE",
        "expected_normalized": build_normalized(s["name"], norm_overrides),
        "expected_compliance": build_compliance(s["name"], comp_overrides)
    })

with open(os.path.join(base_dir, "dataset/ground_truth/cisco_ground_truth.json"), "w") as f:
    json.dump(cisco_gt, f, indent=2)


juniper_template = """system {{
    host-name {hostname};
    services {{
        {ssh_config}
        {telnet_config}
    }}
    {aaa_config}
    {syslog_config}
    {ntp_config}
}}
{snmp_config}
"""

juniper_samples = [
    {"name": "juniper_compliant_01.conf", "hostname": "JUNIPER-FW-01", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_compliant_02.conf", "hostname": "JUNIPER-FW-02", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community DiffComm {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_telnet_enabled.conf", "hostname": "JUNIPER-FW-03", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "telnet {\n            connection-limit 5;\n        }", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_no_ssh.conf", "hostname": "JUNIPER-FW-04", "ssh_config": "", "telnet_config": "telnet {\n        }", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_snmp_public.conf", "hostname": "JUNIPER-FW-05", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community public {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_no_aaa.conf", "hostname": "JUNIPER-FW-06", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "", "aaa_config": "", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_no_syslog.conf", "hostname": "JUNIPER-FW-07", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_multi_violation.conf", "hostname": "JUNIPER-FW-08", "ssh_config": "ssh {\n            protocol-version v1;\n        }", "telnet_config": "", "aaa_config": "login {\n        class admin-class {\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "", "snmp_config": "snmp {\n    community public {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_many_violations.conf", "hostname": "JUNIPER-FW-09", "ssh_config": "ssh {\n            protocol-version v1;\n        }", "telnet_config": "telnet {\n        }", "aaa_config": "", "syslog_config": "", "ntp_config": "", "snmp_config": "snmp {\n    community public {\n        authorization read-write;\n    }\n}"},
    {"name": "juniper_noisy.conf", "hostname": "JUNIPER-FW-10", "ssh_config": "ssh {\n            protocol-version v2;\n        }", "telnet_config": "", "aaa_config": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog_config": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp_config": "ntp {\n        server 10.1.1.50;\n    }", "snmp_config": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}\nrouting-options {\n    static {\n        route 0.0.0.0/0 next-hop 192.168.1.1;\n    }\n}\n"},
    {"name": "juniper_format_variant.conf", "hostname": "JUNIPER-FW-11", "ssh_config": "ssh { protocol-version v2; }", "telnet_config": "", "aaa_config": "login { class admin-class { idle-timeout 10; } }", "syslog_config": "syslog { host 10.1.1.100 { any informational; } }", "ntp_config": "ntp { server 10.1.1.50; }", "snmp_config": "snmp { community MyC0mmun1ty { authorization read-only; } }"}
]

for sample in juniper_samples:
    content = juniper_template.format(**sample)
    with open(os.path.join(base_dir, "dataset/samples/juniper", sample["name"]), "w") as f:
        f.write(content)

juniper_gt = {
    "vendor": "juniper",
    "samples": []
}

for s in juniper_samples:
    norm_overrides = {}
    comp_overrides = {}
    if "telnet_enabled" in s["name"]:
        norm_overrides["management.telnet.enabled"] = True
        comp_overrides["NET-SSH-001"] = "FAIL"
    elif "no_ssh" in s["name"]:
        norm_overrides["management.ssh.enabled"] = False
        norm_overrides["management.telnet.enabled"] = True
        comp_overrides["NET-SSH-001"] = "FAIL"
        comp_overrides["NET-SSH-002"] = "FAIL"
    elif "snmp_public" in s["name"]:
        norm_overrides["snmp.default_community"] = True
        comp_overrides["NET-SNMP-001"] = "FAIL"
    elif "no_aaa" in s["name"]:
        norm_overrides["authentication.aaa_enabled"] = False
        comp_overrides["NET-AAA-001"] = "FAIL"
    elif "no_syslog" in s["name"]:
        norm_overrides["logging.syslog.enabled"] = False
        comp_overrides["NET-LOG-001"] = "FAIL"
    elif "multi_violation" in s["name"] and "many" not in s["name"]:
        norm_overrides["management.ssh.version"] = 1
        norm_overrides["time.ntp.enabled"] = False
        norm_overrides["snmp.default_community"] = True
        norm_overrides["management.session_timeout"] = 0
        comp_overrides["NET-SSH-002"] = "FAIL"
        comp_overrides["NET-NTP-001"] = "FAIL"
        comp_overrides["NET-SNMP-001"] = "FAIL"
        comp_overrides["NET-SSH-003"] = "FAIL"
    elif "many_violations" in s["name"]:
        norm_overrides = {
            "management.telnet.enabled": True,
            "management.ssh.version": 1,
            "management.session_timeout": 0,
            "authentication.aaa_enabled": False,
            "logging.syslog.enabled": False,
            "time.ntp.enabled": False,
            "snmp.default_community": True,
            "services.http_server_enabled": False,
            "management.login_banner": "Authorized Access Only"
        }
        comp_overrides = {k: "FAIL" for k in build_compliance("")}
        comp_overrides["NET-HTTP-001"] = "PASS"
        comp_overrides["NET-BAN-001"] = "PASS"
        
    juniper_gt["samples"].append({
        "filename": s["name"],
        "expected_vendor_detection": "juniper",
        "expected_platform": "JUNOS",
        "expected_normalized": build_normalized(s["name"], norm_overrides),
        "expected_compliance": build_compliance(s["name"], comp_overrides)
    })

with open(os.path.join(base_dir, "dataset/ground_truth/juniper_ground_truth.json"), "w") as f:
    json.dump(juniper_gt, f, indent=2)

fortinet_template = """config system global
    set hostname "{hostname}"
    {admin_config}
end
{aaa_config}
{syslog_config}
{ntp_config}
{snmp_config}
"""

fortinet_samples = [
    {"name": "fortinet_compliant_01.conf", "hostname": "FORTI-FW-01", "admin_config": "set admin-sport 443\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_compliant_02.conf", "hostname": "FORTI-FW-02", "admin_config": "set admin-sport 443\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"DiffComm\"\n    next\nend"},
    {"name": "fortinet_telnet_enabled.conf", "hostname": "FORTI-FW-03", "admin_config": "set admin-sport 443\n    set admin-telnet enable\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_weak_admin.conf", "hostname": "FORTI-FW-04", "admin_config": "set admin-sport 80\n    set admintimeout 0", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_snmp_public.conf", "hostname": "FORTI-FW-05", "admin_config": "set admin-sport 443\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"public\"\n    next\nend"},
    {"name": "fortinet_no_syslog.conf", "hostname": "FORTI-FW-06", "admin_config": "set admin-sport 443\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status disable\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_no_ntp.conf", "hostname": "FORTI-FW-07", "admin_config": "set admin-sport 443\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync disable\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_multi_violation.conf", "hostname": "FORTI-FW-08", "admin_config": "set admin-sport 80\n    set admintimeout 0\n    set admin-telnet enable", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status disable\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"public\"\n    next\nend"},
    {"name": "fortinet_many_violations.conf", "hostname": "FORTI-FW-09", "admin_config": "set admin-sport 80\n    set admintimeout 0\n    set admin-telnet enable", "aaa_config": "", "syslog_config": "config log syslogd setting\n    set status disable\nend", "ntp_config": "config system ntp\n    set ntpsync disable\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"public\"\n    next\nend"},
    {"name": "fortinet_noisy.conf", "hostname": "FORTI-FW-10", "admin_config": "set admin-sport 443\n    set admintimeout 10", "aaa_config": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog_config": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp_config": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp_config": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend\nconfig firewall policy\n    edit 1\n        set srcintf \"any\"\n        set dstintf \"any\"\n        set srcaddr \"all\"\n        set dstaddr \"all\"\n        set action accept\n        set schedule \"always\"\n        set service \"ALL\"\n    next\nend"},
    {"name": "fortinet_format_variant.conf", "hostname": "FORTI-FW-11", "admin_config": "set admin-sport 443\nset admintimeout 10", "aaa_config": "config system admin\nedit \"admin\"\nset accprofile \"prof_admin\"\nset password ENC hash\nnext\nend", "syslog_config": "config log syslogd setting\nset status enable\nset server \"10.1.1.100\"\nset port 514\nend", "ntp_config": "config system ntp\nset ntpsync enable\nset type custom\nconfig ntpserver\nedit 1\nset server \"10.1.1.50\"\nnext\nend\nend", "snmp_config": "config system snmp community\nedit 1\nset name \"MyC0mmun1ty\"\nnext\nend"}
]

for sample in fortinet_samples:
    content = fortinet_template.format(**sample)
    with open(os.path.join(base_dir, "dataset/samples/fortinet", sample["name"]), "w") as f:
        f.write(content)
        
fortinet_gt = {
    "vendor": "fortinet",
    "samples": []
}

for s in fortinet_samples:
    norm_overrides = {}
    comp_overrides = {}
    if "telnet_enabled" in s["name"]:
        norm_overrides["management.telnet.enabled"] = True
        comp_overrides["NET-SSH-001"] = "FAIL"
    elif "weak_admin" in s["name"]:
        norm_overrides["services.http_server_enabled"] = True
        norm_overrides["management.session_timeout"] = 0
        comp_overrides["NET-HTTP-001"] = "FAIL"
        comp_overrides["NET-SSH-003"] = "FAIL"
    elif "snmp_public" in s["name"]:
        norm_overrides["snmp.default_community"] = True
        comp_overrides["NET-SNMP-001"] = "FAIL"
    elif "no_syslog" in s["name"]:
        norm_overrides["logging.syslog.enabled"] = False
        comp_overrides["NET-LOG-001"] = "FAIL"
    elif "no_ntp" in s["name"]:
        norm_overrides["time.ntp.enabled"] = False
        comp_overrides["NET-NTP-001"] = "FAIL"
    elif "multi_violation" in s["name"] and "many" not in s["name"]:
        norm_overrides["services.http_server_enabled"] = True
        norm_overrides["management.session_timeout"] = 0
        norm_overrides["management.telnet.enabled"] = True
        norm_overrides["logging.syslog.enabled"] = False
        norm_overrides["snmp.default_community"] = True
        comp_overrides["NET-HTTP-001"] = "FAIL"
        comp_overrides["NET-SSH-003"] = "FAIL"
        comp_overrides["NET-SSH-001"] = "FAIL"
        comp_overrides["NET-LOG-001"] = "FAIL"
        comp_overrides["NET-SNMP-001"] = "FAIL"
    elif "many_violations" in s["name"]:
        norm_overrides = {
            "management.telnet.enabled": True,
            "management.ssh.version": 1,
            "management.session_timeout": 0,
            "authentication.aaa_enabled": False,
            "logging.syslog.enabled": False,
            "time.ntp.enabled": False,
            "snmp.default_community": True,
            "services.http_server_enabled": True,
            "management.login_banner": "Authorized Access Only"
        }
        comp_overrides = {k: "FAIL" for k in build_compliance("")}
        comp_overrides["NET-BAN-001"] = "PASS"
        comp_overrides["NET-SSH-002"] = "PASS"
        
    fortinet_gt["samples"].append({
        "filename": s["name"],
        "expected_vendor_detection": "fortinet",
        "expected_platform": "FortiOS",
        "expected_normalized": build_normalized(s["name"], norm_overrides),
        "expected_compliance": build_compliance(s["name"], comp_overrides)
    })

with open(os.path.join(base_dir, "dataset/ground_truth/fortinet_ground_truth.json"), "w") as f:
    json.dump(fortinet_gt, f, indent=2)

paloalto_template = """{hostname}
{banner_config}
{telnet}
{http_config}
{timeout_config}
{syslog}
{ntp_config}
{snmp_config}
"""

paloalto_samples = [
    {"name": "paloalto_compliant_01.conf", "hostname": "set deviceconfig system hostname PA-FW-01", "banner_config": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system service disable-telnet yes", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_compliant_02.conf", "hostname": "set deviceconfig system hostname PA-FW-02", "banner_config": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system service disable-telnet yes", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_telnet_enabled.conf", "hostname": "set deviceconfig system hostname PA-FW-03", "banner_config": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system service disable-telnet no", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_no_banner.conf", "hostname": "set deviceconfig system hostname PA-FW-04", "banner_config": "", "telnet_config": "set deviceconfig system service disable-telnet yes", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_no_syslog.conf", "hostname": "set deviceconfig system hostname PA-FW-05", "banner_config": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system service disable-telnet yes", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_no_ntp.conf", "hostname": "set deviceconfig system hostname PA-FW-06", "banner_config": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system service disable-telnet yes", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_multi_violation.conf", "hostname": "set deviceconfig system hostname PA-FW-07", "banner_config": "", "telnet_config": "set deviceconfig system service disable-telnet no", "http_config": "set deviceconfig system service disable-http no", "timeout_config": "set deviceconfig system idle-timeout 0", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_many_violations.conf", "hostname": "set deviceconfig system hostname PA-FW-08", "banner_config": "", "telnet_config": "set deviceconfig system service disable-telnet no", "http_config": "set deviceconfig system service disable-http no", "timeout_config": "set deviceconfig system idle-timeout 0", "syslog_config": "", "ntp_config": "", "snmp_config": ""},
    {"name": "paloalto_noisy.conf", "hostname": "set deviceconfig system hostname PA-FW-09", "banner_config": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system service disable-telnet yes", "http_config": "set deviceconfig system service disable-http yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3\nset network interface ethernet ethernet1/1 link-state auto\nset network interface ethernet ethernet1/2 link-state auto"},
    {"name": "paloalto_format_variant.conf", "hostname": "set  deviceconfig system hostname PA-FW-10", "banner_config": "set deviceconfig  system login-banner \"Authorized Access Only\"", "telnet_config": "set deviceconfig system  service disable-telnet yes", "http_config": "set deviceconfig system service disable-http  yes", "timeout_config": "set deviceconfig system idle-timeout 10", "syslog_config": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp_config": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp_config": "set deviceconfig system snmp-setting snmp-v3"}
]

for sample in paloalto_samples:
    content = paloalto_template.format(**sample)
    with open(os.path.join(base_dir, "dataset/samples/paloalto", sample["name"]), "w") as f:
        f.write(content)
        
paloalto_gt = {
    "vendor": "paloalto",
    "samples": []
}

for s in paloalto_samples:
    norm_overrides = {}
    comp_overrides = {}
    if "telnet_enabled" in s["name"]:
        norm_overrides["management.telnet.enabled"] = True
        comp_overrides["NET-SSH-001"] = "FAIL"
    elif "no_banner" in s["name"]:
        norm_overrides["management.login_banner"] = ""
        comp_overrides["NET-BAN-001"] = "FAIL"
    elif "no_syslog" in s["name"]:
        norm_overrides["logging.syslog.enabled"] = False
        comp_overrides["NET-LOG-001"] = "FAIL"
    elif "no_ntp" in s["name"]:
        norm_overrides["time.ntp.enabled"] = False
        comp_overrides["NET-NTP-001"] = "FAIL"
    elif "multi_violation" in s["name"] and "many" not in s["name"]:
        norm_overrides["management.telnet.enabled"] = True
        norm_overrides["services.http_server_enabled"] = True
        norm_overrides["management.session_timeout"] = 0
        norm_overrides["management.login_banner"] = ""
        comp_overrides["NET-SSH-001"] = "FAIL"
        comp_overrides["NET-HTTP-001"] = "FAIL"
        comp_overrides["NET-SSH-003"] = "FAIL"
        comp_overrides["NET-BAN-001"] = "FAIL"
    elif "many_violations" in s["name"]:
        norm_overrides = {
            "management.telnet.enabled": True,
            "management.ssh.version": 1,
            "management.session_timeout": 0,
            "authentication.aaa_enabled": False,
            "logging.syslog.enabled": False,
            "time.ntp.enabled": False,
            "snmp.default_community": True,
            "services.http_server_enabled": True,
            "management.login_banner": ""
        }
        comp_overrides = {k: "FAIL" for k in build_compliance("")}
        comp_overrides["NET-SSH-002"] = "PASS"
        
    paloalto_gt["samples"].append({
        "filename": s["name"],
        "expected_vendor_detection": "paloalto",
        "expected_platform": "PAN-OS",
        "expected_normalized": build_normalized(s["name"], norm_overrides),
        "expected_compliance": build_compliance(s["name"], comp_overrides)
    })

with open(os.path.join(base_dir, "dataset/ground_truth/paloalto_ground_truth.json"), "w") as f:
    json.dump(paloalto_gt, f, indent=2)

unknown_template = """secure-admin {{
    protocol ssh-v2;
    timeout 300;
}}
network-logging {{
    remote-server 10.1.1.{ip};
    level info;
}}
"""

for i in range(1, 4):
    content = unknown_template.format(ip=100+i)
    with open(os.path.join(base_dir, f"dataset/samples/unknown/unknown_vendor_0{i}.conf"), "w") as f:
        f.write(content)

print("Done")
