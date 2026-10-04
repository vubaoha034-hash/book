"""Regression checks for the human correction gate, not for literary quality."""
from pathlib import Path
import copy,hashlib,importlib.util,json,shutil,tempfile,unittest
REPO=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('correction_gate',REPO/'scripts/verify_scoped_text_correction.py');gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)
class CorrectionGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='novel-lexical-test-');self.root=Path(self.temp.name)
        shutil.copytree(REPO,self.root,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','__pycache__','.pytest_cache'))
        self.p=json.loads((self.root/'state/project_state.json').read_bytes());self.c=json.loads((self.root/'state/continuity/LATEST_CHECKPOINT.json').read_bytes())
    def tearDown(self):self.temp.cleanup()
    def save_state(self):
        data=(json.dumps(self.p,ensure_ascii=False,indent=2)+'\n').encode();(self.root/'state/project_state.json').write_bytes(data)
        self.c['action_guard']['project_state_sha256']=hashlib.sha256(data).hexdigest()
    def blocked(self,pattern):
        self.save_state()
        with self.assertRaisesRegex(ValueError,pattern):gate.verify(self.root,self.p,self.c)
    def test_valid_correction_is_not_quality_pass(self):
        r=gate.verify(self.root,self.p,self.c);self.assertEqual(r['checks_passed'],93);self.assertFalse(r['new_prose_authorized']);self.assertEqual(r['human_quality_result'],'UNKNOWN')
    def test_no_new_writer_budget(self):
        for v in(self.p,self.c):v['scoped_text_correction']['remaining_repair_budget']=1
        self.blocked('LEXICAL_BUDGET_OR_FALSE_PASS')
    def test_no_human_pass_from_relative_praise(self):
        for v in(self.p,self.c):v['latest_human_review']['wants_to_continue']='YES'
        self.blocked('LEXICAL_CURRENT_ENTRY_DRIFT')
    def test_old_state_cannot_change(self):
        self.p['mainline_state']['new_prose_authorized_now']=True
        self.blocked('LEXICAL_HISTORICAL_STATE_DRIFT')
    def test_original_body_cannot_change(self):
        path=self.root/self.p['scoped_text_correction']['source_artifact']['path'];path.write_bytes(path.read_bytes()+b'\n')
        self.blocked('LEXICAL_HISTORICAL_FILE_CHANGED')
    def test_corrected_body_binding_cannot_drift(self):
        path=self.root/self.p['scoped_text_correction']['final_artifact']['path'];path.write_bytes(path.read_bytes()+b'\n')
        self.blocked('PROSE_IDENTITY_DRIFT')
    def test_no_claim_of_new_independent_review(self):
        for v in(self.p,self.c):v['scoped_text_correction']['independent_review_of_corrected_version']=True
        self.blocked('LEXICAL_BUDGET_OR_FALSE_PASS')
    def test_checkpoint_hash_must_match(self):
        self.c['action_guard']['project_state_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'LEXICAL_CHECKPOINT_OR_HASH_DRIFT'):gate.verify(self.root,self.p,self.c)
if __name__=='__main__':unittest.main()
