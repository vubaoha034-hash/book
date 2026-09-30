"""Prepare and validate the scoped novel-state fix without committing or pushing.

Default is dry-run. --apply writes only the three specified files in a clean,
exact-version local checkout. Original story and receipt bytes stay unchanged.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

SOURCE_HEAD = '9c6079d16be04f54f636f1cac47b56c892053226'
EXPECTED = {
    'state/project_state.json': 'f2af481a4bfca65e35c4e7ca324e375ec19703cd',
    'state/continuity/LATEST_CHECKPOINT.json': 'e85a40759fa671926bb1067f29f2fdeac47ac0e1',
    'scripts/verify_current_state.py': '7b19e9836e69dc517607da3a6e05d91767d63428',
}
EVENT = 'actual_human_opening_trial_verdict_20260930'
MODULE = Path(__file__).with_name('verify_current_state.py')
spec = importlib.util.spec_from_file_location('new_verify', MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def project_changes(project, checkpoint):
    project, checkpoint = copy.deepcopy(project), copy.deepcopy(checkpoint)
    event = project[EVENT]
    if event != checkpoint.get(EVENT) or not event['verdict'].startswith(('FAIL', 'REJECT')):
        raise ValueError('CURRENT_HUMAN_EVENT_MISSING_OR_CONFLICTED')
    p = project['phase422_state']['opening_trial']
    q = checkpoint['phase422_state']['opening_trial']
    if p.get('path') != q.get('path') or p.get('blob') != q.get('blob'):
        raise ValueError('TRIAL_IDENTITY_CONFLICT')
    if event.get('artifact') != p.get('path') or event.get('artifact_blob') != p.get('blob'):
        raise ValueError('EVENT_DOES_NOT_BIND_CURRENT_TRIAL')
    for state in (project, checkpoint):
        trial = state['phase422_state']['opening_trial']
        trial['human_style_verdict'] = event['verdict']
        trial['human_exact_feedback'] = event['human_exact_feedback']
        trial['human_verdict_event_key'] = EVENT
        trial['final_quality_accepted'] = False
        state['opening_trial_human_gate'] = 'CLOSED_HUMAN_REJECTED'
        state['next_action'] = state['next_required_action']
    checkpoint['sequence'] = int(checkpoint['sequence']) + 1
    checkpoint['action_guard']['project_state_sha256'] = hashlib.sha256(encoded(project)).hexdigest()
    return project, checkpoint

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', type=Path)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve()
    head = subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if head != SOURCE_HEAD:
        raise ValueError('HEAD_CHANGED: do not apply to a newer revision without reconciliation')
    if subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip():
        raise ValueError('WORKTREE_NOT_CLEAN')
    originals = {}
    for rel, sha in EXPECTED.items():
        data = (root / rel).read_bytes()
        if mod.git_blob(data) != sha:
            raise ValueError('SOURCE_BLOB_MISMATCH: ' + rel)
        originals[rel] = data
    project, cp = project_changes(json.loads(originals['state/project_state.json']), json.loads(originals['state/continuity/LATEST_CHECKPOINT.json']))
    candidate = {'state/project_state.json': encoded(project), 'state/continuity/LATEST_CHECKPOINT.json': encoded(cp), 'scripts/verify_current_state.py': MODULE.read_bytes()}
    protected = [mod.RECEIPT, project['phase422_state']['opening_trial']['path']]
    protected_bytes = {rel: mod.safe_file(root, rel).read_bytes() for rel in protected}
    with tempfile.TemporaryDirectory() as td:
        staged = Path(td)
        for rel, data in {**protected_bytes, **candidate}.items():
            path = staged / rel; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        result = mod.verify(staged)
    if args.apply:
        for rel, data in originals.items():
            if (root / rel).read_bytes() != data:
                raise ValueError('CONCURRENT_LOCAL_CHANGE: ' + rel)
        try:
            for rel, data in candidate.items():
                (root / rel).write_bytes(data)
            mod.verify(root)
            if any((root / rel).read_bytes() != data for rel, data in protected_bytes.items()):
                raise ValueError('PROTECTED_CONTENT_CHANGED')
        except Exception:
            for rel, data in originals.items():
                (root / rel).write_bytes(data)
            raise
    print(json.dumps({'applied': args.apply, 'source_head': head, 'changed_files': list(candidate),
                      'protected_files_unchanged': protected, 'verification': result,
                      'commit_or_push_performed': False}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
