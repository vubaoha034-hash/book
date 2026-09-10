import json
from pathlib import Path

state_path = Path('state/project_state.json')
cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')

state = json.loads(state_path.read_text(encoding='utf-8'))
active = state.get('active_task', {})
if active.get('task_id') != 'PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1':
    raise SystemExit('unexpected active task; refuse cleanup')
if active.get('status') != 'READY_FOR_TWO_FRESH_NEUTRAL_GENERATOR_CHATS':
    raise SystemExit('unexpected Phase380 status; refuse cleanup')
if state.get('accepted_checkpoint', {}).get('phase_ordinal') != 320:
    raise SystemExit('accepted checkpoint drift; refuse cleanup')
state['schema_version'] = '3.10.1'
state['updated_at'] = '2026-09-10T17:01:00+08:00'
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 32
state.setdefault('invariants', {})['Phase380_duplicate_task_superseded'] = True
state['invariants']['Phase380_ready_receipt_bound_to_authoritative_task'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp = json.loads(cp_path.read_text(encoding='utf-8'))
if cp.get('sequence') != 32:
    raise SystemExit(f"unexpected checkpoint sequence {cp.get('sequence')}; refuse cleanup")
if cp.get('highest_accepted_phase_ordinal') != 320:
    raise SystemExit('accepted checkpoint drift in LATEST_CHECKPOINT; refuse cleanup')
if cp.get('active_task_ids') != ['PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1']:
    raise SystemExit('unexpected active task ids; refuse cleanup')

obsolete_incomplete = {
    'Phase378 R1 fresh generator has not yet been executed',
    'Phase378 R2 fresh generator has not yet been executed',
    'Phase378 isolated process candidate versus control human comparison is not available',
    'Phase378 actual target-reader blind verdict is pending',
    'Phase378 process-level AI-smell transfer signal is not yet established',
    'YMGQ writing remains paused during Phase378',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 30'
}
cp['incomplete'] = [x for x in cp.get('incomplete', []) if x not in obsolete_incomplete]
ledger_note = 'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 32'
if ledger_note not in cp['incomplete']:
    cp['incomplete'].append(ledger_note)
phase380_pause = 'YMGQ writing remains paused during Phase380 prospective discriminator calibration'
if phase380_pause not in cp['incomplete']:
    cp['incomplete'].append(phase380_pause)

obsolete_blocked = {
    'PHASE378_TWO_FRESH_GENERATOR_OUTPUTS_PENDING',
    'YMGQ_WRITING_PAUSED_DURING_PHASE378'
}
cp['blocked'] = [x for x in cp.get('blocked', []) if x not in obsolete_blocked]
for x in ['PHASE380_TWO_NEUTRAL_FRESH_GENERATOR_OUTPUTS_PENDING', 'YMGQ_WRITING_PAUSED_DURING_PHASE380_CALIBRATION']:
    if x not in cp['blocked']:
        cp['blocked'].append(x)

cp['recorded_at'] = '2026-09-10T17:02:00+08:00'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
