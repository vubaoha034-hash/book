from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PASS = "PASS"
REGRESSION = "STATE_REGRESSION_CONFLICT"
SOURCE_CONFLICT = "STATE_SOURCE_CONFLICT"
UNKNOWN = "UNKNOWN"


def _closed(active: dict) -> bool:
    status = str(active.get("status", "")).upper()
    return bool(active.get("completed_at")) or status in {"DONE", "ACCEPTED", "CLOSED", "CANCELLED", "SUPERSEDED"} or any(token in status for token in ("REJECTED", "CAMPAIGN_CLOSED", "CLOSED_MERGED"))


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
    if not isinstance(current_phase, int):
        return UNKNOWN, "accepted checkpoint phase ordinal missing or invalid"

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
        current_progress = checkpoint.get("progress_ordinal")
        if not isinstance(current_progress, int):
            return UNKNOWN, "accepted checkpoint progress ordinal missing or invalid for same-phase comparison"
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

    # Research acceptance is not the work queue. A closed phase may be newer
    # than the highest accepted research checkpoint and still cannot run again.
    if task_id in set(state.get("closed_task_ids") or []):
        if task_status in {"DONE", "ACCEPTED", "CLOSED", "SUPERSEDED"}:
            return PASS, "closed task record comparison only; idempotent no-op"
        return REGRESSION, f"task_id {task_id} is closed; re-dispatch forbidden"

    active = state.get("active_task")
    if isinstance(active, dict):
        if not task_id:
            return UNKNOWN, "current task identity required; phase rank alone cannot authorize execution"
        if task_id != active.get("task_id"):
            return SOURCE_CONFLICT, "candidate task is not the current native task"
        if phase_ordinal != active.get("phase_ordinal"):
            return SOURCE_CONFLICT, "candidate phase does not match the current task"
        if _closed(active):
            return REGRESSION, "current candidate is closed; prepare a scoped successor task instead of re-dispatch"

    return PASS, "forward or idempotent transition"


def require_current_action(root: Path, *, task_id: str, phase_ordinal: int,
                           action_id: str, parameters: dict | None = None) -> None:
    """Fail before a cooperating script reads payloads or changes files.

    The actual handler action and parameters must equal a request registered in
    the current native task. This is not a host-wide tool interception hook.
    """
    try:
        root = Path(root).resolve()
        state_raw = (root / "state/project_state.json").read_bytes()
        state = json.loads(state_raw)
        cp = load_state(root / "state/continuity/LATEST_CHECKPOINT.json")
        active = state.get("active_task", {})
        verdict, reason = validate_transition(state, phase_ordinal=phase_ordinal,
            progress_ordinal=None, task_id=task_id, task_status="RUNNING", rollback_authorized=False)
        if verdict != PASS:
            raise ValueError(verdict + ": " + reason)
        if _closed(active) or task_id in set(state.get("closed_task_ids") or []) or task_id in set(state.get("accepted_task_ids") or []):
            raise ValueError("CLOSED_TASK_DISPATCH")
        if cp.get("active_task_ids") != [task_id]:
            raise ValueError("CHECKPOINT_TASK_CONFLICT")
        binding = cp.get("action_guard", {})
        if binding.get("project_state_sha256") != hashlib.sha256(state_raw).hexdigest():
            raise ValueError("STALE_OR_UNBOUND_STATE")
        if binding.get("closed_task_ids") != state.get("closed_task_ids", []):
            raise ValueError("CLOSED_TASK_MIRROR_CONFLICT")
        if parameters is not None and not isinstance(parameters, dict):
            raise ValueError("ACTION_PARAMETERS_MUST_BE_OBJECT")
        request = {"action_id": action_id, "parameters": {} if parameters is None else parameters}
        canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        if not any(canonical(request) == canonical(allowed) for allowed in active.get("allowed_action_requests", [])):
            raise ValueError("ACTION_OR_PARAMETERS_NOT_AUTHORIZED")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit("PROJECT_ACTION_BLOCKED: " + str(exc)) from exc


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
