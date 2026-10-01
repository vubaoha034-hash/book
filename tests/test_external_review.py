"""Test authority, evidence binding and reviewer calibration; not prose quality."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('external_current_state', REPO / 'scripts/verify_current_state.py')
current = importlib.util.module_from_spec(spec)
spec.loader.exec_module(current)


class ExternalReviewBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        project = json.loads((REPO / 'state/project_state.json').read_text(encoding='utf-8'))
        self.project = copy.deepcopy(project)
        self.cp = {'external_review_state': copy.deepcopy(project['external_review_state'])}
        self.receipt_path = project['external_review_state']['receipt']['path']
        self.receipt = json.loads((REPO / self.receipt_path).read_text(encoding='utf-8'))
        lock = json.loads((REPO / current.EXTERNAL_REVIEW_LOCK_PATH).read_text(encoding='utf-8'))
        names = {current.EXTERNAL_REVIEW_LOCK_PATH, self.receipt_path,
                 lock['task']['path'], lock['protocol']['path'],
                 self.receipt['mainline_binding']['artifact']['path']}
        names.update(ref['path'] for ref in self.receipt['reports'].values())
        names.update(row['artifact']['path'] for row in self.receipt['blind_samples'])
        for row in self.receipt['calibration']['initial']['known_negatives']:
            ref = row['human_receipt']
            names.add(ref['path'])
            names.add(json.loads((REPO / ref['path']).read_text(encoding='utf-8'))['artifact']['path'])
        retest = self.receipt['calibration']['unseen_retest']
        names.update(retest[key]['path'] for key in ('source_artifact', 'excerpt', 'human_receipt'))
        for name in names:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((REPO / name).read_bytes())
        self.frozen = project['mainline_state']['test_artifacts']
        self.outcomes = {'TEST_01': 'UNKNOWN'}
        self.base_action = 'AWAIT_ACTUAL_HUMAN_READING_OF_TEST_01'

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def ref(self, name):
        data = (self.root / name).read_bytes()
        return {'path': name, 'blob': current.git_blob(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def bind_receipt(self):
        self.write(self.receipt_path, self.receipt)
        self.project['external_review_state']['receipt'] = self.ref(self.receipt_path)
        self.cp['external_review_state'] = copy.deepcopy(self.project['external_review_state'])

    def change_report(self, key, fn):
        path = self.receipt['reports'][key]['path']
        data = json.loads((self.root / path).read_text(encoding='utf-8'))
        fn(data)
        self.write(path, data)
        self.receipt['reports'][key] = self.ref(path)
        self.bind_receipt()

    def run_gate(self):
        return current.external_review_action(self.root, self.project, self.cp,
            'TEST_01', self.outcomes, self.frozen, self.base_action)

    def expect_block(self, reason):
        with self.assertRaisesRegex(ValueError, reason):
            self.run_gate()

    def test_actual_roundtrip_only_authorizes_scoped_preparation(self):
        self.assertEqual(self.run_gate(), 'DEFINE_ONE_SCOPED_METHOD_REVISION_FROM_EXTERNAL_REVIEW')
        self.assertEqual(self.receipt['human_quality_result'], 'UNKNOWN')
        self.assertFalse(self.project['mainline_state']['new_prose_authorized_now'])
        self.assertFalse(self.receipt['standalone_quality_gate_allowed'])

    def test_external_report_cannot_claim_human_source(self):
        self.receipt['source']['actual_human'] = True
        self.bind_receipt()
        self.expect_block('EXTERNAL_REVIEW_SCOPE_PROMOTION')

    def test_failed_calibration_cannot_be_inflated(self):
        self.receipt['calibration']['initial']['hits'] = 2
        self.bind_receipt()
        self.expect_block('EXTERNAL_REVIEW_CALIBRATION_DRIFT')

    def test_unseen_retest_miss_cannot_be_recorded_as_detection(self):
        self.receipt['calibration']['unseen_retest']['hits'] = 1
        self.bind_receipt()
        self.expect_block('EXTERNAL_REVIEW_CALIBRATION_DRIFT')

    def test_same_context_retest_cannot_be_called_a_fresh_reader(self):
        self.change_report('C', lambda data: data.update(review_context='FRESH_EXTERNAL_CHAT_FIRST_READ'))
        self.expect_block('EXTERNAL_REVIEW_INDEPENDENCE_MISREPRESENTED')

    def test_invented_priority_quote_is_rejected_even_after_rehashing(self):
        invented = 'This quoted sentence does not exist in the frozen novel.'
        self.receipt['priority_issue']['quote'] = invented
        self.change_report('D', lambda data: data['priority_issue'].update(quote=invented))
        self.expect_block('EXTERNAL_REVIEW_UNLOCATED_DIAGNOSIS')

    def test_rating_permission_cannot_be_restored_in_report(self):
        self.change_report('D', lambda data: data.update(automatic_literary_quality_certification=True))
        self.expect_block('EXTERNAL_REVIEW_SCOPE_PROMOTION')

    def test_wrong_human_negative_artifact_is_rejected(self):
        negatives = self.receipt['calibration']['initial']['known_negatives']
        negatives[0]['human_receipt'] = negatives[1]['human_receipt']
        self.bind_receipt()
        self.expect_block('EXTERNAL_REVIEW_CALIBRATION_NOT_HUMAN_BOUND')

    def test_modified_source_excerpt_is_rejected(self):
        path = self.root / self.receipt['calibration']['unseen_retest']['excerpt']['path']
        path.write_text(path.read_text(encoding='utf-8') + 'extra', encoding='utf-8')
        self.expect_block('EXTERNAL_REVIEW_RETEST_SOURCE_DRIFT')

    def test_project_chat_cannot_replace_outside_project_chat(self):
        self.receipt['source']['conversation_url'] = 'https://chatgpt.com/g/g-p-example/c/example'
        self.bind_receipt()
        self.expect_block('EXTERNAL_REVIEW_SCOPE_PROMOTION')

    def test_unconfirmed_send_cannot_be_counted_as_success(self):
        self.receipt['dispatch_proofs'][3]['verdict'] = 'DISPATCH_UNCONFIRMED'
        self.bind_receipt()
        self.expect_block('EXTERNAL_REVIEW_DISPATCH_UNCONFIRMED')

    def test_receipt_hash_drift_is_rejected(self):
        with (self.root / self.receipt_path).open('a', encoding='utf-8') as f:
            f.write(' ')
        self.expect_block('EXTERNAL_REVIEW_IDENTITY_DRIFT')

    def test_checkpoint_route_must_match_current_state(self):
        self.cp['external_review_state']['next_action'] = 'GENERATE_FULL_MANUSCRIPT'
        self.expect_block('EXTERNAL_REVIEW_STATE_DRIFT')

    def test_user_rejection_has_priority_over_external_route(self):
        self.outcomes['TEST_01'] = 'FAIL'
        self.base_action = 'DEFINE_ONE_SCOPED_METHOD_REVISION_AFTER_TEST_01_FAILURE'
        self.receipt['next_action'] = self.base_action
        self.project['external_review_state']['next_action'] = self.base_action
        self.bind_receipt()
        self.assertEqual(self.run_gate(), self.base_action)

    def test_model_praise_cannot_release_prose_after_failed_calibration(self):
        self.receipt['editorial_verdict'] = 'EXTERNAL_PASS_PROVISIONAL'
        next_action = 'REPAIR_EXTERNAL_REVIEW_BEFORE_PROSE_RELEASE'
        self.receipt['next_action'] = next_action
        self.project['external_review_state']['next_action'] = next_action
        self.change_report('B', lambda data: data.update(current_editorial_verdict='EXTERNAL_PASS_PROVISIONAL'))
        self.assertEqual(self.run_gate(), next_action)
        self.assertFalse(self.receipt['standalone_quality_gate_allowed'])
        self.assertFalse(self.project['external_review_state']['new_prose_authorized'])

    def test_existing_route_lock_cannot_be_replaced(self):
        path = self.root / current.EXTERNAL_REVIEW_LOCK_PATH
        with path.open('a', encoding='utf-8') as f:
            f.write(' ')
        self.expect_block('EXTERNAL_REVIEW_LOCK_CHANGED')


if __name__ == '__main__':
    unittest.main()
