"""Evidence, isolation and authority corruption tests; never literary scores."""
from pathlib import Path
import copy,hashlib,importlib.util,json,tempfile,unittest
REPO=Path(__file__).resolve().parents[1];GIT_REPO=REPO
s=importlib.util.spec_from_file_location('scoped_test_gate',REPO/'scripts/verify_scoped_short_repair.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
current_project=json.loads((REPO/'state/project_state.json').read_bytes())
if current_project.get('scoped_short_repair',{}).get('scope_kind')=='NATURAL_SCENE_RELATION_EMOTION':
    REPO=g.history.frozen_tree(GIT_REPO,current_project['scoped_short_repair']['source_head'])

class ScopedShortRepairTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name).resolve();self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes());self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes());self.route=self.project['scoped_short_repair']
        source=g.history.frozen_tree(GIT_REPO,self.route['source_head'])
        for p in source.rglob('*'):
            if p.is_file()and '__pycache__'not in p.parts:
                rel=p.relative_to(source);q=self.root/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((REPO/rel).read_bytes());self.seen.add(rel.as_posix())
        self.copy_refs(self.route)
        directory=self.read(self.route['manifests']['writer']['path'])['result_dir']
        for role in('writer','editor','reader'):self.copy(directory+'/'+role+'.attempt.json')
    def copy(self,path):
        if path in self.seen or not(REPO/path).is_file():return
        self.seen.add(path);q=self.root/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(q.read_bytes()))
    def copy_refs(self,v):
        if isinstance(v,dict):
            if all(k in v for k in('path','blob','sha256')):self.copy(v['path'])
            for x in v.values():self.copy_refs(x)
        elif isinstance(v,list):
            for x in v:self.copy_refs(x)
    def read(self,p):return json.loads((self.root/p).read_bytes())
    def write(self,p,v):(self.root/p).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
    def rebind(self):
        done=set()
        def update(v):
            if isinstance(v,dict):
                if all(k in v for k in('path','blob','sha256')):
                    p=self.root/v['path'];active='fear-concealment-20261004'in v['path']or'FEAR_CONCEALMENT_REPAIR_'in v['path']
                    if p.is_file():
                        if active and v['path'].endswith('.json')and v['path']not in done:
                            done.add(v['path']);j=self.read(v['path']);update(j);self.write(v['path'],j)
                        b=p.read_bytes();v.update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for x in list(v.values()):update(x)
            elif isinstance(v,list):
                for x in v:update(x)
        update(self.route);self.cp['scoped_short_repair']=copy.deepcopy(self.route);self.write('state/project_state.json',self.project);self.cp['action_guard']['project_state_sha256']=hashlib.sha256((self.root/'state/project_state.json').read_bytes()).hexdigest()
    def mutate(self,p,fn):
        v=self.read(p);fn(v);self.write(p,v);self.rebind()
    def verify(self):return g.verify(self.root,self.project,self.cp)
    def test_three_calls_and_one_repair_stop_at_human_unknown(self):
        r=self.verify();self.assertEqual(r['sequence'],208);self.assertEqual(r['historical_checks_passed'],61);self.assertFalse(r['new_prose_authorized'])
    def test_missing_report_is_not_pass(self):
        (self.root/self.route['raw_reports']['editor']['path']).unlink()
        with self.assertRaises(ValueError):self.verify()
    def test_failed_runtime_is_not_pass(self):
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(turn_status='failed'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_fake_max_rejected(self):
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_shared_thread_rejected(self):
        same=self.read(self.route['runtimes']['writer']['path'])['thread_id'];self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(thread_id=same))
        with self.assertRaisesRegex(ValueError,'SHARED_CONTEXT'):self.verify()
    def test_AI_cannot_promote_human(self):
        self.route['human_quality_result']='PASS';self.rebind()
        with self.assertRaisesRegex(ValueError,'BUDGET_OR_HUMAN'):self.verify()
    def test_human_emotion_fail_is_not_new_retention_fail(self):
        self.mutate(self.route['human_feedback']['path'],lambda v:v['review'].update(wants_to_continue=False))
        with self.assertRaisesRegex(ValueError,'HUMAN_SCOPE'):self.verify()
    def test_cold_reader_cannot_receive_failure(self):
        m=self.read(self.route['manifests']['reviews']['path']);packet=self.read(m['jobs']['reader']['packet']['path']);packet['human_feedback']='known failure'
        with self.assertRaisesRegex(ValueError,'ALLOWLIST'):g.runner.review.validate_packet(packet)
    def test_writer_cannot_gain_life_fact(self):
        self.mutate(self.route['writer_input']['path'],lambda v:v['facts'].update(childhood_debt='invented'))
        with self.assertRaisesRegex(ValueError,'FACT_OR_ANSWER'):self.verify()
    def test_old_budget_cannot_reset(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_RC3_remaining_rounds=1))
        with self.assertRaisesRegex(ValueError,'AUTHORITY'):self.verify()
    def test_reaction_claim_requires_real_quote(self):
        self.mutate(self.route['settlement']['path'],lambda v:v['reaction_and_restraint_checks'][0].update(quote='不存在的惊吓'))
        with self.assertRaisesRegex(ValueError,'COORDINATOR_QUOTE'):self.verify()
    def test_restraint_cannot_be_only_a_pass_label(self):
        self.mutate(self.route['settlement']['path'],lambda v:v.update(reaction_and_restraint_checks=[]))
        with self.assertRaisesRegex(ValueError,'REACTION_EVIDENCE_MISSING'):self.verify()
    def test_report_window_misplacement_must_be_separately_corrected(self):
        s=self.read(self.route['settlement']['path']);self.mutate(s['report_interpretation_audit']['path'],lambda v:v.update(corrections=[]))
        with self.assertRaisesRegex(ValueError,'WINDOW_CORRECTION_MISSING'):self.verify()
if __name__=='__main__':unittest.main()
