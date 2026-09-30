"""Validate the current Phase422 artifact against its own recorded human verdict.

This validates identity, feedback scope, and state consistency, not literary quality.
It does not change any file or infer a positive human verdict.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

RECEIPT = 'state/review_receipts/PHASE422_RJ_OE408_I_FULL_MANUSCRIPT_PROSE_REAUTHORING_V4_V1.json'
EVENT = 'actual_human_opening_trial_verdict_20260930'

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def safe_file(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise ValueError('INVALID_ARTIFACT_PATH')
    root = root.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('MISSING_OR_OUTSIDE_ARTIFACT: ' + relative)
    return path

def load(root: Path, relative: str) -> dict:
    return json.loads(safe_file(root, relative).read_text(encoding='utf-8'))

def verify(root: Path) -> dict:
    root = root.resolve()
    project_path = safe_file(root, 'state/project_state.json')
    project = load(root, 'state/project_state.json')
    cp = load(root, 'state/continuity/LATEST_CHECKPOINT.json')
    receipt_path = safe_file(root, RECEIPT)
    receipt = load(root, RECEIPT)
    phase = project.get('phase422_state', {})
    cp_phase = cp.get('phase422_state', {})
    trial = phase.get('opening_trial', {})
    event = project.get(EVENT, {})
    artifact_path = safe_file(root, trial.get('path', ''))
    verdict = event.get('verdict', '')
    is_rejected = verdict.startswith(('FAIL', 'REJECT'))
    checks = {
        'same_project': project.get('project_id') == cp.get('project_id') == receipt.get('project_id') == 'novel-distillation',
        # The old V4 receipt describes V4, not the later opening trial.
        'same_current_status': bool(project.get('status')) and project.get('status') == cp.get('status'),
        'same_current_next': bool(project.get('next_required_action')) and project.get('next_required_action') == cp.get('next_required_action') == project.get('next_action') == cp.get('next_action'),
        'project_hash': cp.get('action_guard', {}).get('project_state_sha256') == hashlib.sha256(project_path.read_bytes()).hexdigest(),
        'v4_human_rejection_preserved': receipt.get('actual_human_style_verdict_20260929', {}).get('verdict') == 'FAIL_SEVERE_AI_SMELL',
        'v4_human_ref': project.get('human_verdict_receipt') == cp.get('human_verdict_receipt') == RECEIPT,
        'v4_receipt_blob': phase.get('receipt', {}).get('blob') == cp_phase.get('receipt', {}).get('blob') == git_blob(receipt_path.read_bytes()),
        'same_current_event': bool(event) and event == cp.get(EVENT),
        'actual_feedback_present': bool(event.get('human_exact_feedback', '').strip()),
        'same_trial': bool(trial) and trial == cp_phase.get('opening_trial'),
        'trial_identity': trial.get('path') == event.get('artifact') and trial.get('blob') == event.get('artifact_blob') == git_blob(artifact_path.read_bytes()),
        'trial_verdict_follows_own_event': trial.get('human_style_verdict') == verdict,
        'current_event_reference': trial.get('human_verdict_event_key') == EVENT,
        # This repair closes a rejected trial. A genuinely new candidate needs its
        # own task and feedback binding, not editing this rejection into a PASS.
        'current_trial_rejected': is_rejected,
        'no_automatic_promotion': event.get('final_quality_accepted') is False and event.get('automatic_full_v5_authorized') is False,
        'same_trial_not_resubmitted': event.get('same_trial_must_not_be_resubmitted') is True,
        'closed_human_gate': project.get('opening_trial_human_gate') == cp.get('opening_trial_human_gate') == 'CLOSED_HUMAN_REJECTED',
        'no_active_successor': cp.get('active_task_ids') == [],
        'repair_basis_mirror': phase.get('repair_basis') == cp_phase.get('repair_basis'),
        'positive_scope_not_upgraded': project.get('phase363_prose_anchor', {}).get('mechanism_only_scale_proven_sufficient') is False and project.get('phase370_settlement', {}).get('ai_smell_direction_vs_phase369') == 'SAME',
    }
    for flag in ('same_v4_resubmission_allowed', 'automatic_v5_allowed', 'final_pass'):
        checks['preserve_' + flag] = phase.get(flag) is False and cp_phase.get(flag) is False
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise ValueError('CURRENT_STATE_DRIFT: ' + ', '.join(failed))
    return {'status': 'CURRENT_STATE_VALID_CURRENT_TRIAL_REJECTED', 'sequence': cp.get('sequence'),
            'next_action': cp['next_required_action'], 'checks_passed': len(checks),
            'literary_quality_tested': False, 'new_prose_authorized': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'CURRENT_STATE_BLOCKED', 'reason': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
