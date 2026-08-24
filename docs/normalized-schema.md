# Vendor-Neutral Security IR Schema

## Overview

The Vendor-Neutral Security Intermediate Representation (IR) is the canonical
data model that ALL vendor configurations are normalized into. The compliance
engine evaluates ONLY this model — never raw vendor CLI syntax.

## Architecture Principle

```
Cisco    ─┐
Juniper  ─┤
Fortinet ─┼─► NormalizedConfig ──► Compliance Engine ──► PASS/FAIL/UNKNOWN
PaloAlto ─┤
Unknown  ─┘
```

## Schema Structure

```json
{
  "device": {
    "vendor": "cisco",
    "platform": "IOS-XE",
    "device_type": "router",
    "version": "17.3",
    "hostname": "ROUTER-01"
  },
  "management": {
    "ssh": { "enabled": true, "version": 2 },
    "telnet": { "enabled": false },
    "http_admin": { "enabled": false, "https_only": true },
    "session_timeout": 600,
    "login_banner": "Authorized Access Only"
  },
  "authentication": {
    "aaa_enabled": true,
    "method": "tacacs+",
    "local_fallback": true,
    "password_policy": { "min_length": 14, "complexity_enabled": true }
  },
  "logging": {
    "syslog": { "enabled": true, "server": "10.1.1.100", "level": "informational" },
    "local_logging_enabled": true,
    "buffer_size": 65536
  },
  "snmp": {
    "version": "3",
    "community_string": "MyS3cr3t",
    "default_community": false
  },
  "time": {
    "ntp": { "enabled": true, "servers": ["10.1.1.50"], "authentication_enabled": true }
  },
  "services": {
    "http_server_enabled": false,
    "cdp_enabled": false,
    "lldp_enabled": true
  },
  "access_control": {
    "acl_enabled": true,
    "rules_count": 15
  }
}
```

## Property Evidence

Each normalized property carries provenance metadata:

```json
{
  "field": "management.ssh.version",
  "value": 2,
  "confidence": 0.98,
  "source": "line 182",
  "method": "deterministic_parser",
  "raw_evidence": "ip ssh version 2"
}
```

### Interpretation Methods

| Method | Confidence | Description |
|--------|-----------|-------------|
| `deterministic_parser` | 1.0 | Exact regex/parser match |
| `regex_match` | 0.95-1.0 | Pattern match with high confidence |
| `llm_inference` | 0.5-0.9 | AI-assisted interpretation |
| `human_confirmed` | 1.0 | Administrator verified |
| `default_assumed` | 0.8 | Vendor default behavior |

## Adding a New Vendor

1. Create `backend/app/normalization/<vendor>_adapter.py`
2. Inherit from `BaseVendorAdapter`
3. Implement `detect()` and `normalize()`
4. Register in `backend/app/normalization/__init__.py`
5. Add sample configs to `dataset/samples/<vendor>/`
6. Add ground truth to `dataset/ground_truth/`
