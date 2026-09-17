import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('execution_guard', ROOT/'scripts/validate_project_state_transition.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
OLD = 'PHASE380_PROSPECTIVE_AI_SMELL_DISCRIMINATOR_CALIBRATION_V1'
TOOLS = ('phase372_materialize.py','phase378_to_379.py','phase379_to_380.py','phase380_mark_ready.py','phase380_state_cleanup.py')

class CurrentTaskGuardTests(unittest.TestCase):
    def state(self):
        return json.loads((ROOT/'state/project_state.json').read_text())

    def transition(self, state, phase, task, status='PENDING'):
        return guard.validate_transition(state, phase_ordinal=phase, progress_ordinal=None,
            task_id=task, task_status=status, rollback_authorized=False)[0]

    def test_real_closed_phase380_above_accepted320_is_rejected(self):
        state=self.state()
        self.assertTrue(state['phase380_execution_state']['campaign_closed'])
        self.assertNotEqual(self.transition(state,380,OLD),guard.PASS)

    def test_noncurrent_task_cannot_pass_with_future_phase(self):
        self.assertEqual(self.transition(self.state(),999,'NOT_THE_ACTIVE_TASK'),guard.SOURCE_CONFLICT)

    def test_missing_task_identity_is_not_execution_permission(self):
        self.assertEqual(self.transition(self.state(),382,None),guard.UNKNOWN)

    def test_rejected_current_candidate_cannot_be_redispatched(self):
        state=self.state()
        self.assertNotEqual(self.transition(state,381,state['active_task']['task_id']),guard.PASS)

    def test_closed_task_stays_blocked_after_successor_becomes_active(self):
        state=self.state()
        state['active_task']={'task_id':'NEXT','phase_ordinal':382,'status':'READY_NOT_STARTED'}
        self.assertEqual(self.transition(state,380,OLD),guard.REGRESSION)

    def fixture(self, root):
        state={'accepted_checkpoint':{'phase_ordinal':40},'rollback':{'authorized':False,'receipt':None},
               'closed_task_ids':['OLD'], 'active_task':{'task_id':'CURRENT','phase_ordinal':41,'status':'IN_PROGRESS',
               'allowed_action_requests':[{'action_id':'write_test_marker','parameters':{'value':'one'}}]}}
        p=root/'state/project_state.json';p.parent.mkdir(parents=True);p.write_text(json.dumps(state))
        cp={'active_task_ids':['CURRENT'],'action_guard':{'project_state_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'closed_task_ids':['OLD']}}
        p=root/'state/continuity/LATEST_CHECKPOINT.json';p.parent.mkdir(parents=True);p.write_text(json.dumps(cp))
        return state

    def invoke(self, root, **overrides):
        args={'task_id':'CURRENT','phase_ordinal':41,'action_id':'write_test_marker','parameters':{'value':'one'}}
        args.update(overrides)
        guard.require_current_action(root,**args)
        (root/'handler_ran').write_text('one')

    def test_exact_current_action_can_reach_handler(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root);self.invoke(root)
            self.assertEqual((root/'handler_ran').read_text(),'one')

    def test_wrong_action_is_rejected_before_handler(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            with self.assertRaisesRegex(SystemExit,'ACTION_OR_PARAMETERS_NOT_AUTHORIZED'):
                self.invoke(root,action_id='different_action')
            self.assertFalse((root/'handler_ran').exists())

    def test_changed_parameters_are_rejected_before_handler(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            with self.assertRaisesRegex(SystemExit,'ACTION_OR_PARAMETERS_NOT_AUTHORIZED'):
                self.invoke(root,parameters={'value':'two'})
            self.assertFalse((root/'handler_ran').exists())

    def test_malformed_empty_parameters_cannot_match_an_empty_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            with self.assertRaisesRegex(SystemExit,'ACTION_PARAMETERS_MUST_BE_OBJECT'):
                self.invoke(root,parameters=[])
            self.assertFalse((root/'handler_ran').exists())

    def test_stale_checkpoint_is_rejected_before_handler(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);state=self.fixture(root);state['extra']='changed'
            (root/'state/project_state.json').write_text(json.dumps(state))
            with self.assertRaisesRegex(SystemExit,'STALE_OR_UNBOUND_STATE'):
                self.invoke(root)
            self.assertFalse((root/'handler_ran').exists())

    def test_conflicting_checkpoint_task_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root);p=root/'state/continuity/LATEST_CHECKPOINT.json'
            cp=json.loads(p.read_text());cp['active_task_ids']=['OTHER'];p.write_text(json.dumps(cp))
            with self.assertRaisesRegex(SystemExit,'CHECKPOINT_TASK_CONFLICT'):
                self.invoke(root)

    def test_five_real_legacy_tools_stop_before_payloads_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            files=['scripts/validate_project_state_transition.py','state/project_state.json','state/continuity/LATEST_CHECKPOINT.json']+['tools/'+name for name in TOOLS]
            for rel in files:
                dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dst)
            def snapshot():
                return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
            before=snapshot()
            for name in TOOLS:
                with self.subTest(tool=name):
                    run=subprocess.run([sys.executable,'tools/'+name],cwd=root,capture_output=True,text=True)
                    self.assertNotEqual(run.returncode,0)
                    self.assertIn('PROJECT_ACTION_BLOCKED:',run.stderr+run.stdout)
                    self.assertEqual(snapshot(),before)

if __name__ == '__main__':
    unittest.main()
