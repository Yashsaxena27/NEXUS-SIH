import pytest
from backend.app.schemas.security_ir import NormalizedConfig, DeviceInfo, NormalizationResult
from backend.app.normalization.base_adapter import BaseVendorAdapter

class DummyAdapter(BaseVendorAdapter):
    VENDOR_NAME = "dummy"
    def detect(self, raw_config: str):
        return 1.0 if "dummy" in raw_config else 0.0
    def normalize(self, raw_config: str):
        config = NormalizedConfig(device=self._make_device_info(hostname="dummy_host"))
        return NormalizationResult(config=config, evidence=[])

def test_dummy_adapter_detect():
    adapter = DummyAdapter()
    assert adapter.detect("this is dummy config") == 1.0
    assert adapter.detect("this is cisco config") == 0.0

def test_dummy_adapter_normalize():
    adapter = DummyAdapter()
    res = adapter.normalize("dummy")
    assert res.config.device.hostname == "dummy_host"
    assert res.config.device.vendor == "dummy"
    assert len(res.evidence) == 0

def test_empty_config():
    adapter = DummyAdapter()
    res = adapter.normalize("")
    assert res.config.device.vendor == "dummy"

def test_evidence_generation():
    adapter = DummyAdapter()
    ev = adapter._make_evidence(field="test", value=True, source="line 1")
    assert ev.field == "test"
    assert ev.value is True
    assert ev.source == "line 1"
