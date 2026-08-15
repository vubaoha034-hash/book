from __future__ import annotations

import argparse
import json
from pathlib import Path


PASS = "PASS"
REGRESSION = "STATE_REGRESSION_CONFLICT"
SOURCE_CONFLICT = "STATE_SOURCE_CONFLICT"
UNKNOWN = "UNKNOWN"


def load_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_transition(
    state: dict,
    *,
    phase_ordinal: int | None,
    progress_ordinal: int | None,
    task_id: str | None,
    task_status: str | None,
    rollback_authorized: bool,
) -> tuple[str, str]:
    checkpoint = state.get("accepted_checkpoint")
    if not isinstance(checkpoint, dict):
        return UNKNOWN, "accepted_checkpoint missing"

    current_phase = checkpoint.get("phase_ordinal")
    current_progress = checkpoint.get("progress_ordinal")
    if not isinstance(current_phase, int) or not isinstance(current_progress, int):
        return UNKNOWN, "accepted checkpoint ordinals missing or invalid"

    rollback = state.get("rollback") or {}
    durable_rollback = rollback.get("authorized") is True and rollback.get("receipt")
    rollback_ok = rollback_authorized and bool(durable_rollback)

    if phase_ordinal is None:
        return UNKNOWN, "candidate phase unknown; preserve accepted checkpoint"

    if phase_ordinal < current_phase and not rollback_ok:
        return REGRESSION, (
            f"candidate phase {phase_ordinal} < accepted phase {current_phase}; "
            "explicit durable rollback receipt required"
        )

    if phase_ordinal == current_phase:
        if progress_ordinal is None:
            return UNKNOWN, "candidate progress unknown; preserve accepted checkpoint"
        if progress_ordinal < current_progress and not rollback_ok:
            return REGRESSION, (
                f"candidate progress {progress_ordinal} < accepted progress {current_progress}; "
                "explicit durable rollback receipt required"
            )

    accepted_task_ids = set(state.get("accepted_task_ids") or [])
    if task_id and task_id in accepted_task_ids:
        if task_status and task_status.upper() in {"PENDING", "RUNNING", "NOT_STARTED"}:
            return REGRESSION, f"task_id {task_id} is already accepted and cannot be re-dispatched"
        return PASS, f"task_id {task_id} already accepted; idempotent no-op"

    return PASS, "forward or idempotent transition"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reject stale/backward project-state transitions before dispatch or mutation."
    )
    parser.add_argument("--state", default="state/project_state.json")
    parser.add_argument("--phase-ordinal", type=int)
    parser.add_argument("--progress-ordinal", type=int)
    parser.add_argument("--task-id")
    parser.add_argument("--task-status")
    parser.add_argument("--rollback-authorized", action="store_true")
    args = parser.parse_args()

    state = load_state(Path(args.state))
    verdict, reason = validate_transition(
        state,
        phase_ordinal=args.phase_ordinal,
        progress_ordinal=args.progress_ordinal,
        task_id=args.task_id,
        task_status=args.task_status,
        rollback_authorized=args.rollback_authorized,
    )
    print(json.dumps({"verdict": verdict, "reason": reason}, ensure_ascii=False))
    return 0 if verdict == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
