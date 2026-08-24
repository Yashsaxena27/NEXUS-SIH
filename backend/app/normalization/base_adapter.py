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
    def normalize(self, raw_config: str) -> NormalizationResult:
        """
        Parse and normalize a raw configuration into the vendor-neutral IR.

        Returns:
            NormalizationResult containing the normalized config, evidence, and unknowns.
        """
        ...

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
