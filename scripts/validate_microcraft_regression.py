#!/usr/bin/env python3
"""Validate the Microcraft Dialogue Regression V1 contract.

This script validates IDs, schema-level expectations, and privacy-safe benchmark
structure. It does NOT decide whether arbitrary manuscript prose is semantically
correct, natural, or high quality. Those judgments require located text evidence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "benchmark/microcraft/dialogue-regression.v1.json"
REQUIRED = {"MC-R001", "MC-R002", "MC-R003"}
VALID_CLASSES = {"PASS", "FAIL", "HOLD"}
REQUIRED_FAILURES = {
    "MC-R001": "TEMPORAL_SEMANTIC_CHAIN_FAIL",
    "MC-R002": "AUTHOR_INFORMATION_MOUTHPIECE_FAIL",
    "MC-R003": "DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE",
}


def main() -> int:
    errors: list[str] = []
    if not SUITE.is_file():
        print(f"Missing suite: {SUITE.relative_to(ROOT)}", file=sys.stderr)
        return 1

    try:
        data = json.loads(SUITE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    if data.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if data.get("copyrighted_source_text_included") is not False:
        errors.append("copyrighted_source_text_included must be false")
    if data.get("manuscript_text_included") is not False:
        errors.append("manuscript_text_included must be false")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
        cases = []

    ids: list[str] = []
    by_id: dict[str, dict] = {}
    for case in cases:
        if not isinstance(case, dict):
            errors.append("every case must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("case missing id")
            continue
        ids.append(case_id)
        by_id[case_id] = case
        expected = case.get("expected")
        if expected not in VALID_CLASSES:
            errors.append(f"{case_id}: invalid expected class {expected!r}")
        if not case.get("rationale"):
            errors.append(f"{case_id}: rationale required")
        if expected == "FAIL" and not case.get("expected_code"):
            errors.append(f"{case_id}: FAIL case requires expected_code")

    if len(ids) != len(set(ids)):
        errors.append("duplicate case IDs are forbidden")

    missing = sorted(REQUIRED - set(ids))
    if missing:
        errors.append("missing mandatory regressions: " + ", ".join(missing))

    for case_id, code in REQUIRED_FAILURES.items():
        case = by_id.get(case_id)
        if not case:
            continue
        if case.get("expected") != "FAIL":
            errors.append(f"{case_id}: mandatory regression must expect FAIL")
        if case.get("expected_code") != code:
            errors.append(f"{case_id}: expected_code must be {code}")

    if errors:
        print("Microcraft regression contract FAILED", file=sys.stderr)
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}", file=sys.stderr)
        return 1

    print(f"Microcraft regression contract PASSED ({len(cases)} cases)")
    print("NOTE: schema validation is not semantic manuscript-quality validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
