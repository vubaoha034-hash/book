"""Two separate tool-less AI contexts; frozen one-shot packets, no fiction/state writes.

Reuses the proven logged-in Codex transport. Reader reaction and post-failure
editor diagnosis are distinct jobs and never receive one another's output.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import queue
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
TASK = 'NOVEL-TWO-ROLE-OPENING-REVIEW-20261003-01'
SOURCE = 'f1283b8b4daaf3ded67a42de7784dca3f3e09603'
BODY = 'delivery/r2-entry-trial-20261003/short-a1.md'
BODY_SHA = '6ec604bffc4c60727e102dde328663273f648a0e0b2e6d27b0350833128085aa'
AUTH = 'state/review_receipts/NOVEL_TWO_ROLE_REVIEW_AUTHORIZATION_20261003.json'
HUMAN = 'state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_RETENTION_SUPPLEMENT_20261003.json'
MANIFEST = 'config/novel-two-role-review-20261003.json'
DIRECTORY = 'state/reviews/two-role-opening-20261003'
PACKETS = 'delivery/two-role-opening-20261003'
ROLE_REQUEST = '一，我需要多角色的介入。我不希望你自己做图而后自己审核。加入一个专业人士审核，还有一个普通观众是否愿意看，二，我知道skill里面专门有这类审核的skill，你可以直接照搬过来，或者你自己检查下，是否有用，把有用的拿过来。明白我的意思吗？而后有了审核就进行下一步。'
RETENTION_FEEDBACK = '讲真的，我一直觉得这个开头非常难以让我有看下去的冲动，现在的快时代，一开始应该快速抓住要求，几百个字根本让我没有欲望，那说明问题就很大。'
ISOLATION = 'FRESH_PROCESS_FRESH_EPHEMERAL_THREAD_ENVIRONMENTS_DISABLED_NO_HISTORY'
spec = importlib.util.spec_from_file_location('two_role_transport', ROOT / 'scripts/codex_review.py')
review = importlib.util.module_from_spec(spec); spec.loader.exec_module(review)


def validate_scope(manifest, auth):
    if (manifest.get('task_id') != TASK or manifest.get('source_head') != SOURCE or
            auth.get('task_id') != TASK or auth.get('source_head') != SOURCE or
            auth.get('source_checkpoint') != 197 or auth.get('exact_user_instruction') != ROLE_REQUEST or
            auth.get('source') != 'ACTUAL_CURRENT_USER_MESSAGE' or
            auth.get('generation_budget') != 0 or auth.get('new_prose_authorized') is not False or
            auth.get('old_RC3_remaining_rounds') != 0 or auth.get('old_197_character_protection_released') is not False or
            auth.get('maximum_new_review_calls') != 2 or manifest.get('generation_budget') != 0 or
            manifest.get('model') != 'gpt-6.1-sol' or manifest.get('reasoning_effort') != 'max' or
            set(manifest.get('jobs', {})) != {'reader', 'editor'} or
            any(x.get('max_calls') != 1 for x in manifest['jobs'].values())):
        raise ValueError('TWO_ROLE_AUTHORIZATION_OR_SCOPE_DRIFT')


def prepare():
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() != SOURCE:
        raise ValueError('SOURCE_HEAD_CHANGED_RECONCILE_FIRST')
    body = (ROOT / BODY).read_bytes()
    if hashlib.sha256(body).hexdigest() != BODY_SHA:
        raise ValueError('WRONG_395_BODY')
    prior_path = 'state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_FAIL_20261003.json'
    prior = review.read(ROOT / prior_path)
    if prior['output'] != review.ref(BODY) or prior['outcome'] != 'FAIL':
        raise ValueError('WRONG_PRIOR_HUMAN_FAILURE')
    current = dict(prior['review'])
    current.update(human_exact_feedback=RETENTION_FEEDBACK,
        feedback_summary='刘先生继续明确指出当前395字开头没有继续阅读欲望；前次AI味、情绪和互动否决保留。',
        wants_to_continue=False, retention_verdict='FAIL',
        source={'kind': 'ACTUAL_CURRENT_USER_MESSAGE', 'message_observed_directly': True},
        carried_dimensions_source=review.ref(prior_path),
        scope_note='在当前395字稿及其反馈之后的直接补充；不是旧448/404字的新判决。')
    human = {'schema_version': 'native-human-retention-supplement/v1', 'project_id': 'novel-distillation',
        'task_id': TASK, 'source_head': SOURCE, 'source_checkpoint': 197,
        'output': review.ref(BODY), 'prior_human_feedback': review.ref(prior_path), 'outcome': 'FAIL',
        'review': current, 'processed_once': True, 'new_generation_budget': 0,
        'exact_stop_sentence': 'UNKNOWN_NOT_PROVIDED', 'prior_receipt_rewritten': False}
    review.dump(ROOT / HUMAN, human, exclusive=True)
    auth = {'schema_version': 'native-two-role-review-authorization/v1', 'task_id': TASK,
        'source_head': SOURCE, 'source_checkpoint': 197, 'source': 'ACTUAL_CURRENT_USER_MESSAGE',
        'exact_user_instruction': ROLE_REQUEST, 'retention_feedback': review.ref(HUMAN),
        'previous_learning_result': review.ref('state/review_receipts/NOVEL_EMOTION_PACING_LEARNING_RESULT_20261003.json'),
        'maximum_new_review_calls': 2, 'generation_budget': 0, 'new_prose_authorized': False,
        'old_RC3_remaining_rounds': 0, 'old_197_character_protection_released': False,
        'authorized_next_work': 'TWO_ACTUAL_ISOLATED_AI_ROLES_THEN_ONE_EVIDENCE_BASED_OPENING_SCOPE_AND_INPUT_PREPARATION',
        'new_writing_budget_inferred_from_review_completion': False,
        'full_v5_authorized': False, 'new_life_facts_authorized': False, 'automatic_background_tasks_authorized': False}
    review.dump(ROOT / AUTH, auth, exclusive=True)
    reader = {'packet_version': 'codex-review-packet/v1', 'job_id': 'R198', 'work_kind': 'COLD_SCREEN',
        'medium': '手机阅读的中文小说', 'excerpt_position': '第二场开头摘录；不是全书开篇或完整场景',
        'samples': [{'artifact_id': 'A08', 'original_sha256': BODY_SHA, 'text': body.decode()}]}
    editor = {**reader, 'job_id': 'E198', 'work_kind': 'POST_FAILURE_DIAGNOSIS',
        'facts': review.read(ROOT / 'delivery/r2-entry-trial-20261003/facts.packet.json')['facts'],
        'human_feedback': [prior['review']['human_exact_feedback'], RETENTION_FEEDBACK],
        'boundaries': ['已知失败后的局部诊断，非盲读；不读取普通读者报告或协调者先前诊断。',
            '二至三个上游根因；需要改变进入时刻或开头可明确提出，但本轮只准备范围与冻结输入，不写作。',
            '旧RC3预算零、旧197字保护不释放、原404真人未知；人物世界结局不变，不补新事实。',
            '真人明确当前开头没有继续阅读欲望，精确停止句仍未知。AI评审不能覆盖真人否决。'],
        'historical_material': {'status': 'NOT_TRANSMITTED_NO_WRITER_DIRECTIONS_OR_OTHER_REPORTS', 'text': ''}}
    jobs = {}
    for role, packet in [('reader', reader), ('editor', editor)]:
        review.validate_packet(packet)
        path = f'{PACKETS}/{role}.packet.json'
        review.dump(ROOT / path, packet, exclusive=True)
        jobs[role] = {'packet': review.ref(path), 'policy': review.ref(f'modules/review-roles/{role}-policy.md'), 'max_calls': 1}
    manifest = {'schema_version': 'native-two-role-review/v1', 'task_id': TASK, 'source_head': SOURCE,
        'authorization': review.ref(AUTH), 'human_feedback': review.ref(HUMAN), 'artifact': review.ref(BODY),
        'facts_source': review.ref('delivery/r2-entry-trial-20261003/facts.packet.json'),
        'jobs': jobs, 'model': 'gpt-6.1-sol', 'reasoning_effort': 'max', 'generation_budget': 0,
        'blind_calibration_rerun': False, 'standalone_quality_gate_allowed': False,
        'result_directory': DIRECTORY, 'roles_are_actual_humans': False}
    validate_scope(manifest, auth)
    review.dump(ROOT / MANIFEST, manifest, exclusive=True)
    print('FROZEN_READER_NO_LABELS_EDITOR_KNOWN_FAILURE_TWO_ONE_SHOT_CONTEXTS')


def validated_packet(manifest, role):
    auth = json.loads(review.bound(manifest['authorization']))
    validate_scope(manifest, auth)
    job = manifest['jobs'][role]
    packet = json.loads(review.bound(job['packet']))
    review.validate_packet(packet)
    if (packet['job_id'] != {'reader': 'R198', 'editor': 'E198'}[role] or
            packet['work_kind'] != {'reader': 'COLD_SCREEN', 'editor': 'POST_FAILURE_DIAGNOSIS'}[role] or
            packet['samples'] != [{'artifact_id': 'A08', 'original_sha256': BODY_SHA,
                'text': review.bound(manifest['artifact']).decode()}]):
        raise ValueError('TWO_ROLE_PACKET_IDENTITY_DRIFT')
    if role == 'editor':
        current = json.loads(review.bound(manifest['human_feedback']))
        prior = json.loads(review.bound(current['prior_human_feedback']))
        if (packet['facts'] != json.loads(review.bound(manifest['facts_source']))['facts'] or
                packet['human_feedback'] != [prior['review']['human_exact_feedback'], RETENTION_FEEDBACK] or
                packet['historical_material'] != {'status': 'NOT_TRANSMITTED_NO_WRITER_DIRECTIONS_OR_OTHER_REPORTS', 'text': ''}):
            raise ValueError('EDITOR_FACT_OR_FAILURE_BINDING_DRIFT')
    return packet


def run(role):
    manifest = review.read(ROOT / MANIFEST)
    packet = validated_packet(manifest, role)
    job = manifest['jobs'][role]
    policy = review.bound(job['policy']).decode()
    result_dir = ROOT / DIRECTORY; result_dir.mkdir(parents=True, exist_ok=True)
    review.dump(result_dir / f'{role}.attempt.json', {'task_id': TASK, 'job_id': packet['job_id'],
        'role': role, 'packet': job['packet'], 'max_calls': 1, 'started_at': review.utc()}, exclusive=True)
    runtime = {'task_id': TASK, 'job_id': packet['job_id'], 'role': role, 'packet': job['packet'],
        'policy': job['policy'], 'started_at': review.utc(), 'requested_model': manifest['model'],
        'requested_reasoning_effort': 'max', 'status': 'BLOCKED', 'report_received': False,
        'model_turn_dispatched': False, 'isolation': ISOLATION, 'repository_write_permission': False,
        'generation_count': 0, 'prompt_policy_sha256': hashlib.sha256(policy.encode()).hexdigest()}
    started, server = time.monotonic(), None
    try:
        with review.review_workspace(lambda: server) as workspace:
            server = review.Server(workspace)
            server.request('initialize', {'clientInfo': {'name': 'novel_two_role_review', 'version': '1.0'},
                'capabilities': {'experimentalApi': True}}); server.send({'method': 'initialized'})
            catalog = server.request('model/list', {})
            selected = next((m for m in catalog['data'] if m['model'] == manifest['model']), None)
            if selected is None or 'max' not in {x['reasoningEffort'] for x in selected['supportedReasoningEfforts']}:
                raise ValueError('REQUESTED_MODEL_OR_MAX_NOT_IN_ACTUAL_CATALOG')
            runtime['model_catalog_entry'] = selected
            response = server.request('thread/start', {'model': manifest['model'], 'allowProviderModelFallback': False,
                'cwd': workspace, 'sandbox': 'read-only', 'approvalPolicy': 'never', 'ephemeral': True,
                'environments': [], 'runtimeWorkspaceRoots': [], 'selectedCapabilityRoots': [], 'dynamicTools': [],
                'baseInstructions': 'You are a tool-less independent AI reviewer. Read only the submitted material; never write fiction.',
                'developerInstructions': policy, 'config': {'model_reasoning_effort': 'max', 'project_doc_max_bytes': 0}})
            runtime['resolved_thread_settings'] = {k: response.get(k) for k in ('model', 'modelProvider', 'reasoningEffort',
                'approvalPolicy', 'sandbox', 'activePermissionProfile', 'instructionSources', 'runtimeWorkspaceRoots')}
            runtime['thread_id'] = response['thread']['id']
            if (response['model'] != manifest['model'] or response['reasoningEffort'] != 'max' or
                    response.get('instructionSources') or response.get('runtimeWorkspaceRoots') or
                    response['sandbox'] != {'type': 'readOnly', 'networkAccess': False}):
                raise ValueError('ACTUAL_MODEL_OR_ISOLATION_NOT_AS_REQUESTED')
            prompt = {'verified_runtime': {'model': response['model'], 'reasoning_effort': response['reasoningEffort'],
                'isolation': ISOLATION}, 'review_packet': packet}
            runtime['submitted_payload_sha256'] = hashlib.sha256(json.dumps(prompt, ensure_ascii=False).encode()).hexdigest()
            runtime['model_turn_dispatched'] = True
            print(json.dumps({'role': role, 'status': 'DISPATCHING_ONCE', 'actual_model': response['model'],
                'actual_reasoning_effort': response['reasoningEffort']}), flush=True)
            server.request('turn/start', {'threadId': runtime['thread_id'], 'input': [{'type': 'text',
                'text': json.dumps(prompt, ensure_ascii=False)}], 'model': response['model'], 'effort': 'max',
                'environments': [], 'runtimeWorkspaceRoots': [], 'approvalPolicy': 'never',
                'sandboxPolicy': {'type': 'readOnly', 'networkAccess': False}})
            deadline = time.monotonic() + 900
            while time.monotonic() < deadline:
                try:
                    value = server.receive(min(30, max(1, deadline-time.monotonic())))
                except queue.Empty:
                    print(json.dumps({'role': role, 'status': 'WAITING_NO_VERDICT',
                        'elapsed_seconds': round(time.monotonic()-started, 1)}), flush=True); continue
                if value.get('method') == 'turn/completed':
                    runtime['turn_status'] = value['params']['turn']['status']; break
            else: raise ValueError('TIMEOUT_NO_SUCCESSFUL_OUTPUT')
            completed = [e['params']['item'] for e in server.events if e.get('method') == 'item/completed']
            runtime['completed_item_types'] = [i.get('type') for i in completed]
            runtime['tool_activity_detected'] = [i.get('type') for i in completed if i.get('type') not in ('userMessage', 'agentMessage', 'reasoning')]
            runtime['model_initiated_requests'] = [e['method'] for e in server.events if 'id' in e]
            if runtime['tool_activity_detected'] or runtime['model_initiated_requests']:
                raise ValueError('ISOLATION_TOOL_ACTIVITY_REJECTED')
            finals = [i.get('text', '') for i in completed if i.get('type') == 'agentMessage' and i.get('phase') == 'final_answer']
            if not finals: finals = [i.get('text', '') for i in completed if i.get('type') == 'agentMessage'][-1:]
            if len(finals) != 1 or not finals[0].strip() or runtime.get('turn_status') != 'completed':
                raise ValueError('NO_ONE_SUCCESSFUL_FINAL_REPORT')
            raw_path = DIRECTORY + f'/{role}.raw.txt'
            with (ROOT / raw_path).open('xb') as out: out.write(finals[0].encode())
            runtime.update(raw_report=review.ref(raw_path), report_received=True, status='RETURNED_RAW_REPORT_NOT_YET_SETTLED')
    except (ValueError, OSError, KeyError, queue.Empty) as exc:
        runtime['error_code'] = str(exc).split(':')[0][:120]
    finally:
        if server: server.close()
        runtime.update(finished_at=review.utc(), elapsed_seconds=round(time.monotonic()-started, 3))
        review.dump(result_dir / f'{role}.runtime.json', runtime, exclusive=True)
    print(json.dumps({'role': role, 'status': runtime['status'], 'elapsed_seconds': runtime['elapsed_seconds'],
        'error_code': runtime.get('error_code')}))
    if not runtime['report_received']: raise SystemExit(1)


def audit_reader(packet, report, runtime, expected_scope='SECOND_SCENE_OPENING_EXCERPT'):
    if expected_scope not in ('SECOND_SCENE_OPENING_EXCERPT', 'NEW_STORY_OPENING_EXCERPT'):
        raise ValueError('UNAUTHORIZED_REVIEW_SCOPE')
    errors, located, corrections = [], [], []
    required = {'job_id','work_kind','runtime_context','artifact_id','original_sha256','scope','reader_profile',
        'wants_to_continue','reading_expectations','reactions','protected_parts','recheck_conditions','unknowns'}
    if set(report) != required: errors.append('READER_REPORT_SCHEMA_DRIFT')
    sample = packet['samples'][0]
    if (report.get('job_id') != packet['job_id'] or report.get('work_kind') != 'COLD_SCREEN' or
            report.get('artifact_id') != sample['artifact_id'] or report.get('original_sha256') != sample['original_sha256'] or
            report.get('scope') != expected_scope or report.get('runtime_context') !=
            {'model':'gpt-6.1-sol','reasoning_effort':'max','isolation':ISOLATION} or
            report.get('wants_to_continue') not in ('YES','NO','UNCERTAIN') or not report.get('reader_profile') or
            not report.get('unknowns') or set(report.get('reading_expectations',{})) != {'first_30_60','first_150_300','ending'}):
        errors.append('READER_IDENTITY_SETTINGS_OR_REACTION_DRIFT')
    items = list(report.get('reading_expectations',{}).values()) + report.get('reactions',[]) + report.get('protected_parts',[])
    text = sample['text']
    for index, item in enumerate(items):
        quote = item.get('quote',''); offset = text.find(quote) if quote else -1
        if offset < 0: errors.append('READER_QUOTE_NOT_FOUND'); continue
        actual = text[:offset].count('\n')+1
        located.append({'index':index,'quote':quote,'actual_line':actual,'start_character_0_based':offset})
        if actual != item.get('line'): corrections.append({'index':index,'claimed_line':item.get('line'),'actual_line':actual})
    if not 2 <= len(report.get('reactions',[])) <= 5 or not report.get('recheck_conditions'):
        errors.append('READER_REACTION_EVIDENCE_INSUFFICIENT')
    return {'status':'READER_REACTION_EVIDENCE_LOCATED_NOT_HUMAN_PROOF' if not errors else 'BLOCKED_READER_REPORT',
        'errors':errors,'located_quotes':located,'position_corrections':corrections,
        'raw_report_rewritten':False,'automatic_revision_authorized':False,'human_quality_result_changed':False}


def audit(role):
    manifest = review.read(ROOT / MANIFEST)
    runtime = review.read(ROOT / DIRECTORY / f'{role}.runtime.json')
    if not runtime.get('report_received') or runtime.get('tool_activity_detected') or runtime.get('model_initiated_requests'):
        raise ValueError('NO_COMPLETE_ISOLATED_REVIEW')
    packet = validated_packet(manifest, role)
    report = review.parse_report(review.bound(runtime['raw_report']))
    evidence = audit_reader(packet, report, runtime) if role == 'reader' else review.audit_report(packet, report, runtime)
    evidence.update(task_id=TASK, role=role, packet=manifest['jobs'][role]['packet'], raw_report=runtime['raw_report'])
    review.dump(ROOT / DIRECTORY / f'{role}.evidence.json', evidence, exclusive=True)
    print(json.dumps({'role':role,'status':evidence['status'],'errors':evidence['errors'],
        'located_quote_count':len(evidence['located_quotes']),'position_corrections':evidence['position_corrections']}))
    if evidence['errors']: raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare','run','audit'))
    parser.add_argument('--role',choices=('reader','editor'))
    args = parser.parse_args()
    if args.action == 'prepare': prepare()
    elif not args.role: parser.error('--role required for run/audit')
    else: {'run':run,'audit':audit}[args.action](args.role)
