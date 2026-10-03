"""One tool-less post-failure diagnosis; never writes fiction or business state.

This separate scope reuses the completed review transport without reopening its
calibration jobs or the consumed one-short writing allowance.
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
TASK = 'NOVEL-EMOTION-REACTION-AND-PACING-LEARNING-20261003-01'
SOURCE = '7997b03fb3a0ec5eaf8e0e5b55f91cd651094fde'
TARGET = 'delivery/r2-entry-trial-20261003/short-a1.md'
BODY_SHA = '6ec604bffc4c60727e102dde328663273f648a0e0b2e6d27b0350833128085aa'
AUTH = 'state/review_receipts/NOVEL_EMOTION_PACING_LEARNING_AUTHORIZATION_20261003.json'
MANIFEST = 'config/novel-emotion-learning-20261003.json'
PACKET = 'delivery/emotion-learning-20261003/diagnosis.packet.json'
DIRECTORY = 'state/reviews/emotion-learning-20261003'
spec = importlib.util.spec_from_file_location('emotion_review_transport', ROOT / 'scripts/codex_review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def validate_scope(manifest, auth):
    if (manifest.get('task_id') != TASK or manifest.get('source_head') != SOURCE or
            manifest.get('model') != 'gpt-6.1-sol' or manifest.get('reasoning_effort') != 'max' or
            manifest.get('maximum_diagnostic_calls') != 1 or manifest.get('generation_budget') != 0 or
            manifest.get('work_kind') != 'POST_FAILURE_DIAGNOSIS' or
            auth.get('task_id') != TASK or auth.get('source_head') != SOURCE or
            auth.get('source_checkpoint') != 196 or auth.get('generation_budget') != 0 or
            auth.get('new_prose_authorized') is not False or
            auth.get('maximum_new_diagnostic_calls') != 1 or
            auth.get('authority', {}).get('source') != 'ACTUAL_CURRENT_USER_INSTRUCTION' or
            auth.get('old_RC3_remaining_rounds') != 0 or
            auth.get('old_197_character_protection_released') is not False):
        raise ValueError('EMOTION_LEARNING_AUTHORIZATION_OR_SCOPE_DRIFT')


def prepare():
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() != SOURCE:
        raise ValueError('SOURCE_HEAD_CHANGED_RECONCILE_FIRST')
    auth = review.read(ROOT / AUTH)
    human = json.loads(review.bound(auth['human_feedback']))
    body = (ROOT / TARGET).read_bytes()
    if (hashlib.sha256(body).hexdigest() != BODY_SHA or human.get('outcome') != 'FAIL' or
            human.get('output') != review.ref(TARGET)):
        raise ValueError('WRONG_FAILED_395_BODY_OR_HUMAN_LABEL')
    facts = review.read(ROOT / 'delivery/r2-entry-trial-20261003/facts.packet.json')['facts']
    packet = {'packet_version': 'codex-review-packet/v1', 'job_id': 'D197',
        'work_kind': 'POST_FAILURE_DIAGNOSIS', 'medium': '手机阅读的中文小说',
        'excerpt_position': '第二场起始395字短段；不是全书开篇或完整场景',
        'samples': [{'artifact_id': 'S197', 'original_sha256': BODY_SHA, 'text': body.decode('utf-8')}],
        'facts': facts, 'human_feedback': human['review']['human_exact_feedback'],
        'boundaries': ['已知395字失败后的诊断，不是盲读。真人认为AI味重、情绪平、互动像机器人；精确停止句、继续欲望的直接答复未知。',
            '一次诊断，仅二至三个主要上游根因。区分真人原话、正文确定事实和编辑假设。不得补写替换句、候选正文或新稿。',
            '核对30—60字、150—300字、段尾期待及私人情绪。区分进入时刻、事实输入缺口、呈现方式。惊讶和难过是例子，不是人物必须哭或惊叫的指令。',
            '只提出最小范围、保护项、未知项及复验条件。原404字结果未知、旧448字只有其原判决，不扩张题材否决。',
            '本轮写作预算为零；旧RC3额度零，旧197字保护及世界人物结局不解除，不新增生活史。AI解释不能推翻真人否决。'],
        'historical_material': {'status': 'NOT_TRANSMITTED_NO_WRITER_DIRECTIONS_OR_OTHER_REPORTS', 'text': ''}}
    review.validate_packet(packet)
    review.dump(ROOT / PACKET, packet, exclusive=True)
    manifest = {'schema_version': 'native-one-post-failure-diagnosis/v1', 'task_id': TASK,
        'source_head': SOURCE, 'authorization': review.ref(AUTH), 'human_feedback': auth['human_feedback'],
        'artifact': review.ref(TARGET), 'facts_source': review.ref('delivery/r2-entry-trial-20261003/facts.packet.json'),
        'packet': review.ref(PACKET), 'work_kind': 'POST_FAILURE_DIAGNOSIS', 'model': 'gpt-6.1-sol',
        'reasoning_effort': 'max', 'maximum_diagnostic_calls': 1, 'generation_budget': 0,
        'blind_read': False, 'calibration_rerun': False, 'result_directory': DIRECTORY}
    validate_scope(manifest, auth)
    review.dump(ROOT / MANIFEST, manifest, exclusive=True)
    print('FROZEN_ONE_KNOWN_FAILURE_DIAGNOSIS_NO_PROSE')


def run():
    manifest = review.read(ROOT / MANIFEST)
    auth = json.loads(review.bound(manifest['authorization']))
    validate_scope(manifest, auth)
    packet = json.loads(review.bound(manifest['packet']))
    review.validate_packet(packet)
    human = json.loads(review.bound(manifest['human_feedback']))
    if (packet['work_kind'] != 'POST_FAILURE_DIAGNOSIS' or packet['job_id'] != 'D197' or
            packet['samples'] != [{'artifact_id': 'S197', 'original_sha256': BODY_SHA,
                'text': review.bound(manifest['artifact']).decode('utf-8')}] or
            packet['human_feedback'] != human['review']['human_exact_feedback'] or
            packet['facts'] != json.loads(review.bound(manifest['facts_source']))['facts']):
        raise ValueError('DIAGNOSIS_PACKET_OR_FACT_IDENTITY_DRIFT')
    result_dir = ROOT / DIRECTORY
    result_dir.mkdir(parents=True, exist_ok=True)
    review.dump(result_dir / 'diagnosis.attempt.json', {'task_id': TASK, 'job_id': 'D197',
        'packet': manifest['packet'], 'max_calls': 1, 'started_at': review.utc()}, exclusive=True)
    runtime = {'task_id': TASK, 'job_id': 'D197', 'packet': manifest['packet'], 'started_at': review.utc(),
        'requested_model': manifest['model'], 'requested_reasoning_effort': 'max',
        'status': 'BLOCKED', 'report_received': False, 'model_turn_dispatched': False,
        'isolation': 'FRESH_PROCESS_FRESH_EPHEMERAL_THREAD_ENVIRONMENTS_DISABLED_NO_HISTORY',
        'repository_write_permission': False, 'generation_count': 0,
        'prompt_policy_sha256': hashlib.sha256(review.REVIEW_INSTRUCTIONS.encode()).hexdigest()}
    started, server = time.monotonic(), None
    try:
        with review.review_workspace(lambda: server) as workspace:
            server = review.Server(workspace)
            server.request('initialize', {'clientInfo': {'name': 'novel_emotion_diagnosis', 'version': '1.0'},
                'capabilities': {'experimentalApi': True}})
            server.send({'method': 'initialized'})
            catalog = server.request('model/list', {})
            selected = next((m for m in catalog['data'] if m['model'] == manifest['model']), None)
            if selected is None:
                raise ValueError('REQUESTED_MODEL_NOT_IN_ACTUAL_CATALOG')
            runtime['model_catalog_entry'] = selected
            response = server.request('thread/start', {'model': manifest['model'], 'allowProviderModelFallback': False,
                'cwd': workspace, 'sandbox': 'read-only', 'approvalPolicy': 'never', 'ephemeral': True,
                'environments': [], 'runtimeWorkspaceRoots': [], 'selectedCapabilityRoots': [], 'dynamicTools': [],
                'baseInstructions': 'You are a text evidence editor. Review only the submitted packet. Never write fiction or use tools.',
                'developerInstructions': review.REVIEW_INSTRUCTIONS,
                'config': {'model_reasoning_effort': 'max', 'project_doc_max_bytes': 0}})
            runtime['resolved_thread_settings'] = {k: response.get(k) for k in ('model', 'modelProvider', 'reasoningEffort',
                'approvalPolicy', 'sandbox', 'activePermissionProfile', 'instructionSources', 'runtimeWorkspaceRoots')}
            runtime['thread_id'] = response['thread']['id']
            if (response['model'] != manifest['model'] or response['reasoningEffort'] != 'max' or
                    response.get('instructionSources') or response.get('runtimeWorkspaceRoots') or
                    response['sandbox'].get('type') != 'readOnly' or response['sandbox'].get('networkAccess') is not False):
                raise ValueError('ACTUAL_MODEL_OR_ISOLATION_NOT_AS_REQUESTED')
            prompt = {'verified_runtime': {'model': response['model'], 'reasoning_effort': response['reasoningEffort'],
                'isolation': runtime['isolation']}, 'review_packet': packet}
            runtime['submitted_payload_sha256'] = hashlib.sha256(json.dumps(prompt, ensure_ascii=False).encode()).hexdigest()
            runtime['model_turn_dispatched'] = True
            print(json.dumps({'status': 'DISPATCHING_ONE_KNOWN_FAILURE_DIAGNOSIS', 'actual_model': response['model'],
                'actual_reasoning_effort': response['reasoningEffort']}, ensure_ascii=False), flush=True)
            server.request('turn/start', {'threadId': runtime['thread_id'],
                'input': [{'type': 'text', 'text': json.dumps(prompt, ensure_ascii=False)}], 'model': response['model'],
                'effort': response['reasoningEffort'], 'environments': [], 'runtimeWorkspaceRoots': [],
                'approvalPolicy': 'never', 'sandboxPolicy': {'type': 'readOnly', 'networkAccess': False}})
            deadline = time.monotonic() + 900
            while time.monotonic() < deadline:
                try:
                    value = server.receive(min(30, max(1, deadline-time.monotonic())))
                except queue.Empty:
                    print(json.dumps({'status': 'WAITING_NO_REPORT_OR_VERDICT',
                        'elapsed_seconds': round(time.monotonic()-started, 1)}), flush=True)
                    continue
                if value.get('method') == 'turn/completed':
                    runtime['turn_status'] = value['params']['turn']['status']
                    break
            else:
                raise ValueError('TIMEOUT_NO_SUCCESSFUL_OUTPUT')
            completed = [e['params']['item'] for e in server.events if e.get('method') == 'item/completed']
            runtime['completed_item_types'] = [i.get('type') for i in completed]
            runtime['tool_activity_detected'] = [i.get('type') for i in completed if i.get('type') not in ('userMessage', 'agentMessage', 'reasoning')]
            runtime['model_initiated_requests'] = [e['method'] for e in server.events if 'id' in e]
            if runtime['tool_activity_detected'] or runtime['model_initiated_requests']:
                raise ValueError('ISOLATION_TOOL_ACTIVITY_REJECTED')
            finals = [i.get('text', '') for i in completed if i.get('type') == 'agentMessage' and i.get('phase') == 'final_answer']
            if not finals:
                finals = [i.get('text', '') for i in completed if i.get('type') == 'agentMessage'][-1:]
            if len(finals) != 1 or not finals[0].strip() or runtime.get('turn_status') != 'completed':
                raise ValueError('NO_ONE_SUCCESSFUL_FINAL_OUTPUT')
            raw_path = DIRECTORY + '/diagnosis.raw.txt'
            with (ROOT / raw_path).open('xb') as output:
                output.write(finals[0].encode('utf-8'))
            runtime.update(raw_report=review.ref(raw_path), report_received=True, status='RETURNED_RAW_REPORT_NOT_YET_SETTLED')
    except (ValueError, OSError, KeyError, queue.Empty) as exc:
        runtime['error_code'] = str(exc).split(':')[0][:120]
    finally:
        if server:
            server.close()
        runtime.update(finished_at=review.utc(), elapsed_seconds=round(time.monotonic()-started, 3))
        review.dump(result_dir / 'diagnosis.runtime.json', runtime, exclusive=True)
    print(json.dumps({'status': runtime['status'], 'elapsed_seconds': runtime['elapsed_seconds'],
        'error_code': runtime.get('error_code')}))
    if not runtime['report_received']:
        raise SystemExit(1)


def audit():
    manifest = review.read(ROOT / MANIFEST)
    runtime = review.read(ROOT / DIRECTORY / 'diagnosis.runtime.json')
    if not runtime.get('report_received') or runtime.get('tool_activity_detected') or runtime.get('model_initiated_requests'):
        raise ValueError('NO_RETURNED_INDEPENDENT_DIAGNOSIS')
    packet = json.loads(review.bound(manifest['packet']))
    report = review.parse_report(review.bound(runtime['raw_report']))
    evidence = review.audit_report(packet, report, runtime)
    evidence.update(task_id=TASK, packet=manifest['packet'], raw_report=runtime['raw_report'])
    review.dump(ROOT / DIRECTORY / 'diagnosis.evidence.json', evidence, exclusive=True)
    print(json.dumps({'status': evidence['status'], 'errors': evidence['errors'],
        'located_quote_count': len(evidence['located_quotes']), 'position_corrections': len(evidence['position_corrections'])}))
    if evidence['errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'run', 'audit'))
    {'prepare': prepare, 'run': run, 'audit': audit}[parser.parse_args().action]()
