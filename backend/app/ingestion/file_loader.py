"""
Configuration file ingestion — load configs from files or text input.

Supports:
    - Single file upload
    - Bulk file upload (directory)
    - Raw text input (for testing/API)

Designed to be extensible for future sources:
    - Netmiko / SSH
    - NAPALM
    - Device APIs
    - Configuration repositories
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class IngestionResult:
    """Result of ingesting a configuration."""
    raw_config: str
    source: str  # File path or "text_input" or "api"
    filename: Optional[str] = None
    file_size: int = 0
    sha256_hash: str = ""
    ingested_at: str = ""

    def __post_init__(self):
        if not self.sha256_hash:
            self.sha256_hash = hashlib.sha256(self.raw_config.encode()).hexdigest()
        if not self.ingested_at:
            self.ingested_at = datetime.now(timezone.utc).isoformat()


class FileIngestionSource:
    """Load configuration from local files."""

    SUPPORTED_EXTENSIONS = {".cfg", ".conf", ".txt", ".config", ".log"}

    def load_file(self, file_path: str | Path) -> IngestionResult:
        """Load a single configuration file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file extension '{path.suffix}'. "
                f"Supported: {self.SUPPORTED_EXTENSIONS}"
            )

        raw_config = path.read_text(encoding="utf-8", errors="replace")

        return IngestionResult(
            raw_config=raw_config,
            source=str(path.absolute()),
            filename=path.name,
            file_size=path.stat().st_size,
        )

    def load_directory(self, dir_path: str | Path) -> list[IngestionResult]:
        """Load all configuration files from a directory."""
        path = Path(dir_path)
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        results = []
        for file_path in sorted(path.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    result = self.load_file(file_path)
                    results.append(result)
                except (ValueError, UnicodeDecodeError) as e:
                    print(f"  WARNING: Skipping {file_path.name}: {e}")

        return results


class TextIngestionSource:
    """Load configuration from raw text (for testing and API)."""

    def load_text(self, raw_config: str, label: str = "text_input") -> IngestionResult:
        """Create an ingestion result from raw text."""
        return IngestionResult(
            raw_config=raw_config,
            source=label,
            filename=None,
            file_size=len(raw_config.encode()),
        )
