"""One bounded clarity repair; reuse the verified isolated transport and audits."""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('clarity_transport',ROOT/'scripts/novel_story_trial.py')
base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
engine,review,roles,ISOLATION=base.engine,base.review,base.roles,base.ISOLATION
def select(path):
    p=(ROOT/path).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file():raise ValueError('CLARITY_MANIFEST_MISSING')
    m=review.read(p);a=json.loads(review.bound(m['authorization']))
    if (m.get('schema_version')!='one-local-clarity-repair-manifest/v1' or m.get('task_id')!=a.get('task_id') or m.get('source_head')!=a.get('source_head') or
        a.get('authority',{}).get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or not a['authority'].get('exact_message') or
        a.get('scope')!='ONE_LOCAL_CLARITY_REPAIR_OF_SAME_NEW_STORY_SHORT_ONLY' or a.get('repair_limit')!=1 or
        a.get('old_RC3_remaining_rounds')!=0 or any(a.get(k) is not False for k in ('old_197_character_protection_released','new_plot_or_life_facts_authorized','full_scene_or_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized')) or
        m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or m.get('generation_limit')!=1 or m.get('quality_certification_allowed') is not False):raise ValueError('CLARITY_PERMISSION_OR_BUDGET_DRIFT')
    directory=m.get('result_dir','')
    if not directory.startswith('state/reviews/') or not (ROOT/directory).resolve().is_relative_to(ROOT):raise ValueError('CLARITY_DIRECTORY_OUTSIDE_REPOSITORY')
    for k,v in {'TASK':m['task_id'],'SOURCE':m['source_head'],'DIRECTORY':directory,'MANIFEST':path}.items():setattr(engine,k,v)
    def load():
        if review.read(ROOT/path)!=m:raise ValueError('MANIFEST_CHANGED_DURING_RUN')
        review.bound(m['authorization']);return m,a
    engine.load=load;return m,a
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('run','audit'));p.add_argument('--manifest',required=True)
    p.add_argument('--role',required=True,choices=('writer','editor','reader'));a=p.parse_args();select(a.manifest)
    engine.run(a.role) if a.action=='run' else base.audit(a.role)
