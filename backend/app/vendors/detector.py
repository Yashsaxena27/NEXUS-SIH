import re
from typing import Optional
from pydantic import BaseModel

class VendorDetectionResult(BaseModel):
    vendor: str
    platform: str
    device_type: str
    confidence: float

class VendorDetector:
    @staticmethod
    def detect_vendor(raw_config: str) -> VendorDetectionResult:
        if not raw_config:
            return VendorDetectionResult(vendor='unknown', platform='unknown', device_type='unknown', confidence=0.0)

        cisco_score = 0
        juniper_score = 0
        fortinet_score = 0
        paloalto_score = 0
        
        lines = raw_config.splitlines()
        
        for line in lines:
            line_str = line.strip()
            # Cisco
            if re.match(r'^version \d+\.\d+', line_str):
                cisco_score += 3
            if line_str.startswith('hostname '):
                cisco_score += 1
            if line_str.startswith('interface GigabitEthernet') or line_str.startswith('interface FastEthernet'):
                cisco_score += 2
            if line_str.startswith('line vty') or line_str.startswith('line con'):
                cisco_score += 2
            if line_str.startswith('router ospf') or line_str.startswith('router bgp'):
                cisco_score += 2
            if line_str == '!':
                cisco_score += 1
            
            # Juniper
            if line_str.endswith('{') or line_str.endswith('}'):
                juniper_score += 1
            if line_str.startswith('system {') or line_str.startswith('interfaces {') or line_str.startswith('protocols {'):
                juniper_score += 3
            if line_str.endswith(';'):
                juniper_score += 1
            if line_str.startswith('set system '):
                juniper_score += 2
                
            # Fortinet
            if line_str.startswith('config system global') or line_str.startswith('config firewall policy'):
                fortinet_score += 3
            if line_str in ('edit', 'next', 'end'):
                fortinet_score += 1
            if line_str.startswith('set ') and fortinet_score > 0:
                fortinet_score += 1
                
            # Palo Alto
            if line_str.startswith('set deviceconfig '):
                paloalto_score += 3
            if line_str.startswith('set network '):
                paloalto_score += 2
            if line_str.startswith('set rulebase '):
                paloalto_score += 2
            if line_str.startswith('set shared '):
                paloalto_score += 2
                
        scores = {
            'cisco': cisco_score,
            'juniper': juniper_score,
            'fortinet': fortinet_score,
            'paloalto': paloalto_score
        }
        
        max_vendor = max(scores, key=scores.get)
        max_score = scores[max_vendor]
        
        if max_score == 0:
            return VendorDetectionResult(vendor='unknown', platform='unknown', device_type='unknown', confidence=0.0)
            
        confidence = min(max_score / 10.0, 1.0)
        
        platforms = {
            'cisco': ('IOS-XE', 'router'),
            'juniper': ('Junos', 'router'),
            'fortinet': ('FortiOS', 'firewall'),
            'paloalto': ('PAN-OS', 'firewall')
        }
        
        platform, device_type = platforms[max_vendor]
        
        return VendorDetectionResult(
            vendor=max_vendor,
            platform=platform,
            device_type=device_type,
            confidence=confidence
        )
