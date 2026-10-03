"""Authorization and evidence corruption tests; no model calls or fiction."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reentry_gate', REPO / 'scripts/verify_reentry_preparation.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ReentryPreparationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project = json.loads((REPO / 'state/project_state.json').read_text(encoding='utf-8'))
        self.checkpoint = json.loads((REPO / 'state/continuity/LATEST_CHECKPOINT.json').read_text(encoding='utf-8'))
        self.route = self.project['r2_reentry_fact_preparation']
        self.seen = set()
        self.copy('START_HERE.md')
        self.copy_refs(self.route)

    def copy(self, relative):
        if relative in self.seen or not (REPO / relative).is_file():
            return
        self.seen.add(relative)
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / relative).read_bytes())
        if relative.endswith('.json') and ('r2-reentry-facts-' in relative or 'NOVEL_R2_REENTRY_' in relative):
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

    def read(self, path):
        return json.loads((self.root / path).read_text(encoding='utf-8'))

    def write(self, path, value):
        (self.root / path).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        data = (self.root / path).read_bytes()
        return {'path': path, 'blob': gate.blob(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def rebind(self):
        # Simulate a coordinator rehashing a bad claim. Hashes alone must not
        # turn permission, invented facts, or nonexistent quotes into evidence.
        for key in ('authorization', 'writer_context'):
            path = self.route[key]['path']
            self.route[key] = self.write(path, self.read(path))
        for key in ('evidence', 'next_task_proposal', 'result', 'task'):
            path = self.route[key]['path']
            value = self.read(path)
            value['writer_context'] = copy.deepcopy(self.route['writer_context'])
            if key == 'next_task_proposal':
                value['preparation_evidence'] = copy.deepcopy(self.route['evidence'])
            if key in ('result', 'task'):
                for ref_key in ('authorization', 'evidence', 'next_task_proposal'):
                    value[ref_key] = copy.deepcopy(self.route[ref_key])
            if key == 'task':
                value['result'] = copy.deepcopy(self.route['result'])
            self.route[key] = self.write(path, value)
        self.checkpoint['r2_reentry_fact_preparation'] = copy.deepcopy(self.route)

    def mutate(self, key, callback):
        path = self.route[key]['path']
        value = self.read(path)
        callback(value)
        self.write(path, value)
        self.rebind()

    def verify(self, action=None):
        return gate.reentry_preparation_action(self.root, self.project, self.checkpoint,
            gate.OLD_ACTION if action is None else action)

    def blocked(self, expected):
        with self.assertRaisesRegex(ValueError, expected):
            self.verify()

    def test_saved_preparation_has_no_prose_authorization(self):
        self.assertEqual(self.verify(), gate.NEXT_ACTION)
        self.assertEqual(self.route['generation_budget'], 0)

    def test_preparation_cannot_skip_previous_human_and_review_gates(self):
        with self.assertRaisesRegex(ValueError, 'CANNOT_SKIP_HISTORICAL_GATES'):
            self.verify('WRITE_NOW')

    def test_checkpoint_mirror_drift_blocks(self):
        self.checkpoint['r2_reentry_fact_preparation']['generation_budget'] = 1
        self.blocked('STATE_DRIFT')

    def test_preparation_reply_does_not_authorize_prose(self):
        self.mutate('authorization', lambda v: v.update(new_prose_authorized=True, generation_budget=1))
        self.blocked('SCOPE_OR_BUDGET_PROMOTION')

    def test_old_rounds_cannot_be_refilled(self):
        self.mutate('result', lambda v: v.update(old_RC3_remaining_rounds=1))
        self.blocked('SCOPE_OR_BUDGET_PROMOTION')

    def test_old_protection_cannot_be_released(self):
        self.mutate('evidence', lambda v: v['protected_old_prefix'].update(released_now=True))
        self.blocked('OLD_PROTECTION_CHANGED')

    def test_nonexistent_quote_blocks_even_after_rehash(self):
        self.mutate('evidence', lambda v: v['located_evidence'][0].update(quote='这句话不存在于原稿。'))
        self.blocked('UNLOCATED_QUOTE')

    def test_missing_fact_projection_is_not_completion(self):
        (self.root / self.route['writer_context']['path']).unlink()
        self.blocked('MISSING_MATERIAL')

    def test_old_writing_command_cannot_enter_future_writer_context(self):
        self.mutate('writer_context', lambda v: v.update(historical_command='只返回正文'))
        self.blocked('WRITER_DIAGNOSIS_OR_COMMAND_LEAKAGE')

    def test_later_truth_cannot_enter_future_writer_context(self):
        self.mutate('writer_context', lambda v: v.update(later_truth='连续性项目造成两套过去。'))
        self.blocked('WRITER_DIAGNOSIS_OR_COMMAND_LEAKAGE')

    def test_new_life_detail_cannot_enter_frozen_context_after_rehash(self):
        self.mutate('writer_context', lambda v: v.update(new_life_fact='搬家司机正在等他。'))
        self.blocked('FROZEN_CONTEXT_CHANGED')

    def test_human_failure_cannot_be_promoted(self):
        self.mutate('result', lambda v: v.update(human_emotion_retention='PASS'))
        self.blocked('COMPLETION_OR_QUALITY_PROMOTION')

    def test_proposal_cannot_activate_itself(self):
        self.mutate('next_task_proposal', lambda v: v.update(status='AUTHORIZED', authorized_generation_budget=1))
        self.blocked('NEXT_WRITER_NOT_AUTHORIZED')

    def test_stale_live_entry_blocks(self):
        (self.root / 'START_HERE.md').write_bytes(b'Old entry only\n')
        self.blocked('ENTRYPOINT_STALE')


if __name__ == '__main__':
    unittest.main()
