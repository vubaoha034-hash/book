import json
from pathlib import Path

state_path = Path('state/project_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.6.0'
state['updated_at'] = '2026-09-09T17:51:00+08:00'
active = state['active_task']
assert active['task_id'] == 'PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1'
active['status'] = 'ATTEMPT2_AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
active['execution_scope'] = 'Phase376 Attempt1 was invalidated before human review due blinding contamination. Attempt2 uses a different fresh natural baseline frozen before validation; one passive-validator repair was produced and cleanly blinded. No defect detail or X/Y mapping may be disclosed before verdict. No direct RX generation, YMGQ writing, or scale-up is authorized.'
active['next_action'] = 'Actual target reader reads only PHASE376_ATTEMPT2_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt in Drive folder 小说蒸馏_真人验收 and compares X/Y. Do not disclose repair detail or mapping before verdict.'
state['phase376_attempt1'] = {
    'status': 'INVALIDATED_BEFORE_HUMAN_REVIEW',
    'receipt': 'state/review_receipts/PHASE376_ATTEMPT1_BLINDING_CONTAMINATION_V1.json',
    'counts_as_replication_evidence': False
}
state['phase376_outputs'] = {
    'attempt': 2,
    'status': 'CLEAN_BLIND_PACK_RECEIVED_PENDING_ACTUAL_HUMAN_REVIEW',
    'baseline': 'state/calibration/PHASE376_ATTEMPT2_FRESH_NATURAL_BASELINE_V1.txt',
    'baseline_git_blob_sha': '2830b20aca0dec47bbe5c7f86a5b05e6853eee9f',
    'baseline_frozen_before_validation': True,
    'diagnosis': 'state/calibration/PHASE376_ATTEMPT2_SINGLE_DEFECT_DIAGNOSIS_V1.md',
    'blind_choice_pack': 'state/calibration/PHASE376_ATTEMPT2_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt',
    'receipt': 'state/review_receipts/PHASE376_ATTEMPT2_PASSIVE_VALIDATOR_REPLICATION_PENDING_HUMAN_V1.json',
    'drive_folder_id': '1by_PdzIkx8KJYq9-z9T29egd5ZSrpcu_',
    'drive_file_id': '17_0KtKmpurIapwaM-AuQIbxx93oa0942',
    'selected_defect_count': 1,
    'repair_detail_sealed_until_human_verdict': True,
    'mapping_sealed_until_human_verdict': True,
    'direct_RX_generation_activation': False,
    'candidate_stacking': False,
    'human_review_pending': True,
    'replication_status': 'UNPROVEN',
    'span_growth_authorized': False,
    'YMGQ_writing_authorized': False,
    'accepted_checkpoint_advance': False
}
state.setdefault('reader_experience_transfer_state', {})['passive_validator_calling_mode'] = 'PHASE376_ATTEMPT2_CLEAN_HUMAN_BLIND_REVIEW_PENDING'
state['reader_experience_transfer_state']['span_growth_authorized'] = False
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 28
inv = state.setdefault('invariants', {})
inv['Phase376_attempt1_may_not_count_due_blinding_contamination'] = True
inv['Phase376_attempt2_repair_detail_may_not_be_revealed_before_human_verdict'] = True
inv['Phase376_attempt2_mapping_may_not_be_revealed_before_human_verdict'] = True
inv['Phase376_may_not_scale_before_clean_actual_human_replication_result'] = True
inv['Phase320_remains_highest_accepted_promotion_checkpoint'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')
cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 28
cp['recorded_at'] = '2026-09-09T17:52:00+08:00'
cp['active_task_ids'] = ['PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1']
cp['current_focus'] = 'Phase376 Attempt1 was invalidated before human review because the assistant disclosed the exact repair defect pre-verdict. Attempt2 now uses a different fresh natural baseline, frozen before validation, with exactly one passive-validator repair and a clean X/Y blind pack. Repair detail and mapping are sealed until actual-human verdict. Phase375 remains weak-positive only; no transfer support or scale-up exists.'
cp['completed'] = list(dict.fromkeys(cp.get('completed', []) + [
    'Phase376 Attempt1 invalidated before human review for blinding contamination; no replication evidence counted',
    'Phase376 Attempt2 fresh natural baseline created and frozen before passive validation',
    'Phase376 Attempt2 passive validation executed only after baseline freeze',
    'Exactly one minimal repair produced in Attempt2; repair detail sealed until verdict',
    'Phase376 Attempt2 clean X/Y blind comparison pack produced with mapping sealed',
    'Phase376 Attempt2 human-review artifact stored as real text/plain in Drive folder 小说蒸馏_真人验收',
    'Phase320 remains highest accepted promotion checkpoint'
]))
cp['incomplete'] = [
    'Actual target reader has not yet blind-compared Phase376 Attempt2 X/Y',
    'Passive-validator repeatability is not proven',
    'No RX candidate has TRANSFER_SUPPORTED status',
    'No bounded span-growth survival test is authorized',
    'Stable long-form scale transfer remains UNPROVEN',
    'Current full YMGQ manuscript remains actual-human rejected',
    'YMGQ writing remains paused during transfer-method repair',
    'No full-manuscript reconstruction is authorized',
    'Final freeze remains blocked',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 28'
]
cp['blocked'] = [
    'PHASE376_ATTEMPT2_ACTUAL_HUMAN_BLIND_REVIEW_PENDING',
    'PASSIVE_VALIDATOR_REPEATABILITY_UNPROVEN',
    'READER_EXPERIENCE_WRITING_TRANSFER_NOT_SUPPORTED',
    'SPAN_GROWTH_BLOCKED_UNTIL_CLEAN_REPLICATION_EVIDENCE',
    'YMGQ_WRITING_PAUSED_DURING_TRANSFER_METHOD_REPAIR',
    'CURRENT_FULL_MANUSCRIPT_ACTUAL_HUMAN_REJECTED',
    'FULL_REWRITE_BLOCKED',
    'FINAL_FREEZE_BLOCKED'
]
cp['do_not_reopen'] = list(dict.fromkeys([
    'Use Phase376 Attempt1 as replication evidence',
    'Reveal Phase376 Attempt2 repair detail or X/Y mapping before actual-human verdict',
    'Repair more than the one selected defect in Phase376 Attempt2',
    'Treat Phase375 weak preference as decisive transfer proof',
    'Scale Phase375 or Phase376 before clean replication verdict',
    'Directly activate RX-C01 through RX-C08 as stacked prose-construction targets',
    'Accepted Phase320 checkpoint or GN-VDNA-01 semantics'
] + cp.get('do_not_reopen', [])))
cp['next_required_action'] = 'Actual target reader reads only PHASE376_ATTEMPT2_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt and reports: overall X/Y/tie; desire to continue X/Y/tie; least AI-like X/Y/tie; clarity/flow X/Y/tie; tension X/Y/tie; first skim/stop point X/Y/none. Do not reveal repair detail or mapping before verdict.'
cp['source_state_refs'] = [
    {'path':'state/project_state.json','role':'authoritative Phase376 Attempt2 human-blind-review-pending state'},
    {'path':'state/review_receipts/PHASE376_ATTEMPT1_BLINDING_CONTAMINATION_V1.json','role':'invalidated Attempt1 receipt'},
    {'path':'state/tasks/PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1.json','role':'Phase376 replication contract'},
    {'path':'state/calibration/PHASE376_ATTEMPT2_FRESH_NATURAL_BASELINE_V1.txt','role':'Attempt2 frozen natural baseline'},
    {'path':'state/calibration/PHASE376_ATTEMPT2_SINGLE_DEFECT_DIAGNOSIS_V1.md','role':'private one-defect diagnosis; do not disclose pre-verdict'},
    {'path':'state/calibration/PHASE376_ATTEMPT2_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt','role':'actual-human clean X/Y blind-review artifact'},
    {'path':'state/review_receipts/PHASE376_ATTEMPT2_PASSIVE_VALIDATOR_REPLICATION_PENDING_HUMAN_V1.json','role':'sealed mapping and Drive binding receipt'},
    {'path':'rules/reader-experience-passive-validator-only-v1.md','role':'mandatory passive-validator calling mode'},
    {'path':'state/continuity/STATE_LEDGER.jsonl','role':'physical ledger remains verified through sequence18'}
]
cp['status'] = 'ACTIVE_PHASE376_ATTEMPT2_CLEAN_PASSIVE_VALIDATOR_REPLICATION_AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
