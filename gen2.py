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

# --- Cisco ---
cisco_template = """!
version 17.3
service timestamps debug datetime msec
service timestamps log datetime msec
service password-encryption
!
hostname {hostname}
!
{aaa}
!
{banner}
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
{http}
!
{ssh}
!
{logging}
!
{snmp}
!
{ntp}
!
line vty 0 4
 {timeout}
 {transport}
!
end
"""
cisco_samples = [
    {"name": "cisco_compliant_01.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-01"},
    {"name": "cisco_compliant_02.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community diffComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-02"},
    {"name": "cisco_telnet_violation.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input all", "hostname": "RTR-03"},
    {"name": "cisco_sshv1_violation.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 1", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-04"},
    {"name": "cisco_snmp_default.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community public RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-05"},
    {"name": "cisco_no_aaa.cfg", "aaa": "! no aaa config", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-06"},
    {"name": "cisco_no_syslog.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "! no syslog", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-07"},
    {"name": "cisco_multi_violation_01.cfg", "aaa": "! no aaa", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "! no syslog", "snmp": "snmp-server community public RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-08"},
    {"name": "cisco_multi_violation_02.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "! no banner", "http": "ip http server", "ssh": "ip ssh version 1", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 0 0", "transport": "transport input ssh", "hostname": "RTR-09"},
    {"name": "cisco_noisy_01.cfg", "aaa": "aaa new-model\naaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-10\n!\ninterface Loopback0\n ip address 1.1.1.1 255.255.255.255\n!\n! random noisy block\n"},
    {"name": "cisco_format_variant.cfg", "aaa": "aaa new-model\n aaa authentication login default local", "banner": "banner login ^C Authorized Access Only ^C", "http": "no ip http server", "ssh": "ip ssh version 2", "logging": "logging host 10.1.1.100", "snmp": "snmp-server community secureComm RO", "ntp": "ntp server 10.1.1.50", "timeout": "exec-timeout 10 0", "transport": "transport input ssh", "hostname": "RTR-11"},
    {"name": "cisco_many_violations.cfg", "aaa": "! no aaa", "banner": "! no banner", "http": "ip http server", "ssh": "ip ssh version 1", "logging": "! no syslog", "snmp": "snmp-server community public RW", "ntp": "! no ntp", "timeout": "exec-timeout 0 0", "transport": "transport input telnet", "hostname": "RTR-12"}
]
for s in cisco_samples:
    with open(os.path.join(base_dir, "dataset/samples/cisco", s["name"]), "w") as f:
        f.write(cisco_template.format(**s))

# --- Juniper ---
juniper_template = """system {{
    host-name {hostname};
    services {{
        {ssh}
        {telnet}
    }}
    {aaa}
    {syslog}
    {ntp}
}}
{snmp}
"""
juniper_samples = [
    {"name": "juniper_compliant_01.conf", "hostname": "JUNIPER-FW-01", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_compliant_02.conf", "hostname": "JUNIPER-FW-02", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community DiffComm {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_telnet_enabled.conf", "hostname": "JUNIPER-FW-03", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "telnet {\n            connection-limit 5;\n        }", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_no_ssh.conf", "hostname": "JUNIPER-FW-04", "ssh": "", "telnet": "telnet {\n        }", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_snmp_public.conf", "hostname": "JUNIPER-FW-05", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community public {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_no_aaa.conf", "hostname": "JUNIPER-FW-06", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "", "aaa": "", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_no_syslog.conf", "hostname": "JUNIPER-FW-07", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_multi_violation.conf", "hostname": "JUNIPER-FW-08", "ssh": "ssh {\n            protocol-version v1;\n        }", "telnet": "", "aaa": "login {\n        class admin-class {\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "", "snmp": "snmp {\n    community public {\n        authorization read-only;\n    }\n}"},
    {"name": "juniper_many_violations.conf", "hostname": "JUNIPER-FW-09", "ssh": "ssh {\n            protocol-version v1;\n        }", "telnet": "telnet {\n        }", "aaa": "", "syslog": "", "ntp": "", "snmp": "snmp {\n    community public {\n        authorization read-write;\n    }\n}"},
    {"name": "juniper_noisy.conf", "hostname": "JUNIPER-FW-10", "ssh": "ssh {\n            protocol-version v2;\n        }", "telnet": "", "aaa": "login {\n        class admin-class {\n            idle-timeout 10;\n        }\n    }", "syslog": "syslog {\n        host 10.1.1.100 {\n            any informational;\n        }\n    }", "ntp": "ntp {\n        server 10.1.1.50;\n    }", "snmp": "snmp {\n    community MyC0mmun1ty {\n        authorization read-only;\n    }\n}\nrouting-options {\n    static {\n        route 0.0.0.0/0 next-hop 192.168.1.1;\n    }\n}\n"},
    {"name": "juniper_format_variant.conf", "hostname": "JUNIPER-FW-11", "ssh": "ssh { protocol-version v2; }", "telnet": "", "aaa": "login { class admin-class { idle-timeout 10; } }", "syslog": "syslog { host 10.1.1.100 { any informational; } }", "ntp": "ntp { server 10.1.1.50; }", "snmp": "snmp { community MyC0mmun1ty { authorization read-only; } }"}
]
for s in juniper_samples:
    with open(os.path.join(base_dir, "dataset/samples/juniper", s["name"]), "w") as f:
        f.write(juniper_template.format(**s))

# --- Fortinet ---
fortinet_template = """config system global
    set hostname "{hostname}"
    {admin}
end
{aaa}
{syslog}
{ntp}
{snmp}
"""
fortinet_samples = [
    {"name": "fortinet_compliant_01.conf", "hostname": "FORTI-FW-01", "admin": "set admin-sport 443\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_compliant_02.conf", "hostname": "FORTI-FW-02", "admin": "set admin-sport 443\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"DiffComm\"\n    next\nend"},
    {"name": "fortinet_telnet_enabled.conf", "hostname": "FORTI-FW-03", "admin": "set admin-sport 443\n    set admin-telnet enable\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_weak_admin.conf", "hostname": "FORTI-FW-04", "admin": "set admin-sport 80\n    set admintimeout 0", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_snmp_public.conf", "hostname": "FORTI-FW-05", "admin": "set admin-sport 443\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"public\"\n    next\nend"},
    {"name": "fortinet_no_syslog.conf", "hostname": "FORTI-FW-06", "admin": "set admin-sport 443\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status disable\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_no_ntp.conf", "hostname": "FORTI-FW-07", "admin": "set admin-sport 443\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync disable\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend"},
    {"name": "fortinet_multi_violation.conf", "hostname": "FORTI-FW-08", "admin": "set admin-sport 80\n    set admintimeout 0\n    set admin-telnet enable", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status disable\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"public\"\n    next\nend"},
    {"name": "fortinet_many_violations.conf", "hostname": "FORTI-FW-09", "admin": "set admin-sport 80\n    set admintimeout 0\n    set admin-telnet enable", "aaa": "", "syslog": "config log syslogd setting\n    set status disable\nend", "ntp": "config system ntp\n    set ntpsync disable\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"public\"\n    next\nend"},
    {"name": "fortinet_noisy.conf", "hostname": "FORTI-FW-10", "admin": "set admin-sport 443\n    set admintimeout 10", "aaa": "config system admin\n    edit \"admin\"\n        set accprofile \"prof_admin\"\n        set password ENC hash\n    next\nend", "syslog": "config log syslogd setting\n    set status enable\n    set server \"10.1.1.100\"\n    set port 514\nend", "ntp": "config system ntp\n    set ntpsync enable\n    set type custom\n    config ntpserver\n        edit 1\n            set server \"10.1.1.50\"\n        next\n    end\nend", "snmp": "config system snmp community\n    edit 1\n        set name \"MyC0mmun1ty\"\n    next\nend\nconfig firewall policy\n    edit 1\n        set srcintf \"any\"\n        set dstintf \"any\"\n        set srcaddr \"all\"\n        set dstaddr \"all\"\n        set action accept\n        set schedule \"always\"\n        set service \"ALL\"\n    next\nend"},
    {"name": "fortinet_format_variant.conf", "hostname": "FORTI-FW-11", "admin": "set admin-sport 443\nset admintimeout 10", "aaa": "config system admin\nedit \"admin\"\nset accprofile \"prof_admin\"\nset password ENC hash\nnext\nend", "syslog": "config log syslogd setting\nset status enable\nset server \"10.1.1.100\"\nset port 514\nend", "ntp": "config system ntp\nset ntpsync enable\nset type custom\nconfig ntpserver\nedit 1\nset server \"10.1.1.50\"\nnext\nend\nend", "snmp": "config system snmp community\nedit 1\nset name \"MyC0mmun1ty\"\nnext\nend"}
]
for s in fortinet_samples:
    with open(os.path.join(base_dir, "dataset/samples/fortinet", s["name"]), "w") as f:
        f.write(fortinet_template.format(**s))

# --- PaloAlto ---
paloalto_template = """{hostname}
{banner}
{telnet}
{http}
{timeout}
{syslog}
{ntp}
{snmp}
"""
paloalto_samples = [
    {"name": "paloalto_compliant_01.conf", "hostname": "set deviceconfig system hostname PA-FW-01", "banner": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system service disable-telnet yes", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_compliant_02.conf", "hostname": "set deviceconfig system hostname PA-FW-02", "banner": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system service disable-telnet yes", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_telnet_enabled.conf", "hostname": "set deviceconfig system hostname PA-FW-03", "banner": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system service disable-telnet no", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_no_banner.conf", "hostname": "set deviceconfig system hostname PA-FW-04", "banner": "", "telnet": "set deviceconfig system service disable-telnet yes", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_no_syslog.conf", "hostname": "set deviceconfig system hostname PA-FW-05", "banner": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system service disable-telnet yes", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_no_ntp.conf", "hostname": "set deviceconfig system hostname PA-FW-06", "banner": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system service disable-telnet yes", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_multi_violation.conf", "hostname": "set deviceconfig system hostname PA-FW-07", "banner": "", "telnet": "set deviceconfig system service disable-telnet no", "http": "set deviceconfig system service disable-http no", "timeout": "set deviceconfig system idle-timeout 0", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"},
    {"name": "paloalto_many_violations.conf", "hostname": "set deviceconfig system hostname PA-FW-08", "banner": "", "telnet": "set deviceconfig system service disable-telnet no", "http": "set deviceconfig system service disable-http no", "timeout": "set deviceconfig system idle-timeout 0", "syslog": "", "ntp": "", "snmp": ""},
    {"name": "paloalto_noisy.conf", "hostname": "set deviceconfig system hostname PA-FW-09", "banner": "set deviceconfig system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system service disable-telnet yes", "http": "set deviceconfig system service disable-http yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3\nset network interface ethernet ethernet1/1 link-state auto\nset network interface ethernet ethernet1/2 link-state auto"},
    {"name": "paloalto_format_variant.conf", "hostname": "set  deviceconfig system hostname PA-FW-10", "banner": "set deviceconfig  system login-banner \"Authorized Access Only\"", "telnet": "set deviceconfig system  service disable-telnet yes", "http": "set deviceconfig system service disable-http  yes", "timeout": "set deviceconfig system idle-timeout 10", "syslog": "set shared log-settings syslog Syslog-Server server addr 10.1.1.100", "ntp": "set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 10.1.1.50", "snmp": "set deviceconfig system snmp-setting snmp-v3"}
]
for s in paloalto_samples:
    with open(os.path.join(base_dir, "dataset/samples/paloalto", s["name"]), "w") as f:
        f.write(paloalto_template.format(**s))

# --- Unknown ---
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
    with open(os.path.join(base_dir, f"dataset/samples/unknown/unknown_vendor_0{i}.conf"), "w") as f:
        f.write(unknown_template.format(ip=100+i))

# --- Ground Truth Builders ---
def build_compliance(overrides):
    base = {
        "NET-SSH-001": "PASS", "NET-SSH-002": "PASS", "NET-SSH-003": "PASS",
        "NET-AAA-001": "PASS", "NET-LOG-001": "PASS", "NET-NTP-001": "PASS",
        "NET-SNMP-001": "PASS", "NET-HTTP-001": "PASS", "NET-BAN-001": "PASS"
    }
    base.update(overrides)
    return base

def build_normalized(overrides):
    base = {
        "management.ssh.enabled": True, "management.ssh.version": 2, "management.telnet.enabled": False,
        "management.session_timeout": 600, "authentication.aaa_enabled": True, "logging.syslog.enabled": True,
        "logging.syslog.server": "10.1.1.100", "snmp.default_community": False, "time.ntp.enabled": True,
        "services.http_server_enabled": False, "management.login_banner": "Authorized Access Only"
    }
    base.update(overrides)
    return base

def generate_gt(samples, vendor, platform):
    gt = {"vendor": vendor, "samples": []}
    for s in samples:
        norm = {}
        comp = {}
        name = s["name"]
        
        if "telnet_enabled" in name or "telnet_violation" in name:
            norm["management.telnet.enabled"] = True
            comp["NET-SSH-001"] = "FAIL"
        if "sshv1_violation" in name:
            norm["management.ssh.version"] = 1
            comp["NET-SSH-002"] = "FAIL"
        if "snmp_default" in name or "snmp_public" in name:
            norm["snmp.default_community"] = True
            comp["NET-SNMP-001"] = "FAIL"
        if "no_aaa" in name:
            norm["authentication.aaa_enabled"] = False
            comp["NET-AAA-001"] = "FAIL"
        if "no_syslog" in name:
            norm["logging.syslog.enabled"] = False
            comp["NET-LOG-001"] = "FAIL"
        if "no_ssh" in name:
            norm["management.ssh.enabled"] = False
            norm["management.telnet.enabled"] = True
            comp["NET-SSH-001"] = "FAIL"
            comp["NET-SSH-002"] = "FAIL"
        if "weak_admin" in name:
            norm["services.http_server_enabled"] = True
            norm["management.session_timeout"] = 0
            comp["NET-HTTP-001"] = "FAIL"
            comp["NET-SSH-003"] = "FAIL"
        if "no_ntp" in name:
            norm["time.ntp.enabled"] = False
            comp["NET-NTP-001"] = "FAIL"
        if "no_banner" in name:
            norm["management.login_banner"] = ""
            comp["NET-BAN-001"] = "FAIL"
        
        if "multi_violation" in name and "many" not in name:
            if vendor == "cisco":
                norm["authentication.aaa_enabled"] = False
                norm["logging.syslog.enabled"] = False
                norm["snmp.default_community"] = True
                comp["NET-AAA-001"] = "FAIL"
                comp["NET-LOG-001"] = "FAIL"
                comp["NET-SNMP-001"] = "FAIL"
                if "02" in name:
                    norm = {"services.http_server_enabled": True, "management.ssh.version": 1, "management.login_banner": "", "management.session_timeout": 0}
                    comp = {"NET-HTTP-001": "FAIL", "NET-SSH-002": "FAIL", "NET-BAN-001": "FAIL", "NET-SSH-003": "FAIL"}
            elif vendor == "juniper":
                norm = {"management.ssh.version": 1, "time.ntp.enabled": False, "snmp.default_community": True, "management.session_timeout": 0}
                comp = {"NET-SSH-002": "FAIL", "NET-NTP-001": "FAIL", "NET-SNMP-001": "FAIL", "NET-SSH-003": "FAIL"}
            elif vendor == "fortinet":
                norm = {"services.http_server_enabled": True, "management.session_timeout": 0, "management.telnet.enabled": True, "logging.syslog.enabled": False, "snmp.default_community": True}
                comp = {"NET-HTTP-001": "FAIL", "NET-SSH-003": "FAIL", "NET-SSH-001": "FAIL", "NET-LOG-001": "FAIL", "NET-SNMP-001": "FAIL"}
            elif vendor == "paloalto":
                norm = {"management.telnet.enabled": True, "services.http_server_enabled": True, "management.session_timeout": 0, "management.login_banner": ""}
                comp = {"NET-SSH-001": "FAIL", "NET-HTTP-001": "FAIL", "NET-SSH-003": "FAIL", "NET-BAN-001": "FAIL"}

        if "many_violations" in name:
            norm = {
                "management.telnet.enabled": True, "management.ssh.version": 1, "management.session_timeout": 0,
                "authentication.aaa_enabled": False, "logging.syslog.enabled": False, "time.ntp.enabled": False,
                "snmp.default_community": True, "services.http_server_enabled": True, "management.login_banner": ""
            }
            comp = {k: "FAIL" for k in build_compliance({})}
            if vendor == "fortinet":
                comp["NET-BAN-001"] = "PASS"
                comp["NET-SSH-002"] = "PASS"
            if vendor == "paloalto":
                comp["NET-SSH-002"] = "PASS"
            if vendor == "juniper":
                comp["NET-HTTP-001"] = "PASS"
                comp["NET-BAN-001"] = "PASS"

        gt["samples"].append({
            "filename": name,
            "expected_vendor_detection": vendor,
            "expected_platform": platform,
            "expected_normalized": build_normalized(norm),
            "expected_compliance": build_compliance(comp)
        })
    return gt

with open(os.path.join(base_dir, "dataset/ground_truth/cisco_ground_truth.json"), "w") as f:
    json.dump(generate_gt(cisco_samples, "cisco", "IOS-XE"), f, indent=2)
with open(os.path.join(base_dir, "dataset/ground_truth/juniper_ground_truth.json"), "w") as f:
    json.dump(generate_gt(juniper_samples, "juniper", "JUNOS"), f, indent=2)
with open(os.path.join(base_dir, "dataset/ground_truth/fortinet_ground_truth.json"), "w") as f:
    json.dump(generate_gt(fortinet_samples, "fortinet", "FortiOS"), f, indent=2)
with open(os.path.join(base_dir, "dataset/ground_truth/paloalto_ground_truth.json"), "w") as f:
    json.dump(generate_gt(paloalto_samples, "paloalto", "PAN-OS"), f, indent=2)
