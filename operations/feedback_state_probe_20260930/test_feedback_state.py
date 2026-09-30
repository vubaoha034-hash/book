"""Synthetic state-transition tests. These are not literary/visual blind tests."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from verify_current_state import verify, git_blob, RECEIPT, EVENT
from prepare_patch import project_changes, encoded

class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.story = '测试正文。此处仅是工程夹具，不是用户作品。\n'.encode()
        self.artifact = 'delivery/phase422/07-opening-scene-trial-after-v4.md'
        self.receipt = {'project_id':'novel-distillation','status':'V4-only historical rejection',
                        'actual_human_style_verdict_20260929':{'verdict':'FAIL_SEVERE_AI_SMELL'}}
        self.put(self.artifact,self.story)
        self.put(RECEIPT,encoded(self.receipt))
        self.event = {'verdict':'FAIL_EMOTIONLESS_ROBOTIC_DIALOGUE','human_exact_feedback':'合成测试反馈：无情感。',
                      'artifact':self.artifact,'artifact_blob':git_blob(self.story),
                      'final_quality_accepted':False,'same_trial_must_not_be_resubmitted':True,
                      'automatic_full_v5_authorized':False}
        phase = {'opening_trial':{'path':self.artifact,'blob':git_blob(self.story),'human_style_verdict':'PENDING'},
                 'receipt':{'blob':git_blob(encoded(self.receipt))},'repair_basis':{'scope':'local only'},
                 'same_v4_resubmission_allowed':False,'automatic_v5_allowed':False,'final_pass':False}
        common = {'project_id':'novel-distillation','status':'current trial rejected',
                  'next_required_action':'STOP_CURRENT_TRIAL','next_action':'OLD_WAIT',
                  'human_verdict_receipt':RECEIPT,'phase422_state':phase,
                  EVENT:self.event,'opening_trial_human_gate':'PENDING_ACTUAL_HUMAN_READING'}
        p = copy.deepcopy(common)
        p['phase363_prose_anchor'] = {'mechanism_only_scale_proven_sufficient':False}
        p['phase370_settlement'] = {'ai_smell_direction_vs_phase369':'SAME'}
        c = copy.deepcopy(common)
        c.update(sequence=137,active_task_ids=[],action_guard={'project_state_sha256':'stale'})
        self.before_p,self.before_c = copy.deepcopy(p),copy.deepcopy(c)
        self.p,self.c = project_changes(p,c)
        self.flush()
    def put(self,rel,data):
        path=self.root/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    def flush(self):
        self.c['action_guard']['project_state_sha256']=hashlib.sha256(encoded(self.p)).hexdigest()
        self.put('state/project_state.json',encoded(self.p))
        self.put('state/continuity/LATEST_CHECKPOINT.json',encoded(self.c))
    def rejected(self):
        with self.assertRaises((ValueError,KeyError)): verify(self.root)
    def test_valid_rejection_and_historical_status_can_differ(self):
        result=verify(self.root)
        self.assertFalse(result['literary_quality_tested'])
        self.assertGreaterEqual(result['checks_passed'],20)
    def test_stale_pending_inside_current_trial_is_blocked(self):
        self.p['phase422_state']['opening_trial']['human_style_verdict']='PENDING';self.flush();self.rejected()
    def test_wrong_artifact_identity_is_blocked(self):
        self.p[EVENT]['artifact']='delivery/some-other-version.md';self.c[EVENT]=copy.deepcopy(self.p[EVENT]);self.flush();self.rejected()
    def test_changed_story_bytes_are_blocked(self):
        self.put(self.artifact,self.story+b'Changed');self.rejected()
    def test_missing_story_is_blocked(self):
        (self.root/self.artifact).unlink();self.rejected()
    def test_machine_quality_flag_cannot_override_human_rejection(self):
        self.p[EVENT]['final_quality_accepted']=True;self.c[EVENT]=copy.deepcopy(self.p[EVENT]);self.flush();self.rejected()
    def test_local_signal_cannot_be_promoted_to_full_quality(self):
        self.p['phase363_prose_anchor']['mechanism_only_scale_proven_sufficient']=True;self.flush();self.rejected()
    def test_stale_project_digest_is_blocked(self):
        self.c['action_guard']['project_state_sha256']='0'*64
        self.put('state/continuity/LATEST_CHECKPOINT.json',encoded(self.c));self.rejected()
    def test_stale_next_action_is_blocked(self):
        self.c['next_action']='AWAIT_OLD_TRIAL_REVIEW';self.flush();self.rejected()
    def test_source_dicts_and_original_receipt_story_are_unchanged(self):
        p,c=copy.deepcopy(self.before_p),copy.deepcopy(self.before_c)
        project_changes(p,c)
        self.assertEqual(p,self.before_p);self.assertEqual(c,self.before_c)
        self.assertEqual((self.root/self.artifact).read_bytes(),self.story)
        self.assertEqual((self.root/RECEIPT).read_bytes(),encoded(self.receipt))
    def test_path_cannot_escape_repository(self):
        self.p['phase422_state']['opening_trial']['path']='../../outside.md'
        self.flush();self.rejected()

if __name__=='__main__':unittest.main(verbosity=2)
