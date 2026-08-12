"""Machine validation for chapter-relative EvidenceRef V1 coordinates."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator

from .hashing import sha256_text


_SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")
_HASH = re.compile(r"^[a-f0-9]{64}$")


class EvidenceValidationError(ValueError):
    pass


def _safe_work_dir(private_root: Path, work_id: str) -> Path:
    if not isinstance(work_id, str) or not _SAFE_ID.fullmatch(work_id):
        raise EvidenceValidationError("work_id 格式非法。")
    structured_root = (private_root / "02_结构化文本").resolve()
    work_dir = (structured_root / work_id).resolve()
    try:
        work_dir.relative_to(structured_root)
    except ValueError as exc:
        raise EvidenceValidationError("work_id 越出结构化文本目录。") from exc
    if not work_dir.is_dir():
        raise EvidenceValidationError(f"找不到结构化作品: {work_id}")
    return work_dir


def _chapter_record(work_dir: Path, chapter_id: str) -> dict[str, Any]:
    if not isinstance(chapter_id, str) or not _SAFE_ID.fullmatch(chapter_id):
        raise EvidenceValidationError("chapter_id 格式非法。")
    try:
        records = [
            json.loads(line)
            for line in (work_dir / "chapters.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError("chapters.jsonl 无法读取。") from exc
    matches = [record for record in records if record.get("chapter_id") == chapter_id]
    if len(matches) != 1:
        raise EvidenceValidationError(f"chapter_id 必须唯一存在，实际匹配 {len(matches)} 条。")
    return matches[0]


def validate_evidence_ref(evidence_ref: dict[str, Any], private_root: Path) -> dict[str, Any]:
    required = {
        "work_id",
        "chapter_id",
        "chapter_text_sha256",
        "span_scope",
        "source_span",
        "quote_sha256",
    }
    missing = sorted(required - set(evidence_ref))
    if missing:
        raise EvidenceValidationError(f"EvidenceRef 缺少字段: {', '.join(missing)}")
    if evidence_ref["span_scope"] != "chapter_text":
        raise EvidenceValidationError("span_scope 必须是 chapter_text。")
    if not isinstance(evidence_ref["chapter_text_sha256"], str) or not _HASH.fullmatch(evidence_ref["chapter_text_sha256"]):
        raise EvidenceValidationError("chapter_text_sha256 必须是小写 SHA-256。")
    if not isinstance(evidence_ref["quote_sha256"], str) or not _HASH.fullmatch(evidence_ref["quote_sha256"]):
        raise EvidenceValidationError("quote_sha256 必须是小写 SHA-256。")

    work_dir = _safe_work_dir(private_root.resolve(), evidence_ref["work_id"])
    chapter = _chapter_record(work_dir, evidence_ref["chapter_id"])
    if chapter.get("work_id") != evidence_ref["work_id"]:
        raise EvidenceValidationError("章节记录的 work_id 不匹配。")
    relative = Path(str(chapter.get("relative_path", "")))
    chapter_path = (work_dir / relative).resolve()
    try:
        chapter_path.relative_to(work_dir.resolve())
    except ValueError as exc:
        raise EvidenceValidationError("章节相对路径越界。") from exc
    try:
        chapter_text = chapter_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise EvidenceValidationError("章节正文文件无法读取。") from exc

    actual_chapter_sha = sha256_text(chapter_text)
    if chapter.get("chapter_text_sha256") != actual_chapter_sha:
        raise EvidenceValidationError("结构化章节记录的 Hash 与正文不一致。")
    if evidence_ref["chapter_text_sha256"] != actual_chapter_sha:
        raise EvidenceValidationError("EvidenceRef 的 chapter_text_sha256 不匹配。")

    span = evidence_ref["source_span"]
    if not isinstance(span, dict):
        raise EvidenceValidationError("source_span 必须是对象。")
    start = span.get("start_char")
    end = span.get("end_char")
    if (
        isinstance(start, bool)
        or isinstance(end, bool)
        or not isinstance(start, int)
        or not isinstance(end, int)
        or start < 0
        or end <= start
        or end > len(chapter_text)
    ):
        raise EvidenceValidationError(
            "source_span 必须是 chapter-relative、0-based、start inclusive、end exclusive，且非空不越界。"
        )
    quote = chapter_text[start:end]
    actual_quote_sha = sha256_text(quote)
    if evidence_ref["quote_sha256"] != actual_quote_sha:
        raise EvidenceValidationError("quote_sha256 与章节切片不匹配。")
    return {
        "status": "PASS",
        "work_id": evidence_ref["work_id"],
        "chapter_id": evidence_ref["chapter_id"],
        "start_char": start,
        "end_char": end,
        "quote_sha256": actual_quote_sha,
    }


def iter_evidence_refs(payload: Any) -> Iterator[dict[str, Any]]:
    if isinstance(payload, dict):
        if "quote_sha256" in payload and ("chapter_id" in payload or "source_span" in payload):
            yield payload
        for value in payload.values():
            yield from iter_evidence_refs(value)
    elif isinstance(payload, list):
        for value in payload:
            yield from iter_evidence_refs(value)


def validate_evidence_payload(payload: Any, private_root: Path) -> list[dict[str, Any]]:
    refs = list(iter_evidence_refs(payload))
    if not refs:
        raise EvidenceValidationError("输入中没有 EvidenceRef。")
    return [validate_evidence_ref(ref, private_root) for ref in refs]
