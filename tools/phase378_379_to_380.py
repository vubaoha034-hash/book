import json
from pathlib import Path

state_path = Path('state/project_state.json')
cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')

state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.10.0'
state['updated_at'] = '2026-09-10T16:52:00+08:00'
state['active_task'] = {
    'task_id': 'PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1',
    'phase': 'PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION',
    'phase_ordinal': 380,
    'status': 'READY_FOR_TWO_FRESH_NEUTRAL_GENERATOR_CHATS',
    'task_contract': 'state/tasks/PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1.json',
    'execution_scope': 'Two neutral fresh generators receive equivalent story facts with no Phase377/379 diagnosis and no anti-AI process intervention. After both outputs are frozen, the recalibrated discriminator must seal a directional AI-smell prediction before target-reader blind review.',
    'R1_drive_file_id': '1OiASyZl6Lhv0qLw7-RVoHwWp9QyirI4z',
    'R2_drive_file_id': '1a16_NQn7suEMe0yeeo4KE3WQ45NIRW1W',
    'execution_drive_folder_id': '1LXWW3Vs-Hkx19Ogwzv20w2wUjP7RgCMu',
    'YMGQ_writing_authorized': False,
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Run R1 and R2 Drive invocation files in two separate brand-new chats and return each DONE marker plus actual output Drive File ID.'
}
state['phase378_settlement'] = {
    'execution': 'TWO_FRESH_GENERATORS_COMPLETED_AND_ACTUAL_HUMAN_BLIND_REVIEW_COMPLETE',
    'human_receipt': 'state/review_receipts/PHASE378_ACTUAL_HUMAN_BLIND_REVIEW_H1_V1.json',
    'A': 'R1_PROCESS',
    'B': 'R2_CONTROL',
    'human_overall_preference': 'B_CONTROL',
    'human_lower_ai_smell': 'B_CONTROL',
    'A_ai_smell': 'VERY_HEAVY',
    'B_ai_smell': 'SOME_BUT_NOT_STRONG',
    'human_A_clarity': 'MESSY_WITH_SKIM_OR_STOP_URGE',
    'first_A_ai_smell_locator': '你要那个？ / 他说过给我。 / 什么时候？',
    'sealed_model_prediction': 'R1_LOWER_AI_SMELL_THAN_R2',
    'model_prediction_correct': False,
    'PROCESS_protocol_supported': False,
    'process_level_transfer_signal': False,
    'accepted_checkpoint_advance': False
}
state['phase379_settlement'] = {
    'execution': 'TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_ACCEPTED_DIAGNOSTIC_ONLY',
    'receipt': 'state/review_receipts/PHASE379_TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_V1.json',
    'report': 'docs/PHASE379_TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_V1.md',
    'matrix': 'state/calibration/PHASE379_TARGET_READER_AI_SMELL_CONTRASTIVE_MATRIX_V1.jsonl',
    'rule': 'rules/target-reader-ai-smell-discriminator-v1.md',
    'AS_F01_status': 'HIGH_PRIORITY_TARGET_READER_CANDIDATE_NOT_UNIVERSAL_RULE',
    'phase377_global_family_status': 'RETAINED_DIAGNOSTIC_NOT_SUFFICIENT_GATE',
    'model_AI_smell_evaluator_status': 'DIAGNOSTIC_ONLY_UNTIL_PROSPECTIVE_REPLICATIONS',
    'generation_repair_proven': False,
    'accepted_checkpoint_advance': False
}
state['phase380_execution_state'] = {
    'neutral_generator_invocations_ready': True,
    'generation_started': False,
    'discriminator_prediction_sealed': False,
    'human_blind_review_pending': False,
    'quality_gate_promoted': False,
    'generation_repair_supported': False,
    'accepted_checkpoint_advance': False
}
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 32
inv = state.setdefault('invariants', {})
inv['Phase378_PROCESS_protocol_may_not_be_reused_as_validated_repair'] = True
inv['Phase379_AI_smell_evaluator_is_diagnostic_only_until_prospective_replication'] = True
inv['Phase380_generators_may_not_receive_Phase377_or_Phase379_diagnostics'] = True
inv['Phase380_may_not_authorize_YMGQ_writing_or_scale'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 32
cp['recorded_at'] = '2026-09-10T16:53:00+08:00'
cp['active_task_ids'] = ['PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1']
cp['current_focus'] = 'Phase378 blinded target reader decisively preferred CONTROL/B over PROCESS/A on all six comparative judgments; PROCESS/A was very AI-heavy and felt messy. The sealed model evaluator predicted the opposite, so Phase379 recalibrated the AI-smell discriminator by adding high-priority functionally exact dialogue adjacency ladders while retaining Phase377 global signatures as diagnostic only. Phase380 now prospectively tests discriminator direction on two neutral fresh-generator outputs before any new generation intervention.'
cp['status'] = 'ACTIVE_PHASE380_READY_FOR_TWO_FRESH_NEUTRAL_GENERATOR_CHATS'
completed = cp.setdefault('completed', [])
for item in [
    'Phase378 actual-human blind verdict completed: B/R2/CONTROL wins all six comparisons',
    'Phase378 PROCESS/R1 rejected: A judged very AI-heavy and messy',
    'Phase378 sealed pre-human evaluator direction was false positive',
    'Phase379 target-reader AI-smell discriminator recalibration completed and accepted diagnostic-only',
    'Phase379 added AS-F01 functionally exact dialogue adjacency ladder as high-priority target-reader candidate',
    'Phase380 fixed neutral story facts and two equivalent fresh generator invocation files created',
    'Phase380 R1/R2 invocation files stored as text/plain in Drive folder 小说蒸馏_新聊天执行'
]:
    if item not in completed:
        completed.append(item)
incomplete = cp.setdefault('incomplete', [])
for item in [
    'Phase380 two neutral fresh generator outputs have not yet been produced',
    'Phase380 prospective discriminator prediction has not yet been sealed',
    'Target-reader AI-smell evaluator remains DIAGNOSTIC ONLY',
    'Generation repair remains UNPROVEN',
    'Stable long-form scale transfer remains UNPROVEN'
]:
    if item not in incomplete:
        incomplete.append(item)
cp['next_required_action'] = 'Run Phase380 R1 Drive invocation 1OiASyZl6Lhv0qLw7-RVoHwWp9QyirI4z and R2 Drive invocation 1a16_NQn7suEMe0yeeo4KE3WQ45NIRW1W in two separate brand-new ChatGPT chats. Return only the two DONE markers with actual output Drive File IDs.'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# trigger one-shot workflow after workflow file exists
