#!/usr/bin/env python3
"""Run all local STEP-01 engineering gates without network access."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(label: str, *arguments: str) -> None:
    print(f"\n=== {label} ===", flush=True)
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> int:
    run("Python compile", "-m", "compileall", "-q", "src", "scripts", "tests")
    run("Synthetic unit/integration tests", "-m", "unittest", "discover", "-s", "tests", "-v")
    run("Scene/Story Card schemas", "scripts/validate_card_schemas.py")
    run("Private/source leakage", "scripts/validate_private_boundaries.py")
    run("Skill structure", "scripts/validate_skill.py")
    print("\nSTEP-01 LOCAL VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
