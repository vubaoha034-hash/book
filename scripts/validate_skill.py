#!/usr/bin/env python3
"""Validate the Novel Writing Master repository structure.

Uses only the Python standard library so it can run locally and in GitHub Actions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "AGENTS.md",
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

REQUIRED_GATE_IDS = {f"G{i}" for i in range(8)}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"Missing required file: {relative}")
            continue
        if path.stat().st_size == 0:
            fail(errors, f"Required file is empty: {relative}")


def validate_skill_frontmatter(errors: list[str]) -> None:
    path = ROOT / "SKILL.md"
    if not path.is_file():
        return

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(errors, "SKILL.md must start with YAML frontmatter delimiter '---'.")
        return

    try:
        closing = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        fail(errors, "SKILL.md frontmatter has no closing '---' delimiter.")
        return

    frontmatter = "\n".join(lines[1:closing])
    if "name: novel-writing-master" not in frontmatter:
        fail(errors, "SKILL.md frontmatter must declare name: novel-writing-master")
    if "version: \"2.0.0\"" not in frontmatter:
        fail(errors, "SKILL.md frontmatter must declare metadata version 2.0.0")


def validate_quality_gates(errors: list[str]) -> None:
    path = ROOT / "config/novel-quality-gates.v2.json"
    if not path.is_file():
        return

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return

    if config.get("schema_version") != "2.0.0":
        fail(errors, "Quality gate schema_version must be 2.0.0")
    if config.get("skill") != "novel-writing-master":
        fail(errors, "Quality gate config has the wrong skill name")
    if config.get("pipeline") != "staged-independent-review":
        fail(errors, "Quality gate config has the wrong pipeline identifier")

    gates = config.get("gates")
    if not isinstance(gates, list):
        fail(errors, "Quality gate config must contain a gates list")
        return

    ids = {gate.get("id") for gate in gates if isinstance(gate, dict)}
    missing = sorted(REQUIRED_GATE_IDS - ids)
    if missing:
        fail(errors, f"Quality gate config is missing gate IDs: {', '.join(missing)}")

    for gate in gates:
        if not isinstance(gate, dict):
            fail(errors, "Every gate entry must be an object")
            continue
        gate_id = gate.get("id", "<unknown>")
        if not gate.get("name"):
            fail(errors, f"Gate {gate_id} has no name")
        if not gate.get("checks"):
            fail(errors, f"Gate {gate_id} has no checks")
        if not gate.get("on_fail"):
            fail(errors, f"Gate {gate_id} has no on_fail action")


def validate_cross_references(errors: list[str]) -> None:
    skill = ROOT / "SKILL.md"
    agents = ROOT / "AGENTS.md"
    if not skill.is_file() or not agents.is_file():
        return

    combined = skill.read_text(encoding="utf-8") + "\n" + agents.read_text(encoding="utf-8")
    for relative in REQUIRED_FILES:
        if relative in {"SKILL.md", "README.md", "AGENTS.md"}:
            continue
        if relative not in combined and relative.startswith(("modules/", "config/", "rules/pass", "rules/reader-trust", "workflows/06")):
            fail(errors, f"Core file is not referenced by SKILL.md or AGENTS.md: {relative}")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_skill_frontmatter(errors)
    validate_quality_gates(errors)
    validate_cross_references(errors)

    if errors:
        print("Novel Writing Master validation FAILED", file=sys.stderr)
        for index, error in enumerate(errors, start=1):
            print(f"{index}. {error}", file=sys.stderr)
        return 1

    print(f"Novel Writing Master validation PASSED ({len(REQUIRED_FILES)} required files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
