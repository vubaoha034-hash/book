"""Bind one separately authorized short to actual isolated runs and evidence.

This is a business/identity gate, not a literary-quality classifier. Historical
gates run first. Missing output, incomplete review, or spent budgets never pass.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path

TASK = 'NOVEL-R2-REENTRY-ONE-SHORT-TRIAL-20261003-01'
SOURCE = 'b1d1bbc16ea8b37f3886e9aa932ecfea3287d3e4'
SCOPE = 'ONE_NEW_300_500_CHARACTER_SECOND_SCENE_ENTRY_SHORT_TRIAL_WITH_EXPLICIT_OPENING_PERMISSION'
OLD_ACTION = 'AWAIT_LIU_AUTHORIZATION_OF_ONE_NEW_300_500_CHAR_R2_ENTRY_TRIAL_WITH_OPENING_SCOPE'
NEXT_ACTION = 'AWAIT_ACTUAL_HUMAN_READING_OF_R2_ENTRY_SHORT_A1'
STATUS = 'ONE_SHORT_FROZEN_FACT_CLEAR_AWAIT_ACTUAL_HUMAN_READING'
BODY_SHA = '6ec604bffc4c60727e102dde328663273f648a0e0b2e6d27b0350833128085aa'
AUTH_PATH = 'state/review_receipts/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_AUTHORIZATION_20261003.json'
CHECK_IDS = {f'T{i:02}' for i in range(1, 10)}
spec = importlib.util.spec_from_file_location('one_short_runner', Path(__file__).with_name('novel_one_short_trial.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
review = runner.review


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def bound(root, reference, as_json=True):
    path = (root / reference.get('path', '')).resolve()
    if not reference.get('path') or not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('ONE_SHORT_MISSING_MATERIAL')
    data = path.read_bytes()
    if reference.get('blob') != blob(data) or reference.get('sha256') != hashlib.sha256(data).hexdigest():
        raise ValueError('ONE_SHORT_IDENTITY_DRIFT')
    return json.loads(data) if as_json else data


def validate_authorization(root, project, checkpoint):
    route = project.get('r2_entry_short_trial')
    if not route or route != checkpoint.get('r2_entry_short_trial'):
        raise ValueError('ONE_SHORT_STATE_DRIFT')
    auth = bound(root, route['authorization'])
    manifest = bound(root, route['manifest'])
    proposal = bound(root, auth['authorized_proposal'])
    preparation = project.get('r2_reentry_fact_preparation', {})
    if (route['authorization'].get('path') != AUTH_PATH or
            auth.get('task_id') != TASK or auth.get('source_head') != SOURCE or
            auth.get('source_checkpoint') != 195 or auth.get('scope') != SCOPE or
            auth.get('parent_task_id') != preparation.get('task_id') or
            auth.get('authorized_proposal') != preparation.get('next_task_proposal') or
            auth.get('writer_context') != preparation.get('writer_context') or
            auth.get('authority', {}).get('source') != 'ACTUAL_USER_INSTRUCTION' or
            auth.get('authority', {}).get('exact_user_instruction') != '不用问，你直接完成就是。我们不要停下来。' or
            auth.get('authorized_generation_budget') != 1 or
            auth.get('new_version_opening_reorganization_authorized') is not True or
            auth.get('old_prefix_positions_may_change_in_new_version') != 197 or
            auth.get('old_artifacts_and_locks_must_remain_byte_identical') is not True or
            auth.get('human_quality_verdict_supplied_by_authorization') is not False or
            proposal.get('status') != 'PROPOSED_NOT_AUTHORIZED' or
            proposal.get('authorized_generation_budget') != 0 or proposal.get('proposed_generation_budget') != 1):
        raise ValueError('ONE_SHORT_USER_AUTHORIZATION_OR_PROPOSAL_DRIFT')
    if (manifest.get('task_id') != TASK or manifest.get('source_head') != SOURCE or
            manifest.get('authorization') != route['authorization'] or
            manifest.get('prepared_context') != auth.get('writer_context') or
            manifest.get('writer_input') != route.get('writer_input') or
            manifest.get('output_path') != route.get('artifact', {}).get('path') or
            manifest.get('model') != 'gpt-6.1-sol' or manifest.get('reasoning_effort') != 'max' or
            manifest.get('max_writer_calls') != 1 or manifest.get('max_fact_review_calls') != 1 or
            manifest.get('new_generation_budget') != 1 or manifest.get('automatic_retry') is not False):
        raise ValueError('ONE_SHORT_MANIFEST_SCOPE_DRIFT')
    for value in (auth, manifest):
        if (value.get('old_RC3_remaining_rounds') != 0 or
                value.get('old_197_character_protection_released') is not False or
                value.get('new_life_facts_authorized') is not False or
                value.get('full_v5_authorized') is not False or
                value.get('multiple_candidates_authorized') is not False):
            raise ValueError('ONE_SHORT_OLD_BUDGET_OR_SCOPE_PROMOTION')
    return route['authorization']


def runtime_check(root, reference, role, packet_ref, raw_ref, policy):
    runtime = bound(root, reference)
    settings = runtime.get('resolved_thread_settings', {})
    if (runtime.get('task_id') != TASK or runtime.get('role') != role or
            runtime.get('status') != 'RETURNED_RAW_OUTPUT_NOT_YET_SETTLED' or
            runtime.get('report_received') is not True or runtime.get('model_turn_dispatched') is not True or
            runtime.get('turn_status') != 'completed' or runtime.get('packet') != packet_ref or
            runtime.get('raw_report') != raw_ref or not runtime.get('thread_id') or
            runtime.get('isolation') != 'FRESH_PROCESS_FRESH_EPHEMERAL_THREAD_ENVIRONMENTS_DISABLED_NO_HISTORY' or
            runtime.get('repository_write_permission') is not False or
            runtime.get('tool_activity_detected') != [] or runtime.get('model_initiated_requests') != [] or
            set(runtime.get('completed_item_types', [])) - {'userMessage', 'reasoning', 'agentMessage'} or
            runtime.get('completed_item_types', []).count('agentMessage') != 1):
        raise ValueError('ONE_SHORT_NO_COMPLETE_ISOLATED_RUNTIME')
    if (settings.get('model') != 'gpt-6.1-sol' or settings.get('reasoningEffort') != 'max' or
            settings.get('sandbox') != {'type': 'readOnly', 'networkAccess': False} or
            settings.get('approvalPolicy') != 'never' or settings.get('instructionSources') != [] or
            settings.get('runtimeWorkspaceRoots') != [] or
            runtime.get('model_catalog_entry', {}).get('model') != 'gpt-6.1-sol' or
            'max' not in {v.get('reasoningEffort') for v in runtime.get('model_catalog_entry', {}).get('supportedReasoningEfforts', [])} or
            runtime.get('prompt_policy_sha256') != hashlib.sha256(policy.encode()).hexdigest()):
        raise ValueError('ONE_SHORT_ACTUAL_MODEL_OR_ISOLATION_DRIFT')
    packet = bound(root, packet_ref)
    payload = {'verified_runtime': {'model': settings['model'], 'reasoning_effort': settings['reasoningEffort'],
        'isolation': runtime['isolation']}, 'writer_packet' if role == 'writer' else 'review_packet': packet}
    if runtime.get('submitted_payload_sha256') != hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest():
        raise ValueError('ONE_SHORT_SUBMITTED_PACKET_DRIFT')
    return runtime


def one_short_trial_action(root, project, checkpoint, historical_action):
    if historical_action != OLD_ACTION:
        raise ValueError('ONE_SHORT_CANNOT_SKIP_HISTORICAL_GATES')
    validate_authorization(root, project, checkpoint)
    route = project['r2_entry_short_trial']
    task, receipt = (bound(root, route[k]) for k in ('task', 'result'))
    manifest = bound(root, route['manifest'])
    for value in (route, task, receipt):
        if (value.get('task_id') != TASK or value.get('source_head') != SOURCE or value.get('scope') != SCOPE or
                value.get('status') != STATUS or value.get('authorized_generation_budget') != 1 or
                value.get('generation_count') != 1 or value.get('remaining_new_generation_budget') != 0 or
                value.get('new_version_opening_reorganization_authorized') is not True or
                value.get('old_RC3_remaining_rounds') != 0 or
                value.get('old_197_character_protection_released') is not False or
                value.get('new_life_facts_authorized') is not False or value.get('full_v5_authorized') is not False or
                value.get('human_quality_result') != 'UNKNOWN' or value.get('original_404_human_result') != 'UNKNOWN' or
                value.get('old_448_human_emotion_retention') != 'FAIL' or
                value.get('literary_quality_validated') is not False or value.get('automatic_retry') is not False or
                value.get('next_action') != NEXT_ACTION):
            raise ValueError('ONE_SHORT_BUDGET_SCOPE_OR_HUMAN_PROMOTION')
    for value in (task, receipt):
        for key in ('authorization', 'manifest', 'writer_input', 'artifact', 'writer_runtime', 'facts_packet',
                    'facts_runtime', 'facts_raw_report', 'facts_evidence', 'coordinator_settlement'):
            if value.get(key) != route.get(key):
                raise ValueError('ONE_SHORT_DELIVERABLE_BINDING_DRIFT')
    text = bound(root, route['artifact'], False).decode('utf-8')
    count = sum(not c.isspace() for c in text)
    if (hashlib.sha256(text.encode()).hexdigest() != BODY_SHA or not 300 <= count <= 500 or
            count != route.get('non_whitespace_characters') or text.startswith('#') or '```' in text):
        raise ValueError('ONE_SHORT_FROZEN_BODY_OR_LENGTH_DRIFT')
    context = bound(root, manifest['prepared_context'])
    if manifest['prepared_context'].get('sha256') != runner.CONTEXT_SHA:
        raise ValueError('ONE_SHORT_FROZEN_FACT_CONTEXT_CHANGED')
    writer_packet = bound(root, route['writer_input'])
    runner.validate_writer_input(writer_packet, context)
    writer = runtime_check(root, route['writer_runtime'], 'writer', route['writer_input'], route['artifact'], runner.WRITER_POLICY)
    if writer.get('generation_count') != 1 or writer.get('non_whitespace_characters') != count or writer.get('authorized_length_matches') is not True:
        raise ValueError('ONE_SHORT_WRITER_GENERATION_OR_RANGE_DRIFT')
    facts = runtime_check(root, route['facts_runtime'], 'facts', route['facts_packet'], route['facts_raw_report'], review.REVIEW_INSTRUCTIONS)
    if writer['thread_id'] == facts['thread_id']:
        raise ValueError('ONE_SHORT_REVIEW_INHERITED_WRITER_CONTEXT')
    for role, directory in (('writer', manifest['writer_result_dir']), ('facts', manifest['fact_result_dir'])):
        attempt = json.loads((root / directory / f'{role}.attempt.json').read_bytes())
        if attempt.get('task_id') != TASK or attempt.get('role') != role or attempt.get('max_calls') != 1:
            raise ValueError('ONE_SHORT_DISPATCH_BUDGET_DRIFT')
    packet = bound(root, route['facts_packet'])
    expected_facts = {k: context[k] for k in ('setting', 'previous_scene', 'rojun_memory_and_responsibility',
        'xucheng_private_state', 'xucheng_own_life', 'shared_obligation', 'known_time_boundary',
        'viewpoint_and_knowledge', 'material_boundary', 'existing_locks')}
    expected_facts['short_span_endpoint'] = context['current_short_span_boundary']
    if (packet.get('work_kind') != 'FACT_AUDIT' or packet.get('job_id') != 'F196' or packet.get('facts') != expected_facts or
            packet.get('samples') != [{'artifact_id': 'S196', 'original_sha256': BODY_SHA, 'text': text}]):
        raise ValueError('ONE_SHORT_FACT_PACKET_SCOPE_OR_IDENTITY_DRIFT')
    report = review.parse_report(bound(root, route['facts_raw_report'], False))
    recomputed = review.audit_report(packet, report, facts)
    recomputed.update(task_id=TASK, packet=route['facts_packet'], raw_report=route['facts_raw_report'])
    if bound(root, route['facts_evidence']) != recomputed or recomputed['errors']:
        raise ValueError('ONE_SHORT_REPORT_OR_QUOTE_AUDIT_REJECTED')
    if report['results'][0]['verdict'] != 'FACT_CLEAR':
        raise ValueError('ONE_SHORT_FACT_REPORT_NOT_CLEAR')
    settlement = bound(root, route['coordinator_settlement'])
    if (settlement.get('task_id') != TASK or settlement.get('artifact') != route['artifact'] or
            settlement.get('facts_evidence') != route['facts_evidence'] or
            settlement.get('fact_context') != manifest['prepared_context'] or
            settlement.get('fact_disposition') != 'CLEAR_WITHIN_THIS_SHORT_SPAN' or
            settlement.get('unresolved_fact_conflicts') != [] or
            settlement.get('raw_body_rewritten') is not False or settlement.get('raw_report_rewritten') is not False or
            settlement.get('human_quality_result') != 'UNKNOWN' or settlement.get('automatic_revision_authorized') is not False or
            settlement.get('position_corrections') != recomputed['position_corrections'] or
            settlement.get('located_report_quote_count') != len(recomputed['located_quotes'])):
        raise ValueError('ONE_SHORT_COORDINATOR_SETTLEMENT_MISSING_OR_PROMOTED')
    checks = settlement.get('text_fact_checks', [])
    if {c.get('check_id') for c in checks} != CHECK_IDS or len(checks) != len(CHECK_IDS):
        raise ValueError('ONE_SHORT_FACT_COVERAGE_MISSING')
    for check in checks:
        quote = check.get('quote', '')
        offset = text.find(quote) if quote else -1
        if (offset < 0 or text[:offset].count('\n') + 1 != check.get('line') or
                check.get('disposition') != 'CLEAR' or not check.get('interpretation') or not check.get('fact_bindings')):
            raise ValueError('ONE_SHORT_SETTLEMENT_QUOTE_OR_SCOPE_MISSING')
        for source in check['fact_bindings']:
            if source.get('value') != context.get(source.get('context_field')):
                raise ValueError('ONE_SHORT_SETTLEMENT_FACT_COPY_DRIFT')
    dispositions = settlement.get('report_finding_dispositions', [])
    if len(dispositions) != len(report['results'][0]['findings']):
        raise ValueError('ONE_SHORT_REPORT_FINDING_NOT_SETTLED')
    for item, original in zip(dispositions, report['results'][0]['findings']):
        if (any(item.get(k) != original.get(k) for k in ('id', 'quote', 'line')) or
                item.get('disposition') != 'ACCEPT_FACT_OBSERVATION_NO_PROSE_CHANGE' or
                item.get('scope_checked') is not True or not item.get('coordinator_reason')):
            raise ValueError('ONE_SHORT_REPORT_FINDING_NOT_SETTLED')
    if (settlement.get('protected_parts_checked') != report['results'][0]['protected_parts'] or
            settlement.get('unknowns_preserved') != report['results'][0]['unknowns'] or
            receipt.get('fact_report_verdict') != 'FACT_CLEAR' or
            receipt.get('located_report_quote_count') != len(recomputed['located_quotes']) or
            receipt.get('coordinator_text_fact_checks') != len(checks) or
            receipt.get('writer_model_calls') != 1 or receipt.get('independent_fact_review_model_calls') != 1 or
            receipt.get('human_feedback') != {} or task.get('human_feedback') != {} or
            receipt.get('human_exact_stop') != 'UNKNOWN' or
            receipt.get('literary_effect_relative_to_old_short') != 'UNTESTED'):
        raise ValueError('ONE_SHORT_EVIDENCE_COUNT_UNKNOWN_OR_HUMAN_DRIFT')
    for value in (project, checkpoint):
        if (value.get('last_completed_task_id') != TASK or value.get('last_completed_task_contract') != route['task']['path'] or
                value.get('next_action') != NEXT_ACTION or value.get('next_required_action') != NEXT_ACTION):
            raise ValueError('ONE_SHORT_LIVE_CURSOR_DRIFT')
    if checkpoint.get('sequence') != 196 or checkpoint.get('stop') is not True:
        raise ValueError('ONE_SHORT_CHECKPOINT_OR_STOP_DRIFT')
    entry = (root / 'START_HERE.md').read_text(encoding='utf-8')
    if TASK not in entry or NEXT_ACTION not in entry or '当前位置：检查点196。' not in entry:
        raise ValueError('ONE_SHORT_ENTRYPOINT_STALE')
    return NEXT_ACTION
