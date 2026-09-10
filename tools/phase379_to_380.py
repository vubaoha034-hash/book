import json
from pathlib import Path

# one-shot Phase379 -> Phase380 authoritative transition
state_path = Path('state/project_state.json')
cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')

state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '4.0.0'
state['updated_at'] = '2026-09-10T16:40:00+08:00'
state['phase379_settlement'] = {
    'execution': 'ACCEPT_TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_DIAGNOSTIC_ONLY',
    'task': 'state/tasks/PHASE379_TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_V1.json',
    'matrix': 'state/calibration/PHASE379_TARGET_READER_AI_SMELL_CONTRASTIVE_MATRIX_V1.jsonl',
    'report': 'docs/PHASE379_TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_V1.md',
    'rule': 'rules/target-reader-ai-smell-discriminator-v1.md',
    'receipt': 'state/review_receipts/PHASE379_TARGET_READER_AI_SMELL_DISCRIMINATOR_RECALIBRATION_V1.json',
    'phase378_PROCESS_protocol_rejected': True,
    'phase377_model_evaluator_directional_false_positive_confirmed': True,
    'AS_F01_functionally_exact_dialogue_adjacency_ladder_added': True,
    'global_authorial_optimization_retained_as_diagnostic_not_scalar_gate': True,
    'automatic_AI_smell_evaluator_reliable': False,
    'generation_repair_proven': False,
    'accepted_checkpoint_advance': False
}
state['active_task'] = {
    'task_id': 'PHASE380_PROSPECTIVE_TARGET_READER_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1',
    'phase': 'PROSPECTIVE_TARGET_READER_AI_SMELL_DISCRIMINATOR_CALIBRATION',
    'phase_ordinal': 380,
    'status': 'READY_NOT_STARTED',
    'task_contract': 'state/tasks/PHASE380_PROSPECTIVE_TARGET_READER_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1.json',
    'execution_scope': 'Prospectively test the recalibrated target-reader AI-smell discriminator on a new neutral fresh pair. Generators receive equivalent ordinary prompts and may not see the discriminator. Freeze both outputs, seal evaluator prediction before human blind review, then compare direction. No generation-repair protocol is being tested in this phase.',
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Prepare a new neutral fixed story-facts packet and two equivalent fresh generator invocation files. Do not generate prose in the current evaluator context.'
}
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 33
state.setdefault('invariants', {})['Phase379_generic_backfire_task_superseded'] = True
state['invariants']['Phase379_discriminator_is_diagnostic_only'] = True
state['invariants']['Phase380_may_not_expose_discriminator_to_generators'] = True
state['invariants']['Phase380_single_correct_prediction_may_not_promote_gate'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 33
cp['recorded_at'] = '2026-09-10T16:41:00+08:00'
cp['active_task_ids'] = ['PHASE380_PROSPECTIVE_TARGET_READER_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1']
cp['status'] = 'ACTIVE_PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_READY'
cp['current_focus'] = 'Phase379 target-reader AI-smell discriminator recalibration is complete and accepted only as diagnostic calibration. Phase378 PROCESS was decisively rejected; CONTROL won but retained some AI smell. The previous model evaluator produced a directional false positive. Phase379 added AS-F01 functionally exact dialogue adjacency ladder as a high-priority local discriminator and retained Phase377 global signatures only as diagnostic context. Phase380 will prospectively test evaluator direction on a new neutral fresh pair before using any discriminator to guide generation.'
cp['next_required_action'] = 'Prepare Phase380 new neutral fixed story facts and two equivalent fresh generator invocations; execute them in genuinely separate new chats, freeze outputs, seal discriminator prediction, then obtain actual-human blind verdict.'
completed = cp.setdefault('completed', [])
for item in [
    'Phase379 target-reader AI-smell contrastive matrix completed',
    'Phase379 discriminator recalibration report completed',
    'rules/target-reader-ai-smell-discriminator-v1.md completed',
    'Phase379 diagnostic recalibration accepted; generation repair remains unproven',
    'Generic Phase379 PROCESS backfire task superseded by the more specific completed recalibration task'
]:
    if item not in completed:
        completed.append(item)
obsolete = {
    'Phase379 PROCESS backfire diagnosis pending',
    'Phase378 actual target-reader blind verdict is pending',
    'Phase378 process-level AI-smell transfer signal is not yet established'
}
cp['incomplete'] = [item for item in cp.get('incomplete', []) if item not in obsolete]
for item in [
    'Phase380 prospective discriminator calibration not yet executed',
    'Reliable AI-smell evaluator remains unproven',
    'Stable low-AI generation process remains unproven',
    'Stable long-form scale transfer remains UNPROVEN'
]:
    if item not in cp['incomplete']:
        cp['incomplete'].append(item)
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
