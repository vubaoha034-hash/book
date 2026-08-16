# BOOK-01 PARITY RECOVERY ACCESS DIAGNOSTIC V1

Status: READY
Purpose: determine why the reported BOOK-01 parity recovery scan was BLOCKED, without performing literary work or project regression.

## Inputs

Read first:
- `state/project_state.json`
- `state/tasks/BOOK-01_PARITY_RECOVERY_SCAN_V1.md`
- `state/review_receipts/BOOK-01_PARITY_RECOVERY_SCAN_V1_BLOCKED_REPORTED.json`
- `docs/PROJECT_STATE_ANTI_ROLLBACK_POLICY.md`

Reported recovery result:
- status: BLOCKED
- reported report SHA-256: `6ebe825fc8b380c38e559d9b77b974f1176d2a237b191ce6029cb97c30f8f010`
- reported path: `E:\蒸馏小说_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V1.json`
- canonical expected path: `E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V1.json`

The path discrepancy is an anomaly only; do not assume it is the root cause.

## Strict scope

This is environment/path diagnosis plus an optional single conditional retry of the existing read-only recovery scan.

Do NOT:
- perform literary analysis;
- regenerate packets;
- modify sources;
- rerun Source Gate;
- rerun Evidence Extraction;
- generate candidates or Novel DNA;
- mutate project state;
- commit/push;
- use web/network/LLM.

## Diagnostic sequence

1. Identify execution environment mechanically:
   - OS/platform;
   - current working directory;
   - whether this runtime is Windows local or a remote/container/cloud environment;
   - list available filesystem roots/drives where supported.

2. Test exact paths without creating/modifying content:
   - `E:\`
   - `E:\蒸馏小说`
   - `E:\蒸馏小说\_private`
   - `E:\蒸馏小说\_private\recovery`
   - malformed reported parent: `E:\蒸馏小说_private\recovery`

3. Look for the previously reported JSON at BOTH exact paths:
   - canonical expected path;
   - malformed reported path.

4. If a prior report exists:
   - compute SHA-256;
   - compare with reported SHA-256;
   - read only enough JSON to extract the exact blocking reason/status/minimal_gaps;
   - do not infer missing fields.

5. Decision:

### Case A — local E: execution plane unavailable
If `E:\蒸馏小说` cannot be accessed because the runtime is remote/non-Windows/cloud or does not mount the user's local drive:
- diagnostic result = `LOCAL_EXECUTION_PLANE_UNAVAILABLE`;
- do NOT retry the recovery scan;
- stop.

### Case B — canonical E: paths accessible and prior block was only path construction/normalization error
If `E:\蒸馏小说\_private` is accessible and evidence supports that the previous block resulted only from the malformed path:
- perform exactly ONE retry of `BOOK-01_PARITY_RECOVERY_SCAN_V1` under its original contract;
- force the output path to the canonical exact path:
  `E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V1.json`
- preserve all original read-only/non-literary constraints;
- after retry, stop.

### Case C — canonical paths accessible but block reason is something else
- report exact mechanical blocker;
- do NOT auto-fix unless it is strictly a path normalization issue;
- do NOT retry;
- stop.

## Diagnostic output

If canonical local private path is accessible, write only:
`E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_ACCESS_DIAGNOSTIC_V1.json`

If the local execution plane is unavailable, do not fake a local file; print the diagnostic summary only.

Minimum fields:
- task
- status: PASS | BLOCKED
- diagnosis: PATH_NORMALIZATION_ERROR | LOCAL_EXECUTION_PLANE_UNAVAILABLE | OTHER_MECHANICAL_BLOCKER | UNKNOWN
- environment_os
- execution_plane
- e_drive_visible
- project_root_visible
- private_root_visible
- canonical_report_exists
- malformed_report_exists
- prior_report_sha256_match
- prior_block_reason
- retry_performed
- retry_result
- literary_analysis_performed: false
- source_modified: false
- network_used: false
- llm_used: false

## Stop condition

Stop after diagnosis, or after the one allowed path-error retry.
No Phase 50-80 work may begin in this task.
