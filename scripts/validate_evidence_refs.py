#!/usr/bin/env python3
"""Validate EvidenceRef V1 objects against private structured chapters."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from novel_preprocessor.evidence import EvidenceValidationError, validate_evidence_payload  # noqa: E402


def _read_payload(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return json.loads(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="验证 chapter-relative EvidenceRef 的章节和引用 Hash。")
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    args = parser.parse_args()
    reports: list[dict[str, Any]] = []
    try:
        for path in args.inputs:
            results = validate_evidence_payload(_read_payload(path), args.private_root.resolve())
            reports.append({"input": str(path), "evidence_refs": results})
    except (OSError, json.JSONDecodeError, EvidenceValidationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "inputs": reports}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
