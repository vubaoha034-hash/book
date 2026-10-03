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
PREPARATION_SOURCE = 'fcc71ed5425a9479bde55db6d560114fa4c793a0'
PREPARATION_NEW_FILES = (
    'delivery/r2-reentry-facts-20261003/writer-context.json',
    'delivery/r2-reentry-facts-20261003/preparation-evidence.json',
    'docs/NOVEL_R2_REENTRY_FACT_PREPARATION_RESULT_20261003.md',
    'scripts/verify_reentry_preparation.py', 'tests/test_reentry_preparation.py',
    'state/tasks/NOVEL_R2_REENTRY_FACT_PREPARATION_20261003.json',
    'state/tasks/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_PROPOSAL_20261003.json',
    'state/review_receipts/NOVEL_R2_REENTRY_FACT_PREPARATION_AUTHORIZATION_20261003.json',
    'state/review_receipts/NOVEL_R2_REENTRY_FACT_PREPARATION_RESULT_20261003.json',
    'state/review_receipts/NOVEL_R2_REENTRY_FACT_PREPARATION_VALIDATION_20261003.json',
    'state/review_receipts/NOVEL_R2_REENTRY_FACT_PREPARATION_REMOTE_SAVE_VERIFIED_20261003.json')
PREPARATION_MUTABLE_FILES = (
    'START_HERE.md', 'README.md', 'AGENTS.md', 'SKILL.md',
    'scripts/verify_current_state.py', 'scripts/verify_review_publication.py',
    'tests/test_current_state.py', 'state/project_state.json',
    'state/continuity/LATEST_CHECKPOINT.json')
SHORT_TRIAL_SOURCE = 'b1d1bbc16ea8b37f3886e9aa932ecfea3287d3e4'
SHORT_TRIAL_PREFIX = 'state/review_receipts/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_'
SHORT_TRIAL_NEW_FILES = (
    'config/novel-r2-entry-trial-20261003.json',
    'delivery/r2-entry-trial-20261003/writer-input.json',
    'delivery/r2-entry-trial-20261003/short-a1.md',
    'delivery/r2-entry-trial-20261003/facts.packet.json',
    'docs/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_RESULT_20261003.md',
    'scripts/novel_one_short_trial.py', 'scripts/verify_one_short_trial.py',
    'tests/test_one_short_trial.py',
    'state/authoring/r2-entry-trial-20261003/writer.attempt.json',
    'state/authoring/r2-entry-trial-20261003/writer.runtime.json',
    'state/reviews/r2-entry-trial-20261003/facts.attempt.json',
    'state/reviews/r2-entry-trial-20261003/facts.runtime.json',
    'state/reviews/r2-entry-trial-20261003/facts.raw.txt',
    'state/reviews/r2-entry-trial-20261003/facts.evidence.json',
    'state/reviews/r2-entry-trial-20261003/coordinator-settlement.json',
    'state/tasks/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_20261003.json',
    SHORT_TRIAL_PREFIX + 'AUTHORIZATION_20261003.json',
    SHORT_TRIAL_PREFIX + 'RESULT_20261003.json',
    SHORT_TRIAL_PREFIX + 'VALIDATION_20261003.json',
    SHORT_TRIAL_PREFIX + 'REMOTE_SAVE_VERIFIED_20261003.json')
SHORT_TRIAL_MUTABLE_FILES = PREPARATION_MUTABLE_FILES + (
    'scripts/verify_reentry_preparation.py', 'tests/test_reentry_preparation.py')


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
                'state/review_receipts/NOVEL_CODEX_REVIEW_REMOTE_SAVE_VERIFIED_20261003.json'))
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


def verify_preparation(expected):
    """Check the new scope; older readback receipts remain frozen snapshots."""
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    if remote != expected:
        raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch', 'origin', 'main')
    if git('rev-parse', 'origin/main').decode().strip() != remote:
        raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', remote)))
    base = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', PREPARATION_SOURCE)))
    old_files = {p for p in base.namelist() if not p.endswith('/')}
    new_files = {p for p in archive.namelist() if not p.endswith('/')}
    allowed_mutations = set(PREPARATION_MUTABLE_FILES)
    if new_files - old_files - set(PREPARATION_NEW_FILES) or old_files - new_files:
        raise ValueError('PREPARATION_UNEXPECTED_REMOTE_ADDITION_OR_DELETION')
    protected = old_files - allowed_mutations
    for path in protected:
        if archive.read(path) != base.read(path):
            raise ValueError('PREPARATION_HISTORICAL_BYTES_CHANGED: ' + path)
    seen, checked = set(), []

    def inspect(path, reference=None):
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to(ROOT.resolve()):
            raise ValueError('REMOTE_REFERENCE_OUTSIDE_REPOSITORY')
        data = archive.read(path)
        if data != resolved.read_bytes():
            raise ValueError('REMOTE_LOCAL_BYTES_DIFFER: ' + path)
        digest = hashlib.sha256(data).hexdigest()
        if reference and (reference.get('blob') != blob(data) or reference.get('sha256') != digest):
            raise ValueError('REMOTE_REFERENCE_IDENTITY_DRIFT: ' + path)
        if path in seen:
            return
        seen.add(path)
        checked.append({'path': path, 'blob': blob(data), 'sha256': digest})
        if path in PREPARATION_NEW_FILES and path.endswith('.json'):
            walk(json.loads(data))

    def walk(value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')):
                inspect(value['path'], value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    project = json.loads(archive.read('state/project_state.json'))
    checkpoint = json.loads(archive.read('state/continuity/LATEST_CHECKPOINT.json'))
    route = project.get('r2_reentry_fact_preparation')
    if (not route or route != checkpoint.get('r2_reentry_fact_preparation') or
            checkpoint.get('sequence') != 195 or checkpoint.get('stop') is not True or
            checkpoint.get('action_guard', {}).get('project_state_sha256') !=
            hashlib.sha256(archive.read('state/project_state.json')).hexdigest()):
        raise ValueError('REMOTE_PREPARATION_STATE_OR_CHECKPOINT_DRIFT')
    walk(route)
    for path in (*PREPARATION_MUTABLE_FILES, *PREPARATION_NEW_FILES):
        if path == PREPARATION_NEW_FILES[-1] and path not in new_files:
            continue  # The readback receipt is saved after implementation proof.
        inspect(path)
    validation = json.loads(archive.read(PREPARATION_NEW_FILES[-2]))
    if validation.get('status') != 'SCOPED_PREPARATION_VALIDATION_PASSED_NO_PROSE':
        raise ValueError('REMOTE_PREPARATION_VALIDATION_NOT_COMPLETED')
    if git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] != remote:
        raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status': 'REMOTE_PREPARATION_BYTES_AND_HISTORY_VERIFIED', 'remote_head': remote,
            'source_head': PREPARATION_SOURCE, 'checkpoint': 195, 'checked_count': len(checked),
            'files': checked, 'protected_source_file_count': len(protected),
            'all_prior_prose_and_raw_reports_unchanged': True, 'model_calls': 0, 'generation_count': 0}


def verify_short_trial(expected):
    """Verify actual checkpoint196 bytes and protect the entire source history."""
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    if remote != expected:
        raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch', 'origin', 'main')
    if git('rev-parse', 'origin/main').decode().strip() != remote:
        raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', remote)))
    base = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', SHORT_TRIAL_SOURCE)))
    old_files = {p for p in base.namelist() if not p.endswith('/')}
    new_files = {p for p in archive.namelist() if not p.endswith('/')}
    if new_files - old_files - set(SHORT_TRIAL_NEW_FILES) or old_files - new_files:
        raise ValueError('SHORT_TRIAL_UNEXPECTED_REMOTE_ADDITION_OR_DELETION')
    protected = old_files - set(SHORT_TRIAL_MUTABLE_FILES)
    for path in protected:
        if archive.read(path) != base.read(path):
            raise ValueError('SHORT_TRIAL_HISTORICAL_BYTES_CHANGED: ' + path)
    seen, checked = set(), []

    def inspect(path, reference=None):
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to(ROOT.resolve()):
            raise ValueError('REMOTE_REFERENCE_OUTSIDE_REPOSITORY')
        data = archive.read(path)
        if data != resolved.read_bytes():
            raise ValueError('REMOTE_LOCAL_BYTES_DIFFER: ' + path)
        digest = hashlib.sha256(data).hexdigest()
        if reference and (reference.get('blob') != blob(data) or reference.get('sha256') != digest):
            raise ValueError('REMOTE_REFERENCE_IDENTITY_DRIFT: ' + path)
        if path in seen:
            return
        seen.add(path)
        checked.append({'path': path, 'blob': blob(data), 'sha256': digest})
        # Older receipts are snapshots and leaves. Current business gates
        # independently validate their preserved facts, feedback and budgets.
        if path in SHORT_TRIAL_NEW_FILES and path.endswith('.json'):
            walk(json.loads(data))

    def walk(value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')):
                inspect(value['path'], value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    project = json.loads(archive.read('state/project_state.json'))
    checkpoint = json.loads(archive.read('state/continuity/LATEST_CHECKPOINT.json'))
    route = project.get('r2_entry_short_trial')
    if (not route or route != checkpoint.get('r2_entry_short_trial') or
            route.get('human_quality_result') != 'UNKNOWN' or route.get('generation_count') != 1 or
            route.get('remaining_new_generation_budget') != 0 or checkpoint.get('sequence') != 196 or
            checkpoint.get('stop') is not True or checkpoint.get('action_guard', {}).get('project_state_sha256') !=
            hashlib.sha256(archive.read('state/project_state.json')).hexdigest()):
        raise ValueError('REMOTE_SHORT_TRIAL_STATE_OR_CHECKPOINT_DRIFT')
    walk(route)
    for path in (*SHORT_TRIAL_MUTABLE_FILES, *SHORT_TRIAL_NEW_FILES):
        if path == SHORT_TRIAL_NEW_FILES[-1] and path not in new_files:
            continue  # Save actual readback receipt after implementation proof.
        inspect(path)
    validation = json.loads(archive.read(SHORT_TRIAL_PREFIX + 'VALIDATION_20261003.json'))
    if validation.get('status') != 'SCOPED_ONE_SHORT_TRIAL_VALIDATION_PASSED':
        raise ValueError('REMOTE_SHORT_TRIAL_VALIDATION_NOT_COMPLETED')
    # Reuse all historical and current business checks after byte equivalence.
    import importlib.util
    spec = importlib.util.spec_from_file_location('current_short_state', ROOT / 'scripts/verify_current_state.py')
    current = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(current)
    state_result = current.verify(ROOT)
    if state_result.get('sequence') != 196 or state_result.get('new_prose_authorized') is not False:
        raise ValueError('REMOTE_SHORT_TRIAL_BUSINESS_GATE_NOT_CLOSED')
    if git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] != remote:
        raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status': 'REMOTE_ONE_SHORT_TRIAL_BYTES_HISTORY_AND_BUSINESS_GATES_VERIFIED',
            'remote_head': remote, 'source_head': SHORT_TRIAL_SOURCE, 'checkpoint': 196,
            'checked_count': len(checked), 'files': checked, 'protected_source_file_count': len(protected),
            'all_prior_prose_locks_and_raw_reports_unchanged': True, 'current_state': state_result,
            'model_calls_during_readback': 0, 'generation_count_during_readback': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-head', required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--preparation', action='store_true', help='Verify checkpoint195 preparation and preserve all checkpoint194 history')
    mode.add_argument('--short-trial', action='store_true', help='Verify checkpoint196 frozen short and preserve all checkpoint195 history')
    args = parser.parse_args()
    try:
        result = (verify_short_trial(args.expected_head) if args.short_trial else
                  verify_preparation(args.expected_head) if args.preparation else verify(args.expected_head))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'REMOTE_READBACK_NOT_CONFIRMED', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
