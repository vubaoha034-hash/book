"""Frozen processing contract for reproducible structured artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


PROCESSING_CONTRACT_VERSION = "1.0.0"


@dataclass(frozen=True)
class ProcessingContract:
    """Versions of every component that can change a structured artifact."""

    version: str = PROCESSING_CONTRACT_VERSION
    extraction: str = "extract-v1"
    normalization: str = "normalize-v1"
    chapter_segmentation: str = "chapter-v2-conservative"
    id_contract: str = "artifact-id-v2"
    structured_output_schema: str = "structured-v2"

    def as_dict(self) -> dict[str, str]:
        return asdict(self)

    @property
    def fingerprint(self) -> str:
        payload = json.dumps(
            self.as_dict(),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


DEFAULT_PROCESSING_CONTRACT = ProcessingContract()
