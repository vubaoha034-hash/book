"""Validate two actual isolated AI roles without promoting taste or prose budget."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('two_role_runner', Path(__file__).with_name('novel_two_role_review.py'))
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
review = runner.review
TASK, SOURCE = runner.TASK, runner.SOURCE
NEXT = 'AWAIT_ONE_NEW_BOUNDED_WRITING_BUDGET_FOR_REVIEWED_OPENING_REENTRY_INPUT'
OLD = 'AWAIT_NEW_EXPLICIT_BOUNDED_WRITING_BUDGET_FOR_PREPARED_EMOTION_REACTION_TRIAL'
STATUS = 'TWO_INDEPENDENT_AI_REVIEWS_AND_ONE_OPENING_SCOPE_PREPARATION_COMPLETE_NO_PROSE'
REF_KEYS = ('authorization','human_feedback','previous_human_feedback','target','manifest','sources',
    'reader_runtime','reader_raw','reader_evidence','editor_runtime','editor_raw','editor_evidence',
    'settlement','prepared_input','next_task_proposal','method_document','result_document')


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def bound(root, reference, as_json=True):
    path = (root / reference.get('path','')).resolve()
    if not reference.get('path') or not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('TWO_ROLE_MISSING_MATERIAL')
    data = path.read_bytes()
    if reference.get('blob') != blob(data) or reference.get('sha256') != hashlib.sha256(data).hexdigest():
        raise ValueError('TWO_ROLE_IDENTITY_DRIFT')
    return json.loads(data) if as_json else data


def validate_authorization(root, project, checkpoint):
    route = project.get('two_role_opening_review')
    if not route or route != checkpoint.get('two_role_opening_review'):
        raise ValueError('TWO_ROLE_STATE_DRIFT')
    auth = bound(root, route['authorization'])
    manifest = bound(root, route['manifest'])
    runner.validate_scope(manifest, auth)
    human = bound(root, route['human_feedback'])
    previous = project.get('emotion_pacing_learning',{})
    old = bound(root, route['previous_human_feedback'])
    text = bound(root, route['target'], False)
    if (route['authorization'].get('path') != runner.AUTH or route['human_feedback'].get('path') != runner.HUMAN or
            route['target'].get('path') != runner.BODY or hashlib.sha256(text).hexdigest() != runner.BODY_SHA or
            route['target'] != previous.get('target') or route['previous_human_feedback'] != previous.get('human_feedback') or
            auth.get('retention_feedback') != route['human_feedback'] or auth.get('previous_learning_result') != previous.get('result') or
            auth.get('new_writing_budget_inferred_from_review_completion') is not False or
            auth.get('authorized_next_work') != 'TWO_ACTUAL_ISOLATED_AI_ROLES_THEN_ONE_EVIDENCE_BASED_OPENING_SCOPE_AND_INPUT_PREPARATION' or
            any(auth.get(k) is not False for k in ('full_v5_authorized','new_life_facts_authorized','automatic_background_tasks_authorized'))):
        raise ValueError('TWO_ROLE_SCOPE_OR_NEW_WRITING_BUDGET_DRIFT')
    current = human.get('review',{})
    expected = dict(old['review'])
    expected.update(human_exact_feedback=runner.RETENTION_FEEDBACK,
        feedback_summary='刘先生继续明确指出当前395字开头没有继续阅读欲望；前次AI味、情绪和互动否决保留。',
        wants_to_continue=False, retention_verdict='FAIL',
        source={'kind':'ACTUAL_CURRENT_USER_MESSAGE','message_observed_directly':True},
        carried_dimensions_source=route['previous_human_feedback'],
        scope_note='在当前395字稿及其反馈之后的直接补充；不是旧448/404字的新判决。')
    if (human.get('task_id') != TASK or human.get('source_head') != SOURCE or human.get('source_checkpoint') != 197 or
            human.get('output') != route['target'] or human.get('prior_human_feedback') != route['previous_human_feedback'] or
            human.get('outcome') != 'FAIL' or human.get('processed_once') is not True or
            human.get('prior_receipt_rewritten') is not False or human.get('new_generation_budget') != 0 or
            human.get('exact_stop_sentence') != 'UNKNOWN_NOT_PROVIDED' or current != expected or
            old.get('outcome') != 'FAIL' or old.get('review',{}).get('wants_to_continue') != 'UNKNOWN_NOT_EXPLICITLY_ANSWERED'):
        raise ValueError('TWO_ROLE_ACTUAL_HUMAN_SUPPLEMENT_DRIFT')
    if any(v.get('human_verdict_receipt') != runner.HUMAN or v.get('latest_human_review') != current for v in (project,checkpoint)):
        raise ValueError('TWO_ROLE_CURRENT_HUMAN_MIRROR_DRIFT')
    return route['authorization']


def historical_learning_view(root, project, checkpoint):
    """Only after validating the new authority, retain checkpoint197's own view."""
    auth = validate_authorization(root, project, checkpoint)
    p, c = copy.deepcopy(project), copy.deepcopy(checkpoint)
    route = p['emotion_pacing_learning']
    human = bound(root, route['human_feedback'])
    for value in (p,c):
        value.update(human_verdict_receipt=route['human_feedback']['path'], latest_human_review=human['review'],
            last_completed_task_id=route['task_id'],last_completed_task_contract=route['task']['path'],
            next_action=OLD,next_required_action=OLD,
            current_human_gate='CURRENT_395_HUMAN_FAIL_OLD_448_FAIL_ORIGINAL_404_UNKNOWN')
    c.update(sequence=197,stop=True)
    return p,c,auth


def check_runtime(root, route, manifest, role, packet):
    runtime = bound(root, route[f'{role}_runtime'])
    settings = runtime.get('resolved_thread_settings',{})
    job = manifest['jobs'][role]
    if (runtime.get('task_id') != TASK or runtime.get('role') != role or runtime.get('job_id') != packet['job_id'] or
            runtime.get('status') != 'RETURNED_RAW_REPORT_NOT_YET_SETTLED' or runtime.get('report_received') is not True or
            runtime.get('model_turn_dispatched') is not True or runtime.get('turn_status') != 'completed' or
            runtime.get('packet') != job['packet'] or runtime.get('policy') != job['policy'] or
            runtime.get('raw_report') != route[f'{role}_raw'] or runtime.get('generation_count') != 0 or
            runtime.get('repository_write_permission') is not False or runtime.get('tool_activity_detected') != [] or
            runtime.get('model_initiated_requests') != [] or runtime.get('isolation') != runner.ISOLATION or
            not runtime.get('thread_id') or set(runtime.get('completed_item_types',[]))-{'userMessage','reasoning','agentMessage'} or
            runtime.get('completed_item_types',[]).count('agentMessage') != 1):
        raise ValueError('TWO_ROLE_NO_COMPLETE_ISOLATED_REPORT')
    if (settings.get('model') != 'gpt-6.1-sol' or settings.get('reasoningEffort') != 'max' or
            settings.get('sandbox') != {'type':'readOnly','networkAccess':False} or settings.get('approvalPolicy') != 'never' or
            settings.get('instructionSources') != [] or settings.get('runtimeWorkspaceRoots') != [] or
            runtime.get('model_catalog_entry',{}).get('model') != 'gpt-6.1-sol' or
            'max' not in {x.get('reasoningEffort') for x in runtime.get('model_catalog_entry',{}).get('supportedReasoningEfforts',[])} or
            runtime.get('prompt_policy_sha256') != hashlib.sha256(bound(root,job['policy'],False)).hexdigest()):
        raise ValueError('TWO_ROLE_ACTUAL_MODEL_OR_PERMISSION_DRIFT')
    payload = {'verified_runtime':{'model':'gpt-6.1-sol','reasoning_effort':'max','isolation':runner.ISOLATION},
        'review_packet':packet}
    if runtime.get('submitted_payload_sha256') != hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest():
        raise ValueError('TWO_ROLE_SUBMITTED_PAYLOAD_DRIFT')
    attempt = json.loads((root / runner.DIRECTORY / f'{role}.attempt.json').read_bytes())
    if (attempt.get('task_id') != TASK or attempt.get('role') != role or attempt.get('max_calls') != 1 or
            attempt.get('job_id') != packet['job_id'] or attempt.get('packet') != job['packet']):
        raise ValueError('TWO_ROLE_ATTEMPT_BUDGET_DRIFT')
    return runtime


def two_role_action(root, project, checkpoint, historical_action, successor_authorization=None, successor_human_feedback=None):
    if historical_action != OLD: raise ValueError('TWO_ROLE_CANNOT_SKIP_HISTORICAL_GATES')
    validate_authorization(root,project,checkpoint)
    route = project['two_role_opening_review']
    task, result = (bound(root,route[k]) for k in ('task','result'))
    for value in (route,task,result):
        if (value.get('task_id') != TASK or value.get('source_head') != SOURCE or value.get('status') != STATUS or
                value.get('generation_budget') != 0 or value.get('generation_count') != 0 or
                value.get('new_prose_authorized') is not False or value.get('old_RC3_remaining_rounds') != 0 or
                value.get('old_197_character_protection_released') is not False or value.get('full_v5_authorized') is not False or
                value.get('new_life_facts_authorized') is not False or value.get('formal_mainline_method_revision') != 4 or
                value.get('human_quality_result') != 'FAIL' or value.get('human_wants_to_continue') is not False or
                value.get('original_404_human_result') != 'UNKNOWN' or value.get('old_448_human_emotion_retention') != 'FAIL' or
                value.get('independent_AI_review_calls') != 2 or value.get('actual_human_reviewer_count') != 0 or
                value.get('standalone_quality_gate_allowed') is not False or value.get('next_action') != NEXT):
            raise ValueError('TWO_ROLE_QUALITY_SCOPE_OR_BUDGET_PROMOTION')
        if any(value.get(k) != route.get(k) for k in REF_KEYS): raise ValueError('TWO_ROLE_DELIVERABLE_BINDING_DRIFT')
    manifest = bound(root,route['manifest'])
    if (manifest.get('authorization') != route['authorization'] or manifest.get('human_feedback') != route['human_feedback'] or
            manifest.get('artifact') != route['target'] or manifest.get('roles_are_actual_humans') is not False or
            manifest.get('blind_calibration_rerun') is not False or manifest.get('standalone_quality_gate_allowed') is not False):
        raise ValueError('TWO_ROLE_MANIFEST_OR_QUALITY_GATE_DRIFT')
    reports, runtimes = {}, {}
    for role in ('reader','editor'):
        packet = bound(root,manifest['jobs'][role]['packet'])
        review.validate_packet(packet)
        if (packet['samples'] != [{'artifact_id':'A08','original_sha256':runner.BODY_SHA,
                'text':bound(root,route['target'],False).decode()}] or
                packet.get('job_id') != {'reader':'R198','editor':'E198'}[role] or
                packet.get('work_kind') != {'reader':'COLD_SCREEN','editor':'POST_FAILURE_DIAGNOSIS'}[role] or
                packet.get('medium') != '手机阅读的中文小说' or
                packet.get('excerpt_position') != '第二场开头摘录；不是全书开篇或完整场景'):
            raise ValueError('TWO_ROLE_PACKET_OR_SCOPE_DRIFT')
        if role == 'editor' and (packet.get('facts') != bound(root,manifest['facts_source'])['facts'] or
                packet.get('human_feedback') != [bound(root,route['previous_human_feedback'])['review']['human_exact_feedback'],runner.RETENTION_FEEDBACK] or
                packet.get('historical_material') != {'status':'NOT_TRANSMITTED_NO_WRITER_DIRECTIONS_OR_OTHER_REPORTS','text':''}):
            raise ValueError('TWO_ROLE_EDITOR_FACTS_OR_CONTEXT_DRIFT')
        runtime = check_runtime(root,route,manifest,role,packet)
        report = review.parse_report(bound(root,route[f'{role}_raw'],False))
        recomputed = runner.audit_reader(packet,report,runtime) if role == 'reader' else review.audit_report(packet,report,runtime)
        evidence = bound(root,route[f'{role}_evidence'])
        if recomputed['errors'] or any(evidence.get(k) != v for k,v in recomputed.items()):
            raise ValueError('TWO_ROLE_REPORT_OR_QUOTE_DRIFT')
        reports[role],runtimes[role] = report,runtime
    prior = project['r2_entry_short_trial']
    earlier_ids = {bound(root,prior[k])['thread_id'] for k in ('writer_runtime','facts_runtime')}
    earlier_ids.add(bound(root,project['emotion_pacing_learning']['runtime'])['thread_id'])
    if runtimes['reader']['thread_id'] == runtimes['editor']['thread_id'] or any(r['thread_id'] in earlier_ids for r in runtimes.values()):
        raise ValueError('TWO_ROLE_SHARED_OR_INHERITED_CONTEXT')
    settlement = bound(root,route['settlement'])
    editor = reports['editor']['results'][0]
    if (settlement.get('status') != 'TWO_ROLE_EVIDENCE_FACTS_AND_SCOPE_SETTLED_NO_HUMAN_PROMOTION' or
            settlement.get('raw_reports') != {role:route[f'{role}_raw'] for role in ('reader','editor')} or
            settlement.get('reader_wants_to_continue') != reports['reader']['wants_to_continue'] or
            settlement.get('human_wants_to_continue') is not False or settlement.get('human_quality_result') != 'FAIL' or
            settlement.get('raw_reports_rewritten') is not False or settlement.get('automatic_revision_authorized') is not False or
            settlement.get('known_failure_editor_diagnosis') is not True or settlement.get('reader_is_AI_not_actual_audience') is not True or
            settlement.get('reader_report_received_by_editor') is not False or settlement.get('editor_report_received_by_reader') is not False or
            settlement.get('previous_calibration') != {'false_negatives':2,'failure_count':2,'heldout_false_negatives':1,'heldout_failure_count':1,'same_scope_positive_count':0,'false_positive_rate':'NOT_ESTIMABLE'} or
            settlement.get('current_reader_case_is_new_heldout_validation') is not False or
            not settlement.get('disagreements') or not settlement.get('scope_decision')):
        raise ValueError('TWO_ROLE_COORDINATOR_SETTLEMENT_MISSING_OR_OVERCLAIMED')
    dispositions = settlement.get('editor_finding_dispositions',[])
    if len(dispositions) != len(editor['findings']): raise ValueError('TWO_ROLE_FINDING_NOT_SETTLED')
    facts = bound(root,project['r2_reentry_fact_preparation']['writer_context'])
    for original,item in zip(editor['findings'],dispositions):
        if (any(original[k] != item.get(k) for k in ('id','basis','quote','line')) or
                item.get('scope_checked') is not True or not item.get('coordinator_reason') or not item.get('fact_bindings') or
                item.get('disposition') not in ('ACCEPT_AS_LOCAL_EDITORIAL_HYPOTHESIS','PARTIAL_ACCEPT_LIMIT_SCOPE','REJECT_FACT_OR_SCOPE_ERROR')):
            raise ValueError('TWO_ROLE_FINDING_NOT_SETTLED')
        for f in item['fact_bindings']:
            if f.get('value') != facts.get(f.get('context_field')): raise ValueError('TWO_ROLE_EDITOR_FACT_MISREAD')
    checks = settlement.get('editor_window_quote_checks',[])
    if len(checks) != 3: raise ValueError('TWO_ROLE_EDITOR_WINDOW_EVIDENCE_MISSING')
    text = bound(root,route['target'],False).decode()
    for item in checks:
        original = editor['reading_expectations'][item['window']]
        offset = text.find(item.get('quote','')) if item.get('quote') else -1
        if (offset < 0 or original.get('quote') != item['quote'] or item.get('actual_line') != text[:offset].count('\n')+1 or
                item.get('start_character_0_based') != offset or item.get('interpretation') != 'EDITOR_HYPOTHESIS_NOT_HUMAN_TRACE'):
            raise ValueError('TWO_ROLE_EDITOR_WINDOW_QUOTE_DRIFT')
    prepared = bound(root,route['prepared_input'])
    proposal = bound(root,route['next_task_proposal'])
    if (prepared.get('based_on_frozen_context') != project['r2_reentry_fact_preparation']['writer_context'] or
            prepared.get('new_life_fact_count') != 0 or prepared.get('replacement_sentences') != [] or
            prepared.get('body_written') is not False or not prepared.get('single_entry_moment') or
            prepared.get('authoring_scope') != 'ONE_NEW_300_500_CHAR_SECOND_SCENE_OPENING_ONLY' or
            proposal.get('status') != 'PREPARED_NOT_AUTHORIZED' or proposal.get('prepared_input') != route['prepared_input'] or
            proposal.get('authorized_generation_budget') != 0 or proposal.get('proposed_generation_budget') != 1 or
            proposal.get('generation_count') != 0 or proposal.get('automatic_activation') is not False or
            proposal.get('old_197_character_protection_released') is not False or
            proposal.get('old_RC3_remaining_rounds') != 0 or proposal.get('multiple_candidates_allowed') is not False):
        raise ValueError('TWO_ROLE_PREPARATION_OR_UNAUTHORIZED_WRITING')
    writer = prepared.get('writer_packet',{})
    projected_facts = copy.deepcopy(facts)
    projected_facts['single_entry_moment'] = prepared['single_entry_moment']
    if (set(writer) != {'scope','facts','positive_craft_guidance'} or writer.get('facts') != projected_facts or
            writer.get('scope') != {'scene_id':'SP414-S02','output_count':1,'minimum_non_whitespace_characters':300,
                'maximum_non_whitespace_characters':500,'endpoint':facts['current_short_span_boundary']} or
            writer.get('positive_craft_guidance') != [
                '从人物正面对无法绕开的具体事情处进入，以他的注意与当下打算组织信息。',
                '让新认识引起个人反应，并实际影响接下来的回应或选择。',
                '金额和期限随当前需要出现，段尾保留尚未解除、与人物有关的问题。']):
        raise ValueError('TWO_ROLE_FUTURE_WRITER_FAILURE_OR_FACT_LEAKAGE')
    entries = prepared.get('entry_evidence',[])
    if len(entries) != 2: raise ValueError('TWO_ROLE_ENTRY_EVIDENCE_MISSING')
    for item in entries:
        offset = text.find(item.get('quote','')) if item.get('quote') else -1
        if item.get('artifact') != route['target'] or offset < 0 or item.get('line') != text[:offset].count('\n')+1:
            raise ValueError('TWO_ROLE_ENTRY_EVIDENCE_DRIFT')
    sources = bound(root,route['sources'])
    if (sources.get('external_skill_commit') != '0d5bf7fd987554e05db7e05d569736e648297722' or
            sources.get('adopted_skills') != ['story-review','reader-sim'] or len(sources.get('skill_resources',[])) != 5 or
            sources.get('external_code_executed') is not False or sources.get('actual_audience_research') is not False or
            sources.get('writing_transfer') != 'UNPROVEN' or len(sources.get('professional_opening_sources',[])) != 3):
        raise ValueError('TWO_ROLE_SKILL_OR_PROFESSIONAL_LEARNING_OVERCLAIM')
    for key in ('method_document','result_document'):
        if len(bound(root,route[key],False)) < 500: raise ValueError('TWO_ROLE_EMPTY_DOCUMENT')
    for value in (project,checkpoint):
        if (value.get('last_completed_task_id') != TASK or value.get('last_completed_task_contract') != route['task']['path'] or
                value.get('next_action') != NEXT or value.get('next_required_action') != NEXT or
                value.get('current_human_gate') != 'CURRENT_395_HUMAN_EMOTION_AI_SMELL_INTERACTION_AND_RETENTION_FAIL_OLD_448_FAIL_404_UNKNOWN'):
            raise ValueError('TWO_ROLE_LIVE_CURSOR_DRIFT')
    entry = (root/'START_HERE.md').read_text(encoding='utf-8')
    successor_entry = False
    later_entry = False
    if successor_human_feedback is not None:
        later = bound(root,successor_human_feedback)
        later_entry = (successor_human_feedback.get('path') == 'state/review_receipts/NOVEL_AUTONOMOUS_OPENING_390_HUMAN_FAIL_20261003.json' and
            later.get('source_checkpoint') == 199 and later.get('outcome') == 'FAIL' and
            later.get('output') == project.get('autonomous_opening_to_human',{}).get('final_artifact') and
            later.get('review',{}).get('source') == {'kind':'ACTUAL_CURRENT_USER_MESSAGE','message_observed_directly':True} and
            ('当前位置：检查点200。' in entry or '上一检查点200：' in entry) and '上一检查点199：' in entry)
    if successor_authorization is not None:
        successor = bound(root,successor_authorization)
        successor_entry = (successor_authorization.get('path') == 'state/review_receipts/NOVEL_AUTONOMOUS_TO_HUMAN_AUTHORIZATION_20261003.json' and
            successor.get('source_checkpoint') == 198 and successor.get('source') == 'ACTUAL_CURRENT_USER_MESSAGE' and
            successor.get('intermediate_user_authorization_required') is False and successor.get('authorized_primary_generation_budget') == 1 and
            successor.get('old_RC3_remaining_rounds') == 0 and successor.get('old_197_character_protection_released') is False and
            ('当前位置：检查点199。' in entry or later_entry))
    if checkpoint.get('sequence') != 198 or checkpoint.get('stop') is not True or TASK not in entry or NEXT not in entry or ('当前位置：检查点198。' not in entry and not successor_entry):
        raise ValueError('TWO_ROLE_CHECKPOINT_OR_ENTRY_DRIFT')
    return NEXT
