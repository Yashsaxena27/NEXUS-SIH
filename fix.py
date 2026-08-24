import re

with open('gen.py', 'r') as f:
    text = f.read()

replacements = {
    '"aaa":': '"aaa_config":',
    '"banner":': '"banner_config":',
    '"http":': '"http_config":',
    '"ssh":': '"ssh_config":',
    '"logging":': '"logging_config":',
    '"snmp":': '"snmp_config":',
    '"ntp":': '"ntp_config":',
    '"timeout":': '"timeout_config":',
    '"transport":': '"transport_config":',
    '"telnet":': '"telnet_config":',
    '"syslog":': '"syslog_config":'
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open('gen.py', 'w') as f:
    f.write(text)
