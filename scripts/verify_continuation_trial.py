"""Bind one continuation to its unchanged prefix and actual isolated reviews.

This checks saved evidence and scope, never literary quality or user taste.
"""
from __future__ import annotations
import copy,hashlib,importlib.util,json
from pathlib import Path
def module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
runner=module('continuation_runner','novel_continuation_trial.py')
hook=module('continuation_hook','verify_hook_trial.py')
common=hook.common
bound,blob=common.bound,common.blob
TASK,SOURCE=runner.TASK,runner.SOURCE
OLD=hook.READING_NEXT
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_CONTINUATION_SHORT'
GATE='CONTINUATION_SHORT_HUMAN_UNKNOWN_PREFIX_WEAK_POSITIVE_FULL_SCENE_UNTESTED'
WRITER_SCOPE='只写紧接已给上段之后的一份300—500字接续；输出新段正文，不重复或改写上段。仍是同一第二场局部摘录，至多开始独立核验，不给结果、认账、付款或恢复关系。'
CURRENT_MOMENT='承接上段末尾：罗钧已经输入合同公司名，还没提交搜索；设备款、本期期限、许澄自己的押金安排及她三点离开的有限协助已由她说出。他仍无第二过去的主观记忆。'
ENDPOINT='承接已给上段末尾，至多开始独立查证，不给核验结果、认账、付款或恢复关系；仅审当前短段，不是完整场景。'

def validate_authorization(root,project,cp):
    route=project.get('continuation_short_trial')
    if not route or route!=cp.get('continuation_short_trial'):raise ValueError('CONTINUATION_STATE_DRIFT')
    a=bound(root,route['authorization']);h=bound(root,a['opening_human_feedback']);standing=bound(root,a['standing_user_authorization'])
    opening=project['opening_hook_trial'];supplement=project['hook_trial_human_feedback']['reading_supplement']
    if (route['authorization'].get('path')!=runner.AUTH or a.get('task_id')!=TASK or a.get('source_head')!=SOURCE or a.get('source_checkpoint')!=203 or
        a.get('source')!='STANDING_USER_AUTONOMY_FOR_ONE_BOUNDED_SAME_SCENE_CONTINUATION' or
        a.get('scope')!='ONE_300_500_CHARACTER_CONTINUATION_AFTER_UNCHANGED_401_OPENING_SAME_SECOND_SCENE' or
        a.get('previous_excerpt')!=opening['final_artifact'] or a.get('opening_human_feedback')!=supplement['receipt'] or
        a.get('standing_user_authorization')!=bound(root,opening['authorization'])['standing_user_authorization'] or
        a.get('primary_writer_limit')!=1 or a.get('maximum_evidenced_repairs')!=1 or a.get('new_segment_character_range')!=[300,500] or
        a.get('intermediate_user_authorization_required') is not False or a.get('old_RC3_remaining_rounds')!=0 or
        any(a.get(k) is not False for k in ('old_197_character_protection_released','new_life_facts_authorized','full_v5_authorized',
            'full_scene_or_TEST01_promoted','multiple_visible_candidates_allowed','background_tasks_authorized','goal_or_world_or_ending_change_authorized')) or
        standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False or
        h.get('output')!=a['previous_excerpt'] or h.get('outcome')!='SHORT_LIMITED_PASS' or
        h.get('human_exact_feedback')!=hook.READING_EXACT or h.get('review',{}).get('interaction_exact_feedback')!=hook.INTERACTION_EXACT or
        h.get('review',{}).get('continuation_strength')!='LOW_EXPLICITLY_QUALIFIED'):
        raise ValueError('CONTINUATION_PERMISSION_OR_PREFIX_DRIFT')
    b=bound(root,a['previous_excerpt'],False)
    if hashlib.sha256(b).hexdigest()!='38c768aa19195482896b3a0433d7cc2b1cc86aee120b8b93c984d48dfb4ff1c9':
        raise ValueError('CONTINUATION_ACCEPTED_PREFIX_CHANGED')
    return route['authorization']

def historical_hook_view(root,project,cp):
    auth=validate_authorization(root,project,cp)
    p,c=copy.deepcopy(project),copy.deepcopy(cp);record=p['hook_trial_human_feedback']['reading_supplement'];h=bound(root,record['receipt'])
    for v in (p,c):
        v.pop('continuation_short_trial',None)
        v.update(last_completed_task_id=hook.READING_TASK,last_completed_task_contract=record['task']['path'],
            human_verdict_receipt=hook.READING_RECEIPT,latest_human_review=h['review'],next_action=OLD,next_required_action=OLD,
            current_human_gate='HOOK_TRIAL_LOCAL_SHORT_PASS_WITH_LOW_CONTINUATION_STRENGTH_FULL_SCENE_UNTESTED')
    c.update(sequence=203,stop=True)
    return p,c,auth

def runtime_check(root,ref,role,job):
    old_runner,old_task,old_dir=common.runner,common.TASK,runner.DIRECTORY
    common.runner,common.TASK=runner,TASK;runner.DIRECTORY=str(Path(ref['path']).parent).replace('\\','/')
    try:return common.runtime_check(root,ref,role,job)
    finally:common.runner,common.TASK,runner.DIRECTORY=old_runner,old_task,old_dir

def continuation_action(root,project,cp,historical_action):
    if historical_action!=OLD:raise ValueError('CONTINUATION_CANNOT_SKIP_HISTORICAL_GATES')
    validate_authorization(root,project,cp)
    r=project['continuation_short_trial'];result=bound(root,r['result']);m=bound(root,r['manifest']);task=bound(root,r['task']);a=bound(root,r['authorization'])
    for v in (r,result,task):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('primary_generation_count')!=1 or v.get('internal_repair_count')!=0 or
            v.get('visible_candidate_count')!=1 or v.get('human_quality_result')!='UNKNOWN' or v.get('actual_model_calls')!=4 or
            v.get('successful_model_calls')!=4 or v.get('remaining_new_generation_budget')!=0 or v.get('remaining_internal_repair_budget')!=0 or
            v.get('old_RC3_remaining_rounds')!=0 or v.get('next_action')!=NEXT or v.get('status')!='ONE_CONTINUATION_FROZEN_REVIEW_SETTLED_AWAIT_ACTUAL_HUMAN_READING' or
            any(v.get(k) is not False for k in ('old_197_character_protection_released','full_v5_authorized','full_scene_or_TEST01_promoted','literary_quality_validated','automatic_background_sync','automatic_writer_dispatch'))):
            raise ValueError('CONTINUATION_BUDGET_OR_HUMAN_PROMOTION')
    keys=('authorization','manifest','previous_excerpt','opening_human_feedback','writer_input','final_artifact','reading_copy','settlement','pending_human_review','runtimes','raw_reports','evidence','result_document')
    for k in keys:
        if r.get(k)!=result.get(k) or r.get(k)!=task.get(k):raise ValueError('CONTINUATION_RESULT_BINDING_DRIFT')
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('authorization')!=r['authorization'] or m.get('generation_limit')!=1 or
        m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or m.get('quality_certification_allowed') is not False or
        m.get('maximum_evidenced_repairs')!=1 or set(m.get('jobs',{}))!={'writer','facts','editor','reader'} or
        m.get('previous_excerpt')!=a['previous_excerpt'] or r['previous_excerpt']!=a['previous_excerpt'] or
        r['opening_human_feedback']!=a['opening_human_feedback'] or m.get('reading_copy')!=r['reading_copy']):raise ValueError('CONTINUATION_MANIFEST_DRIFT')
    body=bound(root,r['final_artifact'],False);text=body.decode();prefix=bound(root,r['previous_excerpt'],False)
    if not 300<=sum(not c.isspace() for c in text)<=500 or text.startswith('#') or '```' in text or prefix.decode() in text:
        raise ValueError('CONTINUATION_BODY_SCOPE_DRIFT')
    assembled=prefix+b'\n\n'+body
    if bound(root,r['reading_copy'],False)!=assembled:raise ValueError('CONTINUATION_READING_COPY_NOT_EXACT_CONCATENATION')
    writer=bound(root,r['writer_input']);old=project['opening_hook_trial'];old_writer=bound(root,old['writer_input'])
    expected=copy.deepcopy(old_writer['facts']);expected.update(previous_excerpt=prefix.decode(),current_moment=CURRENT_MOMENT)
    if (set(writer)!={'scope','facts','positive_craft_guidance'} or writer.get('scope')!=WRITER_SCOPE or writer.get('facts')!=expected or
        len(writer.get('positive_craft_guidance',[]))!=3 or any(k in json.dumps(writer,ensure_ascii=False) for k in ('FAIL','刘先生','findings','human_feedback','EDITORIAL_CLEAR'))):
        raise ValueError('CONTINUATION_WRITER_ANSWER_OR_NEW_FACT_LEAKAGE')
    frozen=copy.deepcopy(bound(root,bound(root,old['manifest'])['jobs']['facts']['packet'])['facts'])
    frozen.update(previous_excerpt=prefix.decode(),current_moment=CURRENT_MOMENT,short_span_endpoint=ENDPOINT)
    reports={};ids=[]
    for role,job in m['jobs'].items():
        packet=bound(root,job['packet']);rt=runtime_check(root,r['runtimes'][role],role,job);ids.append(rt['thread_id'])
        if rt['raw_report']!=(r['final_artifact'] if role=='writer' else r['raw_reports'][role]):raise ValueError('CONTINUATION_RAW_BINDING_DRIFT')
        if role=='writer':continue
        runner.review.validate_packet(packet)
        expected_text=assembled.decode() if role=='reader' else text
        if packet.get('work_kind')!={'facts':'FACT_AUDIT','editor':'EDITORIAL_REVIEW','reader':'COLD_SCREEN'}[role] or packet['samples']!=[{
            'artifact_id':'CN72' if role=='reader' else 'CN71','original_sha256':hashlib.sha256(expected_text.encode()).hexdigest(),'text':expected_text}]:
            raise ValueError('CONTINUATION_REVIEW_WRONG_ARTIFACT')
        if role in ('facts','editor') and packet.get('facts')!=frozen:raise ValueError('CONTINUATION_REVIEW_FROZEN_FACT_DRIFT')
        if role=='reader' and any(k in json.dumps(packet,ensure_ascii=False) for k in ('刘先生','human_feedback','FACT_CLEAR','已认可','已失败')):
            raise ValueError('CONTINUATION_COLD_KNOWN_ANSWER_LEAKAGE')
        if bound(root,job['policy'],False)!=(root/f'delivery/hook-trial-20261003/{role}-policy.txt').read_bytes():raise ValueError('CONTINUATION_REVIEW_POLICY_DRIFT')
        report=runner.review.parse_report(bound(root,r['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,rt) if role=='reader' else runner.review.audit_report(packet,report,rt)
        saved=bound(root,r['evidence'][role])
        if audit['errors'] or any(saved.get(k)!=v for k,v in audit.items()):raise ValueError('CONTINUATION_REPORT_OR_QUOTE_EVIDENCE_DRIFT')
    prior_ids={bound(root,v)['thread_id'] for v in old['runtimes'].values()}
    if len(set(ids))!=4 or prior_ids.intersection(ids):raise ValueError('CONTINUATION_SHARED_CONTEXT')
    if reports['facts']['results'][0]['verdict']!='FACT_CLEAR' or reports['editor']['results'][0]['verdict'] not in ('EDITORIAL_CLEAR','REVISE'):
        raise ValueError('CONTINUATION_MISSING_OR_INSUFFICIENT_REVIEW_CANNOT_PASS')
    s=bound(root,r['settlement']);pending=bound(root,r['pending_human_review'])
    if (s.get('final_artifact')!=r['final_artifact'] or s.get('raw_reports_rewritten') is not False or s.get('human_quality_result')!='UNKNOWN' or
        s.get('AI_quality_certification') is not False or s.get('reader_vote_triggers_more_generation') is not False or
        s.get('fact_conflicts_unresolved')!=[] or s.get('high_impact_unresolved')!=[] or s.get('coordinator_prose_edits')!=0 or
        pending.get('artifact')!=r['final_artifact'] or pending.get('reading_copy')!=r['reading_copy'] or pending.get('outcome')!='UNKNOWN' or
        pending.get('human_feedback')!={} or pending.get('accepted') is not False or pending.get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED'):
        raise ValueError('CONTINUATION_SETTLEMENT_OR_UNKNOWN_DRIFT')
    findings={(role,f['id']) for role in ('facts','editor') for f in reports[role]['results'][0]['findings']}
    items=s.get('finding_dispositions',[])
    if len(items)!=len(findings) or {(v.get('role'),v.get('id')) for v in items}!=findings:raise ValueError('CONTINUATION_FINDING_NOT_SETTLED')
    for item in items:
        f=next(f for f in reports[item['role']]['results'][0]['findings'] if f['id']==item['id'])
        if any(item.get(k)!=f.get(k) for k in ('basis','quote','line')) or not item.get('coordinator_reason') or item.get('scope_checked') is not True:
            raise ValueError('CONTINUATION_FINDING_NOT_SETTLED')
    windows=s.get('editor_window_quote_checks',[])
    if len(windows)!=3 or {w.get('window') for w in windows}!={'first_30_60','first_150_300','ending'}:raise ValueError('CONTINUATION_EDITOR_WINDOW_MISSING')
    for w in windows:
        original=reports['editor']['results'][0]['reading_expectations'][w['window']];offset=text.find(w.get('quote','')) if w.get('quote') else -1
        if offset<0 or original['quote']!=w['quote'] or w.get('actual_line')!=text[:offset].count('\n')+1 or w.get('start_character_0_based')!=offset:
            raise ValueError('CONTINUATION_EDITOR_WINDOW_QUOTE_DRIFT')
    checks=s.get('manual_fact_checks',[])
    if len(checks)<5 or len({v.get('dimension') for v in checks})!=len(checks):raise ValueError('CONTINUATION_MANUAL_FACT_CHECK_MISSING')
    for item in checks:
        off=text.find(item.get('quote','')) if item.get('quote') else -1;field=item.get('fact_source_field')
        if off<0 or item.get('line')!=text[:off].count('\n')+1 or field not in frozen or item.get('source_value')!=frozen[field] or item.get('disposition')!='CLEAR' or not item.get('coordinator_reason'):
            raise ValueError('CONTINUATION_MANUAL_FACT_EVIDENCE_DRIFT')
    bound(root,r['result_document'],False)
    for v in (project,cp):
        if v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=r['task']['path'] or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or v.get('current_human_gate')!=GATE:
            raise ValueError('CONTINUATION_LIVE_CURSOR_DRIFT')
        if v.get('human_verdict_receipt')!=a['opening_human_feedback']['path'] or v.get('latest_human_review')!=bound(root,a['opening_human_feedback'])['review']:
            raise ValueError('CONTINUATION_PREVIOUS_HUMAN_FEEDBACK_DRIFT')
    entry=(root/'START_HERE.md').read_text(encoding='utf-8')
    if cp.get('sequence')!=204 or cp.get('stop') is not True or '当前位置：检查点204。' not in entry or '上一检查点203：' not in entry or TASK not in entry or NEXT not in entry:
        raise ValueError('CONTINUATION_ENTRY_DRIFT')
    return NEXT
