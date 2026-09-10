import json
from pathlib import Path

# one-shot Phase380 ready-state settlement
state_path = Path('state/project_state.json')
cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')

state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '4.0.1'
state['updated_at'] = '2026-09-10T16:56:00+08:00'
active = state['active_task']
if active.get('task_id') != 'PHASE380_PROSPECTIVE_TARGET_READER_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1':
    raise SystemExit('unexpected active task; refuse overwrite')
active['status'] = 'READY_FOR_TWO_FRESH_GENERATOR_CHATS'
active['fixed_story_facts'] = 'state/calibration/PHASE380_FIXED_STORY_FACTS_PACKET_V1.json'
active['R1_invocation_path'] = 'state/tasks/PHASE380_FRESH_NEUTRAL_GENERATOR_R1_INVOCATION_V1.txt'
active['R2_invocation_path'] = 'state/tasks/PHASE380_FRESH_NEUTRAL_GENERATOR_R2_INVOCATION_V1.txt'
active['R1_drive_file_id'] = '1OiASyZl6Lhv0qLw7-RVoHwWp9QyirI4z'
active['R2_drive_file_id'] = '1a16_NQn7suEMe0yeeo4KE3WQ45NIRW1W'
active['invocations_ready_receipt'] = 'state/review_receipts/PHASE380_NEUTRAL_GENERATOR_INVOCATIONS_READY_V1.json'
active['next_action'] = 'Execute the R1 and R2 Drive invocation files in two genuinely separate brand-new ChatGPT chats. Do not expose Phase377/379 discriminator material to either generator.'
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 34
state.setdefault('invariants', {})['Phase380_neutral_invocations_ready'] = True
state['invariants']['Phase380_current_evaluator_chat_may_not_generate_R1_R2'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp = json.loads(cp_path.read_text(encoding='utf-8'))
if cp.get('highest_accepted_phase_ordinal') != 320:
    raise SystemExit('accepted checkpoint drift; refuse overwrite')
cp['sequence'] = 34
cp['recorded_at'] = '2026-09-10T16:57:00+08:00'
cp['active_task_ids'] = ['PHASE380_PROSPECTIVE_TARGET_READER_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1']
cp['status'] = 'ACTIVE_PHASE380_TWO_NEUTRAL_FRESH_GENERATOR_INVOCATIONS_READY'
cp['current_focus'] = 'Phase379 target-reader AI-smell discriminator recalibration is complete as diagnostic-only. Phase380 fixed bus-depot lost-and-found facts and two equivalent neutral fresh-generator invocation files are prepared and bound to real Drive text/plain files. The current evaluator-aware chat may not generate either output. Next step is two separate fresh neutral generator chats, then byte-freeze both outputs and seal the recalibrated discriminator prediction before any human blind review.'
cp['next_required_action'] = 'Run Phase380 R1 Drive invocation 1OiASyZl6Lhv0qLw7-RVoHwWp9QyirI4z and R2 Drive invocation 1a16_NQn7suEMe0yeeo4KE3WQ45NIRW1W in two separate brand-new chats and return both DONE markers with actual output Drive File IDs.'

obsolete_incomplete = {
    'Phase378 R1 fresh generator has not yet been executed',
    'Phase378 R2 fresh generator has not yet been executed',
    'Phase378 isolated process candidate versus control human comparison is not available',
    'Phase378 actual target-reader blind verdict is pending',
    'Phase378 process-level AI-smell transfer signal is not yet established',
    'YMGQ writing remains paused during Phase378',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 30',
    'Phase380 prospective discriminator calibration not yet executed'
}
cp['incomplete'] = [x for x in cp.get('incomplete', []) if x not in obsolete_incomplete]
for x in [
    'Phase380 two neutral fresh generator outputs are pending',
    'Phase380 prospective discriminator prediction is not yet available',
    'Reliable AI-smell evaluator remains unproven',
    'Stable low-AI generation process remains unproven',
    'Stable long-form scale transfer remains UNPROVEN',
    'YMGQ writing remains paused during Phase380 discriminator calibration',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 34'
]:
    if x not in cp['incomplete']:
        cp['incomplete'].append(x)

obsolete_blocked = {
    'PHASE378_TWO_FRESH_GENERATOR_OUTPUTS_PENDING',
    'YMGQ_WRITING_PAUSED_DURING_PHASE378'
}
cp['blocked'] = [x for x in cp.get('blocked', []) if x not in obsolete_blocked]
for x in ['PHASE380_TWO_NEUTRAL_FRESH_GENERATOR_OUTPUTS_PENDING', 'YMGQ_WRITING_PAUSED_DURING_PHASE380_CALIBRATION']:
    if x not in cp['blocked']:
        cp['blocked'].append(x)

for x in [
    'Phase380 fixed story facts packet prepared',
    'Phase380 equivalent neutral R1/R2 invocation files prepared',
    'Phase380 R1/R2 invocation files stored as real Drive text/plain files'
]:
    if x not in cp.setdefault('completed', []):
        cp['completed'].append(x)

cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
