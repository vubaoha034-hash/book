"""Verify actual human failure, source access, isolated diagnosis and no prose.

Advances the live cursor only. All prior receipts, rejected prose, calibration
limitations and writing budgets remain independently checked by older gates.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path

TASK = 'NOVEL-EMOTION-REACTION-AND-PACING-LEARNING-20261003-01'
SOURCE = '7997b03fb3a0ec5eaf8e0e5b55f91cd651094fde'
SCOPE = 'RECORD_395_HUMAN_FAILURE_READ_PROFESSIONAL_SOURCES_AND_IMPROVE_REUSABLE_EMOTION_REACTION_PACING_METHOD_NO_PROSE'
OLD_ACTION = 'AWAIT_ACTUAL_HUMAN_READING_OF_R2_ENTRY_SHORT_A1'
NEXT_ACTION = 'AWAIT_NEW_EXPLICIT_BOUNDED_WRITING_BUDGET_FOR_PREPARED_EMOTION_REACTION_TRIAL'
STATUS = 'PROFESSIONAL_STUDY_AND_DIAGNOSIS_COMPLETE_HUMAN_FAIL_PRESERVED_NO_PROSE'
BODY = 'delivery/r2-entry-trial-20261003/short-a1.md'
BODY_SHA = '6ec604bffc4c60727e102dde328663273f648a0e0b2e6d27b0350833128085aa'
HUMAN_PATH = 'state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_FAIL_20261003.json'
AUTH_PATH = 'state/review_receipts/NOVEL_EMOTION_PACING_LEARNING_AUTHORIZATION_20261003.json'
EXACT = '一，我不是很满意，ai味道很重。  二，情绪还是平。   比如我会惊讶，会难过等等对吧。这个就跟机器人一样。  三，我觉得现在应该有大量的小说写的教程，书籍，视频等等，你应该自己查找，自己看看如何才能提高小说的写作方法，特别是现在的小说追求快节奏。明白我的意思吗？不应该让我总在这里帮你出主意，网络上大量的专业性质的。'
REF_KEYS = ('authorization', 'human_feedback', 'previous_human_feedback', 'previous_short_result',
    'target', 'manifest', 'packet', 'runtime', 'raw_report', 'evidence', 'settlement', 'sources',
    'method_document', 'study_document', 'craft_capsule', 'next_task_proposal', 'diagnosis_document')
spec = importlib.util.spec_from_file_location('emotion_diagnosis_runner', Path(__file__).with_name('novel_emotion_diagnosis.py'))
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
review = runner.review


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def bound(root, ref, as_json=True):
    path = (root / ref.get('path', '')).resolve()
    if not ref.get('path') or not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('LEARNING_MISSING_MATERIAL')
    data = path.read_bytes()
    if ref.get('blob') != blob(data) or ref.get('sha256') != hashlib.sha256(data).hexdigest():
        raise ValueError('LEARNING_IDENTITY_DRIFT')
    return json.loads(data) if as_json else data


def validate_authorization(root, project, checkpoint):
    route = project.get('emotion_pacing_learning')
    if not route or route != checkpoint.get('emotion_pacing_learning'):
        raise ValueError('LEARNING_STATE_DRIFT')
    if route.get('authorization', {}).get('path') != AUTH_PATH or route.get('human_feedback', {}).get('path') != HUMAN_PATH:
        raise ValueError('LEARNING_AUTHORITY_PATH_DRIFT')
    auth = bound(root, route['authorization'])
    human = bound(root, route['human_feedback'])
    report = human.get('review', {})
    text = bound(root, route['target'], False)
    prior = project.get('r2_entry_short_trial', {})
    if (auth.get('task_id') != TASK or auth.get('source_head') != SOURCE or auth.get('source_checkpoint') != 196 or
            auth.get('scope') != SCOPE or auth.get('authority', {}).get('source') != 'ACTUAL_CURRENT_USER_INSTRUCTION' or
            auth.get('authority', {}).get('exact_user_instruction') != EXACT or
            auth.get('human_feedback') != route['human_feedback'] or auth.get('maximum_new_diagnostic_calls') != 1 or
            auth.get('generation_budget') != 0 or auth.get('new_prose_authorized') is not False or
            auth.get('old_RC3_remaining_rounds') != 0 or auth.get('old_197_character_protection_released') is not False or
            any(auth.get(k) is not False for k in ('full_v5_authorized', 'new_life_facts_authorized', 'automatic_background_tasks_authorized'))):
        raise ValueError('LEARNING_AUTHORIZATION_OR_BUDGET_DRIFT')
    if (human.get('task_id') != TASK or human.get('source_head') != SOURCE or human.get('source_checkpoint') != 196 or
            human.get('output') != route['target'] or route['target'] != prior.get('artifact') or
            route['target'].get('path') != BODY or hashlib.sha256(text).hexdigest() != BODY_SHA or
            sum(not c.isspace() for c in text.decode()) != 395 or human.get('outcome') != 'FAIL' or
            human.get('processed_once') is not True or human.get('new_generation_budget') != 0 or
            human.get('generation_count_this_feedback_record') != 0 or
            human.get('prior_snapshot_result') != route.get('previous_short_result') or route.get('previous_short_result') != prior.get('result') or
            report.get('human_exact_feedback') != EXACT or report.get('source', {}).get('kind') != 'ACTUAL_CURRENT_USER_MESSAGE' or
            report.get('source', {}).get('message_observed_directly') is not True or
            report.get('bound_artifact_path') != BODY or report.get('bound_blob') != blob(text) or report.get('bound_sha256') != BODY_SHA or
            report.get('bound_method_revision') != 4 or report.get('bound_version') != 'SHORT-ENTRY-A1-395' or
            any(report.get(k) != 'FAIL' for k in ('robotic_interaction_verdict', 'emotion_verdict', 'ai_smell_verdict')) or
            report.get('wants_to_continue') != 'UNKNOWN_NOT_EXPLICITLY_ANSWERED' or
            report.get('exact_stop_sentence') != 'UNKNOWN_NOT_PROVIDED' or
            any(report.get(k) is not False for k in ('human_quality_accepted', 'same_artifact_resubmission_allowed', 'topic_rejection', 'full_v5_authorized'))):
        raise ValueError('LEARNING_ACTUAL_HUMAN_FEEDBACK_OR_ARTIFACT_DRIFT')
    if any(v.get('human_verdict_receipt') != HUMAN_PATH or v.get('latest_human_review') != report for v in (project, checkpoint)):
        raise ValueError('LEARNING_LATEST_HUMAN_MIRROR_DRIFT')
    old = bound(root, route['previous_human_feedback'])
    if (route['previous_human_feedback'].get('path') != 'state/review_receipts/NOVEL_RC3_R2_HUMAN_RETENTION_FAIL_20261002.json' or
            old.get('outcome') != 'FAIL' or old.get('output', {}).get('blob') != 'f0545b15cf01dd6de83e105003e3af34b22cf4db'):
        raise ValueError('LEARNING_PRIOR_HUMAN_REJECTION_DRIFT')
    return route['authorization']


def validate_capsule(capsule):
    if set(capsule) != {'point_of_view', 'craft_guidance'} or len(capsule['craft_guidance']) != 3:
        raise ValueError('LEARNING_WRITER_CAPSULE_ALLOWLIST_DRIFT')
    text = json.dumps(capsule, ensure_ascii=False)
    if len(text) > 600 or any(word in text for word in ('FAIL', 'PASS', 'feedback', 'diagnosis', '刘先生', '395', '448',
            '惊讶', '难过', '罗钧', '许澄', '连续性项目', '只返回正文', 'reviewer-input', '十八万六')):
        raise ValueError('LEARNING_WRITER_FAILURE_OR_ANSWER_LEAKAGE')


def learning_action(root, project, checkpoint, historical_action, successor_authorization=None):
    if historical_action != OLD_ACTION:
        raise ValueError('LEARNING_CANNOT_SKIP_HISTORICAL_GATES')
    validate_authorization(root, project, checkpoint)
    route = project['emotion_pacing_learning']
    task, result = (bound(root, route[k]) for k in ('task', 'result'))
    for value in (route, task, result):
        if (value.get('task_id') != TASK or value.get('source_head') != SOURCE or value.get('scope') != SCOPE or
                value.get('status') != STATUS or value.get('generation_budget') != 0 or value.get('generation_count') != 0 or
                value.get('new_prose_authorized') is not False or value.get('old_RC3_remaining_rounds') != 0 or
                value.get('old_197_character_protection_released') is not False or value.get('full_v5_authorized') is not False or
                value.get('new_life_facts_authorized') is not False or value.get('story_goal_changed') is not False or
                value.get('formal_mainline_method_revision') != 4 or value.get('human_quality_result') != 'FAIL' or
                value.get('original_404_human_result') != 'UNKNOWN' or value.get('old_448_human_emotion_retention') != 'FAIL' or
                value.get('literary_quality_validated') is not False or value.get('writing_transfer') != 'UNPROVEN' or
                value.get('independent_diagnostic_model_calls') != 1 or value.get('cold_screen_calls') != 0 or
                value.get('next_action') != NEXT_ACTION):
            raise ValueError('LEARNING_SCOPE_OR_QUALITY_PROMOTION')
        if any(value.get(k) != route.get(k) for k in REF_KEYS):
            raise ValueError('LEARNING_DELIVERABLE_BINDING_DRIFT')
    manifest = bound(root, route['manifest'])
    runner.validate_scope(manifest, bound(root, route['authorization']))
    if any(manifest.get(k) != route.get(k) for k in ('authorization', 'human_feedback', 'packet')) or manifest.get('artifact') != route['target']:
        raise ValueError('LEARNING_MANIFEST_BINDING_DRIFT')
    packet = bound(root, route['packet'])
    review.validate_packet(packet)
    if (packet.get('work_kind') != 'POST_FAILURE_DIAGNOSIS' or packet.get('job_id') != 'D197' or
            packet['samples'] != [{'artifact_id': 'S197', 'original_sha256': BODY_SHA, 'text': bound(root, route['target'], False).decode()}] or
            packet.get('human_feedback') != EXACT or packet.get('facts') != bound(root, manifest['facts_source'])['facts'] or
            packet.get('historical_material') != {'status': 'NOT_TRANSMITTED_NO_WRITER_DIRECTIONS_OR_OTHER_REPORTS', 'text': ''}):
        raise ValueError('LEARNING_DIAGNOSTIC_CONTEXT_DRIFT')
    runtime = bound(root, route['runtime'])
    settings = runtime.get('resolved_thread_settings', {})
    if (runtime.get('status') != 'RETURNED_RAW_REPORT_NOT_YET_SETTLED' or runtime.get('report_received') is not True or
            runtime.get('model_turn_dispatched') is not True or runtime.get('turn_status') != 'completed' or
            runtime.get('task_id') != TASK or runtime.get('job_id') != 'D197' or runtime.get('generation_count') != 0 or
            runtime.get('packet') != route['packet'] or runtime.get('raw_report') != route['raw_report'] or
            runtime.get('repository_write_permission') is not False or runtime.get('tool_activity_detected') != [] or
            runtime.get('model_initiated_requests') != [] or runtime.get('isolation') !=
            'FRESH_PROCESS_FRESH_EPHEMERAL_THREAD_ENVIRONMENTS_DISABLED_NO_HISTORY' or not runtime.get('thread_id') or
            set(runtime.get('completed_item_types', [])) - {'userMessage', 'reasoning', 'agentMessage'} or
            runtime.get('completed_item_types', []).count('agentMessage') != 1):
        raise ValueError('LEARNING_NO_COMPLETE_ISOLATED_DIAGNOSIS')
    if (settings.get('model') != 'gpt-6.1-sol' or settings.get('reasoningEffort') != 'max' or
            settings.get('sandbox') != {'type': 'readOnly', 'networkAccess': False} or settings.get('approvalPolicy') != 'never' or
            settings.get('instructionSources') != [] or settings.get('runtimeWorkspaceRoots') != [] or
            runtime.get('model_catalog_entry', {}).get('model') != 'gpt-6.1-sol' or 'max' not in
            {x.get('reasoningEffort') for x in runtime.get('model_catalog_entry', {}).get('supportedReasoningEfforts', [])} or
            runtime.get('prompt_policy_sha256') != hashlib.sha256(review.REVIEW_INSTRUCTIONS.encode()).hexdigest()):
        raise ValueError('LEARNING_ACTUAL_MODEL_OR_ISOLATION_DRIFT')
    payload = {'verified_runtime': {'model': settings['model'], 'reasoning_effort': settings['reasoningEffort'],
        'isolation': runtime['isolation']}, 'review_packet': packet}
    if runtime.get('submitted_payload_sha256') != hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest():
        raise ValueError('LEARNING_ACTUAL_PAYLOAD_DRIFT')
    previous_route = project['r2_entry_short_trial']
    if runtime['thread_id'] in {bound(root, previous_route[k])['thread_id'] for k in ('writer_runtime', 'facts_runtime')}:
        raise ValueError('LEARNING_INHERITED_PREVIOUS_CONTEXT')
    attempt = json.loads((root / runner.DIRECTORY / 'diagnosis.attempt.json').read_bytes())
    if attempt.get('task_id') != TASK or attempt.get('max_calls') != 1 or attempt.get('packet') != route['packet']:
        raise ValueError('LEARNING_DIAGNOSTIC_BUDGET_DRIFT')
    report = review.parse_report(bound(root, route['raw_report'], False))
    recomputed = review.audit_report(packet, report, runtime)
    saved = bound(root, route['evidence'])
    if recomputed['errors'] or any(saved.get(k) != v for k, v in recomputed.items()):
        raise ValueError('LEARNING_REPORT_OR_QUOTE_EVIDENCE_DRIFT')
    settlement = bound(root, route['settlement'])
    findings = report['results'][0]['findings']
    dispositions = settlement.get('finding_dispositions', [])
    if (settlement.get('status') != 'DIAGNOSIS_EVIDENCE_AND_SCOPE_SETTLED_HYPOTHESES_NOT_HUMAN_PROOF' or
            settlement.get('raw_report') != route['raw_report'] or settlement.get('evidence') != route['evidence'] or
            settlement.get('raw_report_rewritten') is not False or settlement.get('automatic_revision_authorized') is not False or
            settlement.get('known_failure_diagnosis') is not True or settlement.get('human_quality_result') != 'FAIL' or
            settlement.get('protected_parts_checked') != report['results'][0]['protected_parts'] or
            settlement.get('unknowns_preserved') != report['results'][0]['unknowns'] or
            len(dispositions) != len(findings) or not 2 <= len(dispositions) <= 3):
        raise ValueError('LEARNING_COORDINATOR_SETTLEMENT_MISSING_OR_PROMOTED')
    window_checks = settlement.get('reading_window_quote_checks', [])
    if (len(window_checks) != 3 or {x.get('window') for x in window_checks} !=
            {'first_30_60', 'first_150_300', 'ending'}):
        raise ValueError('LEARNING_READING_WINDOW_EVIDENCE_MISSING')
    text = packet['samples'][0]['text']
    for item in window_checks:
        original = report['results'][0]['reading_expectations'][item['window']]
        offset = text.find(item.get('quote', '')) if item.get('quote') else -1
        if (offset < 0 or item.get('quote') != original.get('quote') or
                text[:offset].count('\n') + 1 != item.get('line') or
                item.get('start_character_0_based') != offset or item.get('exact_quote_found') is not True or
                item.get('interpretation') != 'EDITOR_HYPOTHESIS_NOT_ACTUAL_HUMAN_READING_TRACE'):
            raise ValueError('LEARNING_READING_WINDOW_QUOTE_OR_INFERENCE_DRIFT')
    context = bound(root, previous_route['manifest'])['prepared_context']
    frozen_facts = bound(root, context)
    for finding, item in zip(findings, dispositions):
        if (any(item.get(k) != finding.get(k) for k in ('id', 'quote', 'line', 'basis')) or
                item.get('disposition') != 'ACCEPT_AS_EDITORIAL_HYPOTHESIS_NO_PROSE_CHANGE' or
                item.get('scope_checked') is not True or not item.get('coordinator_reason') or
                not item.get('fact_bindings') or not item.get('source_ids')):
            raise ValueError('LEARNING_FINDING_NOT_SETTLED')
        for fact in item['fact_bindings']:
            if fact.get('value') != frozen_facts.get(fact.get('context_field')):
                raise ValueError('LEARNING_FACT_MISREAD_OR_INVENTED')
    sources = bound(root, route['sources'])
    by_id = {x.get('source_id'): x for x in sources.get('sources', [])}
    if (set(by_id) != {f'S{i:02}' for i in range(1, 12)} or sources.get('adopted_source_count') != 9 or
            sum(x.get('adopted') is True for x in by_id.values()) != 9 or
            sources.get('full_book_read') is not False or sources.get('complete_video_watched') is not False or
            sources.get('raw_copyrighted_sources_in_public_git') is not False or
            sources.get('writing_transfer') != 'UNPROVEN' or sources.get('automatic_learning') is not False or
            by_id['S05'].get('access_level') != 'OFFICIAL_LECTURE_NOTES_ONLY' or
            by_id['S08'].get('access_level') != 'PUBLISHER_DESCRIPTION_AND_PUBLIC_INTRODUCTION_EXCERPT' or
            by_id['S10'].get('adopted') is not False or by_id['S11'].get('adopted') is not False or
            by_id['S09'].get('commit') != '0d5bf7fd987554e05db7e05d569736e648297722' or
            len(by_id['S09'].get('resources', [])) != 3):
        raise ValueError('LEARNING_SOURCE_READING_OR_TRANSFER_OVERCLAIM')
    if any(not x.get('url') or not x.get('read_locator') or not x.get('own_learning_note') or not x.get('transfer_limit') for x in by_id.values()):
        raise ValueError('LEARNING_SOURCE_EVIDENCE_MISSING')
    if any(s not in by_id or by_id[s]['adopted'] is not True for x in dispositions for s in x['source_ids']):
        raise ValueError('LEARNING_UNREAD_SOURCE_NOT_EVIDENCE')
    validate_capsule(bound(root, route['craft_capsule']))
    proposal = bound(root, route['next_task_proposal'])
    if (proposal.get('status') != 'PREPARED_NOT_AUTHORIZED' or proposal.get('authorized_generation_budget') != 0 or
            proposal.get('proposed_generation_budget') != 1 or proposal.get('generation_count') != 0 or
            proposal.get('new_prose_authorized') is not False or proposal.get('automatic_activation') is not False or
            proposal.get('old_RC3_remaining_rounds') != 0 or proposal.get('old_197_character_protection_released') is not False or
            proposal.get('new_life_facts_authorized') is not False or proposal.get('full_v5_authorized') is not False or
            proposal.get('multiple_candidates_allowed') is not False or proposal.get('context') != context or
            proposal.get('craft_capsule') != route['craft_capsule'] or proposal.get('minimum_non_whitespace_characters') != 300 or
            proposal.get('maximum_non_whitespace_characters') != 500 or proposal.get('output_count') != 1 or
            proposal.get('proposed_change', {}).get('new_life_fact_count') != 0 or
            proposal.get('proposed_change', {}).get('replacement_sentences') != [] or
            proposal.get('proposed_change', {}).get('mandatory_action_sequence') is not False):
        raise ValueError('LEARNING_NEXT_WRITER_NOT_AUTHORIZED')
    for k in ('method_document', 'study_document', 'diagnosis_document'):
        if len(bound(root, route[k], False)) < 400:
            raise ValueError('LEARNING_EMPTY_DOCUMENT_NOT_COMPLETED')
    for value in (project, checkpoint):
        if (value.get('last_completed_task_id') != TASK or value.get('last_completed_task_contract') != route['task']['path'] or
                value.get('next_action') != NEXT_ACTION or value.get('next_required_action') != NEXT_ACTION or
                value.get('current_human_gate') != 'CURRENT_395_HUMAN_FAIL_OLD_448_FAIL_ORIGINAL_404_UNKNOWN'):
            raise ValueError('LEARNING_LIVE_CURSOR_DRIFT')
    if checkpoint.get('sequence') != 197 or checkpoint.get('stop') is not True:
        raise ValueError('LEARNING_CHECKPOINT_OR_STOP_DRIFT')
    entry = (root / 'START_HERE.md').read_text(encoding='utf-8')
    valid_new_entry = False
    if successor_authorization is not None:
        successor = bound(root, successor_authorization)
        valid_new_entry = (successor_authorization.get('path') == 'state/review_receipts/NOVEL_TWO_ROLE_REVIEW_AUTHORIZATION_20261003.json' and
            successor.get('task_id') == 'NOVEL-TWO-ROLE-OPENING-REVIEW-20261003-01' and successor.get('source_checkpoint') == 197 and
            successor.get('generation_budget') == 0 and successor.get('new_prose_authorized') is False and
            successor.get('maximum_new_review_calls') == 2 and '当前位置：检查点198。' in entry)
    if TASK not in entry or NEXT_ACTION not in entry or ('当前位置：检查点197。' not in entry and not valid_new_entry):
        raise ValueError('LEARNING_ENTRYPOINT_STALE')
    return NEXT_ACTION
