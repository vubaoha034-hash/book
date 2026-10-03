"""Corrupt real review/failure bindings in temporary copies; no model calls."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('prose_gate',REPO/'scripts/verify_prose_repair.py')
gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)

class ProseRepairTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes())
        self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route=self.project['opening_prose_repair']
        human=json.loads((REPO/self.route['human_feedback']['path']).read_bytes())
        for v in (self.project,self.cp):
            v.pop('opening_hook_trial',None)
            v.update(last_completed_task_id=gate.TASK,last_completed_task_contract=self.route['task']['path'],
                next_action=gate.NEXT,next_required_action=gate.NEXT,human_verdict_receipt=self.route['human_feedback']['path'],
                latest_human_review=human['review'],current_human_gate='PROSE_REPAIRED_NEW_SHORT_HUMAN_UNKNOWN_PRIOR_390_FAIL_OLD_FAILURES_PRESERVED')
        self.cp.update(sequence=200,stop=True)
        self.copy_refs(self.route);self.copy_refs(self.project['autonomous_opening_to_human']);self.copy('START_HERE.md')
        entry=self.root/'START_HERE.md';entry.write_bytes(('当前位置：检查点200。\n'+entry.read_text(encoding='utf-8')).encode())
        for role in ('diagnosis','writer','facts','editor','reader'):self.copy(gate.runner.DIRECTORY+f'/{role}.attempt.json')
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
    def read(self,path):return json.loads((self.root/path).read_bytes())
    def write(self,path,v):(self.root/path).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
    def rebind(self):
        done=set()
        def refresh(v):
            if isinstance(v,dict):
                if all(k in v for k in ('path','blob','sha256')):
                    path=v['path'];p=self.root/path
                    if p.is_file():
                        current=('prose-repair-20261003/' in path or 'PROSE_REPAIR_' in path or 'OPENING_390_HUMAN_FAIL' in path or path==gate.runner.MANIFEST)
                        if current and path.endswith('.json') and path not in done:
                            done.add(path);j=self.read(path);refresh(j);self.write(path,j)
                        b=p.read_bytes();v.update(blob=gate.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for child in v.values():refresh(child)
            elif isinstance(v,list):
                for child in v:refresh(child)
        refresh(self.route);self.cp['opening_prose_repair']=copy.deepcopy(self.route)
    def mutate(self,path,fn):
        v=self.read(path);fn(v);self.write(path,v);self.rebind()
    def path(self,key):return self.route[key]['path']
    def job_packet(self,role):return self.read(self.path('manifest'))['jobs'][role]['packet']['path']
    def verify(self):return gate.prose_action(self.root,self.project,self.cp,gate.OLD)
    def blocked(self,pattern):
        with self.assertRaisesRegex(ValueError,pattern):self.verify()

    def test_actual_failure_then_one_new_five_isolated_contexts(self):
        self.assertEqual(self.verify(),gate.NEXT)
        self.assertFalse(self.route['literary_quality_validated'])
        self.assertEqual(self.route['human_quality_result'],'UNKNOWN')
        self.assertEqual(self.route['previous_390_human_result'],'FAIL')
    def test_cannot_skip_historical_gates(self):
        with self.assertRaisesRegex(ValueError,'CANNOT_SKIP'):
            gate.prose_action(self.root,self.project,self.cp,'WRITE')
    def test_human_rejection_bound_to_exact_old_artifact(self):
        self.mutate(self.path('human_feedback'),lambda v:v['output'].update(self.route['final_artifact']))
        self.blocked('ACTUAL_REJECTION')
    def test_opening_description_is_not_an_exact_stop_sentence(self):
        self.mutate(self.path('human_feedback'),lambda v:v['review'].update(exact_stop_sentence='罗钧盯住两个姓名'))
        self.blocked('HUMAN_SCOPE_OR_STOP')
    def test_no_new_robot_or_emotion_human_verdict(self):
        self.mutate(self.path('human_feedback'),lambda v:v['review'].update(robotic_interaction_verdict='FAIL'))
        self.blocked('HUMAN_SCOPE_OR_STOP')
    def test_standing_permission_not_a_new_permission_loop(self):
        self.mutate(self.path('authorization'),lambda v:v.update(intermediate_user_authorization_required=True))
        self.blocked('STANDING_SCOPE_PERMISSION')
    def test_old_protection_not_released(self):
        self.mutate(self.path('authorization'),lambda v:v.update(old_197_character_protection_released=True))
        self.blocked('STANDING_SCOPE_PERMISSION')
    def test_no_old_budget_reset(self):
        self.mutate(self.path('authorization'),lambda v:v.update(old_RC3_remaining_rounds=1))
        self.blocked('STANDING_SCOPE_PERMISSION')
    def test_no_new_life_fact_in_writer_packet(self):
        self.mutate(self.path('writer_input'),lambda v:v['facts'].update(past_payment=12000))
        self.blocked('NEW_LIFE_FACT')
    def test_writer_no_diagnosis(self):
        self.mutate(self.path('writer_input'),lambda v:v.update(diagnosis='known FAIL'))
        self.blocked('WRITER_ANSWER')
    def test_cold_reader_no_known_answer(self):
        self.mutate(self.job_packet('reader'),lambda v:v.update(human_feedback='known FAIL'))
        self.blocked('CONTEXT_ALLOWLIST')
    def test_cold_reader_no_editor_report(self):
        self.mutate(self.job_packet('reader'),lambda v:v.update(editor_report='accepted'))
        self.blocked('CONTEXT_ALLOWLIST')
    def test_wrong_body_hash(self):
        self.mutate(self.job_packet('facts'),lambda v:v['samples'][0].update(original_sha256='0'*64))
        self.blocked('PACKET_TEXT_HASH|REVIEW_WRONG_ARTIFACT')
    def test_actual_effort_not_prompt_name(self):
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        self.blocked('ACTUAL_ISOLATED_SOL_MAX')
    def test_shared_writer_reader_context(self):
        w=self.read(self.route['runtimes']['writer']['path'])['thread_id']
        self.mutate(self.route['runtimes']['reader']['path'],lambda v:v.update(thread_id=w))
        self.blocked('SHARED_CONTEXT')
    def test_missing_report_no_success(self):
        (self.root/self.route['raw_reports']['facts']['path']).unlink()
        self.blocked('MISSING_MATERIAL')
    def test_failed_turn_no_success(self):
        self.mutate(self.route['runtimes']['editor']['path'],lambda v:v.update(turn_status='failed'))
        self.blocked('ACTUAL_ISOLATED_SOL_MAX')
    def test_no_extra_writer_generation(self):
        self.mutate(self.route['runtimes']['writer']['path'],lambda v:v.update(generation_count=2))
        self.blocked('RUNTIME_GENERATION_COUNT')
    def test_nonexistent_quote_not_repair_evidence(self):
        self.mutate(self.route['raw_reports']['diagnosis']['path'],lambda v:v['results'][0]['findings'][0].update(quote='不存在的原文'))
        self.blocked('REPORT_OR_QUOTE')
    def test_ai_yes_cannot_promote_human(self):
        self.mutate(self.path('pending_human_review'),lambda v:v.update(outcome='PASS',accepted=True))
        self.blocked('SETTLEMENT_OR_HUMAN_UNKNOWN')
    def test_reader_vote_not_more_generation(self):
        self.mutate(self.path('settlement'),lambda v:v.update(reader_vote_triggers_more_generation=True))
        self.blocked('SETTLEMENT_OR_HUMAN_UNKNOWN')
    def test_duplicate_finding_does_not_settle_all(self):
        self.mutate(self.path('settlement'),lambda v:v['finding_dispositions'].__setitem__(1,copy.deepcopy(v['finding_dispositions'][0])))
        self.blocked('FINDING_NOT_SETTLED')
    def test_window_quote_actual_location(self):
        self.mutate(self.path('settlement'),lambda v:v['editor_window_quote_checks'][0].update(actual_line=99))
        self.blocked('EDITOR_WINDOW_QUOTE')
    def test_manual_fact_source_unchanged(self):
        self.mutate(self.path('settlement'),lambda v:v['manual_fact_checks'][0]['source_value'].update(current_due_installment_yuan=186000))
        self.blocked('MANUAL_FACT_EVIDENCE')
    def test_manual_fact_quote_exists(self):
        self.mutate(self.path('settlement'),lambda v:v['manual_fact_checks'][0].update(quote='不存在的事实引文'))
        self.blocked('MANUAL_FACT_EVIDENCE')

if __name__=='__main__':unittest.main()
