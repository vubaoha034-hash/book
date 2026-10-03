"""Verify a genuine retention failure and one independently reviewed hook trial."""
from __future__ import annotations
import copy,hashlib,importlib.util,json
from pathlib import Path
def module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
runner=module('hook_runner','novel_hook_trial.py')
common=module('hook_common','verify_prose_repair.py')
review=runner.review
bound,blob=common.bound,common.blob
TASK,SOURCE=runner.TASK,runner.SOURCE
OLD=common.NEXT
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_HOOK_TRIAL_SHORT'

def validate_failure(root,project,cp):
    route=project.get('opening_hook_trial')
    if not route or route!=cp.get('opening_hook_trial'):raise ValueError('HOOK_STATE_DRIFT')
    h=bound(root,route['human_feedback']);auth=bound(root,route['authorization']);old=project['opening_prose_repair']
    if (route['human_feedback'].get('path')!=runner.HUMAN or h.get('source_head')!=SOURCE or h.get('source_checkpoint')!=200 or
        h.get('human_exact_feedback')!=runner.EXACT or h.get('outcome')!='FAIL' or h.get('output')!=old['final_artifact'] or
        h.get('prior_result_and_pending_record_rewritten') is not False):raise ValueError('HOOK_ACTUAL_REJECTION_DRIFT')
    v=h.get('review',{})
    if (v.get('source')!={'kind':'ACTUAL_CURRENT_USER_MESSAGE','message_observed_directly':True} or v.get('human_exact_feedback')!=runner.EXACT or
        v.get('bound_artifact_path')!=old['final_artifact']['path'] or v.get('bound_blob')!=old['final_artifact']['blob'] or
        v.get('bound_sha256')!=old['final_artifact']['sha256'] or v.get('wants_to_continue') is not False or v.get('retention_verdict')!='FAIL' or
        v.get('ai_smell_verdict')!='RELATIVE_IMPROVEMENT_NOT_A_FULL_PASS' or v.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED' or
        v.get('emotion_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or v.get('robotic_interaction_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or
        v.get('topic_rejection') is not False):raise ValueError('HOOK_HUMAN_SCOPE_OR_STOP_INVENTED')
    standing=bound(root,auth['standing_user_authorization'])
    if (auth.get('task_id')!=TASK or auth.get('source_head')!=SOURCE or auth.get('source_checkpoint')!=200 or
        auth.get('human_feedback')!=route['human_feedback'] or auth.get('rejected_artifact')!=old['final_artifact'] or
        auth.get('source')!='STANDING_USER_AUTONOMY_AND_ACTUAL_FROZEN_TEST_FAILURE' or
        standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False or
        auth.get('intermediate_user_authorization_required') is not False or auth.get('primary_writer_limit')!=1 or
        auth.get('maximum_evidenced_repairs')!=1 or auth.get('old_RC3_remaining_rounds')!=0 or
        any(auth.get(k) is not False for k in ('old_197_character_protection_released','new_life_facts_authorized','full_v5_authorized',
            'multiple_visible_candidates_allowed','background_tasks_authorized','goal_or_world_or_ending_change_authorized'))):
        raise ValueError('HOOK_STANDING_SCOPE_PERMISSION_DRIFT')
    return route['human_feedback']

def historical_prose_view(root,project,cp):
    feedback=validate_failure(root,project,cp)
    p,c=copy.deepcopy(project),copy.deepcopy(cp);old=p['opening_prose_repair'];h=bound(root,old['human_feedback'])
    for v in (p,c):
        v.pop('opening_hook_trial',None)
        v.update(last_completed_task_id=old['task_id'],last_completed_task_contract=old['task']['path'],
            next_action=OLD,next_required_action=OLD,human_verdict_receipt=old['human_feedback']['path'],latest_human_review=h['review'],
            current_human_gate='PROSE_REPAIRED_NEW_SHORT_HUMAN_UNKNOWN_PRIOR_390_FAIL_OLD_FAILURES_PRESERVED')
    c.update(sequence=200,stop=True)
    return p,c,feedback

def runtime_check(root,ref,role,job):
    old_runner=common.runner;old_directory=runner.DIRECTORY;old_task=common.TASK
    common.runner=runner;common.TASK=TASK;runner.DIRECTORY=str(Path(ref['path']).parent).replace('\\','/')
    try:return common.runtime_check(root,ref,role,job)
    finally:common.runner=old_runner;common.TASK=old_task;runner.DIRECTORY=old_directory

def hook_action(root,project,cp,historical_action):
    if historical_action!=OLD:raise ValueError('HOOK_CANNOT_SKIP_HISTORICAL_GATES')
    validate_failure(root,project,cp);route=project['opening_hook_trial'];result=bound(root,route['result']);m=bound(root,route['manifest'])
    task=bound(root,route['task'])
    if task.get('task_id')!=TASK or task.get('authorization')!=route['authorization']:raise ValueError('HOOK_TASK_DRIFT')
    for v in (route,result):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('primary_generation_count')!=1 or v.get('internal_repair_count')!=1 or
            v.get('visible_candidate_count')!=1 or v.get('human_quality_result')!='UNKNOWN' or v.get('previous_375_human_result')!='FAIL' or
            v.get('old_RC3_remaining_rounds')!=0 or v.get('old_197_character_protection_released') is not False or
            v.get('literary_quality_validated') is not False or v.get('full_v5_authorized') is not False or v.get('next_action')!=NEXT):
            raise ValueError('HOOK_BUDGET_OR_HUMAN_PROMOTION')
    for k in ('authorization','manifest','human_feedback','writer_input','initial_artifact','final_artifact','repair','settlement','pending_human_review','runtimes','raw_reports','evidence','result_document'):
        if result.get(k)!=route.get(k):raise ValueError('HOOK_RESULT_BINDING_DRIFT')
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('authorization')!=route['authorization'] or
        m.get('generation_limit')!=1 or m.get('quality_certification_allowed') is not False or set(m.get('jobs',{}))!={'diagnosis','writer','facts','editor','reader'}):
        raise ValueError('HOOK_MANIFEST_DRIFT')
    recovery=bound(root,m['transport_failure']);failed=bound(root,recovery['failed_runtime']);bound(root,recovery['failed_attempt'])
    if (m.get('transport_recovery_limit')!=1 or failed.get('report_received') is not False or failed.get('turn_status')!='failed' or
        failed.get('completed_item_types')!=['userMessage'] or recovery.get('no_prompt_tuning_or_quality_vote_retry') is not True or
        result.get('actual_model_calls')!=8 or result.get('successful_model_calls')!=7):raise ValueError('HOOK_TRANSPORT_FAILURE_NOT_A_QUALITY_RETRY')
    writer=bound(root,route['writer_input']);old=project['opening_prose_repair'];old_writer=bound(root,old['writer_input'])
    if writer.get('facts')!=old_writer['facts'] or len(writer.get('positive_craft_guidance',[]))!=3:raise ValueError('HOOK_NEW_LIFE_FACT_OR_PILED_WRITER_RULES')
    if set(writer)!={'scope','facts','positive_craft_guidance'} or any(k in json.dumps(writer,ensure_ascii=False) for k in ('FAIL','刘先生','findings','human_feedback','EDITORIAL_CLEAR')):
        raise ValueError('HOOK_WRITER_ANSWER_LEAKAGE')
    body=bound(root,route['initial_artifact'],False);text=body.decode();old_body=bound(root,old['final_artifact'],False)
    if not 300<=sum(not c.isspace() for c in text)<=500 or text.startswith('#') or '```' in text:raise ValueError('HOOK_BODY_SCOPE_DRIFT')
    reports={};ids=[]
    frozen_facts=bound(root,bound(root,old['manifest'])['jobs']['facts']['packet'])['facts']
    for role,job in m['jobs'].items():
        packet=bound(root,job['packet'])
        if role!='writer':review.validate_packet(packet)
        rt=runtime_check(root,route['runtimes'][role],role,job);ids.append(rt['thread_id'])
        if rt['raw_report']!=(route['initial_artifact'] if role=='writer' else route['raw_reports'][role]):raise ValueError('HOOK_RAW_BINDING_DRIFT')
        if role=='writer':continue
        expected=old_body if role=='diagnosis' else body
        if packet['samples']!=[{'artifact_id':'F60' if role=='diagnosis' else 'N61','original_sha256':hashlib.sha256(expected).hexdigest(),'text':expected.decode()}]:
            raise ValueError('HOOK_REVIEW_WRONG_ARTIFACT')
        if packet['work_kind']!={'diagnosis':'POST_FAILURE_DIAGNOSIS','facts':'FACT_AUDIT','editor':'EDITORIAL_REVIEW','reader':'COLD_SCREEN'}[role]:raise ValueError('HOOK_REVIEW_WORK_KIND_DRIFT')
        if role=='diagnosis' and packet.get('human_feedback')!=runner.EXACT:raise ValueError('HOOK_DIAGNOSIS_IS_KNOWN_FAILURE')
        if role in ('diagnosis','facts','editor') and packet.get('facts')!=frozen_facts:
            raise ValueError('HOOK_REVIEW_FROZEN_FACT_DRIFT')
        report=review.parse_report(bound(root,route['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,rt) if role=='reader' else review.audit_report(packet,report,rt)
        saved=bound(root,route['evidence'][role])
        if audit['errors'] or any(saved.get(k)!=v for k,v in audit.items()):raise ValueError('HOOK_REPORT_OR_QUOTE_EVIDENCE_DRIFT')
    prior={bound(root,v)['thread_id'] for v in old['runtimes'].values()}
    if len(set(ids))!=5 or prior.intersection(ids) or failed.get('thread_id') in ids:raise ValueError('HOOK_SHARED_CONTEXT')
    if reports['diagnosis']['results'][0]['verdict']!='REVISE' or reports['facts']['results'][0]['verdict']!='FACT_CLEAR':raise ValueError('HOOK_UNSETTLED_DIAGNOSIS_OR_FACTS')
    if reports['editor']['results'][0]['verdict'] not in ('EDITORIAL_CLEAR','REVISE'):raise ValueError('HOOK_EDITOR_MATERIAL_OR_RUNTIME_NOT_SETTLED')
    repair=route['repair'];rm=bound(root,repair['manifest']);plan=bound(root,rm['repair_plan'])
    final=bound(root,route['final_artifact'],False);final_text=final.decode()
    expected=text.replace('我明天下午也得交一万二','我明天下午前也得交一万二')
    if (text.count('我明天下午也得交一万二')!=1 or final_text!=expected or
        plan.get('primary_artifact')!=route['initial_artifact'] or plan.get('internal_repair_limit')!=1 or
        plan.get('quality_vote_did_not_trigger_repair') is not True or plan.get('required_output_sha256')!=hashlib.sha256(final).hexdigest() or
        repair.get('editor_and_reader_scope')!='INITIAL_400_CHARACTER_BODY_ONLY_FINAL_SINGLE_CHARACTER_FACT_REPAIR_NOT_REASSESSED'):
        raise ValueError('HOOK_REPAIR_SCOPE_OR_RAW_IDENTITY_DRIFT')
    for role in ('writer','facts'):
        rt=runtime_check(root,repair['runtimes'][role],role,rm['jobs'][role]);ids.append(rt['thread_id'])
        if role=='writer':
            packet=bound(root,rm['jobs'][role]['packet'])
            if packet.get('facts')!={'current_text':text,'deposit_deadline':frozen_facts['xucheng_own_life']['ordinary_plan']} or rt.get('raw_report')!=route['final_artifact']:
                raise ValueError('HOOK_REPAIR_WRITER_PACKET_DRIFT')
        else:
            packet=bound(root,rm['jobs'][role]['packet']);review.validate_packet(packet)
            if (packet.get('work_kind')!='FACT_AUDIT' or packet.get('facts')!=frozen_facts or
                packet['samples']!=[{'artifact_id':'N62','original_sha256':hashlib.sha256(final).hexdigest(),'text':final_text}]):
                raise ValueError('HOOK_REPAIR_FACT_PACKET_DRIFT')
            report=review.parse_report(bound(root,repair['fact_raw_report'],False));audit=review.audit_report(packet,report,rt)
            saved=bound(root,repair['fact_evidence'])
            if report['results'][0]['verdict']!='FACT_CLEAR' or audit['errors'] or any(saved.get(k)!=v for k,v in audit.items()):
                raise ValueError('HOOK_REPAIRED_FACTS_NOT_SETTLED')
    if len(set(ids))!=7 or prior.intersection(ids):raise ValueError('HOOK_SHARED_CONTEXT')
    settlement=bound(root,route['settlement']);pending=bound(root,route['pending_human_review'])
    if (settlement.get('final_artifact')!=route['final_artifact'] or settlement.get('raw_reports_rewritten') is not False or
        settlement.get('raw_body_rewritten') is not False or settlement.get('human_quality_result')!='UNKNOWN' or settlement.get('AI_quality_certification') is not False or
        settlement.get('reader_vote_triggers_more_generation') is not False or settlement.get('fact_conflicts_unresolved')!=[] or
        pending.get('artifact')!=route['final_artifact'] or pending.get('outcome')!='UNKNOWN' or pending.get('human_feedback')!={} or
        pending.get('accepted') is not False or pending.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED'):
        raise ValueError('HOOK_SETTLEMENT_OR_HUMAN_UNKNOWN_DRIFT')
    findings={(r,f['id']) for r,report in reports.items() if r!='reader' for f in report['results'][0]['findings']}
    items=settlement.get('finding_dispositions',[])
    if len(items)!=len(findings) or {(v.get('role'),v.get('id')) for v in items}!=findings:raise ValueError('HOOK_FINDING_NOT_SETTLED')
    for item in items:
        f=next(f for f in reports[item['role']]['results'][0]['findings'] if f['id']==item['id'])
        if any(item.get(k)!=f.get(k) for k in ('basis','quote','line')) or item.get('scope_checked') is not True or not item.get('coordinator_reason'):
            raise ValueError('HOOK_FINDING_NOT_SETTLED')
    final_findings=report['results'][0]['findings']
    final_items=settlement.get('final_fact_finding_dispositions',[])
    if len(final_items)!=len(final_findings) or {v.get('id') for v in final_items}!={v['id'] for v in final_findings}:
        raise ValueError('HOOK_FINAL_FACT_FINDING_NOT_SETTLED')
    for item in final_items:
        finding=next(v for v in final_findings if v['id']==item['id'])
        if any(item.get(k)!=finding.get(k) for k in ('basis','quote','line')) or item.get('scope_checked') is not True or not item.get('coordinator_reason'):
            raise ValueError('HOOK_FINAL_FACT_FINDING_NOT_SETTLED')
    windows=settlement.get('editor_window_quote_checks',[])
    if len(windows)!=3:raise ValueError('HOOK_EDITOR_WINDOW_MISSING')
    for w in windows:
        original=reports['editor']['results'][0]['reading_expectations'][w['window']];offset=text.find(w.get('quote','')) if w.get('quote') else -1
        if offset<0 or original['quote']!=w['quote'] or w.get('actual_line')!=text[:offset].count('\n')+1 or w.get('start_character_0_based')!=offset:
            raise ValueError('HOOK_EDITOR_WINDOW_QUOTE_DRIFT')
    facts=frozen_facts;checks=settlement.get('manual_fact_checks',[])
    if not checks or len({v.get('dimension') for v in checks})!=len(checks):raise ValueError('HOOK_MANUAL_FACT_CHECK_MISSING')
    for item in checks:
        off=final_text.find(item.get('quote','')) if item.get('quote') else -1;field=item.get('fact_source_field')
        if off<0 or item.get('line')!=final_text[:off].count('\n')+1 or field not in facts or item.get('source_value')!=facts[field] or item.get('disposition')!='CLEAR':
            raise ValueError('HOOK_MANUAL_FACT_EVIDENCE_DRIFT')
    for v in (project,cp):
        if (v.get('last_completed_task_id')!=TASK or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or
            v.get('human_verdict_receipt')!=route['human_feedback']['path'] or v.get('latest_human_review')!=bound(root,route['human_feedback'])['review'] or
            v.get('current_human_gate')!='HOOK_TRIAL_HUMAN_UNKNOWN_PRIOR_375_RETENTION_FAIL_AI_SMELL_RELATIVELY_IMPROVED'):
            raise ValueError('HOOK_LIVE_CURSOR_OR_ACTUAL_FEEDBACK_DRIFT')
    entry=(root/'START_HERE.md').read_text(encoding='utf-8')
    if cp.get('sequence')!=201 or cp.get('stop') is not True or TASK not in entry or NEXT not in entry or '当前位置：检查点201。' not in entry:
        raise ValueError('HOOK_CHECKPOINT_OR_ENTRY_DRIFT')
    return NEXT

prose_action=hook_action
