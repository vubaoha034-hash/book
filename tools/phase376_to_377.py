import json
from pathlib import Path

state_path = Path('state/project_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.7.0'
state['updated_at'] = '2026-09-10T14:37:00+08:00'
state['phase376_settlement'] = {
    'execution': 'ATTEMPT1_INVALIDATED_ATTEMPT2_ACTUAL_HUMAN_REPLICATION_COMPLETE_BASELINE_WIN',
    'attempt1_receipt': 'state/review_receipts/PHASE376_ATTEMPT1_BLINDING_CONTAMINATION_V1.json',
    'attempt2_human_receipt': 'state/review_receipts/PHASE376_ATTEMPT2_ACTUAL_HUMAN_BLIND_REVIEW_H1_V1.json',
    'attempt2_revealed_mapping': {'X':'SINGLE_DEFECT_REPAIR','Y':'BASELINE_UNTOUCHED'},
    'overall_preference': 'Y_BASELINE',
    'desire_to_continue': 'Y_BASELINE',
    'clarity_flow': 'Y_BASELINE',
    'tension': 'Y_BASELINE',
    'ai_smell': 'BOTH_HEAVY',
    'first_skim_or_stop': 'NONE_FOR_BOTH',
    'phase375_weak_positive_replicated': False,
    'passive_validator_repeatability': 'FAILED',
    'repair_transfer_signal': False,
    'span_growth_authorized': False,
    'accepted_checkpoint_advance': False
}
state['active_task'] = {
    'task_id': 'PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1',
    'phase': 'AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT',
    'phase_ordinal': 377,
    'status': 'READY_NOT_STARTED',
    'task_contract': 'state/tasks/PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1.json',
    'execution_scope': 'Contrast human-positive and AI-heavy generated prose against recoverable source-prose surface evidence to identify actual AI-smell signatures. No new fiction generation, no one-sentence repair loop, no YMGQ writing, no scale-up.',
    'new_fiction_generation_authorized': False,
    'direct_RX_generation_activation': False,
    'passive_RX_validation_as_primary_repair': False,
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Execute Phase377 contrastive AI-smell evidence audit before any new repair experiment.'
}
state.setdefault('reader_experience_transfer_state', {})['passive_validator_calling_mode'] = 'PHASE376_VALID_REPLICATION_FAILED_NOT_PRIMARY_REPAIR_PATH'
state['reader_experience_transfer_state']['span_growth_authorized'] = False
state['ai_smell_state'] = {
    'status': 'OPEN_BLOCKING_FAILURE',
    'latest_actual_human_evidence': 'PHASE376_ATTEMPT2_BOTH_VARIANTS_HEAVY_AI_SMELL_NO_SKIM',
    'story_propulsion_separable_from_ai_smell': True,
    'one_sentence_deletion_method': 'NOT_REPEATABLE_NOT_PRIMARY_REPAIR',
    'next_required_task': 'PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1'
}
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 29
state.setdefault('invariants', {})['Phase376_baseline_win_may_not_be_rewritten_as_repair_success'] = True
state['invariants']['Phase375_weak_positive_is_not_repeatable_evidence'] = True
state['invariants']['no_skim_does_not_imply_low_ai_smell'] = True
state['invariants']['Phase377_may_not_generate_new_fiction'] = True
state['invariants']['Phase320_remains_highest_accepted_promotion_checkpoint'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')
cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 29
cp['recorded_at'] = '2026-09-10T14:38:00+08:00'
cp['active_task_ids'] = ['PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1']
cp['current_focus'] = 'Phase376 Attempt2 valid blind replication ended with Y/untouched baseline winning multiple human judgments over X/single-defect repair. Both versions were judged strongly AI-like, while neither caused skim. Therefore Phase375 weak repair preference did not replicate, one-sentence passive deletion is not a validated primary repair method, and story propulsion must be separated from prose-surface AI smell. Phase377 now audits AI-smell root causes contrastively before any new fiction repair experiment.'
cp['completed'] = list(dict.fromkeys(cp.get('completed', []) + [
    'Phase376 Attempt2 actual-human blind review completed',
    'Phase376 Attempt2 mapping revealed after verdict: X=single-defect repair, Y=untouched baseline',
    'Human preferred Y baseline on multiple judgments',
    'Both Phase376 Attempt2 versions judged heavy AI smell',
    'Neither Phase376 Attempt2 version produced a skim/stop point',
    'Phase375 weak-positive passive-validator signal failed clean replication',
    'One-sentence deletion repair loop removed as primary repair path',
    'Phase377 AI-smell root-cause contrastive audit task created',
    'Phase320 remains highest accepted promotion checkpoint'
]))
cp['incomplete'] = [
    'Phase377 AI-smell root-cause contrastive audit has not yet been executed',
    'The dominant prose-surface causes of target-reader AI smell are not yet evidence-ranked',
    'No repair method for heavy AI smell is validated',
    'No RX candidate has TRANSFER_SUPPORTED status',
    'No bounded span-growth survival test is authorized',
    'Stable long-form scale transfer remains UNPROVEN',
    'Current full YMGQ manuscript remains actual-human rejected',
    'YMGQ writing remains paused during AI-smell root-cause audit',
    'No full-manuscript reconstruction is authorized',
    'Final freeze remains blocked',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 29'
]
cp['blocked'] = [
    'HEAVY_AI_SMELL_ROOT_CAUSE_NOT_YET_RESOLVED',
    'PASSIVE_VALIDATOR_REPEATABILITY_FAILED',
    'READER_EXPERIENCE_WRITING_TRANSFER_NOT_SUPPORTED',
    'SPAN_GROWTH_BLOCKED',
    'YMGQ_WRITING_PAUSED_DURING_PHASE377',
    'CURRENT_FULL_MANUSCRIPT_ACTUAL_HUMAN_REJECTED',
    'FULL_REWRITE_BLOCKED',
    'FINAL_FREEZE_BLOCKED'
]
cp['do_not_reopen'] = list(dict.fromkeys([
    'Treat Phase376 X repair as successful despite human baseline win',
    'Treat Phase375 weak repair preference as repeatable evidence',
    'Use one-sentence deletion loops as the primary AI-smell solution',
    'Equate no skim with low AI smell',
    'Directly activate RX-C01 through RX-C08 as stacked prose-construction targets',
    'Another immediate long pilot or full-manuscript rewrite',
    'Accepted Phase320 checkpoint or GN-VDNA-01 semantics'
] + cp.get('do_not_reopen', [])))
cp['next_required_action'] = 'Execute PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1. Compare human-positive and AI-heavy generated prose with recoverable source-prose surface evidence; rank actual AI-smell signatures with located evidence. Do not generate new fiction during this audit.'
cp['source_state_refs'] = [
    {'path':'state/project_state.json','role':'authoritative Phase377 ready state'},
    {'path':'state/review_receipts/PHASE376_ATTEMPT2_ACTUAL_HUMAN_BLIND_REVIEW_H1_V1.json','role':'valid Phase376 replication failure and heavy-AI-smell human evidence'},
    {'path':'state/tasks/PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1.json','role':'active Phase377 audit contract'},
    {'path':'state/review_receipts/REAL_MANUSCRIPT_YMGQ_PHASE363_EMBODIED_DIALOGUE_FUSION_ROUND3_V1.json','role':'historical human-positive bounded prose anchor'},
    {'path':'state/calibration/PHASE370_B_MOTIVE_CLARITY_REPAIR_V1.txt','role':'latest positive YMGQ bounded prose evidence'},
    {'path':'state/continuity/STATE_LEDGER.jsonl','role':'physical ledger remains verified through sequence18'}
]
cp['status'] = 'ACTIVE_PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_READY_NOT_STARTED'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
