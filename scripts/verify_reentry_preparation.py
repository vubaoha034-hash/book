"""Scoped preparation gate, called only after every historical business gate."""
from __future__ import annotations

import hashlib
import json

TASK = 'NOVEL-R2-REENTRY-FACT-PREPARATION-20261003-01'
SOURCE = 'fcc71ed5425a9479bde55db6d560114fa4c793a0'
OLD_ACTION = 'AWAIT_LIU_AUTHORIZATION_OF_ONE_BOUNDED_R2_REENTRY_FACT_PREPARATION_TASK_NO_PROSE'
NEXT_ACTION = 'AWAIT_LIU_AUTHORIZATION_OF_ONE_NEW_300_500_CHAR_R2_ENTRY_TRIAL_WITH_OPENING_SCOPE'
SCOPE = 'ONE_SECOND_SCENE_REENTRY_AND_MINIMAL_FACT_PREPARATION_ONLY'
CONTEXT_SHA256 = '0fd229b688a68812b9c23f1f226ef12dce7829b93f198a3300f723052fd8d5da'
PREFIX_SHA256 = '4118de6e79177af5a528dfaae2c415c3650aeb26df5c73ed42b31df7a2c9aa8f'
TARGET_BLOB = 'f0545b15cf01dd6de83e105003e3af34b22cf4db'


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def bound(root, reference, as_json=True):
    path = (root / reference.get('path', '')).resolve()
    if not reference.get('path') or not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('REENTRY_MISSING_MATERIAL')
    data = path.read_bytes()
    if reference.get('blob') != blob(data) or reference.get('sha256') != hashlib.sha256(data).hexdigest():
        raise ValueError('REENTRY_IDENTITY_DRIFT')
    return json.loads(data) if as_json else data


def pointer(value, path):
    for key in path.lstrip('/').split('/'):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def reentry_preparation_action(root, project, checkpoint, historical_action):
    route = project.get('r2_reentry_fact_preparation')
    if route is None and checkpoint.get('r2_reentry_fact_preparation') is None:
        return historical_action
    if not route or route != checkpoint.get('r2_reentry_fact_preparation'):
        raise ValueError('REENTRY_STATE_DRIFT')
    if historical_action != OLD_ACTION:
        raise ValueError('REENTRY_CANNOT_SKIP_HISTORICAL_GATES')
    auth = bound(root, route['authorization'])
    task = bound(root, route['task'])
    receipt = bound(root, route['result'])
    evidence = bound(root, route['evidence'])
    proposal = bound(root, route['next_task_proposal'])
    original = bound(root, auth['authorized_proposal'])
    target = bound(root, receipt['target'], False)
    for item in (auth, task, receipt, evidence, route):
        if (item.get('task_id') != TASK or item.get('source_head') != SOURCE or
                item.get('scope', item.get('authorized_scope')) != SCOPE or
                item.get('new_prose_authorized') is not False or item.get('generation_count') != 0 or
                item.get('new_life_facts_authorized') is not False or item.get('old_RC3_remaining_rounds') != 0 or
                item.get('old_197_character_protection_released') is not False):
            raise ValueError('REENTRY_SCOPE_OR_BUDGET_PROMOTION')
    if (auth.get('authority', {}).get('source') != 'ACTUAL_USER_INSTRUCTION' or
            auth.get('authority', {}).get('exact_user_instruction') != '授权。' or
            auth.get('source_checkpoint') != 194 or auth.get('generation_budget') != 0 or
            original.get('status') != 'PROPOSED_NOT_AUTHORIZED' or
            original.get('task_id') != 'NOVEL-R2-REENTRY-FACT-PREPARATION-PROPOSED-20261003-01' or
            original.get('scope') != SCOPE or task.get('authorization') != route['authorization'] or
            receipt.get('authorization') != route['authorization']):
        raise ValueError('REENTRY_AUTHORIZATION_NOT_BOUND_TO_PREPARATION')
    if (any(v.get('status', v.get('outcome')) != 'COMPLETE_PREPARATION_NO_PROSE' for v in (task, receipt, route)) or
            any(v.get('next_action') != NEXT_ACTION for v in (task, receipt, evidence, route, proposal)) or
            any(v.get('full_v5_authorized') is not False for v in (auth, task, receipt, route, proposal)) or
            route.get('generation_budget') != 0 or task.get('generation_budget') != 0 or
            route.get('automatic_writer_dispatch') is not False or
            receipt.get('review_model_calls_this_task') != 0 or receipt.get('independent_review_this_task') is not False or
            receipt.get('literary_effect_retested') is not False or receipt.get('human_emotion_retention') != 'FAIL' or
            receipt.get('original_404_human_result') != 'UNKNOWN'):
        raise ValueError('REENTRY_COMPLETION_OR_QUALITY_PROMOTION')
    if (receipt.get('evidence') != route['evidence'] or task.get('evidence') != route['evidence'] or
            receipt.get('writer_context') != route['writer_context'] or evidence.get('writer_context') != route['writer_context'] or
            task.get('writer_context') != route['writer_context'] or proposal.get('writer_context') != route['writer_context'] or
            receipt.get('next_task_proposal') != route['next_task_proposal'] or
            task.get('next_task_proposal') != route['next_task_proposal'] or task.get('result') != route['result'] or
            proposal.get('preparation_evidence') != route['evidence'] or
            receipt['target'].get('blob') != TARGET_BLOB or auth.get('target') != receipt['target']):
        raise ValueError('REENTRY_DELIVERABLE_BINDING_DRIFT')
    context_data = bound(root, route['writer_context'], False)
    forbidden = ('FAIL', 'PASS_PROVISIONAL', '校准', '漏检', 'diagnosis', 'feedback',
                 'reviewer-input', '只返回正文', '写一份', 'NOVEL-', 'R2', '刘先生', '连续性项目')
    if any(word in context_data.decode('utf-8') for word in forbidden):
        raise ValueError('REENTRY_WRITER_DIAGNOSIS_OR_COMMAND_LEAKAGE')
    if hashlib.sha256(context_data).hexdigest() != CONTEXT_SHA256:
        raise ValueError('REENTRY_FROZEN_CONTEXT_CHANGED')
    context = json.loads(context_data)
    sources = {key: bound(root, ref, False) for key, ref in evidence['sources'].items()}
    quotes = evidence.get('located_evidence', [])
    if (len(quotes) != 12 or {q.get('evidence_id') for q in quotes} != {f'E{i:02}' for i in range(1, 13)} or
            receipt.get('located_quote_count') != 12 or receipt.get('quotes_and_scope_checked') is not True):
        raise ValueError('REENTRY_EVIDENCE_MISSING')
    for quote in quotes:
        lines = sources[quote['source_id']].decode('utf-8').splitlines()
        start, end = quote['line_start'], quote['line_end']
        if (not isinstance(start, int) or not isinstance(end, int) or not 1 <= start <= end <= len(lines) or
                not quote.get('quote') or quote['quote'] not in '\n'.join(lines[start - 1:end]) or
                not quote.get('use_scope') or quote.get('exact_location_checked') is not True):
            raise ValueError('REENTRY_UNLOCATED_QUOTE')
    for copy in evidence.get('copied_frozen_facts', []):
        source_value = pointer(json.loads(sources[copy['source_id']]), copy['source_pointer'])
        if copy.get('projection') == 'FIRST_CLAUSE_BEFORE_SEMICOLON_WITH_FULL_STOP':
            source_value = source_value.split('；')[0] + '。'
        elif 'projection' in copy:
            raise ValueError('REENTRY_UNSUPPORTED_FACT_PROJECTION')
        if source_value != pointer(context, copy['context_pointer']):
            raise ValueError('REENTRY_FACT_COPY_DRIFT')
    if len(evidence.get('copied_frozen_facts', [])) != 16:
        raise ValueError('REENTRY_FACT_BINDINGS_MISSING')
    entry = evidence.get('selected_entry', {})
    front = evidence.get('front_scene_settlement', {})
    if (entry.get('count') != 1 or entry.get('private_stake_count') != 1 or
            entry.get('moment') != context.get('single_entry_moment') or
            entry.get('primary_private_stake') != context.get('primary_private_stake') or
            entry.get('effectiveness') != 'UNTESTED_EDITORIAL_PREPARATION_CHOICE' or
            entry.get('new_action_sequence_frozen') is not False or evidence.get('necessary_new_life_facts') != [] or
            front.get('housing_private_value_absent_from_all_prior_prose') is not False or
            front.get('current_accepted_composed_front_scene') != 'NOT_ESTABLISHED_FOR_CURRENT_448_EXCERPT' or
            evidence.get('formal_method_revision') != 4 or evidence.get('method_revision_changed') is not False):
        raise ValueError('REENTRY_NEW_FACT_OR_EFFECTIVENESS_CLAIM')
    protection = evidence.get('protected_old_prefix', {})
    original_text = bound(root, protection['source'], False).decode('utf-8')
    if (protection.get('characters') != 197 or protection.get('sha256') != PREFIX_SHA256 or
            hashlib.sha256(original_text[:197].encode()).hexdigest() != PREFIX_SHA256 or
            not target.decode('utf-8').startswith(original_text[:197]) or protection.get('released_now') is not False):
        raise ValueError('REENTRY_OLD_PROTECTION_CHANGED')
    if (proposal.get('status') != 'PROPOSED_NOT_AUTHORIZED' or proposal.get('new_prose_authorized') is not False or
            proposal.get('authorized_generation_budget') != 0 or proposal.get('proposed_generation_budget') != 1 or
            proposal.get('generation_count') != 0 or proposal.get('new_life_facts_authorized') is not False or
            proposal.get('multiple_candidates_allowed') is not False or
            proposal.get('automatic_activation') is not False or proposal.get('old_RC3_remaining_rounds') != 0 or
            proposal.get('old_197_character_protection_released') is not False or
            proposal.get('proposed_change', {}).get('new_life_fact_count') != 0):
        raise ValueError('REENTRY_NEXT_WRITER_NOT_AUTHORIZED')
    for value in (project, checkpoint):
        if (value.get('last_completed_task_id') != TASK or value.get('last_completed_task_contract') != route['task']['path'] or
                value.get('next_action') != NEXT_ACTION or value.get('next_required_action') != NEXT_ACTION):
            raise ValueError('REENTRY_LIVE_CURSOR_DRIFT')
    if checkpoint.get('sequence') != 195 or checkpoint.get('stop') is not True:
        raise ValueError('REENTRY_CHECKPOINT_OR_STOP_DRIFT')
    entry_text = (root / 'START_HERE.md').read_text(encoding='utf-8')
    if TASK not in entry_text or NEXT_ACTION not in entry_text or '当前位置：检查点195。' not in entry_text:
        raise ValueError('REENTRY_ENTRYPOINT_STALE')
    return NEXT_ACTION
