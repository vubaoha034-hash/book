#!/usr/bin/env python3
"""Validate active Microcraft regression contracts after Phase344 calibration.

This validator checks schema-level expectations, privacy-safe benchmark structure,
and the calibrated layer split. It does NOT decide whether arbitrary manuscript
prose is semantically correct, natural, or high quality.

Historical dialogue-regression.v1.json is preserved as an audit artifact. Its
old MC-R002/MC-R003 mandatory hard labels are not treated as the current
promotion contract after Phase344 label calibration.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "benchmark/microcraft/dialogue-regression.v1.json"
CALIBRATION = ROOT / "benchmark/microcraft/label-calibration.v1.json"
ACTIVE = ROOT / "benchmark/microcraft/epistemic-pattern-regression.v1.json"

LEGACY_IDS = {"MC-R001", "MC-R002", "MC-R003"}
CALIBRATION_IDS = {"LC-R001", "LC-R002", "LC-R003", "LC-R004", "LC-R005", "LC-R006"}
ACTIVE_IDS = {f"EPD-R{i:03d}" for i in range(1, 11)}
VALID_EXPECTED = {"PASS", "FAIL", "HOLD", "RISK"}


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}


def privacy_check(data: dict, name: str, errors: list[str]) -> None:
    for key in ("copyrighted_source_text_included", "real_manuscript_text_included", "manuscript_text_included"):
        if key in data and data.get(key) is not False:
            errors.append(f"{name}: {key} must be false")


def case_map(data: dict, key: str, errors: list[str]) -> dict[str, dict]:
    cases = data.get(key)
    if not isinstance(cases, list) or not cases:
        errors.append(f"{key} must be a non-empty list")
        return {}
    result: dict[str, dict] = {}
    for case in cases:
        if not isinstance(case, dict):
            errors.append(f"{key}: every case must be an object")
            continue
        case_id = case.get("id") or case.get("legacy_id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{key}: case missing id")
            continue
        if case_id in result:
            errors.append(f"{key}: duplicate id {case_id}")
        result[case_id] = case
    return result


def main() -> int:
    errors: list[str] = []

    legacy = load_json(LEGACY, errors)
    calibration = load_json(CALIBRATION, errors)
    active = load_json(ACTIVE, errors)

    privacy_check(legacy, "legacy", errors)
    privacy_check(calibration, "calibration", errors)
    privacy_check(active, "active", errors)

    legacy_cases = case_map(legacy, "cases", errors)
    missing_legacy = sorted(LEGACY_IDS - set(legacy_cases))
    if missing_legacy:
        errors.append("legacy suite missing historical IDs: " + ", ".join(missing_legacy))

    calibration_cases = case_map(calibration, "calibrated_cases", errors)
    missing_calibration = sorted(CALIBRATION_IDS - set(calibration_cases))
    if missing_calibration:
        errors.append("calibration suite missing IDs: " + ", ".join(missing_calibration))

    legacy_reclass = case_map(calibration, "legacy_seed_reclassification", errors)
    for legacy_id in LEGACY_IDS:
        if legacy_id not in legacy_reclass:
            errors.append(f"calibration missing legacy reclassification {legacy_id}")

    r1 = legacy_reclass.get("MC-R001", {})
    if r1.get("calibrated_class") != "HARD_G6D_FAIL" or r1.get("status") != "PRESERVED":
        errors.append("MC-R001 must remain preserved HARD_G6D_FAIL")
    for legacy_id in ("MC-R002", "MC-R003"):
        if "SUPERSEDED" not in str(legacy_reclass.get(legacy_id, {}).get("status", "")):
            errors.append(f"{legacy_id} must be superseded as mandatory single-instance hard label")

    active_cases = case_map(active, "cases", errors)
    missing_active = sorted(ACTIVE_IDS - set(active_cases))
    if missing_active:
        errors.append("active suite missing IDs: " + ", ".join(missing_active))

    for case_id, case in active_cases.items():
        expected = case.get("expected")
        if expected not in VALID_EXPECTED:
            errors.append(f"{case_id}: invalid expected {expected!r}")
        if not case.get("rationale"):
            errors.append(f"{case_id}: rationale required")
        if expected in {"FAIL", "RISK"} and not case.get("expected_code"):
            errors.append(f"{case_id}: {expected} requires expected_code")
        if case.get("layer") not in {"G6D", "G8_STYLE_DENSITY"}:
            errors.append(f"{case_id}: invalid layer {case.get('layer')!r}")

    required_semantics = {
        "EPD-R001": ("G6D", "FAIL", "TEMPORAL_SEMANTIC_CHAIN_FAIL"),
        "EPD-R002": ("G6D", "PASS", None),
        "EPD-R004": ("G6D", "FAIL", "AUTHOR_INFORMATION_MOUTHPIECE_FAIL"),
        "EPD-R006": ("G6D", "PASS", None),
        "EPD-R008": ("G8_STYLE_DENSITY", "RISK", "DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK"),
        "EPD-R009": ("G8_STYLE_DENSITY", "PASS", None),
    }
    for case_id, (layer, expected, code) in required_semantics.items():
        case = active_cases.get(case_id, {})
        if case.get("layer") != layer or case.get("expected") != expected or case.get("expected_code") != code:
            errors.append(f"{case_id}: calibrated semantics mismatch")

    if active.get("universal_numeric_density_threshold", "MISSING") is not None:
        errors.append("active suite must not freeze a universal numeric density threshold")

    acceptance = active.get("acceptance", {})
    for key in (
        "MC_R001_equivalent_remains_hard",
        "object_fact_and_public_knowledge_must_be_distinguished",
        "pure_shared_background_still_fails",
        "single_context_supported_banter_not_hard_failed_for_removability_alone",
        "repeated_portable_family_routes_to_G8",
        "no_universal_numeric_density_threshold",
    ):
        if acceptance.get(key) is not True:
            errors.append(f"active acceptance.{key} must be true")

    if errors:
        print("Microcraft calibrated regression contract FAILED", file=sys.stderr)
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}", file=sys.stderr)
        return 1

    print(f"Microcraft calibrated regression contract PASSED ({len(active_cases)} active cases)")
    print("Legacy MC-R001/R002/R003 suite preserved as historical evidence; current promotion semantics come from calibration + active suite.")
    print("NOTE: schema validation is not semantic manuscript-quality validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
