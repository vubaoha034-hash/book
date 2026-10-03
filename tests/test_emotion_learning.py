"""Corrupt frozen artifacts and claims; no paid/model calls or prose generation."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('emotion_learning_gate', REPO / 'scripts/verify_emotion_learning.py')
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)


class EmotionLearningTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project = json.loads((REPO / 'state/project_state.json').read_bytes())
        self.checkpoint = json.loads((REPO / 'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route = self.project['emotion_pacing_learning']
        self.seen = set()
        self.copy('START_HERE.md')
        self.copy_refs(self.route)
        self.copy_refs(self.project['r2_entry_short_trial'])
        self.copy(gate.runner.DIRECTORY + '/diagnosis.attempt.json')
        # Test checkpoint197's immutable diagnosis and human UNKNOWN field in
        # its own view; the later direct retention answer has separate tests.
        human = self.read(self.route['human_feedback']['path'])
        for value in (self.project, self.checkpoint):
            value.pop('two_role_opening_review', None)
            value.update(human_verdict_receipt=self.route['human_feedback']['path'], latest_human_review=human['review'],
                last_completed_task_id=gate.TASK, last_completed_task_contract=self.route['task']['path'],
                next_action=gate.NEXT_ACTION, next_required_action=gate.NEXT_ACTION,
                current_human_gate='CURRENT_395_HUMAN_FAIL_OLD_448_FAIL_ORIGINAL_404_UNKNOWN')
        self.checkpoint.update(sequence=197,stop=True)
        entry = self.root / 'START_HERE.md'
        entry.write_text('当前位置：检查点197。\n'+entry.read_text(encoding='utf-8'),encoding='utf-8')

    def copy(self, path):
        if path in self.seen or not (REPO / path).is_file(): return
        self.seen.add(path)
        target = self.root / path; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / path).read_bytes())
        if path.endswith('.json'): self.copy_refs(json.loads(target.read_bytes()))

    def copy_refs(self, value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')): self.copy(value['path'])
            for child in value.values(): self.copy_refs(child)
        elif isinstance(value, list):
            for child in value: self.copy_refs(child)

    def read(self, path): return json.loads((self.root / path).read_bytes())

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def refresh(self, value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')):
                p = self.root / value['path']
                if p.is_file():
                    data = p.read_bytes(); value.update(blob=gate.blob(data), sha256=hashlib.sha256(data).hexdigest())
            for child in value.values(): self.refresh(child)
        elif isinstance(value, list):
            for child in value: self.refresh(child)

    def rebind(self):
        for key in ('human_feedback', 'authorization', 'manifest', 'runtime', 'evidence', 'settlement',
                    'next_task_proposal', 'result', 'task'):
            path = self.route[key]['path']; value = self.read(path)
            self.refresh(value); self.write(path, value)
        self.refresh(self.route)
        self.checkpoint['emotion_pacing_learning'] = copy.deepcopy(self.route)

    def mutate(self, key, callback):
        p = self.route[key]['path']; value = self.read(p); callback(value); self.write(p, value); self.rebind()

    def verify(self, previous=gate.OLD_ACTION):
        return gate.learning_action(self.root, self.project, self.checkpoint, previous)

    def blocked(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern): self.verify()

    def test_real_diagnosis_keeps_human_fail_and_zero_budget(self):
        self.assertEqual(self.verify(), gate.NEXT_ACTION)
        self.assertEqual(self.route['human_quality_result'], 'FAIL')
        self.assertEqual(self.route['generation_count'], 0)

    def test_cannot_skip_old_human_failure_and_consumed_trial(self):
        with self.assertRaisesRegex(ValueError, 'CANNOT_SKIP_HISTORICAL_GATES'): self.verify('WRITE_NEW')

    def test_feedback_cannot_bind_old_448_or_original_404(self):
        self.mutate('human_feedback', lambda v: v['review'].update(bound_artifact_path='delivery/local-revision-rc3-r2/short-r2-a1.md'))
        self.blocked('ACTUAL_HUMAN_FEEDBACK_OR_ARTIFACT')

    def test_original_human_words_cannot_be_replaced_by_ai_label(self):
        self.mutate('human_feedback', lambda v: v['review'].update(human_exact_feedback='AI判定很精彩'))
        self.blocked('ACTUAL_HUMAN_FEEDBACK_OR_ARTIFACT')

    def test_not_provided_stop_sentence_cannot_be_invented(self):
        self.mutate('human_feedback', lambda v: v['review'].update(exact_stop_sentence='我自己找他们公开的电话'))
        self.blocked('ACTUAL_HUMAN_FEEDBACK_OR_ARTIFACT')

    def test_not_answered_continue_question_cannot_be_filled_in(self):
        self.mutate('human_feedback', lambda v: v['review'].update(wants_to_continue=False))
        self.blocked('ACTUAL_HUMAN_FEEDBACK_OR_ARTIFACT')

    def test_latest_human_pointer_cannot_stay_on_old_failure(self):
        self.project['human_verdict_receipt'] = self.route['previous_human_feedback']['path']
        self.blocked('LATEST_HUMAN_MIRROR')

    def test_body_cannot_be_rewritten_even_when_rehashed(self):
        p = self.root / gate.BODY; p.write_text(p.read_text(encoding='utf-8') + '新一句', encoding='utf-8'); self.rebind()
        self.blocked('ACTUAL_HUMAN_FEEDBACK_OR_ARTIFACT')

    def test_learning_authorization_cannot_reset_writing_budget(self):
        self.mutate('authorization', lambda v: v.update(generation_budget=1, new_prose_authorized=True))
        self.blocked('AUTHORIZATION_OR_BUDGET')

    def test_old_197_protection_cannot_be_released(self):
        self.mutate('authorization', lambda v: v.update(old_197_character_protection_released=True))
        self.blocked('AUTHORIZATION_OR_BUDGET')

    def test_missing_report_is_not_completion(self):
        (self.root / self.route['raw_report']['path']).unlink()
        self.blocked('MISSING_MATERIAL')

    def test_failed_model_run_is_not_completion(self):
        self.mutate('runtime', lambda v: v.update(turn_status='failed', report_received=False))
        self.blocked('NO_COMPLETE_ISOLATED')

    def test_actual_model_settings_cannot_be_replaced_by_prompt_claim(self):
        self.mutate('runtime', lambda v: v['resolved_thread_settings'].update(model='some-other-model'))
        self.blocked('ACTUAL_MODEL_OR_ISOLATION')

    def test_inherited_chat_is_not_independent(self):
        previous=self.read(self.project['r2_entry_short_trial']['writer_runtime']['path'])['thread_id']
        self.mutate('runtime', lambda v: v.update(thread_id=previous))
        self.blocked('INHERITED_PREVIOUS_CONTEXT')

    def test_tool_activity_rejects_report(self):
        self.mutate('runtime', lambda v: v.update(tool_activity_detected=['fileChange']))
        self.blocked('NO_COMPLETE_ISOLATED')

    def test_nonexistent_quote_is_not_usable_after_rehash(self):
        self.mutate('raw_report', lambda v: v['results'][0]['findings'][0].update(quote='原文不存在的情绪'))
        self.blocked('REPORT_OR_QUOTE_EVIDENCE')

    def test_report_with_replacement_prose_is_not_usable(self):
        self.mutate('raw_report', lambda v: v.update(replacement_sentence='替换正文'))
        self.blocked('REPORT_OR_QUOTE_EVIDENCE')

    def test_unsettled_report_is_not_completed_diagnosis(self):
        self.mutate('settlement', lambda v: v.update(finding_dispositions=[]))
        self.blocked('COORDINATOR_SETTLEMENT')

    def test_reading_window_cannot_be_claimed_as_real_human_stop(self):
        self.mutate('settlement', lambda v: v['reading_window_quote_checks'][0].update(interpretation='ACTUAL_HUMAN_STOP'))
        self.blocked('READING_WINDOW_QUOTE_OR_INFERENCE')

    def test_known_failure_diagnosis_cannot_be_called_blind_reading(self):
        self.mutate('settlement', lambda v: v.update(known_failure_diagnosis=False))
        self.blocked('COORDINATOR_SETTLEMENT')

    def test_invented_character_fact_is_not_learning(self):
        self.mutate('settlement', lambda v: v['finding_dispositions'][0]['fact_bindings'][0].update(value='他记得三年'))
        self.blocked('FACT_MISREAD_OR_INVENTED')

    def test_unread_course_index_cannot_be_claimed_as_evidence(self):
        self.mutate('settlement', lambda v: v['finding_dispositions'][0].update(source_ids=['S10']))
        self.blocked('UNREAD_SOURCE_NOT_EVIDENCE')

    def test_public_intro_is_not_whole_book_reading(self):
        self.mutate('sources', lambda v: v.update(full_book_read=True))
        self.blocked('SOURCE_READING_OR_TRANSFER_OVERCLAIM')

    def test_lecture_notes_are_not_full_video_watching(self):
        self.mutate('sources', lambda v: v.update(complete_video_watched=True))
        self.blocked('SOURCE_READING_OR_TRANSFER_OVERCLAIM')

    def test_prepared_capsule_excludes_failure_and_known_answers(self):
        self.mutate('craft_capsule', lambda v: v['craft_guidance'].append('刘先生395字FAIL，必须修F1'))
        self.blocked('WRITER_CAPSULE_ALLOWLIST')

    def test_old_writer_instruction_is_not_new_craft_guidance(self):
        self.mutate('craft_capsule', lambda v: v['craft_guidance'].__setitem__(0, '只返回正文，连续性项目'))
        self.blocked('WRITER_FAILURE_OR_ANSWER_LEAKAGE')

    def test_prepared_next_task_does_not_authorize_its_generation(self):
        self.mutate('next_task_proposal', lambda v: v.update(authorized_generation_budget=1, automatic_activation=True))
        self.blocked('NEXT_WRITER_NOT_AUTHORIZED')

    def test_learning_cannot_claim_human_quality_improvement(self):
        self.mutate('result', lambda v: v.update(writing_transfer='PROVEN', human_quality_result='PASS'))
        self.blocked('SCOPE_OR_QUALITY_PROMOTION')

    def test_live_entry_cannot_wait_for_feedback_already_received(self):
        p=self.root/'START_HERE.md'; p.write_text(p.read_text(encoding='utf-8').replace(gate.NEXT_ACTION,gate.OLD_ACTION),encoding='utf-8')
        self.blocked('ENTRYPOINT_STALE')


if __name__ == '__main__': unittest.main()
