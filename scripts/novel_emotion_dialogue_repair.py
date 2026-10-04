"""Reuse the isolated transport for one bounded same-story repair."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('emotion_dialogue_transport',ROOT/'scripts/novel_story_trial.py')
base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
engine,review,roles=base.engine,base.review,base.roles
def select(path):
    q=(ROOT/path).resolve()
    if not q.is_relative_to(ROOT):raise ValueError('MANIFEST_OUTSIDE_REPOSITORY')
    m=review.read(q);a=json.loads(review.bound(m['authorization']))
    if (m.get('task_id')!=a.get('task_id') or m.get('source_head')!=a.get('source_head') or
        a.get('scope')!='ONE_SAME_STORY_EMOTION_AND_DIALOGUE_REPAIR_300_500_ONLY' or a.get('writer_limit')!=1 or
        a.get('standing_authorization',{}).get('path')!='state/review_receipts/NOVEL_AUTONOMOUS_TO_HUMAN_AUTHORIZATION_20261003.json' or
        a.get('old_RC3_remaining_rounds')!=0 or any(a.get(k) is not False for k in ('new_plot_or_life_facts_authorized','old_197_character_protection_released','full_scene_or_V5_authorized','multiple_visible_candidates_authorized','background_tasks_authorized')) or
        m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or m.get('generation_limit')!=1 or m.get('quality_certification_allowed') is not False):raise ValueError('EMOTION_DIALOGUE_SCOPE_DRIFT')
    review.bound(a['standing_authorization']);review.bound(a['human_feedback']);review.bound(a['source_artifact'])
    if not m['result_dir'].startswith('state/reviews/') or not (ROOT/m['result_dir']).resolve().is_relative_to(ROOT):raise ValueError('RESULT_DIRECTORY_OUTSIDE_REPOSITORY')
    for k,v in {'TASK':m['task_id'],'SOURCE':m['source_head'],'DIRECTORY':m['result_dir'],'MANIFEST':path}.items():setattr(engine,k,v)
    def load():
        if review.read(q)!=m:raise ValueError('MANIFEST_CHANGED_DURING_RUN')
        review.bound(m['authorization']);return m,a
    engine.load=load;return m,a
def audit(role):base.audit(role)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=('run','audit'));p.add_argument('--manifest',required=True);p.add_argument('--role',choices=('diagnosis','writer','editor','reader'),required=True)
    a=p.parse_args();select(a.manifest);engine.run(a.role) if a.action=='run' else audit(a.role)
