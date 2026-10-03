"""Validate the current mainline, feedback binding and preserved rejections.

This validates identity, feedback scope, and state consistency, not literary quality.
It does not change any file or infer a positive human verdict.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

RECEIPT = 'state/review_receipts/PHASE422_RJ_OE408_I_FULL_MANUSCRIPT_PROSE_REAUTHORING_V4_V1.json'
EVENT = 'actual_human_opening_trial_verdict_20260930'
ROOT_LOCK_PATH = 'state/review_receipts/NOVEL_MAINLINE_V1_LOCK_20261001.json'
ROOT_LOCK_BLOB = 'efb0717bdf2faa9bbc67b89898cbe11059c39214'
EXTERNAL_REVIEW_LOCK_PATH = 'state/review_receipts/NOVEL_EXTERNAL_REVIEW_ROUTE_LOCK_20261001.json'
EXTERNAL_REVIEW_LOCK_BLOB = 'bc42595c43f12a7b8399fb97378ff54648c897d1'

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

def bound_json(root: Path, ref: dict) -> dict:
    data = safe_file(root, ref.get('path', '')).read_bytes()
    if ref.get('blob') != git_blob(data) or ref.get('sha256') != hashlib.sha256(data).hexdigest():
        raise ValueError('EXTERNAL_REVIEW_IDENTITY_DRIFT')
    return json.loads(data)

def external_review_action(root: Path, project: dict, cp: dict, target_test: str | None,
                          outcomes: dict, frozen: dict, base_action: str) -> str:
    """Route a located external diagnosis without inventing a human verdict.

    This permits preparation of a bounded revision. It cannot authorize prose,
    turn AI praise into a human pass, or promote a short excerpt to a full scene.
    """
    route = project.get('external_review_state')
    if route is None and cp.get('external_review_state') is None:
        return base_action
    if not route or route != cp.get('external_review_state'):
        raise ValueError('EXTERNAL_REVIEW_STATE_DRIFT')
    if route.get('active') is not True:
        return base_action
    lock_data = safe_file(root, EXTERNAL_REVIEW_LOCK_PATH).read_bytes()
    if git_blob(lock_data) != EXTERNAL_REVIEW_LOCK_BLOB:
        raise ValueError('EXTERNAL_REVIEW_LOCK_CHANGED')
    lock = json.loads(lock_data)
    task = bound_json(root, lock.get('task', {}))
    protocol_ref = lock.get('protocol', {})
    protocol = safe_file(root, protocol_ref.get('path', '')).read_bytes()
    if (git_blob(protocol) != protocol_ref.get('blob') or
        hashlib.sha256(protocol).hexdigest() != protocol_ref.get('sha256') or
        task.get('authority') != lock.get('basis') or
        lock.get('basis', {}).get('type') != 'EXPLICIT_USER_SCOPE_CHANGE' or
        lock.get('basis', {}).get('source') != 'ACTUAL_USER_INSTRUCTION' or
        not lock.get('basis', {}).get('instruction', '').strip()):
        raise ValueError('EXTERNAL_REVIEW_WITHOUT_BOUND_AUTHORITY')
    receipt = bound_json(root, route.get('receipt', {}))
    state = project.get('mainline_state', {})
    binding = receipt.get('mainline_binding', {})
    if (receipt.get('schema_version') != 'novel-external-review-receipt/v1' or
        receipt.get('project_id') != project.get('project_id') or
        receipt.get('task_id') != task.get('task_id') or
        receipt.get('protocol') != protocol_ref or
        binding.get('task_id') != state.get('task_id') or
        binding.get('method_revision') != state.get('revision') or
        binding.get('test_id') != target_test or
        binding.get('artifact') != frozen.get(target_test) or
        binding.get('validation_scope') != 'FIRST_SCREEN'):
        raise ValueError('EXTERNAL_REVIEW_TARGET_DRIFT')
    source = receipt.get('source', {})
    import re
    if (source.get('kind') != 'EXTERNAL_AI_CHAT' or source.get('actual_human') is not False or
        source.get('surface') != 'OPERA_NEON' or
        not re.fullmatch(r'https://chatgpt.com/c/[^/]+', source.get('conversation_url', '')) or
        receipt.get('standalone_quality_gate_allowed') is not False or
        receipt.get('human_quality_result') != 'UNKNOWN' or
        route.get('new_prose_authorized') is not False):
        raise ValueError('EXTERNAL_REVIEW_SCOPE_PROMOTION')
    proofs = receipt.get('dispatch_proofs', [])
    if (len(proofs) != 4 or len({p.get('task_id') for p in proofs}) != 4 or
        any(p.get('verdict') != 'OBSERVED_SINGLE_COMPLETE_NEW_MESSAGE' or
            p.get('conversation_url') != source['conversation_url'] or
            not re.fullmatch(r'[0-9a-f]{64}', p.get('message_sha256', '')) for p in proofs)):
        raise ValueError('EXTERNAL_REVIEW_DISPATCH_UNCONFIRMED')
    reports = receipt.get('reports', {})
    a, b, c, d = (bound_json(root, reports.get(key, {})) for key in ('A', 'B', 'C', 'D'))
    if (a.get('review_context') != 'FRESH_EXTERNAL_CHAT_FIRST_READ' or
        b.get('review_context') != 'SAME_EXTERNAL_REVIEWER_SECOND_STAGE' or
        c.get('review_context') != 'SAME_EXTERNAL_CHAT_UNSEEN_TEXT_TEST' or
        d.get('review_context') != 'SAME_EXTERNAL_REVIEWER_DIAGNOSTIC_STAGE'):
        raise ValueError('EXTERNAL_REVIEW_INDEPENDENCE_MISREPRESENTED')
    items = {item.get('sample_id'): item for item in a.get('items', [])}
    samples = {s.get('sample_id'): s.get('artifact', {}) for s in receipt.get('blind_samples', [])}
    if (len(samples) != 3 or set(samples) != set(items) or
        samples.get('S02') != binding.get('artifact') or
        b.get('target_sample_id') != 'S02' or
        c.get('technical_errata', {}).get('target_sample_id') != 'S02' or
        d.get('target_sample_id') != 'S02'):
        raise ValueError('EXTERNAL_REVIEW_SAMPLE_BINDING_DRIFT')
    for artifact in samples.values():
        if git_blob(safe_file(root, artifact.get('path', '')).read_bytes()) != artifact.get('blob'):
            raise ValueError('EXTERNAL_REVIEW_SAMPLE_BINDING_DRIFT')
    calibration = receipt.get('calibration', {}).get('initial', {})
    negatives = calibration.get('known_negatives', [])
    if len(negatives) != 2 or len({n.get('sample_id') for n in negatives}) != 2:
        raise ValueError('EXTERNAL_REVIEW_CALIBRATION_DRIFT')
    hits = 0
    for negative in negatives:
        human_ref = negative.get('human_receipt', {})
        human = bound_json(root, human_ref)
        if (test_outcome(root, human_ref['path']) != 'FAIL' or
            human.get('human_feedback', {}).get('source') != 'ACTUAL_USER_FEEDBACK' or
            human.get('artifact') != samples.get(negative.get('sample_id'))):
            raise ValueError('EXTERNAL_REVIEW_CALIBRATION_NOT_HUMAN_BOUND')
        item = items.get(negative.get('sample_id'))
        if not item:
            raise ValueError('EXTERNAL_REVIEW_CALIBRATION_DRIFT')
        hits += item.get('wants_to_continue') is False or item.get('robotic_or_tiring') is True
    if (calibration.get('hits') != hits or calibration.get('count') != len(negatives) or
        b.get('calibration', {}).get('known_negative_rejection_hits') != hits or
        b.get('calibration', {}).get('known_negative_count') != len(negatives)):
        raise ValueError('EXTERNAL_REVIEW_CALIBRATION_DRIFT')
    retest = receipt.get('calibration', {}).get('unseen_retest', {})
    original = safe_file(root, retest.get('source_artifact', {}).get('path', '')).read_bytes()
    excerpt_ref = retest.get('excerpt', {})
    excerpt = safe_file(root, excerpt_ref.get('path', '')).read_bytes()
    original_text = original.decode('utf-8')
    if (git_blob(original) != retest.get('source_artifact', {}).get('blob') or
        git_blob(excerpt) != excerpt_ref.get('blob') or
        hashlib.sha256(excerpt).hexdigest() != excerpt_ref.get('sha256') or
        excerpt.decode('utf-8') != original_text[retest.get('start_character'):retest.get('end_character_exclusive')]):
        raise ValueError('EXTERNAL_REVIEW_RETEST_SOURCE_DRIFT')
    retest_human_ref = retest.get('human_receipt', {})
    retest_human = bound_json(root, retest_human_ref)
    if (test_outcome(root, retest_human_ref['path']) != 'FAIL' or
        retest_human.get('artifact') != retest.get('source_artifact') or
        retest_human.get('human_feedback', {}).get('source') != 'ACTUAL_USER_FEEDBACK'):
        raise ValueError('EXTERNAL_REVIEW_CALIBRATION_NOT_HUMAN_BOUND')
    unseen = c.get('unseen_review', {})
    retest_hits = int(unseen.get('wants_to_continue') is False or unseen.get('robotic_or_tiring') is True)
    if retest.get('hits') != retest_hits or retest.get('count') != 1:
        raise ValueError('EXTERNAL_REVIEW_CALIBRATION_DRIFT')
    admission = d.get('calibration_admission', {})
    if (d.get('role') != 'EVIDENCE_AUDITOR' or
        d.get('automatic_literary_quality_certification') is not False or
        receipt.get('reviewer_role') != 'EVIDENCE_AUDITOR' or
        admission.get('initial_hits') != hits or admission.get('initial_count') != len(negatives) or
        admission.get('unseen_retest_hits') != retest_hits or admission.get('unseen_retest_count') != 1 or
        admission.get('user_taste_alignment') != 'NOT_VALIDATED'):
        raise ValueError('EXTERNAL_REVIEW_SCOPE_PROMOTION')
    verdict = b.get('current_editorial_verdict')
    if verdict != receipt.get('editorial_verdict') or verdict not in (
            'EXTERNAL_PASS_PROVISIONAL', 'REVISE', 'BLOCKED', 'INSUFFICIENT'):
        raise ValueError('EXTERNAL_REVIEW_VERDICT_DRIFT')
    corrections = c.get('technical_errata', {}).get('root_cause_corrections', [])
    roots = b.get('root_causes', [])
    text = safe_file(root, binding['artifact']['path']).read_text(encoding='utf-8')
    if (not roots or len(roots) > 3 or len(corrections) != len(roots) or
        len({r.get('id') for r in corrections}) != len(corrections) or
        {r.get('id') for r in roots} != {r.get('id') for r in corrections}):
        raise ValueError('EXTERNAL_REVIEW_UNLOCATED_DIAGNOSIS')
    for correction in corrections:
        if (correction.get('severity') not in ('P0', 'P1', 'P2') or
            not correction.get('quote') or correction['quote'] not in text):
            raise ValueError('EXTERNAL_REVIEW_UNLOCATED_DIAGNOSIS')
    priority = d.get('priority_issue', {})
    if (priority.get('id') not in {r.get('id') for r in roots} or
        not priority.get('quote') or priority['quote'] not in text or
        not priority.get('retest_condition') or
        priority != receipt.get('priority_issue') or
        d.get('verdict') != receipt.get('active_evidence_verdict') or
        d.get('verdict') not in ('REVISE', 'BLOCKED', 'NO_LOCATED_BLOCKERS', 'INSUFFICIENT')):
        raise ValueError('EXTERNAL_REVIEW_UNLOCATED_DIAGNOSIS')
    # A user's verdict always wins. A reviewer's positive label, especially after
    # failed calibration, cannot open any human or full-manuscript gate.
    if outcomes.get(target_test) in ('FAIL', 'PASS'):
        expected = base_action
    elif verdict in ('REVISE', 'BLOCKED'):
        expected = 'DEFINE_ONE_SCOPED_METHOD_REVISION_FROM_EXTERNAL_REVIEW'
    elif verdict == 'INSUFFICIENT':
        expected = 'RESOLVE_LOCATED_EXTERNAL_REVIEW_EVIDENCE_GAP'
    else:
        expected = 'REPAIR_EXTERNAL_REVIEW_BEFORE_PROSE_RELEASE'
    if receipt.get('next_action') != expected or route.get('next_action') != expected:
        raise ValueError('EXTERNAL_REVIEW_NEXT_ACTION_DRIFT')
    return scoped_revision_preparation_action(root, project, route, frozen, target_test, expected)

def scoped_revision_preparation_action(root: Path, project: dict, route: dict,
                                      frozen: dict, target_test: str | None, expected: str) -> str:
    """Follow a frozen input-preparation task without opening prose or human gates."""
    preparation = route.get('scoped_revision_preparation')
    if preparation is None:
        return expected
    if expected != 'DEFINE_ONE_SCOPED_METHOD_REVISION_FROM_EXTERNAL_REVIEW':
        # A human rejection or reviewer repair supersedes pending preparation.
        # Do not let the lower-priority scoped branch veto that action.
        return expected
    lock = bound_json(root, preparation.get('lock', {}))
    task = bound_json(root, preparation.get('task', {}))
    packet = safe_file(root, task.get('writer_packet', {}).get('path', '')).read_bytes()
    plan = safe_file(root, task.get('plan', {}).get('path', '')).read_bytes()
    artifact = frozen.get(target_test)
    original = safe_file(root, artifact.get('path', '')).read_text(encoding='utf-8')
    prefix_end = original.index('“我三点就得走')
    if (lock.get('schema_version') != 'novel-scoped-revision-preparation-lock/v1' or
        task.get('schema_version') != 'novel-scoped-revision-preparation/v1' or
        lock.get('project_id') != project.get('project_id') or task.get('project_id') != project.get('project_id') or
        lock.get('task_id') != task.get('task_id') or task.get('task_id') != preparation.get('task_id') or
        lock.get('task') != preparation.get('task') or lock.get('basis') != route.get('receipt') or
        task.get('basis') != route.get('receipt') or lock.get('authority_route_lock') != route.get('route_lock') or
        task.get('base_method_revision') != project['mainline_state']['revision'] or
        task.get('mainline_task_id') != project['mainline_state']['task_id'] or
        task.get('base_artifact') != artifact or lock.get('base_artifact') != artifact):
        raise ValueError('SCOPED_PREPARATION_BINDING_DRIFT')
    if (lock.get('writer_packet') != task.get('writer_packet') or lock.get('plan') != task.get('plan') or
        task['writer_packet'].get('blob') != git_blob(packet) or
        task['writer_packet'].get('sha256') != hashlib.sha256(packet).hexdigest() or
        task['plan'].get('blob') != git_blob(plan) or task['plan'].get('sha256') != hashlib.sha256(plan).hexdigest() or
        task.get('protected_prefix_characters') != prefix_end or
        task.get('protected_prefix_sha256') != hashlib.sha256(original[:prefix_end].encode()).hexdigest() or
        original not in packet.decode('utf-8')):
        raise ValueError('SCOPED_PREPARATION_CONTENT_DRIFT')
    if (task.get('new_prose_authorized_now') is not False or lock.get('new_prose_authorized') is not False or
        preparation.get('new_prose_authorized') is not False or task.get('generation_count') != 0 or
        task.get('used_prose_revision_rounds') != 0 or task.get('max_output_count') != 1 or
        task.get('max_consecutive_prose_revision_rounds') != 2 or
        task.get('writer_fresh_context_required') is not True or task.get('diagnostic_context_may_write') is not False or
        task.get('writer_read_allowlist') != [task['writer_packet']['path']] or
        task.get('human_result') != 'UNKNOWN' or task.get('full_scene_authorized') is not False or
        task.get('full_v5_authorized') is not False):
        raise ValueError('SCOPED_PREPARATION_SCOPE_PROMOTION')
    if task.get('correction_basis') is not None:
        correction = bound_json(root, task['correction_basis'])
        predecessor = bound_json(root, task.get('supersedes_preparation', {}))
        report = correction.get('report', {})
        predecessor_packet = safe_file(root, predecessor['writer_packet']['path']).read_text(encoding='utf-8')
        callback_id = correction.get('callback_id')
        if (lock.get('correction_basis') != task['correction_basis'] or
            preparation.get('correction_basis') != task['correction_basis'] or
            correction.get('schema_version') != 'novel-scoped-preparation-review-receipt/v1' or
            correction.get('callback_received') is not True or correction.get('processed_once') is not True or
            callback_id != predecessor.get('review_callback_id') or
            route.get('processed_preparation_callback_ids', []).count(callback_id) != 1 or
            report.get('verdict') != 'REVISE' or report.get('target_task_id') != predecessor.get('task_id') or
            report.get('writer_packet_blob') != predecessor['writer_packet']['blob'] or
            not report.get('issues') or
            not all(issue.get('quote') and issue['quote'] in predecessor_packet for issue in report['issues'])):
            raise ValueError('SCOPED_PREPARATION_CORRECTION_PROVENANCE_DRIFT')
    action = 'AWAIT_EXTERNAL_REVIEW_OF_RC3_REVISION_PREPARATION'
    if (task.get('current_action') != action or preparation.get('next_action') != action or
        preparation.get('status') != 'FROZEN_AWAITING_EXTERNAL_INPUT_REVIEW' or
        preparation.get('review_task_id') != task.get('review_task_id') or
        preparation.get('review_callback_id') != task.get('review_callback_id')):
        raise ValueError('SCOPED_PREPARATION_NEXT_ACTION_DRIFT')
    execution = route.get('scoped_revision_execution')
    if execution is None:
        return action
    return scoped_local_execution_action(root, project, route, preparation, execution, original)

def scoped_local_execution_action(root: Path, project: dict, route: dict,
                                  preparation: dict, execution: dict, original: str) -> str:
    if execution.get('status') == 'FROZEN_HUMAN_REJECTED_AWAITING_EMOTION_RETENTION_DIAGNOSIS':
        return scoped_human_rejection_action(root, project, route, preparation, execution, original)
    task = bound_json(root, execution.get('task', {}))
    lock = bound_json(root, execution.get('lock', {}))
    review = bound_json(root, task.get('input_review', {}))
    report = review.get('report', {})
    revision_round = task.get('prose_revision_round')
    approved_ref, preparation_lock_ref = preparation.get('task'), preparation.get('lock')
    packet_ref, preparation_id = preparation.get('writer_packet'), preparation.get('task_id')
    if revision_round == 2:
        repair = bound_json(root, task.get('approved_preparation', {}))
        repair_lock = bound_json(root, task.get('preparation_lock', {}))
        previous = bound_json(root, task.get('previous_execution', {}))
        previous_result = bound_json(root, task.get('previous_writer_result', {}))
        history = [row for row in route.get('scoped_revision_execution_history', [])
                   if row.get('task') == task.get('previous_execution')]
        if (repair.get('schema_version') != 'novel-writer-output-contract-repair-preparation/v1' or
            repair_lock.get('task') != task.get('approved_preparation') or
            repair.get('failure_result') != task.get('previous_writer_result') or
            previous.get('prose_revision_round') != 1 or previous_result.get('task_id') != previous.get('task_id') or
            previous_result.get('technical_verdict') != 'FAIL_OUTPUT_CONTRACT' or
            repair.get('remaining_prose_revision_rounds') != 1 or repair.get('used_prose_revision_rounds') != 1 or
            lock.get('previous_execution') != task.get('previous_execution') or
            lock.get('previous_writer_result') != task.get('previous_writer_result') or
            len(history) != 1 or history[0].get('used_prose_revision_rounds') != 1 or
            history[0].get('status') != 'BOUNDARY_FAILED_AWAITING_INPUT_REVIEW'):
            raise ValueError('SCOPED_LAST_ROUND_WITHOUT_BOUND_PARENT_FAILURE')
        approved_ref, preparation_lock_ref = task['approved_preparation'], task['preparation_lock']
        packet_ref, preparation_id = repair['writer_packet'], repair['task_id']
    packet_bytes = safe_file(root, task['writer_packet']['path']).read_bytes()
    if (task.get('schema_version') != 'novel-scoped-local-revision-execution/v1' or
        lock.get('schema_version') != 'novel-scoped-local-revision-execution-lock/v1' or
        task.get('project_id') != project.get('project_id') or lock.get('project_id') != project.get('project_id') or
        task.get('task_id') != execution.get('task_id') or lock.get('task_id') != task.get('task_id') or
        lock.get('task') != execution.get('task') or task.get('approved_preparation') != approved_ref or
        task.get('preparation_lock') != preparation_lock_ref or
        task.get('writer_packet') != packet_ref or execution.get('writer_packet') != packet_ref or
        task['writer_packet'].get('blob') != git_blob(packet_bytes) or
        task['writer_packet'].get('sha256') != hashlib.sha256(packet_bytes).hexdigest() or
        lock.get('writer_packet') != task.get('writer_packet') or
        lock.get('input_review') != task.get('input_review') or execution.get('input_review') != task.get('input_review') or
        review.get('callback_received') is not True or review.get('processed_once') is not True or
        route.get('processed_preparation_callback_ids', []).count(review.get('callback_id')) != 1 or
        report.get('target_task_id') != preparation_id or
        report.get('writer_packet_blob') != task['writer_packet']['blob'] or
        report.get('verdict') != 'NO_LOCATED_BLOCKERS' or report.get('issues') != []):
        raise ValueError('SCOPED_LOCAL_EXECUTION_PROVENANCE_DRIFT')
    if (task.get('base_method_revision') != 4 or task.get('max_output_count') != 1 or
        task.get('writer_fresh_context_required') is not True or task.get('diagnostic_context_may_write') is not False or
        task.get('writer_read_allowlist') != [task['writer_packet']['path']] or
        task.get('max_writer_dispatches') != 1 or revision_round not in (1, 2) or
        task.get('max_consecutive_prose_revision_rounds') != 2 or
        task.get('full_scene_authorized') is not False or task.get('full_v5_authorized') is not False or
        task.get('human_result') != 'UNKNOWN' or execution.get('human_result') != 'UNKNOWN' or
        execution.get('literary_acceptance') is not False or execution.get('full_v5_authorized') is not False):
        raise ValueError('SCOPED_LOCAL_EXECUTION_SCOPE_PROMOTION')
    status = execution.get('status')
    actions = {'CLAIMED_READY_TO_DISPATCH': 'EXECUTE_ONE_FRESH_CONTEXT_RC3_LOCAL_REVISION',
               'DISPATCHED_AWAITING_WRITER_RESULT': 'AWAIT_ONE_FRESH_CONTEXT_RC3_LOCAL_REVISION_RESULT',
               'FROZEN_AWAITING_REVIEW_DISPATCH': 'SEND_ONE_FROZEN_RC3_LOCAL_REVISION_FOR_EXTERNAL_REVIEW',
               'FROZEN_AWAITING_EXTERNAL_REVIEW': 'AWAIT_EXTERNAL_REVIEW_OF_ONE_FROZEN_RC3_LOCAL_REVISION',
               'FROZEN_REVIEW_SETTLED_AWAITING_MILESTONE_READING': 'AWAIT_MILESTONE_HUMAN_READING_OF_FROZEN_RC3_SHORT_EXCERPT',
               'FROZEN_REVIEW_SETTLED_AWAITING_FRESH_QUALITY_REVIEW': 'AWAIT_FRESH_EXTERNAL_QUALITY_REVIEW_CALLBACK',
               'FROZEN_QUALITY_PASS_PENDING_FACT_RECHECK': 'AWAIT_FRESH_EXTERNAL_QUALITY_REVIEW_FACT_RECHECK_CALLBACK',
               'FROZEN_INTERNAL_REVIEW_PASS_AWAITING_FINAL_READING': 'AWAIT_LIU_FINAL_READING_OF_INTERNAL_REVIEW_PASSED_448_CHARACTER_EXCERPT',
               'BOUNDARY_FAILED_AWAITING_INPUT_REVIEW': 'AWAIT_EXTERNAL_REVIEW_OF_RC3_WRITER_OUTPUT_BOUNDARY_REPAIR'}
    if status not in actions or execution.get('next_action') != actions[status]:
        raise ValueError('SCOPED_LOCAL_EXECUTION_ACTION_DRIFT')
    frozen = status.startswith('FROZEN_')
    produced = frozen or status == 'BOUNDARY_FAILED_AWAITING_INPUT_REVIEW'
    if (execution.get('generation_count') != int(produced) or execution.get('used_prose_revision_rounds') != revision_round - 1 + int(produced) or
        execution.get('writer_attempt_count') != (0 if status == 'CLAIMED_READY_TO_DISPATCH' else 1) or
        execution.get('new_prose_authorized_now') is not (status == 'CLAIMED_READY_TO_DISPATCH')):
        raise ValueError('SCOPED_LOCAL_EXECUTION_COUNT_DRIFT')
    if frozen:
        output = execution.get('output', {})
        data = safe_file(root, output.get('path', '')).read_bytes()
        text = data.decode('utf-8')
        if (output.get('path') != task.get('output_path') or output.get('blob') != git_blob(data) or
            output.get('sha256') != hashlib.sha256(data).hexdigest() or not text.startswith(original[:197]) or
            not 300 <= len(''.join(text.split())) <= 500):
            raise ValueError('SCOPED_LOCAL_EXECUTION_OUTPUT_DRIFT')
    if status in ('FROZEN_REVIEW_SETTLED_AWAITING_MILESTONE_READING',
                  'FROZEN_REVIEW_SETTLED_AWAITING_FRESH_QUALITY_REVIEW',
                  'FROZEN_QUALITY_PASS_PENDING_FACT_RECHECK',
                  'FROZEN_INTERNAL_REVIEW_PASS_AWAITING_FINAL_READING'):
        settled = bound_json(root, execution.get('review_result', {}))
        dispatch = bound_json(root, execution.get('review_dispatch_evidence', {}))
        prose_report = settled.get('report', {})
        source = settled.get('source', {})
        retest = prose_report.get('rc3_retest', {})
        if (settled.get('schema_version') != 'novel-scoped-prose-review-receipt/v1' or
            settled.get('project_id') != project.get('project_id') or
            settled.get('callback_id') != execution.get('review_callback_id') or
            settled.get('parent_review_task_id') != execution.get('review_task_id') or
            settled.get('output') != execution.get('output') or
            settled.get('execution_task') != execution.get('task') or
            settled.get('output_freeze') != execution.get('output_freeze') or
            settled.get('dispatch_evidence') != execution.get('review_dispatch_evidence') or
            settled.get('callback_received') is not True or settled.get('processed_once') is not True or
            execution.get('callback_received') is not True or
            route.get('processed_prose_callback_ids', []).count(settled.get('callback_id')) != 1 or
            dispatch.get('review_task_id') != execution.get('review_task_id') or
            dispatch.get('expected_callback_id') != settled.get('callback_id') or
            dispatch.get('output') != execution.get('output') or
            dispatch.get('observed_new_user_message_count') != 1 or
            dispatch.get('send_click_count') != 1 or dispatch.get('complete_authored_body_verified') is not True or
            source.get('kind') != 'EXTERNAL_AI_CHAT' or source.get('actual_human') is not False or
            source.get('conversation_url') != dispatch.get('reviewer_conversation_url') or
            prose_report.get('schema_version') != 'novel-scoped-local-revision-review/v1' or
            prose_report.get('review_context') != 'SAME_EXTERNAL_REVIEWER_SCOPED_PROSE_RETEST' or
            prose_report.get('project_id') != project.get('project_id') or
            prose_report.get('target_task_id') != task.get('task_id') or
            prose_report.get('base_method_revision') != 4 or
            prose_report.get('output_blob') != execution['output']['blob'] or
            prose_report.get('verdict') != 'NO_LOCATED_BLOCKERS' or retest.get('status') != 'CLOSED_BY_LOCATED_TEXT'):
            raise ValueError('SCOPED_PROSE_REVIEW_BINDING_DRIFT')
        quotes = retest.get('before', []) + retest.get('after', [])
        quotes += [row.get('quote') for row in prose_report.get('protect', []) + prose_report.get('issues', [])]
        if (not retest.get('before') or not retest.get('after') or
            not retest.get('mechanism') or not retest.get('evidence_boundary') or
            any(not quote or quote not in text for quote in quotes)):
            raise ValueError('SCOPED_PROSE_REVIEW_UNLOCATED_EVIDENCE')
        if (settled.get('human_result') != 'UNKNOWN' or settled.get('literary_acceptance') is not False or
            settled.get('full_scene_authorized') is not False or settled.get('third_candidate_authorized') is not False or
            settled.get('remaining_prose_revision_rounds') != 0 or execution.get('remaining_prose_revision_rounds') != 0 or
            execution.get('rc3_external_evidence_status') != 'CLOSED_BY_LOCATED_TEXT' or
            settled.get('other_diagnostic_issues_closed') != []):
            raise ValueError('SCOPED_PROSE_REVIEW_SCOPE_PROMOTION')
        quality = route.get('fresh_external_quality_review')
        if quality:
            ready = status == 'FROZEN_INTERNAL_REVIEW_PASS_AWAITING_FINAL_READING'
            correction = bound_json(root, quality.get('route_correction', {}))
            if (correction.get('project_id') != project.get('project_id') or
                correction.get('source') != 'ACTUAL_USER_ROUTE_CORRECTION' or
                correction.get('output') != execution.get('output') or
                correction.get('fresh_quality_review_task_id') != quality.get('task_id') or
                correction.get('reviewer_conversation_url') != quality.get('conversation_url') or
                correction.get('launch_evidence', {}).get('frozen_output_exact') is not True or
                quality.get('output') != execution.get('output') or
                quality.get('conversation_url') == source.get('conversation_url') or
                quality.get('human_result') != 'UNKNOWN' or
                quality.get('internal_deliverability') != ('INTERNAL_REVIEW_PASS_READY_FOR_LIU_FINAL_READING' if ready else 'PENDING') or
                quality.get('direct_user_reading_authorized_now') is not ready or
                execution.get('final_user_reading_authorized_now') is not ready):
                raise ValueError('FRESH_QUALITY_REVIEW_ROUTE_DRIFT')
            if (status not in ('FROZEN_REVIEW_SETTLED_AWAITING_FRESH_QUALITY_REVIEW',
                               'FROZEN_QUALITY_PASS_PENDING_FACT_RECHECK',
                               'FROZEN_INTERNAL_REVIEW_PASS_AWAITING_FINAL_READING') or
                quality.get('next_action') != actions[status]):
                raise ValueError('FRESH_QUALITY_REVIEW_BYPASSED')
            if status == 'FROZEN_REVIEW_SETTLED_AWAITING_FRESH_QUALITY_REVIEW' and quality.get('callback_received') is not False:
                raise ValueError('FRESH_QUALITY_REVIEW_CALLBACK_STATE_DRIFT')
            if status in ('FROZEN_QUALITY_PASS_PENDING_FACT_RECHECK',
                          'FROZEN_INTERNAL_REVIEW_PASS_AWAITING_FINAL_READING'):
                quality_result = bound_json(root, quality.get('result', {}))
                if (quality.get('callback_received') is not True or
                    quality_result.get('callback_id') != quality.get('callback_id') or
                    route.get('processed_quality_callback_ids', []).count(quality.get('callback_id')) != 1 or
                    quality_result.get('review_task_id') != quality.get('task_id') or
                    quality_result.get('reviewer_conversation_url') != quality.get('conversation_url') or
                    quality_result.get('output') != execution.get('output') or
                    quality_result.get('processed_once') is not True or
                    quality_result.get('report', {}).get('verdict') != 'EXTERNAL_PASS_READY_FOR_FINAL_USER_READING' or
                    quality_result.get('internal_deliverability') != 'PENDING_REVIEW_FACT_RECHECK' or
                    not quality_result.get('unresolved_review_fact_errors') or
                    quality_result.get('human_result') != 'UNKNOWN' or
                    quality_result.get('literary_acceptance') is not False or
                    quality.get('fact_recheck', {}).get('callback_received') is not ready):
                    raise ValueError('FRESH_QUALITY_REVIEW_SETTLEMENT_DRIFT')
                if ready:
                    recheck_route = quality['fact_recheck']
                    recheck = bound_json(root, recheck_route.get('result', {}))
                    recheck_dispatch = bound_json(root, recheck_route.get('dispatch_evidence', {}))
                    if (recheck.get('schema_version') != 'novel-quality-fact-recheck-receipt/v1' or
                        recheck.get('project_id') != project.get('project_id') or
                        recheck.get('callback_id') != recheck_route.get('callback_id') or
                        route.get('processed_quality_fact_callback_ids', []).count(recheck.get('callback_id')) != 1 or
                        recheck.get('review_task_id') != recheck_route.get('task_id') or
                        recheck.get('parent_review_task_id') != quality.get('task_id') or
                        recheck.get('reviewer_conversation_url') != quality.get('conversation_url') or
                        recheck.get('output') != execution.get('output') or
                        recheck.get('original_quality_result') != quality.get('result') or
                        recheck.get('dispatch_evidence') != recheck_route.get('dispatch_evidence') or
                        recheck_dispatch.get('task_id') != recheck_route.get('task_id') or
                        recheck_dispatch.get('output') != execution.get('output') or
                        recheck_dispatch.get('send_click_count') != 1 or
                        recheck.get('processed_once') is not True or
                        recheck.get('report', {}).get('verdict') != 'EXTERNAL_PASS_READY_FOR_FINAL_USER_READING' or
                        recheck.get('coordinator_validation', {}).get('timing_erratum_resolved') is not True or
                        recheck.get('unresolved_blockers') != [] or
                        quality.get('unresolved_review_fact_errors') != [] or
                        recheck.get('human_result') != 'UNKNOWN' or recheck.get('literary_acceptance') is not False or
                        recheck.get('coordinator_prose_edits') != 0 or
                        recheck.get('internal_deliverability') != quality.get('internal_deliverability')):
                        raise ValueError('FRESH_QUALITY_FACT_RECHECK_RELEASE_DRIFT')
        elif status == 'FROZEN_REVIEW_SETTLED_AWAITING_FRESH_QUALITY_REVIEW':
            raise ValueError('FRESH_QUALITY_REVIEW_ROUTE_MISSING')
    if status == 'BOUNDARY_FAILED_AWAITING_INPUT_REVIEW':
        result = bound_json(root, execution.get('writer_result', {}))
        repair_route = execution.get('output_boundary_repair', {})
        repair = bound_json(root, repair_route.get('task', {}))
        repair_lock = bound_json(root, repair_route.get('lock', {}))
        raw_ref = execution.get('raw_writer_output', {})
        raw_bytes = safe_file(root, raw_ref.get('path', '')).read_bytes()
        raw = raw_bytes.decode('utf-8')
        repair_bytes = safe_file(root, repair['writer_packet']['path']).read_bytes()
        if (raw_ref.get('blob') != git_blob(raw_bytes) or raw_ref.get('sha256') != hashlib.sha256(raw_bytes).hexdigest() or
            result.get('technical_verdict') != 'FAIL_OUTPUT_CONTRACT' or result.get('raw_output') != raw_ref or
            result.get('task_id') != task.get('task_id') or result.get('coordinator_prose_edits') != 0 or
            result.get('human_result') != 'UNKNOWN' or result.get('rc3_closed') is not False or
            raw.startswith(original[:197]) or not raw.startswith('“我三点就得走') or
            len(''.join(raw.split())) != result['observations']['raw_characters_excluding_whitespace'] or
            len(''.join((original[:197]+raw).split())) <= 500 or
            repair.get('schema_version') != 'novel-writer-output-contract-repair-preparation/v1' or
            repair_lock.get('task') != repair_route.get('task') or repair.get('failure_result') != execution.get('writer_result') or
            repair.get('previous_approved_packet') != task.get('writer_packet') or
            repair_lock.get('writer_packet') != repair.get('writer_packet') or
            repair_route.get('writer_packet') != repair.get('writer_packet') or
            repair['writer_packet'].get('blob') != git_blob(repair_bytes) or
            repair['writer_packet'].get('sha256') != hashlib.sha256(repair_bytes).hexdigest() or
            repair.get('remaining_prose_revision_rounds') != 1 or execution.get('remaining_prose_revision_rounds') != 1 or
            repair.get('new_prose_authorized_now') is not False or repair_lock.get('new_prose_authorized') is not False):
            raise ValueError('SCOPED_LOCAL_BOUNDARY_FAILURE_DRIFT')
    return actions[status]

def scoped_human_rejection_action(root: Path, project: dict, route: dict,
                                 preparation: dict, execution: dict, original: str) -> str:
    """Preserve the verified AI stage while binding a later actual human FAIL."""
    human = route.get('actual_human_reading', {})
    receipt = bound_json(root, human.get('receipt', {}))
    prior = receipt.get('prior_stage_snapshot', {})
    prior_execution = prior.get('scoped_revision_execution', {})
    prior_quality = prior.get('fresh_external_quality_review', {})
    if prior_execution.get('status') != 'FROZEN_INTERNAL_REVIEW_PASS_AWAITING_FINAL_READING':
        raise ValueError('HUMAN_REJECTION_PRIOR_STAGE_DRIFT')
    historical_route = dict(route, scoped_revision_execution=prior_execution,
                            fresh_external_quality_review=prior_quality)
    scoped_local_execution_action(root, project, historical_route, preparation, prior_execution, original)
    review = receipt.get('review', {})
    preparation_route = route.get('emotion_retention_preparation', {})
    task = bound_json(root, preparation_route.get('task', {}))
    packet = safe_file(root, task.get('reviewer_packet', {}).get('path', '')).read_bytes()
    plan = safe_file(root, task.get('plan', {}).get('path', '')).read_bytes()
    quality = route.get('fresh_external_quality_review', {})
    action = 'RESTORE_OPERA_NEON_AND_SEND_ONE_R2_EMOTION_RETENTION_DIAGNOSIS_TASK'
    blocked_action = 'AWAIT_NEW_UNIFIED_COMMAND_AFTER_R2_DIAGNOSIS_PRE_SEND_COMPOSER_MISMATCH_NO_RETRY'
    # A newly bound human verdict supersedes only the live latest pointer.
    # This older failure must still be checked against its immutable receipt.
    historical_human_path = project.get('human_verdict_receipt')
    historical_human_review = project.get('latest_human_review')
    if project.get('emotion_pacing_learning'):
        prior_ref = project['emotion_pacing_learning'].get('previous_human_feedback', {})
        if prior_ref != human.get('receipt'):
            raise ValueError('SCOPED_HISTORICAL_HUMAN_REFERENCE_DRIFT')
        prior_human = bound_json(root, prior_ref)
        historical_human_path = prior_ref['path']
        historical_human_review = prior_human.get('review')
    if (receipt.get('schema_version') != 'novel-scoped-human-reading-receipt/v1' or
        receipt.get('project_id') != project.get('project_id') or receipt.get('outcome') != 'FAIL' or
        receipt.get('processed_once') is not True or human.get('outcome') != 'FAIL' or
        execution.get('human_verdict') != human.get('receipt') or
        historical_human_path != human.get('receipt', {}).get('path') or
        historical_human_review != review or
        review.get('source', {}).get('kind') != 'ACTUAL_CURRENT_USER_MESSAGE' or
        not review.get('human_exact_feedback') or review.get('human_quality_accepted') is not False or
        review.get('same_artifact_resubmission_allowed') is not False or
        review.get('bound_blob') != execution.get('output', {}).get('blob') or
        review.get('bound_artifact_path') != execution.get('output', {}).get('path') or
        receipt.get('output') != execution.get('output') or
        receipt.get('execution_task') != execution.get('task') or
        receipt.get('coordinator_prose_edits') != 0 or
        execution.get('human_result') != 'FAIL' or execution.get('literary_acceptance') is not False or
        execution.get('new_prose_authorized_now') is not False or
        execution.get('final_user_reading_authorized_now') is not False or
        execution.get('internal_deliverability') != 'REJECTED_BY_ACTUAL_HUMAN_READING' or
        execution.get('full_v5_authorized') is not False or
        any(execution.get(k) != prior_execution.get(k) for k in
            ('task', 'lock', 'writer_packet', 'output', 'output_freeze', 'review_result',
             'writer_attempt_count', 'generation_count', 'used_prose_revision_rounds', 'remaining_prose_revision_rounds')) or
        quality.get('human_result') != 'FAIL' or quality.get('direct_user_reading_authorized_now') is not False or
        quality.get('internal_deliverability') != 'REJECTED_BY_ACTUAL_HUMAN_READING' or
        quality.get('human_verdict') != human.get('receipt') or
        any(quality.get(k) != prior_quality.get(k) for k in
            ('task_id', 'conversation_url', 'output', 'result', 'fact_recheck', 'external_verdict'))):
        raise ValueError('SCOPED_ACTUAL_HUMAN_REJECTION_DRIFT')
    if (task.get('schema_version') != 'novel-scoped-diagnostic-preparation/v1' or
        task.get('project_id') != project.get('project_id') or
        task.get('task_id') != preparation_route.get('task_id') or
        task.get('basis') != human.get('receipt') or task.get('output') != execution.get('output') or
        task.get('plan') != preparation_route.get('plan') or
        task.get('reviewer_packet', {}).get('blob') != git_blob(packet) or
        task.get('reviewer_packet', {}).get('sha256') != hashlib.sha256(packet).hexdigest() or
        task.get('plan', {}).get('blob') != git_blob(plan) or
        task.get('plan', {}).get('sha256') != hashlib.sha256(plan).hexdigest() or
        task.get('required_surface') != 'CHAT' or task.get('required_thinking_effort') != 'EXTREME_HIGH' or
        task.get('send_click_count') != 0 or task.get('dispatch_attempt_count') != 0 or
        task.get('generation_count') != 0 or task.get('new_prose_authorized_now') is not False or
        task.get('old_RC3_budget_remaining') != 0 or task.get('old_task_not_reopened') is not True or
        task.get('full_scene_authorized') is not False or task.get('full_v5_authorized') is not False or
        task.get('callback_received') is not False or
        task.get('status') != 'PREPARED_DISPATCH_BLOCKED_OPERA_SESSION_TERMINATED' or
        execution.get('next_action') != action or quality.get('next_action') != action or
        task.get('next_action') != action):
        raise ValueError('HUMAN_FAIL_DIAGNOSTIC_PREPARATION_DRIFT')
    blocker_ref = preparation_route.get('dispatch_blocker')
    if blocker_ref:
        blocker = bound_json(root, blocker_ref)
        dispatch = blocker.get('dispatch_message', {})
        if (preparation_route.get('status') != 'DISPATCH_BLOCKED_PRE_SEND_EXACT_COMPOSER_MISMATCH_NO_SEND_NO_RETRY' or
            preparation_route.get('next_action') != blocked_action or
            preparation_route.get('callback_received') is not False or
            preparation_route.get('new_prose_authorized_now') is not False or
            preparation_route.get('external_review_started') is not False or
            preparation_route.get('reviewer_conversation_url') is not None or
            preparation_route.get('send_click_count') != 0 or
            preparation_route.get('composer_fill_count') != 1 or
            preparation_route.get('same_task_retry_allowed') is not False or
            blocker.get('schema_version') != 'novel-external-diagnosis-pre-send-blocker-receipt/v1' or
            blocker.get('project_id') != project.get('project_id') or
            blocker.get('task_id') != task.get('task_id') or
            blocker.get('callback_id') != task.get('callback_id') or
            blocker.get('prepared_task') != preparation_route.get('task') or
            blocker.get('reviewer_packet') != task.get('reviewer_packet') or
            blocker.get('review_target') != task.get('output') or
            blocker.get('outcome') != 'BLOCKED_PRE_SEND_EXACT_COMPOSER_MISMATCH' or
            blocker.get('external_review_started') is not False or
            blocker.get('callback_received') is not False or
            blocker.get('reviewer_conversation_url') is not None or
            blocker.get('retry_allowed_in_same_task') is not False or
            blocker.get('new_prose_authorized') is not False or
            dispatch.get('exact_match') is not False or
            dispatch.get('fill_count') != 1 or dispatch.get('send_click_count') != 0 or
            dispatch.get('dispatch_attempt_count') != 0 or
            dispatch.get('expected_sha256') == dispatch.get('composer_actual_sha256')):
            raise ValueError('HUMAN_FAIL_DIAGNOSTIC_PRE_SEND_BLOCKER_DRIFT')
        return blocked_action
    if (preparation_route.get('callback_received') is not False or
        preparation_route.get('status') != 'PREPARED_DISPATCH_BLOCKED_OPERA_SESSION_TERMINATED' or
        preparation_route.get('next_action') != action):
        raise ValueError('HUMAN_FAIL_DIAGNOSTIC_PREPARATION_ROUTE_DRIFT')
    return action

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
    learning_module, learning_authorization = None, None
    if 'emotion_pacing_learning' in project or 'emotion_pacing_learning' in cp:
        spec = importlib.util.spec_from_file_location('emotion_learning_state',
            Path(__file__).with_name('verify_emotion_learning.py'))
        learning_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(learning_module)
        # Validate actual current user feedback before selecting a historical
        # view for any older gate; never trust a successor-present boolean.
        learning_authorization = learning_module.validate_authorization(root, project, cp)
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
                    failed_test.get('test_id') not in ('TEST_01', 'TEST_01_FULL', 'TEST_02')):
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
    full_scene_stage = 'TEST_01_FULL' in task.get('tests', {})
    valid_tests = ('TEST_01', 'TEST_01_FULL', 'TEST_02') if full_scene_stage else ('TEST_01', 'TEST_02')
    for test_id, artifact in frozen.items():
        if test_id not in valid_tests or not isinstance(artifact, dict):
            raise ValueError('INVALID_FROZEN_TEST_ARTIFACT')
        if git_blob(safe_file(root, artifact.get('path', '')).read_bytes()) != artifact.get('blob'):
            raise ValueError('FROZEN_TEST_ARTIFACT_CHANGED')
    for test_id, relative in state.get('test_results', {}).items():
        test = load(root, relative)
        if (test_id not in valid_tests or test.get('test_id') != test_id or
            test.get('task_id') != task_id or test.get('method_revision') != state['revision']):
            raise ValueError('TEST_ID_BINDING_DRIFT')
        if test.get('artifact') != frozen.get(test_id):
            raise ValueError('TEST_RESULT_WITHOUT_FROZEN_ARTIFACT')
        scope = task.get('tests', {}).get(test_id, {}).get('validation_scope')
        if scope and test.get('validation_scope') != scope:
            raise ValueError('TEST_READING_SCOPE_DRIFT')
        outcomes[test_id] = test_outcome(root, relative)
    target_test = steps[index].get('test_id') if full_scene_stage else {2: 'TEST_01', 3: 'TEST_02'}.get(index)
    awaiting = target_test in frozen if target_test else False
    expected_action = steps[index].get('await_action') if awaiting else steps[index].get('action')
    if target_test and outcomes.get(target_test) == 'FAIL':
        # The locked change policy already requires a scoped revision after a
        # recorded failure. Do not keep asking for feedback already received.
        if 'RECORDED_FROZEN_TEST_FAILURE' not in task.get('change_policy', {}).get('allowed_revision_basis', []):
            raise ValueError('FAILED_TEST_WITHOUT_REVISION_POLICY')
        expected_action = 'DEFINE_ONE_SCOPED_METHOD_REVISION_AFTER_' + target_test + '_FAILURE'
    expected_action = external_review_action(root, project, cp, target_test,
        outcomes, frozen, expected_action)
    # The current explicit execution change follows all historical gates. It
    # cannot replace or bypass the prior human rejection / exhausted budget.
    if 'codex_review_integration' in project or 'codex_review_integration' in cp:
        spec = importlib.util.spec_from_file_location('codex_review_state',
            Path(__file__).with_name('verify_codex_review.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        expected_action = module.codex_review_action(root, project, cp, expected_action)
    successor_module, successor_authorization = None, None
    if 'r2_entry_short_trial' in project or 'r2_entry_short_trial' in cp:
        spec = importlib.util.spec_from_file_location('one_short_trial_state',
            Path(__file__).with_name('verify_one_short_trial.py'))
        successor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(successor_module)
        successor_authorization = successor_module.validate_authorization(root, project, cp)
    # A separate user authorization advances preparation only. It supplies no
    # prose budget and follows (rather than replaces) the completed review gate.
    if 'r2_reentry_fact_preparation' in project or 'r2_reentry_fact_preparation' in cp:
        spec = importlib.util.spec_from_file_location('reentry_preparation_state',
            Path(__file__).with_name('verify_reentry_preparation.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        expected_action = module.reentry_preparation_action(root, project, cp, expected_action,
            successor_authorization=successor_authorization)
    if successor_module is not None:
        expected_action = successor_module.one_short_trial_action(root, project, cp, expected_action,
            successor_authorization=learning_authorization)
    if learning_module is not None:
        expected_action = learning_module.learning_action(root, project, cp, expected_action)
    if project.get('next_action') != expected_action:
        raise ValueError('STALE_MAINLINE_NEXT_ACTION')
    if index >= 3 and outcomes.get('TEST_01') != 'PASS':
        raise ValueError('TEST_02_WITHOUT_TEST_01_PASS')
    if full_scene_stage and index >= 4 and outcomes.get('TEST_01_FULL') != 'PASS':
        raise ValueError('TEST_02_WITHOUT_FULL_SCENE_PASS')
    expansion_index = 5 if full_scene_stage else 4
    if (index >= expansion_index or state.get('literary_quality_validated')) and outcomes.get('TEST_02') != 'PASS':
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
