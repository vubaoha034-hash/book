"""Run one frozen standalone-short job through the existing isolated transport."""
from pathlib import Path
import argparse,importlib.util,inspect,json
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('standalone_transport',ROOT/'scripts/novel_prose_repair.py');engine=importlib.util.module_from_spec(s);s.loader.exec_module(engine)
review=engine.review
SCOPE='ONE_STANDALONE_COMPLETE_SHORT_WITH_EVIDENCED_INTERNAL_REVISION_TO_SELF9'
REPORT_SCOPE='STANDALONE_COMPLETE_SHORT'
def select(path):
    q=(ROOT/path).resolve()
    if not q.is_relative_to(ROOT)or not q.is_file():raise ValueError('MANIFEST_OUTSIDE_REPOSITORY')
    m=review.read(q);a=json.loads(review.bound(m['authorization']))
    if m.get('schema_version')!='standalone-short-manifest/v1'or m.get('task_id')!=a.get('task_id')or m.get('source_head')!=a.get('source_head')or a.get('scope')!=SCOPE or a.get('authority',{}).get('source')!='ACTUAL_CURRENT_USER_MESSAGE'or not a['authority'].get('exact_message')or m.get('model')!='gpt-6.1-sol'or m.get('reasoning_effort')!='max'or m.get('generation_limit')!=1 or m.get('quality_certification_allowed')is not False or a.get('old_RC3_remaining_rounds')!=0 or any(a.get(k)is not False for k in('old_197_character_protection_released','old_story_retcon_authorized','full_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized')):raise ValueError('STANDALONE_EXPLICIT_SCOPE_REQUIRED')
    directory=m.get('result_dir','')
    if not directory.startswith('state/reviews/standalone-short-20261004/')or not(ROOT/directory).resolve().is_relative_to(ROOT):raise ValueError('RESULT_DIRECTORY_SCOPE_DRIFT')
    if any(v.get('max_calls')!=1 for v in m['jobs'].values()):raise ValueError('ONE_FROZEN_JOB_ONE_CALL')
    for role,job in m['jobs'].items():
        effort=job.get('reasoning_effort','max')
        if effort!='max':
            fallback=json.loads(review.bound(m.get('runtime_fallback',{})))
            failed=json.loads(review.bound(fallback['failed_runtime']))
            if effort!='high'or failed.get('error_code')!='TIMEOUT_NO_SUCCESSFUL_OUTPUT'or failed.get('report_received')is not False or fallback.get('requested_fallback_effort')!='high'or fallback.get('same_model')!='gpt-6.1-sol':raise ValueError('EVIDENCED_RUNTIME_ADAPTATION_REQUIRED')
            if role!='copyeditor':
                prior=json.loads(review.bound(fallback.get('successful_max_reviews',{}).get(role,{})))
                goals=json.loads(review.bound(fallback.get('targeted_revision',{})))
                if role not in('editor','reader')or fallback.get('mode')!='TARGETED_LOCAL_WORDING_RECHECK_AFTER_ACTUAL_MAX_REVIEWS'or prior.get('report_received')is not True or prior.get('turn_status')!='completed'or prior.get('resolved_thread_settings',{}).get('reasoningEffort')!='max'or goals.get('new_plot_or_fact_changes')is not False or not goals.get('exact_changes'):raise ValueError('SUCCESSFUL_MAX_REVIEW_AND_BOUNDED_COPYEDIT_REQUIRED')
    for k,v in dict(TASK=m['task_id'],SOURCE=m['source_head'],DIRECTORY=directory,MANIFEST=path).items():setattr(engine,k,v)
    def load():
        if review.read(q)!=m:raise ValueError('MANIFEST_CHANGED_DURING_RUN')
        review.bound(m['authorization']);return m,a
    engine.load=load;return m,a
def run_job(role,m):
    effort=m['jobs'][role].get('reasoning_effort','max')
    if effort!='max':
        # Existing transport is reused with the declared effort at every RPC and
        # its returned-settings check. No historical script or guard is edited.
        source=inspect.getsource(engine.run).replace("'max'",repr(effort))
        exec(compile(source,'standalone_declared_effort_transport','exec'),engine.__dict__)
    engine.run(role)
def audit(packet,report,runtime):
    review.validate_packet(packet);sample=packet['samples'][0];errors=[];located=[]
    if runtime.get('report_received')is not True or runtime.get('turn_status')!='completed':errors.append('NO_COMPLETED_REPORT')
    expected=dict(model=runtime['resolved_thread_settings']['model'],reasoning_effort=runtime['resolved_thread_settings']['reasoningEffort'],isolation=runtime['isolation'])
    if report.get('job_id')!=packet['job_id']or report.get('work_kind')!=packet['work_kind']or report.get('runtime_context')!=expected:errors.append('REPORT_CONTEXT_OR_JOB_DRIFT')
    if packet['work_kind']=='COLD_SCREEN':
        result=report
        if report.get('wants_to_continue')not in('YES','NO','UNCERTAIN')or not report.get('ending_response')or not report.get('reader_profile'):errors.append('INCOMPLETE_READER_RESPONSE')
    else:
        if len(report.get('results',[]))!=1:errors.append('REPORT_RESULT_COUNT_DRIFT')
        result=report.get('results',[{}])[0]
        allowed={'EDITORIAL_REVIEW':{'EDITORIAL_CLEAR','REVISE','INSUFFICIENT','BLOCKED'},'FACT_AUDIT':{'FACT_CLEAR','REVISE','INSUFFICIENT','BLOCKED'}}
        if result.get('verdict')not in allowed[packet['work_kind']]:errors.append('INVALID_EDITOR_VERDICT')
    if result.get('artifact_id')!=sample['artifact_id']or result.get('original_sha256')!=sample['original_sha256']or result.get('scope')!=REPORT_SCOPE:errors.append('WRONG_ARTIFACT_OR_SCOPE')
    if not result.get('unknowns'):errors.append('LIMITATIONS_MISSING')
    if any(k in result for k in('score','target_score','human_score')):errors.append('UNREQUESTED_NUMERIC_REVIEW_TARGET')
    for finding in result.get('findings',[]):
        if finding.get('basis')not in('TEXT_FACT','EDITOR_HYPOTHESIS')or finding.get('severity')not in('BLOCKER','MAJOR','MINOR','STYLE')or not all(finding.get(k)for k in('explanation','reading_impact','minimum_scope','recheck')):errors.append('INCOMPLETE_OR_UNLABELLED_FINDING')
    if packet['work_kind']=='FACT_AUDIT'and len(result.get('line_pass',[]))<3:errors.append('COPYEDITOR_LINE_PASS_MISSING')
    def walk(v):
        if isinstance(v,dict):
            if'quote'in v:
                q=v['quote'];off=sample['text'].find(q)if q else -1
                actual=sample['text'][:off].count('\n')+1 if off>=0 else None
                row=dict(quote=q,reported_line=v.get('line'),actual_line=actual,offset=off,exact_quote_found=off>=0,line_matches=v.get('line')==actual);located.append(row)
                if off<0:errors.append('NONEXISTENT_QUOTE')
            for child in v.values():walk(child)
        elif isinstance(v,list):
            for child in v:walk(child)
    walk(result)
    if len(located)<3:errors.append('EVIDENCE_INSUFFICIENT')
    return dict(status='REPORT_EVIDENCE_LOCATED_REQUIRES_COORDINATOR_SETTLEMENT'if not errors else'REJECTED_REPORT',errors=sorted(set(errors)),located_quotes=located,position_corrections=[v for v in located if v['exact_quote_found']and not v['line_matches']],raw_report_rewritten=False,human_quality_result_changed=False,automatic_quality_certification=False)

def validate_self9(settlement):
    """Check declared release evidence; a self-score never becomes a human result."""
    dimensions=settlement.get('self_evaluation',{}).get('dimensions',[])
    if len(dimensions)!=5 or {d.get('id')for d in dimensions}!={'opening','clarity_language','emotion','causality','payoff'}:raise ValueError('SELF9_DIMENSIONS_MISSING')
    if any(not isinstance(d.get('score'),(int,float))or not 0<=d['score']<=2 or not d.get('quote')or not d.get('reason')or not d.get('line')for d in dimensions):raise ValueError('SELF9_SCORE_EVIDENCE_MISSING')
    total=round(sum(d['score']for d in dimensions),3)
    if total<9 or settlement['self_evaluation'].get('total')!=total:raise ValueError('SELF9_THRESHOLD_NOT_REACHED')
    if settlement.get('open_major_or_blocker')!=[]or settlement.get('quote_or_fact_errors')!=[]or settlement.get('line_pass_complete')is not True or settlement.get('complete_story')is not True:raise ValueError('SELF9_OPEN_PROBLEMS')
    if set(settlement.get('current_reports',{}))!={'editor','reader','copyeditor'}or settlement.get('all_current_reports_successful_and_bound')is not True:raise ValueError('SELF9_REPORTS_REQUIRED')
    if settlement.get('human_score')!='UNKNOWN'or settlement.get('human_quality_result')!='UNKNOWN'or settlement.get('AI_quality_certification')is not False:raise ValueError('SELF9_FALSE_HUMAN_PROMOTION')
    return total
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('run','audit'));parser.add_argument('--manifest',required=True);parser.add_argument('--role',required=True,choices=('writer','editor','reader','copyeditor'));args=parser.parse_args();m,a=select(args.manifest)
    if args.action=='run':run_job(args.role,m)
    else:
        rt=review.read(ROOT/engine.DIRECTORY/f'{args.role}.runtime.json')
        if not rt.get('report_received')or rt.get('turn_status')!='completed':raise ValueError('MISSING_SUCCESSFUL_REPORT')
        job=m['jobs'][args.role];packet=json.loads(review.bound(job['packet']));report=review.parse_report(review.bound(rt['raw_report']));evidence=audit(packet,report,rt)
        evidence.update(task_id=m['task_id'],role=args.role,packet=job['packet'],raw_report=rt['raw_report']);review.dump(ROOT/engine.DIRECTORY/f'{args.role}.evidence.json',evidence,exclusive=True)
        print(json.dumps(dict(role=args.role,errors=evidence['errors'],quotes=len(evidence['located_quotes']),position_corrections=len(evidence['position_corrections']))));raise SystemExit(bool(evidence['errors']))
