"""Reuse corruption checks for the new scoped route without model calls."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
def module(name,path):
    s=importlib.util.spec_from_file_location(name,REPO/path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
gate=module('hook_test_gate','scripts/verify_hook_trial.py')
fixture=module('hook_reusable_fixture','tests/test_prose_repair.py');fixture.gate=gate

class HookTrialTests(fixture.ProseRepairTests):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.seen=set()
        self.project=json.loads((REPO/'state/project_state.json').read_bytes())
        self.cp=json.loads((REPO/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
        self.route=self.project['opening_hook_trial']
        if 'hook_trial_human_feedback' in self.project:
            self.project,self.cp,_=gate.human_feedback_view(REPO,self.project,self.cp)
            self.route=self.project['opening_hook_trial']
        self.copy_refs(self.route);self.copy_refs(self.project['opening_prose_repair']);self.copy('START_HERE.md')
        entry=self.root/'START_HERE.md'
        if '当前位置：检查点201。' not in entry.read_text(encoding='utf-8'):
            entry.write_bytes(('当前位置：检查点201。\n'+entry.read_text(encoding='utf-8')).encode())
        for role in ('diagnosis','writer','facts','editor','reader'):
            self.copy(gate.runner.DIRECTORY+f'/{role}.attempt.json')
        self.copy(gate.runner.DIRECTORY+'/transport-recovery/diagnosis.attempt.json')
        for role in ('writer','facts'):
            self.copy(gate.runner.DIRECTORY+f'/repair/{role}.attempt.json')
    def rebind(self):
        done=set()
        def refresh(v):
            if isinstance(v,dict):
                if all(k in v for k in ('path','blob','sha256')):
                    path=v['path'];p=self.root/path
                    if p.is_file():
                        current=('hook-trial-20261003/' in path or 'HOOK_' in path or 'PROSE_REPAIR_375_HUMAN' in path or path in (gate.runner.MANIFEST,'config/novel-hook-repair-20261003.json'))
                        if current and path.endswith('.json') and path not in done:
                            done.add(path);j=self.read(path);refresh(j);self.write(path,j)
                        b=p.read_bytes();v.update(blob=gate.blob(b),sha256=__import__('hashlib').sha256(b).hexdigest())
                for child in v.values():refresh(child)
            elif isinstance(v,list):
                for child in v:refresh(child)
        refresh(self.route);self.cp['opening_hook_trial']=copy.deepcopy(self.route)
    def test_ai_smell_relative_improvement_not_pass(self):
        self.mutate(self.path('human_feedback'),lambda v:v['review'].update(ai_smell_verdict='PASS'))
        self.blocked('HUMAN_SCOPE_OR_STOP')
    def test_transport_failure_is_not_a_report(self):
        m=self.read(self.path('manifest'));recovery=self.read(m['transport_failure']['path'])
        self.mutate(recovery['failed_runtime']['path'],lambda v:v.update(report_received=True))
        self.blocked('TRANSPORT_FAILURE_NOT_A_QUALITY_RETRY')
    def test_human_failed_375_but_new_body_unknown(self):
        self.assertEqual(self.verify(),gate.NEXT)
        self.assertEqual(self.route['previous_375_human_result'],'FAIL')
        self.assertEqual(self.route['human_quality_result'],'UNKNOWN')
    def test_factual_repair_cannot_change_other_words(self):
        path=self.path('final_artifact');p=self.root/path
        p.write_bytes(p.read_bytes().replace('矮桌'.encode(),'长桌'.encode()))
        self.rebind();self.blocked('REPAIR_SCOPE_OR_RAW_IDENTITY')
    def test_quality_vote_cannot_trigger_factual_repair(self):
        rm=self.read(self.route['repair']['manifest']['path'])
        self.mutate(rm['repair_plan']['path'],lambda v:v.update(quality_vote_did_not_trigger_repair=False))
        self.blocked('REPAIR_SCOPE_OR_RAW_IDENTITY')
    def test_reader_report_stays_on_actual_initial_body(self):
        self.route['raw_reports']['reader']=copy.deepcopy(self.project['opening_prose_repair']['raw_reports']['reader'])
        result=self.read(self.path('result'));result['raw_reports']['reader']=copy.deepcopy(self.route['raw_reports']['reader'])
        self.write(self.path('result'),result)
        self.rebind();self.blocked('RAW_BINDING')
    def test_final_fact_findings_need_coordinator_settlement(self):
        self.mutate(self.path('settlement'),lambda v:v.update(final_fact_finding_dispositions=[]))
        self.blocked('FINAL_FACT_FINDING_NOT_SETTLED')

if __name__=='__main__':unittest.main()
