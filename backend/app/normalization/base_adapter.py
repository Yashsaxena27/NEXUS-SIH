"""
Base adapter interface for vendor-specific configuration normalization.

Each vendor adapter inherits from BaseVendorAdapter and implements:
    - detect(): check if a raw config belongs to this vendor
    - normalize(): convert raw config into NormalizedConfig + evidence
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Optional

from backend.app.schemas.security_ir import (
    DeviceInfo,
    InterpretationMethod,
    NormalizationResult,
    NormalizedConfig,
    PropertyEvidence,
    UnknownCommand,
)


class BaseVendorAdapter(ABC):
    """Abstract base class for vendor-specific configuration adapters."""

    VENDOR_NAME: str = ""
    PLATFORM: str = ""
    DEVICE_TYPE: str = ""

    @abstractmethod
    def detect(self, raw_config: str) -> Optional[float]:
        """
        Check if this adapter can handle the given configuration.

        Returns:
            Confidence score (0.0–1.0) if this vendor is detected, None otherwise.
        """
        ...

    @abstractmethod
    def normalize(self, raw_config: str, adaptive_rules: Optional[list] = None) -> NormalizationResult:
        """
        Parse and normalize a raw configuration into the vendor-neutral IR.

        Returns:
            NormalizationResult containing the normalized config, evidence, and unknowns.
        """
        ...
        
    def _apply_adaptive_rules(self, raw_config: str, config: NormalizedConfig, evidence: list, adaptive_rules: Optional[list]):
        if not adaptive_rules:
            return
            
        for rule in adaptive_rules:
            if rule.vendor == self.VENDOR_NAME or rule.vendor == "all":
                # We do a simple substring match for the raw pattern
                if rule.raw_pattern in raw_config:
                    parts = rule.mapped_control.split('.')
                    obj = config
                    try:
                        for part in parts[:-1]:
                            if hasattr(obj, part):
                                obj = getattr(obj, part)
                                if obj is None:
                                    break
                        if obj is not None:
                            setattr(obj, parts[-1], rule.mapped_value_json)
                            evidence.append(self._make_evidence(
                                field=rule.mapped_control,
                                value=rule.mapped_value_json,
                                source="adaptive_rule",
                                raw_evidence=rule.raw_pattern,
                                method=InterpretationMethod.HUMAN_CONFIRMED
                            ))
                    except Exception as e:
                        print(f"Failed to apply adaptive rule: {e}")

    # -------------------------------------------------------------------
    # Helper methods available to all adapters
    # -------------------------------------------------------------------

    def _make_evidence(
        self,
        field: str,
        value,
        source: Optional[str] = None,
        raw_evidence: Optional[str] = None,
        confidence: float = 1.0,
        method: InterpretationMethod = InterpretationMethod.DETERMINISTIC_PARSER,
    ) -> PropertyEvidence:
        """Create a PropertyEvidence record."""
        return PropertyEvidence(
            field=field,
            value=value,
            confidence=confidence,
            source=source,
            method=method,
            raw_evidence=raw_evidence,
        )

    def _make_device_info(
        self,
        hostname: Optional[str] = None,
        version: Optional[str] = None,
    ) -> DeviceInfo:
        """Create DeviceInfo with this adapter's vendor/platform defaults."""
        return DeviceInfo(
            vendor=self.VENDOR_NAME,
            platform=self.PLATFORM,
            device_type=self.DEVICE_TYPE,
            version=version,
            hostname=hostname,
        )

    def _find_lines(self, raw_config: str, pattern: str, flags: int = 0) -> list[tuple[int, str]]:
        """
        Find all lines matching a regex pattern.

        Returns list of (line_number, line_text) tuples (1-indexed).
        """
        results = []
        for i, line in enumerate(raw_config.splitlines(), start=1):
            if re.search(pattern, line, flags):
                results.append((i, line.strip()))
        return results

    def _find_first_line(self, raw_config: str, pattern: str, flags: int = 0) -> Optional[tuple[int, str]]:
        """Find the first line matching a regex pattern."""
        matches = self._find_lines(raw_config, pattern, flags)
        return matches[0] if matches else None

    def _extract_value(self, line: str, pattern: str, group: int = 1) -> Optional[str]:
        """Extract a regex group from a line."""
        m = re.search(pattern, line)
        return m.group(group) if m else None
