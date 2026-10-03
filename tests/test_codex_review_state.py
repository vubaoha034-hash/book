"""Corrupt the completed integration without calling a model or writing prose."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('codex_route', REPO / 'scripts/verify_codex_review.py')
route_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route_check)


class CompletedReviewStateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project = json.loads((REPO / 'state/project_state.json').read_text(encoding='utf-8'))
        self.checkpoint = json.loads((REPO / 'state/continuity/LATEST_CHECKPOINT.json').read_text(encoding='utf-8'))
        self.route = self.project['codex_review_integration']
        self.copied = set()
        self.copy('START_HERE.md')
        self.copy('scripts/codex_review.py')
        self.copy_refs(self.route)

    def copy(self, relative):
        if relative in self.copied:
            return
        source = REPO / relative
        if not source.is_file():
            return
        self.copied.add(relative)
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        if source.suffix == '.json':
            self.copy_refs(self.read(relative))

    def copy_refs(self, value):
        if isinstance(value, dict):
            if isinstance(value.get('path'), str):
                self.copy(value['path'])
            for child in value.values():
                self.copy_refs(child)
        elif isinstance(value, list):
            for child in value:
                self.copy_refs(child)

    def read(self, relative):
        return json.loads((self.root / relative).read_text(encoding='utf-8'))

    def write_bound(self, reference, value):
        data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        (self.root / reference['path']).write_bytes(data)
        reference.update(blob=route_check.blob(data), sha256=hashlib.sha256(data).hexdigest())

    def settle_result_ref(self, receipt):
        self.write_bound(self.route['result'], receipt)
        self.checkpoint['codex_review_integration'] = copy.deepcopy(self.route)

    def verify(self, historical=None):
        return route_check.codex_review_action(self.root, self.project, self.checkpoint,
            route_check.OLD_ACTION if historical is None else historical)

    def expect_block(self, message):
        with self.assertRaisesRegex(ValueError, message):
            self.verify()

    def test_complete_state_has_one_next_step_and_no_quality_claim(self):
        self.assertEqual(self.verify(), route_check.NEXT_ACTION)
        self.assertFalse(self.route['standalone_quality_gate_allowed'])
        self.assertFalse(self.route['new_prose_authorized_now'])

    def test_historical_gate_cannot_be_skipped(self):
        with self.assertRaisesRegex(ValueError, 'CANNOT_SKIP_HISTORICAL_GATES'):
            self.verify('GENERATE_FULL_V5')

    def test_state_checkpoint_drift_blocks(self):
        self.checkpoint['codex_review_integration']['next_action'] = 'WRITE_NOW'
        self.expect_block('STATE_DRIFT')

    def test_exhausted_rounds_cannot_be_replenished(self):
        receipt = self.read(self.route['result']['path'])
        receipt['old_RC3_remaining_rounds'] = 1
        self.settle_result_ref(receipt)
        self.expect_block('AUTHORITY_OR_SCOPE_PROMOTION')

    def test_old_protection_cannot_be_released(self):
        receipt = self.read(self.route['result']['path'])
        receipt['old_197_character_protection_released'] = True
        self.settle_result_ref(receipt)
        self.expect_block('AUTHORITY_OR_SCOPE_PROMOTION')

    def test_ai_praise_cannot_overturn_human_failure(self):
        receipt = self.read(self.route['result']['path'])
        receipt['human_emotion_retention'] = 'PASS'
        self.settle_result_ref(receipt)
        self.expect_block('AUTHORITY_OR_SCOPE_PROMOTION')

    def test_no_report_is_not_completion(self):
        receipt = self.read(self.route['result']['path'])
        (self.root / receipt['jobs']['diagnosis']['raw_report']['path']).unlink()
        self.expect_block('MISSING_MATERIAL')

    def test_wrong_target_is_blocked_after_receipt_rehash(self):
        receipt = self.read(self.route['result']['path'])
        receipt['target']['blob'] = '0' * 40
        self.settle_result_ref(receipt)
        self.expect_block('WRONG_CURRENT_TARGET_OR_MANIFEST')

    def test_runtime_failure_cannot_be_counted_as_returned_report(self):
        receipt = self.read(self.route['result']['path'])
        runtime_ref = receipt['jobs']['diagnosis']['runtime']
        runtime = self.read(runtime_ref['path'])
        runtime.update(status='BLOCKED', report_received=False)
        self.write_bound(runtime_ref, runtime)
        self.settle_result_ref(receipt)
        self.expect_block('INDEPENDENCE_OR_RUNTIME_NOT_PROVEN')

    def test_model_name_in_report_does_not_prove_runtime(self):
        receipt = self.read(self.route['result']['path'])
        runtime_ref = receipt['jobs']['facts']['runtime']
        runtime = self.read(runtime_ref['path'])
        runtime['resolved_thread_settings']['reasoningEffort'] = 'low'
        self.write_bound(runtime_ref, runtime)
        self.settle_result_ref(receipt)
        self.expect_block('INDEPENDENCE_OR_RUNTIME_NOT_PROVEN')

    def test_missing_manual_fact_and_scope_settlement_blocks(self):
        receipt = self.read(self.route['result']['path'])
        settlement_ref = receipt['coordinator_settlement']
        settlement = self.read(settlement_ref['path'])
        settlement['facts_and_scope_checked'] = False
        self.write_bound(settlement_ref, settlement)
        self.settle_result_ref(receipt)
        self.expect_block('COORDINATOR_SETTLEMENT_MISSING')

    def test_stale_live_entry_blocks(self):
        (self.root / 'START_HERE.md').write_text('Historical entry only', encoding='utf-8')
        self.expect_block('ENTRYPOINT_STALE')


if __name__ == '__main__':
    unittest.main()
