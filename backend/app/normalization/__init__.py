from typing import Optional
from backend.app.schemas.security_ir import NormalizationResult, NormalizedConfig, DeviceInfo
from backend.app.vendors.detector import VendorDetector, VendorDetectionResult

from .cisco_adapter import CiscoAdapter
from .juniper_adapter import JuniperAdapter
from .fortinet_adapter import FortinetAdapter
from .paloalto_adapter import PaloAltoAdapter

def detect_vendor(raw_config: str) -> VendorDetectionResult:
    return VendorDetector.detect_vendor(raw_config)

def normalize_config(raw_config: str, vendor_hint: Optional[str] = None) -> NormalizationResult:
    if vendor_hint:
        vendor_name = vendor_hint.lower()
    else:
        detection = detect_vendor(raw_config)
        vendor_name = detection.vendor
        
    adapters = {
        'cisco': CiscoAdapter(),
        'juniper': JuniperAdapter(),
        'fortinet': FortinetAdapter(),
        'paloalto': PaloAltoAdapter()
    }
    
    if vendor_name in adapters:
        return adapters[vendor_name].normalize(raw_config)
        
    # Fallback for unknown vendor
    return NormalizationResult(
        config=NormalizedConfig(
            device=DeviceInfo(vendor="unknown", platform="unknown", device_type="unknown")
        ),
        evidence=[],
        raw_config=raw_config,
        parse_errors=[f"Unsupported or unknown vendor: {vendor_name}"]
    )
