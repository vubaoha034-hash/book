"""Deterministic hashes and identifiers."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_work_id(normalized_text_sha256: str) -> str:
    return f"wrk_{normalized_text_sha256[:24]}"


def make_deferred_work_id(source_sha256: str) -> str:
    return f"deferred_{source_sha256[:24]}"


def make_chapter_id(normalized_text_sha256: str, chapter_index: int) -> str:
    seed = f"{normalized_text_sha256}:{chapter_index}".encode("ascii")
    return f"ch_{hashlib.sha256(seed).hexdigest()[:24]}"
