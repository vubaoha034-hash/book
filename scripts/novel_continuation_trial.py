"""One 300–500-character continuation, using the existing isolated transport."""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('continuation_transport',ROOT/'scripts/novel_prose_repair.py')
engine=importlib.util.module_from_spec(s);s.loader.exec_module(engine)
TASK='NOVEL-SAME-SCENE-ONE-CONTINUATION-SHORT-20261003-01'
SOURCE='bfa925c353aef6d6b5a63b6e42833b02f7e3583d'
DIRECTORY='state/reviews/continuation-short-20261003'
DELIVERY='delivery/continuation-short-20261003'
MANIFEST='config/novel-continuation-short-20261003.json'
AUTH='state/review_receipts/NOVEL_CONTINUATION_SHORT_AUTHORIZATION_20261003.json'
for k in ('TASK','SOURCE','DIRECTORY','DELIVERY','MANIFEST','AUTH'):setattr(engine,k,globals()[k])
review,roles,ISOLATION=engine.review,engine.roles,engine.ISOLATION
def load():
    m=review.read(ROOT/MANIFEST);auth=json.loads(review.bound(m['authorization']))
    human=json.loads(review.bound(auth['opening_human_feedback']));standing=json.loads(review.bound(auth['standing_user_authorization']))
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or
        auth.get('task_id')!=TASK or auth.get('source_head')!=SOURCE or auth.get('source_checkpoint')!=203 or
        auth.get('source')!='STANDING_USER_AUTONOMY_FOR_ONE_BOUNDED_SAME_SCENE_CONTINUATION' or
        auth.get('primary_writer_limit')!=1 or auth.get('maximum_evidenced_repairs')!=1 or auth.get('new_segment_character_range')!=[300,500] or
        auth.get('intermediate_user_authorization_required') is not False or auth.get('old_RC3_remaining_rounds')!=0 or
        any(auth.get(k) is not False for k in ('old_197_character_protection_released','new_life_facts_authorized','full_v5_authorized',
            'full_scene_or_TEST01_promoted','multiple_visible_candidates_allowed','background_tasks_authorized','goal_or_world_or_ending_change_authorized')) or
        human.get('outcome')!='SHORT_LIMITED_PASS' or human.get('review',{}).get('wants_to_continue') is not True or
        human.get('review',{}).get('continuation_strength')!='LOW_EXPLICITLY_QUALIFIED' or
        human.get('review',{}).get('robotic_interaction_verdict')!='POSITIVE_NOT_MARKEDLY_ROBOTIC_IN_THIS_SHORT' or
        standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False):
        raise ValueError('CONTINUATION_SCOPE_OR_PERMISSION_DRIFT')
    if human.get('output')!=auth.get('previous_excerpt'):raise ValueError('CONTINUATION_WRONG_PREVIOUS_EXCERPT')
    review.bound(auth['previous_excerpt'])
    return m,auth
engine.load=load
run,audit=engine.run,engine.audit
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('run','audit'))
    parser.add_argument('--role',choices=('writer','facts','editor','reader'),required=True)
    parser.add_argument('--repair-stage',action='store_true')
    args=parser.parse_args()
    if args.repair_stage:
        if args.role not in ('writer','facts'):raise ValueError('CONTINUATION_REPAIR_ROLE_DRIFT')
        MANIFEST='config/novel-continuation-short-repair-20261003.json';engine.MANIFEST=MANIFEST;engine.DIRECTORY=DIRECTORY+'/repair'
    run(args.role) if args.action=='run' else audit(args.role)
