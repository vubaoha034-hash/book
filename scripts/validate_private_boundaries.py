#!/usr/bin/env python3
"""Fail if private/source/full-chapter material is tracked or staged."""

from __future__ import annotations

import argparse
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
    return reasons


def validate_repo(repo: Path) -> dict[str, object]:
    tracked = set(_git_paths(repo, ["ls-files", "-z"]))
    staged = set(_git_paths(repo, ["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]))
    inspected = sorted(tracked | staged)
    findings: list[dict[str, object]] = []
    counts = {"private": 0, "novel_source": 0, "full_chapter_text": 0}
    for path in inspected:
        reasons = classify_forbidden(path)
        if reasons:
            findings.append({"path": path, "reasons": sorted(reasons)})
            for reason in reasons:
                counts[reason] += 1
    return {
        "status": "PASS" if not findings else "FAIL",
        "tracked_or_staged_files_checked": len(inspected),
        "counts": counts,
        "findings": findings,
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="验证 Git 中没有私有小说资料或完整章节正文。")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        report = validate_repo(args.repo.resolve())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
