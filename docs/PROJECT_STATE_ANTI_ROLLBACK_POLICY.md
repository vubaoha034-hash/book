# Project State Anti-Rollback Policy V1

Status: ACTIVE
Scope: all persistent project workflows using ChatGPT, Codex, local executors, GitHub, task ledgers, checkpoints, or review receipts.

## 1. Purpose

Prevent stale task specifications, stale chats, stale files, missing search hits, or disconnected execution environments from moving an already completed project backward.

The system MUST distinguish:

- TASK_SPEC: what was requested.
- EXECUTION_RESULT: what a runner reported.
- REVIEW_RECEIPT: ChatGPT/human acceptance, rejection, or block decision.
- ACCEPTED_CHECKPOINT: highest accepted durable progress.
- CURRENT_STATE: reconciled state after applying this policy.
- SUPERSEDED: an older artifact that may remain for audit but cannot become current again.

A task specification is never evidence that the task is still pending.

## 2. Source-of-truth priority

When sources disagree, use this order from highest to lowest:

1. Durable CURRENT_STATE record.
2. Latest ACCEPTED_CHECKPOINT / accepted REVIEW_RECEIPT.
3. Latest verified execution result bound to a task_id/result hash.
4. Current branch/ref/runtime metadata relevant to the active project.
5. Explicit later completion evidence in the current project conversation.
6. Historical task specs, handoff files, archived chats, retry instructions, old screenshots, or old status notes.

Lower-priority evidence MUST NOT overwrite higher-priority evidence.

## 3. Monotonic progress invariant

Progress is monotonic by default.

For a candidate state C and accepted state A:

- If C.phase_ordinal < A.phase_ordinal: REJECT with STATE_REGRESSION_CONFLICT.
- If C.phase_ordinal == A.phase_ordinal and C.progress_ordinal < A.progress_ordinal: REJECT with STATE_REGRESSION_CONFLICT.
- If a task_id is already ACCEPTED, it MUST NOT be dispatched again.
- If an accepted result hash is seen again, processing MUST be idempotent: no duplicate state advance, no duplicate write, no duplicate external action.

Backward movement is allowed only by an explicit ROLLBACK_RECEIPT containing:

- rollback_authorized = true
- project_id
- from_checkpoint
- to_checkpoint
- reason
- authorizer
- timestamp
- evidence_ref or evidence_hash

Without this receipt, rollback is forbidden.

## 4. UNKNOWN is not NOT_STARTED

Failure to find a result means UNKNOWN, not NOT_STARTED.

Forbidden inference:

`no search hit -> task never ran`

Required behavior:

`no search hit -> UNKNOWN -> reconcile against higher-priority state sources`

The system MUST NOT lower the current checkpoint because a file, chat, local path, or connector result is unavailable.

## 5. Task-spec isolation

Historical task instructions, retry files, blocked-run instructions, and handoff notes are immutable audit artifacts. They may prove that a task once existed; they cannot prove current pending status.

Any task spec whose task_id or phase lies below the accepted checkpoint is automatically SUPERSEDED unless an authorized rollback exists.

## 6. Local/cloud separation

ChatGPT/GitHub state MUST NOT be treated as proof of Windows local runtime state, and local runtime absence MUST NOT be treated as proof that durable project progress never occurred.

When a required environment cannot be inspected:

- mark that environment facet UNKNOWN;
- preserve the accepted checkpoint;
- do not invent execution results;
- do not regress the project.

## 7. Mandatory reconciliation before answering “what next?”

Before selecting or dispatching a next task, the coordinator MUST:

1. Read/recover the highest accepted checkpoint.
2. Read the latest review receipt if one exists.
3. Identify current task_id and result status.
4. Mark older task specs as superseded when their stage is below the accepted checkpoint.
5. Compare the proposed next phase/progress against the accepted checkpoint.
6. Stop on any backwards transition with STATE_REGRESSION_CONFLICT.
7. Treat missing evidence as UNKNOWN, never as NOT_STARTED.
8. Only then emit/execute NEXT_STEP.

## 8. Mutation gate

Before any write, dispatch, Codex task, Git update, local execution request, betting/finance action, or artifact generation that depends on project state:

- proposed state must pass monotonicity validation;
- the action must bind to the current checkpoint/task_id;
- stale/superseded tasks must be refused;
- accepted tasks must be idempotent.

## 9. Conflict behavior

On conflict, do not choose the older or more convenient source.

Return one of:

- PASS: proposed transition is forward or idempotent.
- STATE_REGRESSION_CONFLICT: proposed transition moves backward.
- STATE_SOURCE_CONFLICT: two high-priority durable sources disagree.
- UNKNOWN: insufficient evidence, while preserving the highest accepted checkpoint.

No automatic destructive repair is allowed under conflict.

## 10. Current novel-project checkpoint

As of 2026-08-15T21:30:00+08:00, the accepted BOOK-02 《诛仙》 checkpoint is:

- numbered evidence completed through chapter 210;
- target numbered chapters: 256;
- coverage: 210 / 256 = 82.03125%;
- Formal ZX Candidates: 10;
- Supporting Patterns: 16;
- Novel DNA: 0;
- next batch: chapters 211-220.

Any proposal that returns BOOK-02 to Source Gate, Packet Gate, or evidence <= 210 without an explicit rollback receipt MUST be rejected as STATE_REGRESSION_CONFLICT.

## 11. Cross-project requirement

This policy is intended as the baseline invariant for the user’s other long-running projects as well: novel distillation, song distillation, football, investment/market systems, automation bridges, and future staged workflows. Project-specific state schemas may differ, but the anti-rollback invariants above do not.
