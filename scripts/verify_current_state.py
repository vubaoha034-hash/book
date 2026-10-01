"""Validate the current mainline, feedback binding and preserved rejections.

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
ROOT_LOCK_PATH = 'state/review_receipts/NOVEL_MAINLINE_V1_LOCK_20261001.json'
ROOT_LOCK_BLOB = 'efb0717bdf2faa9bbc67b89898cbe11059c39214'

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

def test_outcome(root: Path, relative: str) -> str:
    """Check evidence completeness; do not judge the prose or invent feedback."""
    result = load(root, relative)
    if result.get('schema_version') != 'novel-mainline-test/v1' or result.get('project_id') != 'novel-distillation':
        raise ValueError('INVALID_TEST_RECEIPT')
    artifact = result.get('artifact', {})
    data = safe_file(root, artifact.get('path', '')).read_bytes()
    if artifact.get('blob') != git_blob(data):
        raise ValueError('TEST_ARTIFACT_IDENTITY_DRIFT')
    human = result.get('human_feedback', {})
    facts = result.get('fact_check', {}).get('verdict')
    actual_human = human.get('source') == 'ACTUAL_USER_FEEDBACK' and bool(human.get('feedback', '').strip())
    wants, robotic = human.get('wants_to_continue'), human.get('robotic_or_tiring')
    if (wants is not None and type(wants) is not bool) or (robotic is not None and type(robotic) is not bool) or facts not in ('CLEAR', 'FAIL', 'PENDING'):
        raise ValueError('INVALID_TEST_OBSERVATION')
    if facts == 'FAIL' and not result.get('fact_check', {}).get('located_evidence'):
        raise ValueError('UNLOCATED_FACT_FAILURE')
    if facts == 'FAIL' or (actual_human and (wants is False or robotic is True)):
        expected = 'FAIL'
    elif actual_human and wants is True and robotic is False and facts == 'CLEAR':
        expected = 'PASS'
    else:
        expected = 'UNKNOWN'
    if result.get('outcome') != expected:
        raise ValueError('TEST_VERDICT_NOT_SUPPORTED: ' + relative)
    return expected

def verify_mainline(root: Path, project: dict, cp: dict) -> dict:
    state = project.get('mainline_state', {})
    if not state or state != cp.get('mainline_state'):
        raise ValueError('MAINLINE_STATE_DRIFT')
    chain = state.get('lock_chain', [])
    if not chain:
        raise ValueError('MISSING_MAINLINE_LOCK')
    previous, previous_lock = None, None
    for index, ref in enumerate(chain):
        data = safe_file(root, ref.get('path', '')).read_bytes()
        actual = git_blob(data)
        lock = json.loads(data)
        if actual != ref.get('blob') or lock.get('project_id') != project.get('project_id') or lock.get('revision') != index + 1:
            raise ValueError('LOCK_RECEIPT_IDENTITY_DRIFT')
        if index == 0:
            if ref.get('path') != ROOT_LOCK_PATH or actual != ROOT_LOCK_BLOB or lock.get('basis', {}).get('type') != 'USER_INITIAL_LOCK':
                raise ValueError('INITIAL_LOCK_REWRITTEN')
        else:
            basis = lock.get('basis', {})
            if lock.get('previous_lock_blob') != previous or not lock.get('changed_scope'):
                raise ValueError('UNBOUND_MAINLINE_REVISION')
            if basis.get('type') == 'RECORDED_FROZEN_TEST_FAILURE':
                evidence = safe_file(root, basis.get('evidence_path', '')).read_bytes()
                failed_test = json.loads(evidence)
                if (git_blob(evidence) != basis.get('evidence_blob') or test_outcome(root, basis['evidence_path']) != 'FAIL' or
                    failed_test.get('task_id') != previous_lock.get('task_id') or
                    failed_test.get('method_revision') != previous_lock.get('revision') or
                    failed_test.get('test_id') not in ('TEST_01', 'TEST_02')):
                    raise ValueError('REVISION_WITHOUT_FAILED_TEST')
            elif basis.get('type') == 'EXPLICIT_USER_SCOPE_CHANGE':
                if basis.get('source') != 'ACTUAL_USER_INSTRUCTION' or not basis.get('instruction', '').strip():
                    raise ValueError('REVISION_WITHOUT_USER_INSTRUCTION')
            else:
                raise ValueError('UNSUPPORTED_REVISION_BASIS')
        previous, previous_lock = actual, lock
    task_ref, plan_ref = state.get('contract', {}), state.get('plan', {})
    task_data = safe_file(root, task_ref.get('path', '')).read_bytes()
    plan_data = safe_file(root, plan_ref.get('path', '')).read_bytes()
    task = json.loads(task_data)
    if (task_ref.get('path') != lock.get('task', {}).get('path') or
        task_ref.get('blob') != lock['task'].get('blob') or task_ref['blob'] != git_blob(task_data) or
        hashlib.sha256(task_data).hexdigest() != lock['task'].get('sha256') or
        plan_ref != lock.get('plan') or hashlib.sha256(plan_data).hexdigest() != plan_ref.get('sha256')):
        raise ValueError('LOCKED_MAINLINE_CONTENT_CHANGED')
    task_id = task.get('task_id')
    if (not task_id or task_id != state.get('task_id') or task_id != lock.get('task_id') or
        task.get('revision') != state.get('revision') or task['revision'] != lock.get('revision') or
        task.get('project_id') != project.get('project_id') or
        project.get('active_task_ids') != cp.get('active_task_ids') or
        project.get('active_task_ids') != [task_id] or
        project.get('active_task_contract') != cp.get('active_task_contract') or
        project.get('active_task_contract') != task_ref['path'] or
        project.get('active_task', {}).get('task_id') != task_id or
        project.get('active_task', {}).get('contract') != task_ref['path'] or
        task_id in project.get('closed_task_ids', []) or task_id in cp.get('action_guard', {}).get('closed_task_ids', [])):
        raise ValueError('CURRENT_TASK_BINDING_DRIFT')
    steps = task.get('execution_order', [])
    matching = [i for i, row in enumerate(steps) if row.get('step_id') == state.get('current_step')]
    if len(matching) != 1:
        raise ValueError('INVALID_CURRENT_MAINLINE_STEP')
    index = matching[0]
    completed = state.get('completed_steps', [])
    if any(row['step_id'] not in completed for row in steps[:index]):
        raise ValueError('MAINLINE_STEP_SKIPPED')
    outcomes, frozen = {}, state.get('test_artifacts', {})
    for test_id, artifact in frozen.items():
        if test_id not in ('TEST_01', 'TEST_02') or not isinstance(artifact, dict):
            raise ValueError('INVALID_FROZEN_TEST_ARTIFACT')
        if git_blob(safe_file(root, artifact.get('path', '')).read_bytes()) != artifact.get('blob'):
            raise ValueError('FROZEN_TEST_ARTIFACT_CHANGED')
    for test_id, relative in state.get('test_results', {}).items():
        test = load(root, relative)
        if (test_id not in ('TEST_01', 'TEST_02') or test.get('test_id') != test_id or
            test.get('task_id') != task_id or test.get('method_revision') != state['revision']):
            raise ValueError('TEST_ID_BINDING_DRIFT')
        if test.get('artifact') != frozen.get(test_id):
            raise ValueError('TEST_RESULT_WITHOUT_FROZEN_ARTIFACT')
        outcomes[test_id] = test_outcome(root, relative)
    target_test = {2: 'TEST_01', 3: 'TEST_02'}.get(index)
    awaiting = target_test in frozen if target_test else False
    expected_action = steps[index].get('await_action') if awaiting else steps[index].get('action')
    if target_test and outcomes.get(target_test) == 'FAIL':
        # The locked change policy already requires a scoped revision after a
        # recorded failure. Do not keep asking for feedback already received.
        if 'RECORDED_FROZEN_TEST_FAILURE' not in task.get('change_policy', {}).get('allowed_revision_basis', []):
            raise ValueError('FAILED_TEST_WITHOUT_REVISION_POLICY')
        expected_action = 'DEFINE_ONE_SCOPED_METHOD_REVISION_AFTER_' + target_test + '_FAILURE'
    if project.get('next_action') != expected_action:
        raise ValueError('STALE_MAINLINE_NEXT_ACTION')
    if index >= 3 and outcomes.get('TEST_01') != 'PASS':
        raise ValueError('TEST_02_WITHOUT_TEST_01_PASS')
    if (index >= 4 or state.get('literary_quality_validated')) and outcomes.get('TEST_02') != 'PASS':
        raise ValueError('EXPANSION_WITHOUT_REPLICATION_PASS')
    if state.get('full_v5_authorized') is not False or task.get('preserved', {}).get('full_manuscript_v5_authorized') is not False:
        raise ValueError('AUTOMATIC_FULL_V5_PROMOTION')
    if state.get('new_prose_authorized_now') is not (index >= 2 and not awaiting):
        raise ValueError('PROSE_AUTHORIZATION_STEP_DRIFT')
    return {'task_id': task_id, 'revision': state['revision'], 'step': state['current_step'], 'outcomes': outcomes}

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
    mainline = verify_mainline(root, project, cp)
    current_receipt = load(root, project.get('human_verdict_receipt', ''))
    current_review = project.get('latest_human_review', {})
    current_artifact = safe_file(root, current_review.get('bound_artifact_path', ''))
    checks = {
        'same_project': project.get('project_id') == cp.get('project_id') == receipt.get('project_id') == 'novel-distillation',
        # The old V4 receipt describes V4, not the later opening trial.
        'same_current_status': bool(project.get('status')) and project.get('status') == cp.get('status'),
        'same_current_next': bool(project.get('next_required_action')) and project.get('next_required_action') == cp.get('next_required_action') == project.get('next_action') == cp.get('next_action'),
        'project_hash': cp.get('action_guard', {}).get('project_state_sha256') == hashlib.sha256(project_path.read_bytes()).hexdigest(),
        'v4_human_rejection_preserved': receipt.get('actual_human_style_verdict_20260929', {}).get('verdict') == 'FAIL_SEVERE_AI_SMELL',
        'current_human_ref': project.get('human_verdict_receipt') == cp.get('human_verdict_receipt') and current_receipt.get('project_id') == project.get('project_id'),
        'current_feedback_mirror': bool(current_review) and current_review == cp.get('latest_human_review') == current_receipt.get('review'),
        'current_feedback_artifact': current_review.get('bound_blob') == git_blob(current_artifact.read_bytes()),
        'current_feedback_present': bool(current_review.get('feedback_summary', '').strip()),
        'current_human_gate_mirror': project.get('current_human_gate') == cp.get('current_human_gate'),
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
        'preserved_research_checkpoint': project.get('accepted_checkpoint', {}).get('phase') == cp.get('highest_accepted_checkpoint') and project.get('accepted_checkpoint', {}).get('phase_ordinal') == cp.get('highest_accepted_phase_ordinal') == 320,
        'repair_basis_mirror': phase.get('repair_basis') == cp_phase.get('repair_basis'),
        'positive_scope_not_upgraded': project.get('phase363_prose_anchor', {}).get('mechanism_only_scale_proven_sufficient') is False and project.get('phase370_settlement', {}).get('ai_smell_direction_vs_phase369') == 'SAME',
    }
    for flag in ('same_v4_resubmission_allowed', 'automatic_v5_allowed', 'final_pass'):
        checks['preserve_' + flag] = phase.get(flag) is False and cp_phase.get(flag) is False
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise ValueError('CURRENT_STATE_DRIFT: ' + ', '.join(failed))
    return {'status': 'CURRENT_STATE_VALID_MAINLINE_LOCKED', 'sequence': cp.get('sequence'),
            'next_action': cp['next_required_action'], 'checks_passed': len(checks),
            'mainline': mainline, 'literary_quality_tested_by_this_script': False,
            'new_prose_authorized': project['mainline_state']['new_prose_authorized_now'],
            'lock_coverage': 'COOPERATING_PROJECT_ENTRYPOINTS_ONLY'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'CURRENT_STATE_BLOCKED', 'reason': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
