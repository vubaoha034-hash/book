"""Reusable evidence gate for one same-story short repair; no quality rating."""
from pathlib import Path
import hashlib,importlib.util,json

def module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
history=module('scoped_history','frozen_history.py')
common=module('scoped_runtime_gate','verify_prose_repair.py')
runner=module('scoped_transport','novel_emotion_dialogue_repair.py')
bound,blob=common.bound,common.blob
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_SCOPED_REPAIRED_SHORT'
MUTABLE=('AGENTS.md','README.md','SKILL.md','START_HERE.md','scripts/verify_current_state.py','state/project_state.json','state/continuity/LATEST_CHECKPOINT.json','tests/test_emotion_dialogue_repair.py')
SCENE_MUTABLE=(*MUTABLE,'scripts/verify_scoped_short_repair.py','tests/test_scoped_short_repair.py')
LIVE_KEYS={'updated_at','recorded_at','sequence','stop','action_guard','closed_task_ids','current_focus','status','last_completed_task_id','last_completed_task_contract','next_action','next_required_action','current_human_gate','human_verdict_receipt','latest_human_review','scoped_short_repair'}
_baselines={}

def baseline(root,p,c,r):
    head=r['source_head'];source=history.frozen_tree(Path(__file__).resolve().parents[1],head)
    bp=json.loads((source/'state/project_state.json').read_bytes());bc=json.loads((source/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    if head not in _baselines:
        current=module('scoped_prior_current','verify_current_state.py');_baselines[head]=current.verify(source)
    old=_baselines[head]
    if old['sequence']!=r['source_checkpoint'] or old['new_prose_authorized'] is not False:raise ValueError('SCOPED_INVALID_BASELINE')
    for live,prior in ((p,bp),(c,bc)):
        if {k:v for k,v in live.items()if k not in LIVE_KEYS}!={k:v for k,v in prior.items()if k not in LIVE_KEYS}:raise ValueError('SCOPED_HISTORICAL_STATE_DRIFT')
    if p['closed_task_ids']!=bp['closed_task_ids']+[r['task_id']] or {k:v for k,v in c['action_guard'].items()if k not in ('closed_task_ids','project_state_sha256')}!={k:v for k,v in bc['action_guard'].items()if k not in ('closed_task_ids','project_state_sha256')}:raise ValueError('SCOPED_OLD_LOCK_OR_CLOSED_TASK_DRIFT')
    mutable=SCENE_MUTABLE if r.get('scope_kind')=='NATURAL_SCENE_RELATION_EMOTION'else MUTABLE
    files=[f.relative_to(source).as_posix()for f in source.rglob('*')if f.is_file()and '__pycache__'not in f.parts and f.relative_to(source).as_posix()not in mutable]
    for name in files:
        if not(root/name).is_file()or(root/name).read_bytes()!=(source/name).read_bytes():raise ValueError('SCOPED_HISTORICAL_FILE_CHANGED: '+name)
    prior_route=bp.get('scoped_short_repair')or bp['emotion_dialogue_repair']
    return old,len(files),prior_route

def runtime_check(root,ref,role,job,directory,task):
    saved=common.TASK,common.runner
    common.TASK,common.runner=task,runner.engine;runner.engine.DIRECTORY=directory
    try:return common.runtime_check(root,ref,role,job)
    finally:common.TASK,common.runner=saved

def located(body,items):
    for item in items:
        q=item.get('quote','');off=body.find(q)if q else -1
        if off<0 or item.get('line')!=body[:off].count('\n')+1 or not item.get('reason'):raise ValueError('SCOPED_COORDINATOR_QUOTE_DRIFT')

def verify(root,p,c):
    r=p.get('scoped_short_repair')
    if not r or r!=c.get('scoped_short_repair'):raise ValueError('SCOPED_CURRENT_ROUTE_DRIFT')
    old,protected,prior=baseline(root,p,c,r);task=r['task_id'];head=r['source_head'];seq=r['source_checkpoint']
    a,h,t,result,s=[bound(root,r[k])for k in ('authorization','human_feedback','task','result','settlement')]
    scene=r.get('scope_kind')=='NATURAL_SCENE_RELATION_EMOTION'
    if r.get('scope_kind')not in(None,'NATURAL_SCENE_RELATION_EMOTION')or a.get('scope_kind')!=r.get('scope_kind'):raise ValueError('SCOPED_SCOPE_KIND_DRIFT')
    calls=4 if scene else 3
    expected_review=(dict(scene_emotion='CHALLENGED_NATURAL_RELATION_EMOTION_MISSING',revision_effect='CHALLENGED_BY_HUMAN',wants_to_continue='UNKNOWN_NOT_DIRECTLY_ANSWERED',ai_smell_verdict='UNKNOWN_NOT_SEPARATELY_ANSWERED',exact_stop_sentence='UNKNOWN_NOT_PROVIDED')if scene else dict(dialogue_emotion='FAIL_ROBOTIC_INTERACTION',emotion_verdict='FAIL_UNFELT_FEAR_AND_CONCEALMENT',wants_to_continue='UNKNOWN_NOT_DIRECTLY_ANSWERED',ai_smell_verdict='UNKNOWN_NOT_SEPARATELY_ANSWERED',exact_stop_sentence='UNKNOWN_NOT_PROVIDED'))
    outcome='HUMAN_CHALLENGES_PATCH_ONLY_EMOTION_AND_RESEARCH_APPLICATION'if scene else'HUMAN_REJECTS_ROBOTIC_DIALOGUE_AND_UNFELT_FEAR'
    if (a.get('task_id')!=task or a.get('source_head')!=head or a.get('source_checkpoint')!=seq or a.get('source')!='STANDING_AUTONOMY_AND_CURRENT_HUMAN_REVIEW' or a.get('scope')!='ONE_SAME_STORY_EMOTION_AND_DIALOGUE_REPAIR_300_500_ONLY' or
        a.get('writer_limit')!=1 or a.get('diagnosis_limit')!=(1 if scene else 0) or a.get('maximum_internal_repair')!=0 or a.get('old_RC3_remaining_rounds')!=0 or not a.get('authorized_reaction') or
        a.get('source_artifact')!=prior['final_artifact'] or r.get('source_artifact')!=a.get('source_artifact') or a.get('human_feedback')!=r['human_feedback'] or
        a.get('prior_diagnosis')!=p['emotion_dialogue_repair']['raw_reports']['diagnosis'] or a.get('new_independent_diagnosis_claimed')is not scene or
        any(a.get(k)is not False for k in ('new_plot_or_life_facts_authorized','old_197_character_protection_released','full_scene_or_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized')) or
        h.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or h.get('human_exact_feedback')!=a.get('authority',{}).get('exact_message') or not h.get('human_exact_feedback') or h.get('output')!=a['source_artifact'] or h.get('source_head')!=head or h.get('source_checkpoint')!=seq or h.get('prior_records_rewritten')is not False or
        h.get('outcome')!=outcome or h.get('review')!=expected_review):raise ValueError('SCOPED_AUTHORITY_OR_HUMAN_SCOPE_DRIFT')
    standing=bound(root,a['standing_authorization'])
    if standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required')is not False:raise ValueError('SCOPED_NO_STANDING_AUTHORITY')
    keys=('authorization','human_feedback','source_artifact','manifests','writer_input','final_artifact','settlement','pending_human_review','runtimes','raw_reports','evidence','learning_application','result_document')
    for v in (r,t,result):
        if(v.get('task_id')!=task or v.get('source_head')!=head or v.get('source_checkpoint')!=seq or v.get('next_action')!=NEXT or v.get('actual_model_calls')!=calls or v.get('successful_model_calls')!=calls or
           v.get('primary_generation_count')!=0 or v.get('local_repair_count')!=1 or v.get('visible_candidate_count')!=1 or v.get('human_quality_result')!='UNKNOWN' or v.get('remaining_repair_budget')!=0 or v.get('old_RC3_remaining_rounds')!=0 or
           any(v.get(k)is not False for k in ('full_scene_or_TEST01_promoted','AI_quality_certification','automatic_writer_dispatch','automatic_background_sync','old_197_character_protection_released')) or any(v.get(k)!=r.get(k)for k in keys)):raise ValueError('SCOPED_BUDGET_OR_HUMAN_PROMOTION')
    source=bound(root,r['source_artifact'],False).decode();body=bound(root,r['final_artifact'],False).decode()
    if not 300<=sum(not x.isspace()for x in body)<=500 or body.startswith('#')or'```'in body:raise ValueError('SCOPED_BODY_SCOPE_DRIFT')
    facts=bound(root,p['story_replacement_trial']['writer_input'])['facts'];authorized={**facts,'authorized_current_reaction':a['authorized_reaction']};writer=bound(root,r['writer_input'])
    expected_writer=authorized if scene else{**authorized,'source_text':source}
    if set(writer)!={'scope','facts','positive_craft_guidance'}or writer['facts']!=expected_writer or len(writer['positive_craft_guidance'])!=3 or any(x in json.dumps(writer,ensure_ascii=False)for x in('FAIL','刘先生','human_feedback','findings','EDITORIAL_CLEAR')):raise ValueError('SCOPED_WRITER_FACT_OR_ANSWER_LEAKAGE')
    if scene and a.get('writer_receives_failed_text')is not False:raise ValueError('SCOPED_WRITER_PATCH_ANCHORING')
    jobs={}
    stages=(('production',{'writer','diagnosis'}),('reviews',{'editor','reader'}))if scene else(('writer',{'writer'}),('reviews',{'editor','reader'}))
    for stage,expected in stages:
        m=bound(root,r['manifests'][stage])
        if(m.get('task_id')!=task or m.get('source_head')!=head or m.get('authorization')!=r['authorization']or m.get('model')!='gpt-6.1-sol'or m.get('reasoning_effort')!='max'or m.get('generation_limit')!=1 or m.get('quality_certification_allowed')is not False or set(m['jobs'])!=expected):raise ValueError('SCOPED_MANIFEST_DRIFT')
        jobs.update({role:(job,m['result_dir'])for role,job in m['jobs'].items()})
    if jobs['writer'][0]['packet']!=r['writer_input']:raise ValueError('SCOPED_WRITER_BINDING_DRIFT')
    ids=[];reports={}
    for role,(job,directory)in jobs.items():
        rt=runtime_check(root,r['runtimes'][role],role,job,directory,task);ids.append(rt['thread_id'])
        if rt['raw_report']!=(r['final_artifact']if role=='writer'else r['raw_reports'][role]):raise ValueError('SCOPED_RAW_BINDING_DRIFT')
        if role=='writer':continue
        packet=bound(root,job['packet']);runner.review.validate_packet(packet)
        target=source if role=='diagnosis'else body
        if len(packet['samples'])!=1 or packet['samples'][0]['text']!=target or packet['samples'][0]['original_sha256']!=hashlib.sha256(target.encode()).hexdigest():raise ValueError('SCOPED_REVIEW_WRONG_ARTIFACT')
        if packet['work_kind']!={'editor':'EDITORIAL_REVIEW','reader':'COLD_SCREEN','diagnosis':'POST_FAILURE_DIAGNOSIS'}[role]:raise ValueError('SCOPED_REVIEW_WORK_KIND_DRIFT')
        if role=='editor'and packet['facts']!=(facts if scene else authorized):raise ValueError('SCOPED_EDITOR_FACT_DRIFT')
        if role=='diagnosis'and(packet['facts']!=facts or packet['human_feedback']['exact_message']!=h['human_exact_feedback']or packet['historical_material']!=[]):raise ValueError('SCOPED_DIAGNOSIS_SCOPE_DRIFT')
        if role=='reader'and any(x in json.dumps(packet,ensure_ascii=False)for x in('刘先生','human_feedback','FAIL','findings','diagnosis','fear','concealment')):raise ValueError('SCOPED_COLD_ANSWER_LEAKAGE')
        report=runner.review.parse_report(bound(root,r['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,rt,'NEW_STORY_OPENING_EXCERPT')if role=='reader'else runner.review.audit_report(packet,report,rt,'NEW_STORY_OPENING_EXCERPT')
        evidence=bound(root,r['evidence'][role])
        if audit['errors']or any(evidence.get(k)!=v for k,v in audit.items()):raise ValueError('SCOPED_REPORT_OR_QUOTE_DRIFT')
    prior_ids={bound(root,v)['thread_id']for v in prior['runtimes'].values()}
    if len(set(ids))!=calls or set(ids)&prior_ids:raise ValueError('SCOPED_SHARED_CONTEXT')
    if reports['editor']['results'][0]['verdict']not in('EDITORIAL_CLEAR','REVISE'):raise ValueError('SCOPED_INSUFFICIENT_REPORT')
    if scene and reports['diagnosis']['results'][0]['verdict']!='REVISE':raise ValueError('SCOPED_INSUFFICIENT_DIAGNOSIS')
    pending=bound(root,r['pending_human_review'])
    if(pending.get('artifact')!=r['final_artifact']or pending.get('outcome')!='UNKNOWN'or pending.get('accepted')is not False or pending.get('human_feedback')!={}or
       s.get('final_artifact')!=r['final_artifact']or s.get('raw_reports_rewritten')is not False or s.get('AI_quality_certification')is not False or s.get('coordinator_prose_edits')!=0 or s.get('reader_vote_triggers_more_generation')is not False or s.get('high_impact_unresolved')!=[]or s.get('fact_conflicts_unresolved')!=[]):raise ValueError('SCOPED_SETTLEMENT_OR_UNKNOWN_DRIFT')
    for role in(('diagnosis','editor')if scene else('editor',)):
        findings=reports[role]['results'][0]['findings'];items=s['finding_dispositions'][role]
        if {f['id']for f in findings}!={i.get('id')for i in items}:raise ValueError('SCOPED_FINDING_UNSETTLED')
        for item in items:
            f=next(f for f in findings if f['id']==item['id'])
            if any(item.get(k)!=f.get(k)for k in('quote','line','basis'))or not item.get('reason'):raise ValueError('SCOPED_FINDING_EVIDENCE_DRIFT')
    checks=s.get('fact_and_dialogue_checks',[]);reaction=s.get('reaction_and_restraint_checks',[])
    required_kinds={'CHILD_RELATIONSHIP_AFFECT','FAMILY_RELATIONSHIP_AFFECT','NARRATOR_CHANGE_AND_RESTRAINT'}if scene else{'IMMEDIATE_REACTION','OUTWARD_RESTRAINT','SOCIAL_REPLY_PRESSURE'}
    if len(checks)<6 or {x.get('kind')for x in reaction}!=required_kinds:raise ValueError('SCOPED_REACTION_EVIDENCE_MISSING')
    located(body,checks+reaction)
    for item in s.get('coordinator_post_failure_hypotheses',[]):
        q=item.get('quote','');off=source.find(q)if q else -1
        if off<0 or item.get('source_line')!=source[:off].count('\n')+1 or item.get('basis')!='COORDINATOR_EDITORIAL_HYPOTHESIS':raise ValueError('SCOPED_SOURCE_HYPOTHESIS_QUOTE_DRIFT')
    if s.get('new_independent_diagnosis_claimed')is not scene or s.get('prior_independent_diagnosis')!=a['prior_diagnosis']:raise ValueError('SCOPED_DIAGNOSIS_OVERCLAIM')
    interpretation=bound(root,s['report_interpretation_audit']);expected_corrections=[]
    for role,report in reports.items():
        if role not in('editor','reader'):continue
        record=report['results'][0]if role=='editor'else report
        for window,item in record['reading_expectations'].items():
            q=item['quote'];off=body.find(q)
            if off<0 or item['line']!=body[:off].count('\n')+1:raise ValueError('SCOPED_WINDOW_QUOTE_DRIFT')
            start=sum(not c.isspace()for c in body[:off])+1;end=start+sum(not c.isspace()for c in q)-1
            if window=='first_150_300'and not(start<=300 and end>=150):expected_corrections.append((role,window,q,item['line'],[start,end]))
    corrections=interpretation.get('corrections',[])
    if (interpretation.get('raw_reports_rewritten')is not False or interpretation.get('new_model_call')is not False or interpretation.get('final_artifact')!=r['final_artifact']or
        [(v['role'],v['window'],v['quote'],v['line'],v['actual_non_whitespace_range'])for v in corrections]!=expected_corrections or any(v.get('disposition')!='DO_NOT_TREAT_AS_A_QUOTE_FROM_CHARACTERS_150_TO_300'for v in corrections)):raise ValueError('SCOPED_WINDOW_CORRECTION_MISSING')
    learning=bound(root,r['learning_application'])
    if learning.get('research_read_is_quality_pass')is not False or learning.get('diagnosis_or_human_label_in_writer')is not False or learning.get('new_independent_diagnosis_claimed')is not scene or not learning.get('gap'):raise ValueError('SCOPED_LEARNING_CAPABILITY_OVERCLAIM')
    if scene and (learning.get('writer_receives_failed_text')is not False or learning.get('full_book_read')is not False or learning.get('full_video_or_audio_completed')is not False):raise ValueError('SCOPED_LEARNING_OVERCLAIM')
    status='SCOPED_REPAIRED_SHORT_AWAIT_ACTUAL_HUMAN_READING';gate='SOURCE_417_SCENE_EMOTION_CHALLENGED_NEW_SHORT_HUMAN_UNKNOWN'if scene else'SOURCE_392_ROBOTIC_EMOTION_FAIL_REPAIRED_SHORT_HUMAN_UNKNOWN'
    for v in(p,c):
        if(v.get('last_completed_task_id')!=task or v.get('last_completed_task_contract')!=r['task']['path']or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT or v.get('latest_human_review')!=h['review']or v.get('human_verdict_receipt')!=r['human_feedback']['path']or v.get('status')!=status or v.get('current_human_gate')!=gate):raise ValueError('SCOPED_CURRENT_CURSOR_DRIFT')
    if c.get('sequence')!=seq+1 or c.get('stop')is not True or c['action_guard']['closed_task_ids']!=p['closed_task_ids']or c['action_guard']['project_state_sha256']!=hashlib.sha256((root/'state/project_state.json').read_bytes()).hexdigest():raise ValueError('SCOPED_CHECKPOINT_GUARD_DRIFT')
    for name in('START_HERE.md','README.md','AGENTS.md','SKILL.md'):
        text=(root/name).read_text(encoding='utf-8')
        if f'检查点{seq+1}'not in text or task not in text or r['result_document']['path']not in text:raise ValueError('SCOPED_ENTRY_DRIFT')
    bound(root,r['result_document'],False)
    return dict(sequence=seq+1,status=p['status'],next_action=NEXT,historical_checks_passed=old['checks_passed'],checks_passed=old['checks_passed']+11,protected_source_file_count=protected,new_prose_authorized=False,human_quality_result='UNKNOWN',mainline=old['mainline'],model_calls_during_validation=0,generation_count_during_validation=0,literary_quality_tested_by_this_script=False)
