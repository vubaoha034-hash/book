"""Pinned history and internal-self9 evidence gate; never certifies human taste."""
from pathlib import Path
import hashlib,importlib.util,inspect,json
def module(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
history=module('standalone_history','frozen_history.py');common=module('standalone_common','verify_prose_repair.py');controller=module('standalone_controller','novel_standalone_short.py');bound=common.bound
SOURCE='38c46c0e6de3099b660aaffe4fe8e5fcf7be6f0d';TASK='NOVEL-STANDALONE-COMPLETE-SHORT-SELF9-20261004-01';NEXT='AWAIT_ACTUAL_HUMAN_SCORE_OF_ONE_STANDALONE_COMPLETE_SHORT'
MUTABLE=('AGENTS.md','README.md','SKILL.md','START_HERE.md','scripts/verify_current_state.py','state/project_state.json','state/continuity/LATEST_CHECKPOINT.json')
LIVE={'updated_at','recorded_at','sequence','stop','action_guard','closed_task_ids','current_focus','status','last_completed_task_id','last_completed_task_contract','next_action','next_required_action','current_human_gate','standalone_short_self9'}
EXACT='首先这种任务不应该再出现，而后你自己再写一个短篇小说，自我评价。直到九分给我看。而后我来打分，最后看看情况如何了'
_baseline=None
def verify(root,p,c):
    global _baseline
    root=Path(root);r=p.get('standalone_short_self9')
    if not r or r!=c.get('standalone_short_self9')or r.get('task_id')!=TASK or r.get('source_head')!=SOURCE or r.get('source_checkpoint')!=210:raise ValueError('STANDALONE_ROUTE_OR_SOURCE_DRIFT')
    source=history.frozen_tree(Path(__file__).resolve().parents[1],SOURCE);bp=json.loads((source/'state/project_state.json').read_bytes());bc=json.loads((source/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    if _baseline is None:_baseline=module('standalone_prior_current','verify_current_state.py').verify(source)
    old=_baseline
    if old['sequence']!=210 or old['checks_passed']!=93 or old['new_prose_authorized']is not False:raise ValueError('STANDALONE_PRIOR_GATES_REQUIRED')
    for live,prior in((p,bp),(c,bc)):
        if {k:v for k,v in live.items()if k not in LIVE}!={k:v for k,v in prior.items()if k not in LIVE}:raise ValueError('STANDALONE_OLD_STATE_OR_HUMAN_FEEDBACK_CHANGED')
    protected=[f.relative_to(source).as_posix()for f in source.rglob('*')if f.is_file()and'__pycache__'not in f.parts and f.relative_to(source).as_posix()not in MUTABLE]
    if len(protected)!=752:raise ValueError('STANDALONE_HISTORY_COUNT_DRIFT')
    for path in protected:
        if not(root/path).is_file()or(root/path).read_bytes()!=(source/path).read_bytes():raise ValueError('STANDALONE_HISTORY_CHANGED: '+path)
    if p['closed_task_ids']!=bp['closed_task_ids']+[TASK]or c['action_guard']['closed_task_ids']!=p['closed_task_ids']or {k:v for k,v in c['action_guard'].items()if k not in('closed_task_ids','project_state_sha256')}!={k:v for k,v in bc['action_guard'].items()if k not in('closed_task_ids','project_state_sha256')}:raise ValueError('STANDALONE_OLD_LOCK_CHANGED')
    a,t,result,settlement,contract,rubric,pending=[bound(root,r[k])for k in('authorization','task','result','settlement','story_contract','score_rubric','pending_human_score')]
    if a.get('task_id')!=TASK or a.get('source_head')!=SOURCE or a.get('source_checkpoint')!=210 or a.get('authority')!=dict(source='ACTUAL_CURRENT_USER_MESSAGE',exact_message=EXACT)or a.get('scope')!=controller.SCOPE or a.get('primary_writer_limit')!=1 or a.get('evidenced_revisions_authorized')is not True or a.get('unchanged_manuscript_repeated_score_calls_authorized')is not False or a.get('internal_self_target')!=9 or a.get('old_RC3_remaining_rounds')!=0 or any(a.get(k)is not False for k in('old_197_character_protection_released','old_story_retcon_authorized','full_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized','internal_score_is_human_quality_proof')):raise ValueError('STANDALONE_AUTHORIZATION_DRIFT')
    if a.get('prior_body')!=bp['scoped_text_correction']['final_artifact']:raise ValueError('STANDALONE_OLD_BODY_BINDING')
    refs=('authorization','final_artifact','delivery_copy','settlement','story_contract','score_rubric','pending_human_score','passes','result_document','language_check_module','report_interpretation_audit','measurements')
    for v in(r,t,result):
        if v.get('task_id')!=TASK or v.get('source_head')!=SOURCE or v.get('source_checkpoint')!=210 or v.get('next_action')!=NEXT or v.get('primary_generation_count')!=1 or v.get('visible_candidate_count')!=1 or v.get('human_score')!='UNKNOWN'or v.get('human_quality_result')!='UNKNOWN'or v.get('old_RC3_remaining_rounds')!=0 or any(v.get(k)is not False for k in('old_197_character_protection_released','full_V5_authorized','AI_quality_certification','full_scene_or_TEST01_promoted','automatic_writer_dispatch','automatic_background_sync'))or any(v.get(k)!=r.get(k)for k in refs):raise ValueError('STANDALONE_RESULT_OR_FALSE_PROMOTION')
    if t.get('result')!=r['result']or rubric.get('task_id')!=TASK or rubric.get('target')!=9 or rubric.get('source')!='COORDINATOR_DECLARED_BEFORE_WRITING'or rubric.get('reviewers_receive_numeric_target')is not False or not contract.get('coordinator_design_check',{}).get('open_design_blockers')==[]:raise ValueError('STANDALONE_DESIGN_OR_RUBRIC_DRIFT')
    threads=[];hashes=[];model_calls=0;successful_calls=0;failed_calls=0;final_reports={};final_artifact=None
    for index,record in enumerate(r['passes']):
        manifests={stage:bound(root,ref)for stage,ref in record['manifests'].items()};jobs={}
        copyedit=record.get('kind')=='COORDINATOR_LOCATED_COPYEDIT'
        if set(manifests)!=({'reviews'}if copyedit else{'writer','reviews'}):raise ValueError('STANDALONE_PASS_MANIFEST_MISSING')
        for stage,m in manifests.items():
            if m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('authorization')!=r['authorization']or m.get('model')!='gpt-6.1-sol'or m.get('reasoning_effort')!='max'or m.get('generation_limit')!=1 or m.get('quality_certification_allowed')is not False or set(m['jobs'])!=({'writer'}if stage=='writer'else{'editor','reader','copyeditor'}):raise ValueError('STANDALONE_MODEL_OR_ROLE_DRIFT')
            jobs.update({role:(job,m['result_dir'])for role,job in m['jobs'].items()})
        body=bound(root,record['artifact'],False).decode();hashes.append(record['artifact']['sha256'])
        if not 1500<=sum(not x.isspace()for x in body)<=2300 or body.startswith('#')or'```'in body:raise ValueError('STANDALONE_COMPLETE_BODY_SCOPE')
        writer=None if copyedit else bound(root,jobs['writer'][0]['packet'])
        if not copyedit and(set(writer)!={'scope','facts','positive_craft_guidance'}or any(x in json.dumps(writer,ensure_ascii=False)for x in('human_feedback','刘先生','self_evaluation','score_rubric','EDITORIAL_CLEAR','target_score'))):raise ValueError('STANDALONE_WRITER_ANSWER_LEAKAGE')
        if index==0 and(copyedit or writer['facts']!=contract['writer_facts']):raise ValueError('STANDALONE_WRITER_FACT_DRIFT')
        if index>0:
            goals=bound(root,record['revision_goals'])
            if not goals.get('located_issues')or goals.get('prior_artifact')!=r['passes'][index-1]['artifact']:raise ValueError('STANDALONE_REVISION_WITHOUT_EVIDENCE')
            prior_body=bound(root,goals['prior_artifact'],False).decode()
            if copyedit:
                for change in goals.get('exact_changes',[]):
                    if not change.get('reason')or prior_body.count(change.get('old',''))!=1:raise ValueError('STANDALONE_UNBOUNDED_COPYEDIT')
                    prior_body=prior_body.replace(change['old'],change['new'],1)
                if not goals.get('exact_changes')or body!=prior_body:raise ValueError('STANDALONE_COPYEDIT_CHANGED_OTHER_PROSE')
            elif writer['facts'].get('source_text')!=prior_body:raise ValueError('STANDALONE_REVISION_SOURCE_DRIFT')
        reports={}
        for role,(job,directory)in jobs.items():
            if role in record.get('failed_roles',[]):
                rt=bound(root,record['runtimes'][role]);cfg=rt.get('resolved_thread_settings',{})
                if index!=0 or role!='copyeditor'or rt.get('report_received')is not False or rt.get('status')!='BLOCKED'or rt.get('error_code')!='TIMEOUT_NO_SUCCESSFUL_OUTPUT'or cfg.get('model')!='gpt-6.1-sol'or cfg.get('reasoningEffort')!='max'or cfg.get('sandbox')!={'type':'readOnly','networkAccess':False}or cfg.get('instructionSources')!=[]or cfg.get('runtimeWorkspaceRoots')!=[]or rt.get('packet')!=job['packet']or not rt.get('thread_id'):raise ValueError('STANDALONE_FAILED_CALL_NOT_PRESERVED')
                model_calls+=1;failed_calls+=1;threads.append(rt['thread_id']);continue
            saved=common.TASK,common.runner;common.TASK,common.runner=TASK,controller.engine;controller.engine.DIRECTORY=directory
            try:
                if job.get('reasoning_effort','max')=='max':rt=common.runtime_check(root,record['runtimes'][role],role,job)
                else:
                    if role not in('copyeditor','editor','reader')or job.get('reasoning_effort')!='high':raise ValueError('STANDALONE_UNAUTHORIZED_EFFORT_FALLBACK')
                    fallback=bound(root,manifests['reviews']['runtime_fallback']);failed=bound(root,fallback['failed_runtime'])
                    if failed.get('error_code')!='TIMEOUT_NO_SUCCESSFUL_OUTPUT'or failed.get('report_received')is not False or fallback.get('requested_fallback_effort')!='high':raise ValueError('STANDALONE_NO_EVIDENCED_FALLBACK')
                    if role!='copyeditor':
                        earlier=bound(root,fallback.get('successful_max_reviews',{}).get(role,{}));goals=bound(root,fallback.get('targeted_revision',{}))
                        if fallback.get('mode')!='TARGETED_LOCAL_WORDING_RECHECK_AFTER_ACTUAL_MAX_REVIEWS'or earlier.get('report_received')is not True or earlier.get('turn_status')!='completed'or earlier.get('resolved_thread_settings',{}).get('reasoningEffort')!='max'or goals.get('new_plot_or_fact_changes')is not False or not goals.get('exact_changes'):raise ValueError('STANDALONE_TARGETED_EFFORT_WITHOUT_PRIOR_MAX_EVIDENCE')
                    scope={**common.__dict__};exec(compile(inspect.getsource(common.runtime_check).replace("'max'","'high'"),'standalone_observed_high_runtime_guard','exec'),scope)
                    rt=scope['runtime_check'](root,record['runtimes'][role],role,job)
            finally:common.TASK,common.runner=saved
            model_calls+=1;successful_calls+=1;threads.append(rt['thread_id'])
            if rt['raw_report']!=(record['artifact']if role=='writer'else record['raw_reports'][role]):raise ValueError('STANDALONE_RAW_REPORT_BINDING')
            if role=='writer':continue
            packet=bound(root,job['packet']);controller.review.validate_packet(packet)
            if packet['samples']!=[dict(artifact_id='T211'+record['id'],original_sha256=record['artifact']['sha256'],text=body)]:raise ValueError('STANDALONE_REVIEW_WRONG_BODY')
            if role=='reader'and(set(packet)!={'packet_version','job_id','work_kind','medium','excerpt_position','samples'}or any(x in json.dumps(packet,ensure_ascii=False)for x in('score_rubric','target_score','self_evaluation','human_feedback','刘先生'))):raise ValueError('STANDALONE_COLD_CONTEXT_LEAKAGE')
            if role=='editor'and packet.get('facts')!=contract['review_facts']:raise ValueError('STANDALONE_EDITOR_FACT_DRIFT')
            if role=='copyeditor'and packet.get('facts')!=[]:raise ValueError('STANDALONE_COPYEDITOR_CONTEXT_DRIFT')
            report=controller.review.parse_report(bound(root,record['raw_reports'][role],False));evidence=controller.audit(packet,report,rt);persisted=bound(root,record['evidence'][role])
            if evidence['errors']or any(persisted.get(k)!=v for k,v in evidence.items()):raise ValueError('STANDALONE_REPORT_EVIDENCE_DRIFT')
            reports[role]=report
        final_reports,final_artifact=reports,record['artifact']
    if len(set(threads))!=len(threads)or len(set(hashes))!=len(hashes)or not hashes or r.get('actual_verified_model_calls')!=model_calls or r.get('successful_model_calls')!=successful_calls or r.get('failed_model_calls')!=failed_calls or r.get('internal_repair_count')!=len(hashes)-1 or r['final_artifact']!=final_artifact:raise ValueError('STANDALONE_REPEATED_CALL_OR_FINAL_BODY_DRIFT')
    body=bound(root,r['final_artifact'],False).decode();total=controller.validate_self9(settlement)
    if bound(root,r['delivery_copy'],False).decode()!=body or settlement.get('delivery_copy')!=r['delivery_copy']:raise ValueError('STANDALONE_DELIVERY_COPY_DRIFT')
    if settlement.get('task_id')!=TASK or settlement.get('final_artifact')!=r['final_artifact']or settlement.get('raw_reports_rewritten')is not False or settlement.get('current_reports')!=r['passes'][-1]['raw_reports']or r.get('internal_self_score')!=total:raise ValueError('STANDALONE_SETTLEMENT_DRIFT')
    for d in settlement['self_evaluation']['dimensions']:
        offset=body.find(d['quote'])
        if offset<0 or body[:offset].count('\n')+1!=d['line']:raise ValueError('STANDALONE_SELF_SCORE_QUOTE_DRIFT')
    if final_reports['editor']['results'][0]['verdict']!='EDITORIAL_CLEAR'or final_reports['copyeditor']['results'][0]['verdict']!='FACT_CLEAR'or final_reports['reader']['wants_to_continue']!='YES':raise ValueError('STANDALONE_CURRENT_REVIEW_UNRESOLVED')
    if pending.get('artifact')!=r['final_artifact']or pending.get('delivery_copy')!=r['delivery_copy']or pending.get('human_score')!='UNKNOWN'or pending.get('internal_self_score')!=total or pending.get('score_comparison')!='PENDING_ACTUAL_HUMAN_SCORE':raise ValueError('STANDALONE_PENDING_HUMAN_SCORE_DRIFT')
    if c.get('sequence')!=211 or c.get('stop')is not True or c['action_guard']['project_state_sha256']!=hashlib.sha256((root/'state/project_state.json').read_bytes()).hexdigest():raise ValueError('STANDALONE_CHECKPOINT_HASH_DRIFT')
    for v in(p,c):
        if v.get('last_completed_task_id')!=TASK or v.get('last_completed_task_contract')!=r['task']['path']or v.get('status')!=r['status']or v.get('current_human_gate')!='STANDALONE_COMPLETE_SHORT_INTERNAL_9_HUMAN_SCORE_UNKNOWN'or v.get('next_action')!=NEXT or v.get('next_required_action')!=NEXT:raise ValueError('STANDALONE_CURRENT_CURSOR_DRIFT')
    bound(root,r['result_document'],False)
    for k in('language_check_module','report_interpretation_audit','measurements'):bound(root,r[k],False)
    for path in('START_HERE.md','README.md','AGENTS.md','SKILL.md'):
        entry=(root/path).read_text(encoding='utf8')
        if TASK not in entry or NEXT not in entry or r['delivery_copy']['path']not in entry:raise ValueError('STANDALONE_ENTRYPOINT_DRIFT')
    return dict(sequence=211,status=r['status'],next_action=NEXT,historical_checks_passed=93,checks_passed=105,protected_source_file_count=752,internal_self_score=total,human_score='UNKNOWN',human_quality_result='UNKNOWN',new_prose_authorized=False,mainline=old['mainline'],actual_verified_model_calls=model_calls,successful_model_calls=successful_calls,failed_model_calls=failed_calls,internal_repair_count=len(hashes)-1,model_calls_during_validation=0,generation_count_during_validation=0,literary_quality_tested_by_this_script=False)
