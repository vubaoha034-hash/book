import json
from pathlib import Path

state_path = Path('state/project_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.5.0'
state['updated_at'] = '2026-09-09T17:38:00+08:00'
active = state['active_task']
assert active['task_id'] == 'PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1'
active['status'] = 'AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
active['execution_scope'] = 'A fresh natural short-fiction baseline was frozen before validation. Passive RX validation located exactly one redundant author-inference sentence; exactly one deletion-only repair was produced and blinded against the untouched baseline. No direct RX generation, candidate stacking, YMGQ writing, or scale-up is authorized.'
active['next_action'] = 'Actual target reader reads only PHASE376_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt in Drive folder 小说蒸馏_真人验收 and compares X/Y. Mapping remains sealed until verdict.'
state['phase376_outputs'] = {
    'status': 'ONE_DEFECT_REPAIR_BLIND_PACK_RECEIVED_PENDING_ACTUAL_HUMAN_REVIEW',
    'baseline': 'state/calibration/PHASE376_FRESH_NATURAL_BASELINE_V1.txt',
    'baseline_git_blob_sha': '2dffb0b62830a53b1454f66900590f88bcfaf49f',
    'baseline_frozen_before_validation': True,
    'diagnosis': 'state/calibration/PHASE376_SINGLE_DEFECT_DIAGNOSIS_V1.md',
    'blind_choice_pack': 'state/calibration/PHASE376_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt',
    'receipt': 'state/review_receipts/PHASE376_PASSIVE_VALIDATOR_REPLICATION_PENDING_HUMAN_V1.json',
    'drive_folder_id': '1by_PdzIkx8KJYq9-z9T29egd5ZSrpcu_',
    'drive_file_id': '1KUS8e7iLx2mtoni7gjpul9ETQMCwc008',
    'selected_defect_count': 1,
    'direct_RX_generation_activation': False,
    'candidate_stacking': False,
    'human_review_pending': True,
    'replication_status': 'UNPROVEN',
    'span_growth_authorized': False,
    'YMGQ_writing_authorized': False,
    'accepted_checkpoint_advance': False
}
state.setdefault('reader_experience_transfer_state', {})['passive_validator_calling_mode'] = 'PHASE376_HUMAN_BLIND_REVIEW_PENDING'
state['reader_experience_transfer_state']['span_growth_authorized'] = False
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 27
state.setdefault('invariants', {})['Phase376_mapping_may_not_be_revealed_before_human_verdict'] = True
state['invariants']['Phase376_may_not_scale_before_actual_human_replication_result'] = True
state['invariants']['Phase320_remains_highest_accepted_promotion_checkpoint'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')
cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 27
cp['recorded_at'] = '2026-09-09T17:39:00+08:00'
cp['active_task_ids'] = ['PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1']
cp['current_focus'] = 'Phase376 fresh replication baseline was frozen before passive validation. Exactly one redundant author-inference sentence was selected for a deletion-only repair; baseline versus repair is now blinded as X/Y and stored in Drive folder 小说蒸馏_真人验收. Actual-human replication verdict is pending. Phase375 remains weak-positive only; no transfer support or scale-up exists yet.'
cp['completed'] = list(dict.fromkeys(cp.get('completed', []) + [
    'Phase376 fresh natural short-fiction baseline created and frozen before passive validation',
    'Phase376 passive RX validation executed only after baseline freeze',
    'Exactly one located defect selected: redundant author inference immediately before concrete reveal',
    'Exactly one deletion-only repair produced; all unrelated prose and story facts preserved',
    'Phase376 X/Y blind comparison pack produced with mapping sealed',
    'Phase376 human-review artifact stored as real text/plain in Drive folder 小说蒸馏_真人验收',
    'Phase320 remains highest accepted promotion checkpoint'
]))
cp['incomplete'] = [
    'Actual target reader has not yet blind-compared Phase376 X/Y',
    'Passive-validator repeatability is not proven',
    'No RX candidate has TRANSFER_SUPPORTED status',
    'No bounded span-growth survival test is authorized',
    'Stable long-form scale transfer remains UNPROVEN',
    'Current full YMGQ manuscript remains actual-human rejected',
    'YMGQ writing remains paused during transfer-method repair',
    'No full-manuscript reconstruction is authorized',
    'Final freeze remains blocked',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 27'
]
cp['blocked'] = [
    'PHASE376_ACTUAL_HUMAN_BLIND_REVIEW_PENDING',
    'PASSIVE_VALIDATOR_REPEATABILITY_UNPROVEN',
    'READER_EXPERIENCE_WRITING_TRANSFER_NOT_SUPPORTED',
    'SPAN_GROWTH_BLOCKED_UNTIL_REPLICATION_EVIDENCE',
    'YMGQ_WRITING_PAUSED_DURING_TRANSFER_METHOD_REPAIR',
    'CURRENT_FULL_MANUSCRIPT_ACTUAL_HUMAN_REJECTED',
    'FULL_REWRITE_BLOCKED',
    'FINAL_FREEZE_BLOCKED'
]
cp['do_not_reopen'] = list(dict.fromkeys([
    'Reveal Phase376 X/Y mapping before actual-human verdict',
    'Repair more than the one selected defect in Phase376',
    'Treat Phase375 weak Y preference as decisive transfer proof',
    'Scale Phase375 or Phase376 before replication verdict',
    'Directly activate RX-C01 through RX-C08 as stacked prose-construction targets',
    'Accepted Phase320 checkpoint or GN-VDNA-01 semantics'
] + cp.get('do_not_reopen', [])))
cp['next_required_action'] = 'Actual target reader reads only PHASE376_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt and reports: overall X/Y/tie; desire to continue X/Y/tie; least AI-like X/Y/tie; clarity/flow X/Y/tie; tension X/Y/tie; first skim/stop point X/Y/none. Do not reveal mapping before verdict.'
cp['source_state_refs'] = [
    {'path':'state/project_state.json','role':'authoritative Phase376 human-blind-review-pending state'},
    {'path':'state/tasks/PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_V1.json','role':'Phase376 replication contract'},
    {'path':'state/calibration/PHASE376_FRESH_NATURAL_BASELINE_V1.txt','role':'frozen natural baseline'},
    {'path':'state/calibration/PHASE376_SINGLE_DEFECT_DIAGNOSIS_V1.md','role':'one located defect diagnosis'},
    {'path':'state/calibration/PHASE376_PASSIVE_VALIDATOR_BLIND_CHOICE_PACK_V1.txt','role':'actual-human X/Y blind-review artifact'},
    {'path':'state/review_receipts/PHASE376_PASSIVE_VALIDATOR_REPLICATION_PENDING_HUMAN_V1.json','role':'sealed mapping and Drive binding receipt'},
    {'path':'rules/reader-experience-passive-validator-only-v1.md','role':'mandatory passive-validator calling mode'},
    {'path':'state/continuity/STATE_LEDGER.jsonl','role':'physical ledger remains verified through sequence18'}
]
cp['status'] = 'ACTIVE_PHASE376_FRESH_NATURAL_BASELINE_PASSIVE_VALIDATOR_REPLICATION_AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
