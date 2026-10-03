"""Exercise real state corruption and feedback boundaries, never prose quality."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('current_state', REPO / 'scripts/verify_current_state.py')
current = importlib.util.module_from_spec(spec)
spec.loader.exec_module(current)


class CurrentStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('state/project_state.json', 'state/continuity/LATEST_CHECKPOINT.json'):
            self.copy(name)
        project = self.read('state/project_state.json')
        mainline = project['mainline_state']
        self.task_id, self.revision = mainline['task_id'], mainline['revision']
        for name in (current.RECEIPT, project['phase422_state']['opening_trial']['path'],
                     project['human_verdict_receipt'], project['latest_human_review']['bound_artifact_path'],
                     mainline['contract']['path'], mainline['plan']['path']):
            self.copy(name)
        for ref in mainline['lock_chain']:
            self.copy(ref['path'])
            basis = self.read(ref['path']).get('basis', {})
            if basis.get('type') == 'RECORDED_FROZEN_TEST_FAILURE':
                self.copy(basis['evidence_path'])
                self.copy(self.read(basis['evidence_path'])['artifact']['path'])
        self.plan_path = mainline['plan']['path']
        self.contract_path = mainline['contract']['path']
        self.previous_lock_blob = mainline['lock_chain'][-1]['blob']
        self.steps = self.read(self.contract_path)['execution_order']
        # Use a fresh STEP_01 fixture of the current locked method. The real
        # project may legitimately advance; CI must not freeze its live cursor.
        def fresh_fixture(state):
            # The baseline fixtures test the human mainline route. External
            # review is exercised separately against its real frozen protocol.
            state.pop('external_review_state', None)
            # Codex integration has its own corruption tests. These synthetic
            # STEP_01 fixtures intentionally exercise only the locked mainline.
            state.pop('codex_review_integration', None)
            # The later preparation authorization has separate corruption tests.
            state.pop('r2_reentry_fact_preparation', None)
            state.pop('r2_entry_short_trial', None)
            state.pop('emotion_pacing_learning', None)
            state.pop('two_role_opening_review', None)
            state.pop('autonomous_opening_to_human', None)
            state.pop('opening_prose_repair', None)
            state.pop('opening_hook_trial', None)
            state.pop('hook_trial_human_feedback', None)
            state.pop('continuation_short_trial', None)
            state['mainline_state'].update(current_step='STEP_01', completed_steps=[],
                test_artifacts={}, test_results={}, literary_quality_validated=False,
                new_prose_authorized_now=False, full_v5_authorized=False)
            state['next_action'] = state['next_required_action'] = self.steps[0]['action']
        self.mutate_state(fresh_fixture)

    def copy(self, name):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((REPO / name).read_bytes())

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding='utf-8'))

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def mutate_state(self, fn):
        for name in ('state/project_state.json', 'state/continuity/LATEST_CHECKPOINT.json'):
            value = self.read(name)
            fn(value)
            self.write(name, value)
        cp = self.read('state/continuity/LATEST_CHECKPOINT.json')
        cp['action_guard']['project_state_sha256'] = hashlib.sha256((self.root / 'state/project_state.json').read_bytes()).hexdigest()
        self.write('state/continuity/LATEST_CHECKPOINT.json', cp)

    def expect_block(self, reason):
        with self.assertRaisesRegex(ValueError, reason):
            current.verify(self.root)

    def test_saved_mainline_is_consistent_without_claiming_quality(self):
        result = current.verify(self.root)
        self.assertEqual(result['mainline']['step'], 'STEP_01')
        self.assertFalse(result['new_prose_authorized'])
        self.assertFalse(result['literary_quality_tested_by_this_script'])

    def test_unreviewed_mainline_edit_is_blocked(self):
        with (self.root / self.plan_path).open('a', encoding='utf-8') as f:
            f.write('\nChange route immediately.\n')
        self.expect_block('LOCKED_MAINLINE_CONTENT_CHANGED')

    def test_rewriting_initial_lock_and_its_pointer_is_blocked(self):
        lock = self.read(current.ROOT_LOCK_PATH)
        lock['basis']['source'] = 'MODEL_CHANGED_ITS_MIND'
        self.write(current.ROOT_LOCK_PATH, lock)
        digest = current.git_blob((self.root / current.ROOT_LOCK_PATH).read_bytes())
        self.mutate_state(lambda state: state['mainline_state']['lock_chain'][0].update(blob=digest))
        self.expect_block('INITIAL_LOCK_REWRITTEN')

    def test_stale_phase426_route_is_blocked(self):
        self.mutate_state(lambda state: state.update(next_action='OPEN_ONE_SEPARATE_CLEAN_WRITER_RENDER_FOR_FROZEN_PHASE426_TRACE'))
        self.expect_block('STALE_MAINLINE_NEXT_ACTION')

    def test_skipping_preparation_is_blocked(self):
        def change(state):
            state['mainline_state'].update(current_step='STEP_03', new_prose_authorized_now=True)
            state['next_action'] = state['next_required_action'] = self.steps[2]['action']
        self.mutate_state(change)
        self.expect_block('MAINLINE_STEP_SKIPPED')

    def test_test02_without_test01_human_pass_is_blocked(self):
        def change(state):
            state['mainline_state'].update(current_step='STEP_04', completed_steps=['STEP_01','STEP_02','STEP_03'], new_prose_authorized_now=True)
            state['next_action'] = state['next_required_action'] = self.steps[3]['action']
        self.mutate_state(change)
        self.expect_block('TEST_02_WITHOUT_TEST_01_PASS')

    def test_mismatched_feedback_version_is_blocked(self):
        self.mutate_state(lambda state: state['latest_human_review'].update(bound_blob='0' * 40))
        self.expect_block('current_feedback_mirror.*current_feedback_artifact')

    def test_stale_checkpoint_hash_is_blocked(self):
        project = self.read('state/project_state.json')
        project['updated_at'] = 'changed-without-checkpoint'
        self.write('state/project_state.json', project)
        self.expect_block('project_hash')

    def test_historical_opening_rejection_cannot_be_promoted(self):
        self.mutate_state(lambda state: state['phase422_state'].update(final_pass=True))
        self.expect_block('preserve_final_pass')

    def test_full_v5_cannot_be_automatically_enabled(self):
        self.mutate_state(lambda state: state['mainline_state'].update(full_v5_authorized=True))
        self.expect_block('AUTOMATIC_FULL_V5_PROMOTION')

    def make_test_receipt(self, human, outcome='UNKNOWN', facts=None):
        artifact = 'delivery/test-fixture.txt'
        path = self.root / artifact
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Synthetic test artifact; not fiction or a real verdict.\n', encoding='utf-8')
        receipt = 'state/review_receipts/test-fixture.json'
        self.write(receipt, {
            'schema_version':'novel-mainline-test/v1','project_id':'novel-distillation',
            'task_id':self.task_id,'method_revision':self.revision,'test_id':'TEST_01',
            'artifact':{'path':artifact,'blob':current.git_blob(path.read_bytes())},
            'human_feedback':human,'fact_check':facts or {'verdict':'CLEAR'},'outcome':outcome,
            'validation_scope':self.read(self.contract_path)['tests']['TEST_01'].get('validation_scope'),
        })
        return receipt

    def test_no_feedback_stays_unknown(self):
        receipt = self.make_test_receipt({})
        self.assertEqual(current.test_outcome(self.root, receipt), 'UNKNOWN')

    def test_model_high_score_cannot_be_human_pass(self):
        receipt = self.make_test_receipt({'source':'MODEL_SELF_SCORE','wants_to_continue':True,'robotic_or_tiring':False,'feedback':'9.9/10'}, 'PASS')
        with self.assertRaisesRegex(ValueError, 'TEST_VERDICT_NOT_SUPPORTED'):
            current.test_outcome(self.root, receipt)

    def test_missing_reading_answer_is_not_pass(self):
        receipt = self.make_test_receipt({'source':'ACTUAL_USER_FEEDBACK','wants_to_continue':True,'feedback':'愿意继续'}, 'PASS')
        with self.assertRaisesRegex(ValueError, 'TEST_VERDICT_NOT_SUPPORTED'):
            current.test_outcome(self.root, receipt)

    def test_no_feedback_cannot_be_used_as_failure(self):
        receipt = self.make_test_receipt({}, 'FAIL')
        with self.assertRaisesRegex(ValueError, 'TEST_VERDICT_NOT_SUPPORTED'):
            current.test_outcome(self.root, receipt)

    def test_one_negative_reading_answer_is_failure(self):
        receipt = self.make_test_receipt({'source':'ACTUAL_USER_FEEDBACK','wants_to_continue':False,'feedback':'不想继续'}, 'FAIL')
        self.assertEqual(current.test_outcome(self.root, receipt), 'FAIL')

    def test_frozen_scene_waits_for_reading_without_authorizing_another(self):
        receipt = self.make_test_receipt({})
        artifact = self.read(receipt)['artifact']
        def change(state):
            state['mainline_state'].update(current_step='STEP_03', completed_steps=['STEP_01','STEP_02'],
                test_artifacts={'TEST_01':artifact}, test_results={'TEST_01':receipt}, new_prose_authorized_now=False)
            state['next_action'] = state['next_required_action'] = self.steps[2]['await_action']
        self.mutate_state(change)
        result = current.verify(self.root)
        self.assertEqual(result['mainline']['outcomes']['TEST_01'], 'UNKNOWN')
        self.assertFalse(result['new_prose_authorized'])

    def test_same_frozen_test_cannot_be_redispatched(self):
        receipt = self.make_test_receipt({})
        artifact = self.read(receipt)['artifact']
        def change(state):
            state['mainline_state'].update(current_step='STEP_03', completed_steps=['STEP_01','STEP_02'],
                test_artifacts={'TEST_01':artifact}, new_prose_authorized_now=True)
            state['next_action'] = state['next_required_action'] = self.steps[2]['action']
        self.mutate_state(change)
        self.expect_block('STALE_MAINLINE_NEXT_ACTION')

    def freeze_rejected_test(self, action):
        receipt = self.make_test_receipt({'source':'ACTUAL_USER_FEEDBACK',
            'wants_to_continue':False,'robotic_or_tiring':True,
            'feedback':'不想看，剧情拖拉，两个人像机器人。'}, 'FAIL')
        artifact = self.read(receipt)['artifact']
        def change(state):
            state['mainline_state'].update(current_step='STEP_03', completed_steps=['STEP_01','STEP_02'],
                test_artifacts={'TEST_01':artifact}, test_results={'TEST_01':receipt}, new_prose_authorized_now=False)
            state['next_action'] = state['next_required_action'] = action
        self.mutate_state(change)

    def test_rejected_test_moves_to_scoped_revision_without_authorizing_prose(self):
        self.freeze_rejected_test('DEFINE_ONE_SCOPED_METHOD_REVISION_AFTER_TEST_01_FAILURE')
        result = current.verify(self.root)
        self.assertEqual(result['mainline']['outcomes']['TEST_01'], 'FAIL')
        self.assertFalse(result['new_prose_authorized'])
        self.assertEqual(result['mainline']['revision'], self.revision)
        self.mutate_state(lambda state: state['mainline_state'].update(new_prose_authorized_now=True))
        self.expect_block('PROSE_AUTHORIZATION_STEP_DRIFT')

    def test_rejected_test_cannot_remain_awaiting_repeat_feedback(self):
        self.freeze_rejected_test(self.steps[2]['await_action'])
        self.expect_block('STALE_MAINLINE_NEXT_ACTION')

    def test_continuity_failure_requires_a_location(self):
        receipt = self.make_test_receipt({}, 'FAIL', {'verdict':'FAIL'})
        with self.assertRaisesRegex(ValueError, 'UNLOCATED_FACT_FAILURE'):
            current.test_outcome(self.root, receipt)

    def propose_revision(self, basis_receipt):
        revision = self.revision + 1
        task_path = 'state/tasks/NOVEL_IMPROVEMENT_MAINLINE_V' + str(revision) + '.json'
        task = self.read(self.contract_path)
        task.update(task_id='NOVEL-IMPROVEMENT-MAINLINE-V' + str(revision), revision=revision)
        self.write(task_path, task)
        with (self.root / self.plan_path).open('a', encoding='utf-8') as f:
            f.write('\nSynthetic scoped method revision for guard verification.\n')
        plan = {'path':self.plan_path,'sha256':hashlib.sha256((self.root / self.plan_path).read_bytes()).hexdigest()}
        task_ref = {'path':task_path,'blob':current.git_blob((self.root / task_path).read_bytes())}
        lock_path = 'state/review_receipts/test-v2-lock.json'
        self.write(lock_path, {
            'project_id':'novel-distillation','task_id':task['task_id'],'revision':revision,
            'previous_lock_blob':self.previous_lock_blob,'changed_scope':['writer_packet'],
            'basis':{'type':'RECORDED_FROZEN_TEST_FAILURE','evidence_path':basis_receipt,
                     'evidence_blob':current.git_blob((self.root / basis_receipt).read_bytes())},
            'plan':plan,'task':dict(task_ref,sha256=hashlib.sha256((self.root / task_path).read_bytes()).hexdigest()),
        })
        lock_ref = {'path':lock_path,'blob':current.git_blob((self.root / lock_path).read_bytes())}
        def change(state):
            state['mainline_state'].update(task_id=task['task_id'], revision=revision, contract=task_ref, plan=plan)
            state['mainline_state']['lock_chain'].append(lock_ref)
            state.update(active_task_ids=[task['task_id']], active_task_contract=task_path)
            if 'active_task' in state:
                state['active_task'].update(task_id=task['task_id'], contract=task_path)
        self.mutate_state(change)

    def test_actual_failed_frozen_test_allows_scoped_new_revision(self):
        receipt = self.make_test_receipt({'source':'ACTUAL_USER_FEEDBACK','wants_to_continue':False,'feedback':'不想继续'}, 'FAIL')
        self.propose_revision(receipt)
        result = current.verify(self.root)
        self.assertEqual(result['mainline']['revision'], self.revision + 1)
        self.assertFalse(result['new_prose_authorized'])

    def test_unknown_feedback_cannot_unlock_new_revision(self):
        receipt = self.make_test_receipt({})
        self.propose_revision(receipt)
        self.expect_block('REVISION_WITHOUT_FAILED_TEST')

    def test_complete_human_observations_only_support_local_pass(self):
        receipt = self.make_test_receipt({'source':'ACTUAL_USER_FEEDBACK','wants_to_continue':True,'robotic_or_tiring':False,'feedback':'本场愿意继续，人物互动不累'}, 'PASS')
        self.assertEqual(current.test_outcome(self.root, receipt), 'PASS')
        result = current.verify(self.root)
        self.assertFalse(result['new_prose_authorized'])

    def test_short_reading_pass_cannot_skip_full_scene_validation(self):
        if 'TEST_01_FULL' not in self.read(self.contract_path)['tests']:
            self.skipTest('Current method has no separate short-reading stage')
        receipt = self.make_test_receipt({'source':'ACTUAL_USER_FEEDBACK','wants_to_continue':True,
            'robotic_or_tiring':False,'feedback':'这几百字愿意继续读'}, 'PASS')
        artifact = self.read(receipt)['artifact']
        def change(state):
            state['mainline_state'].update(current_step='STEP_05',
                completed_steps=['STEP_01','STEP_02','STEP_03','STEP_04'],
                test_artifacts={'TEST_01':artifact},test_results={'TEST_01':receipt},new_prose_authorized_now=True)
            state['next_action'] = state['next_required_action'] = self.steps[4]['action']
        self.mutate_state(change)
        self.expect_block('TEST_02_WITHOUT_FULL_SCENE_PASS')

    def test_short_reading_result_cannot_claim_full_scene_scope(self):
        if 'TEST_01_FULL' not in self.read(self.contract_path)['tests']:
            self.skipTest('Current method has no separate short-reading stage')
        receipt = self.make_test_receipt({}, 'UNKNOWN')
        artifact = self.read(receipt)['artifact']
        r = self.read(receipt)
        r['validation_scope'] = 'FULL_SCENE'
        self.write(receipt, r)
        def change(state):
            state['mainline_state'].update(current_step='STEP_03',completed_steps=['STEP_01','STEP_02'],
                test_artifacts={'TEST_01':artifact},test_results={'TEST_01':receipt},new_prose_authorized_now=False)
            state['next_action'] = state['next_required_action'] = self.steps[2]['await_action']
        self.mutate_state(change)
        self.expect_block('TEST_READING_SCOPE_DRIFT')


if __name__ == '__main__':
    unittest.main()
