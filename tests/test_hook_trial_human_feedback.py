"""A partial human compliment must not become acceptance or fresh writing permission."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('hook_feedback_gate',REPO/'scripts/verify_hook_trial.py');gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)
class HookHumanFeedbackTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes());self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        authorization=None
        if 'continuation_short_trial' in self.project:
            continuation=gate.module('partial_fixture_continuation','verify_continuation_trial.py')
            self.project,self.cp,authorization=continuation.historical_hook_view(REPO,self.project,self.cp)
        if self.project.get('hook_trial_human_feedback',{}).get('reading_supplement'):
            self.project,self.cp=gate.reading_historical_view(REPO,self.project,self.cp,authorization)
        self.feedback=self.project['hook_trial_human_feedback'];self.copy_refs(self.project['opening_hook_trial']);self.copy_refs(self.project['opening_prose_repair']);self.copy_refs(self.feedback);self.copy('START_HERE.md')
        entry=self.root/'START_HERE.md'
        if '当前位置：检查点202。' not in entry.read_text(encoding='utf-8'):
            entry.write_bytes(('当前位置：检查点202。\n'+entry.read_text(encoding='utf-8')).encode())
        for role in ('diagnosis','writer','facts','editor','reader'):self.copy(gate.runner.DIRECTORY+f'/{role}.attempt.json')
        self.copy(gate.runner.DIRECTORY+'/transport-recovery/diagnosis.attempt.json')
        for role in ('writer','facts'):self.copy(gate.runner.DIRECTORY+f'/repair/{role}.attempt.json')
    def copy(self,path):
        if path in self.seen or not (REPO/path).is_file():return
        self.seen.add(path);dest=self.root/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(dest.read_bytes()))
    def copy_refs(self,v):
        if isinstance(v,dict):
            if all(k in v for k in ('path','blob','sha256')):self.copy(v['path'])
            for child in v.values():self.copy_refs(child)
        elif isinstance(v,list):
            for child in v:self.copy_refs(child)
    def mutate_receipt(self,fn):
        path=self.feedback['receipt']['path'];receipt=json.loads((self.root/path).read_bytes());fn(receipt)
        b=(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode();(self.root/path).write_bytes(b)
        self.feedback['receipt'].update(blob=gate.blob(b),sha256=hashlib.sha256(b).hexdigest())
        task_path=self.feedback['task']['path'];task=json.loads((self.root/task_path).read_bytes());task['receipt']=copy.deepcopy(self.feedback['receipt'])
        tb=(json.dumps(task,ensure_ascii=False,indent=2)+'\n').encode();(self.root/task_path).write_bytes(tb)
        self.feedback['task'].update(blob=gate.blob(tb),sha256=hashlib.sha256(tb).hexdigest());self.cp['hook_trial_human_feedback']=copy.deepcopy(self.feedback)
        self.project['latest_human_review']=receipt['review'];self.cp['latest_human_review']=copy.deepcopy(receipt['review'])
    def verify(self):return gate.hook_action(self.root,self.project,self.cp,gate.OLD)
    def test_partial_positive_keeps_unknown_and_same_body(self):
        self.assertEqual(self.verify(),gate.HUMAN_NEXT)
        self.assertEqual(self.feedback['generation_count'],0)
        self.assertEqual(self.project['opening_hook_trial']['human_quality_result'],'UNKNOWN')
    def test_cannot_invent_yes(self):
        self.mutate_receipt(lambda v:v['review'].update(wants_to_continue=True))
        with self.assertRaisesRegex(ValueError,'CANNOT_BECOME_QUALITY_VERDICT'):self.verify()
    def test_cannot_invent_emotion_pass(self):
        self.mutate_receipt(lambda v:v['review'].update(emotion_verdict='PASS'))
        with self.assertRaisesRegex(ValueError,'CANNOT_BECOME_QUALITY_VERDICT'):self.verify()
    def test_cannot_turn_partial_into_failure(self):
        self.mutate_receipt(lambda v:v.update(outcome='FAIL'))
        with self.assertRaisesRegex(ValueError,'IDENTITY_DRIFT'):self.verify()
    def test_feedback_bound_to_final_401(self):
        self.mutate_receipt(lambda v:v.update(output=self.project['opening_hook_trial']['initial_artifact']))
        with self.assertRaisesRegex(ValueError,'IDENTITY_DRIFT'):self.verify()
    def test_feedback_does_not_authorize_extra_generation(self):
        self.mutate_receipt(lambda v:v.update(new_prose_authorized=True))
        with self.assertRaisesRegex(ValueError,'CANNOT_TRIGGER_GENERATION'):self.verify()
    def test_old_snapshot_cannot_be_rewritten(self):
        self.mutate_receipt(lambda v:v.update(prior_records_rewritten=True))
        with self.assertRaisesRegex(ValueError,'IDENTITY_DRIFT'):self.verify()
    def test_prior_review_is_still_required(self):
        (self.root/self.project['opening_hook_trial']['raw_reports']['facts']['path']).unlink()
        with self.assertRaisesRegex(ValueError,'MISSING_MATERIAL'):self.verify()
if __name__=='__main__':unittest.main()
