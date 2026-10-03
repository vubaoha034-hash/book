"""Qualified weak interest and natural interaction support this short only."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('qualified_gate',REPO/'scripts/verify_hook_trial.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
# Historical corruption cases use pinned CP204 data; gates above stay current.
_fixture_spec=importlib.util.spec_from_file_location('pinned_test_data',REPO/'scripts/frozen_history.py')
_fixture_module=importlib.util.module_from_spec(_fixture_spec);_fixture_spec.loader.exec_module(_fixture_module)
REPO=_fixture_module.historical_test_data(REPO)

class QualifiedShortTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes());self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        if 'continuation_short_trial' in self.project:
            continuation=g.module('qualified_fixture_continuation','verify_continuation_trial.py')
            self.project,self.cp,_=continuation.historical_hook_view(REPO,self.project,self.cp)
        self.record=self.project['hook_trial_human_feedback']['reading_supplement']
        self.copy_refs(self.project['hook_trial_human_feedback']);self.copy_refs(self.project['opening_hook_trial']);self.copy_refs(self.project['opening_prose_repair']);self.copy('START_HERE.md')
        entry=self.root/'START_HERE.md'
        if '当前位置：检查点203。' not in entry.read_text(encoding='utf-8'):
            entry.write_bytes(('当前位置：检查点203。\n'+entry.read_text(encoding='utf-8')).encode())
        for role in ('diagnosis','writer','facts','editor','reader'):self.copy(g.runner.DIRECTORY+f'/{role}.attempt.json')
        self.copy(g.runner.DIRECTORY+'/transport-recovery/diagnosis.attempt.json')
        for role in ('writer','facts'):self.copy(g.runner.DIRECTORY+f'/repair/{role}.attempt.json')
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
    def mutate(self,fn):
        path=self.record['receipt']['path'];h=json.loads((self.root/path).read_bytes());fn(h)
        b=(json.dumps(h,ensure_ascii=False,indent=2)+'\n').encode();(self.root/path).write_bytes(b)
        self.record['receipt'].update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
        path=self.record['task']['path'];task=json.loads((self.root/path).read_bytes());task['receipt']=copy.deepcopy(self.record['receipt'])
        b=(json.dumps(task,ensure_ascii=False,indent=2)+'\n').encode();(self.root/path).write_bytes(b)
        self.record['task'].update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
        self.cp['hook_trial_human_feedback']=copy.deepcopy(self.project['hook_trial_human_feedback'])
        self.project['latest_human_review']=h['review'];self.cp['latest_human_review']=copy.deepcopy(h['review'])
    def verify(self):return g.hook_action(self.root,self.project,self.cp,g.OLD)
    def test_two_targets_support_only_this_short(self):
        self.assertEqual(self.verify(),g.READING_NEXT)
        self.assertEqual(self.project['opening_hook_trial']['human_quality_result'],'UNKNOWN')
        self.assertEqual(self.record['generation_count'],0)
    def test_cannot_invent_strong_interest(self):
        self.mutate(lambda v:v['review'].update(continuation_strength='STRONG'))
        with self.assertRaisesRegex(ValueError,'SCOPE_OR_STRENGTH'):self.verify()
    def test_cannot_remove_human_qualification(self):
        self.mutate(lambda v:v.update(human_exact_feedback='想继续'))
        with self.assertRaisesRegex(ValueError,'IDENTITY_DRIFT'):self.verify()
    def test_duplicate_answer_is_one_vote(self):
        self.mutate(lambda v:v['review']['interaction_source'].update(independent_votes=2))
        with self.assertRaisesRegex(ValueError,'SCOPE_OR_STRENGTH'):self.verify()
    def test_cannot_invent_emotional_success(self):
        self.mutate(lambda v:v['review'].update(emotion_verdict='PASS'))
        with self.assertRaisesRegex(ValueError,'SCOPE_OR_STRENGTH'):self.verify()
    def test_exact_final_401_version_required(self):
        self.mutate(lambda v:v.update(output=self.project['opening_hook_trial']['initial_artifact']))
        with self.assertRaisesRegex(ValueError,'IDENTITY_DRIFT'):self.verify()
    def test_short_does_not_promote_full_scene(self):
        self.mutate(lambda v:v.update(full_scene_or_TEST01_promoted=True))
        with self.assertRaisesRegex(ValueError,'CANNOT_PROMOTE_OR_GENERATE'):self.verify()
    def test_feedback_itself_grants_no_generation(self):
        self.mutate(lambda v:v.update(new_prose_authorized=True))
        with self.assertRaisesRegex(ValueError,'CANNOT_PROMOTE_OR_GENERATE'):self.verify()
    def test_final_facts_report_still_required(self):
        (self.root/self.project['opening_hook_trial']['repair']['fact_raw_report']['path']).unlink()
        with self.assertRaisesRegex(ValueError,'MISSING_MATERIAL'):self.verify()
if __name__=='__main__':unittest.main()
