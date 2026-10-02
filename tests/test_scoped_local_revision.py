"""Verify one scoped writer cannot expand scope or bypass input review."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scoped_current_state', REPO / 'scripts/verify_current_state.py')
current = importlib.util.module_from_spec(spec)
spec.loader.exec_module(current)


class ScopedLocalRevisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = json.loads((REPO / 'state/project_state.json').read_text())
        self.route = self.project['external_review_state']
        self.preparation = self.route['scoped_revision_preparation']
        self.execution = copy.deepcopy(self.route['scoped_revision_execution'])
        for key in ('task', 'lock', 'input_review'):
            path = self.execution[key]['path']
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((REPO / path).read_bytes())
        self.task = json.loads((REPO / self.execution['task']['path']).read_text())
        for key in ('writer_packet', 'approved_preparation', 'preparation_lock', 'previous_execution', 'previous_writer_result'):
            if key in self.task:
                path = self.task[key]['path']
                target = self.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((REPO / path).read_bytes())
        self.callback_id = json.loads((REPO / self.execution['input_review']['path']).read_text())['callback_id']
        artifact = self.project['mainline_state']['test_artifacts']['TEST_01']['path']
        self.original = (REPO / artifact).read_text()
        self.execution.update(status='CLAIMED_READY_TO_DISPATCH', writer_attempt_count=0,
            generation_count=0, used_prose_revision_rounds=self.task['prose_revision_round'] - 1, new_prose_authorized_now=True,
            next_action='EXECUTE_ONE_FRESH_CONTEXT_RC3_LOCAL_REVISION')

    def run_gate(self):
        return current.scoped_local_execution_action(self.root, self.project, self.route,
            self.preparation, self.execution, self.original)

    def test_clear_input_allows_one_scoped_run_only(self):
        self.assertEqual(self.run_gate(), 'EXECUTE_ONE_FRESH_CONTEXT_RC3_LOCAL_REVISION')
        self.assertFalse(self.project['mainline_state']['full_v5_authorized'])
        self.assertFalse(self.execution['literary_acceptance'])

    def test_consumed_dispatch_cannot_return_to_claimed(self):
        self.execution['writer_attempt_count'] = 1
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_COUNT_DRIFT'):
            self.run_gate()

    def test_preparation_callback_must_be_processed_once(self):
        self.route['processed_preparation_callback_ids'].append(self.callback_id)
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_PROVENANCE_DRIFT'):
            self.run_gate()

    def test_writer_input_cannot_be_changed(self):
        self.execution['writer_packet'] = dict(self.execution['writer_packet'], blob='wrong')
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_PROVENANCE_DRIFT'):
            self.run_gate()

    def test_input_clearance_cannot_claim_literary_acceptance(self):
        self.execution['literary_acceptance'] = True
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_SCOPE_PROMOTION'):
            self.run_gate()

    def test_input_review_bytes_cannot_be_changed(self):
        path = self.root / self.execution['input_review']['path']
        path.write_bytes(path.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'EXTERNAL_REVIEW_IDENTITY_DRIFT'):
            self.run_gate()

    def test_last_round_requires_retained_first_failure(self):
        if self.task['prose_revision_round'] != 2:
            self.skipTest('Only relevant to the last bounded round')
        self.route['scoped_revision_execution_history'] = []
        with self.assertRaisesRegex(ValueError, 'SCOPED_LAST_ROUND_WITHOUT_BOUND_PARENT_FAILURE'):
            self.run_gate()

    def test_last_round_cannot_reset_consumed_round_count(self):
        if self.task['prose_revision_round'] != 2:
            self.skipTest('Only relevant to the last bounded round')
        self.execution['used_prose_revision_rounds'] = 0
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_COUNT_DRIFT'):
            self.run_gate()

    def set_frozen_test_output(self, text):
        path = self.task['output_path']
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        data = target.read_bytes()
        self.execution.update(status='FROZEN_AWAITING_REVIEW_DISPATCH', writer_attempt_count=1,
            generation_count=1, used_prose_revision_rounds=self.task['prose_revision_round'],
            new_prose_authorized_now=False, next_action='SEND_ONE_FROZEN_RC3_LOCAL_REVISION_FOR_EXTERNAL_REVIEW',
            output={'path': path, 'blob': current.git_blob(data), 'sha256': hashlib.sha256(data).hexdigest()})

    def test_scope_valid_output_only_opens_review(self):
        self.set_frozen_test_output(self.original[:197] + '检查用占位文字，非小说正文。' * 10)
        self.assertEqual(self.run_gate(), 'SEND_ONE_FROZEN_RC3_LOCAL_REVISION_FOR_EXTERNAL_REVIEW')
        self.assertFalse(self.execution['literary_acceptance'])

    def test_modified_opening_is_rejected_even_with_new_hash(self):
        self.set_frozen_test_output('改' + self.original[1:197] + '检查用占位文字，非小说正文。' * 10)
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_OUTPUT_DRIFT'):
            self.run_gate()

    def test_overlong_output_is_rejected_even_with_new_hash(self):
        self.set_frozen_test_output(self.original[:197] + '检查用占位文字，非小说正文。' * 30)
        with self.assertRaisesRegex(ValueError, 'SCOPED_LOCAL_EXECUTION_OUTPUT_DRIFT'):
            self.run_gate()


if __name__ == '__main__':
    unittest.main()
