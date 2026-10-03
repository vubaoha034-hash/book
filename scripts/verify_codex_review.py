"""Additional scoped integration checks; historical gates still run first."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

TASK = 'NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01'
OLD_ACTION = 'AWAIT_NEW_UNIFIED_COMMAND_AFTER_R2_DIAGNOSIS_PRE_SEND_COMPOSER_MISMATCH_NO_RETRY'
NEXT_ACTION = 'AWAIT_LIU_AUTHORIZATION_OF_ONE_BOUNDED_R2_REENTRY_FACT_PREPARATION_TASK_NO_PROSE'
CHANGE = 'state/review_receipts/NOVEL_CODEX_REVIEW_EXECUTION_CHANGE_20261003.json'


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def bound_bytes(root, reference):
    path = (root / reference.get('path', '')).resolve()
    if not reference.get('path') or not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('CODEX_REVIEW_MISSING_MATERIAL')
    data = path.read_bytes()
    if reference.get('blob') != blob(data) or reference.get('sha256') != hashlib.sha256(data).hexdigest():
        raise ValueError('CODEX_REVIEW_IDENTITY_DRIFT')
    return data


def load_bound(root, reference):
    return json.loads(bound_bytes(root, reference))


def review_module(root):
    spec = importlib.util.spec_from_file_location('codex_review_packet_checks', root / 'scripts/codex_review.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def codex_review_action(root, project, checkpoint, historical_action):
    route = project.get('codex_review_integration')
    if route is None and checkpoint.get('codex_review_integration') is None:
        return historical_action
    if not route or route != checkpoint.get('codex_review_integration'):
        raise ValueError('CODEX_REVIEW_STATE_DRIFT')
    if historical_action != OLD_ACTION:
        raise ValueError('CODEX_REVIEW_CANNOT_SKIP_HISTORICAL_GATES')
    change = load_bound(root, route['execution_change'])
    receipt = load_bound(root, route['result'])
    task = load_bound(root, route['task'])
    proposal = load_bound(root, route['next_task_proposal'])
    manifest = load_bound(root, route['manifest'])
    if (change.get('task_id') != TASK or change.get('authority', {}).get('source') != 'ACTUAL_CURRENT_USER_INSTRUCTION' or
            change.get('scope') != 'EXECUTION_ROUTE_AND_REVIEW_INTAKE_ONLY_NO_STORY_OR_METHOD_CHANGE' or
            change.get('preserved', {}).get('new_prose_authorized') is not False or
            change.get('preserved', {}).get('old_RC3_remaining_rounds') != 0 or
            change.get('preserved', {}).get('old_197_character_protection_released') is not False or
            receipt.get('task_id') != TASK or task.get('task_id') != TASK or manifest.get('task_id') != TASK or
            task.get('status') != 'COMPLETE_REVIEW_INTEGRATION_AND_DIAGNOSIS_NO_PROSE' or
            receipt.get('outcome') != 'COMPLETE_REVIEW_INTEGRATION_AND_DIAGNOSIS_NO_PROSE' or
            task.get('generation_count') != 0 or receipt.get('generation_count') != 0 or
            route.get('new_prose_authorized_now') is not False or
            receipt.get('new_prose_authorized') is not False or task.get('new_prose_authorized') is not False or
            receipt.get('full_v5_authorized') is not False or receipt.get('old_RC3_remaining_rounds') != 0 or
            receipt.get('old_197_character_protection_released') is not False or
            receipt.get('prior_browser_callback_received') is not False or
            receipt.get('standalone_quality_gate_allowed') is not False or
            route.get('standalone_quality_gate_allowed') is not False or
            receipt.get('human_emotion_retention') != 'FAIL' or receipt.get('original_404_human_result') != 'UNKNOWN' or
            proposal.get('status') != 'PROPOSED_NOT_AUTHORIZED' or proposal.get('new_prose_authorized') is not False or
            proposal.get('old_RC3_remaining_rounds') != 0 or proposal.get('old_197_character_protection_released') is not False or
            proposal.get('scope') != 'ONE_SECOND_SCENE_REENTRY_AND_MINIMAL_FACT_PREPARATION_ONLY' or
            any(v.get('next_action') != NEXT_ACTION for v in (route, receipt, task))):
        raise ValueError('CODEX_REVIEW_AUTHORITY_OR_SCOPE_PROMOTION')
    checker = review_module(root)
    target = receipt.get('target', {})
    if (target.get('path') != checker.TARGET or target.get('blob') != checker.TARGET_BLOB or
            manifest.get('source_head') != checker.HEAD or manifest.get('new_prose_authorized') is not False or
            manifest.get('generation_count') != 0 or manifest.get('old_remaining_rounds') != 0 or
            set(receipt.get('jobs', {})) != {'calibration', 'validation', 'facts', 'diagnosis'}):
        raise ValueError('CODEX_REVIEW_WRONG_CURRENT_TARGET_OR_MANIFEST')
    target_data = bound_bytes(root, target)
    thread_ids = []
    policy_hash = hashlib.sha256(checker.REVIEW_INSTRUCTIONS.encode()).hexdigest()
    for key in ('calibration', 'validation', 'facts', 'diagnosis'):
        job = receipt['jobs'][key]
        packet = load_bound(root, manifest['jobs'][key]['packet'])
        checker.validate_packet(packet)
        expected_kind = {'calibration': 'COLD_SCREEN', 'validation': 'COLD_SCREEN',
                         'facts': 'FACT_AUDIT', 'diagnosis': 'POST_FAILURE_DIAGNOSIS'}[key]
        if (packet['work_kind'] != expected_kind or manifest['jobs'][key].get('max_calls') != 1 or
                key != 'calibration' and (len(packet['samples']) != 1 or
                    packet['samples'][0]['text'].encode('utf-8') != target_data)):
            raise ValueError('CODEX_REVIEW_JOB_MATERIAL_OR_ROLE_DRIFT')
        runtime = load_bound(root, job['runtime'])
        evidence = load_bound(root, job['evidence'])
        report_bytes = bound_bytes(root, runtime['raw_report'])
        if (runtime.get('status') != 'RETURNED_NOT_YET_EVIDENCE_VERIFIED' or runtime.get('report_received') is not True or
                runtime.get('turn_status') != 'completed' or runtime.get('tool_activity_detected') or
                runtime.get('model_initiated_requests') or runtime.get('reviewer_repository_write_permission') is not False or
                runtime.get('packet') != manifest['jobs'][key]['packet'] or
                runtime.get('resolved_thread_settings', {}).get('model') != 'gpt-6.1-sol' or
                runtime.get('resolved_thread_settings', {}).get('reasoningEffort') != 'max' or
                runtime.get('resolved_thread_settings', {}).get('sandbox', {}).get('type') != 'readOnly' or
                runtime.get('resolved_thread_settings', {}).get('sandbox', {}).get('networkAccess') is not False or
                runtime.get('resolved_thread_settings', {}).get('instructionSources') != [] or
                runtime.get('resolved_thread_settings', {}).get('runtimeWorkspaceRoots') != [] or
                runtime.get('resolved_thread_settings', {}).get('approvalPolicy') != 'never' or
                runtime.get('isolation') != 'FRESH_PROCESS_FRESH_EPHEMERAL_THREAD_ENVIRONMENTS_DISABLED_NO_HISTORY' or
                runtime.get('prompt_policy_sha256') != policy_hash or
                runtime.get('raw_report') != job.get('raw_report') or
                runtime['raw_report'].get('blob') != blob(report_bytes) or
                runtime['raw_report'].get('sha256') != hashlib.sha256(report_bytes).hexdigest() or
                evidence.get('errors') or evidence.get('raw_report_rewritten') is not False or
                evidence.get('automatic_revision_authorized') is not False):
            raise ValueError('CODEX_REVIEW_INDEPENDENCE_OR_RUNTIME_NOT_PROVEN')
        submitted = {'verified_runtime': {'model': 'gpt-6.1-sol', 'reasoning_effort': 'max',
            'isolation': runtime['isolation']}, 'review_packet': packet}
        if runtime.get('submitted_payload_sha256') != hashlib.sha256(json.dumps(submitted, ensure_ascii=False).encode()).hexdigest():
            raise ValueError('CODEX_REVIEW_SUBMITTED_CONTEXT_NOT_BOUND')
        report = checker.parse_report(report_bytes)
        checked = checker.audit_report(packet, report, runtime)
        if checked['errors'] or checked['located_quotes'] != evidence.get('located_quotes'):
            raise ValueError('CODEX_REVIEW_UNLOCATED_OR_WRONG_REPORT')
        if key in ('facts', 'diagnosis') and any(r['verdict'] in ('BLOCKED', 'INSUFFICIENT') for r in report['results']):
            raise ValueError('CODEX_REVIEW_INCOMPLETE_DIAGNOSIS_NOT_COMPLETE')
        if not runtime.get('thread_id') or runtime['thread_id'] in thread_ids:
            raise ValueError('CODEX_REVIEW_CONTEXTS_NOT_SEPARATE')
        thread_ids.append(runtime['thread_id'])
    calibration = load_bound(root, receipt['calibration'])
    validation = load_bound(root, receipt['validation'])
    for reveal, key in ((calibration, 'calibration'), (validation, 'validation')):
        if (reveal.get('standalone_quality_gate_allowed') is not False or
                reveal.get('personal_taste_certification') is not False or
                reveal.get('false_positive_rate') != 'UNKNOWN_NO_SCOPE_MATCHED_POSITIVE' or
                reveal.get('prompt_retuned_after_labels') is not False or reveal.get('reruns') != 0 or
                reveal.get('frozen_raw_report') != receipt['jobs'][key]['raw_report'] or
                reveal.get('count') != len(reveal.get('samples', [])) or
                reveal.get('hits') != sum(row['failure_detected'] for row in reveal['samples']) or
                reveal.get('misses') != sum(row['false_release'] for row in reveal['samples'])):
            raise ValueError('CODEX_REVIEW_CALIBRATION_INFLATED')
        report = checker.parse_report(bound_bytes(root, receipt['jobs'][key]['raw_report']))
        reported = {r['artifact_id']: r['verdict'] for r in report['results']}
        labels = manifest['calibration_labels_coordinator_only'] if key == 'calibration' else [manifest['validation_label_coordinator_only']]
        if len(labels) != len(reveal['samples']):
            raise ValueError('CODEX_REVIEW_LABEL_BINDING_DRIFT')
        for row, label in zip(reveal['samples'], labels):
            human = load_bound(root, label['human_receipt'])
            original = bound_bytes(root, label['artifact'])
            # The two mainline receipts use artifact; the scoped R2 human
            # receipt uses output. Preserve and verify both native schemas.
            human_artifact = human.get('artifact') or human.get('output') or {}
            if (any(row.get(k) != label[k] for k in label) or human.get('outcome') != 'FAIL' or
                    human_artifact.get('path') != label['artifact']['path'] or
                    human_artifact.get('blob') != label['artifact']['blob'] or
                    'sha256' in human_artifact and human_artifact['sha256'] != label['artifact']['sha256'] or
                    row.get('frozen_AI_verdict') != reported.get(row['artifact_id']) or
                    row.get('failure_detected') is not (row['frozen_AI_verdict'] == 'REVISE') or
                    row.get('false_release') is not (row['frozen_AI_verdict'] == 'PASS_PROVISIONAL') or
                    row.get('inconclusive') is not (row['frozen_AI_verdict'] in ('BLOCKED', 'INSUFFICIENT'))):
                raise ValueError('CODEX_REVIEW_LABEL_BINDING_DRIFT')
            packet = load_bound(root, manifest['jobs'][key]['packet'])
            sample = next(s for s in packet['samples'] if s['artifact_id'] == row['artifact_id'])
            if sample['text'].encode('utf-8') != original:
                raise ValueError('CODEX_REVIEW_ANONYMOUS_SAMPLE_IDENTITY_DRIFT')
    if set(r['artifact_id'] for r in calibration['samples']) & set(r['artifact_id'] for r in validation['samples']):
        raise ValueError('CODEX_REVIEW_CALIBRATION_VALIDATION_OVERLAP')
    settlement = load_bound(root, receipt['coordinator_settlement'])
    if (settlement.get('all_quotes_checked') is not True or settlement.get('facts_and_scope_checked') is not True or
            settlement.get('diagnosis_label') != 'KNOWN_HUMAN_FAILURE_POST_FAILURE_DIAGNOSIS_NOT_BLIND' or
            settlement.get('new_prose_authorized') is not False or
            settlement.get('raw_reports_rewritten') is not False or
            settlement.get('human_exact_stop_sentence') != 'UNKNOWN' or
            settlement.get('human_robotic_dialogue') != 'UNKNOWN'):
        raise ValueError('CODEX_REVIEW_COORDINATOR_SETTLEMENT_MISSING')
    # START_HERE is the live human entry, not historical frozen plans.
    entry = (root / 'START_HERE.md').read_text(encoding='utf-8')
    if NEXT_ACTION not in entry or TASK not in entry:
        raise ValueError('CODEX_REVIEW_ENTRYPOINT_STALE')
    return NEXT_ACTION
