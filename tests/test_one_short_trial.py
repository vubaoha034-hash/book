"""Corrupt actual isolated-run evidence in temporary copies; never call models."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('short_trial_gate', REPO / 'scripts/verify_one_short_trial.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class OneShortTrialTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project = json.loads((REPO / 'state/project_state.json').read_bytes())
        self.checkpoint = json.loads((REPO / 'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route = self.project['r2_entry_short_trial']
        # Test the immutable checkpoint196 stage in isolation from later tasks.
        for value in (self.project, self.checkpoint):
            value.pop('emotion_pacing_learning', None)
            value.pop('two_role_opening_review', None)
            value.update(last_completed_task_id=gate.TASK,
                last_completed_task_contract=self.route['task']['path'],
                next_action=gate.NEXT_ACTION, next_required_action=gate.NEXT_ACTION)
        self.checkpoint.update(sequence=196, stop=True)
        self.seen = set()
        self.copy('START_HERE.md')
        entry = self.root / 'START_HERE.md'
        entry.write_text('当前位置：检查点196。\n' + entry.read_text(encoding='utf-8'), encoding='utf-8')
        self.copy_refs(self.route)
        for p in ('state/authoring/r2-entry-trial-20261003/writer.attempt.json',
                  'state/reviews/r2-entry-trial-20261003/facts.attempt.json'):
            self.copy(p)

    def copy(self, path):
        if path in self.seen or not (REPO / path).is_file():
            return
        self.seen.add(path)
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((REPO / path).read_bytes())
        if path.endswith('.json'):
            self.copy_refs(json.loads(dest.read_bytes()))

    def copy_refs(self, value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')):
                self.copy(value['path'])
            for child in value.values():
                self.copy_refs(child)
        elif isinstance(value, list):
            for child in value:
                self.copy_refs(child)

    def read(self, path):
        return json.loads((self.root / path).read_bytes())

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def refresh(self, value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')):
                path = self.root / value['path']
                if path.is_file():
                    data = path.read_bytes()
                    value.update(blob=gate.blob(data), sha256=hashlib.sha256(data).hexdigest())
            for child in value.values():
                self.refresh(child)
        elif isinstance(value, list):
            for child in value:
                self.refresh(child)

    def rebind(self):
        # A bad claim remains blocked even when the coordinator rehashes it.
        # References form a DAG: packets/runtimes/evidence/settlement, result,
        # task, then the mirrored live route. Historical files stay untouched.
        order = ('manifest', 'writer_runtime', 'facts_runtime', 'facts_evidence',
                 'coordinator_settlement', 'result', 'task')
        for key in order:
            path = self.route[key]['path']
            value = self.read(path)
            self.refresh(value)
            self.write(path, value)
        self.refresh(self.route)
        self.checkpoint['r2_entry_short_trial'] = copy.deepcopy(self.route)

    def mutate(self, key, callback):
        path = self.route[key]['path']
        value = self.read(path)
        callback(value)
        self.write(path, value)
        self.rebind()

    def verify(self, action=None):
        return gate.one_short_trial_action(self.root, self.project, self.checkpoint,
            gate.OLD_ACTION if action is None else action)

    def blocked(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            self.verify()

    def test_completed_trial_is_unknown_and_budget_spent(self):
        self.assertEqual(self.verify(), gate.NEXT_ACTION)
        self.assertEqual(self.route['human_quality_result'], 'UNKNOWN')
        self.assertEqual(self.route['remaining_new_generation_budget'], 0)

    def test_cannot_skip_historical_failure_and_preparation(self):
        with self.assertRaisesRegex(ValueError, 'CANNOT_SKIP_HISTORICAL_GATES'):
            self.verify('WRITE_MORE')

    def test_unbound_user_authority_is_not_writing_permission(self):
        self.mutate('authorization', lambda v: v['authority'].update(source='MODEL_ASSUMPTION'))
        self.blocked('USER_AUTHORIZATION_OR_PROPOSAL_DRIFT')

    def test_old_budget_cannot_be_restored(self):
        self.mutate('authorization', lambda v: v.update(old_RC3_remaining_rounds=1))
        self.blocked('OLD_BUDGET_OR_SCOPE_PROMOTION')

    def test_new_opening_permission_does_not_release_old_lock(self):
        self.mutate('authorization', lambda v: v.update(old_197_character_protection_released=True))
        self.blocked('OLD_BUDGET_OR_SCOPE_PROMOTION')

    def test_second_generation_is_not_authorized(self):
        self.mutate('result', lambda v: v.update(generation_count=2))
        self.blocked('BUDGET_SCOPE_OR_HUMAN_PROMOTION')

    def test_fact_clear_cannot_be_human_pass(self):
        self.mutate('result', lambda v: v.update(human_quality_result='PASS'))
        self.blocked('BUDGET_SCOPE_OR_HUMAN_PROMOTION')

    def test_exact_human_stop_cannot_be_invented(self):
        self.mutate('result', lambda v: v.update(human_exact_stop='line 3'))
        self.blocked('EVIDENCE_COUNT_UNKNOWN_OR_HUMAN_DRIFT')

    def test_unsettled_finding_is_not_fact_completion(self):
        self.mutate('coordinator_settlement', lambda v: v['report_finding_dispositions'][0].update(scope_checked=False))
        self.blocked('REPORT_FINDING_NOT_SETTLED')

    def test_body_cannot_be_rewritten_even_after_rehash(self):
        path = self.root / self.route['artifact']['path']
        path.write_bytes(path.read_bytes() + '补写'.encode())
        self.rebind()
        self.blocked('FROZEN_BODY_OR_LENGTH_DRIFT')

    def test_missing_raw_report_is_not_pass(self):
        (self.root / self.route['facts_raw_report']['path']).unlink()
        self.blocked('MISSING_MATERIAL')

    def test_runtime_failure_is_not_pass(self):
        self.mutate('facts_runtime', lambda v: v.update(report_received=False))
        self.blocked('NO_COMPLETE_ISOLATED_RUNTIME')

    def test_model_name_in_prompt_does_not_replace_actual_setting(self):
        self.mutate('facts_runtime', lambda v: v['resolved_thread_settings'].update(model='another-model'))
        self.blocked('ACTUAL_MODEL_OR_ISOLATION_DRIFT')

    def test_same_thread_is_not_independent_review(self):
        writer_id = self.read(self.route['writer_runtime']['path'])['thread_id']
        self.mutate('facts_runtime', lambda v: v.update(thread_id=writer_id))
        self.blocked('REVIEW_INHERITED_WRITER_CONTEXT')

    def test_undeclared_tool_activity_blocks(self):
        self.mutate('writer_runtime', lambda v: v.update(tool_activity_detected=['shell']))
        self.blocked('NO_COMPLETE_ISOLATED_RUNTIME')

    def test_diagnosis_cannot_be_added_to_writer_input(self):
        self.mutate('writer_input', lambda v: v.update(diagnosis='已知失败'))
        self.blocked('WRITER_INPUT_CONTEXT_ALLOWLIST')

    def test_wrong_fact_sample_is_not_review_of_this_body(self):
        self.mutate('facts_packet', lambda v: v['samples'][0].update(original_sha256='0' * 64))
        self.blocked('SUBMITTED_PACKET_DRIFT|FACT_PACKET_SCOPE_OR_IDENTITY_DRIFT')

    def test_nonexistent_report_quote_cannot_be_rehashed_into_evidence(self):
        self.mutate('facts_raw_report', lambda v: v['results'][0]['findings'][0].update(quote='不存在的引文'))
        self.blocked('REPORT_OR_QUOTE_AUDIT_REJECTED')

    def test_nonexistent_coordinator_quote_blocks(self):
        self.mutate('coordinator_settlement', lambda v: v['text_fact_checks'][0].update(quote='不存在的引文'))
        self.blocked('SETTLEMENT_QUOTE_OR_SCOPE_MISSING')

    def test_fact_copy_and_unknown_assets_cannot_be_invented(self):
        self.mutate('coordinator_settlement', lambda v: v['text_fact_checks'][0]['fact_bindings'][0].update(value='新编生活史'))
        self.blocked('SETTLEMENT_FACT_COPY_DRIFT')

    def test_live_entry_cannot_point_back_to_consumed_generation(self):
        (self.root / 'START_HERE.md').write_bytes(b'WRITE_NEW_SHORT_NOW\n')
        self.blocked('ENTRYPOINT_STALE')


if __name__ == '__main__':
    unittest.main()
