"""Offline export of private structured chapters for manual ChatGPT upload."""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .hashing import sha256_text


PACKET_VERSION = "1.0.0"
DEFAULT_MAX_CHARS_PER_PART = 80_000
_SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


class PacketExportError(ValueError):
    pass


@dataclass(frozen=True)
class ChapterArtifact:
    record: dict[str, Any]
    text: str


@dataclass(frozen=True)
class SliceUnit:
    chapter: ChapterArtifact
    start_char: int
    end_char: int

    @property
    def text(self) -> str:
        return self.chapter.text[self.start_char:self.end_char]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_work_dir(private_root: Path, work_id: str) -> Path:
    if not _SAFE_ID.fullmatch(work_id):
        raise PacketExportError(f"非法 work_id: {work_id}")
    root = (private_root / "02_结构化文本").resolve()
    work_dir = (root / work_id).resolve()
    try:
        work_dir.relative_to(root)
    except ValueError as exc:
        raise PacketExportError("work_id 越出结构化文本目录。") from exc
    if not work_dir.is_dir():
        raise PacketExportError(f"找不到结构化作品: {work_id}")
    return work_dir


def load_structured_work(private_root: Path, work_id: str) -> tuple[dict[str, Any], list[ChapterArtifact]]:
    work_dir = _safe_work_dir(private_root.resolve(), work_id)
    try:
        work = json.loads((work_dir / "work.json").read_text(encoding="utf-8"))
        records = [
            json.loads(line)
            for line in (work_dir / "chapters.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, json.JSONDecodeError) as exc:
        raise PacketExportError(f"结构化作品元数据损坏: {work_id}") from exc
    if work.get("work_id") != work_id or len(records) != work.get("chapter_count"):
        raise PacketExportError(f"结构化作品契约不完整: {work_id}")
    if not work.get("processing_contract_version") or not work.get("processing_fingerprint"):
        raise PacketExportError(f"结构化作品缺少处理契约: {work_id}")

    chapters: list[ChapterArtifact] = []
    for record in records:
        relative = Path(str(record.get("relative_path", "")))
        path = (work_dir / relative).resolve()
        try:
            path.relative_to(work_dir)
            text = path.read_text(encoding="utf-8")
        except (ValueError, OSError) as exc:
            raise PacketExportError(f"章节文件不可读: {record.get('chapter_id')}") from exc
        if (
            record.get("work_id") != work_id
            or record.get("chapter_text_sha256") != sha256_text(text)
            or record.get("processing_fingerprint") != work.get("processing_fingerprint")
        ):
            raise PacketExportError(f"章节 artifact 验证失败: {record.get('chapter_id')}")
        chapters.append(ChapterArtifact(record=record, text=text))
    return work, chapters


def _part_prefix(work: dict[str, Any]) -> str:
    return (
        "# ChatGPT Private Structured Source Packet\n\n"
        f"WORK: {work['work_id']}\n"
        f"PROCESSING_CONTRACT_VERSION: {work['processing_contract_version']}\n"
        f"PROCESSING_FINGERPRINT: {work['processing_fingerprint']}\n"
        "UPLOAD_MODE: manual_only\n\n"
    )


def _render_block(unit: SliceUnit, work: dict[str, Any]) -> tuple[str, int, int]:
    record = unit.chapter.record
    title = record.get("chapter_title") or "(untitled)"
    slice_text = unit.text
    header = (
        f"## CHAPTER: {record['chapter_index']} — {title}\n\n"
        f"CHAPTER_ID: {record['chapter_id']}\n"
        f"CHAPTER_TEXT_SHA256: {record['chapter_text_sha256']}\n"
        f"PROCESSING_CONTRACT_VERSION: {work['processing_contract_version']}\n"
        f"SLICE_START_CHAR: {unit.start_char}\n"
        f"SLICE_END_CHAR: {unit.end_char}\n"
        f"SLICE_SHA256: {sha256_text(slice_text)}\n\n"
        "--- BEGIN STRUCTURED CHAPTER TEXT ---\n"
    )
    suffix = "\n--- END STRUCTURED CHAPTER TEXT ---\n\n"
    return header + slice_text + suffix, len(header), len(header) + len(slice_text)


def _split_chapter(chapter: ChapterArtifact, work: dict[str, Any], max_chars: int) -> list[SliceUnit]:
    prefix_size = len(_part_prefix(work))
    whole = SliceUnit(chapter, 0, len(chapter.text))
    if prefix_size + len(_render_block(whole, work)[0]) <= max_chars:
        return [whole]

    units: list[SliceUnit] = []
    start = 0
    while start < len(chapter.text):
        low, high = start + 1, len(chapter.text)
        best: int | None = None
        while low <= high:
            middle = (low + high) // 2
            candidate = SliceUnit(chapter, start, middle)
            size = prefix_size + len(_render_block(candidate, work)[0])
            if size <= max_chars:
                best = middle
                low = middle + 1
            else:
                high = middle - 1
        if best is None:
            raise PacketExportError("max-chars-per-part 太小，无法容纳 Packet 元数据和一个字符。")
        units.append(SliceUnit(chapter, start, best))
        start = best
    return units


def _write_part(path: Path, work: dict[str, Any], units: list[SliceUnit]) -> dict[str, Any]:
    content = _part_prefix(work)
    slices: list[dict[str, Any]] = []
    for unit in units:
        block, text_start, text_end = _render_block(unit, work)
        base = len(content)
        content += block
        record = unit.chapter.record
        slices.append({
            "chapter_index": record["chapter_index"],
            "chapter_id": record["chapter_id"],
            "chapter_text_sha256": record["chapter_text_sha256"],
            "slice_start_char": unit.start_char,
            "slice_end_char": unit.end_char,
            "slice_sha256": sha256_text(unit.text),
            "part_text_start_char": base + text_start,
            "part_text_end_char": base + text_end,
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as target:
        target.write(content)
    return {
        "relative_path": path.parent.name + "/" + path.name,
        "character_count": len(content),
        "part_sha256": sha256_text(content),
        "slices": slices,
    }


def export_work_packet(private_root: Path, work_id: str, max_chars_per_part: int = DEFAULT_MAX_CHARS_PER_PART) -> Path:
    if max_chars_per_part < 400:
        raise PacketExportError("max-chars-per-part 必须至少为 400。")
    work, chapters = load_structured_work(private_root, work_id)
    packet_root = private_root / "03_ChatGPT蒸馏包"
    destination = packet_root / work_id
    staging = packet_root / f".{work_id}.{os.getpid()}.staging"
    backup = packet_root / f".{work_id}.{os.getpid()}.backup"
    if staging.exists():
        shutil.rmtree(staging)
    if backup.exists():
        shutil.rmtree(backup)
    (staging / "parts").mkdir(parents=True, exist_ok=False)

    units: list[SliceUnit] = []
    for chapter in chapters:
        units.extend(_split_chapter(chapter, work, max_chars_per_part))

    grouped: list[list[SliceUnit]] = []
    current: list[SliceUnit] = []
    current_size = len(_part_prefix(work))
    for unit in units:
        block_size = len(_render_block(unit, work)[0])
        if current and current_size + block_size > max_chars_per_part:
            grouped.append(current)
            current = []
            current_size = len(_part_prefix(work))
        current.append(unit)
        current_size += block_size
    if current:
        grouped.append(current)

    parts: list[dict[str, Any]] = []
    for index, group in enumerate(grouped, start=1):
        part = _write_part(staging / "parts" / f"part_{index:03d}.md", work, group)
        if part["character_count"] > max_chars_per_part:
            raise PacketExportError("内部错误：生成的 part 超过 max-chars-per-part。")
        parts.append(part)

    manifest = {
        "packet_version": PACKET_VERSION,
        "work_id": work_id,
        "normalized_text_sha256": work["normalized_text_sha256"],
        "processing_contract_version": work["processing_contract_version"],
        "processing_fingerprint": work["processing_fingerprint"],
        "title": work.get("title"),
        "author": work.get("author"),
        "chapter_count": work["chapter_count"],
        "character_count": work["character_count"],
        "chapters": [
            {
                "chapter_index": chapter.record["chapter_index"],
                "chapter_id": chapter.record["chapter_id"],
                "chapter_text_sha256": chapter.record["chapter_text_sha256"],
                "character_count": len(chapter.text),
            }
            for chapter in chapters
        ],
        "max_chars_per_part": max_chars_per_part,
        "parts": parts,
        "created_at": _utc_now(),
    }
    with (staging / "packet_manifest.json").open("w", encoding="utf-8", newline="\n") as target:
        json.dump(manifest, target, ensure_ascii=False, indent=2)
        target.write("\n")

    if destination.exists():
        destination.replace(backup)
    try:
        staging.replace(destination)
    except Exception:
        if backup.exists() and not destination.exists():
            backup.replace(destination)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)
    return destination


def available_work_ids(private_root: Path) -> list[str]:
    root = private_root / "02_结构化文本"
    if not root.is_dir():
        return []
    return sorted(path.name for path in root.iterdir() if path.is_dir() and (path / "work.json").is_file())


def export_packets(
    private_root: Path,
    work_ids: Iterable[str],
    max_chars_per_part: int = DEFAULT_MAX_CHARS_PER_PART,
) -> list[Path]:
    selected = list(dict.fromkeys(work_ids))
    if not selected:
        raise PacketExportError("没有选择任何 work_id。")
    return [export_work_packet(private_root, work_id, max_chars_per_part) for work_id in selected]
