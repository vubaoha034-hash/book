"""One scoped repair after an actual human prose/retention rejection.

Reuses the isolated Codex transport and auditors. Every job consumes one
exclusive attempt; history and reports never enter the fresh writer/reader.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,queue,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TASK='NOVEL-OPENING-PROSE-REPAIR-AFTER-HUMAN-FAIL-20261003-01'
SOURCE='df1e08a59373e9777bf478b85ebe0707c4dfdef0'
DIRECTORY='state/reviews/prose-repair-20261003'
DELIVERY='delivery/prose-repair-20261003'
MANIFEST='config/novel-prose-repair-20261003.json'
HUMAN='state/review_receipts/NOVEL_AUTONOMOUS_OPENING_390_HUMAN_FAIL_20261003.json'
AUTH='state/review_receipts/NOVEL_OPENING_PROSE_REPAIR_AUTHORIZATION_20261003.json'
EXACT='不愿意，ai味道依旧很重。是那种开头开始就很重的。感觉写小说根本不会用这种文笔去写的感觉。感觉就特别特别别扭。'
ISOLATION='FRESH_PROCESS_FRESH_EPHEMERAL_THREAD_ENVIRONMENTS_DISABLED_NO_HISTORY'
spec=importlib.util.spec_from_file_location('prose_transport',ROOT/'scripts/codex_review.py')
review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)
spec=importlib.util.spec_from_file_location('prose_reader_auditor',ROOT/'scripts/novel_two_role_review.py')
roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)


def load():
    m=review.read(ROOT/MANIFEST);auth=json.loads(review.bound(m['authorization']))
    human=json.loads(review.bound(auth['human_feedback']))
    if (m.get('task_id')!=TASK or m.get('source_head')!=SOURCE or m.get('model')!='gpt-6.1-sol' or m.get('reasoning_effort')!='max' or
            auth.get('task_id')!=TASK or auth.get('source_head')!=SOURCE or auth.get('source_checkpoint')!=199 or
            auth.get('source')!='STANDING_USER_AUTONOMY_AND_ACTUAL_FROZEN_TEST_FAILURE' or
            auth.get('primary_writer_limit')!=1 or auth.get('maximum_evidenced_repairs')!=1 or
            auth.get('intermediate_user_authorization_required') is not False or auth.get('old_RC3_remaining_rounds')!=0 or
            any(auth.get(k) is not False for k in ('old_197_character_protection_released','new_life_facts_authorized','full_v5_authorized',
                'multiple_visible_candidates_allowed','background_tasks_authorized','goal_or_world_or_ending_change_authorized')) or
            human.get('human_exact_feedback')!=EXACT or human.get('outcome')!='FAIL'):
        raise ValueError('PROSE_REPAIR_SCOPE_OR_ACTUAL_FAILURE_DRIFT')
    standing=json.loads(review.bound(auth['standing_user_authorization']))
    if standing.get('source')!='ACTUAL_CURRENT_USER_MESSAGE' or standing.get('intermediate_user_authorization_required') is not False:
        raise ValueError('NO_STANDING_EXECUTION_PERMISSION')
    return m,auth


def run(role):
    m,_=load();job=m['jobs'][role]
    if job.get('max_calls')!=1:raise ValueError('ONE_JOB_ONE_CALL_ONLY')
    packet=json.loads(review.bound(job['packet']));policy=review.bound(job['policy']).decode()
    if role!='writer':review.validate_packet(packet)
    if role=='writer':
        if set(packet)!={'scope','facts','positive_craft_guidance'} or any(k in json.dumps(packet,ensure_ascii=False) for k in ('FAIL','刘先生','human_feedback','findings','reviewer-input','EDITORIAL_CLEAR')):
            raise ValueError('WRITER_DIAGNOSTIC_OR_ANSWER_LEAKAGE')
    result_dir=ROOT/DIRECTORY;result_dir.mkdir(parents=True,exist_ok=True)
    review.dump(result_dir/f'{role}.attempt.json',{'task_id':TASK,'role':role,'packet':job['packet'],'max_calls':1,'started_at':review.utc()},exclusive=True)
    runtime={'task_id':TASK,'role':role,'packet':job['packet'],'started_at':review.utc(),
        'requested_model':m['model'],'requested_reasoning_effort':'max','status':'BLOCKED','report_received':False,
        'model_turn_dispatched':False,'isolation':ISOLATION,'repository_write_permission':False,'generation_count':0,
        'prompt_policy_sha256':hashlib.sha256(policy.encode()).hexdigest()}
    started,server=time.monotonic(),None
    try:
        with review.review_workspace(lambda:server) as workspace:
            server=review.Server(workspace)
            server.request('initialize',{'clientInfo':{'name':'novel_prose_repair','version':'1.0'},'capabilities':{'experimentalApi':True}})
            server.send({'method':'initialized'})
            catalog=server.request('model/list',{})
            selected=next((v for v in catalog['data'] if v['model']=='gpt-6.1-sol'),None)
            if not selected or 'max' not in {v['reasoningEffort'] for v in selected['supportedReasoningEfforts']}:
                raise ValueError('ACTUAL_SOL_MAX_NOT_AVAILABLE')
            runtime['model_catalog_entry']=selected
            response=server.request('thread/start',{'model':'gpt-6.1-sol','allowProviderModelFallback':False,
                'cwd':workspace,'sandbox':'read-only','approvalPolicy':'never','ephemeral':True,'environments':[],
                'runtimeWorkspaceRoots':[],'selectedCapabilityRoots':[],'dynamicTools':[],
                'baseInstructions':'Work only on the supplied text packet; no tools or inherited history.',
                'developerInstructions':policy,'config':{'model_reasoning_effort':'max','project_doc_max_bytes':0}})
            runtime['resolved_thread_settings']={k:response.get(k) for k in ('model','modelProvider','reasoningEffort','approvalPolicy','sandbox','instructionSources','runtimeWorkspaceRoots')}
            runtime['thread_id']=response['thread']['id']
            if (response['model']!='gpt-6.1-sol' or response['reasoningEffort']!='max' or response.get('instructionSources') or
                    response.get('runtimeWorkspaceRoots') or response['sandbox']!={'type':'readOnly','networkAccess':False}):
                raise ValueError('ACTUAL_MODEL_OR_ISOLATION_DRIFT')
            prompt={'verified_runtime':{'model':'gpt-6.1-sol','reasoning_effort':'max','isolation':ISOLATION},
                'writer_packet' if role=='writer' else 'review_packet':packet}
            runtime['submitted_payload_sha256']=hashlib.sha256(json.dumps(prompt,ensure_ascii=False).encode()).hexdigest()
            runtime['model_turn_dispatched']=True
            print(json.dumps({'role':role,'status':'DISPATCHING_ONCE','actual_model':'gpt-6.1-sol','actual_effort':'max'}),flush=True)
            server.request('turn/start',{'threadId':runtime['thread_id'],'input':[{'type':'text','text':json.dumps(prompt,ensure_ascii=False)}],
                'model':'gpt-6.1-sol','effort':'max','environments':[],'runtimeWorkspaceRoots':[],'approvalPolicy':'never',
                'sandboxPolicy':{'type':'readOnly','networkAccess':False}})
            deadline=time.monotonic()+900
            while time.monotonic()<deadline:
                try:value=server.receive(min(30,max(1,deadline-time.monotonic())))
                except queue.Empty:
                    print(json.dumps({'role':role,'status':'WAITING_NO_RESULT','elapsed_seconds':round(time.monotonic()-started,1)}),flush=True);continue
                if value.get('method')=='turn/completed':runtime['turn_status']=value['params']['turn']['status'];break
            else:raise ValueError('TIMEOUT_NO_SUCCESSFUL_OUTPUT')
            items=[e['params']['item'] for e in server.events if e.get('method')=='item/completed']
            runtime['completed_item_types']=[v.get('type') for v in items]
            runtime['tool_activity_detected']=[v.get('type') for v in items if v.get('type') not in ('userMessage','agentMessage','reasoning')]
            runtime['model_initiated_requests']=[e['method'] for e in server.events if 'id' in e]
            finals=[v.get('text','') for v in items if v.get('type')=='agentMessage' and v.get('phase')=='final_answer']
            if not finals:finals=[v.get('text','') for v in items if v.get('type')=='agentMessage'][-1:]
            if runtime['tool_activity_detected'] or runtime['model_initiated_requests'] or runtime.get('turn_status')!='completed' or len(finals)!=1 or not finals[0].strip():
                raise ValueError('NO_ONE_SUCCESSFUL_ISOLATED_OUTPUT')
            with (ROOT/job['raw_path']).open('xb') as out:out.write(finals[0].encode())
            runtime.update(report_received=True,status='RETURNED_RAW_OUTPUT_NOT_YET_SETTLED',raw_report=review.ref(job['raw_path']))
            if role=='writer':runtime.update(generation_count=1,non_whitespace_characters=sum(not c.isspace() for c in finals[0]))
    except (ValueError,OSError,KeyError,queue.Empty) as exc:runtime['error_code']=str(exc).split(':')[0][:120]
    finally:
        if server:server.close()
        runtime.update(finished_at=review.utc(),elapsed_seconds=round(time.monotonic()-started,3))
        review.dump(result_dir/f'{role}.runtime.json',runtime,exclusive=True)
    print(json.dumps({'role':role,'status':runtime['status'],'elapsed_seconds':runtime['elapsed_seconds'],'error_code':runtime.get('error_code')}))
    if not runtime['report_received']:raise SystemExit(1)


def audit(role):
    m,_=load();job=m['jobs'][role];runtime=review.read(ROOT/DIRECTORY/f'{role}.runtime.json')
    packet=json.loads(review.bound(job['packet']));report=review.parse_report(review.bound(runtime['raw_report']))
    result=roles.audit_reader(packet,report,runtime) if role=='reader' else review.audit_report(packet,report,runtime)
    result.update(task_id=TASK,role=role,packet=job['packet'],raw_report=runtime['raw_report'])
    review.dump(ROOT/DIRECTORY/f'{role}.evidence.json',result,exclusive=True)
    print(json.dumps({'role':role,'errors':result['errors'],'quotes':len(result['located_quotes']),'corrections':result['position_corrections']}))
    if result['errors']:raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('run','audit'))
    p.add_argument('--role',choices=('diagnosis','writer','facts','editor','reader'),required=True)
    a=p.parse_args();run(a.role) if a.action=='run' else audit(a.role)
