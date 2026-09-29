"""Fail closed when the Phase422 human verdict and current project pointers drift."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def verify(root: Path) -> dict:
    project_path = root / "state/project_state.json"
    checkpoint_path = root / "state/continuity/LATEST_CHECKPOINT.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    receipt_rel = "state/review_receipts/PHASE422_RJ_OE408_I_FULL_MANUSCRIPT_PROSE_REAUTHORING_V4_V1.json"
    receipt_path = root / receipt_rel
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    expected_hash = hashlib.sha256(project_path.read_bytes()).hexdigest()
    trial = project["phase422_state"].get("opening_trial", {})
    trial_path = root / trial.get("path", "")
    checks = {
        "same_project": project["project_id"] == checkpoint["project_id"] == receipt["project_id"],
        "same_status": project["status"] == checkpoint["status"] == receipt["status"],
        "same_next": project["next_required_action"] == checkpoint["next_required_action"] == project["next_action"] == checkpoint["next_action"],
        "project_hash": checkpoint["action_guard"]["project_state_sha256"] == expected_hash,
        "verdict": receipt["actual_human_style_verdict_20260929"]["verdict"] == "FAIL_SEVERE_AI_SMELL",
        "human_ref": project["human_verdict_receipt"] == checkpoint["human_verdict_receipt"] == receipt_rel,
        "closed_v4": project["phase422_state"]["same_v4_resubmission_allowed"] is False and checkpoint["phase422_state"]["same_v4_resubmission_allowed"] is False,
        "no_auto_v5": project["phase422_state"]["automatic_v5_allowed"] is False and checkpoint["phase422_state"]["automatic_v5_allowed"] is False,
        "not_final": project["phase422_state"]["final_pass"] is False and checkpoint["phase422_state"]["final_pass"] is False,
        "receipt_blob": project["phase422_state"]["receipt"]["blob"] == checkpoint["phase422_state"]["receipt"]["blob"] == subprocess.check_output(["git", "hash-object", str(receipt_path)], text=True).strip(),
        "no_active_successor": checkpoint["active_task_ids"] == [],
        "positive_scope_not_upgraded": project["phase363_prose_anchor"]["mechanism_only_scale_proven_sufficient"] is False and project["phase370_settlement"]["ai_smell_direction_vs_phase369"] == "SAME",
        "repair_basis_mirror": project["phase422_state"].get("repair_basis") == checkpoint["phase422_state"].get("repair_basis"),
        "trial_mirror": trial == checkpoint["phase422_state"].get("opening_trial"),
        "trial_blob": trial_path.is_file() and trial.get("blob") == subprocess.check_output(["git", "hash-object", str(trial_path)], text=True).strip(),
        "trial_not_human_pass": trial.get("human_style_verdict") == "PENDING" and project.get("opening_trial_human_gate") == checkpoint.get("opening_trial_human_gate") == "PENDING_ACTUAL_HUMAN_READING",
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError("CURRENT_STATE_DRIFT: " + ", ".join(failed))
    return {"status": "CURRENT_STATE_VALID_HUMAN_V4_REJECTED", "sequence": checkpoint["sequence"], "next_action": checkpoint["next_required_action"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(verify(args.root), ensure_ascii=False))
