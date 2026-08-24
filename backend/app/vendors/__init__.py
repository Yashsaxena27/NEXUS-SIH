from .detector import VendorDetector, VendorDetectionResult

def detect_vendor(raw_config: str) -> VendorDetectionResult:
    return VendorDetector.detect_vendor(raw_config)
