"""Evidence-bound continuation permission through the actual human reading gate."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

s=importlib.util.spec_from_file_location('autonomous_runner',Path(__file__).with_name('novel_autonomous_opening.py'))
runner=importlib.util.module_from_spec(s);s.loader.exec_module(runner)
review=runner.review
TASK,SOURCE=runner.TASK,runner.SOURCE
OLD='AWAIT_ONE_NEW_BOUNDED_WRITING_BUDGET_FOR_REVIEWED_OPENING_REENTRY_INPUT'
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_REVIEWED_NEW_OPENING'
STATUS='ONE_FINAL_FROZEN_SHORT_AND_INDEPENDENT_REVIEWS_SETTLED_AWAIT_HUMAN'


def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def bound(root,ref,as_json=True):
    p=(root/ref.get('path','')).resolve()
    if not ref.get('path') or not p.is_relative_to(root.resolve()) or not p.is_file():raise ValueError('AUTONOMOUS_MISSING_MATERIAL')
    b=p.read_bytes()
    if ref.get('blob')!=blob(b) or ref.get('sha256')!=hashlib.sha256(b).hexdigest():raise ValueError('AUTONOMOUS_IDENTITY_DRIFT')
    return json.loads(b) if as_json else b


def validate_authorization(root,project,checkpoint):
    route=project.get('autonomous_opening_to_human')
    if not route or route!=checkpoint.get('autonomous_opening_to_human'):raise ValueError('AUTONOMOUS_STATE_DRIFT')
    auth=bound(root,route['authorization']);manifest=bound(root,route['manifest'])
    previous=project.get('two_role_opening_review',{})
    if (route['authorization'].get('path')!=runner.AUTH or auth.get('task_id')!=TASK or auth.get('source_head')!=SOURCE or
            auth.get('source_checkpoint')!=198 or auth.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or
            auth.get('exact_user_instruction')!=runner.EXACT or auth.get('intermediate_user_authorization_required') is not False or
            auth.get('authorized_primary_generation_budget')!=1 or auth.get('authorized_maximum_internal_repairs')!=1 or
            auth.get('new_version_opening_reorganization_authorized') is not True or
            auth.get('old_artifacts_and_locks_must_remain_byte_identical') is not True or auth.get('old_RC3_remaining_rounds')!=0 or
            any(auth.get(k) is not False for k in ('old_197_character_protection_released','new_life_facts_authorized',
                'full_v5_authorized','multiple_visible_candidates_allowed','background_tasks_authorized',
                'goal_or_world_or_ending_change_authorized','human_quality_supplied_by_authorization')) or
            auth.get('authorized_proposal')!=previous.get('next_task_proposal') or auth.get('prepared_input')!=previous.get('prepared_input') or
            auth.get('previous_review_result')!=previous.get('result') or auth.get('previous_human_feedback')!=previous.get('human_feedback')):
        raise ValueError('AUTONOMOUS_USER_SCOPE_OR_STANDING_PERMISSION_DRIFT')
    proposal=bound(root,auth['authorized_proposal']);prepared=bound(root,auth['prepared_input'])
    if proposal.get('status')!='PREPARED_NOT_AUTHORIZED' or proposal.get('authorized_generation_budget')!=0 or proposal.get('proposed_generation_budget')!=1:
        raise ValueError('AUTONOMOUS_OLD_PROPOSAL_REWRITTEN')
    if (manifest.get('task_id')!=TASK or manifest.get('source_head')!=SOURCE or manifest.get('authorization')!=route['authorization'] or
            manifest.get('prepared_input')!=auth['prepared_input'] or manifest.get('authorized_proposal')!=auth['authorized_proposal'] or
            manifest.get('model')!='gpt-6.1-sol' or manifest.get('reasoning_effort')!='max' or
            manifest.get('primary_writer_limit')!=1 or manifest.get('evidenced_repair_limit')!=1 or
            manifest.get('review_calls_per_stage')!={'facts':1,'editor':1,'reader':1} or
            manifest.get('human_quality_result')!='UNKNOWN' or manifest.get('standalone_AI_quality_gate_allowed') is not False or
            manifest.get('automatic_verdict_retries') is not False):raise ValueError('AUTONOMOUS_MANIFEST_SCOPE_DRIFT')
    if manifest.get('review_policies',{}).get('facts')!={'kind':'BUILT_IN_FROZEN_PROTOCOL','sha256':hashlib.sha256(review.REVIEW_INSTRUCTIONS.encode()).hexdigest()}:
        raise ValueError('AUTONOMOUS_FACT_POLICY_DRIFT')
    runner.validate_writer_packet(bound(root,manifest['writer_input']),prepared)
    policy=bound(root,route['autonomy_policy'])
    if policy.get('authority')!=route['authorization'] or policy.get('intermediate_user_authorization_required') is not False:
        raise ValueError('AUTONOMOUS_ENTRY_PERMISSION_POLICY_DRIFT')
    return route['authorization']


def historical_two_role_view(root,project,checkpoint):
    auth=validate_authorization(root,project,checkpoint)
    p,c=copy.deepcopy(project),copy.deepcopy(checkpoint)
    old=p['two_role_opening_review']
    for v in (p,c):v.update(last_completed_task_id=old['task_id'],last_completed_task_contract=old['task']['path'],
        next_action=OLD,next_required_action=OLD,
        current_human_gate='CURRENT_395_HUMAN_EMOTION_AI_SMELL_INTERACTION_AND_RETENTION_FAIL_OLD_448_FAIL_404_UNKNOWN')
    c.update(sequence=198,stop=True)
    return p,c,auth


def runtime_check(root,reference,role,stage,packet,policy,raw):
    r=bound(root,reference);settings=r.get('resolved_thread_settings',{})
    if (r.get('task_id')!=TASK or r.get('role')!=role or r.get('stage')!=stage or
            r.get('packet')!=packet or r.get('raw_report')!=raw or r.get('status')!='RETURNED_RAW_OUTPUT_NOT_YET_SETTLED' or
            r.get('report_received') is not True or r.get('model_turn_dispatched') is not True or r.get('turn_status')!='completed' or
            r.get('repository_write_permission') is not False or r.get('tool_activity_detected')!=[] or r.get('model_initiated_requests')!=[] or
            r.get('isolation')!=runner.ISOLATION or not r.get('thread_id') or
            set(r.get('completed_item_types',[]))-{'userMessage','agentMessage','reasoning'} or r.get('completed_item_types',[]).count('agentMessage')!=1):
        raise ValueError('AUTONOMOUS_NO_COMPLETE_ISOLATED_CALL')
    if (settings.get('model')!='gpt-6.1-sol' or settings.get('reasoningEffort')!='max' or
            settings.get('sandbox')!={'type':'readOnly','networkAccess':False} or settings.get('approvalPolicy')!='never' or
            settings.get('instructionSources')!=[] or settings.get('runtimeWorkspaceRoots')!=[] or
            r.get('model_catalog_entry',{}).get('model')!='gpt-6.1-sol' or
            'max' not in {x.get('reasoningEffort') for x in r.get('model_catalog_entry',{}).get('supportedReasoningEfforts',[])} or
            r.get('prompt_policy_sha256')!=hashlib.sha256(policy).hexdigest()):raise ValueError('AUTONOMOUS_ACTUAL_MODEL_OR_ISOLATION_DRIFT')
    payload={'verified_runtime':{'model':'gpt-6.1-sol','reasoning_effort':'max','isolation':runner.ISOLATION},
        'writer_packet' if role=='writer' else 'review_packet':bound(root,packet)}
    if r.get('submitted_payload_sha256')!=hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest():raise ValueError('AUTONOMOUS_PAYLOAD_DRIFT')
    attempt=json.loads((root/runner.DIRECTORY/f'{stage}.{role}.attempt.json').read_bytes())
    if attempt.get('task_id')!=TASK or attempt.get('role')!=role or attempt.get('stage')!=stage or attempt.get('packet')!=packet or attempt.get('max_calls')!=1:
        raise ValueError('AUTONOMOUS_ATTEMPT_BUDGET_DRIFT')
    return r


def autonomous_action(root,project,checkpoint,historical_action,successor_human_feedback=None):
    if historical_action!=OLD:raise ValueError('AUTONOMOUS_CANNOT_SKIP_HISTORICAL_GATES')
    validate_authorization(root,project,checkpoint)
    route=project['autonomous_opening_to_human'];manifest=bound(root,route['manifest'])
    task=bound(root,route['task']);result=bound(root,route['result'])
    if (task.get('task_id')!=TASK or task.get('source_head')!=SOURCE or task.get('authorization')!=route['authorization'] or
            task.get('manifest')!=route['manifest'] or task.get('primary_writer_limit')!=1 or task.get('evidenced_repair_limit')!=1 or
            task.get('intermediate_user_authorization_required') is not False or task.get('visible_candidate_count')!=1):
        raise ValueError('AUTONOMOUS_TASK_CONTRACT_DRIFT')
    for v in (route,result):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('status')!=STATUS or v.get('primary_generation_count')!=1 or
                v.get('internal_repair_count') not in (0,1) or v.get('total_generation_count')!=1+v['internal_repair_count'] or
                v.get('remaining_primary_generation_budget')!=0 or v.get('visible_candidate_count')!=1 or
                v.get('old_RC3_remaining_rounds')!=0 or v.get('old_197_character_protection_released') is not False or
                v.get('full_v5_authorized') is not False or v.get('new_life_facts_authorized') is not False or
                v.get('human_quality_result')!='UNKNOWN' or v.get('literary_quality_validated') is not False or
                v.get('original_404_human_result')!='UNKNOWN' or v.get('prior_395_human_result')!='FAIL' or v.get('old_448_human_result')!='FAIL' or
                v.get('formal_mainline_method_revision')!=4 or v.get('intermediate_user_authorization_required') is not False or v.get('next_action')!=NEXT):
            raise ValueError('AUTONOMOUS_SCOPE_BUDGET_OR_HUMAN_PROMOTION')
    for k in ('authorization','manifest','autonomy_policy','primary_artifact','primary_runtime','stages','final_artifact',
            'settlement','pending_human_review','result_document'):
        if route.get(k)!=result.get(k):raise ValueError('AUTONOMOUS_RESULT_BINDING_DRIFT')
    expected_stages=['a1'] if route['internal_repair_count']==0 else ['a1','a2']
    if [x.get('stage') for x in route.get('stages',[])]!=expected_stages:raise ValueError('AUTONOMOUS_STAGE_BUDGET_DRIFT')
    primary=runtime_check(root,route['primary_runtime'],'writer','a1',manifest['writer_input'],bound(root,manifest['writer_policy'],False),route['primary_artifact'])
    if primary.get('generation_count')!=1:raise ValueError('AUTONOMOUS_PRIMARY_GENERATION_DRIFT')
    writer_ids=[primary['thread_id']];all_ids=[primary['thread_id']]
    prepared=bound(root,manifest['prepared_input']);facts=runner.fact_projection(prepared['writer_packet']['facts'])
    reports={}
    for stage in route['stages']:
        name=stage['stage'];body=bound(root,stage['artifact'],False);text=body.decode()
        count=sum(not c.isspace() for c in text)
        if not 300<=count<=500 or text.startswith('#') or '```' in text:raise ValueError('AUTONOMOUS_BODY_LENGTH_OR_FORMAT_DRIFT')
        frozen=bound(root,stage['review_manifest'])
        if frozen.get('task_id')!=TASK or frozen.get('stage')!=name or frozen.get('artifact')!=stage['artifact'] or set(frozen.get('jobs',{}))!={'facts','editor','reader'}:
            raise ValueError('AUTONOMOUS_REVIEW_MANIFEST_DRIFT')
        if name=='a2':
            repair=bound(root,route['repair_authorization']);packet=bound(root,stage['writer_input'])
            if (repair.get('task_id')!=TASK or repair.get('repair_index')!=1 or repair.get('evidence_verified') is not True or
                    repair.get('authorization')!=route['authorization'] or repair.get('source_artifact')!=route['primary_artifact'] or
                    repair.get('trigger') not in ('VERIFIED_FACT_CONFLICT','VERIFIED_HIGH_IMPACT_EDITORIAL_ISSUE','LENGTH_OR_FORMAT') or
                    repair.get('replacement_sentences')!=[] or not repair.get('selected_issue') or
                    packet.get('source_draft')!=bound(root,route['primary_artifact'],False).decode() or
                    packet.get('minimal_repair')!=repair.get('repair_direction') or
                    {k:packet.get(k) for k in ('scope','facts','positive_craft_guidance')}!=prepared['writer_packet'] or
                    set(packet)!={'scope','facts','positive_craft_guidance','source_draft','minimal_repair'}):
                raise ValueError('AUTONOMOUS_REPAIR_NOT_EVIDENCED_OR_SCOPE_DRIFT')
            wr=runtime_check(root,stage['writer_runtime'],'writer',name,stage['writer_input'],bound(root,stage['writer_policy'],False),stage['artifact'])
            writer_ids.append(wr['thread_id']);all_ids.append(wr['thread_id'])
        for role in ('facts','editor','reader'):
            job=frozen['jobs'][role];packet=bound(root,job['packet']);review.validate_packet(packet)
            if (job.get('max_calls')!=1 or packet.get('job_id')!=f'{role.upper()}199{name.upper()}' or
                    packet.get('work_kind')!={'facts':'FACT_AUDIT','editor':'EDITORIAL_REVIEW','reader':'COLD_SCREEN'}[role] or
                    packet.get('samples')!=[{'artifact_id':'A51','original_sha256':hashlib.sha256(body).hexdigest(),'text':text}] or
                    packet.get('medium')!='手机阅读的中文小说' or packet.get('excerpt_position')!='第二场开头摘录；不是全书开篇或完整场景' or
                    role!='reader' and packet.get('facts')!=facts):raise ValueError('AUTONOMOUS_REVIEW_SCOPE_OR_LABEL_LEAKAGE')
            if role=='editor' and packet.get('boundaries')!=['当前新稿尚无真人结果；本次是局部编辑审查，不是已知失败后的诊断。',
                    '只提出最小目标；不补新生活事实，不改变世界人物结局，不给替换句。']:
                raise ValueError('AUTONOMOUS_EDITOR_OLD_FAILURE_OR_ANSWER_LEAKAGE')
            policy=review.REVIEW_INSTRUCTIONS.encode() if role=='facts' else bound(root,manifest['review_policies'][role],False)
            runtime=runtime_check(root,stage[f'{role}_runtime'],role,name,job['packet'],policy,stage[f'{role}_raw'])
            all_ids.append(runtime['thread_id'])
            report=review.parse_report(bound(root,stage[f'{role}_raw'],False))
            recomputed=runner.roles.audit_reader(packet,report,runtime) if role=='reader' else review.audit_report(packet,report,runtime)
            saved=bound(root,stage[f'{role}_evidence'])
            if recomputed['errors'] or any(saved.get(k)!=v for k,v in recomputed.items()):raise ValueError('AUTONOMOUS_REPORT_OR_QUOTE_EVIDENCE_DRIFT')
            reports[(name,role)]=report
    old=project['two_role_opening_review']
    prior_ids={bound(root,old[k])['thread_id'] for k in ('reader_runtime','editor_runtime')}
    prior_ids.add(bound(root,project['r2_entry_short_trial']['writer_runtime'])['thread_id'])
    if len(all_ids)!=len(set(all_ids)) or prior_ids.intersection(all_ids):raise ValueError('AUTONOMOUS_SHARED_OR_INHERITED_CONTEXT')
    final=route['stages'][-1]
    if route.get('final_artifact')!=final['artifact']:raise ValueError('AUTONOMOUS_FINAL_ARTIFACT_DRIFT')
    settlement=bound(root,route['settlement']);pending=bound(root,route['pending_human_review'])
    if (settlement.get('status')!='ALL_FINAL_REPORTS_EVIDENCE_AND_FACTS_SETTLED_AWAIT_HUMAN' or settlement.get('final_artifact')!=route['final_artifact'] or
            settlement.get('raw_body_rewritten') is not False or settlement.get('raw_reports_rewritten') is not False or
            settlement.get('human_quality_result')!='UNKNOWN' or settlement.get('AI_quality_certification') is not False or
            settlement.get('fact_conflicts_unresolved')!=[] or settlement.get('reader_vote_triggers_more_generation') is not False or
            pending.get('artifact')!=route['final_artifact'] or pending.get('outcome')!='UNKNOWN' or pending.get('human_feedback')!={} or
            pending.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED' or pending.get('accepted') is not False):
        raise ValueError('AUTONOMOUS_SETTLEMENT_OR_UNKNOWN_HUMAN_DRIFT')
    if reports[(final['stage'],'facts')]['results'][0]['verdict']!='FACT_CLEAR':raise ValueError('AUTONOMOUS_FINAL_FACTS_NOT_CLEAR')
    if reports[(final['stage'],'editor')]['results'][0]['verdict']!='EDITORIAL_CLEAR':raise ValueError('AUTONOMOUS_FINAL_EDITOR_NOT_CLEAR')
    if settlement.get('final_reader_reaction')!=reports[(final['stage'],'reader')]['wants_to_continue'] or settlement.get('final_editor_verdict')!=reports[(final['stage'],'editor')]['results'][0]['verdict']:
        raise ValueError('AUTONOMOUS_VERDICT_REWRITTEN')
    dispositions=settlement.get('report_dispositions',[])
    expected_count=sum(len(r['results'][0]['findings']) for (stage,role),r in reports.items() if role!='reader')
    expected_ids={(stage,role,f['id']) for (stage,role),r in reports.items() if role!='reader' for f in r['results'][0]['findings']}
    if len(dispositions)!=expected_count or {(d.get('stage'),d.get('role'),d.get('id')) for d in dispositions}!=expected_ids:
        raise ValueError('AUTONOMOUS_FINDING_NOT_SETTLED')
    context=prepared['writer_packet']['facts']
    for item in dispositions:
        finding=next((f for f in reports[(item['stage'],item['role'])]['results'][0]['findings'] if f['id']==item.get('id')),None)
        if (not finding or any(item.get(k)!=finding.get(k) for k in ('basis','quote','line')) or item.get('scope_checked') is not True or
                not item.get('coordinator_reason') or not item.get('fact_bindings')):raise ValueError('AUTONOMOUS_FINDING_NOT_SETTLED')
        for f in item['fact_bindings']:
            if f.get('context_field') not in context or f.get('value')!=context[f['context_field']]:raise ValueError('AUTONOMOUS_FACT_BINDING_DRIFT')
    windows=settlement.get('editor_window_quote_checks',[])
    if len(windows)!=3*len(expected_stages):raise ValueError('AUTONOMOUS_EDITOR_WINDOW_EVIDENCE_MISSING')
    for item in windows:
        body=bound(root,next(x['artifact'] for x in route['stages'] if x['stage']==item['stage']),False).decode()
        original=reports[(item['stage'],'editor')]['results'][0]['reading_expectations'][item['window']]
        offset=body.find(item.get('quote','')) if item.get('quote') else -1
        if (offset<0 or original.get('quote')!=item['quote'] or item.get('actual_line')!=body[:offset].count('\n')+1 or
                item.get('start_character_0_based')!=offset or item.get('interpretation')!='AI_EDITOR_HYPOTHESIS_NOT_HUMAN_TRACE'):
            raise ValueError('AUTONOMOUS_EDITOR_WINDOW_QUOTE_DRIFT')
    text=bound(root,route['final_artifact'],False).decode()
    checks=settlement.get('text_fact_checks',[])
    if len(checks)!=9 or len({x.get('dimension') for x in checks})!=9:raise ValueError('AUTONOMOUS_FACT_CHECK_COVERAGE_MISSING')
    for check in checks:
        offset=text.find(check.get('quote','')) if check.get('quote') else -1
        if offset<0 or check.get('line')!=text[:offset].count('\n')+1 or check.get('disposition')!='CLEAR' or not check.get('interpretation') or not check.get('fact_bindings'):
            raise ValueError('AUTONOMOUS_TEXT_FACT_CHECK_DRIFT')
        for f in check['fact_bindings']:
            if f.get('context_field') not in context or f.get('value')!=context[f['context_field']]:raise ValueError('AUTONOMOUS_FACT_BINDING_DRIFT')
    for v in (project,checkpoint):
        if (v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=route['task']['path'] or
                v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or
                v.get('current_human_gate')!='NEW_REVIEWED_OPENING_HUMAN_UNKNOWN_PRIOR_395_AND_448_FAIL_404_UNKNOWN'):
            raise ValueError('AUTONOMOUS_LIVE_CURSOR_DRIFT')
    entry=(root/'START_HERE.md').read_text(encoding='utf-8')
    successor_entry=False
    if successor_human_feedback is not None:
        actual=bound(root,successor_human_feedback)
        successor_entry=(successor_human_feedback.get('path')=='state/review_receipts/NOVEL_AUTONOMOUS_OPENING_390_HUMAN_FAIL_20261003.json' and
            actual.get('source_checkpoint')==199 and actual.get('outcome')=='FAIL' and actual.get('output')==route['final_artifact'] and
            actual.get('review',{}).get('source',{}).get('kind')=='ACTUAL_CURRENT_USER_MESSAGE' and '当前位置：检查点200。' in entry)
    if checkpoint.get('sequence')!=199 or checkpoint.get('stop') is not True or TASK not in entry or NEXT not in entry or ('当前位置：检查点199。' not in entry and not successor_entry):
        raise ValueError('AUTONOMOUS_CHECKPOINT_OR_ENTRY_DRIFT')
    return NEXT
