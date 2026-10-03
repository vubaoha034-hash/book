"""New route corruption tests against actual evidence; no model calls."""
import copy,hashlib,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('new_story_gate',REPO/'scripts/verify_story_trial.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
class StoryTrialTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name).resolve()
        source=g.history.frozen_tree(REPO,g.SOURCE)
        for p in source.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                rel=p.relative_to(source);target=self.root/rel;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((REPO/rel).read_bytes())
        for folder in ('delivery/new-story-20261004','state/reviews/new-story-20261004','state/learning/new-story-20261004'):
            shutil.copytree(REPO/folder,self.root/folder)
        for p in ['config/novel-new-story-20261004.json','state/tasks/NOVEL_NEW_STORY_PSYCHOLOGY_OPENING_TRIAL_20261004.json',
            *[v.relative_to(REPO).as_posix() for v in (REPO/'state/review_receipts').glob('*20261004.json')]]:
            q=self.root/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((REPO/p).read_bytes())
        p=self.root/'docs/NOVEL_NEW_STORY_TRIAL_RESULT_20261004.md';p.write_bytes((REPO/'docs/NOVEL_NEW_STORY_TRIAL_RESULT_20261004.md').read_bytes())
        self.project=self.read('state/project_state.json');self.cp=self.read('state/continuity/LATEST_CHECKPOINT.json');self.route=self.project['story_replacement_trial']
    def read(self,path):return json.loads((self.root/path).read_bytes())
    def write(self,path,v):(self.root/path).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
    def rebind(self):
        done=set()
        def update(v):
            if isinstance(v,dict):
                if all(k in v for k in ('path','blob','sha256')):
                    p=self.root/v['path']
                    if p.is_file():
                        if ('new-story-20261004/' in v['path'] or 'NEW_STORY_' in v['path'] or v['path']==g.MANIFEST) and v['path'].endswith('.json') and v['path'] not in done:
                            done.add(v['path']);j=self.read(v['path']);update(j);self.write(v['path'],j)
                        b=p.read_bytes();v.update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for child in list(v.values()):update(child)
            elif isinstance(v,list):
                for child in v:update(child)
        update(self.route);self.cp['story_replacement_trial']=copy.deepcopy(self.route)
        self.write('state/project_state.json',self.project);self.cp['action_guard']['project_state_sha256']=hashlib.sha256((self.root/'state/project_state.json').read_bytes()).hexdigest()
    def mutate(self,path,fn):
        v=self.read(path);fn(v);self.write(path,v);self.rebind()
    def verify(self):return g.verify(self.root,self.project,self.cp)
    def test_actual_three_isolated_calls_end_at_unknown(self):
        r=self.verify();self.assertEqual(r['sequence'],205);self.assertEqual(r['historical_checks_passed'],27);self.assertEqual(r['human_quality_result'],'UNKNOWN')
    def test_no_raw_report_cannot_pass(self):
        (self.root/self.route['raw_reports']['reader']['path']).unlink()
        with self.assertRaises(ValueError):self.verify()
    def test_failed_runtime_cannot_pass(self):
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v.update(turn_status='failed'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_model_name_in_prompt_does_not_override_setting(self):
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_shared_context_rejected(self):
        tid=self.read(self.route['runtimes']['writer']['path'])['thread_id'];self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(thread_id=tid))
        with self.assertRaisesRegex(ValueError,'SHARED_CONTEXT'):self.verify()
    def test_cold_packet_cannot_receive_author_explanation(self):
        m=self.read(self.route['manifest']['path']);packet=self.read(m['jobs']['reader']['packet']['path']);packet['facts']={'answer':'hidden'}
        with self.assertRaisesRegex(ValueError,'ALLOWLIST'):g.runner.review.validate_packet(packet)
    def test_wrong_body_hash_rejected(self):
        v=self.read(self.route['raw_reports']['reader']['path']);v['original_sha256']='0'*64;self.write(self.route['raw_reports']['reader']['path'],v);self.rebind()
        with self.assertRaisesRegex(ValueError,'REPORT_OR_QUOTE'):self.verify()
    def test_invented_quote_rejected(self):
        path=self.route['raw_reports']['reader']['path'];v=self.read(path);v['reactions'][0]['quote']='不存在的引文';self.write(path,v);self.rebind()
        with self.assertRaisesRegex(ValueError,'REPORT_OR_QUOTE'):self.verify()
    def test_insufficient_editor_report_rejected(self):
        path=self.route['raw_reports']['editor']['path'];v=self.read(path);v['results'][0]['verdict']='INSUFFICIENT';self.write(path,v);self.rebind()
        with self.assertRaises(ValueError):self.verify()
    def test_old_budget_cannot_reset(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_RC3_remaining_rounds=1))
        with self.assertRaisesRegex(ValueError,'PERMISSION'):self.verify()
    def test_old_197_cannot_unlock(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_197_character_protection_released=True))
        with self.assertRaisesRegex(ValueError,'PERMISSION'):self.verify()
    def test_ai_vote_cannot_be_human_pass(self):
        self.route['human_quality_result']='PASS';self.rebind()
        with self.assertRaisesRegex(ValueError,'BUDGET_OR_HUMAN'):self.verify()
    def test_unknown_cannot_have_fabricated_feedback(self):
        self.mutate(self.route['pending_human_review']['path'],lambda v:v.update(outcome='PASS',accepted=True))
        with self.assertRaisesRegex(ValueError,'SETTLEMENT_OR_UNKNOWN'):self.verify()
    def test_reader_vote_cannot_trigger_generation(self):
        self.mutate(self.route['settlement']['path'],lambda v:v.update(reader_vote_triggers_more_generation=True))
        with self.assertRaisesRegex(ValueError,'SETTLEMENT_OR_UNKNOWN'):self.verify()
    def test_old_body_must_remain_exact(self):
        p=self.root/'delivery/continuation-short-20261003/continuation-a1.md';p.write_bytes(p.read_bytes()+b'x')
        with self.assertRaisesRegex(ValueError,'HISTORICAL_ARTIFACT'):self.verify()
    def test_old_false_negative_calibration_cannot_change(self):
        self.project['codex_review_integration']['quality_certification_allowed']=True;self.cp['codex_review_integration']=copy.deepcopy(self.project['codex_review_integration'])
        with self.assertRaisesRegex(ValueError,'HISTORICAL_STATE'):self.verify()
    def test_closed_historical_task_guard_cannot_delete(self):
        self.project['closed_task_ids'].pop(0);self.cp['action_guard']['closed_task_ids']=self.project['closed_task_ids'];self.rebind()
        with self.assertRaisesRegex(ValueError,'CLOSED_TASK_GUARD'):self.verify()
    def test_default_audit_scope_is_preserved_and_new_scope_explicit(self):
        m=self.read(self.route['manifest']['path']);packet=self.read(m['jobs']['reader']['packet']['path']);report=self.read(self.route['raw_reports']['reader']['path']);runtime=self.read(self.route['runtimes']['reader']['path'])
        self.assertTrue(g.runner.roles.audit_reader(packet,report,runtime)['errors'])
        self.assertEqual(g.runner.roles.audit_reader(packet,report,runtime,'NEW_STORY_OPENING_EXCERPT')['errors'],[])
        with self.assertRaisesRegex(ValueError,'UNAUTHORIZED_REVIEW_SCOPE'):g.runner.roles.audit_reader(packet,report,runtime,'FULL_NOVEL')
if __name__=='__main__':unittest.main()
