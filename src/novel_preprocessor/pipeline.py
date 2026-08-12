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
from .contract import DEFAULT_PROCESSING_CONTRACT, ProcessingContract
from .extractors import DEFERRED_EXTENSIONS, ExtractionError, extract_text, iter_source_files
from .hashing import (
    make_chapter_id,
    make_deferred_work_id,
    make_work_id,
    sha256_file,
    sha256_text,
)
from .integrity import SourceIntegrityResult, analyze_source_integrity, unknown_integrity


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
    processing_contract: ProcessingContract = DEFAULT_PROCESSING_CONTRACT

    @classmethod
    def from_roots(
        cls,
        repo_root: Path,
        private_root: Path,
        processing_contract: ProcessingContract = DEFAULT_PROCESSING_CONTRACT,
    ) -> "PreprocessorConfig":
        return cls(
            repo_root=repo_root,
            private_root=private_root,
            input_dir=private_root / "01_原始小说",
            output_dir=private_root / "02_结构化文本",
            cache_dir=private_root / "cache",
            temp_dir=private_root / "temp",
            logs_dir=private_root / "logs",
            manifest_path=private_root / "manifests" / "library_manifest.jsonl",
            processing_contract=processing_contract,
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
    source_integrity_counts: dict[str, int] = field(
        default_factory=lambda: {"PASS": 0, "WARNING": 0, "FAIL": 0, "UNKNOWN": 0}
    )
    distillation_blocked: list[dict[str, Any]] = field(default_factory=list)


def _record_integrity_summary(
    summary: RunSummary,
    work_id: str | None,
    status: str | None,
    allowed: bool,
    reason_codes: list[str] | None,
) -> None:
    normalized_status = status if status in summary.source_integrity_counts else "UNKNOWN"
    summary.source_integrity_counts[normalized_status] += 1
    if not allowed:
        summary.distillation_blocked.append({
            "work_id": work_id or "unknown",
            "status": normalized_status,
            "reason_codes": list(reason_codes or ["integrity_status_not_pass"]),
        })


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


def _chapter_record(
    work_id: str,
    normalized_sha: str,
    chapter: Any,
    contract: ProcessingContract,
) -> dict[str, Any]:
    chapter_sha = sha256_text(chapter.text)
    chapter_id = make_chapter_id(
        normalized_sha,
        chapter.index,
        chapter_sha,
        contract.fingerprint,
        chapter.start_char,
        chapter.end_char,
    )
    return {
        "work_id": work_id,
        "chapter_id": chapter_id,
        "chapter_index": chapter.index,
        "chapter_title": chapter.title,
        "relative_path": f"text/{chapter.index:04d}.txt",
        "character_count": len(chapter.text),
        "sha256": chapter_sha,
        "chapter_text_sha256": chapter_sha,
        "processing_contract_version": contract.version,
        "processing_fingerprint": contract.fingerprint,
        "detection_confidence": chapter.detection_confidence,
        "span_scope": "chapter_text",
        "source_span": {
            "start_char": 0,
            "end_char": len(chapter.text),
        },
        "work_text_span": {
            "start_char": chapter.start_char,
            "end_char": chapter.end_char,
        },
        "warnings": list(chapter.warnings),
    }


def _structured_output_complete(
    destination: Path,
    normalized_sha: str,
    contract: ProcessingContract,
) -> bool:
    """Verify all files needed for a safe incremental skip."""

    try:
        work = _read_json(destination / "work.json", {})
        if (
            work.get("normalized_text_sha256") != normalized_sha
            or work.get("processing_contract_version") != contract.version
            or work.get("processing_fingerprint") != contract.fingerprint
        ):
            return False
        integrity = work.get("source_integrity")
        integrity_status = work.get("source_integrity_status")
        if (
            not isinstance(integrity, dict)
            or integrity_status not in {"PASS", "WARNING", "FAIL", "UNKNOWN"}
            or integrity.get("source_integrity_status") != integrity_status
            or work.get("distillation_allowed") is not (integrity_status == "PASS")
        ):
            return False
        front_present = work.get("front_matter_present")
        front_relative = work.get("front_matter_relative_path")
        front_count = work.get("front_matter_character_count")
        front_hash = work.get("front_matter_sha256")
        if not isinstance(front_present, bool) or not isinstance(front_count, int) or front_count < 0:
            return False
        if front_present:
            if front_relative != "front_matter.txt":
                return False
            front_text = (destination / front_relative).read_text(encoding="utf-8")
            if len(front_text) != front_count or sha256_text(front_text) != front_hash:
                return False
        elif front_relative is not None or front_hash is not None or front_count != 0:
            return False
        lines = (destination / "chapters.jsonl").read_text(encoding="utf-8").splitlines()
        chapters = [json.loads(line) for line in lines if line.strip()]
        if len(chapters) != work.get("chapter_count") or not chapters:
            return False
        seen_ids: set[str] = set()
        for expected_index, chapter in enumerate(chapters, start=1):
            relative = Path(chapter["relative_path"])
            chapter_path = (destination / relative).resolve()
            chapter_path.relative_to(destination.resolve())
            if not chapter_path.is_file():
                return False
            text = chapter_path.read_text(encoding="utf-8")
            work_span = chapter.get("work_text_span")
            if not isinstance(work_span, dict):
                return False
            start = work_span.get("start_char")
            end = work_span.get("end_char")
            if (
                isinstance(start, bool)
                or isinstance(end, bool)
                or not isinstance(start, int)
                or not isinstance(end, int)
                or start < 0
                or end < start
                or chapter.get("chapter_index") != expected_index
                or chapter.get("work_id") != work.get("work_id")
            ):
                return False
            chapter_sha = sha256_text(text)
            expected_id = make_chapter_id(
                normalized_sha,
                expected_index,
                chapter_sha,
                contract.fingerprint,
                start,
                end,
            )
            if (
                chapter_sha != chapter.get("chapter_text_sha256")
                or chapter.get("chapter_id") != expected_id
                or expected_id in seen_ids
                or chapter.get("processing_fingerprint") != contract.fingerprint
                or chapter.get("processing_contract_version") != contract.version
                or chapter.get("span_scope") != "chapter_text"
                or chapter.get("source_span") != {"start_char": 0, "end_char": len(text)}
            ):
                return False
            seen_ids.add(expected_id)
        return True
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return False


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
    integrity: SourceIntegrityResult,
    processed_at: str,
) -> list[dict[str, Any]]:
    destination = config.output_dir / work_id
    contract = config.processing_contract
    if _structured_output_complete(destination, normalized_sha, contract):
        chapters_path = destination / "chapters.jsonl"
        return [json.loads(line) for line in chapters_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    staging = config.temp_dir / f"{work_id}.{os.getpid()}.staging"
    if staging.exists():
        shutil.rmtree(staging)
    (staging / "text").mkdir(parents=True, exist_ok=False)
    chapter_records: list[dict[str, Any]] = []
    for chapter in segmentation.chapters:
        record = _chapter_record(work_id, normalized_sha, chapter, contract)
        chapter_records.append(record)
        _write_text(staging / record["relative_path"], chapter.text)

    front_matter_present = bool(segmentation.front_matter)
    front_matter_relative_path = "front_matter.txt" if front_matter_present else None
    front_matter_sha256 = sha256_text(segmentation.front_matter) if front_matter_present else None
    if front_matter_present:
        _write_text(staging / "front_matter.txt", segmentation.front_matter)

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
        "front_matter_present": front_matter_present,
        "front_matter_relative_path": front_matter_relative_path,
        "front_matter_sha256": front_matter_sha256,
        "front_matter_character_count": len(segmentation.front_matter),
        "processing_version": __version__,
        "processing_contract_version": contract.version,
        "processing_fingerprint": contract.fingerprint,
        "processing_components": contract.as_dict(),
        "processed_at": processed_at,
        "chapter_detection_confidence": segmentation.detection_confidence,
        "needs_review": segmentation.needs_review,
        "warnings": warnings,
        "source_integrity_status": integrity.source_integrity_status,
        "distillation_allowed": integrity.distillation_allowed,
        "source_integrity": integrity.as_dict(),
    }
    _write_json(staging / "work.json", work_record)
    _write_text(
        staging / "chapters.jsonl",
        "".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n" for item in chapter_records),
    )
    backup = config.temp_dir / f"{work_id}.{os.getpid()}.backup"
    if backup.exists():
        shutil.rmtree(backup)
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
            "manifest_version": "1.1.0",
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
            "processing_contract_version": primary.get("processing_contract_version"),
            "processing_fingerprint": primary.get("processing_fingerprint"),
            "private_location_id": f"structured/{work_id}" if status == "processed" else None,
            "source_private_refs": [f"raw/{path}" for path, _ in sources],
            "source_count": len(sources),
            "possible_duplicate": bool(duplicate_kinds),
            "duplicate_kinds": duplicate_kinds,
            "needs_review": any(bool(item[1].get("needs_review")) for item in sources),
            "warnings": sorted({warning for _, item in sources for warning in item.get("warnings", [])}),
            "source_integrity_status": primary.get("source_integrity_status", "UNKNOWN"),
            "distillation_allowed": bool(primary.get("distillation_allowed", False)),
            "source_integrity": primary.get("source_integrity", unknown_integrity().as_dict()),
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
            contract = config.processing_contract
            if (
                prior
                and prior.get("source_sha256") == source_sha
                and prior.get("processing_fingerprint") == contract.fingerprint
                and prior.get("status") in {"processed", "deferred"}
            ):
                output_ok = prior.get("status") == "deferred" or _structured_output_complete(
                    config.output_dir / str(prior.get("work_id")),
                    str(prior.get("normalized_text_sha256")),
                    contract,
                )
                if output_ok:
                    prior["present"] = True
                    summary.skipped += 1
                    prior_integrity = prior.get("source_integrity", {})
                    _record_integrity_summary(
                        summary,
                        prior.get("work_id"),
                        prior.get("source_integrity_status"),
                        bool(prior.get("distillation_allowed", False)),
                        prior_integrity.get("reason_codes") if isinstance(prior_integrity, dict) else None,
                    )
                    log_records.append({"source_ref": f"raw/{relative_source}", "status": "skipped", "source_sha256": source_sha})
                    continue

            if source_path.suffix.lower() in DEFERRED_EXTENSIONS:
                work_id = make_deferred_work_id(source_sha)
                integrity = unknown_integrity("unsupported_source_format")
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
                    "processing_contract_version": contract.version,
                    "processing_fingerprint": contract.fingerprint,
                    "source_integrity_status": integrity.source_integrity_status,
                    "distillation_allowed": integrity.distillation_allowed,
                    "source_integrity": integrity.as_dict(),
                    "processed_at": processed_at,
                }
                summary.deferred += 1
                _record_integrity_summary(summary, work_id, integrity.source_integrity_status, False, integrity.reason_codes)
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
                integrity = analyze_source_integrity(chapter.title for chapter in segmentation.chapters)
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
                    integrity=integrity,
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
                    "processing_contract_version": contract.version,
                    "processing_fingerprint": contract.fingerprint,
                    "source_integrity_status": integrity.source_integrity_status,
                    "distillation_allowed": integrity.distillation_allowed,
                    "source_integrity": integrity.as_dict(),
                    "processed_at": processed_at,
                }
                summary.processed += 1
                _record_integrity_summary(
                    summary,
                    work_id,
                    integrity.source_integrity_status,
                    integrity.distillation_allowed,
                    integrity.reason_codes,
                )
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
                    "source_integrity_status": integrity.source_integrity_status,
                    "distillation_allowed": integrity.distillation_allowed,
                    "integrity_reason_codes": integrity.reason_codes,
                })
            except Exception as exc:
                message = f"{source_path.name}: {exc}"
                summary.failed += 1
                summary.errors.append(message)
                integrity = unknown_integrity("preprocessing_failed")
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
                    "processing_contract_version": contract.version,
                    "processing_fingerprint": contract.fingerprint,
                    "source_integrity_status": integrity.source_integrity_status,
                    "distillation_allowed": integrity.distillation_allowed,
                    "source_integrity": integrity.as_dict(),
                    "processed_at": processed_at,
                }
                _record_integrity_summary(summary, None, integrity.source_integrity_status, False, integrity.reason_codes)
                log_records.append({"source_ref": f"raw/{relative_source}", "status": "failed", "source_sha256": source_sha, "error": str(exc)})

        state_payload["version"] = "1.2.0"
        state_payload["processing_contract_version"] = config.processing_contract.version
        state_payload["processing_fingerprint"] = config.processing_contract.fingerprint
        state_payload["updated_at"] = processed_at
        _write_json(config.state_path, state_payload)
        _write_manifest(config.manifest_path, _manifest_records(states))
        _write_text(log_path, "".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n" for item in log_records))
    return summary
