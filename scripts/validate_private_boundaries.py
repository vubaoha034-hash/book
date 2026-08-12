#!/usr/bin/env python3
"""Path and exact-content leakage protection for private novel artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence


ARCHIVE_EXTENSIONS = {".epub", ".mobi", ".azw", ".azw3"}


def _git_paths(repo: Path, arguments: Sequence[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [item.decode("utf-8", errors="surrogateescape") for item in result.stdout.split(b"\0") if item]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def classify_forbidden(path: str) -> set[str]:
    normalized = path.replace("\\", "/").lstrip("./")
    pure = PurePosixPath(normalized)
    lower_parts = [part.casefold() for part in pure.parts]
    reasons: set[str] = set()

    if "_private" in lower_parts:
        reasons.add("private")

    extension = pure.suffix.casefold()
    if extension in ARCHIVE_EXTENSIONS:
        reasons.add("novel_source")

    lower_path = normalized.casefold()
    if (
        lower_path.startswith("sources/books/") and pure.name != ".gitkeep"
    ) or "01_原始小说" in pure.parts:
        reasons.add("novel_source")

    if "library/_extracted/" in lower_path and pure.name != ".gitkeep":
        reasons.add("full_chapter_text")
    if "02_结构化文本" in pure.parts:
        reasons.add("full_chapter_text")
    if re.search(r"(?:^|/)(?:structured|结构化文本)(?:/.*)?/text/\d{4,}\.txt$", lower_path):
        reasons.add("full_chapter_text")
    if "03_ChatGPT蒸馏包" in pure.parts or "chatgpt_packets" in lower_parts:
        reasons.add("chatgpt_packet")
    return reasons


def _private_hashes(private_root: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    raw_hashes: dict[str, list[str]] = {}
    chapter_hashes: dict[str, list[str]] = {}

    raw_root = private_root / "01_原始小说"
    if raw_root.is_dir():
        for path in raw_root.rglob("*"):
            if path.is_file() and path.stat().st_size > 0:
                raw_hashes.setdefault(_sha256(path.read_bytes()), []).append(
                    f"01_原始小说/{path.relative_to(raw_root).as_posix()}"
                )

    structured_root = private_root / "02_结构化文本"
    if structured_root.is_dir():
        for path in structured_root.glob("*/text/*.txt"):
            if path.is_file() and path.stat().st_size > 0:
                chapter_hashes.setdefault(_sha256(path.read_bytes()), []).append(
                    f"02_结构化文本/{path.relative_to(structured_root).as_posix()}"
                )
    return raw_hashes, chapter_hashes


def _candidate_hashes(repo: Path, path: str) -> set[str]:
    hashes: set[str] = set()
    working = repo / Path(path)
    if working.is_file():
        hashes.add(_sha256(working.read_bytes()))
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f":{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        hashes.add(_sha256(result.stdout))
    return hashes


def _approved_synthetic_fixture(repo: Path, path: str, digest: str) -> bool:
    """Allow an explicitly declared synthetic Golden, never an arbitrary repo path."""

    pure = PurePosixPath(path.replace("\\", "/"))
    if len(pure.parts) != 4 or pure.parts[:3] != ("tests", "fixtures", "golden") or pure.suffix != ".txt":
        return False
    expected = repo / Path(*pure.with_suffix(".expected.json").parts)
    try:
        payload = json.loads(expected.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return payload.get("synthetic_public_fixture") is True and payload.get("source_sha256") == digest


def validate_repo(repo: Path, private_root: Path | None = None) -> dict[str, object]:
    tracked = set(_git_paths(repo, ["ls-files", "-z"]))
    staged = set(_git_paths(repo, ["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]))
    inspected = sorted(tracked | staged)
    findings: list[dict[str, object]] = []
    count_keys = (
        "private",
        "novel_source",
        "full_chapter_text",
        "chatgpt_packet",
        "raw_novel_exact_content",
        "structured_chapter_exact_content",
    )
    counts = {key: 0 for key in count_keys}
    for path in inspected:
        reasons = classify_forbidden(path)
        if reasons:
            findings.append({"path": path, "reasons": sorted(reasons)})
            for reason in reasons:
                counts[reason] += 1

    exact_findings: list[dict[str, object]] = []
    approved_synthetic_matches = 0
    effective_private = private_root or (repo.parent / "_private")
    raw_hashes: dict[str, list[str]] = {}
    chapter_hashes: dict[str, list[str]] = {}
    if effective_private.is_dir():
        raw_hashes, chapter_hashes = _private_hashes(effective_private)
        for path in inspected:
            candidate_hashes = _candidate_hashes(repo, path)
            raw_matches: list[str] = []
            for digest in candidate_hashes:
                matches = raw_hashes.get(digest, [])
                if matches and _approved_synthetic_fixture(repo, path, digest):
                    approved_synthetic_matches += 1
                else:
                    raw_matches.extend(matches)
            raw_matches = sorted(set(raw_matches))
            chapter_matches = sorted({ref for digest in candidate_hashes for ref in chapter_hashes.get(digest, [])})
            reasons: list[str] = []
            matches: dict[str, list[str]] = {}
            if raw_matches:
                reasons.append("raw_novel_exact_content")
                matches["raw_private_refs"] = raw_matches
                counts["raw_novel_exact_content"] += 1
            if chapter_matches:
                reasons.append("structured_chapter_exact_content")
                matches["structured_private_refs"] = chapter_matches
                counts["structured_chapter_exact_content"] += 1
            if reasons:
                exact_findings.append({"path": path, "reasons": reasons, "matches": matches})
    findings.extend(exact_findings)
    return {
        "status": "PASS" if not findings else "FAIL",
        "tracked_or_staged_files_checked": len(inspected),
        "counts": counts,
        "findings": findings,
        "exact_content_leakage_protection": {
            "scope": ["01_原始小说", "02_结构化文本/*/text/*.txt"],
            "benchmark_private_scanned": False,
            "private_root_available": effective_private.is_dir(),
            "raw_source_hashes": len(raw_hashes),
            "structured_chapter_hashes": len(chapter_hashes),
            "matches": len(exact_findings),
            "approved_synthetic_fixture_matches": approved_synthetic_matches,
            "limitation": "Exact byte-for-byte SHA-256 matches only; modified or lightly rewritten leakage is not detected.",
        },
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="验证 Git 中没有私有小说资料或完整章节正文。")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--private-root", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        report = validate_repo(
            args.repo.resolve(),
            args.private_root.resolve() if args.private_root else None,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
