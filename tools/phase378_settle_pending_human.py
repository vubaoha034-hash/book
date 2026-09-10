import json
from pathlib import Path

state_path = Path('state/project_state.json')
cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')

state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.8.1'
state['updated_at'] = '2026-09-10T16:16:00+08:00'
state['active_task'] = {
    'task_id': 'PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1',
    'phase': 'GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE',
    'phase_ordinal': 378,
    'status': 'AWAITING_ACTUAL_HUMAN_BLIND_REVIEW',
    'task_contract': 'state/tasks/PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1.json',
    'execution_scope': 'Two genuinely separate fresh generator chats completed R1 and R2 on the same frozen story facts. Both raw text/plain outputs were fetched, byte-frozen and independently evaluated only after freeze. A/B mapping and generator role mapping remain sealed. No output rewrite, YMGQ writing or scale-up is authorized before actual-human blind verdict.',
    'R1_output_drive_file_id': '1SZ7OiqyxlcnYIF8RaYXMjCPcPsCfVLkd',
    'R2_output_drive_file_id': '1JXokSBnxk6KeDoMMHsTgN60YyZwy4uvG',
    'output_freeze_receipt': 'state/review_receipts/PHASE378_GENERATOR_OUTPUT_FREEZE_AND_PREHUMAN_EVALUATOR_V1.json',
    'human_blind_review_receipt': 'state/review_receipts/PHASE378_ACTUAL_HUMAN_BLIND_REVIEW_PENDING_V1.json',
    'human_blind_review_drive_file_id': '1Yn1vXyhWKyw4FAlj5fWNIhhxmRfncjrP',
    'role_mapping_reveal_authorized': False,
    'A_B_mapping_reveal_authorized': False,
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Actual target reader reads only PHASE378_ACTUAL_HUMAN_BLIND_REVIEW_PACK_V1.txt in Drive folder 小说蒸馏_真人验收 and reports the 11 requested judgments. Do not reveal A/B or R1/R2 roles before verdict.'
}
state['phase378_execution_state'] = {
    'generation_complete': True,
    'both_outputs_frozen': True,
    'pre_human_evaluator_complete_sealed': True,
    'human_blind_review_pending': True,
    'transfer_supported': False,
    'span_growth_authorized': False,
    'accepted_checkpoint_advance': False
}
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 31
state.setdefault('invariants', {})['Phase378_mapping_may_not_be_revealed_before_actual_human_verdict'] = True
state['invariants']['Phase378_outputs_may_not_be_rewritten_before_actual_human_verdict'] = True
state['invariants']['Phase378_short_probe_may_not_authorize_long_form_scale'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 31
cp['recorded_at'] = '2026-09-10T16:17:00+08:00'
cp['active_task_ids'] = ['PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1']
cp['current_focus'] = 'Phase378 R1/R2 fresh generator outputs are complete and byte-frozen. A separate post-generation evaluator applied Phase377 diagnostics after freeze and sealed its pre-human prediction. A deterministic hash-derived A/B blind pack is now in Drive. Actual-human AI-smell and reading-quality verdict is pending; mappings remain sealed. No YMGQ writing or scale-up is authorized.'
cp['next_required_action'] = 'Actual target reader reads only PHASE378_ACTUAL_HUMAN_BLIND_REVIEW_PACK_V1.txt (Drive ID 1Yn1vXyhWKyw4FAlj5fWNIhhxmRfncjrP) and reports the requested A/B judgments. Do not reveal A/B to R1/R2 or R1/R2 to CONTROL/PROCESS before verdict.'
cp['status'] = 'ACTIVE_PHASE378_TWO_FRESH_OUTPUTS_FROZEN_AWAITING_ACTUAL_HUMAN_BLIND_REVIEW'
completed = cp.setdefault('completed', [])
for item in [
    'Phase378 R1 and R2 executed in two genuinely separate fresh generator chats',
    'Both Phase378 generated outputs fetched as text/plain and frozen by SHA-256 before human review',
    'Separate post-generation Phase377 evaluator completed and sealed before human review',
    'Phase378 A/B order derived deterministically from frozen output hashes rather than evaluator preference',
    'Phase378 actual-human blind-review pack stored in Drive folder 小说蒸馏_真人验收'
]:
    if item not in completed:
        completed.append(item)
incomplete = cp.setdefault('incomplete', [])
for item in [
    'Phase378 actual target-reader blind verdict is pending',
    'Phase378 process-level AI-smell transfer signal is not yet established',
    'Stable long-form scale transfer remains UNPROVEN'
]:
    if item not in incomplete:
        incomplete.append(item)
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
