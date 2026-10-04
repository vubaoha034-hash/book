"""Corrupt actual local-repair evidence; preserve the earlier positive and failures."""
import copy,hashlib,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
GIT_REPO=REPO
s=importlib.util.spec_from_file_location('clarity_test_gate',REPO/'scripts/verify_clarity_repair.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
# Preserve the completed CP206 evidence when a later human review starts repair.
_live=json.loads((REPO/'state/project_state.json').read_bytes())
if _live.get('emotion_dialogue_repair'):REPO=g.history.frozen_tree(GIT_REPO,_live['emotion_dialogue_repair']['source_head'])
class ClarityRepairTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name).resolve();self.seen=set()
        for p in g.history.frozen_tree(GIT_REPO,g.SOURCE).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                rel=p.relative_to(g.history.frozen_tree(GIT_REPO,g.SOURCE));target=self.root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((REPO/rel).read_bytes());self.seen.add(rel.as_posix())
        self.project=json.loads((REPO/'state/project_state.json').read_bytes());self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes());self.route=self.project['clarity_repair'];self.copy_refs(self.route)
        for role in ('writer','editor','reader'):self.copy('state/reviews/clarity-repair-20261004/'+role+'.attempt.json')
    def copy(self,path):
        if path in self.seen or not(REPO/path).is_file():return
        self.seen.add(path);p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(p.read_bytes()))
    def copy_refs(self,v):
        if isinstance(v,dict):
            if all(k in v for k in ('path','blob','sha256')):self.copy(v['path'])
            for x in v.values():self.copy_refs(x)
        elif isinstance(v,list):
            for x in v:self.copy_refs(x)
    def read(self,p):return json.loads((self.root/p).read_bytes())
    def write(self,p,v):(self.root/p).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
    def rebind(self):
        done=set()
        def update(v):
            if isinstance(v,dict):
                if all(k in v for k in ('path','blob','sha256')):
                    p=self.root/v['path'];active='clarity-repair-20261004/' in v['path'] or 'CLARITY_REPAIR_' in v['path'] or v['path']=='config/novel-clarity-repair-20261004.json'
                    if p.is_file():
                        if active and v['path'].endswith('.json') and v['path'] not in done:
                            done.add(v['path']);j=self.read(v['path']);update(j);self.write(v['path'],j)
                        b=p.read_bytes();v.update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for x in list(v.values()):update(x)
            elif isinstance(v,list):
                for x in v:update(x)
        update(self.route);self.cp['clarity_repair']=copy.deepcopy(self.route);self.write('state/project_state.json',self.project);self.cp['action_guard']['project_state_sha256']=hashlib.sha256((self.root/'state/project_state.json').read_bytes()).hexdigest()
    def mutate(self,path,fn):
        v=self.read(path);fn(v);self.write(path,v);self.rebind()
    def verify(self):return g.verify(self.root,self.project,self.cp)
    def test_one_local_repair_stops_at_human_unknown(self):
        v=self.verify();self.assertEqual(v['sequence'],206);self.assertEqual(v['historical_checks_passed'],39);self.assertEqual(v['source_retention_result'],'YES_ONLY_FOR_383')
    def test_missing_report_rejected(self):
        (self.root/self.route['raw_reports']['reader']['path']).unlink()
        with self.assertRaises(ValueError):self.verify()
    def test_runtime_failure_rejected(self):
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(turn_status='failed'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_fake_model_setting_rejected(self):
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_old_call_cannot_be_reused(self):
        same=self.read(self.route['runtimes']['writer']['path'])['thread_id'];self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(thread_id=same))
        with self.assertRaisesRegex(ValueError,'SHARED_CONTEXT'):self.verify()
    def test_ai_cannot_promote_human_verdict(self):
        self.route['human_quality_result']='PASS';self.rebind()
        with self.assertRaisesRegex(ValueError,'BUDGET_OR_HUMAN'):self.verify()
    def test_source_positive_cannot_promote_ai_style(self):
        self.mutate(self.route['human_feedback']['path'],lambda v:v['review'].update(ai_smell_verdict='PASS'))
        with self.assertRaisesRegex(ValueError,'HUMAN_SCOPE'):self.verify()
    def test_no_new_plot_facts(self):
        self.mutate(self.route['writer_input']['path'],lambda v:v['facts'].update(new_crime='new crime'))
        with self.assertRaisesRegex(ValueError,'NEW_FACT_OR_ANSWER'):self.verify()
    def test_protected_phone_paragraph_must_be_exact(self):
        p=self.root/self.route['final_artifact']['path'];text=p.read_text(encoding='utf-8').replace('“出来再说。”','“我知道真相。”');p.write_bytes(text.encode());self.rebind()
        with self.assertRaisesRegex(ValueError,'PROTECTED_SCOPE'):self.verify()
    def test_cold_reader_does_not_receive_known_criticism(self):
        manifest=self.read(self.route['manifest']['path']);packet=self.read(manifest['jobs']['reader']['packet']['path']);packet['human_feedback']='known confusion'
        with self.assertRaisesRegex(ValueError,'ALLOWLIST'):g.runner.review.validate_packet(packet)
    def test_unknown_is_not_invented_pass(self):
        self.mutate(self.route['pending_human_review']['path'],lambda v:v.update(outcome='PASS',accepted=True))
        with self.assertRaisesRegex(ValueError,'SETTLEMENT_OR_UNKNOWN'):self.verify()
    def test_actor_claim_must_have_actual_quote(self):
        self.mutate(self.route['settlement']['path'],lambda v:v['clarity_checks'][0].update(quote='不存在的动作'))
        with self.assertRaisesRegex(ValueError,'OWNERSHIP_EVIDENCE'):self.verify()
    def test_old_source_body_immutable(self):
        p=self.root/self.route['source_artifact']['path'];p.write_bytes(p.read_bytes()+b'x')
        with self.assertRaisesRegex(ValueError,'HISTORICAL_FILE_CHANGED'):self.verify()
    def test_old_budget_cannot_reset(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_RC3_remaining_rounds=1))
        with self.assertRaisesRegex(ValueError,'PERMISSION'):self.verify()
if __name__=='__main__':unittest.main()
