"""Evidence gate for a human-specified mechanical correction; no literary rating."""
from pathlib import Path
import hashlib,importlib.util,json

def module(name,file):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
history=module('lexical_history','frozen_history.py')
common=module('lexical_binding','verify_prose_repair.py')
bound=common.bound
SOURCE='1ca70db7ca2dfa74e0a462657bf0e1e894acd614'
TASK='NOVEL-SCENE-EMOTION-ONE-WORD-CORRECTION-20261004-01'
NEXT='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_LEXICALLY_CORRECTED_SHORT'
MUTABLE=('AGENTS.md','README.md','SKILL.md','START_HERE.md','scripts/verify_current_state.py','state/project_state.json','state/continuity/LATEST_CHECKPOINT.json')
LIVE_KEYS={'updated_at','recorded_at','sequence','stop','action_guard','closed_task_ids','current_focus','status','last_completed_task_id','last_completed_task_contract','next_action','next_required_action','current_human_gate','human_verdict_receipt','latest_human_review','scoped_text_correction'}
EXACT='你舅舅好容易回来   为什么会出现这么严重的问题。明明是好不容易回来。     但是整体改善了很多确实。'
REVIEW=dict(overall_change='RELATIVE_IMPROVEMENT_CONFIRMED_BY_HUMAN',wording='ONE_EXPRESSION_CORRECTION_REQUESTED',wants_to_continue='UNKNOWN_NOT_SEPARATELY_ANSWERED',ai_smell_verdict='UNKNOWN_NOT_SEPARATELY_ANSWERED',whole_story='UNKNOWN_NOT_REVIEWED',exact_stop_sentence='UNKNOWN_NOT_PROVIDED')
_baseline=None

def verify(root,p,c):
    global _baseline
    root=Path(root);r=p.get('scoped_text_correction')
    if not r or r!=c.get('scoped_text_correction')or r.get('task_id')!=TASK or r.get('source_head')!=SOURCE or r.get('source_checkpoint')!=209:raise ValueError('LEXICAL_ROUTE_OR_SOURCE_DRIFT')
    source=history.frozen_tree(Path(__file__).resolve().parents[1],SOURCE)
    bp=json.loads((source/'state/project_state.json').read_bytes());bc=json.loads((source/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    if _baseline is None:_baseline=module('lexical_prior_current','verify_current_state.py').verify(source)
    old=_baseline
    if old['sequence']!=209 or old['checks_passed']!=83 or old['new_prose_authorized']is not False:raise ValueError('LEXICAL_INVALID_BASELINE')
    for live,prior in((p,bp),(c,bc)):
        if {k:v for k,v in live.items()if k not in LIVE_KEYS}!={k:v for k,v in prior.items()if k not in LIVE_KEYS}:raise ValueError('LEXICAL_HISTORICAL_STATE_DRIFT')
    if p['closed_task_ids']!=bp['closed_task_ids']+[TASK]or c['action_guard']['closed_task_ids']!=p['closed_task_ids']or {k:v for k,v in c['action_guard'].items()if k not in('closed_task_ids','project_state_sha256')}!={k:v for k,v in bc['action_guard'].items()if k not in('closed_task_ids','project_state_sha256')}:raise ValueError('LEXICAL_OLD_LOCK_DRIFT')
    protected=[f.relative_to(source).as_posix()for f in source.rglob('*')if f.is_file()and'__pycache__'not in f.parts and f.relative_to(source).as_posix()not in MUTABLE]
    if len(protected)!=742:raise ValueError('LEXICAL_PROTECTED_FILE_COUNT_DRIFT')
    for path in protected:
        if not(root/path).is_file()or(root/path).read_bytes()!=(source/path).read_bytes():raise ValueError('LEXICAL_HISTORICAL_FILE_CHANGED: '+path)
    t,result,h,audit=[bound(root,r[k])for k in('task','result','human_feedback','report_miss_audit')]
    refs=('source_artifact','final_artifact','human_feedback','report_miss_audit','result_document','correction')
    flags=('old_197_character_protection_released','full_scene_or_TEST01_promoted','AI_quality_certification','automatic_writer_dispatch','automatic_background_sync','independent_review_of_corrected_version')
    for v in(r,t,result):
        if v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('source_checkpoint')!=209 or v.get('next_action')!=NEXT or any(v.get(k)!=r.get(k)for k in refs)or any(v.get(k)is not False for k in flags)or any(v.get(k)!=0 for k in('actual_model_calls','generation_count','rewrite_count','remaining_repair_budget','old_RC3_remaining_rounds'))or v.get('human_quality_result')!='UNKNOWN'or v.get('source_overall_improvement')!='CONFIRMED_RELATIVE_ONLY'or v.get('corrected_version_human_result')!='UNKNOWN_NOT_YET_READ':raise ValueError('LEXICAL_BUDGET_OR_FALSE_PASS')
    if t.get('result')!=r['result']or r['source_artifact']!=bp['scoped_short_repair']['final_artifact']:raise ValueError('LEXICAL_TASK_OR_ARTIFACT_BINDING')
    original=bound(root,r['source_artifact'],False).decode();corrected=bound(root,r['final_artifact'],False).decode()
    correction=dict(old='你舅舅好容易回来',new='你舅舅好不容易回来',line=9,inserted_character='不',inserted_nonwhite_characters=1)
    if r['correction']!=correction or original.count(correction['old'])!=1 or corrected!=original.replace(correction['old'],correction['new'],1)or sum(not x.isspace()for x in original)!=384 or sum(not x.isspace()for x in corrected)!=385 or original[:original.index(correction['old'])].count('\n')+1!=9:raise ValueError('LEXICAL_EXACT_SINGLE_INSERTION_REQUIRED')
    if h.get('task_id')!=TASK or h.get('source')!='ACTUAL_CURRENT_USER_MESSAGE'or h.get('source_head')!=SOURCE or h.get('source_checkpoint')!=209 or h.get('output')!=r['source_artifact']or h.get('human_exact_feedback')!=EXACT or h.get('review')!=REVIEW or h.get('corrected_artifact_not_yet_human_read')is not True or h.get('prior_records_rewritten')is not False or h.get('requested_change')!={k:correction[k]for k in('old','new','line')}:raise ValueError('LEXICAL_HUMAN_FEEDBACK_SCOPE_DRIFT')
    reports=bp['scoped_short_repair']['raw_reports'];editor=bound(root,reports['editor'])['results'][0]['protected_parts'][2];reader=bound(root,reports['reader'])['reactions'][2]
    quote='“吃完再去吧，”母亲说，“你舅舅好容易回来。”'
    if audit.get('task_id')!=TASK or audit.get('source_head')!=SOURCE or audit.get('source_artifact')!=r['source_artifact']or audit.get('human_feedback')!=r['human_feedback']or audit.get('prior_raw_reports')!=reports or audit.get('editor_observation')!=editor or audit.get('reader_observation')!=reader or editor['quote']!=reader['quote']or editor['quote']!=quote or editor['line']!=reader['line']or editor['line']!=9 or quote not in original or audit.get('actual_model_calls')!=0 or audit.get('old_reports_rewritten')is not False or audit.get('new_review_of_corrected_artifact_claimed')is not False:raise ValueError('LEXICAL_PRIOR_REVIEW_MISS_EVIDENCE_DRIFT')
    if c.get('sequence')!=210 or c.get('stop')is not True or c['action_guard']['project_state_sha256']!=hashlib.sha256((root/'state/project_state.json').read_bytes()).hexdigest():raise ValueError('LEXICAL_CHECKPOINT_OR_HASH_DRIFT')
    for v in(p,c):
        if v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=r['task']['path']or v.get('human_verdict_receipt')!=r['human_feedback']['path']or v.get('latest_human_review')!=REVIEW or v.get('status')!=r['status']or v.get('current_human_gate')!='SOURCE_384_HUMAN_RELATIVE_IMPROVEMENT_CORRECTED_385_HUMAN_UNKNOWN'or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT:raise ValueError('LEXICAL_CURRENT_ENTRY_DRIFT')
    bound(root,r['result_document'],False)
    for path in('START_HERE.md','README.md','AGENTS.md','SKILL.md'):
        entry=(root/path).read_text(encoding='utf8')
        if TASK not in entry or NEXT not in entry or r['final_artifact']['path']not in entry:raise ValueError('LEXICAL_ENTRYPOINT_DRIFT')
    return dict(sequence=210,status=r['status'],next_action=NEXT,historical_checks_passed=83,checks_passed=93,protected_source_file_count=742,source_overall_improvement='CONFIRMED_RELATIVE_ONLY',human_quality_result='UNKNOWN',corrected_version_human_result='UNKNOWN_NOT_YET_READ',new_prose_authorized=False,mainline=old['mainline'],actual_model_calls=0,model_calls_during_validation=0,generation_count_during_validation=0,literary_quality_tested_by_this_script=False)
