"""Verify the current repair and preserve every prior failure, lock and report."""
from pathlib import Path
import hashlib,importlib.util,json
def module(n,f):
    s=importlib.util.spec_from_file_location(n,Path(__file__).with_name(f));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
prior=module('emotion_prior_gate','verify_clarity_repair.py');runner=module('emotion_runner','novel_emotion_dialogue_repair.py')
history,bound,blob=prior.history,prior.bound,prior.blob
SOURCE='d5bf06d6b08704fc9b6c9033ead41e20fb1f980e';TASK='NOVEL-SAME-STORY-EMOTION-DIALOGUE-REPAIR-20261004-01'
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_EMOTION_DIALOGUE_REPAIRED_SHORT'
EXACT='我对妈说：“明早要喝，怕店关了。”\n你自己看下这句话是什么意思。  而后是不是情感还是太平了。这就是你读取了后学习的吗？'
MUTABLE=(*(p for p in prior.MUTABLE if p!='tests/test_story_trial.py'),'tests/test_clarity_repair.py');LIVE_KEYS=prior.LIVE_KEYS|{'emotion_dialogue_repair'};_baseline=None
def baseline(root,p,c):
    global _baseline
    source=history.frozen_tree(Path(__file__).resolve().parents[1],SOURCE)
    bp=json.loads((source/'state/project_state.json').read_bytes());bc=json.loads((source/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    if _baseline is None:_baseline=prior.verify(source,bp,bc)
    if _baseline['sequence']!=206 or _baseline['new_prose_authorized'] is not False:raise ValueError('EMOTION_BASELINE_DRIFT')
    for live,old in ((p,bp),(c,bc)):
        if {k:v for k,v in live.items() if k not in LIVE_KEYS}!={k:v for k,v in old.items() if k not in LIVE_KEYS}:raise ValueError('EMOTION_HISTORICAL_STATE_DRIFT')
    if p['closed_task_ids']!=bp['closed_task_ids']+[TASK] or {k:v for k,v in c['action_guard'].items() if k not in ('closed_task_ids','project_state_sha256')}!={k:v for k,v in bc['action_guard'].items() if k not in ('closed_task_ids','project_state_sha256')}:raise ValueError('EMOTION_OLD_LOCK_OR_CLOSED_TASK_DRIFT')
    files=[f.relative_to(source).as_posix() for f in source.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.relative_to(source).as_posix() not in MUTABLE]
    for name in files:
        if not(root/name).is_file() or (root/name).read_bytes()!=(source/name).read_bytes():raise ValueError('EMOTION_HISTORICAL_FILE_CHANGED: '+name)
    return _baseline,len(files)
def runtime_check(root,ref,role,job,directory):
    common=prior.prior.common;old=common.TASK,common.runner
    common.TASK,common.runner=TASK,runner.engine;runner.engine.DIRECTORY=directory
    try:return common.runtime_check(root,ref,role,job)
    finally:common.TASK,common.runner=old
def verify(root,p,c):
    r=p.get('emotion_dialogue_repair')
    if not r or r!=c.get('emotion_dialogue_repair'):raise ValueError('EMOTION_CURRENT_ROUTE_DRIFT')
    old,protected=baseline(root,p,c)
    a,h,t,result,s=[bound(root,r[k]) for k in ('authorization','human_feedback','task','result','settlement')]
    if (a.get('task_id')!=TASK or a.get('source_head')!=SOURCE or a.get('source')!='STANDING_AUTONOMY_AND_CURRENT_HUMAN_REVIEW' or a.get('scope')!='ONE_SAME_STORY_EMOTION_AND_DIALOGUE_REPAIR_300_500_ONLY' or
        a.get('writer_limit')!=1 or a.get('maximum_internal_repair')!=0 or a.get('old_RC3_remaining_rounds')!=0 or a.get('authority',{}).get('exact_message')!=EXACT or
        a.get('source_artifact')!=p['clarity_repair']['final_artifact'] or r.get('source_artifact')!=a.get('source_artifact') or a.get('human_feedback')!=r['human_feedback'] or
        any(a.get(k) is not False for k in ('new_plot_or_life_facts_authorized','old_197_character_protection_released','full_scene_or_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized')) or
        h.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or h.get('human_exact_feedback')!=EXACT or h.get('output')!=a['source_artifact'] or h.get('source_head')!=SOURCE or h.get('source_checkpoint')!=206 or h.get('prior_records_rewritten') is not False or
        h.get('outcome')!='DIALOGUE_MEANING_CHALLENGED_AND_EMOTION_FLATNESS_RAISED' or h.get('review')!=dict(dialogue_meaning='CHALLENGED_AT_QUOTED_LINE',emotion_verdict='HUMAN_RAISED_STILL_FLAT_AS_QUESTION',wants_to_continue='UNKNOWN_NOT_DIRECTLY_ANSWERED',ai_smell_verdict='UNKNOWN_NOT_DIRECTLY_ANSWERED',exact_stop_sentence='UNKNOWN_NOT_PROVIDED')):raise ValueError('EMOTION_AUTHORITY_OR_HUMAN_SCOPE_DRIFT')
    standing=bound(root,a['standing_authorization'])
    if standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False:raise ValueError('EMOTION_NO_STANDING_AUTHORITY')
    keys=('authorization','human_feedback','source_artifact','manifests','writer_input','final_artifact','settlement','pending_human_review','runtimes','raw_reports','evidence','learning_application','result_document')
    for v in (r,t,result):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('next_action')!=NEXT or v.get('actual_model_calls')!=4 or v.get('successful_model_calls')!=4 or
            v.get('primary_generation_count')!=0 or v.get('local_repair_count')!=1 or v.get('visible_candidate_count')!=1 or v.get('human_quality_result')!='UNKNOWN' or v.get('remaining_repair_budget')!=0 or v.get('old_RC3_remaining_rounds')!=0 or
            any(v.get(k) is not False for k in ('full_scene_or_TEST01_promoted','AI_quality_certification','automatic_writer_dispatch','automatic_background_sync','old_197_character_protection_released')) or any(v.get(k)!=r.get(k) for k in keys)):raise ValueError('EMOTION_BUDGET_OR_HUMAN_PROMOTION')
    source=bound(root,r['source_artifact'],False).decode();body=bound(root,r['final_artifact'],False).decode()
    if not 300<=sum(not x.isspace() for x in body)<=500 or body.startswith('#') or '```' in body:raise ValueError('EMOTION_BODY_SCOPE_DRIFT')
    facts=bound(root,p['story_replacement_trial']['writer_input'])['facts'];writer=bound(root,r['writer_input'])
    if set(writer)!={'scope','facts','positive_craft_guidance'} or writer['facts']!={**facts,'source_text':source} or len(writer['positive_craft_guidance'])!=3 or any(x in json.dumps(writer,ensure_ascii=False) for x in ('FAIL','刘先生','human_feedback','findings','EDITORIAL_CLEAR')):raise ValueError('EMOTION_WRITER_FACT_OR_ANSWER_LEAKAGE')
    jobs={}
    for stage,expected in (('diagnosis',{'diagnosis'}),('writer',{'writer'}),('reviews',{'editor','reader'})):
        m=bound(root,r['manifests'][stage])
        if m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('authorization')!=r['authorization'] or m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or m.get('generation_limit')!=1 or m.get('quality_certification_allowed') is not False or set(m['jobs'])!=expected:raise ValueError('EMOTION_MANIFEST_DRIFT')
        jobs.update({role:(job,m['result_dir']) for role,job in m['jobs'].items()})
    if jobs['writer'][0]['packet']!=r['writer_input']:raise ValueError('EMOTION_WRITER_BINDING_DRIFT')
    ids=[];reports={}
    for role,(job,directory) in jobs.items():
        rt=runtime_check(root,r['runtimes'][role],role,job,directory);ids.append(rt['thread_id'])
        if rt['raw_report']!=(r['final_artifact'] if role=='writer' else r['raw_reports'][role]):raise ValueError('EMOTION_RAW_BINDING_DRIFT')
        if role=='writer':continue
        packet=bound(root,job['packet']);runner.review.validate_packet(packet)
        target=source if role=='diagnosis' else body;identifier={'diagnosis':'ED417','editor':'ED82','reader':'ED83'}[role]
        if packet['samples']!=[dict(artifact_id=identifier,original_sha256=hashlib.sha256(target.encode()).hexdigest(),text=target)]:raise ValueError('EMOTION_REVIEW_WRONG_ARTIFACT')
        if role=='diagnosis' and (packet['human_feedback']['exact_message']!=EXACT or packet['facts']!=facts or packet['historical_material']!=[]):raise ValueError('EMOTION_DIAGNOSIS_SCOPE_DRIFT')
        if role=='editor' and packet['facts']!=facts:raise ValueError('EMOTION_EDITOR_FACT_DRIFT')
        if role=='reader' and any(x in json.dumps(packet,ensure_ascii=False) for x in ('刘先生','human_feedback','FAIL','findings','diagnosis')):raise ValueError('EMOTION_COLD_ANSWER_LEAKAGE')
        report=runner.review.parse_report(bound(root,r['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,rt,'NEW_STORY_OPENING_EXCERPT') if role=='reader' else runner.review.audit_report(packet,report,rt,'NEW_STORY_OPENING_EXCERPT')
        evidence=bound(root,r['evidence'][role])
        if audit['errors'] or any(evidence.get(k)!=v for k,v in audit.items()):raise ValueError('EMOTION_REPORT_OR_QUOTE_DRIFT')
    prior_ids={bound(root,v)['thread_id'] for v in p['clarity_repair']['runtimes'].values()}
    if len(set(ids))!=4 or set(ids)&prior_ids:raise ValueError('EMOTION_SHARED_CONTEXT')
    if reports['diagnosis']['results'][0]['verdict']!='REVISE' or reports['editor']['results'][0]['verdict'] not in ('EDITORIAL_CLEAR','REVISE'):raise ValueError('EMOTION_INSUFFICIENT_REPORT')
    pending=bound(root,r['pending_human_review'])
    if (pending.get('artifact')!=r['final_artifact'] or pending.get('outcome')!='UNKNOWN' or pending.get('accepted') is not False or pending.get('human_feedback')!={} or
        s.get('final_artifact')!=r['final_artifact'] or s.get('raw_reports_rewritten') is not False or s.get('AI_quality_certification') is not False or s.get('coordinator_prose_edits')!=0 or s.get('reader_vote_triggers_more_generation') is not False or s.get('high_impact_unresolved')!=[] or s.get('fact_conflicts_unresolved')!=[]):raise ValueError('EMOTION_SETTLEMENT_OR_UNKNOWN_DRIFT')
    for role in ('diagnosis','editor'):
        findings=reports[role]['results'][0]['findings'];items=s['finding_dispositions'][role]
        if {f['id'] for f in findings}!={i.get('id') for i in items}:raise ValueError('EMOTION_FINDING_UNSETTLED')
        for item in items:
            f=next(f for f in findings if f['id']==item['id'])
            if any(item.get(k)!=f.get(k) for k in ('quote','line','basis')) or not item.get('reason'):raise ValueError('EMOTION_FINDING_EVIDENCE_DRIFT')
    checks=s.get('fact_and_dialogue_checks',[])
    if len(checks)<6:raise ValueError('EMOTION_FACT_CHECK_MISSING')
    for item in checks:
        q=item.get('quote','');off=body.find(q) if q else -1
        if off<0 or item.get('line')!=body[:off].count('\n')+1 or not item.get('reason'):raise ValueError('EMOTION_COORDINATOR_QUOTE_DRIFT')
    learning=bound(root,r['learning_application'])
    if learning.get('research_read_is_quality_pass') is not False or learning.get('diagnosis_or_human_label_in_writer') is not False or not learning.get('gap'):raise ValueError('EMOTION_LEARNING_CAPABILITY_OVERCLAIM')
    for v in (p,c):
        if v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=r['task']['path'] or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or v.get('latest_human_review')!=h['review'] or v.get('human_verdict_receipt')!=r['human_feedback']['path'] or v.get('status')!='EMOTION_DIALOGUE_REPAIRED_SHORT_AWAIT_ACTUAL_HUMAN_READING' or v.get('current_human_gate')!='SOURCE_417_DIALOGUE_EMOTION_CHALLENGED_REPAIRED_392_HUMAN_UNKNOWN':raise ValueError('EMOTION_CURRENT_CURSOR_DRIFT')
    if c.get('sequence')!=207 or c.get('stop') is not True or c['action_guard']['closed_task_ids']!=p['closed_task_ids'] or c['action_guard']['project_state_sha256']!=hashlib.sha256((root/'state/project_state.json').read_bytes()).hexdigest():raise ValueError('EMOTION_CHECKPOINT_GUARD_DRIFT')
    for name in ('START_HERE.md','README.md','AGENTS.md','SKILL.md'):
        text=(root/name).read_text(encoding='utf-8')
        if '检查点207' not in text or TASK not in text or r['result_document']['path'] not in text:raise ValueError('EMOTION_ENTRY_DRIFT')
    bound(root,r['result_document'],False)
    return dict(sequence=207,status=p['status'],next_action=NEXT,historical_checks_passed=old['checks_passed'],checks_passed=old['checks_passed']+11,protected_source_file_count=protected,new_prose_authorized=False,human_quality_result='UNKNOWN',mainline=old['mainline'],model_calls_during_validation=0,generation_count_during_validation=0,literary_quality_tested_by_this_script=False)
