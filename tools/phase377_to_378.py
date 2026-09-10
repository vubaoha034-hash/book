import json
from pathlib import Path

state_path = Path('state/project_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
state['schema_version'] = '3.8.0'
state['updated_at'] = '2026-09-10T15:18:00+08:00'
state['phase377_settlement'] = {
    'execution': 'AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_ACCEPTED_AS_EVIDENCE_NOT_REPAIR_PROOF',
    'receipt': 'state/review_receipts/PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1.json',
    'report': 'docs/PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1.md',
    'matrix': 'state/calibration/PHASE377_AI_SMELL_CONTRASTIVE_EVIDENCE_MATRIX_V1.jsonl',
    'new_rule': 'rules/ai-smell-global-optimization-diagnostic-v1.md',
    'primary_failure_family': 'AI-F01_GLOBAL_AUTHORIAL_OPTIMIZATION_REGULARITY',
    'supported_high_signatures': ['AS-01','AS-02','AS-03','AS-04','AS-06'],
    'supported_amplifiers': ['AS-05','AS-07'],
    'simple_short_sentence_rule': 'REJECTED',
    'simple_explanation_ban': 'REJECTED',
    'concrete_object_reduction_simple_rule': 'REJECTED',
    'one_sentence_deletion_primary_method': 'DOWNGRADED_NOT_REPEATABLE',
    'repair_method': 'UNPROVEN',
    'writing_transfer': 'NOT_SUPPORTED',
    'span_growth_authorized': False,
    'accepted_checkpoint_advance': False
}
state['active_task'] = {
    'task_id': 'PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1',
    'phase': 'GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE',
    'phase_ordinal': 378,
    'status': 'READY_FOR_TWO_FRESH_GENERATOR_CHATS',
    'task_contract': 'state/tasks/PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1.json',
    'execution_scope': 'Use two genuinely separate fresh generator chats on one frozen social-realism story packet. R1/R2 roles are sealed. This Phase377 chat may not generate either output because it has seen the diagnostic taxonomy. No YMGQ writing or scale-up.',
    'current_chat_generation_authorized': False,
    'fresh_generator_contexts_required': 2,
    'R1_drive_file_id': '1ChOJYeD7Y3WFupshMkAGcMbZ7DEx4mg8',
    'R2_drive_file_id': '1pm5sbHpQpdE3btCgqPxVYrQ55Zz27RCU',
    'execution_drive_folder_id': '1LXWW3Vs-Hkx19Ogwzv20w2wUjP7RgCMu',
    'role_mapping_receipt': 'state/review_receipts/PHASE378_GENERATOR_ROLE_MAPPING_SEALED_V1.json',
    'role_mapping_reveal_authorized': False,
    'YMGQ_span_growth_authorized': False,
    'full_manuscript_rewrite_authorized': False,
    'architecture_promotion_authorized': False,
    'next_action': 'Run R1 and R2 Drive invocation files in two separate brand-new ChatGPT chats; each must write its exact output to Drive and return a DONE marker plus actual Drive File ID.'
}
state.setdefault('ai_smell_state', {})['status'] = 'OPEN_BLOCKING_FAILURE_PHASE377_ROOT_CAUSE_TAXONOMY_ACCEPTED_REPAIR_UNPROVEN'
state['ai_smell_state']['primary_failure_family'] = 'AI-F01_GLOBAL_AUTHORIAL_OPTIMIZATION_REGULARITY'
state['ai_smell_state']['diagnostic_rule'] = 'rules/ai-smell-global-optimization-diagnostic-v1.md'
state['ai_smell_state']['next_required_task'] = 'PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1'
state.setdefault('reader_experience_transfer_state', {})['span_growth_authorized'] = False
state.setdefault('continuity_settlement', {})['logical_latest_checkpoint_sequence'] = 30
state.setdefault('invariants', {})['Phase377_audit_acceptance_does_not_close_ai_smell'] = True
state['invariants']['Phase378_current_chat_may_not_generate_either_arm'] = True
state['invariants']['Phase378_roles_may_not_be_revealed_before_human_verdict'] = True
state['invariants']['Phase378_requires_two_separate_fresh_generator_contexts'] = True
state['invariants']['Phase320_remains_highest_accepted_promotion_checkpoint'] = True
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

cp_path = Path('state/continuity/LATEST_CHECKPOINT.json')
cp = json.loads(cp_path.read_text(encoding='utf-8'))
cp['sequence'] = 30
cp['recorded_at'] = '2026-09-10T15:19:00+08:00'
cp['active_task_ids'] = ['PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1']
cp['current_focus'] = 'Phase377 contrastive audit accepted an evidence-supported AI-smell root-cause family: GLOBAL_AUTHORIAL_OPTIMIZATION_REGULARITY. The issue is not simply short sentences, explanation, or concrete objects; it is repeated coupling of reader-facing inference closure, maximized functional density, clue/inference/action cycles, task-processor cognition, causal neatness, generic social voice and engineered reveals. Repair remains unproven. Phase378 is prepared as an isolated process probe requiring two genuinely separate fresh generator chats; this current chat is contaminated for generation because it has seen the taxonomy.'
cp['completed'] = list(dict.fromkeys(cp.get('completed', []) + [
    'Phase377 re-opened Phase363 human-positive prose and Phase364 human-rejected long prose from private Drive',
    'Phase377 re-read representative prose surface from all three verified source novels',
    'Phase377 created a 10-entry contrastive AI-smell evidence matrix',
    'Seven AI-smell signatures accepted as evidence-supported or supported amplifiers',
    'Short-sentence ban rejected as simple AI-smell rule',
    'Explanation ban rejected as simple AI-smell rule',
    'Concrete-object reduction rejected as simple AI-smell rule',
    'AI-F01 GLOBAL_AUTHORIAL_OPTIMIZATION_REGULARITY accepted as primary open failure family',
    'rules/ai-smell-global-optimization-diagnostic-v1.md added',
    'Phase377 audit accepted as evidence; repair method remains unproven',
    'Phase378 fixed social-realism story facts packet frozen',
    'Phase378 R1/R2 fresh generator invocations created with sealed roles',
    'R1/R2 invocation files stored as real text/plain in Drive folder 小说蒸馏_新聊天执行',
    'Phase320 remains highest accepted promotion checkpoint'
]))
cp['incomplete'] = [
    'Phase378 R1 fresh generator has not yet been executed',
    'Phase378 R2 fresh generator has not yet been executed',
    'Phase378 isolated process candidate versus control human comparison is not available',
    'AI-smell repair method remains UNPROVEN',
    'AI-F01 remains OPEN_BLOCKING_FAILURE',
    'No RX candidate has TRANSFER_SUPPORTED status',
    'No bounded span-growth survival test is authorized',
    'Stable long-form scale transfer remains UNPROVEN',
    'Current full YMGQ manuscript remains actual-human rejected',
    'YMGQ writing remains paused during Phase378',
    'No full-manuscript reconstruction is authorized',
    'Final freeze remains blocked',
    'STATE_LEDGER.jsonl remains physically verified only through sequence 18; logical latest checkpoint is 30'
]
cp['blocked'] = [
    'PHASE378_TWO_FRESH_GENERATOR_OUTPUTS_PENDING',
    'AI_SMELL_REPAIR_METHOD_UNPROVEN',
    'AI_F01_GLOBAL_AUTHORIAL_OPTIMIZATION_REGULARITY_OPEN',
    'SPAN_GROWTH_BLOCKED',
    'YMGQ_WRITING_PAUSED_DURING_PHASE378',
    'CURRENT_FULL_MANUSCRIPT_ACTUAL_HUMAN_REJECTED',
    'FULL_REWRITE_BLOCKED',
    'FINAL_FREEZE_BLOCKED'
]
cp['do_not_reopen'] = list(dict.fromkeys([
    'Treat Phase377 root-cause audit as repair success',
    'Generate Phase378 R1 or R2 inside the Phase377 chat that has seen the taxonomy',
    'Reveal Phase378 R1/R2 role mapping before both outputs are frozen and human verdict is complete',
    'Use short sentences, explanation, or concrete-object counts as simple AI-smell bans',
    'Use one-sentence deletion loops as the primary AI-smell solution',
    'Equate no skim or desire to continue with low AI smell',
    'Another immediate long pilot or full-manuscript rewrite',
    'Accepted Phase320 checkpoint or GN-VDNA-01 semantics'
] + cp.get('do_not_reopen', [])))
cp['next_required_action'] = 'Execute Phase378 R1 and R2 in two separate brand-new ChatGPT chats using the Drive invocation files. Do not let either generator see this chat, the Phase377 taxonomy, the other arm, or prior human results. Each must save its output to Drive and return only DONE plus actual Drive File ID.'
cp['source_state_refs'] = [
    {'path':'state/project_state.json','role':'authoritative Phase378 fresh-generator-pending state'},
    {'path':'state/review_receipts/PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1.json','role':'Phase377 audit settlement'},
    {'path':'docs/PHASE377_AI_SMELL_ROOT_CAUSE_CONTRASTIVE_AUDIT_V1.md','role':'AI-smell contrastive audit'},
    {'path':'rules/ai-smell-global-optimization-diagnostic-v1.md','role':'global AI-smell diagnostic gate'},
    {'path':'state/tasks/PHASE378_GENERATOR_EVALUATOR_ISOLATED_AI_SMELL_PROCESS_PROBE_V1.json','role':'active Phase378 isolation contract'},
    {'path':'state/review_receipts/PHASE378_GENERATOR_ROLE_MAPPING_SEALED_V1.json','role':'sealed R1/R2 role mapping'},
    {'path':'state/continuity/STATE_LEDGER.jsonl','role':'physical ledger remains verified through sequence18'}
]
cp['status'] = 'ACTIVE_PHASE378_ISOLATED_AI_SMELL_PROCESS_PROBE_AWAITING_TWO_FRESH_GENERATOR_CHATS'
cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
