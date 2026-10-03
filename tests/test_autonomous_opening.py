"""Reject real isolation, scope and evidence corruption; never call a model."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('autonomous_gate',REPO/'scripts/verify_autonomous_opening.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


class AutonomousOpeningTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.project=json.loads((REPO/'state/project_state.json').read_bytes())
        self.checkpoint=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route=self.project['autonomous_opening_to_human'];self.seen=set()
        prior_human=self.project['two_role_opening_review']['human_feedback']['path']
        human=json.loads((REPO/prior_human).read_bytes())
        for v in (self.project,self.checkpoint):
            v.pop('opening_prose_repair',None)
            v.update(last_completed_task_id=gate.TASK,last_completed_task_contract=self.route['task']['path'],
                next_action=gate.NEXT,next_required_action=gate.NEXT,human_verdict_receipt=prior_human,latest_human_review=human['review'],
                current_human_gate='NEW_REVIEWED_OPENING_HUMAN_UNKNOWN_PRIOR_395_AND_448_FAIL_404_UNKNOWN')
        self.checkpoint.update(sequence=199,stop=True)
        self.copy('START_HERE.md');self.copy_refs(self.route)
        entry=self.root/'START_HERE.md';entry.write_bytes(('当前位置：检查点199。\n'+entry.read_text(encoding='utf-8')).encode())
        self.copy_refs(self.project['two_role_opening_review'])
        self.copy_refs(self.project['r2_entry_short_trial'])
        for role in ('writer','facts','editor','reader'):
            self.copy(gate.runner.DIRECTORY+f'/a1.{role}.attempt.json')

    def copy(self,path):
        if path in self.seen or not (REPO/path).is_file():return
        self.seen.add(path);p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((REPO/path).read_bytes())
        if path.endswith('.json'):self.copy_refs(json.loads(p.read_bytes()))

    def copy_refs(self,value):
        if isinstance(value,dict):
            if all(k in value for k in ('path','blob','sha256')):self.copy(value['path'])
            for v in value.values():self.copy_refs(v)
        elif isinstance(value,list):
            for v in value:self.copy_refs(v)

    def read(self,path):return json.loads((self.root/path).read_bytes())
    def write(self,path,value):
        (self.root/path).write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())

    def rebind(self):
        done=set()
        def walk(value):
            if isinstance(value,dict):
                if all(k in value for k in ('path','blob','sha256')):
                    path=value['path'];p=self.root/path
                    current=('autonomous-opening-20261003/' in path or 'AUTONOMOUS_' in path or
                             path in ('config/novel-autonomous-opening-20261003.json','rules/autonomy-until-human-review.json'))
                    if p.is_file():
                        if current and path.endswith('.json') and path not in done:
                            done.add(path);v=self.read(path);walk(v);self.write(path,v)
                        b=p.read_bytes();value.update(blob=gate.blob(b),sha256=hashlib.sha256(b).hexdigest())
                for child in value.values():walk(child)
            elif isinstance(value,list):
                for child in value:walk(child)
        walk(self.route);self.checkpoint['autonomous_opening_to_human']=copy.deepcopy(self.route)

    def mutate_path(self,path,fn):
        v=self.read(path);fn(v);self.write(path,v);self.rebind()
    def mutate(self,key,fn):self.mutate_path(self.route[key]['path'],fn)
    def stage_mutate(self,key,fn):self.mutate_path(self.route['stages'][0][key]['path'],fn)
    def packet_path(self,role):
        return self.read(self.route['stages'][0]['review_manifest']['path'])['jobs'][role]['packet']['path']
    def verify(self):return gate.autonomous_action(self.root,self.project,self.checkpoint,gate.OLD)
    def blocked(self,pattern):
        with self.assertRaisesRegex(ValueError,pattern):self.verify()

    def test_actual_four_contexts_stop_only_at_human_unknown(self):
        self.assertEqual(self.verify(),gate.NEXT)
        self.assertEqual(self.route['total_generation_count'],1)
        self.assertEqual(self.route['internal_repair_count'],0)
        self.assertFalse(self.route['intermediate_user_authorization_required'])
        self.assertFalse(self.project['latest_human_review']['wants_to_continue'])

    def test_historical_gates_cannot_be_skipped(self):
        with self.assertRaisesRegex(ValueError,'CANNOT_SKIP_HISTORICAL'):
            gate.autonomous_action(self.root,self.project,self.checkpoint,'WRITE')

    def test_permission_is_actual_user_instruction_not_ai_verdict(self):
        self.mutate('authorization',lambda v:v.update(source='AI_REVIEW_APPROVAL'))
        self.blocked('USER_SCOPE_OR_STANDING')

    def test_no_intermediate_permission_loop(self):
        self.mutate('autonomy_policy',lambda v:v.update(intermediate_user_authorization_required=True))
        self.blocked('ENTRY_PERMISSION_POLICY')

    def test_old_unapproved_proposal_is_preserved(self):
        path=self.read(self.route['authorization']['path'])['authorized_proposal']['path']
        self.mutate_path(path,lambda v:v.update(authorized_generation_budget=1))
        self.blocked('USER_SCOPE_OR_STANDING|OLD_PROPOSAL_REWRITTEN')

    def test_old_rc3_is_not_replenished(self):
        self.route['old_RC3_remaining_rounds']=1;self.checkpoint['autonomous_opening_to_human']=copy.deepcopy(self.route)
        self.blocked('SCOPE_BUDGET_OR_HUMAN')

    def test_old_197_protection_is_not_released(self):
        self.mutate('authorization',lambda v:v.update(old_197_character_protection_released=True))
        self.blocked('USER_SCOPE_OR_STANDING')

    def test_no_full_v5_from_new_permission(self):
        self.mutate('authorization',lambda v:v.update(full_v5_authorized=True))
        self.blocked('USER_SCOPE_OR_STANDING')

    def test_one_primary_no_verdict_retries(self):
        self.mutate('manifest',lambda v:v.update(primary_writer_limit=2))
        self.blocked('MANIFEST_SCOPE')

    def test_writer_cannot_receive_failure_or_diagnosis(self):
        path=self.read(self.route['manifest']['path'])['writer_input']['path']
        self.mutate_path(path,lambda v:v.update(diagnosis='known FAIL'))
        self.blocked('WRITER_CONTEXT')

    def test_cold_reader_cannot_receive_failure(self):
        self.mutate_path(self.packet_path('reader'),lambda v:v.update(human_feedback='known FAIL'))
        self.blocked('CONTEXT_ALLOWLIST')

    def test_cold_reader_cannot_receive_editor_report(self):
        self.mutate_path(self.packet_path('reader'),lambda v:v.update(editor_report='positive answer'))
        self.blocked('CONTEXT_ALLOWLIST')

    def test_editor_cannot_be_told_new_draft_failed(self):
        self.mutate_path(self.packet_path('editor'),lambda v:v.update(boundaries=['刘先生已经FAIL']))
        self.blocked('EDITOR_OLD_FAILURE_OR_ANSWER')

    def test_actual_model_must_be_available_and_resolved(self):
        self.stage_mutate('reader_runtime',lambda v:v['resolved_thread_settings'].update(model='other'))
        self.blocked('ACTUAL_MODEL_OR_ISOLATION')

    def test_actual_max_not_just_prompt_name(self):
        self.stage_mutate('editor_runtime',lambda v:v['resolved_thread_settings'].update(reasoningEffort='low'))
        self.blocked('ACTUAL_MODEL_OR_ISOLATION')

    def test_reviewer_cannot_use_tools_or_write(self):
        self.stage_mutate('facts_runtime',lambda v:v.update(tool_activity_detected=['commandExecution']))
        self.blocked('NO_COMPLETE_ISOLATED_CALL')

    def test_reader_cannot_share_writer_context(self):
        thread=self.read(self.route['primary_runtime']['path'])['thread_id']
        self.stage_mutate('reader_runtime',lambda v:v.update(thread_id=thread))
        self.blocked('SHARED_OR_INHERITED_CONTEXT')

    def test_failed_call_is_not_a_report(self):
        self.stage_mutate('facts_runtime',lambda v:v.update(turn_status='failed'))
        self.blocked('NO_COMPLETE_ISOLATED_CALL')

    def test_missing_report_cannot_pass(self):
        (self.root/self.route['stages'][0]['editor_raw']['path']).unlink()
        self.blocked('MISSING_MATERIAL')

    def test_report_bound_to_wrong_body_rejected(self):
        self.mutate_path(self.packet_path('reader'),lambda v:v['samples'][0].update(original_sha256='0'*64))
        self.blocked('PACKET_TEXT_HASH_DRIFT')

    def test_nonexistent_quote_does_not_enter_result(self):
        self.stage_mutate('facts_raw',lambda v:v['results'][0]['findings'][0].update(quote='不存在的引文'))
        self.blocked('REPORT_OR_QUOTE_EVIDENCE')

    def test_material_insufficiency_cannot_be_clear(self):
        self.stage_mutate('facts_raw',lambda v:v['results'][0].update(verdict='INSUFFICIENT'))
        self.blocked('REPORT_OR_QUOTE_EVIDENCE|FINAL_FACTS_NOT_CLEAR')

    def test_ai_yes_does_not_supply_human_pass(self):
        self.mutate('pending_human_review',lambda v:v.update(outcome='PASS',accepted=True))
        self.blocked('SETTLEMENT_OR_UNKNOWN_HUMAN')

    def test_ai_yes_does_not_trigger_more_generation(self):
        self.mutate('settlement',lambda v:v.update(reader_vote_triggers_more_generation=True))
        self.blocked('SETTLEMENT_OR_UNKNOWN_HUMAN')

    def test_unknown_exact_human_stop_cannot_be_invented(self):
        self.mutate('pending_human_review',lambda v:v.update(exact_stop_sentence='某一句'))
        self.blocked('SETTLEMENT_OR_UNKNOWN_HUMAN')

    def test_coordinator_cannot_rewrite_raw_report(self):
        self.mutate('settlement',lambda v:v.update(raw_reports_rewritten=True))
        self.blocked('SETTLEMENT_OR_UNKNOWN_HUMAN')

    def test_all_finding_ids_settled_once(self):
        self.mutate('settlement',lambda v:v['report_dispositions'].__setitem__(1,copy.deepcopy(v['report_dispositions'][0])))
        self.blocked('FINDING_NOT_SETTLED')

    def test_frozen_fact_binding_not_invented(self):
        self.mutate('settlement',lambda v:v['text_fact_checks'][0]['fact_bindings'][0].update(value='替换事实'))
        self.blocked('FACT_BINDING')

    def test_window_quote_location_verified(self):
        self.mutate('settlement',lambda v:v['editor_window_quote_checks'][0].update(actual_line=99))
        self.blocked('EDITOR_WINDOW_QUOTE')

    def test_original_404_does_not_gain_a_human_outcome(self):
        self.route['original_404_human_result']='FAIL';self.checkpoint['autonomous_opening_to_human']=copy.deepcopy(self.route)
        self.blocked('SCOPE_BUDGET_OR_HUMAN')

    def test_live_cursor_must_point_to_actual_reading(self):
        self.project['next_action']='ASK_ANOTHER_PERMISSION'
        self.blocked('LIVE_CURSOR')


if __name__=='__main__':unittest.main()
