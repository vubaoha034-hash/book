#!/usr/bin/env python3
"""Validate Novel Distillation Benchmark V1 contracts.

This script validates benchmark structure, score arithmetic, hard-gate presence,
upstream registry consistency, experiment template fields, and local/private
isolation patterns. It does NOT validate literary quality.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "benchmark/README.md",
    "benchmark/TEST_PLAN_V1.md",
    "benchmark/config/scoring.v1.json",
    "benchmark/config/upstreams.v1.json",
    "benchmark/templates/experiment-manifest.template.json",
]

REQUIRED_GATE_IDS = {f"B-G{i}" for i in range(8)}
REQUIRED_SCORE_IDS = {
    "source_evidence",
    "character_model",
    "plot_structure",
    "style_rhythm",
    "longform_consistency",
    "generalization_originality",
    "new_chapter_quality",
    "engineering_efficiency",
}
REQUIRED_IGNORE_PATTERNS = {
    "benchmark/_private/",
    "benchmark/runs/",
    "benchmark/cache/",
    "benchmark/upstream_checkouts/",
}
REQUIRED_TEMPLATE_TOP_KEYS = {
    "experiment_id",
    "status",
    "question",
    "baseline",
    "variant",
    "input_contract",
    "runtime_contract",
    "cache_contract",
    "evaluation",
    "results",
    "artifacts",
}


def load_json(relative: str, errors: list[str]) -> dict | None:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"Missing required JSON: {relative}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {relative}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{relative} must contain a JSON object")
        return None
    return value


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"Required file is empty: {relative}")


def validate_scoring(errors: list[str]) -> None:
    config = load_json("benchmark/config/scoring.v1.json", errors)
    if config is None:
        return

    if config.get("schema_version") != "1.0.0":
        errors.append("scoring.v1.json schema_version must be 1.0.0")
    if config.get("score_total") != 100:
        errors.append("score_total must equal 100")

    dimensions = config.get("dimensions")
    if not isinstance(dimensions, list):
        errors.append("dimensions must be a list")
    else:
        ids = set()
        weight_total = 0
        for item in dimensions:
            if not isinstance(item, dict):
                errors.append("every scoring dimension must be an object")
                continue
            dim_id = item.get("id")
            weight = item.get("weight")
            if dim_id:
                ids.add(dim_id)
            if not isinstance(weight, (int, float)) or weight <= 0:
                errors.append(f"invalid weight for dimension {dim_id!r}")
            else:
                weight_total += weight
        if ids != REQUIRED_SCORE_IDS:
            missing = sorted(REQUIRED_SCORE_IDS - ids)
            extra = sorted(ids - REQUIRED_SCORE_IDS)
            if missing:
                errors.append("missing scoring dimensions: " + ", ".join(missing))
            if extra:
                errors.append("unexpected scoring dimensions: " + ", ".join(extra))
        if weight_total != 100:
            errors.append(f"scoring dimension weights must sum to 100, got {weight_total}")

    gates = config.get("hard_gates")
    if not isinstance(gates, list):
        errors.append("hard_gates must be a list")
    else:
        gate_ids = {g.get("id") for g in gates if isinstance(g, dict)}
        if gate_ids != REQUIRED_GATE_IDS:
            missing = sorted(REQUIRED_GATE_IDS - gate_ids)
            extra = sorted(gate_ids - REQUIRED_GATE_IDS)
            if missing:
                errors.append("missing hard gates: " + ", ".join(missing))
            if extra:
                errors.append("unexpected hard gates: " + ", ".join(extra))
        for gate in gates:
            if not isinstance(gate, dict):
                errors.append("every hard gate must be an object")
                continue
            if not gate.get("name"):
                errors.append(f"hard gate {gate.get('id')} has no name")
            fail_if = gate.get("fail_if")
            if not isinstance(fail_if, list) or not fail_if:
                errors.append(f"hard gate {gate.get('id')} must define fail_if")

    rules = config.get("experiment_rules", {})
    if rules.get("max_major_variables_per_experiment") != 1:
        errors.append("benchmark must enforce one major variable per experiment")
    if rules.get("feature_count_has_zero_score") is not True:
        errors.append("feature count must have zero benchmark score")


def validate_upstreams(errors: list[str]) -> None:
    config = load_json("benchmark/config/upstreams.v1.json", errors)
    if config is None:
        return

    upstreams = config.get("upstreams")
    if not isinstance(upstreams, list) or not upstreams:
        errors.append("upstreams must be a non-empty list")
        return

    ids = set()
    for item in upstreams:
        if not isinstance(item, dict):
            errors.append("every upstream must be an object")
            continue
        upstream_id = item.get("id")
        if not upstream_id:
            errors.append("upstream missing id")
            continue
        if upstream_id in ids:
            errors.append(f"duplicate upstream id: {upstream_id}")
        ids.add(upstream_id)
        if not item.get("repo") or not item.get("url") or not item.get("role"):
            errors.append(f"upstream {upstream_id} missing repo/url/role")

    wave = config.get("baseline_wave_1")
    if not isinstance(wave, list) or not wave:
        errors.append("baseline_wave_1 must be a non-empty list")
    else:
        unknown = sorted(set(wave) - ids)
        if unknown:
            errors.append("baseline_wave_1 references unknown upstreams: " + ", ".join(unknown))

    policy = config.get("policy", {})
    if policy.get("license_review_before_code_reuse") is not True:
        errors.append("license review must be required before upstream code reuse")
    if policy.get("benchmark_unmodified_before_patch") is not True:
        errors.append("unmodified upstream baseline must be required")


def validate_template(errors: list[str]) -> None:
    template = load_json("benchmark/templates/experiment-manifest.template.json", errors)
    if template is None:
        return
    missing = sorted(REQUIRED_TEMPLATE_TOP_KEYS - set(template))
    if missing:
        errors.append("experiment template missing keys: " + ", ".join(missing))

    input_contract = template.get("input_contract", {})
    for key in (
        "source_hash_manifest",
        "style_holdout_partition_id",
        "future_holdout_partition_id",
    ):
        if key not in input_contract:
            errors.append(f"experiment input_contract missing {key}")

    runtime = template.get("runtime_contract", {})
    for key in ("model", "model_version_or_snapshot", "prompt_or_skill_version"):
        if key not in runtime:
            errors.append(f"experiment runtime_contract missing {key}")


def validate_gitignore(errors: list[str]) -> None:
    path = ROOT / ".gitignore"
    if not path.is_file():
        errors.append("Missing .gitignore")
        return
    lines = {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    missing = sorted(REQUIRED_IGNORE_PATTERNS - lines)
    if missing:
        errors.append(".gitignore missing private benchmark patterns: " + ", ".join(missing))


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_scoring(errors)
    validate_upstreams(errors)
    validate_template(errors)
    validate_gitignore(errors)

    if errors:
        print("Novel Distillation Benchmark V1 validation FAILED", file=sys.stderr)
        for index, error in enumerate(errors, start=1):
            print(f"{index}. {error}", file=sys.stderr)
        return 1

    print("Novel Distillation Benchmark V1 structure PASSED")
    print("NOTE: benchmark structure passing is not literary-quality evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
