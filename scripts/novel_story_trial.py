"""Run one explicitly authorized new-story short with the existing transport."""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('story_trial_transport',ROOT/'scripts/novel_prose_repair.py')
engine=importlib.util.module_from_spec(s);s.loader.exec_module(engine)
review,roles,ISOLATION=engine.review,engine.roles,engine.ISOLATION
def select(path):
    resolved=(ROOT/path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():raise ValueError('MANIFEST_MISSING_OR_OUTSIDE_REPOSITORY')
    m=review.read(resolved);a=json.loads(review.bound(m['authorization']))
    if (m.get('schema_version')!='new-story-short-manifest/v1' or m.get('task_id')!=a.get('task_id') or m.get('source_head')!=a.get('source_head') or
        m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or m.get('generation_limit')!=1 or
        a.get('authority',{}).get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or not a['authority'].get('exact_message') or
        a.get('scope')!='ONE_NEW_STORY_300_500_CHARACTER_OPENING_ONLY_OLD_STORY_PAUSED_PRESERVED' or
        a.get('old_RC3_remaining_rounds')!=0 or a.get('old_197_character_protection_released') is not False or
        a.get('full_scene_or_V5_authorized') is not False or a.get('multiple_visible_candidates_authorized') is not False or
        a.get('background_tasks_authorized') is not False or a.get('old_story_retcon_authorized') is not False or
        a.get('primary_writer_limit')!=1 or a.get('maximum_evidenced_repairs')!=1):raise ValueError('NEW_STORY_EXPLICIT_SCOPE_PERMISSION_REQUIRED')
    directory=m.get('result_dir','')
    if not directory.startswith('state/reviews/') or not (ROOT/directory).resolve().is_relative_to(ROOT):raise ValueError('RESULT_DIRECTORY_OUTSIDE_REPOSITORY')
    for k,v in {'TASK':m['task_id'],'SOURCE':m['source_head'],'DIRECTORY':directory,'MANIFEST':path}.items():setattr(engine,k,v)
    def load():
        fresh=review.read(ROOT/path)
        if fresh!=m:raise ValueError('MANIFEST_CHANGED_DURING_RUN')
        review.bound(m['authorization'])
        return m,a
    engine.load=load
    return m,a

def audit(role):
    m,_=engine.load();job=m['jobs'][role];runtime=review.read(ROOT/engine.DIRECTORY/f'{role}.runtime.json')
    if not runtime.get('report_received') or runtime.get('turn_status')!='completed':raise ValueError('MISSING_OR_FAILED_REVIEW')
    packet=json.loads(review.bound(job['packet']));report=review.parse_report(review.bound(runtime['raw_report']))
    result=roles.audit_reader(packet,report,runtime,'NEW_STORY_OPENING_EXCERPT') if role=='reader' else review.audit_report(packet,report,runtime,'NEW_STORY_OPENING_EXCERPT')
    result.update(task_id=engine.TASK,role=role,packet=job['packet'],raw_report=runtime['raw_report'])
    review.dump(ROOT/engine.DIRECTORY/f'{role}.evidence.json',result,exclusive=True)
    print(json.dumps({'role':role,'errors':result['errors'],'quote_records':len(result['located_quotes']),'corrections':result['position_corrections']}))
    if result['errors']:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('run','audit'))
    p.add_argument('--manifest',required=True);p.add_argument('--role',choices=('writer','editor','reader'),required=True);a=p.parse_args()
    select(a.manifest)
    engine.run(a.role) if a.action=='run' else audit(a.role)
