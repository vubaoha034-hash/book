"""Scoped hook trial using the existing isolated transport and evidence auditors."""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('hook_transport',ROOT/'scripts/novel_prose_repair.py')
engine=importlib.util.module_from_spec(s);s.loader.exec_module(engine)
TASK='NOVEL-OPENING-HOOK-TRIAL-AFTER-RETENTION-FAIL-20261003-01'
SOURCE='5b6e5cb1a23ecb0be1b9f6a92a18c935f4198a3a'
DIRECTORY='state/reviews/hook-trial-20261003'
DELIVERY='delivery/hook-trial-20261003'
MANIFEST='config/novel-hook-trial-20261003.json'
HUMAN='state/review_receipts/NOVEL_PROSE_REPAIR_375_HUMAN_RETENTION_FAIL_20261003.json'
AUTH='state/review_receipts/NOVEL_OPENING_HOOK_TRIAL_AUTHORIZATION_20261003.json'
EXACT='不想。  因为真的一点让人看下去的欲望都没有。毫无欲望，没有一点悬念让人觉得好看的。   ai味道这次变轻了很多。'
for key in ('TASK','SOURCE','DIRECTORY','DELIVERY','MANIFEST','HUMAN','AUTH','EXACT'):setattr(engine,key,globals()[key])
review,roles,ISOLATION=engine.review,engine.roles,engine.ISOLATION

def load():
    m=review.read(ROOT/MANIFEST);auth=json.loads(review.bound(m['authorization']))
    human=json.loads(review.bound(auth['human_feedback']))
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or
        auth.get('task_id')!=TASK or auth.get('source_head')!=SOURCE or auth.get('source_checkpoint')!=200 or
        auth.get('source')!='STANDING_USER_AUTONOMY_AND_ACTUAL_FROZEN_TEST_FAILURE' or
        auth.get('primary_writer_limit')!=1 or auth.get('maximum_evidenced_repairs')!=1 or
        auth.get('intermediate_user_authorization_required') is not False or auth.get('old_RC3_remaining_rounds')!=0 or
        any(auth.get(k) is not False for k in ('old_197_character_protection_released','new_life_facts_authorized','full_v5_authorized',
            'multiple_visible_candidates_allowed','background_tasks_authorized','goal_or_world_or_ending_change_authorized')) or
        human.get('human_exact_feedback')!=EXACT or human.get('outcome')!='FAIL'):
        raise ValueError('HOOK_TRIAL_SCOPE_OR_ACTUAL_FAILURE_DRIFT')
    prior=review.read(ROOT/'state/project_state.json')['opening_prose_repair']
    if human.get('output')!=prior['final_artifact']:raise ValueError('HOOK_WRONG_REJECTED_BODY')
    review.bound(human['output'])
    standing=json.loads(review.bound(auth['standing_user_authorization']))
    if standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False:
        raise ValueError('HOOK_NO_STANDING_EXECUTION_PERMISSION')
    return m,auth

engine.load=load
run,audit=engine.run,engine.audit
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('run','audit'))
    p.add_argument('--role',choices=('diagnosis','writer','facts','editor','reader'),required=True)
    p.add_argument('--transport-recovery',action='store_true',help='One separately recorded retry after a failed turn with no report')
    p.add_argument('--repair-stage',action='store_true',help='One approved factual repair and its fresh fact check')
    a=p.parse_args()
    if a.repair_stage:
        if a.role not in ('writer','facts') or a.transport_recovery:raise ValueError('REPAIR_STAGE_ROLE_DRIFT')
        MANIFEST='config/novel-hook-repair-20261003.json'
        engine.MANIFEST=MANIFEST;engine.DIRECTORY=DIRECTORY+'/repair'
    if a.transport_recovery:
        m,_=load();failure=review.read(ROOT/DIRECTORY/f'{a.role}.runtime.json')
        if (a.role!='diagnosis' or failure.get('report_received') is not False or failure.get('turn_status')!='failed' or
            failure.get('completed_item_types')!=['userMessage'] or m.get('transport_recovery_limit')!=1):
            raise ValueError('RECOVERY_REQUIRES_FAILED_NO_OUTPUT_TURN')
        engine.DIRECTORY=DIRECTORY+'/transport-recovery'
    run(a.role) if a.action=='run' else audit(a.role)
