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
HUMAN_SOURCE='6753868be721f38e38387286217419b7a423ea40'
HUMAN_TASK='NOVEL-HOOK-TRIAL-401-HUMAN-PARTIAL-FEEDBACK-20261003-01'
HUMAN_EXACT='这个稍微好了一些。确实。'
HUMAN_NEXT='AWAIT_HUMAN_CONTINUATION_AND_INTERACTION_VERDICT_FOR_SAME_401_SHORT'
HUMAN_RECEIPT='state/review_receipts/NOVEL_HOOK_TRIAL_401_HUMAN_PARTIAL_FEEDBACK_20261003.json'
READING_SOURCE='9ba1ae731fb2b9a8a2879dbb332b11c4979bb33f'
READING_TASK='NOVEL-HOOK-TRIAL-401-HUMAN-WEAK-CONTINUATION-20261003-01'
READING_EXACT='有一点想继续的想法。但是不多哈。'
READING_NEXT='PREPARE_ONE_BOUNDED_300_500_CHAR_SAME_SCENE_CONTINUATION'
INTERACTION_EXACT='比之前自然，已不明显'
READING_RECEIPT='state/review_receipts/NOVEL_HOOK_TRIAL_401_HUMAN_WEAK_CONTINUATION_20261003.json'

def reading_historical_view(root,project,cp):
    feedback=project.get('hook_trial_human_feedback',{});record=feedback.get('reading_supplement')
    if not record or feedback!=cp.get('hook_trial_human_feedback'):raise ValueError('HOOK_READING_FEEDBACK_STATE_DRIFT')
    h=bound(root,record['receipt']);task=bound(root,record['task']);artifact=project['opening_hook_trial']['final_artifact']
    if (record.get('source_head')!=READING_SOURCE or record.get('task_id')!=READING_TASK or record.get('next_action')!=READING_NEXT or
        record['receipt'].get('path')!=READING_RECEIPT or h.get('task_id')!=READING_TASK or h.get('source_head')!=READING_SOURCE or
        h.get('source_checkpoint')!=202 or h.get('human_exact_feedback')!=READING_EXACT or h.get('output')!=artifact or
        h.get('outcome')!='SHORT_LIMITED_PASS' or h.get('prior_records_rewritten') is not False or h.get('prior_human_feedback')!=feedback['receipt'] or
        h.get('fact_raw_report')!=project['opening_hook_trial']['repair']['fact_raw_report'] or
        task.get('task_id')!=READING_TASK or task.get('receipt')!=record['receipt'] or task.get('status')!='COMPLETED_LIMITED_SHORT_FEEDBACK_AWAIT_BOUNDED_CONTINUATION_PREPARATION'):
        raise ValueError('HOOK_READING_FEEDBACK_IDENTITY_DRIFT')
    review=h.get('review',{})
    if (review.get('source')!={'kind':'ACTUAL_CURRENT_USER_MESSAGE','message_observed_directly':True} or review.get('human_exact_feedback')!=READING_EXACT or
        review.get('bound_artifact_path')!=artifact['path'] or review.get('bound_blob')!=artifact['blob'] or review.get('bound_sha256')!=artifact['sha256'] or
        review.get('wants_to_continue') is not True or review.get('continuation_strength')!='LOW_EXPLICITLY_QUALIFIED' or
        review.get('retention_verdict')!='WEAK_POSITIVE_NOT_FULL_ACCEPTANCE' or review.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED' or
        review.get('interaction_exact_feedback')!=INTERACTION_EXACT or review.get('robotic_interaction_verdict')!='POSITIVE_NOT_MARKEDLY_ROBOTIC_IN_THIS_SHORT' or
        review.get('interaction_source')!={'kind':'ACTUAL_CURRENT_USER_MESSAGES','identical_messages_observed':2,'independent_votes':1} or
        any(review.get(k)!='UNKNOWN_NOT_DIRECTLY_ANSWERED' for k in ('suspense_verdict','ai_smell_verdict','emotion_verdict')) or
        review.get('topic_rejection') is not False):raise ValueError('HOOK_WEAK_CONTINUATION_SCOPE_OR_STRENGTH_DRIFT')
    for v in (record,h,task):
        if (v.get('model_calls')!=0 or v.get('generation_count')!=0 or v.get('new_prose_authorized') is not False or
            v.get('old_RC3_remaining_rounds')!=0 or v.get('old_197_character_protection_released') is not False or v.get('human_quality_result')!='SHORT_LIMITED_PASS_WITH_LOW_CONTINUATION_STRENGTH' or
            v.get('full_scene_or_TEST01_promoted') is not False):
            raise ValueError('HOOK_WEAK_CONTINUATION_CANNOT_PROMOTE_OR_GENERATE')
    for v in (project,cp):
        if (v.get('last_completed_task_id')!=READING_TASK or v.get('last_completed_task_contract')!=record['task']['path'] or
            v.get('human_verdict_receipt')!=READING_RECEIPT or v.get('latest_human_review')!=review or v.get('next_action')!=READING_NEXT or
            v.get('next_required_action')!=READING_NEXT or v.get('current_human_gate')!='HOOK_TRIAL_LOCAL_SHORT_PASS_WITH_LOW_CONTINUATION_STRENGTH_FULL_SCENE_UNTESTED'):
            raise ValueError('HOOK_WEAK_CONTINUATION_LIVE_CURSOR_DRIFT')
    entry=(root/'START_HERE.md').read_text(encoding='utf-8')
    if cp.get('sequence')!=203 or cp.get('stop') is not True or READING_TASK not in entry or READING_NEXT not in entry or '当前位置：检查点203。' not in entry:
        raise ValueError('HOOK_WEAK_CONTINUATION_ENTRY_DRIFT')
    p,c=copy.deepcopy(project),copy.deepcopy(cp);prior=bound(root,feedback['receipt'])
    for v in (p,c):
        v['hook_trial_human_feedback'].pop('reading_supplement',None)
        v.update(last_completed_task_id=HUMAN_TASK,last_completed_task_contract=feedback['task']['path'],human_verdict_receipt=HUMAN_RECEIPT,
            latest_human_review=prior['review'],next_action=HUMAN_NEXT,next_required_action=HUMAN_NEXT,
            current_human_gate='HOOK_TRIAL_PARTIAL_POSITIVE_CONTINUATION_AND_INTERACTION_UNKNOWN')
    c.update(sequence=202,stop=True)
    return p,c

def human_feedback_view(root,project,cp,successor_reading_feedback=None):
    if project.get('hook_trial_human_feedback',{}).get('reading_supplement') or cp.get('hook_trial_human_feedback',{}).get('reading_supplement'):
        p,c=reading_historical_view(root,project,cp)
        return human_feedback_view(root,p,c,successor_reading_feedback=project['hook_trial_human_feedback']['reading_supplement']['receipt'])
    feedback=project.get('hook_trial_human_feedback')
    if not feedback or feedback!=cp.get('hook_trial_human_feedback'):raise ValueError('HOOK_HUMAN_FEEDBACK_STATE_DRIFT')
    receipt=bound(root,feedback['receipt']);task=bound(root,feedback['task']);route=project['opening_hook_trial']
    if (feedback.get('task_id')!=HUMAN_TASK or feedback.get('source_head')!=HUMAN_SOURCE or feedback.get('next_action')!=HUMAN_NEXT or
        receipt.get('source_head')!=HUMAN_SOURCE or receipt.get('source_checkpoint')!=201 or receipt.get('task_id')!=HUMAN_TASK or
        feedback['receipt'].get('path')!=HUMAN_RECEIPT or receipt.get('output')!=route['final_artifact'] or
        receipt.get('human_exact_feedback')!=HUMAN_EXACT or receipt.get('outcome')!='UNKNOWN' or
        receipt.get('prior_records_rewritten') is not False or task.get('task_id')!=HUMAN_TASK or
        task.get('receipt')!=feedback['receipt'] or task.get('status')!='COMPLETED_FEEDBACK_RECORDING_AWAIT_READING_VERDICT'):
        raise ValueError('HOOK_HUMAN_FEEDBACK_IDENTITY_DRIFT')
    review=receipt.get('review',{})
    if (review.get('source')!={'kind':'ACTUAL_CURRENT_USER_MESSAGE','message_observed_directly':True} or
        review.get('human_exact_feedback')!=HUMAN_EXACT or review.get('bound_artifact_path')!=route['final_artifact']['path'] or
        review.get('bound_blob')!=route['final_artifact']['blob'] or review.get('bound_sha256')!=route['final_artifact']['sha256'] or
        review.get('relative_improvement')!='SLIGHTLY_BETTER_UNSPECIFIED_DIMENSION' or review.get('wants_to_continue') is not None or
        any(review.get(k)!='UNKNOWN_NOT_DIRECTLY_ANSWERED' for k in ('retention_verdict','suspense_verdict','ai_smell_verdict','emotion_verdict','robotic_interaction_verdict')) or
        review.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED' or review.get('topic_rejection') is not False):
        raise ValueError('HOOK_PARTIAL_FEEDBACK_CANNOT_BECOME_QUALITY_VERDICT')
    for record in (feedback,receipt,task):
        if (record.get('model_calls')!=0 or record.get('generation_count')!=0 or record.get('new_prose_authorized') is not False or
            record.get('old_RC3_remaining_rounds')!=0 or record.get('old_197_character_protection_released') is not False):
            raise ValueError('HOOK_FEEDBACK_CANNOT_TRIGGER_GENERATION')
    for v in (project,cp):
        if (v.get('last_completed_task_id')!=HUMAN_TASK or v.get('last_completed_task_contract')!=feedback['task']['path'] or
            v.get('human_verdict_receipt')!=HUMAN_RECEIPT or v.get('latest_human_review')!=review or
            v.get('next_action')!=HUMAN_NEXT or v.get('next_required_action')!=HUMAN_NEXT or
            v.get('current_human_gate')!='HOOK_TRIAL_PARTIAL_POSITIVE_CONTINUATION_AND_INTERACTION_UNKNOWN'):
            raise ValueError('HOOK_PARTIAL_FEEDBACK_LIVE_CURSOR_DRIFT')
    entry=(root/'START_HERE.md').read_text(encoding='utf-8')
    successor_entry=False
    if successor_reading_feedback is not None:
        h=bound(root,successor_reading_feedback)
        successor_entry=(successor_reading_feedback.get('path')==READING_RECEIPT and h.get('source_head')==READING_SOURCE and
            h.get('source_checkpoint')==202 and h.get('human_exact_feedback')==READING_EXACT and h.get('output')==route['final_artifact'] and
            h.get('outcome')=='SHORT_LIMITED_PASS' and '当前位置：检查点203。' in entry and '上一检查点202：' in entry)
    if cp.get('sequence')!=202 or cp.get('stop') is not True or HUMAN_TASK not in entry or HUMAN_NEXT not in entry or ('当前位置：检查点202。' not in entry and not successor_entry):
        raise ValueError('HOOK_PARTIAL_FEEDBACK_ENTRY_DRIFT')
    p,c=copy.deepcopy(project),copy.deepcopy(cp);old_human=bound(root,route['human_feedback'])
    for v in (p,c):
        v.pop('hook_trial_human_feedback',None)
        v.update(last_completed_task_id=TASK,last_completed_task_contract=route['task']['path'],next_action=NEXT,next_required_action=NEXT,
            human_verdict_receipt=route['human_feedback']['path'],latest_human_review=old_human['review'],
            current_human_gate='HOOK_TRIAL_HUMAN_UNKNOWN_PRIOR_375_RETENTION_FAIL_AI_SMELL_RELATIVELY_IMPROVED')
    c.update(sequence=201,stop=True)
    return p,c,feedback['receipt']

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

def hook_action(root,project,cp,historical_action,successor_human_feedback=None):
    if 'hook_trial_human_feedback' in project or 'hook_trial_human_feedback' in cp:
        p,c,receipt=human_feedback_view(root,project,cp)
        if hook_action(root,p,c,historical_action,successor_human_feedback=receipt)!=NEXT:
            raise ValueError('HOOK_PARTIAL_FEEDBACK_CANNOT_SKIP_PRIOR_GATE')
        return READING_NEXT if project.get('hook_trial_human_feedback',{}).get('reading_supplement') else HUMAN_NEXT
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
    successor_entry=False
    if successor_human_feedback is not None:
        h=bound(root,successor_human_feedback)
        successor_entry=(successor_human_feedback.get('path')==HUMAN_RECEIPT and h.get('source_head')==HUMAN_SOURCE and
            h.get('source_checkpoint')==201 and h.get('human_exact_feedback')==HUMAN_EXACT and h.get('output')==route['final_artifact'] and
            h.get('outcome')=='UNKNOWN' and ('当前位置：检查点202。' in entry or
                ('当前位置：检查点203。' in entry and '上一检查点202：' in entry)) and '上一检查点201：' in entry)
    if cp.get('sequence')!=201 or cp.get('stop') is not True or TASK not in entry or NEXT not in entry or ('当前位置：检查点201。' not in entry and not successor_entry):
        raise ValueError('HOOK_CHECKPOINT_OR_ENTRY_DRIFT')
    return NEXT

prose_action=hook_action
