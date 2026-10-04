"""Whole-scene scope and isolated evidence checks; no literary certification."""
from pathlib import Path
import copy,hashlib,importlib.util,json,tempfile,unittest
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('scene_test_gate',REPO/'scripts/verify_scoped_short_repair.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
class SceneEmotionTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name).resolve();self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes());self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes());self.route=self.project['scoped_short_repair']
        source=g.history.frozen_tree(REPO,self.route['source_head'])
        for path in source.rglob('*'):
            if path.is_file()and'__pycache__'not in path.parts:
                rel=path.relative_to(source);target=self.root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((REPO/rel).read_bytes());self.seen.add(rel.as_posix())
        self.copy_refs(self.route)
        directory=self.read(self.route['manifests']['production']['path'])['result_dir']
        for role in('diagnosis','writer','editor','reader'):self.copy(directory+'/'+role+'.attempt.json')
    def copy(self,path):
        if path in self.seen or not(REPO/path).is_file():return
        self.seen.add(path);target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(target.read_bytes()))
    def copy_refs(self,v):
        if isinstance(v,dict):
            if all(k in v for k in('path','blob','sha256')):self.copy(v['path'])
            for x in v.values():self.copy_refs(x)
        elif isinstance(v,list):
            for x in v:self.copy_refs(x)
    def read(self,path):return json.loads((self.root/path).read_bytes())
    def write(self,path,v):(self.root/path).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
    def rebind(self):
        done=set()
        def update(v):
            if isinstance(v,dict):
                if all(k in v for k in('path','blob','sha256')):
                    path=v['path'];p=self.root/path;active='scene-emotion-20261004'in path or'NOVEL_SCENE_EMOTION_'in path or'NOVEL_SAME_STORY_NATURAL_SCENE_EMOTION_'in path
                    if p.is_file():
                        if active and path.endswith('.json')and path not in done:
                            done.add(path);obj=self.read(path);update(obj);self.write(path,obj)
                        b=p.read_bytes();v.update(blob=g.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for x in list(v.values()):update(x)
            elif isinstance(v,list):
                for x in v:update(x)
        update(self.route);self.cp['scoped_short_repair']=copy.deepcopy(self.route);self.write('state/project_state.json',self.project);self.cp['action_guard']['project_state_sha256']=hashlib.sha256((self.root/'state/project_state.json').read_bytes()).hexdigest()
    def mutate(self,path,fn):
        v=self.read(path);fn(v);self.write(path,v);self.rebind()
    def verify(self):return g.verify(self.root,self.project,self.cp)
    def test_one_output_four_independent_calls_and_human_unknown(self):
        v=self.verify();self.assertEqual(v['sequence'],209);self.assertEqual(v['historical_checks_passed'],72);self.assertFalse(v['new_prose_authorized'])
    def test_missing_diagnosis_cannot_pass(self):
        (self.root/self.route['raw_reports']['diagnosis']['path']).unlink()
        with self.assertRaises(ValueError):self.verify()
    def test_failed_runtime_cannot_pass(self):
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(turn_status='failed'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_fake_max_cannot_pass(self):
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        with self.assertRaisesRegex(ValueError,'ACTUAL_ISOLATED'):self.verify()
    def test_writer_reader_contexts_are_distinct(self):
        tid=self.read(self.route['runtimes']['writer']['path'])['thread_id'];self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(thread_id=tid))
        with self.assertRaisesRegex(ValueError,'SHARED_CONTEXT'):self.verify()
    def test_writer_is_not_anchored_to_failed_text(self):
        self.mutate(self.route['writer_input']['path'],lambda v:v['facts'].update(source_text='the old manuscript'))
        with self.assertRaisesRegex(ValueError,'FACT_OR_ANSWER'):self.verify()
    def test_editor_has_no_authorized_emotion_answer(self):
        manifest=self.read(self.route['manifests']['reviews']['path']);path=manifest['jobs']['editor']['packet']['path'];self.mutate(path,lambda v:v['facts'].update(authorized_current_reaction='expected answer'))
        # Keep tampered request metadata internally consistent so the semantic
        # fact allowlist itself is exercised, beyond the earlier payload guard.
        payload={'verified_runtime':{'model':'gpt-6.1-sol','reasoning_effort':'max','isolation':g.runner.engine.ISOLATION},'review_packet':self.read(path)}
        digest=hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest()
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v.update(submitted_payload_sha256=digest))
        current_manifest=self.read(self.route['manifests']['reviews']['path'])
        attempt_path=current_manifest['result_dir']+'/editor.attempt.json'
        attempt=self.read(attempt_path);attempt['packet']=current_manifest['jobs']['editor']['packet'];self.write(attempt_path,attempt)
        with self.assertRaisesRegex(ValueError,'EDITOR_FACT'):self.verify()
    def test_current_question_cannot_be_new_retention_verdict(self):
        self.mutate(self.route['human_feedback']['path'],lambda v:v['review'].update(wants_to_continue=False))
        with self.assertRaisesRegex(ValueError,'HUMAN_SCOPE'):self.verify()
    def test_AI_vote_cannot_promote_human_quality(self):
        self.route['human_quality_result']='PASS';self.rebind()
        with self.assertRaisesRegex(ValueError,'BUDGET_OR_HUMAN'):self.verify()
    def test_scene_affect_needs_located_evidence(self):
        self.mutate(self.route['settlement']['path'],lambda v:v['reaction_and_restraint_checks'][0].update(quote='不存在的开心'))
        with self.assertRaisesRegex(ValueError,'COORDINATOR_QUOTE'):self.verify()
    def test_old_budget_cannot_reset(self):
        self.mutate(self.route['authorization']['path'],lambda v:v.update(old_RC3_remaining_rounds=1))
        with self.assertRaisesRegex(ValueError,'AUTHORITY'):self.verify()
    def test_public_article_is_not_a_full_book_read(self):
        self.mutate(self.route['learning_application']['path'],lambda v:v.update(full_book_read=True))
        with self.assertRaisesRegex(ValueError,'LEARNING_OVERCLAIM'):self.verify()
if __name__=='__main__':unittest.main()
