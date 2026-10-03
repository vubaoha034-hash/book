"""Validate a bounded new-story override without weakening historical gates."""
from __future__ import annotations
import hashlib,importlib.util,json
from pathlib import Path
def module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
history=module('story_history','frozen_history.py')
runner=module('story_runner','novel_story_trial.py')
common=module('story_common','verify_prose_repair.py')
bound,blob=common.bound,common.blob
SOURCE='d2283f009fc5527a8427e5b46199ddb54d69cc51'
TASK='NOVEL-NEW-STORY-PSYCHOLOGY-OPENING-TRIAL-20261004-01'
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_NEW_STORY_OPENING'
MANIFEST='config/novel-new-story-20261004.json'
EXACT='一，真的没有读下去的欲望。   二，依旧有ai味道。只是更轻了。   三，实在不行你换个故事，能快速抓住要求的。  四，有大量的心理学研究，如何才能快速让人想看。你自己查下，这个结果花了这么久的时间。  对我来说非常不满意。'
SUPPLEMENT='现在应该有大量的去除ai味道的教程，也有大量爆款小说在网络上。你为什么自己搞不定的情况下自己搜索下？很多现成的你学习，应用呀。反反复复提交这样的结果，真的是浪费。'
MUTABLE=('AGENTS.md','README.md','SKILL.md','START_HERE.md','scripts/verify_current_state.py','scripts/codex_review.py','scripts/novel_two_role_review.py',
    'state/project_state.json','state/continuity/LATEST_CHECKPOINT.json',
    *(f'tests/{n}.py' for n in ('test_current_state','test_continuation_trial','test_hook_trial','test_hook_trial_human_feedback','test_hook_trial_qualified_short','test_prose_repair')))
LIVE_KEYS={'updated_at','recorded_at','sequence','stop','action_guard','closed_task_ids','current_focus','status','last_completed_task_id','last_completed_task_contract',
    'next_action','next_required_action','current_human_gate','human_verdict_receipt','latest_human_review','story_replacement_trial'}
_pinned_validation=None
def baseline_checks(root,project,cp):
    global _pinned_validation
    source=history.frozen_tree(Path(__file__).resolve().parents[1],SOURCE)
    # Cache only validation of the immutable pinned tree in this process.
    # Every call still compares the live state and every protected file.
    if _pinned_validation is None:
        old=module('historical_source_verifier','verify_current_state.py')
        _pinned_validation=old.verify(source)
    result=_pinned_validation
    if result['sequence']!=204 or result['new_prose_authorized'] is not False:raise ValueError('INVALID_PINNED_BASELINE')
    for name,live in [('state/project_state.json',project),('state/continuity/LATEST_CHECKPOINT.json',cp)]:
        prior=json.loads((source/name).read_bytes())
        if {k:v for k,v in live.items() if k not in LIVE_KEYS}!={k:v for k,v in prior.items() if k not in LIVE_KEYS}:raise ValueError('HISTORICAL_STATE_OR_MAINLINE_DRIFT')
    prior_project=json.loads((source/'state/project_state.json').read_bytes())
    prior_cp=json.loads((source/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    if project.get('closed_task_ids')!=prior_project['closed_task_ids']+[TASK]:raise ValueError('HISTORICAL_CLOSED_TASK_GUARD_REMOVED')
    if {k:v for k,v in cp.get('action_guard',{}).items() if k not in ('closed_task_ids','project_state_sha256')}!={k:v for k,v in prior_cp['action_guard'].items() if k not in ('closed_task_ids','project_state_sha256')}:raise ValueError('HISTORICAL_ACTION_GUARD_CHANGED')
    protected=[p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.relative_to(source).as_posix() not in MUTABLE]
    for p in protected:
        if not(root/p).is_file() or (root/p).read_bytes()!=(source/p).read_bytes():raise ValueError('HISTORICAL_ARTIFACT_CHANGED: '+p)
    return result,len(protected)
def runtime_check(root,ref,role,job,directory):
    prior=(common.TASK,common.runner)
    common.TASK,common.runner=TASK,runner.engine;runner.engine.DIRECTORY=directory
    try:return common.runtime_check(root,ref,role,job)
    finally:common.TASK,common.runner=prior
def verify(root,project,cp):
    r=project.get('story_replacement_trial')
    if not r or r!=cp.get('story_replacement_trial'):raise ValueError('NEW_STORY_STATE_DRIFT')
    prior,protected=baseline_checks(root,project,cp)
    a=bound(root,r['authorization']);h=bound(root,r['human_failure']);supplement=bound(root,r['learning_supplement'])
    m=bound(root,r['manifest']);task=bound(root,r['task']);result=bound(root,r['result']);settlement=bound(root,r['settlement'])
    # The runner rechecks actual scope; use the same immutable references here.
    if (r['source_head']!=SOURCE or r['task_id']!=TASK or r['source_checkpoint']!=204 or
        a.get('task_id')!=TASK or a.get('source_head')!=SOURCE or a.get('authority',{}).get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or
        a['authority'].get('exact_message')!=EXACT or a.get('scope')!='ONE_NEW_STORY_300_500_CHARACTER_OPENING_ONLY_OLD_STORY_PAUSED_PRESERVED' or
        a.get('primary_writer_limit')!=1 or a.get('maximum_evidenced_repairs')!=1 or a.get('old_RC3_remaining_rounds')!=0 or
        any(a.get(k) is not False for k in ('old_197_character_protection_released','full_scene_or_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized','old_story_retcon_authorized')) or
        h.get('source_head')!=SOURCE or h.get('source_checkpoint')!=204 or h.get('human_exact_feedback')!=EXACT or h.get('outcome')!='FAIL' or
        h.get('output')!=project['continuation_short_trial']['final_artifact'] or h.get('prior_records_rewritten') is not False or
        h['review'].get('wants_to_continue') is not False or h['review'].get('retention_verdict')!='FAIL' or h['review'].get('ai_smell_verdict')!='FAIL_STILL_PRESENT_BUT_LIGHTER' or
        h['review'].get('exact_stop_sentence')!='UNKNOWN_NOT_PROVIDED' or h['review'].get('topic_rejection') is not False or
        h['review'].get('emotion_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or h['review'].get('robotic_interaction_verdict')!='UNKNOWN_NOT_DIRECTLY_ANSWERED' or
        supplement.get('exact_message')!=SUPPLEMENT or supplement.get('source')!='ACTUAL_CURRENT_USER_MESSAGE'):
        raise ValueError('NEW_STORY_PERMISSION_OR_HUMAN_SCOPE_DRIFT')
    bindkeys=('authorization','human_failure','learning_supplement','manifest','story_contract','writer_input','final_artifact','settlement','pending_human_review','runtimes','raw_reports','evidence','research_sources','research_raw','result_document')
    for v in (r,result,task):
        if (v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('primary_generation_count')!=1 or v.get('internal_repair_count')!=0 or
            v.get('visible_candidate_count')!=1 or v.get('actual_model_calls')!=3 or v.get('successful_model_calls')!=3 or v.get('human_quality_result')!='UNKNOWN' or
            v.get('old_story_status')!='PAUSED_PRESERVED' or v.get('old_RC3_remaining_rounds')!=0 or v.get('remaining_new_generation_budget')!=0 or
            v.get('next_action')!=NEXT or any(v.get(k) is not False for k in ('old_197_character_protection_released','full_scene_or_TEST01_promoted','literary_quality_validated','automatic_writer_dispatch','automatic_background_sync'))):
            raise ValueError('NEW_STORY_BUDGET_OR_HUMAN_PROMOTION')
        for k in bindkeys:
            if v.get(k)!=r.get(k):raise ValueError('NEW_STORY_RESULT_BINDING_DRIFT')
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('authorization')!=r['authorization'] or m.get('story_contract')!=r['story_contract'] or
        m.get('generation_limit')!=1 or m.get('maximum_evidenced_repairs')!=1 or m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or
        m.get('quality_certification_allowed') is not False or set(m.get('jobs',{}))!={'writer','editor','reader'}):raise ValueError('NEW_STORY_MANIFEST_DRIFT')
    body=bound(root,r['final_artifact'],False);text=body.decode();writer=bound(root,r['writer_input']);contract=bound(root,r['story_contract'])
    if not 300<=sum(not c.isspace() for c in text)<=500 or text.startswith('#') or '```' in text:raise ValueError('NEW_STORY_BODY_SCOPE_DRIFT')
    if set(writer)!={'scope','facts','positive_craft_guidance'} or len(writer['positive_craft_guidance'])!=3 or any(k in json.dumps(writer,ensure_ascii=False) for k in ('FAIL','刘先生','human_feedback','findings','reviewer-input')):raise ValueError('NEW_STORY_WRITER_ANSWER_LEAKAGE')
    if (contract.get('story_scope')!='独立新故事试读，不属于《第二套过去》' or contract.get('authorized_outputs')!=1 or
        contract.get('length_range')!=[300,500] or contract.get('human_quality_result')!='UNKNOWN'):raise ValueError('NEW_STORY_CONTRACT_RETCON')
    reports={};ids=[]
    for role,job in m['jobs'].items():
        packet=bound(root,job['packet']);rt=runtime_check(root,r['runtimes'][role],role,job,m['result_dir']);ids.append(rt['thread_id'])
        if rt['raw_report']!=(r['final_artifact'] if role=='writer' else r['raw_reports'][role]):raise ValueError('NEW_STORY_RAW_BINDING_DRIFT')
        if role=='writer':continue
        runner.review.validate_packet(packet)
        if (packet['samples']!=[dict(artifact_id='NS81' if role=='reader' else 'NS80',original_sha256=hashlib.sha256(body).hexdigest(),text=text)] or
            packet['work_kind']!=('COLD_SCREEN' if role=='reader' else 'EDITORIAL_REVIEW')):raise ValueError('NEW_STORY_REVIEW_WRONG_ARTIFACT')
        if role=='reader' and (set(packet)!={'packet_version','job_id','work_kind','medium','excerpt_position','samples'} or any(x in json.dumps(packet,ensure_ascii=False) for x in ('FAIL','刘先生','human_feedback','findings','EDITORIAL_CLEAR'))):raise ValueError('NEW_STORY_COLD_ANSWER_LEAKAGE')
        if role=='editor' and packet.get('facts')!=writer['facts']:raise ValueError('NEW_STORY_REVIEW_FACT_DRIFT')
        report=runner.review.parse_report(bound(root,r['raw_reports'][role],False));reports[role]=report
        audit=runner.roles.audit_reader(packet,report,rt,'NEW_STORY_OPENING_EXCERPT') if role=='reader' else runner.review.audit_report(packet,report,rt,'NEW_STORY_OPENING_EXCERPT')
        saved=bound(root,r['evidence'][role])
        if audit['errors'] or any(saved.get(k)!=v for k,v in audit.items()):raise ValueError('NEW_STORY_REPORT_OR_QUOTE_DRIFT')
    if len(set(ids))!=3 or set(ids)&{bound(root,v)['thread_id'] for v in project['continuation_short_trial']['runtimes'].values()}:raise ValueError('NEW_STORY_SHARED_CONTEXT')
    if reports['editor']['results'][0]['verdict'] not in ('EDITORIAL_CLEAR','REVISE'):raise ValueError('NEW_STORY_INSUFFICIENT_REVIEW')
    pending=bound(root,r['pending_human_review'])
    if (pending.get('artifact')!=r['final_artifact'] or pending.get('outcome')!='UNKNOWN' or pending.get('human_feedback')!={} or pending.get('accepted') is not False or
        settlement.get('final_artifact')!=r['final_artifact'] or settlement.get('raw_reports_rewritten') is not False or settlement.get('AI_quality_certification') is not False or
        settlement.get('reader_vote_triggers_more_generation') is not False or settlement.get('coordinator_prose_edits')!=0 or settlement.get('high_impact_unresolved')!=[] or settlement.get('fact_conflicts_unresolved')!=[]):raise ValueError('NEW_STORY_SETTLEMENT_OR_UNKNOWN_DRIFT')
    for role in ('editor','reader'):
        windows=settlement.get(role+'_window_quote_checks',[])
        original=reports[role]['results'][0]['reading_expectations'] if role=='editor' else reports[role]['reading_expectations']
        if len(windows)!=3 or {w.get('window') for w in windows}!={'first_30_60','first_150_300','ending'}:raise ValueError('NEW_STORY_WINDOW_CHECK_MISSING')
        for w in windows:
            quote=w.get('quote','');off=text.find(quote) if quote else -1
            if off<0 or original[w['window']]['quote']!=quote or w.get('actual_line')!=text[:off].count('\n')+1 or w.get('start_character_0_based')!=off:raise ValueError('NEW_STORY_WINDOW_QUOTE_DRIFT')
    checks=settlement.get('manual_fact_checks',[])
    if len(checks)<5:raise ValueError('NEW_STORY_FACT_CHECKS_MISSING')
    for item in checks:
        quote=item.get('quote','');off=text.find(quote) if quote else -1;field=item.get('fact_source_field')
        if off<0 or item.get('line')!=text[:off].count('\n')+1 or item.get('source_value')!=writer['facts'].get(field) or item.get('disposition')!='CLEAR' or not item.get('coordinator_reason'):raise ValueError('NEW_STORY_MANUAL_FACT_DRIFT')
    for k in ('research_sources','research_raw','result_document'):bound(root,r[k],False)
    for v in (project,cp):
        if (v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=r['task']['path'] or v.get('next_action')!=NEXT or
            v.get('next_required_action')!=NEXT or v.get('human_verdict_receipt')!=r['human_failure']['path'] or v.get('latest_human_review')!=h['review'] or
            v.get('status')!='NEW_STORY_SHORT_AWAIT_ACTUAL_HUMAN_READING' or
            v.get('current_human_gate')!='NEW_STORY_SHORT_HUMAN_UNKNOWN_OLD_STORY_PAUSED_374_FAIL_PRESERVED'):raise ValueError('NEW_STORY_LIVE_CURSOR_DRIFT')
    if (cp.get('sequence')!=205 or cp.get('stop') is not True or project['closed_task_ids']!=cp['action_guard']['closed_task_ids'] or TASK not in project['closed_task_ids'] or
        cp['action_guard']['project_state_sha256']!=hashlib.sha256((root/'state/project_state.json').read_bytes()).hexdigest()):raise ValueError('NEW_STORY_CHECKPOINT_GUARD_DRIFT')
    for path in ('START_HERE.md','README.md','AGENTS.md','SKILL.md'):
        entry=(root/path).read_text(encoding='utf-8')
        if '检查点205' not in entry or TASK not in entry or 'NOVEL_NEW_STORY_TRIAL_RESULT_20261004.md' not in entry:raise ValueError('NEW_STORY_ENTRY_DRIFT')
    return dict(sequence=205,status=project['status'],next_action=NEXT,checks_passed=prior['checks_passed']+12,
        historical_checks_passed=prior['checks_passed'],protected_source_file_count=protected,new_prose_authorized=False,
        model_calls_during_validation=0,generation_count_during_validation=0,mainline=prior['mainline'],human_quality_result='UNKNOWN',new_story_override_only=True)
