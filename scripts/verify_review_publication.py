"""Read actual remote main bytes; no model call, state edit, or Git push."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = 'state/review_receipts/NOVEL_CODEX_REVIEW_INTEGRATION_AND_R2_DIAGNOSIS_RESULT_20261003.json'
SOURCE = '122739a8c6f0ffa47ee77726865c06f8cb2c566a'


def git(*args):
    return subprocess.check_output(['git', '-c', 'http.sslBackend=openssl', *args], cwd=ROOT)


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def verify(expected):
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    if remote != expected:
        raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch', 'origin', 'main')
    if git('rev-parse', 'origin/main').decode().strip() != remote:
        raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', remote)))
    base = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', SOURCE)))
    seen, checked = set(), []

    def inspect(path, reference=None):
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to(ROOT.resolve()):
            raise ValueError('REMOTE_REFERENCE_OUTSIDE_REPOSITORY')
        data = archive.read(path)
        local = resolved.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if data != local:
            raise ValueError('REMOTE_LOCAL_BYTES_DIFFER: ' + path)
        if reference and (reference.get('blob') != blob(data) or reference.get('sha256') != digest):
            raise ValueError('REMOTE_REFERENCE_IDENTITY_DRIFT: ' + path)
        if path in seen:
            return
        seen.add(path)
        checked.append({'path': path, 'blob': blob(data), 'sha256': digest})
        # Follow this run's reference graph. Historical receipts are leaves:
        # their prior snapshots may refer to mutable files at older commits.
        # Active historical business gates run in verify_current_state.py.
        run_record = (path.startswith(('state/reviews/codex-20261003/', 'delivery/codex-review-20261003/')) or
            path in (RECEIPT, 'config/codex-review-run-20261003.json',
                'state/tasks/NOVEL_CODEX_REVIEW_INTEGRATION_AND_R2_DIAGNOSIS_20261003.json',
                'state/tasks/NOVEL_R2_REENTRY_FACT_PREPARATION_PROPOSAL_20261003.json',
                'state/review_receipts/NOVEL_CODEX_REVIEW_VALIDATION_20261003.json',
                'state/review_receipts/NOVEL_CODEX_REVIEW_REMOTE_SAVE_VERIFIED_20261003.json')))
        if path.endswith('.json') and run_record:
            walk(json.loads(data))

    def walk(value):
        if isinstance(value, dict):
            if all(key in value for key in ('path', 'blob', 'sha256')):
                inspect(value['path'], value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    inspect(RECEIPT)
    for path in ('.gitattributes', 'START_HERE.md', 'AGENTS.md', 'SKILL.md', 'README.md',
                 'scripts/codex_review.py', 'scripts/verify_codex_review.py',
                 'scripts/verify_current_state.py', 'scripts/verify_review_publication.py',
                 'state/review_receipts/NOVEL_CODEX_REVIEW_VALIDATION_20261003.json',
                 'state/project_state.json', 'state/continuity/LATEST_CHECKPOINT.json'):
        inspect(path)
    publication = 'state/review_receipts/NOVEL_CODEX_REVIEW_REMOTE_SAVE_VERIFIED_20261003.json'
    if publication in archive.namelist():
        inspect(publication)
    protected = ('MAINLINE.md', 'delivery/local-revision-rc3-r2/short-r2-a1.md',
        'delivery/r2-emotion-retention-diagnosis/reviewer-input.md',
        'state/tasks/NOVEL_R2_EMOTION_RETENTION_DIAGNOSIS_PREP_20261002.json',
        'state/review_receipts/NOVEL_R2_EMOTION_RETENTION_DIAGNOSIS_PRE_SEND_BLOCKED_20261003.json',
        'state/review_receipts/NOVEL_RC3_R2_HUMAN_RETENTION_FAIL_20261002.json',
        'state/tasks/NOVEL_IMPROVEMENT_MAINLINE_V4.json',
        'state/review_receipts/NOVEL_MAINLINE_V4_LOCK_20261001.json')
    for path in protected:
        if archive.read(path) != base.read(path):
            raise ValueError('HISTORICAL_PROTECTED_BYTES_CHANGED: ' + path)
    # Finish with a fresh remote read so a concurrent push is visible.
    if git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] != remote:
        raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status': 'REMOTE_MAIN_BYTES_AND_REFERENCES_VERIFIED', 'remote_head': remote,
            'source_head': SOURCE, 'checked_count': len(checked), 'files': checked,
            'protected_originals_unchanged': list(protected), 'model_calls': 0, 'generation_count': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-head', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.expected_head), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'REMOTE_READBACK_NOT_CONFIRMED', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
