"""Validate the one local repair, scoped human feedback and untouched history."""
from __future__ import annotations
import copy,hashlib,importlib.util,json
from pathlib import Path
def module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
runner=module('clarity_runner','novel_clarity_repair.py');prior=module('clarity_prior','verify_story_trial.py');history=prior.history
bound,blob=prior.bound,prior.blob
SOURCE='897e756b6248e24e29c10dbdf742f8274c1b3ba9';TASK='NOVEL-NEW-STORY-REFERENT-ACTION-CLARITY-REPAIR-20261004-01'
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_CLARITY_REPAIRED_SHORT'
EXACT='有，但是你自己检查下，这整片文章写的多乱。我甚至不知道到底是谁在做什么。我拿起她搭在椅背上的外套，伸手牵她。妈端着汤过来：“他难得回来，你这就往外跑？”\n“明早要喝，怕店关了。”\n我替女儿套上外套，拉着她往门口走。弟弟也放下筷子，拿起了门边的车钥匙。比如这句，我看了半天都没看懂这是什么人在做什么。'
MUTABLE=('AGENTS.md','README.md','SKILL.md','START_HERE.md','scripts/verify_current_state.py','state/project_state.json','state/continuity/LATEST_CHECKPOINT.json','tests/test_story_trial.py')
LIVE_KEYS=prior.LIVE_KEYS|{'clarity_repair'}
_baseline=None
def baseline_checks(root,p,c):
    global _baseline
    source=history.frozen_tree(Path(__file__).resolve().parents[1],SOURCE)
    bp=json.loads((source/'state/project_state.json').read_bytes());bc=json.loads((source/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    if _baseline is None:_baseline=prior.verify(source,bp,bc)
    if _baseline['sequence']!=205 or _baseline['new_prose_authorized'] is not False:raise ValueError('CLARITY_INVALID_BASELINE')
    for live,old in [(p,bp),(c,bc)]:
        if {k:v for k,v in live.items() if k not in LIVE_KEYS}!={k:v for k,v in old.items() if k not in LIVE_KEYS}:raise ValueError('CLARITY_HISTORICAL_STATE_DRIFT')
    if p.get('closed_task_ids')!=bp['closed_task_ids']+[TASK]:raise ValueError('CLARITY_CLOSED_TASK_GUARD_DRIFT')
    if {k:v for k,v in c['action_guard'].items() if k not in ('closed_task_ids','project_state_sha256')}!={k:v for k,v in bc['action_guard'].items() if k not in ('closed_task_ids','project_state_sha256')}:raise ValueError('CLARITY_OLD_ACTION_GUARD_CHANGED')
    files=[v.relative_to(source).as_posix() for v in source.rglob('*') if v.is_file() and '__pycache__' not in v.parts and v.relative_to(source).as_posix() not in MUTABLE]
    for name in files:
        if not(root/name).is_file() or (root/name).read_bytes()!=(source/name).read_bytes():raise ValueError('CLARITY_HISTORICAL_FILE_CHANGED: '+name)
    return _baseline,len(files)
def runtime_check(root,ref,role,job,directory):
    old=(prior.common.TASK,prior.common.runner)
    prior.common.TASK,prior.common.runner=TASK,runner.engine;runner.engine.DIRECTORY=directory
    try:return prior.common.runtime_check(root,ref,role,job)
    finally:prior.common.TASK,prior.common.runner=old
def verify(root,p,c):
    r=p.get('clarity_repair')
    if not r or r!=c.get('clarity_repair'):raise ValueError('CLARITY_STATE_DRIFT')
    baseline,protected=baseline_checks(root,p,c)
    a,h,m,t,result,s=[bound(root,r[k]) for k in ('authorization','human_feedback','manifest','task','result','settlement')]
    if (a.get('authority',{}).get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or a['authority'].get('exact_message')!=h.get('human_exact_feedback') or h.get('human_exact_feedback')!=EXACT or
        a.get('task_id')!=TASK or a.get('source_head')!=SOURCE or a.get('scope')!='ONE_LOCAL_CLARITY_REPAIR_OF_SAME_NEW_STORY_SHORT_ONLY' or
        a.get('repair_limit')!=1 or a.get('source_artifact')!=p['story_replacement_trial']['final_artifact'] or
        a.get('human_feedback')!=r['human_feedback'] or a.get('old_RC3_remaining_rounds')!=0 or
        any(a.get(k) is not False for k in ('old_197_character_protection_released','new_plot_or_life_facts_authorized','full_scene_or_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized')) or
        a.get('protected_paragraph_indices_0_based')!=list(range(1,6)) or a.get('modifiable_paragraph_indices_0_based')!=[0,*range(6,13)] or
        h.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or h.get('output')!=a['source_artifact'] or h.get('outcome')!='INTEREST_YES_CLARITY_FAIL' or
        h.get('source_head')!=SOURCE or h.get('source_checkpoint')!=205 or h.get('prior_records_rewritten') is not False or
        h['review'].get('wants_to_continue') is not True or h['review'].get('clarity_verdict')!='FAIL_CANNOT_FOLLOW_ACTORS_AND_ACTIONS' or
        h['review'].get('ai_smell_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or h['review'].get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED'):
        raise ValueError('CLARITY_PERMISSION_OR_HUMAN_SCOPE_DRIFT')
    keys=('authorization','human_feedback','manifest','source_artifact','writer_input','final_artifact','settlement','pending_human_review','runtimes','raw_reports','evidence','result_document')
    for v in (r,t,result):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('primary_generation_count')!=0 or v.get('local_repair_count')!=1 or
            v.get('visible_candidate_count')!=1 or v.get('actual_model_calls')!=3 or v.get('successful_model_calls')!=3 or v.get('human_quality_result')!='UNKNOWN' or
            v.get('next_action')!=NEXT or v.get('remaining_repair_budget')!=0 or v.get('old_RC3_remaining_rounds')!=0 or
            any(v.get(k) is not False for k in ('old_197_character_protection_released','new_plot_or_life_facts_authorized','full_scene_or_TEST01_promoted','literary_quality_validated','automatic_writer_dispatch','automatic_background_sync'))):raise ValueError('CLARITY_BUDGET_OR_HUMAN_PROMOTION')
        if any(v.get(k)!=r.get(k) for k in keys):raise ValueError('CLARITY_RESULT_BINDING_DRIFT')
    old_body=bound(root,r['source_artifact'],False).decode();body=bound(root,r['final_artifact'],False).decode();before=old_body.split('\n\n');after=body.split('\n\n')
    if len(before)!=13 or len(after)!=13 or any(before[i]!=after[i] for i in (*range(1,6),12)) or not 300<=sum(not c.isspace() for c in body)<=500:raise ValueError('CLARITY_REPAIR_OUTSIDE_PROTECTED_SCOPE')
    source_facts=bound(root,p['story_replacement_trial']['writer_input'])['facts'];writer=bound(root,r['writer_input'])
    if (set(writer)!={'scope','facts','positive_craft_guidance'} or writer.get('facts')!={**source_facts,'source_text':old_body} or
        len(writer.get('positive_craft_guidance',[]))!=3 or any(x in json.dumps(writer,ensure_ascii=False) for x in ('FAIL','刘先生','human_feedback','findings'))):raise ValueError('CLARITY_WRITER_NEW_FACT_OR_ANSWER_LEAKAGE')
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('authorization')!=r['authorization'] or m.get('source_artifact')!=r['source_artifact'] or
        m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or m.get('generation_limit')!=1 or m.get('quality_certification_allowed') is not False or
        set(m.get('jobs',{}))!={'writer','editor','reader'}):raise ValueError('CLARITY_MANIFEST_DRIFT')
    ids=[];reports={}
    for role,job in m['jobs'].items():
        rt=runtime_check(root,r['runtimes'][role],role,job,m['result_dir']);ids.append(rt['thread_id'])
        if rt['raw_report']!=(r['final_artifact'] if role=='writer' else r['raw_reports'][role]):raise ValueError('CLARITY_RAW_BINDING_DRIFT')
        if role=='writer':continue
        packet=bound(root,job['packet']);runner.review.validate_packet(packet)
        if packet['samples']!=[dict(artifact_id='CL83' if role=='reader' else 'CL82',original_sha256=hashlib.sha256(body.encode()).hexdigest(),text=body)] or packet['work_kind']!=('COLD_SCREEN' if role=='reader' else 'EDITORIAL_REVIEW'):raise ValueError('CLARITY_REVIEW_WRONG_ARTIFACT')
        if role=='editor' and packet.get('facts')!=source_facts:raise ValueError('CLARITY_EDITOR_FACT_DRIFT')
        if role=='reader' and any(k in json.dumps(packet,ensure_ascii=False) for k in ('刘先生','human_feedback','FAIL','findings')):raise ValueError('CLARITY_COLD_ANSWER_LEAKAGE')
        report=runner.review.parse_report(bound(root,r['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,rt,'NEW_STORY_OPENING_EXCERPT') if role=='reader' else runner.review.audit_report(packet,report,rt,'NEW_STORY_OPENING_EXCERPT')
        saved=bound(root,r['evidence'][role])
        if audit['errors'] or any(saved.get(k)!=v for k,v in audit.items()):raise ValueError('CLARITY_REPORT_OR_QUOTE_DRIFT')
    prior_ids={bound(root,v)['thread_id'] for v in p['story_replacement_trial']['runtimes'].values()}
    if len(set(ids))!=3 or set(ids)&prior_ids:raise ValueError('CLARITY_SHARED_CONTEXT')
    if reports['editor']['results'][0]['verdict'] not in ('EDITORIAL_CLEAR','REVISE'):raise ValueError('CLARITY_INSUFFICIENT_REVIEW')
    pending=bound(root,r['pending_human_review'])
    if (pending.get('artifact')!=r['final_artifact'] or pending.get('outcome')!='UNKNOWN' or pending.get('accepted') is not False or pending.get('human_feedback')!={} or
        s.get('final_artifact')!=r['final_artifact'] or s.get('raw_reports_rewritten') is not False or s.get('AI_quality_certification') is not False or
        s.get('coordinator_prose_edits')!=0 or s.get('reader_vote_triggers_more_generation') is not False or s.get('high_impact_unresolved')!=[] or s.get('fact_conflicts_unresolved')!=[]):raise ValueError('CLARITY_SETTLEMENT_OR_UNKNOWN_DRIFT')
    positions=s.get('clarity_checks',[])
    if len(positions)<5 or not s.get('coordinator_source_diagnosis') or not s.get('prior_review_miss'):raise ValueError('CLARITY_OWNERSHIP_CHECK_MISSING')
    for item in positions:
        q=item.get('quote','');off=body.find(q) if q else -1
        if off<0 or item.get('line')!=body[:off].count('\n')+1 or not item.get('actor') or not item.get('object_or_listener') or not item.get('reason'):raise ValueError('CLARITY_OWNERSHIP_EVIDENCE_DRIFT')
    findings=reports['editor']['results'][0]['findings'];items=s.get('finding_dispositions',[])
    if {f['id'] for f in findings}!={i.get('id') for i in items}:raise ValueError('CLARITY_FINDING_UNSETTLED')
    for i in items:
        f=next(f for f in findings if f['id']==i['id'])
        if any(i.get(k)!=f.get(k) for k in ('quote','line','basis')) or not i.get('reason'):raise ValueError('CLARITY_FINDING_DISPOSITION_DRIFT')
    for v in (p,c):
        if (v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=r['task']['path'] or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or
            v.get('latest_human_review')!=h['review'] or v.get('human_verdict_receipt')!=r['human_feedback']['path'] or
            v.get('status')!='CLARITY_REPAIRED_SHORT_AWAIT_ACTUAL_HUMAN_READING'):raise ValueError('CLARITY_LIVE_CURSOR_DRIFT')
    if c.get('sequence')!=206 or c.get('stop') is not True or c['action_guard']['closed_task_ids']!=p['closed_task_ids'] or c['action_guard']['project_state_sha256']!=hashlib.sha256((root/'state/project_state.json').read_bytes()).hexdigest():raise ValueError('CLARITY_CHECKPOINT_GUARD_DRIFT')
    for name in ('START_HERE.md','README.md','AGENTS.md','SKILL.md'):
        text=(root/name).read_text(encoding='utf-8')
        if '检查点206' not in text or TASK not in text or r['result_document']['path'] not in text:raise ValueError('CLARITY_ENTRY_DRIFT')
    bound(root,r['result_document'],False)
    return dict(sequence=206,status=p['status'],next_action=NEXT,historical_checks_passed=baseline['checks_passed'],checks_passed=baseline['checks_passed']+11,
        protected_source_file_count=protected,new_prose_authorized=False,human_quality_result='UNKNOWN',source_retention_result='YES_ONLY_FOR_383',source_clarity_result='FAIL',
        model_calls_during_validation=0,generation_count_during_validation=0,mainline=baseline['mainline'],literary_quality_tested_by_this_script=False)
