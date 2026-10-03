"""Validate actual rejection, one scoped prose revision and isolated reports."""
from __future__ import annotations
import copy,hashlib,importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('prose_runner',Path(__file__).with_name('novel_prose_repair.py'))
runner=importlib.util.module_from_spec(s);s.loader.exec_module(runner)
review=runner.review
TASK,SOURCE=runner.TASK,runner.SOURCE
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_PROSE_REPAIRED_OPENING'
OLD='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_REVIEWED_NEW_OPENING'


def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def bound(root,ref,as_json=True):
    path=(root/ref.get('path','')).resolve()
    if not ref.get('path') or not path.is_relative_to(root.resolve()) or not path.is_file():raise ValueError('PROSE_MISSING_MATERIAL')
    b=path.read_bytes()
    if ref.get('blob')!=blob(b) or ref.get('sha256')!=hashlib.sha256(b).hexdigest():raise ValueError('PROSE_IDENTITY_DRIFT')
    return json.loads(b) if as_json else b


def validate_failure(root,project,checkpoint):
    route=project.get('opening_prose_repair')
    if not route or route!=checkpoint.get('opening_prose_repair'):raise ValueError('PROSE_STATE_DRIFT')
    auth=bound(root,route['authorization']);h=bound(root,route['human_feedback']);old=project['autonomous_opening_to_human']
    if (route['human_feedback'].get('path')!=runner.HUMAN or h.get('source_head')!=SOURCE or h.get('source_checkpoint')!=199 or
        h.get('human_exact_feedback')!=runner.EXACT or h.get('outcome')!='FAIL' or h.get('output')!=old['final_artifact'] or
        h.get('prior_result_and_pending_record_rewritten') is not False):raise ValueError('PROSE_ACTUAL_REJECTION_DRIFT')
    v=h.get('review',{})
    if (v.get('human_exact_feedback')!=runner.EXACT or v.get('bound_artifact_path')!=old['final_artifact']['path'] or
        v.get('bound_blob')!=old['final_artifact']['blob'] or v.get('bound_sha256')!=old['final_artifact']['sha256'] or
        v.get('source')!={'kind':'ACTUAL_CURRENT_USER_MESSAGE','message_observed_directly':True} or
        v.get('wants_to_continue') is not False or v.get('ai_smell_verdict')!='FAIL' or v.get('opening_prose_verdict')!='FAIL' or
        v.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED' or v.get('human_location_description')!='开头开始就很重' or
        v.get('robotic_interaction_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or v.get('emotion_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or
        v.get('topic_rejection') is not False):raise ValueError('PROSE_HUMAN_SCOPE_OR_STOP_INVENTED')
    standing=bound(root,auth['standing_user_authorization'])
    if (route['authorization'].get('path')!=runner.AUTH or auth.get('task_id')!=TASK or auth.get('source_head')!=SOURCE or
        auth.get('human_feedback')!=route['human_feedback'] or auth.get('rejected_artifact')!=h['output'] or
        auth.get('standing_user_authorization')!=old['authorization'] or auth.get('prior_result')!=old['result'] or
        auth.get('source')!='STANDING_USER_AUTONOMY_AND_ACTUAL_FROZEN_TEST_FAILURE' or
        standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False or
        auth.get('intermediate_user_authorization_required') is not False or auth.get('primary_writer_limit')!=1 or
        auth.get('maximum_evidenced_repairs')!=1 or auth.get('old_RC3_remaining_rounds')!=0 or
        auth.get('old_197_character_protection_released') is not False or auth.get('new_life_facts_authorized') is not False or
        auth.get('full_v5_authorized') is not False):raise ValueError('PROSE_STANDING_SCOPE_PERMISSION_DRIFT')
    return route['human_feedback']


def historical_autonomous_view(root,project,checkpoint):
    feedback=validate_failure(root,project,checkpoint)
    p,c=copy.deepcopy(project),copy.deepcopy(checkpoint);old=p['autonomous_opening_to_human']
    prior_feedback=p['two_role_opening_review']['human_feedback'];prior=bound(root,prior_feedback)
    for v in (p,c):
        v.pop('opening_prose_repair',None)
        v.update(last_completed_task_id=old['task_id'],last_completed_task_contract=old['task']['path'],
            next_action=OLD,next_required_action=OLD,human_verdict_receipt=prior_feedback['path'],latest_human_review=prior['review'],
            current_human_gate='NEW_REVIEWED_OPENING_HUMAN_UNKNOWN_PRIOR_395_AND_448_FAIL_404_UNKNOWN')
    c.update(sequence=199,stop=True)
    return p,c,feedback


def runtime_check(root,reference,role,job):
    r=bound(root,reference);cfg=r.get('resolved_thread_settings',{})
    if (r.get('task_id')!=TASK or r.get('role')!=role or r.get('packet')!=job['packet'] or r.get('report_received') is not True or
        r.get('status')!='RETURNED_RAW_OUTPUT_NOT_YET_SETTLED' or r.get('turn_status')!='completed' or
        r.get('model_turn_dispatched') is not True or r.get('repository_write_permission') is not False or
        r.get('tool_activity_detected')!=[] or r.get('model_initiated_requests')!=[] or not r.get('thread_id') or
        r.get('completed_item_types',[]).count('agentMessage')!=1 or set(r.get('completed_item_types',[]))-{'reasoning','userMessage','agentMessage'} or
        cfg.get('model')!='gpt-6.1-sol' or cfg.get('reasoningEffort')!='max' or cfg.get('approvalPolicy')!='never' or
        cfg.get('sandbox')!={'type':'readOnly','networkAccess':False} or cfg.get('instructionSources')!=[] or cfg.get('runtimeWorkspaceRoots')!=[] or
        r.get('isolation')!=runner.ISOLATION or r.get('model_catalog_entry',{}).get('model')!='gpt-6.1-sol' or
        'max' not in {v.get('reasoningEffort') for v in r.get('model_catalog_entry',{}).get('supportedReasoningEfforts',[])}):
        raise ValueError('PROSE_NO_ACTUAL_ISOLATED_SOL_MAX_RESULT')
    packet=bound(root,job['packet']);policy=bound(root,job['policy'],False)
    payload={'verified_runtime':{'model':'gpt-6.1-sol','reasoning_effort':'max','isolation':runner.ISOLATION},
        'writer_packet' if role=='writer' else 'review_packet':packet}
    if (job.get('max_calls')!=1 or r.get('prompt_policy_sha256')!=hashlib.sha256(policy).hexdigest() or
        r.get('submitted_payload_sha256')!=hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest() or
        r.get('raw_report',{}).get('path')!=job.get('raw_path')):raise ValueError('PROSE_PAYLOAD_OR_CALL_BUDGET_DRIFT')
    attempt=json.loads((root/runner.DIRECTORY/f'{role}.attempt.json').read_bytes())
    if attempt.get('task_id')!=TASK or attempt.get('max_calls')!=1 or attempt.get('packet')!=job['packet']:raise ValueError('PROSE_ONE_CALL_MARKER_DRIFT')
    bound(root,r['raw_report'],False)
    if r.get('generation_count')!=(1 if role=='writer' else 0):raise ValueError('PROSE_RUNTIME_GENERATION_COUNT_DRIFT')
    return r


def prose_action(root,project,checkpoint,historical_action):
    if historical_action!=OLD:raise ValueError('PROSE_CANNOT_SKIP_HISTORICAL_GATES')
    validate_failure(root,project,checkpoint)
    route=project['opening_prose_repair'];manifest=bound(root,route['manifest']);result=bound(root,route['result'])
    task=bound(root,route['task'])
    if task.get('task_id')!=TASK or task.get('authorization')!=route['authorization']:raise ValueError('PROSE_TASK_DRIFT')
    for v in (route,result):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('primary_generation_count')!=1 or v.get('internal_repair_count')!=0 or
            v.get('visible_candidate_count')!=1 or v.get('human_quality_result')!='UNKNOWN' or v.get('previous_390_human_result')!='FAIL' or
            v.get('old_RC3_remaining_rounds')!=0 or v.get('old_197_character_protection_released') is not False or
            v.get('full_v5_authorized') is not False or v.get('literary_quality_validated') is not False or
            v.get('intermediate_user_authorization_required') is not False or v.get('next_action')!=NEXT):
            raise ValueError('PROSE_BUDGET_OR_HUMAN_PROMOTION')
    for k in ('authorization','manifest','human_feedback','writer_input','final_artifact','settlement','pending_human_review','runtimes','raw_reports','evidence','result_document'):
        if route.get(k)!=result.get(k):raise ValueError('PROSE_RESULT_BINDING_DRIFT')
    if (manifest.get('task_id')!=TASK or manifest.get('source_head')!=SOURCE or manifest.get('authorization')!=route['authorization'] or
        manifest.get('generation_limit')!=1 or manifest.get('quality_certification_allowed') is not False or
        set(manifest.get('jobs',{}))!={'diagnosis','writer','facts','editor','reader'}):raise ValueError('PROSE_MANIFEST_DRIFT')
    writer=bound(root,route['writer_input']);old=project['autonomous_opening_to_human']
    old_input=bound(root,bound(root,old['manifest'])['writer_input'])
    selected=['setting','previous_scene','single_entry_moment','rojun_current_intention','rojun_memory_and_responsibility',
        'xucheng_private_state','xucheng_own_life','shared_obligation','known_time_boundary','viewpoint_and_knowledge','material_boundary']
    if writer['facts']!={k:old_input['facts'][k] for k in selected} or len(writer.get('positive_craft_guidance',[]))!=3:
        raise ValueError('PROSE_NEW_LIFE_FACT_OR_PILED_WRITER_RULES')
    if set(writer)!={'scope','facts','positive_craft_guidance'} or any(x in json.dumps(writer,ensure_ascii=False) for x in ('FAIL','刘先生','findings','human_feedback','EDITORIAL_CLEAR')):
        raise ValueError('PROSE_WRITER_ANSWER_LEAKAGE')
    body=bound(root,route['final_artifact'],False);text=body.decode()
    if not 300<=sum(not c.isspace() for c in text)<=500 or text.startswith('#') or '```' in text:raise ValueError('PROSE_BODY_SCOPE_DRIFT')
    ids=[];reports={}
    for role,job in manifest['jobs'].items():
        if role!='writer':
            packet=bound(root,job['packet']);review.validate_packet(packet)
        runtime=runtime_check(root,route['runtimes'][role],role,job);ids.append(runtime['thread_id'])
        if runtime['raw_report']!=(route['final_artifact'] if role=='writer' else route['raw_reports'][role]):raise ValueError('PROSE_RAW_BINDING_DRIFT')
        if role=='writer':continue
        if packet.get('work_kind')!={'diagnosis':'POST_FAILURE_DIAGNOSIS','facts':'FACT_AUDIT','editor':'EDITORIAL_REVIEW','reader':'COLD_SCREEN'}[role]:
            raise ValueError('PROSE_REVIEW_WORK_KIND_DRIFT')
        expected=bound(root,old['final_artifact'],False) if role=='diagnosis' else body
        if packet['samples']!=[{'artifact_id':'F52' if role=='diagnosis' else 'N53','original_sha256':hashlib.sha256(expected).hexdigest(),'text':expected.decode()}]:
            raise ValueError('PROSE_REVIEW_WRONG_ARTIFACT')
        if role=='diagnosis' and packet['human_feedback']!=runner.EXACT:raise ValueError('PROSE_DIAGNOSIS_IS_KNOWN_FAILURE')
        if role in ('facts','editor'):
            expected_facts=bound(root,bound(root,old['stages'][0]['review_manifest'])['jobs']['facts']['packet'])['facts']
            expected_facts['short_span_endpoint']=writer['scope']['endpoint']
            if packet.get('facts')!=expected_facts:raise ValueError('PROSE_REVIEW_FROZEN_FACT_DRIFT')
        report=review.parse_report(bound(root,route['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,runtime) if role=='reader' else review.audit_report(packet,report,runtime)
        saved=bound(root,route['evidence'][role])
        if audit['errors'] or any(saved.get(k)!=v for k,v in audit.items()):raise ValueError('PROSE_REPORT_OR_QUOTE_EVIDENCE_DRIFT')
    prior_ids={bound(root,old['primary_runtime'])['thread_id']}
    prior_ids.update(bound(root,old['stages'][0][role+'_runtime'])['thread_id'] for role in ('facts','editor','reader'))
    if len(ids)!=len(set(ids)) or prior_ids.intersection(ids):raise ValueError('PROSE_SHARED_CONTEXT')
    if reports['diagnosis']['results'][0]['verdict']!='REVISE' or reports['facts']['results'][0]['verdict']!='FACT_CLEAR':
        raise ValueError('PROSE_UNSETTLED_DIAGNOSIS_OR_FACTS')
    if reports['editor']['results'][0]['verdict'] not in ('EDITORIAL_CLEAR','REVISE'):
        raise ValueError('PROSE_EDITOR_MATERIAL_OR_RUNTIME_NOT_SETTLED')
    settlement=bound(root,route['settlement']);pending=bound(root,route['pending_human_review'])
    if (settlement.get('final_artifact')!=route['final_artifact'] or settlement.get('raw_reports_rewritten') is not False or
        settlement.get('human_quality_result')!='UNKNOWN' or settlement.get('AI_quality_certification') is not False or
        settlement.get('reader_vote_triggers_more_generation') is not False or settlement.get('fact_conflicts_unresolved')!=[] or
        pending.get('artifact')!=route['final_artifact'] or pending.get('outcome')!='UNKNOWN' or pending.get('human_feedback')!={} or
        pending.get('accepted') is not False or pending.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED'):
        raise ValueError('PROSE_SETTLEMENT_OR_HUMAN_UNKNOWN_DRIFT')
    expected_findings={(role,f['id']) for role,report in reports.items() if role!='reader' for f in report['results'][0]['findings']}
    items=settlement.get('finding_dispositions',[])
    if len(items)!=len(expected_findings) or {(v.get('role'),v.get('id')) for v in items}!=expected_findings:
        raise ValueError('PROSE_FINDING_NOT_SETTLED')
    for item in items:
        f=next(f for f in reports[item['role']]['results'][0]['findings'] if f['id']==item['id'])
        if any(item.get(k)!=f.get(k) for k in ('basis','quote','line')) or not item.get('coordinator_reason') or item.get('scope_checked') is not True:
            raise ValueError('PROSE_FINDING_NOT_SETTLED')
    windows=settlement.get('editor_window_quote_checks',[])
    if len(windows)!=3:raise ValueError('PROSE_EDITOR_WINDOW_MISSING')
    for w in windows:
        original=reports['editor']['results'][0]['reading_expectations'][w['window']]
        offset=text.find(w.get('quote','')) if w.get('quote') else -1
        if offset<0 or original.get('quote')!=w['quote'] or w.get('actual_line')!=text[:offset].count('\n')+1 or w.get('start_character_0_based')!=offset:
            raise ValueError('PROSE_EDITOR_WINDOW_QUOTE_DRIFT')
    checks=settlement.get('manual_fact_checks',[])
    dimensions={'ENTRY_AND_CARRIER','PROPERTY_INTENTION','NO_MEMORY_OR_ACKNOWLEDGEMENT','AMOUNT_AND_DUE',
        'HER_OWN_PLAN','CONDITIONAL_RISK','ASSISTANCE_TIME','INDEPENDENT_START','UNRESOLVED_ENDPOINT'}
    if len(checks)!=9 or {v.get('dimension') for v in checks}!=dimensions:
        raise ValueError('PROSE_MANUAL_FACT_CHECK_MISSING')
    frozen_facts=bound(root,manifest['jobs']['facts']['packet'])['facts']
    for item in checks:
        offset=text.find(item.get('quote','')) if item.get('quote') else -1
        field=item.get('fact_source_field')
        if (offset<0 or item.get('line')!=text[:offset].count('\n')+1 or field not in frozen_facts or
            item.get('source_value')!=frozen_facts[field] or item.get('disposition')!='CLEAR' or not item.get('coordinator_reason')):
            raise ValueError('PROSE_MANUAL_FACT_EVIDENCE_DRIFT')
    for v in (project,checkpoint):
        if (v.get('last_completed_task_id')!=TASK or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or
            v.get('human_verdict_receipt')!=route['human_feedback']['path'] or v.get('latest_human_review')!=bound(root,route['human_feedback'])['review'] or
            v.get('current_human_gate')!='PROSE_REPAIRED_NEW_SHORT_HUMAN_UNKNOWN_PRIOR_390_FAIL_OLD_FAILURES_PRESERVED'):
            raise ValueError('PROSE_LIVE_CURSOR_OR_ACTUAL_FEEDBACK_DRIFT')
    entry=(root/'START_HERE.md').read_text(encoding='utf-8')
    if checkpoint.get('sequence')!=200 or checkpoint.get('stop') is not True or TASK not in entry or NEXT not in entry or '当前位置：检查点200。' not in entry:
        raise ValueError('PROSE_CHECKPOINT_OR_ENTRY_DRIFT')
    return NEXT
