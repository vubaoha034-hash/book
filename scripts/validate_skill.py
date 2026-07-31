#!/usr/bin/env python3
"""Validate the Novel Writing Master repository structure and V3 contracts.

This script validates packaging, configuration, and cross-references. It cannot
validate whether a novel is logical, moving, satisfying, or free of AI-sounding
prose; those claims require located evidence from the actual manuscript.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V2_COMPAT_FILES = [
    "config/novel-quality-gates.v2.json",
    "rules/pass-isolation.md",
    "rules/reader-trust-and-economy.md",
    "rules/no-ai-smell.md",
    "rules/novel-logic-checklist.md",
    "rules/suspense-reversal-payoff.md",
    "rules/reader-reward-rhythm.md",
    "modules/developmental-editor.md",
    "modules/opening-retention-reader.md",
    "modules/beta-reader-panel.md",
    "modules/continuity-editor.md",
    "modules/character-pressure-test.md",
    "modules/line-editor-deslop.md",
    "workflows/05-deep-story-dissection.md",
    "workflows/06-novel-master-pipeline.md",
    "templates/novel-quality-gate-template.md",
    "templates/story-contract-template.md",
    "templates/revision-ledger-template.md",
]

V3_REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "config/novel-quality-gates.v3.json",
    "rules/pass-isolation.md",
    "rules/reader-trust-and-economy.md",
    "rules/no-ai-smell.md",
    "rules/novel-logic-checklist.md",
    "rules/reader-reward-rhythm.md",
    "modules/causal-proof-engine.md",
    "modules/emotion-payoff-ledger.md",
    "modules/hate-empathy-test.md",
    "modules/aesthetic-fingerprint.md",
    "modules/developmental-editor.md",
    "modules/opening-retention-reader.md",
    "modules/beta-reader-panel.md",
    "modules/continuity-editor.md",
    "modules/character-pressure-test.md",
    "modules/line-editor-deslop.md",
    "workflows/07-novel-master-pipeline-v3.md",
    "templates/v3-evidence-packet-template.md",
]

REQUIRED_GATE_IDS = {f"V3-G{i}" for i in range(9)}
FORBIDDEN_SUFFICIENCY = {
    "numeric_self_score",
    "all_files_exist",
    "all_boxes_checked",
    "multiple_same_context_personas_agree",
}


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_required_files(errors: list[str]) -> None:
    for relative in V2_COMPAT_FILES + V3_REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            add_error(errors, f"Missing required file: {relative}")
        elif path.stat().st_size == 0:
            add_error(errors, f"Required file is empty: {relative}")


def validate_skill_frontmatter(errors: list[str]) -> None:
    path = ROOT / "SKILL.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        add_error(errors, "SKILL.md must start with closed YAML frontmatter.")
        return
    frontmatter = match.group(1)
    keys = []
    for line in frontmatter.splitlines():
        if line and not line.startswith((" ", "\t")) and ":" in line:
            keys.append(line.split(":", 1)[0].strip())
    if keys != ["name", "description"]:
        add_error(errors, "SKILL.md frontmatter must contain only name and description.")
    if "name: novel-writing-master" not in frontmatter:
        add_error(errors, "SKILL.md must declare name: novel-writing-master")
    if "# Novel Writing Master V3" not in text:
        add_error(errors, "SKILL.md must identify V3 in its body.")


def load_v3(errors: list[str]) -> dict | None:
    path = ROOT / "config/novel-quality-gates.v3.json"
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_error(errors, f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(value, dict):
        add_error(errors, "V3 quality gate config must be an object.")
        return None
    return value


def validate_v3_config(errors: list[str]) -> None:
    config = load_v3(errors)
    if config is None:
        return
    expected = {
        "schema_version": "3.0.0",
        "skill": "novel-writing-master",
        "pipeline": "evidence-driven-staged-writing",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            add_error(errors, f"V3 config {key} must be {value!r}.")

    principles = config.get("principles")
    if not isinstance(principles, dict):
        add_error(errors, "V3 config must contain principles.")
    else:
        for key in (
            "causal_proof_before_draft",
            "emotion_debt_before_payoff",
            "located_evidence_required",
            "self_score_is_not_evidence",
            "simulated_readers_are_not_independent",
        ):
            if principles.get(key) is not True:
                add_error(errors, f"V3 principle {key} must be true.")
        limit = principles.get("max_high_impact_changes_per_pass")
        if not isinstance(limit, int) or not 1 <= limit <= 5:
            add_error(errors, "V3 revision pass must be limited to 1-5 issues.")

    gates = config.get("gates")
    if not isinstance(gates, list):
        add_error(errors, "V3 config must contain a gates list.")
        return
    ids = {gate.get("id") for gate in gates if isinstance(gate, dict)}
    missing = sorted(REQUIRED_GATE_IDS - ids)
    if missing:
        add_error(errors, f"V3 config is missing gates: {', '.join(missing)}")
    for gate in gates:
        if not isinstance(gate, dict):
            add_error(errors, "Every V3 gate must be an object.")
            continue
        gate_id = gate.get("id", "<unknown>")
        if not gate.get("name"):
            add_error(errors, f"Gate {gate_id} has no name.")
        evidence = gate.get("required_evidence") or gate.get(
            "required_evidence_per_key_scene"
        )
        if not evidence:
            add_error(errors, f"Gate {gate_id} has no required_evidence.")
        if not gate.get("on_fail") and gate_id != "V3-G8":
            add_error(errors, f"Gate {gate_id} has no on_fail action.")

    delivery = config.get("delivery")
    if not isinstance(delivery, dict):
        add_error(errors, "V3 config must contain delivery rules.")
    else:
        forbidden = set(delivery.get("never_accept_as_sufficient", []))
        missing_forbidden = sorted(FORBIDDEN_SUFFICIENCY - forbidden)
        if missing_forbidden:
            add_error(
                errors,
                "Delivery rules must reject false evidence: "
                + ", ".join(missing_forbidden),
            )


def validate_cross_references(errors: list[str]) -> None:
    entrypoints = []
    for relative in ("SKILL.md", "AGENTS.md", "README.md"):
        path = ROOT / relative
        if path.is_file():
            entrypoints.append(path.read_text(encoding="utf-8"))
    combined = "\n".join(entrypoints)
    for relative in V3_REQUIRED_FILES:
        if relative in {"SKILL.md", "AGENTS.md", "README.md"}:
            continue
        if relative.startswith(("config/", "modules/", "workflows/", "templates/")):
            if relative not in combined:
                add_error(errors, f"V3 core file is not discoverable: {relative}")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_skill_frontmatter(errors)
    validate_v3_config(errors)
    validate_cross_references(errors)

    if errors:
        print("Novel Writing Master V3 validation FAILED", file=sys.stderr)
        for index, error in enumerate(errors, start=1):
            print(f"{index}. {error}", file=sys.stderr)
        return 1

    checked = len(set(V2_COMPAT_FILES + V3_REQUIRED_FILES))
    print(f"Novel Writing Master V3 structure PASSED ({checked} files checked)")
    print("NOTE: structure validation is not manuscript quality validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
