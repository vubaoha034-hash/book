"""Incremental, local-only preprocessing pipeline."""

from __future__ import annotations

import json
import os
import shutil
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from . import __version__
from .chapters import SegmentationResult, segment_chapters
from .cleaning import normalize_text
from .extractors import DEFERRED_EXTENSIONS, ExtractionError, extract_text, iter_source_files
from .hashing import (
    make_chapter_id,
    make_deferred_work_id,
    make_work_id,
    sha256_file,
    sha256_text,
)


@dataclass(frozen=True)
class PreprocessorConfig:
    repo_root: Path
    private_root: Path
    input_dir: Path
    output_dir: Path
    cache_dir: Path
    temp_dir: Path
    logs_dir: Path
    manifest_path: Path

    @classmethod
    def from_roots(cls, repo_root: Path, private_root: Path) -> "PreprocessorConfig":
        return cls(
            repo_root=repo_root,
            private_root=private_root,
            input_dir=private_root / "01_原始小说",
            output_dir=private_root / "02_结构化文本",
            cache_dir=private_root / "cache",
            temp_dir=private_root / "temp",
            logs_dir=private_root / "logs",
            manifest_path=repo_root / "manifests" / "library_manifest.jsonl",
        )

    @property
    def state_path(self) -> Path:
        return self.cache_dir / "preprocessor_state.v1.json"

    @property
    def lock_path(self) -> Path:
        return self.cache_dir / "preprocessor.lock"

    def ensure_layout(self) -> None:
        repo = self.repo_root.resolve()
        private = self.private_root.resolve()
        try:
            private.relative_to(repo)
        except ValueError:
            pass
        else:
            raise RuntimeError("安全检查失败：private_root 不能位于 Git repo_root 内部。")
        for directory in (
            self.input_dir,
            self.output_dir,
            self.cache_dir,
            self.temp_dir,
            self.logs_dir,
            self.manifest_path.parent,
        ):
            directory.mkdir(parents=True, exist_ok=True)


@dataclass
class RunSummary:
    discovered: int = 0
    processed: int = 0
    skipped: int = 0
    failed: int = 0
    duplicates: int = 0
    needs_review: int = 0
    deferred: int = 0
    errors: list[str] = field(default_factory=list)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as target:
        target.write(text)


def _write_json(path: Path, payload: Any) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"状态文件无法读取: {path}: {exc}") from exc


@contextmanager
def _single_run_lock(path: Path) -> Iterator[None]:
    descriptor: int | None = None
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        yield
    except FileExistsError as exc:
        raise RuntimeError(f"已有预处理任务在运行，或上次异常退出留下锁文件: {path}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
            path.unlink(missing_ok=True)


def _chapter_record(work_id: str, normalized_sha: str, chapter: Any) -> dict[str, Any]:
    chapter_id = make_chapter_id(normalized_sha, chapter.index)
    return {
        "work_id": work_id,
        "chapter_id": chapter_id,
        "chapter_index": chapter.index,
        "chapter_title": chapter.title,
        "relative_path": f"text/{chapter.index:04d}.txt",
        "character_count": len(chapter.text),
        "sha256": sha256_text(chapter.text),
        "chapter_text_sha256": sha256_text(chapter.text),
        "detection_confidence": chapter.detection_confidence,
        "source_span": {
            "start_char": chapter.start_char,
            "end_char": chapter.end_char,
        },
        "warnings": list(chapter.warnings),
    }


def _write_structured_work(
    config: PreprocessorConfig,
    work_id: str,
    relative_source: str,
    source_filename: str,
    source_sha: str,
    normalized_sha: str,
    normalized_text: str,
    extraction: Any,
    segmentation: SegmentationResult,
    processed_at: str,
) -> list[dict[str, Any]]:
    destination = config.output_dir / work_id
    if destination.exists():
        existing = _read_json(destination / "work.json", {})
        if existing.get("normalized_text_sha256") != normalized_sha:
            raise RuntimeError(f"work_id 冲突: {work_id}")
        chapters_path = destination / "chapters.jsonl"
        return [json.loads(line) for line in chapters_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    staging = config.temp_dir / f"{work_id}.{os.getpid()}.staging"
    if staging.exists():
        shutil.rmtree(staging)
    (staging / "text").mkdir(parents=True, exist_ok=False)
    chapter_records: list[dict[str, Any]] = []
    for chapter in segmentation.chapters:
        record = _chapter_record(work_id, normalized_sha, chapter)
        chapter_records.append(record)
        _write_text(staging / record["relative_path"], chapter.text)

    warnings = list(dict.fromkeys([*extraction.warnings, *segmentation.warnings]))
    work_record = {
        "work_id": work_id,
        "source_filename": source_filename,
        "source_private_ref": f"raw/{relative_source}",
        "source_format": extraction.source_format,
        "source_sha256": source_sha,
        "original_file_sha256": source_sha,
        "normalized_sha256": normalized_sha,
        "normalized_text_sha256": normalized_sha,
        "title": extraction.title,
        "author": extraction.author,
        "chapter_count": len(chapter_records),
        "character_count": len(normalized_text),
        "processing_version": __version__,
        "processed_at": processed_at,
        "chapter_detection_confidence": segmentation.detection_confidence,
        "needs_review": segmentation.needs_review,
        "warnings": warnings,
    }
    _write_json(staging / "work.json", work_record)
    _write_text(
        staging / "chapters.jsonl",
        "".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n" for item in chapter_records),
    )
    staging.replace(destination)
    return chapter_records


def _duplicate_kind(states: dict[str, dict[str, Any]], current_path: str, source_sha: str, normalized_sha: str) -> tuple[str | None, str | None]:
    normalized_match: str | None = None
    for path, record in states.items():
        if path == current_path or record.get("status") != "processed" or not record.get("present", True):
            continue
        if record.get("source_sha256") == source_sha:
            return "exact_file", record.get("work_id")
        if record.get("normalized_text_sha256") == normalized_sha:
            normalized_match = record.get("work_id")
    if normalized_match:
        return "normalized_text", normalized_match
    return None, None


def _manifest_records(states: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for path, record in states.items():
        if not record.get("present", True):
            continue
        work_id = record.get("work_id") or f"failed_{record.get('source_sha256', 'unknown')[:24]}"
        grouped.setdefault(work_id, []).append((path, record))

    manifest: list[dict[str, Any]] = []
    for work_id, sources in sorted(grouped.items()):
        sources.sort(key=lambda item: item[0].casefold())
        primary = sources[0][1]
        statuses = {item[1].get("status", "failed") for item in sources}
        status = "processed" if "processed" in statuses else ("deferred" if "deferred" in statuses else "failed")
        duplicate_kinds = sorted({item[1].get("duplicate_kind") for item in sources if item[1].get("duplicate_kind")})
        manifest.append({
            "manifest_version": "1.0.0",
            "work_id": work_id,
            "title": primary.get("title"),
            "author": primary.get("author"),
            "source_format": primary.get("source_format"),
            "chapter_count": primary.get("chapter_count", 0),
            "character_count": primary.get("character_count", 0),
            "hash": primary.get("normalized_text_sha256") or primary.get("source_sha256"),
            "original_file_sha256": primary.get("source_sha256"),
            "normalized_text_sha256": primary.get("normalized_text_sha256"),
            "processing_status": status,
            "private_location_id": f"structured/{work_id}" if status == "processed" else None,
            "source_private_refs": [f"raw/{path}" for path, _ in sources],
            "source_count": len(sources),
            "possible_duplicate": bool(duplicate_kinds),
            "duplicate_kinds": duplicate_kinds,
            "needs_review": any(bool(item[1].get("needs_review")) for item in sources),
            "warnings": sorted({warning for _, item in sources for warning in item.get("warnings", [])}),
        })
    return manifest


def _write_manifest(path: Path, records: list[dict[str, Any]]) -> None:
    content = "".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records)
    _write_text(path, content)


def run_preprocessor(config: PreprocessorConfig) -> RunSummary:
    config.ensure_layout()
    summary = RunSummary()
    processed_at = _utc_now()
    log_path = config.logs_dir / f"preprocessor-{processed_at.replace(':', '').replace('-', '')}.jsonl"
    state_payload = _read_json(config.state_path, {"version": "1.0.0", "sources": {}})
    states: dict[str, dict[str, Any]] = state_payload.setdefault("sources", {})
    for record in states.values():
        record["present"] = False

    log_records: list[dict[str, Any]] = []
    with _single_run_lock(config.lock_path):
        for source_path in iter_source_files(config.input_dir):
            summary.discovered += 1
            relative_source = source_path.relative_to(config.input_dir).as_posix()
            source_sha = sha256_file(source_path)
            prior = states.get(relative_source)
            if prior and prior.get("source_sha256") == source_sha and prior.get("status") in {"processed", "deferred"}:
                output_ok = prior.get("status") == "deferred" or (config.output_dir / str(prior.get("work_id")) / "work.json").exists()
                if output_ok:
                    prior["present"] = True
                    summary.skipped += 1
                    log_records.append({"source_ref": f"raw/{relative_source}", "status": "skipped", "source_sha256": source_sha})
                    continue

            if source_path.suffix.lower() in DEFERRED_EXTENSIONS:
                work_id = make_deferred_work_id(source_sha)
                states[relative_source] = {
                    "present": True,
                    "status": "deferred",
                    "work_id": work_id,
                    "source_sha256": source_sha,
                    "normalized_text_sha256": None,
                    "source_format": source_path.suffix.lower().lstrip("."),
                    "title": None,
                    "author": None,
                    "chapter_count": 0,
                    "character_count": 0,
                    "needs_review": False,
                    "warnings": ["unsupported/deferred_in_v1"],
                    "processed_at": processed_at,
                }
                summary.deferred += 1
                log_records.append({"source_ref": f"raw/{relative_source}", "status": "deferred", "source_sha256": source_sha})
                continue

            try:
                extraction = extract_text(source_path)
                normalized = normalize_text(extraction.text)
                if not normalized.strip():
                    raise ExtractionError("提取结果为空。")
                normalized_sha = sha256_text(normalized)
                work_id = make_work_id(normalized_sha)
                duplicate_kind, duplicate_of = _duplicate_kind(states, relative_source, source_sha, normalized_sha)
                segmentation = segment_chapters(normalized)
                chapter_records = _write_structured_work(
                    config=config,
                    work_id=work_id,
                    relative_source=relative_source,
                    source_filename=source_path.name,
                    source_sha=source_sha,
                    normalized_sha=normalized_sha,
                    normalized_text=normalized,
                    extraction=extraction,
                    segmentation=segmentation,
                    processed_at=processed_at,
                )
                warnings = list(dict.fromkeys([*extraction.warnings, *segmentation.warnings]))
                states[relative_source] = {
                    "present": True,
                    "status": "processed",
                    "work_id": work_id,
                    "source_sha256": source_sha,
                    "normalized_text_sha256": normalized_sha,
                    "source_format": extraction.source_format,
                    "title": extraction.title,
                    "author": extraction.author,
                    "chapter_count": len(chapter_records),
                    "character_count": len(normalized),
                    "chapter_detection_confidence": segmentation.detection_confidence,
                    "needs_review": segmentation.needs_review,
                    "duplicate_kind": duplicate_kind,
                    "duplicate_of_work_id": duplicate_of,
                    "warnings": warnings,
                    "processed_at": processed_at,
                }
                summary.processed += 1
                if duplicate_kind:
                    summary.duplicates += 1
                if segmentation.needs_review:
                    summary.needs_review += 1
                log_records.append({
                    "source_ref": f"raw/{relative_source}",
                    "status": "processed",
                    "work_id": work_id,
                    "source_sha256": source_sha,
                    "normalized_text_sha256": normalized_sha,
                    "duplicate_kind": duplicate_kind,
                    "needs_review": segmentation.needs_review,
                })
            except Exception as exc:
                message = f"{source_path.name}: {exc}"
                summary.failed += 1
                summary.errors.append(message)
                states[relative_source] = {
                    "present": True,
                    "status": "failed",
                    "work_id": None,
                    "source_sha256": source_sha,
                    "normalized_text_sha256": None,
                    "source_format": source_path.suffix.lower().lstrip("."),
                    "title": None,
                    "author": None,
                    "chapter_count": 0,
                    "character_count": 0,
                    "needs_review": False,
                    "warnings": [str(exc)],
                    "processed_at": processed_at,
                }
                log_records.append({"source_ref": f"raw/{relative_source}", "status": "failed", "source_sha256": source_sha, "error": str(exc)})

        state_payload["version"] = "1.0.0"
        state_payload["updated_at"] = processed_at
        _write_json(config.state_path, state_payload)
        _write_manifest(config.manifest_path, _manifest_records(states))
        _write_text(log_path, "".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n" for item in log_records))
    return summary
