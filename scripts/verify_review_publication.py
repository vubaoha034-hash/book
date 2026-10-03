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
LEARNING_SOURCE = '7997b03fb3a0ec5eaf8e0e5b55f91cd651094fde'
LEARNING_PREFIX = 'state/review_receipts/NOVEL_EMOTION_PACING_LEARNING_'
LEARNING_NEW_FILES = (
    'config/novel-emotion-learning-20261003.json',
    'delivery/emotion-learning-20261003/diagnosis.packet.json',
    'delivery/emotion-learning-20261003/craft-capsule.json',
    'docs/NOVEL_EMOTION_PACING_PROFESSIONAL_STUDY_20261003.md',
    'docs/NOVEL_EMOTION_REACTION_DIAGNOSIS_RESULT_20261003.md',
    'modules/emotion-reaction-and-pacing.md',
    'scripts/novel_emotion_diagnosis.py', 'scripts/verify_emotion_learning.py',
    'tests/test_emotion_learning.py',
    'state/learning/emotion-pacing-20261003/sources.json',
    'state/reviews/emotion-learning-20261003/diagnosis.attempt.json',
    'state/reviews/emotion-learning-20261003/diagnosis.runtime.json',
    'state/reviews/emotion-learning-20261003/diagnosis.raw.txt',
    'state/reviews/emotion-learning-20261003/diagnosis.evidence.json',
    'state/reviews/emotion-learning-20261003/coordinator-settlement.json',
    'state/tasks/NOVEL_EMOTION_PACING_LEARNING_20261003.json',
    'state/tasks/NOVEL_EMOTION_REACTION_ONE_SHORT_PROPOSAL_20261003.json',
    'state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_FAIL_20261003.json',
    LEARNING_PREFIX + 'AUTHORIZATION_20261003.json',
    LEARNING_PREFIX + 'RESULT_20261003.json',
    LEARNING_PREFIX + 'VALIDATION_20261003.json',
    LEARNING_PREFIX + 'REMOTE_SAVE_VERIFIED_20261003.json')
LEARNING_MUTABLE_FILES = PREPARATION_MUTABLE_FILES + (
    'scripts/verify_one_short_trial.py', 'tests/test_one_short_trial.py')
TWO_ROLE_SOURCE = 'f1283b8b4daaf3ded67a42de7784dca3f3e09603'
TWO_ROLE_PREFIX = 'state/review_receipts/NOVEL_TWO_ROLE_REVIEW_'
TWO_ROLE_NEW_FILES = (
    'config/novel-two-role-review-20261003.json',
    'delivery/two-role-opening-20261003/reader.packet.json',
    'delivery/two-role-opening-20261003/editor.packet.json',
    'delivery/two-role-opening-20261003/prepared-opening-input.json',
    'docs/NOVEL_TWO_ROLE_OPENING_REVIEW_RESULT_20261003.md',
    'modules/review-roles/reader-policy.md', 'modules/review-roles/editor-policy.md',
    'modules/two-role-opening-review.md',
    'scripts/novel_two_role_review.py', 'scripts/verify_two_role_review.py',
    'tests/test_two_role_review.py',
    'state/learning/two-role-opening-20261003/sources.json',
    'state/reviews/two-role-opening-20261003/reader.attempt.json',
    'state/reviews/two-role-opening-20261003/reader.runtime.json',
    'state/reviews/two-role-opening-20261003/reader.raw.txt',
    'state/reviews/two-role-opening-20261003/reader.evidence.json',
    'state/reviews/two-role-opening-20261003/editor.attempt.json',
    'state/reviews/two-role-opening-20261003/editor.runtime.json',
    'state/reviews/two-role-opening-20261003/editor.raw.txt',
    'state/reviews/two-role-opening-20261003/editor.evidence.json',
    'state/reviews/two-role-opening-20261003/coordinator-settlement.json',
    'state/tasks/NOVEL_TWO_ROLE_OPENING_REVIEW_20261003.json',
    'state/tasks/NOVEL_REVIEWED_OPENING_ONE_SHORT_PROPOSAL_20261003.json',
    'state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_RETENTION_SUPPLEMENT_20261003.json',
    TWO_ROLE_PREFIX+'AUTHORIZATION_20261003.json',
    TWO_ROLE_PREFIX+'RESULT_20261003.json',
    TWO_ROLE_PREFIX+'VALIDATION_20261003.json',
    TWO_ROLE_PREFIX+'REMOTE_SAVE_VERIFIED_20261003.json')
TWO_ROLE_MUTABLE_FILES = PREPARATION_MUTABLE_FILES + (
    'scripts/verify_emotion_learning.py','tests/test_emotion_learning.py','tests/test_one_short_trial.py')
AUTONOMOUS_SOURCE = '0e38c4fa02e4bddd0dba96711241bd678d92da68'
AUTONOMOUS_PREFIX = 'state/review_receipts/NOVEL_AUTONOMOUS_TO_HUMAN_'
AUTONOMOUS_MUTABLE_FILES = PREPARATION_MUTABLE_FILES + (
    'scripts/codex_review.py','scripts/verify_emotion_learning.py',
    'scripts/verify_two_role_review.py','tests/test_two_role_review.py')
AUTONOMOUS_NEW_FILES = (
    'config/novel-autonomous-opening-20261003.json',
    'rules/autonomy-until-human-review.json',
    'modules/autonomous-to-human-review.md',
    'modules/review-roles/new-draft-editor-policy.md',
    'scripts/novel_autonomous_opening.py','scripts/verify_autonomous_opening.py',
    'tests/test_autonomous_opening.py',
    'docs/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_RESULT_20261003.md',
    'state/tasks/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_20261003.json',
    AUTONOMOUS_PREFIX+'AUTHORIZATION_20261003.json',
    AUTONOMOUS_PREFIX+'RESULT_20261003.json',
    AUTONOMOUS_PREFIX+'VALIDATION_20261003.json',
    AUTONOMOUS_PREFIX+'REMOTE_SAVE_VERIFIED_20261003.json',
    'state/authoring/autonomous-opening-20261003/coordinator-settlement.json',
    'state/authoring/autonomous-opening-20261003/pending-human-review.json',
    'delivery/autonomous-opening-20261003/a1.md',
    'delivery/autonomous-opening-20261003/a1.writer-input.json',
    'delivery/autonomous-opening-20261003/writer-policy.txt',
    'delivery/autonomous-opening-20261003/a1.review-manifest.json',
    *(f'delivery/autonomous-opening-20261003/a1.{role}.packet.json' for role in ('facts','editor','reader')),
    *(f'state/authoring/autonomous-opening-20261003/a1.{role}.{suffix}'
      for role in ('writer','facts','editor','reader') for suffix in ('attempt.json','runtime.json')),
    *(f'state/authoring/autonomous-opening-20261003/a1.{role}.{suffix}'
      for role in ('facts','editor','reader') for suffix in ('raw.txt','evidence.json')))
PROSE_SOURCE='df1e08a59373e9777bf478b85ebe0707c4dfdef0'
PROSE_PREFIX='state/review_receipts/NOVEL_OPENING_PROSE_REPAIR_'
PROSE_MUTABLE_FILES=PREPARATION_MUTABLE_FILES+(
    'scripts/verify_autonomous_opening.py','scripts/verify_two_role_review.py',
    'tests/test_autonomous_opening.py','tests/test_two_role_review.py')
PROSE_NEW_FILES=(
    'scripts/novel_prose_repair.py','scripts/verify_prose_repair.py','tests/test_prose_repair.py',
    'config/novel-prose-repair-20261003.json',
    'state/learning/prose-repair-20261003/sources.json',
    'docs/NOVEL_OPENING_PROSE_REPAIR_RESULT_20261003.md',
    'state/tasks/NOVEL_OPENING_PROSE_REPAIR_AFTER_HUMAN_FAIL_20261003.json',
    'state/review_receipts/NOVEL_AUTONOMOUS_OPENING_390_HUMAN_FAIL_20261003.json',
    *(PROSE_PREFIX+k+'_20261003.json' for k in ('AUTHORIZATION','RESULT','VALIDATION','REMOTE_SAVE_VERIFIED')),
    'delivery/prose-repair-20261003/short-a1.md',
    'delivery/prose-repair-20261003/writer-input.json',
    'delivery/prose-repair-20261003/input-change-record.json',
    *(f'delivery/prose-repair-20261003/{role}-policy.txt' for role in ('diagnosis','writer','facts','editor','reader')),
    *(f'delivery/prose-repair-20261003/{role}.packet.json' for role in ('diagnosis','facts','editor','reader')),
    *(f'state/reviews/prose-repair-20261003/{role}.{suffix}' for role in ('diagnosis','writer','facts','editor','reader') for suffix in ('attempt.json','runtime.json')),
    *(f'state/reviews/prose-repair-20261003/{role}.{suffix}' for role in ('diagnosis','facts','editor','reader') for suffix in ('raw.txt','evidence.json')),
    'state/reviews/prose-repair-20261003/diagnosis-settlement.json',
    'state/reviews/prose-repair-20261003/coordinator-settlement.json',
    'state/reviews/prose-repair-20261003/pending-human-review.json')


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


def verify_emotion_learning(expected):
    """Read checkpoint197 bytes and retain every prior frozen artifact."""
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    if remote != expected:
        raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch', 'origin', 'main')
    if git('rev-parse', 'origin/main').decode().strip() != remote:
        raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', remote)))
    base = zipfile.ZipFile(io.BytesIO(git('archive', '--format=zip', LEARNING_SOURCE)))
    old_files = {p for p in base.namelist() if not p.endswith('/')}
    new_files = {p for p in archive.namelist() if not p.endswith('/')}
    if new_files - old_files - set(LEARNING_NEW_FILES) or old_files - new_files:
        raise ValueError('LEARNING_UNEXPECTED_REMOTE_ADDITION_OR_DELETION')
    protected = old_files - set(LEARNING_MUTABLE_FILES)
    for path in protected:
        if archive.read(path) != base.read(path):
            raise ValueError('LEARNING_HISTORICAL_BYTES_CHANGED: ' + path)
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
        if path in seen: return
        seen.add(path)
        checked.append({'path': path, 'blob': blob(data), 'sha256': digest})
        # Prior receipts are immutable snapshots and leaves; their historical
        # mutable-file hashes are not claims about checkpoint197.
        if path in LEARNING_NEW_FILES and path.endswith('.json'):
            walk(json.loads(data))

    def walk(value):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'blob', 'sha256')):
                inspect(value['path'], value)
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)

    project = json.loads(archive.read('state/project_state.json'))
    checkpoint = json.loads(archive.read('state/continuity/LATEST_CHECKPOINT.json'))
    route = project.get('emotion_pacing_learning')
    if (not route or route != checkpoint.get('emotion_pacing_learning') or
            route.get('human_quality_result') != 'FAIL' or route.get('generation_count') != 0 or
            route.get('generation_budget') != 0 or checkpoint.get('sequence') != 197 or
            checkpoint.get('stop') is not True or checkpoint.get('action_guard', {}).get('project_state_sha256') !=
            hashlib.sha256(archive.read('state/project_state.json')).hexdigest()):
        raise ValueError('REMOTE_LEARNING_STATE_OR_CHECKPOINT_DRIFT')
    walk(route)
    for path in (*LEARNING_MUTABLE_FILES, *LEARNING_NEW_FILES):
        if path == LEARNING_NEW_FILES[-1] and path not in new_files:
            continue  # Actual readback proof precedes saving that receipt.
        inspect(path)
    validation = json.loads(archive.read(LEARNING_PREFIX + 'VALIDATION_20261003.json'))
    if validation.get('status') != 'SCOPED_LEARNING_VALIDATION_PASSED_NO_PROSE':
        raise ValueError('REMOTE_LEARNING_VALIDATION_NOT_COMPLETED')
    import importlib.util
    spec = importlib.util.spec_from_file_location('published_learning_state', ROOT / 'scripts/verify_current_state.py')
    current = importlib.util.module_from_spec(spec); spec.loader.exec_module(current)
    state_result = current.verify(ROOT)
    if state_result.get('sequence') != 197 or state_result.get('new_prose_authorized') is not False:
        raise ValueError('REMOTE_LEARNING_BUSINESS_GATE_NOT_CLOSED')
    if git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] != remote:
        raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status': 'REMOTE_LEARNING_BYTES_HISTORY_AND_BUSINESS_GATES_VERIFIED',
        'remote_head': remote, 'source_head': LEARNING_SOURCE, 'checkpoint': 197,
        'checked_count': len(checked), 'files': checked, 'protected_source_file_count': len(protected),
        'all_prior_prose_locks_and_raw_reports_unchanged': True, 'current_state': state_result,
        'model_calls_during_readback': 0, 'generation_count_during_readback': 0}


def verify_two_roles(expected):
    """Actual remote bytes, current evidence graph and all prior frozen history."""
    remote = git('ls-remote','origin','refs/heads/main').decode().split()[0]
    if remote != expected: raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch','origin','main')
    if git('rev-parse','origin/main').decode().strip() != remote: raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive = zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',remote)))
    base = zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',TWO_ROLE_SOURCE)))
    old = {p for p in base.namelist() if not p.endswith('/')}
    new = {p for p in archive.namelist() if not p.endswith('/')}
    if new-old-set(TWO_ROLE_NEW_FILES) or old-new:
        raise ValueError('TWO_ROLE_UNEXPECTED_REMOTE_ADDITION_OR_DELETION')
    protected = old-set(TWO_ROLE_MUTABLE_FILES)
    for path in protected:
        if archive.read(path) != base.read(path): raise ValueError('TWO_ROLE_HISTORICAL_BYTES_CHANGED: '+path)
    seen,checked=set(),[]

    def inspect(path,reference=None):
        resolved=(ROOT/path).resolve()
        if not resolved.is_relative_to(ROOT.resolve()): raise ValueError('REMOTE_REFERENCE_OUTSIDE_REPOSITORY')
        data=archive.read(path)
        if data != resolved.read_bytes(): raise ValueError('REMOTE_LOCAL_BYTES_DIFFER: '+path)
        digest=hashlib.sha256(data).hexdigest()
        if reference and (reference.get('blob') != blob(data) or reference.get('sha256') != digest):
            raise ValueError('REMOTE_REFERENCE_IDENTITY_DRIFT: '+path)
        if path in seen:return
        seen.add(path);checked.append({'path':path,'blob':blob(data),'sha256':digest})
        # Existing receipts stay historical leaves, never rewritten to match
        # today's mutable entrance/state. Follow only this task's new graph.
        if path in TWO_ROLE_NEW_FILES and path.endswith('.json'):walk(json.loads(data))

    def walk(value):
        if isinstance(value,dict):
            if all(k in value for k in ('path','blob','sha256')):inspect(value['path'],value)
            for child in value.values():walk(child)
        elif isinstance(value,list):
            for child in value:walk(child)

    project=json.loads(archive.read('state/project_state.json'))
    cp=json.loads(archive.read('state/continuity/LATEST_CHECKPOINT.json'))
    route=project.get('two_role_opening_review')
    if (not route or route != cp.get('two_role_opening_review') or cp.get('sequence') != 198 or cp.get('stop') is not True or
            route.get('generation_budget') != 0 or route.get('generation_count') != 0 or route.get('human_quality_result') != 'FAIL' or
            cp.get('action_guard',{}).get('project_state_sha256') != hashlib.sha256(archive.read('state/project_state.json')).hexdigest()):
        raise ValueError('REMOTE_TWO_ROLE_STATE_OR_CHECKPOINT_DRIFT')
    walk(route)
    for path in (*TWO_ROLE_MUTABLE_FILES,*TWO_ROLE_NEW_FILES):
        if path == TWO_ROLE_NEW_FILES[-1] and path not in new:continue
        inspect(path)
    validation=json.loads(archive.read(TWO_ROLE_PREFIX+'VALIDATION_20261003.json'))
    if validation.get('status') != 'TWO_ROLE_SCOPE_AND_EVIDENCE_VALIDATION_PASSED_NO_PROSE':
        raise ValueError('REMOTE_TWO_ROLE_VALIDATION_NOT_COMPLETED')
    import importlib.util
    spec=importlib.util.spec_from_file_location('published_two_role_state',ROOT/'scripts/verify_current_state.py')
    current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current)
    state_result=current.verify(ROOT)
    if state_result.get('sequence') != 198 or state_result.get('new_prose_authorized') is not False:
        raise ValueError('REMOTE_TWO_ROLE_BUSINESS_GATE_NOT_CLOSED')
    if git('ls-remote','origin','refs/heads/main').decode().split()[0] != remote:raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status':'REMOTE_TWO_ROLE_BYTES_HISTORY_AND_BUSINESS_GATES_VERIFIED',
        'remote_head':remote,'source_head':TWO_ROLE_SOURCE,'checkpoint':198,'checked_count':len(checked),'files':checked,
        'protected_source_file_count':len(protected),'all_prior_prose_locks_feedback_and_raw_reports_unchanged':True,
        'current_state':state_result,'model_calls_during_readback':0,'generation_count_during_readback':0}


def verify_autonomous(expected):
    """Actual CP199 readback; never infer human acceptance or run a model."""
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    if remote!=expected:raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch','origin','main')
    if git('rev-parse','origin/main').decode().strip()!=remote:raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive=zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',remote)))
    base=zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',AUTONOMOUS_SOURCE)))
    old={p for p in base.namelist() if not p.endswith('/')};new={p for p in archive.namelist() if not p.endswith('/')}
    if new-old-set(AUTONOMOUS_NEW_FILES) or old-new:raise ValueError('AUTONOMOUS_UNEXPECTED_REMOTE_ADDITION_OR_DELETION')
    protected=old-set(AUTONOMOUS_MUTABLE_FILES)
    for path in protected:
        if archive.read(path)!=base.read(path):raise ValueError('AUTONOMOUS_HISTORICAL_BYTES_CHANGED: '+path)
    seen,checked=set(),[]

    def inspect(path,reference=None):
        local=(ROOT/path).resolve()
        if not local.is_relative_to(ROOT.resolve()):raise ValueError('REMOTE_REFERENCE_OUTSIDE_REPOSITORY')
        data=archive.read(path);digest=hashlib.sha256(data).hexdigest()
        if data!=local.read_bytes():raise ValueError('REMOTE_LOCAL_BYTES_DIFFER: '+path)
        if reference and (reference.get('blob')!=blob(data) or reference.get('sha256')!=digest):
            raise ValueError('REMOTE_REFERENCE_IDENTITY_DRIFT: '+path)
        if path in seen:return
        seen.add(path);checked.append({'path':path,'blob':blob(data),'sha256':digest})
        if path in AUTONOMOUS_NEW_FILES and path.endswith('.json'):walk(json.loads(data))

    def walk(value):
        if isinstance(value,dict):
            if all(k in value for k in ('path','blob','sha256')):inspect(value['path'],value)
            for child in value.values():walk(child)
        elif isinstance(value,list):
            for child in value:walk(child)

    project=json.loads(archive.read('state/project_state.json'));cp=json.loads(archive.read('state/continuity/LATEST_CHECKPOINT.json'))
    route=project.get('autonomous_opening_to_human')
    if (not route or route!=cp.get('autonomous_opening_to_human') or cp.get('sequence')!=199 or cp.get('stop') is not True or
            route.get('primary_generation_count')!=1 or route.get('internal_repair_count')!=0 or
            route.get('human_quality_result')!='UNKNOWN' or route.get('literary_quality_validated') is not False or
            cp.get('action_guard',{}).get('project_state_sha256')!=hashlib.sha256(archive.read('state/project_state.json')).hexdigest()):
        raise ValueError('REMOTE_AUTONOMOUS_STATE_OR_CHECKPOINT_DRIFT')
    walk(route)
    for path in (*AUTONOMOUS_MUTABLE_FILES,*AUTONOMOUS_NEW_FILES):
        if path==AUTONOMOUS_PREFIX+'REMOTE_SAVE_VERIFIED_20261003.json' and path not in new:continue
        inspect(path)
    validation=json.loads(archive.read(AUTONOMOUS_PREFIX+'VALIDATION_20261003.json'))
    if validation.get('status')!='AUTONOMOUS_TO_HUMAN_SCOPE_EVIDENCE_AND_HISTORY_VALIDATION_PASSED':
        raise ValueError('REMOTE_AUTONOMOUS_VALIDATION_NOT_COMPLETED')
    import importlib.util
    spec=importlib.util.spec_from_file_location('published_autonomous_state',ROOT/'scripts/verify_current_state.py')
    current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current)
    state_result=current.verify(ROOT)
    if state_result.get('sequence')!=199 or state_result.get('next_action')!='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_REVIEWED_NEW_OPENING':
        raise ValueError('REMOTE_AUTONOMOUS_BUSINESS_GATE_NOT_CLOSED')
    if git('ls-remote','origin','refs/heads/main').decode().split()[0]!=remote:raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status':'REMOTE_AUTONOMOUS_BYTES_HISTORY_AND_HUMAN_GATE_VERIFIED',
        'remote_head':remote,'source_head':AUTONOMOUS_SOURCE,'checkpoint':199,'checked_count':len(checked),'files':checked,
        'protected_source_file_count':len(protected),'all_prior_prose_locks_feedback_and_raw_reports_unchanged':True,
        'current_state':state_result,'human_quality_result':'UNKNOWN',
        'model_calls_during_readback':0,'generation_count_during_readback':0}


def verify_prose_repair(expected):
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    if remote!=expected:raise ValueError('REMOTE_MAIN_CHANGED_RECONCILE_BEFORE_WRITING')
    git('fetch','origin','main')
    if git('rev-parse','origin/main').decode().strip()!=remote:raise ValueError('REMOTE_CHANGED_DURING_READBACK')
    archive=zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',remote)))
    base=zipfile.ZipFile(io.BytesIO(git('archive','--format=zip',PROSE_SOURCE)))
    old={p for p in base.namelist() if not p.endswith('/')};new={p for p in archive.namelist() if not p.endswith('/')}
    if new-old-set(PROSE_NEW_FILES) or old-new:raise ValueError('PROSE_UNEXPECTED_REMOTE_ADDITION_OR_DELETION')
    protected=old-set(PROSE_MUTABLE_FILES)
    for path in protected:
        if archive.read(path)!=base.read(path):raise ValueError('PROSE_HISTORICAL_BYTES_CHANGED: '+path)
    seen,checked=set(),[]
    def inspect(path,reference=None):
        local=(ROOT/path).resolve()
        if not local.is_relative_to(ROOT.resolve()):raise ValueError('REMOTE_REFERENCE_OUTSIDE_REPOSITORY')
        b=archive.read(path)
        if b!=local.read_bytes():raise ValueError('REMOTE_LOCAL_BYTES_DIFFER: '+path)
        digest=hashlib.sha256(b).hexdigest()
        if reference and (reference.get('blob')!=blob(b) or reference.get('sha256')!=digest):raise ValueError('REMOTE_REFERENCE_IDENTITY_DRIFT: '+path)
        if path in seen:return
        seen.add(path);checked.append({'path':path,'blob':blob(b),'sha256':digest})
        if path in PROSE_NEW_FILES and path.endswith('.json'):walk(json.loads(b))
    def walk(v):
        if isinstance(v,dict):
            if all(k in v for k in ('path','blob','sha256')):inspect(v['path'],v)
            for child in v.values():walk(child)
        elif isinstance(v,list):
            for child in v:walk(child)
    project=json.loads(archive.read('state/project_state.json'));cp=json.loads(archive.read('state/continuity/LATEST_CHECKPOINT.json'))
    route=project.get('opening_prose_repair')
    if not route or route!=cp.get('opening_prose_repair') or cp.get('sequence')!=200 or cp.get('stop') is not True or route.get('human_quality_result')!='UNKNOWN':
        raise ValueError('REMOTE_PROSE_STATE_DRIFT')
    if cp.get('action_guard',{}).get('project_state_sha256')!=hashlib.sha256(archive.read('state/project_state.json')).hexdigest():raise ValueError('REMOTE_PROSE_PROJECT_HASH_DRIFT')
    walk(route)
    for path in (*PROSE_MUTABLE_FILES,*PROSE_NEW_FILES):
        if path==PROSE_PREFIX+'REMOTE_SAVE_VERIFIED_20261003.json' and path not in new:continue
        inspect(path)
    if json.loads(archive.read(PROSE_PREFIX+'VALIDATION_20261003.json')).get('status')!='PROSE_REPAIR_SCOPE_EVIDENCE_AND_HISTORY_VALIDATION_PASSED':
        raise ValueError('REMOTE_PROSE_VALIDATION_NOT_COMPLETED')
    import importlib.util
    spec=importlib.util.spec_from_file_location('published_prose_state',ROOT/'scripts/verify_current_state.py')
    current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current);state=current.verify(ROOT)
    if state.get('sequence')!=200 or state.get('next_action')!='AWAIT_ACTUAL_HUMAN_READING_OF_ONE_PROSE_REPAIRED_OPENING':raise ValueError('REMOTE_PROSE_HUMAN_GATE_DRIFT')
    if git('ls-remote','origin','refs/heads/main').decode().split()[0]!=remote:raise ValueError('REMOTE_ADVANCED_DURING_VERIFICATION')
    return {'status':'REMOTE_PROSE_BYTES_HISTORY_AND_ACTUAL_HUMAN_GATE_VERIFIED','remote_head':remote,'source_head':PROSE_SOURCE,
        'checkpoint':200,'checked_count':len(checked),'files':checked,'protected_source_file_count':len(protected),
        'all_prior_prose_reports_receipts_and_locks_unchanged':True,'current_state':state,'human_quality_result':'UNKNOWN',
        'model_calls_during_readback':0,'generation_count_during_readback':0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-head', required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--preparation', action='store_true', help='Verify checkpoint195 preparation and preserve all checkpoint194 history')
    mode.add_argument('--short-trial', action='store_true', help='Verify checkpoint196 frozen short and preserve all checkpoint195 history')
    mode.add_argument('--emotion-learning', action='store_true', help='Verify checkpoint197 actual failure and learning; preserve checkpoint196 history')
    mode.add_argument('--two-roles', action='store_true', help='Verify checkpoint198 independent editor/reader reviews and preserve checkpoint197 history')
    mode.add_argument('--autonomous-opening', action='store_true', help='Verify checkpoint199 final short, independent reviews and actual human UNKNOWN')
    mode.add_argument('--prose-repair', action='store_true', help='Verify checkpoint200 actual prose rejection and new reviewed short')
    args = parser.parse_args()
    try:
        result = (verify_prose_repair(args.expected_head) if args.prose_repair else
                  verify_autonomous(args.expected_head) if args.autonomous_opening else
                  verify_two_roles(args.expected_head) if args.two_roles else
                  verify_emotion_learning(args.expected_head) if args.emotion_learning else
                  verify_short_trial(args.expected_head) if args.short_trial else
                  verify_preparation(args.expected_head) if args.preparation else verify(args.expected_head))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'REMOTE_READBACK_NOT_CONFIRMED', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
