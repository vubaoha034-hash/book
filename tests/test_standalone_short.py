from pathlib import Path
import copy,hashlib,importlib.util,unittest
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('standalone_checks',ROOT/'scripts/novel_standalone_short.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class StandaloneShortEvidenceTests(unittest.TestCase):
    def fixture(self):
        return dict(self_evaluation=dict(dimensions=[dict(id=k,score=1.8,quote='原文',line=1,reason='具体依据')for k in('opening','clarity_language','emotion','causality','payoff')],total=9),open_major_or_blocker=[],quote_or_fact_errors=[],line_pass_complete=True,complete_story=True,current_reports={k:dict(path=k)for k in('editor','reader','copyeditor')},all_current_reports_successful_and_bound=True,human_score='UNKNOWN',human_quality_result='UNKNOWN',AI_quality_certification=False)
    def test_internal_nine_keeps_human_unknown(self):self.assertEqual(m.validate_self9(self.fixture()),9)
    def test_low_score_cannot_release(self):
        v=self.fixture();v['self_evaluation']['dimensions'][0]['score']=1.5;v['self_evaluation']['total']=8.7
        with self.assertRaisesRegex(ValueError,'THRESHOLD'):m.validate_self9(v)
    def test_missing_report_is_not_pass(self):
        v=self.fixture();del v['current_reports']['reader']
        with self.assertRaisesRegex(ValueError,'REPORTS'):m.validate_self9(v)
    def test_open_major_is_not_pass(self):
        v=self.fixture();v['open_major_or_blocker']=['causal contradiction']
        with self.assertRaisesRegex(ValueError,'OPEN_PROBLEMS'):m.validate_self9(v)
    def test_self9_cannot_set_human9(self):
        v=self.fixture();v['human_score']=9
        with self.assertRaisesRegex(ValueError,'FALSE_HUMAN'):m.validate_self9(v)
    def test_language_pass_is_required(self):
        v=self.fixture();v['line_pass_complete']=False
        with self.assertRaisesRegex(ValueError,'OPEN_PROBLEMS'):m.validate_self9(v)
    def test_scores_need_quotes(self):
        v=self.fixture();v['self_evaluation']['dimensions'][2]['quote']=''
        with self.assertRaisesRegex(ValueError,'EVIDENCE'):m.validate_self9(v)
    def test_cold_packet_cannot_include_score_or_facts(self):
        text='匿名完整正文';packet=dict(packet_version='codex-review-packet/v1',job_id='C',work_kind='COLD_SCREEN',medium='中文手机',excerpt_position='完整短篇',samples=[dict(artifact_id='A',original_sha256=hashlib.sha256(text.encode()).hexdigest(),text=text)],facts=dict(score=9))
        with self.assertRaisesRegex(ValueError,'ALLOWLIST'):m.review.validate_packet(packet)
    def reader_fixture(self):
        text='甲。乙。丙。';sample=dict(artifact_id='A',original_sha256=hashlib.sha256(text.encode()).hexdigest(),text=text)
        packet=dict(packet_version='codex-review-packet/v1',job_id='C',work_kind='COLD_SCREEN',medium='中文手机',excerpt_position='完整短篇',samples=[sample])
        runtime=dict(report_received=True,turn_status='completed',resolved_thread_settings=dict(model='gpt-6.1-sol',reasoningEffort='high'),isolation=m.engine.ISOLATION)
        report=dict(job_id='C',work_kind='COLD_SCREEN',runtime_context=dict(model='gpt-6.1-sol',reasoning_effort='high',isolation=m.engine.ISOLATION),artifact_id='A',original_sha256=sample['original_sha256'],scope=m.REPORT_SCOPE,reader_profile='单一AI',wants_to_continue='YES',ending_response=dict(quote='丙。',line=1),reading_expectations=dict(first=dict(quote='甲。',line=1),second=dict(quote='乙。',line=1)),unknowns=['无真人评分'])
        return packet,report,runtime
    def test_actual_high_context_is_not_claimed_as_max(self):
        p,r,rt=self.reader_fixture();self.assertEqual(m.audit(p,r,rt)['errors'],[])
        r['runtime_context']['reasoning_effort']='max';self.assertIn('REPORT_CONTEXT_OR_JOB_DRIFT',m.audit(p,r,rt)['errors'])
    def test_failed_runtime_cannot_release_report(self):
        p,r,rt=self.reader_fixture();rt.update(report_received=False,turn_status='failed')
        self.assertIn('NO_COMPLETED_REPORT',m.audit(p,r,rt)['errors'])
    def test_invented_quote_rejected(self):
        p,r,rt=self.reader_fixture();r['ending_response']['quote']='不存在'
        self.assertIn('NONEXISTENT_QUOTE',m.audit(p,r,rt)['errors'])
    def test_report_bound_to_wrong_body_is_rejected(self):
        p,r,rt=self.reader_fixture();r['original_sha256']='0'*64
        self.assertIn('WRONG_ARTIFACT_OR_SCOPE',m.audit(p,r,rt)['errors'])
if __name__=='__main__':unittest.main()
