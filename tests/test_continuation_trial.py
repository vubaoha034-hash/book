"""Corrupt real artifact, context and budget bindings; never judge prose."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('continuation_gate',REPO/'scripts/verify_continuation_trial.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
# Historical corruption cases use pinned CP204 data; gates above stay current.
_fixture_spec=importlib.util.spec_from_file_location('pinned_test_data',REPO/'scripts/frozen_history.py')
_fixture_module=importlib.util.module_from_spec(_fixture_spec);_fixture_spec.loader.exec_module(_fixture_module)
REPO=_fixture_module.historical_test_data(REPO)

class ContinuationTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes());self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route=self.project['continuation_short_trial'];self.copy_refs(self.route);self.copy_refs(self.project['opening_hook_trial']);self.copy_refs(self.project['hook_trial_human_feedback']);self.copy('START_HERE.md')
        for role in ('writer','facts','editor','reader'):self.copy(g.runner.DIRECTORY+f'/{role}.attempt.json')
        for role in ('facts','editor','reader'):self.copy(f'delivery/hook-trial-20261003/{role}-policy.txt')
        for path in self.project['mainline_state']['test_results'].values():self.copy(path)
    def copy(self,path):
        if path in self.seen or not(REPO/path).is_file():return
        self.seen.add(path);p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(p.read_bytes()))
    def copy_refs(self,v):
        if isinstance(v,dict):
            if all(k in v for k in ('path','blob','sha256')):self.copy(v['path'])
            for child in v.values():self.copy_refs(child)
        elif isinstance(v,list):
            for child in v:self.copy_refs(child)
    def read(self,path):return json.loads((self.root/path).read_bytes())
    def write(self,path,v):(self.root/path).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
    def rebind(self):
        done=set()
        def refresh(v):
            if isinstance(v,dict):
                if all(k in v for k in ('path','blob','sha256')):
                    path=v['path'];p=self.root/path
                    current='continuation-short-20261003/' in path or 'CONTINUATION_SHORT_' in path or 'SAME_SCENE_ONE_CONTINUATION_' in path or path==g.runner.MANIFEST
                    if p.is_file():
                        if current and path.endswith('.json') and path not in done:
                            done.add(path);j=self.read(path);refresh(j);self.write(path,j)
                        b=p.read_bytes();v.update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for child in v.values():refresh(child)
            elif isinstance(v,list):
                for child in v:refresh(child)
        refresh(self.route);self.cp['continuation_short_trial']=copy.deepcopy(self.route)
    def mutate(self,path,fn):
        v=self.read(path);fn(v);self.write(path,v);self.rebind()
    def verify(self):return g.continuation_action(self.root,self.project,self.cp,g.OLD)
    def test_actual_independent_reviews_end_at_human_unknown(self):
        self.assertEqual(self.verify(),g.NEXT);self.assertEqual(self.route['human_quality_result'],'UNKNOWN')
        self.assertEqual(self.read(self.project['mainline_state']['test_results']['TEST_01'])['outcome'],'UNKNOWN')
    def test_no_report_cannot_pass(self):
        (self.root/self.route['raw_reports']['facts']['path']).unlink()
        with self.assertRaisesRegex(ValueError,'MISSING_MATERIAL'):self.verify()
    def test_report_received_false_cannot_pass(self):
        self.mutate(self.route['runtimes']['facts']['path'],lambda v:v.update(report_received=False))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_failed_execution_cannot_pass(self):
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v.update(turn_status='failed'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_model_name_in_prompt_is_not_setting(self):
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_shared_context_is_rejected(self):
        same=self.read(self.route['runtimes']['editor']['path'])['thread_id']
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(thread_id=same))
        with self.assertRaisesRegex(ValueError,'SHARED_CONTEXT'):self.verify()
    def test_cold_packet_disallows_answers(self):
        packet=self.read(self.read(self.route['manifest']['path'])['jobs']['reader']['packet']['path']);packet['human_feedback']='known answer'
        with self.assertRaisesRegex(ValueError,'ALLOWLIST'):g.runner.review.validate_packet(packet)
    def test_writer_fact_cannot_expand(self):
        self.mutate(self.route['writer_input']['path'],lambda v:v['facts'].update(new_life_fact='new debt'))
        with self.assertRaisesRegex(ValueError,'ANSWER_OR_NEW_FACT'):self.verify()
    def test_previous_401_is_immutable(self):
        p=self.root/self.route['previous_excerpt']['path'];p.write_bytes(p.read_bytes()+b'x')
        with self.assertRaisesRegex(ValueError,'IDENTITY_DRIFT'):self.verify()
    def test_reading_copy_is_mechanical_concat_only(self):
        p=self.root/self.route['reading_copy']['path'];p.write_bytes(p.read_bytes()+b'x');self.rebind()
        with self.assertRaisesRegex(ValueError,'EXACT_CONCATENATION'):self.verify()
    def test_old_budget_cannot_reset(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_RC3_remaining_rounds=1))
        with self.assertRaisesRegex(ValueError,'PERMISSION_OR_PREFIX'):self.verify()
    def test_cannot_unlock_197(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_197_character_protection_released=True))
        with self.assertRaisesRegex(ValueError,'PERMISSION_OR_PREFIX'):self.verify()
    def test_full_scene_cannot_promote(self):
        self.route['full_scene_or_TEST01_promoted']=True;self.cp['continuation_short_trial']=copy.deepcopy(self.route)
        with self.assertRaisesRegex(ValueError,'BUDGET_OR_HUMAN'):self.verify()
    def test_ai_vote_cannot_be_human_pass(self):
        self.route['human_quality_result']='PASS';self.cp['continuation_short_trial']=copy.deepcopy(self.route)
        with self.assertRaisesRegex(ValueError,'BUDGET_OR_HUMAN'):self.verify()
    def test_vote_cannot_trigger_new_generation(self):
        self.mutate(self.route['settlement']['path'],lambda v:v.update(reader_vote_triggers_more_generation=True))
        with self.assertRaisesRegex(ValueError,'SETTLEMENT_OR_UNKNOWN'):self.verify()
    def test_fact_conflicts_cannot_be_hidden(self):
        self.mutate(self.route['settlement']['path'],lambda v:v.update(fact_conflicts_unresolved=['pending']))
        with self.assertRaisesRegex(ValueError,'SETTLEMENT_OR_UNKNOWN'):self.verify()
    def test_wrong_report_artifact_is_rejected(self):
        path=self.route['raw_reports']['reader']['path'];v=self.read(path);v['original_sha256']='0'*64;self.write(path,v);self.rebind()
        with self.assertRaisesRegex(ValueError,'REPORT_OR_QUOTE'):self.verify()
    def test_insufficient_material_cannot_pass(self):
        path=self.route['raw_reports']['facts']['path'];v=self.read(path);v['results'][0]['verdict']='INSUFFICIENT';self.write(path,v);self.rebind()
        with self.assertRaises(ValueError):self.verify()
    def test_unlocated_quote_is_rejected(self):
        path=self.route['raw_reports']['reader']['path'];v=self.read(path);v['reactions'][0]['quote']='不存在的引文';self.write(path,v);self.rebind()
        with self.assertRaisesRegex(ValueError,'REPORT_OR_QUOTE'):self.verify()
    def test_unknown_keeps_human_record_empty(self):
        self.mutate(self.route['pending_human_review']['path'],lambda v:v.update(outcome='PASS',accepted=True))
        with self.assertRaisesRegex(ValueError,'SETTLEMENT_OR_UNKNOWN'):self.verify()
if __name__=='__main__':unittest.main()
