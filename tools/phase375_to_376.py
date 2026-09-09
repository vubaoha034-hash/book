import json
from pathlib import Path

state_path = Path('state/project_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.4.0'
state['updated_at'] = '2026-09-09T17:29:00+08:00'
state['phase375_settlement'] = {
    'execution': 'ACTUAL_HUMAN_BLIND_REVIEW_COMPLETE_WEAK_REPAIR_PREFERENCE',
    'human_receipt': 'state/review_receipts/PHASE375_ACTUAL_HUMAN_BLIND_REVIEW_H1_V1.json',
    'revealed_mapping': {'X':'BASELINE_UNTOUCHED_PHASE373_B','Y':'SINGLE_DEFECT_REPAIR'},
    'overall_comparison': 'NEAR_TIE',
    'forced_preference_if_required': 'Y_REPAIR',
    'preference_strength': 'WEAK',
    'passive_validator_caused_harm': False,
    'directional_signal': 'WEAK_POSITIVE',
    'transfer_supported': False,
    'span_growth_authorized': False,
    'accepted_checkpoint_advance': False
}
state['active_task'] = {
    'task_id': 'PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1',
    'phase': 'FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION',
    'phase_ordinal': 376,
    'status': 'READY_NOT_STARTED',
    'task_contract': 'state/tasks/PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1.json',
    'execution_scope': 'Replicate the passive-validator method on a new natural short-fiction baseline. Freeze baseline first, passively locate at most one material defect, make at most one minimal repair, then blind human-compare. No direct RX generation activation, no YMGQ writing, and no scale-up.',
    'direct_RX_generation_activation': False,
    'passive_RX_validation_authorized': True,
    'one_located_defect_max': True,
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Execute Phase376 fresh natural baseline replication and stop at actual-human blind review.'
}
state.setdefault('reader_experience_transfer_state', {})['passive_validator_calling_mode'] = 'PHASE375_WEAK_POSITIVE_PHASE376_REPLICATION_REQUIRED'
state['reader_experience_transfer_state']['span_growth_authorized'] = False
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 26
state.setdefault('invariants', {})['Phase375_weak_preference_may_not_be_scaled_without_replication'] = True
state['invariants']['Phase376_may_repair_at_most_one_located_defect'] = True
state['invariants']['Phase376_may_not_write_or_extend_YMGQ'] = True
state['invariants']['Phase320_remains_highest_accepted_promotion_checkpoint'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')
cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 26
cp['recorded_at'] = '2026-09-09T17:30:00+08:00'
cp['active_task_ids'] = ['PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1']
cp['current_focus'] = 'Phase375 actual-human blind review found X/Y nearly identical; if forced to choose, the human slightly preferred Y. Mapping revealed Y as the single-defect repair. This is a weak positive passive-validator signal, insufficient for transfer support or scale-up. Phase376 now requires replication on a fresh natural baseline with at most one passive-validator repair.'
cp['completed'] = list(dict.fromkeys(cp.get('completed', []) + [
    'Phase375 actual-human blind review completed',
    'Phase375 X/Y mapping revealed after verdict: X=untouched baseline, Y=single-defect repair',
    'Human judgment: near tie; forced preference Y',
    'Phase375 passive-validator result classified WEAK_POSITIVE, not TRANSFER_SUPPORTED',
    'No span growth authorized from Phase375',
    'Phase376 replication task created',
    'Phase320 remains highest accepted promotion checkpoint'
]))
cp['incomplete'] = [
    'Phase376 fresh natural baseline replication has not yet been executed',
    'Passive-validator repeatability is not proven',
    'No RX candidate has TRANSFER_SUPPORTED status',
    'No bounded span-growth survival test is authorized',
    'Stable long-form scale transfer remains UNPROVEN',
    'Current full YMGQ manuscript remains actual-human rejected',
    'YMGQ writing remains paused during transfer-method repair',
    'No full-manuscript reconstruction is authorized',
    'Final freeze remains blocked',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 26'
]
cp['blocked'] = [
    'PHASE376_PASSIVE_VALIDATOR_REPLICATION_NOT_COMPLETE',
    'READER_EXPERIENCE_WRITING_TRANSFER_NOT_SUPPORTED',
    'SPAN_GROWTH_BLOCKED_UNTIL_REPLICATION_EVIDENCE',
    'YMGQ_WRITING_PAUSED_DURING_TRANSFER_METHOD_REPAIR',
    'CURRENT_FULL_MANUSCRIPT_ACTUAL_HUMAN_REJECTED',
    'FULL_REWRITE_BLOCKED',
    'FINAL_FREEZE_BLOCKED'
]
cp['do_not_reopen'] = list(dict.fromkeys([
    'Treat Phase375 weak Y preference as decisive transfer proof',
    'Scale Phase375 repair before replication',
    'Directly activate RX-C01 through RX-C08 as stacked prose-construction targets',
    'Claim Phase372 source extraction proves writing transfer',
    'Another immediate long pilot or full-manuscript rewrite',
    'Accepted Phase320 checkpoint or GN-VDNA-01 semantics'
] + cp.get('do_not_reopen', [])))
cp['next_required_action'] = 'Execute PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1: create and freeze a new natural short baseline, passively locate at most one material defect, make at most one minimal repair, then blind actual-human compare. Do not scale from Phase375.'
cp['source_state_refs'] = [
    {'path':'state/project_state.json','role':'authoritative Phase376 ready state'},
    {'path':'state/review_receipts/PHASE375_ACTUAL_HUMAN_BLIND_REVIEW_H1_V1.json','role':'Phase375 weak-preference actual-human settlement'},
    {'path':'state/tasks/PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1.json','role':'active Phase376 replication contract'},
    {'path':'rules/reader-experience-passive-validator-only-v1.md','role':'mandatory passive-validator calling mode'},
    {'path':'state/continuity/STATE_LEDGER.jsonl','role':'physical ledger remains verified through sequence18'}
]
cp['status'] = 'ACTIVE_PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_READY_NOT_STARTED'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
