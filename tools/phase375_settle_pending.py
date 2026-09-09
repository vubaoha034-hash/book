import json
from pathlib import Path

state_path = Path('state/project_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.3.0'
state['updated_at'] = '2026-09-09T16:15:00+08:00'
active = state['active_task']
active['status'] = 'AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
active['execution_scope'] = 'Phase375 passively validated the immutable Phase373 B baseline, located exactly one redundant author-summary defect, produced one minimal repair, and blinded untouched baseline versus repair as X/Y. No other prose changed; no YMGQ writing or span growth authorized.'
active['next_action'] = 'Actual target reader reads only state/calibration/PHASE375_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt and compares X/Y on overall preference, desire to continue, AI smell, clarity/flow, tension, and skim/stop point. Mapping remains sealed until verdict.'
state['phase375_outputs'] = {
    'status': 'ONE_DEFECT_REPAIR_BLIND_PACK_RECEIVED_PENDING_ACTUAL_HUMAN_REVIEW',
    'diagnosis': 'state/calibration/PHASE375_SINGLE_DEFECT_DIAGNOSIS_V1.md',
    'blind_choice_pack': 'state/calibration/PHASE375_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt',
    'receipt': 'state/review_receipts/PHASE375_PASSIVE_VALIDATOR_SINGLE_DEFECT_REPAIR_PROBE_V1.json',
    'selected_defect_count': 1,
    'direct_RX_generation_activation': False,
    'candidate_stacking': False,
    'human_review_pending': True,
    'span_growth_authorized': False,
    'YMGQ_writing_authorized': False,
    'transfer_status': 'UNPROVEN'
}
state['reader_experience_transfer_state']['passive_validator_calling_mode'] = 'PHASE375_HUMAN_BLIND_REVIEW_PENDING'
state['continuity_settlement']['logical_latest_checkpoint_sequence'] = 25
state['invariants']['Phase375_mapping_may_not_be_revealed_before_human_verdict'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')
cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 25
cp['recorded_at'] = '2026-09-09T16:16:00+08:00'
cp['active_task_ids'] = ['PHASE375_PASSIVE_VALIDATOR_SINGLE_DEFECT_REPAIR_PROBE_V1']
cp['current_focus'] = 'Phase375 passively validated the Phase373 human-winning B/CONTROL baseline. Exactly one redundant author-summary sentence was selected for a minimal deletion repair; all unrelated prose, clues, motives, tension structure and ending were preserved. A blinded X/Y baseline-versus-repair pack now awaits actual-human judgment. Direct RX generation remains OFF, span growth remains blocked, and YMGQ writing remains paused.'
cp['completed'] = [
    'Phase372 source-anchored reader-experience layer remains complete with 90 cards and eight source-derived candidates',
    'Phase373 actual-human blind review remains CONTROL win; candidate direct-transfer signal false',
    'Phase374 activation-overconstraint diagnosis completed; RX direct generation OFF and passive validation ON',
    'Phase375 passive validation executed on immutable Phase373 B baseline',
    'Exactly one located defect selected: redundant author-summary sentence after the reader model was already explicit',
    'Exactly one minimal repair produced; no new clue, mystery, countdown, motive withholding, or candidate stacking',
    'Phase375 X/Y blind comparison pack produced and sealed mapping persisted',
    'Phase320 remains highest accepted promotion checkpoint; GN-VDNA-01 remains DEFAULT OFF'
]
cp['incomplete'] = [
    'Actual target reader has not yet blind-compared Phase375 X/Y',
    'Passive-validator repair transfer signal is unknown',
    'No RX candidate has TRANSFER_SUPPORTED status',
    'No bounded span-growth survival test is authorized',
    'Stable long-form scale transfer remains UNPROVEN',
    'Current full YMGQ manuscript remains actual-human rejected',
    'YMGQ writing remains paused during transfer-method repair',
    'No full-manuscript reconstruction is authorized',
    'Final freeze remains blocked',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 25'
]
cp['blocked'] = [
    'PHASE375_ACTUAL_HUMAN_BLIND_REVIEW_PENDING',
    'READER_EXPERIENCE_WRITING_TRANSFER_NOT_SUPPORTED',
    'SPAN_GROWTH_BLOCKED_UNTIL_PASSIVE_VALIDATOR_HUMAN_WIN',
    'YMGQ_WRITING_PAUSED_DURING_TRANSFER_METHOD_REPAIR',
    'CURRENT_FULL_MANUSCRIPT_ACTUAL_HUMAN_REJECTED',
    'FULL_REWRITE_BLOCKED',
    'FINAL_FREEZE_BLOCKED'
]
cp['do_not_reopen'] = [
    'Reveal Phase375 X/Y mapping before actual-human verdict',
    'Repair more than the one selected defect in this Phase375 iteration',
    'Treat Phase373 B/CONTROL win as a Phase372 candidate success',
    'Directly activate RX-C01 through RX-C08 as stacked prose-construction targets',
    'Claim Phase372 source extraction proves writing transfer',
    'Claim source reading alone proves writing learning',
    'Claim book/global Novel DNA validation proves prose quality',
    'Claim YMGQ improvement as evidence of GN-VDNA-01 success',
    'Another immediate long pilot or full-manuscript rewrite',
    'Accepted Phase320 checkpoint or GN-VDNA-01 semantics'
]
cp['next_required_action'] = 'Actual target reader reads only state/calibration/PHASE375_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt and answers: overall X/Y/tie; desire to continue X/Y/tie; least AI-like X/Y/tie; clarity/flow X/Y/tie; tension X/Y/tie; first skim/stop point X/Y/none. Do not reveal mapping before verdict.'
cp['source_state_refs'] = [
    {'path':'state/project_state.json','role':'authoritative Phase375 human-blind-review-pending state'},
    {'path':'state/tasks/PHASE375_PASSIVE_VALIDATOR_SINGLE_DEFECT_REPAIR_PROBE_V1.json','role':'Phase375 one-defect passive-validator contract'},
    {'path':'state/calibration/PHASE375_SINGLE_DEFECT_DIAGNOSIS_V1.md','role':'single located defect diagnosis'},
    {'path':'state/calibration/PHASE375_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt','role':'actual-human X/Y blind review artifact'},
    {'path':'state/review_receipts/PHASE375_PASSIVE_VALIDATOR_SINGLE_DEFECT_REPAIR_PROBE_V1.json','role':'sealed mapping and pending-human receipt'},
    {'path':'rules/reader-experience-passive-validator-only-v1.md','role':'mandatory passive-validator calling mode'},
    {'path':'state/continuity/STATE_LEDGER.jsonl','role':'physical ledger remains verified through sequence18'}
]
cp['status'] = 'ACTIVE_PHASE375_PASSIVE_VALIDATOR_SINGLE_DEFECT_REPAIR_AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
