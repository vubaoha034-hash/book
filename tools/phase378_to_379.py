import json
from pathlib import Path

state_path = Path('state/project_state.json')
cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')

state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.9.0'
state['updated_at'] = '2026-09-10T16:24:00+08:00'
state['phase378_settlement'] = {
    'actual_human_review_complete': True,
    'A': 'R1_PROCESS',
    'B': 'R2_CONTROL',
    'human_overall_preference': 'B',
    'human_lower_ai_smell': 'B',
    'human_more_human_written_feel': 'B',
    'human_desire_to_continue': 'B',
    'human_character_naturalness': 'B',
    'human_clarity_flow': 'B',
    'A_ai_smell': 'VERY_HEAVY',
    'B_ai_smell': 'SOME_BUT_NOT_STRONG',
    'A_skim_or_stop': 'YES_OR_CLEAR_URGE_DUE_TO_MESSY_FEEL',
    'process_level_transfer_signal': False,
    'control_won_this_replicate': True,
    'pre_human_model_prediction_correct': False,
    'span_growth_authorized': False,
    'accepted_checkpoint_advance': False
}
state['active_task'] = {
    'task_id': 'PHASE379_PROCESS_PROTOCOL_BACKFIRE_DIAGNOSIS_V1',
    'phase': 'PROCESS_PROTOCOL_BACKFIRE_DIAGNOSIS',
    'phase_ordinal': 379,
    'status': 'READY_NOT_STARTED',
    'task_contract': 'state/tasks/PHASE379_PROCESS_PROTOCOL_BACKFIRE_DIAGNOSIS_V1.json',
    'execution_scope': 'Diagnose why the Phase378 PROCESS drafting protocol worsened actual-human AI smell and disorder using only the frozen R1/R2 pair, actual-human locator, and sealed evaluator record. Do not generate or rewrite prose during diagnosis.',
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Run Phase379 contrastive diagnosis and redesign the process/evaluator before any new prose generation.'
}
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 32
state.setdefault('invariants', {})['Phase378_PROCESS_may_not_be_claimed_successful'] = True
state['invariants']['Phase378_CONTROL_may_not_be_called_AI_free'] = True
state['invariants']['Phase378_model_evaluator_may_not_override_actual_human'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 32
cp['recorded_at'] = '2026-09-10T16:25:00+08:00'
cp['active_task_ids'] = ['PHASE379_PROCESS_PROTOCOL_BACKFIRE_DIAGNOSIS_V1']
cp['current_focus'] = 'Phase378 actual-human blind verdict is complete. A=R1=PROCESS and B=R2=CONTROL. B won overall preference, lower AI smell, more human-written feel, desire to continue, character naturalness and clarity/flow. A was judged very AI-heavy and messy enough to create a skim/stop urge. B still has some AI smell and is not accepted as AI-free. The sealed pre-human evaluator predicted the opposite AI-smell direction and failed this replicate. Phase379 must diagnose PROCESS backfire before any new generation.'
cp['next_required_action'] = 'Execute PHASE379_PROCESS_PROTOCOL_BACKFIRE_DIAGNOSIS_V1 using the frozen Phase378 pair and actual-human locator; do not write new fiction yet.'
cp['status'] = 'ACTIVE_PHASE379_PROCESS_PROTOCOL_BACKFIRE_DIAGNOSIS_READY'
completed = cp.setdefault('completed', [])
for item in [
    'Phase378 actual-human blind review completed',
    'Phase378 mapping revealed after verdict: A=R1=PROCESS, B=R2=CONTROL',
    'Phase378 CONTROL won all six comparative human judgments',
    'Phase378 PROCESS judged very AI-heavy and messy enough to create skim/stop urge',
    'Phase378 CONTROL still has some AI smell; no AI-free claim authorized',
    'Phase378 sealed model evaluator prediction failed against actual-human direction'
]:
    if item not in completed:
        completed.append(item)
incomplete = cp.setdefault('incomplete', [])
for item in [
    'Phase379 PROCESS backfire diagnosis pending',
    'Reliable AI-smell evaluator remains unproven',
    'Stable low-AI generation process remains unproven',
    'Stable long-form scale transfer remains UNPROVEN'
]:
    if item not in incomplete:
        incomplete.append(item)
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
