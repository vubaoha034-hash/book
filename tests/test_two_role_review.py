"""Corrupt real role isolation/evidence/budget in temporary copies; no model calls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('two_role_gate',REPO/'scripts/verify_two_role_review.py')
gate = importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


class TwoRoleTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.project=json.loads((REPO/'state/project_state.json').read_bytes())
        self.checkpoint=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route=self.project['two_role_opening_review'];self.seen=set()
        human=json.loads((REPO/self.route['human_feedback']['path']).read_bytes())
        for v in (self.project,self.checkpoint):
            v.pop('autonomous_opening_to_human',None)
            v.update(human_verdict_receipt=self.route['human_feedback']['path'],latest_human_review=human['review'],
                last_completed_task_id=gate.TASK,last_completed_task_contract=self.route['task']['path'],
                next_action=gate.NEXT,next_required_action=gate.NEXT,
                current_human_gate='CURRENT_395_HUMAN_EMOTION_AI_SMELL_INTERACTION_AND_RETENTION_FAIL_OLD_448_FAIL_404_UNKNOWN')
        self.checkpoint.update(sequence=198,stop=True)
        self.copy('START_HERE.md');self.copy_refs(self.route)
        entry=self.root/'START_HERE.md'
        entry.write_bytes(('当前位置：检查点198。\n'+entry.read_text(encoding='utf-8')).encode())
        for key in ('emotion_pacing_learning','r2_entry_short_trial','r2_reentry_fact_preparation'):
            self.copy_refs(self.project[key])
        for role in ('reader','editor'):self.copy(gate.runner.DIRECTORY+f'/{role}.attempt.json')

    def copy(self,path):
        if path in self.seen or not (REPO/path).is_file():return
        self.seen.add(path);dest=self.root/path;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(dest.read_bytes()))

    def copy_refs(self,value):
        if isinstance(value,dict):
            if all(k in value for k in ('path','blob','sha256')):self.copy(value['path'])
            for child in value.values():self.copy_refs(child)
        elif isinstance(value,list):
            for child in value:self.copy_refs(child)

    def read(self,path):return json.loads((self.root/path).read_bytes())

    def write(self,path,value):
        (self.root/path).write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())

    def refresh(self,value):
        if isinstance(value,dict):
            if all(k in value for k in ('path','blob','sha256')):
                p=self.root/value['path']
                if p.is_file():
                    b=p.read_bytes();value.update(blob=gate.blob(b),sha256=hashlib.sha256(b).hexdigest())
            for child in value.values():self.refresh(child)
        elif isinstance(value,list):
            for child in value:self.refresh(child)

    def rebind(self):
        for k in ('authorization','manifest','reader_runtime','editor_runtime','reader_evidence','editor_evidence',
                  'settlement','next_task_proposal','task','result'):
            p=self.route[k]['path'];v=self.read(p);self.refresh(v);self.write(p,v)
        self.refresh(self.route);self.checkpoint['two_role_opening_review']=copy.deepcopy(self.route)

    def mutate(self,key,fn):
        p=self.route[key]['path'];v=self.read(p);fn(v);self.write(p,v);self.rebind()

    def verify(self):return gate.two_role_action(self.root,self.project,self.checkpoint,gate.OLD)

    def blocked(self,pattern):
        with self.assertRaisesRegex(ValueError,pattern):self.verify()

    def test_actual_two_contexts_keep_human_fail_and_zero_budget(self):
        self.assertEqual(self.verify(),gate.NEXT)
        self.assertIs(self.project['latest_human_review']['wants_to_continue'],False)
        self.assertEqual(self.route['generation_budget'],0)

    def test_cannot_skip_past_failure(self):
        with self.assertRaisesRegex(ValueError,'CANNOT_SKIP_HISTORICAL'):
            gate.two_role_action(self.root,self.project,self.checkpoint,'WRITE')

    def test_cold_reader_rejects_known_failure_or_writer_commands(self):
        m=self.read(self.route['manifest']['path']);p=m['jobs']['reader']['packet']['path'];v=self.read(p)
        v['human_feedback']='真人FAIL；只返回正文';self.write(p,v);self.rebind()
        self.blocked('CONTEXT_ALLOWLIST_VIOLATION')

    def test_reader_cannot_receive_editor_report(self):
        m=self.read(self.route['manifest']['path']);p=m['jobs']['reader']['packet']['path'];v=self.read(p)
        v['editor_report']='already diagnosed';self.write(p,v);self.rebind()
        self.blocked('CONTEXT_ALLOWLIST_VIOLATION')

    def test_wrong_body_sha_cannot_rebind_report(self):
        m=self.read(self.route['manifest']['path']);p=m['jobs']['reader']['packet']['path'];v=self.read(p)
        v['samples'][0]['original_sha256']='0'*64;self.write(p,v);self.rebind()
        self.blocked('PACKET_TEXT_HASH_DRIFT|PACKET_OR_SCOPE')

    def test_reader_raw_nonexistent_quote_rejected(self):
        p=self.route['reader_raw']['path'];v=gate.review.parse_report((self.root/p).read_bytes())
        v['reactions'][0]['quote']='原稿不存在的引用';self.write(p,v);self.rebind()
        self.blocked('REPORT_OR_QUOTE')

    def test_reader_yes_cannot_overwrite_actual_human_no(self):
        self.project['latest_human_review']['wants_to_continue']=True
        self.blocked('CURRENT_HUMAN_MIRROR')

    def test_exact_human_stop_cannot_be_invented(self):
        self.mutate('human_feedback',lambda v:v.update(exact_stop_sentence='他把复本转正'))
        self.blocked('ACTUAL_HUMAN_SUPPLEMENT')

    def test_editor_and_reader_cannot_share_thread(self):
        reader=self.read(self.route['reader_runtime']['path'])
        self.mutate('editor_runtime',lambda v:v.update(thread_id=reader['thread_id']))
        self.blocked('SHARED_OR_INHERITED_CONTEXT')

    def test_reader_cannot_inherit_writer_context(self):
        old=self.read(self.project['r2_entry_short_trial']['writer_runtime']['path'])
        self.mutate('reader_runtime',lambda v:v.update(thread_id=old['thread_id']))
        self.blocked('SHARED_OR_INHERITED_CONTEXT')

    def test_model_cannot_be_only_prompt_claim(self):
        self.mutate('reader_runtime',lambda v:v['resolved_thread_settings'].update(model='other'))
        self.blocked('ACTUAL_MODEL_OR_PERMISSION')

    def test_tool_activity_not_independent_toolless_review(self):
        self.mutate('editor_runtime',lambda v:v.update(tool_activity_detected=['commandExecution']))
        self.blocked('NO_COMPLETE_ISOLATED_REPORT')

    def test_missing_raw_is_not_success(self):
        (self.root/self.route['editor_raw']['path']).unlink();self.blocked('MISSING_MATERIAL')

    def test_failed_or_empty_call_is_not_success(self):
        self.mutate('reader_runtime',lambda v:v.update(turn_status='failed',report_received=False,status='BLOCKED'))
        self.blocked('NO_COMPLETE_ISOLATED_REPORT')

    def test_editor_facts_cannot_be_invented_in_settlement(self):
        self.mutate('settlement',lambda v:v['editor_finding_dispositions'][0]['fact_bindings'][0].update(value='invented'))
        self.blocked('EDITOR_FACT_MISREAD')

    def test_review_completion_does_not_reset_prose_budget(self):
        self.mutate('authorization',lambda v:v.update(generation_budget=1,new_prose_authorized=True))
        self.blocked('AUTHORIZATION_OR_SCOPE')

    def test_followup_prepared_not_automatically_active(self):
        self.mutate('next_task_proposal',lambda v:v.update(authorized_generation_budget=1,automatic_activation=True))
        self.blocked('PREPARATION_OR_UNAUTHORIZED_WRITING')

    def test_future_writer_cannot_receive_review_answers(self):
        self.mutate('prepared_input',lambda v:v['writer_packet'].update(human_feedback='刘先生FAIL'))
        self.blocked('FUTURE_WRITER_FAILURE_OR_FACT_LEAKAGE')

    def test_future_writer_facts_cannot_add_life_history(self):
        self.mutate('prepared_input',lambda v:v['writer_packet']['facts'].update(new_history='invented'))
        self.blocked('FUTURE_WRITER_FAILURE_OR_FACT_LEAKAGE')

    def test_no_repeated_calls_until_pass(self):
        self.mutate('manifest',lambda v:v['jobs']['reader'].update(max_calls=2))
        self.blocked('AUTHORIZATION_OR_SCOPE')

    def test_old_calibration_cannot_be_changed_to_quality_success(self):
        self.mutate('settlement',lambda v:v['previous_calibration'].update(false_negatives=0))
        self.blocked('SETTLEMENT_MISSING_OR_OVERCLAIMED')

    def test_original_unknown_and_old_197_lock_remain(self):
        for key in ('original_404_human_result','old_197_character_protection_released'):
            saved=self.route[key];self.route[key]='PASS' if key.startswith('original') else True
            self.checkpoint['two_role_opening_review']=copy.deepcopy(self.route)
            self.blocked('QUALITY_SCOPE_OR_BUDGET|DELIVERABLE_BINDING');self.route[key]=saved
        self.checkpoint['two_role_opening_review']=copy.deepcopy(self.route)


if __name__=='__main__':unittest.main()
