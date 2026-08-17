# BOOK-01 PARITY RECOVERY REPORT BRIDGE DIAGNOSTIC V1

Status: READY_FOR_LOCAL_EXECUTOR

Purpose: identify the exact mechanical reason `BOOK-01_PARITY_RECOVERY_REPORT_BRIDGE_V1` returned BLOCKED before creating/pushing `state/recovery_reports/BOOK-01_PARITY_RECOVERY_SCAN_V2_SANITIZED.json`.

## Hard boundaries

Diagnostic only. Do not create the bridge target in this task. Do not retry the bridge. Do not modify project state, source, packet, provenance, literary outputs, or receipts. Do not perform literary analysis. Do not call any LLM.

The known source report remains:
`E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V2.json`
Expected SHA-256:
`88f94e664adc65482a5e944983c09f7960d9ad445756a7e1d3024e62c9db6652`

GitHub repo: `vubaoha034-hash/book`
Target branch: `novel-distill-v1`
Bridge target: `state/recovery_reports/BOOK-01_PARITY_RECOVERY_SCAN_V2_SANITIZED.json`

## Required diagnostic checks

Read-only/mechanical checks:
- confirm source report exists and hash matches;
- locate local git working tree for `vubaoha034-hash/book`;
- current branch;
- `git status --short`;
- `git remote -v` (sanitize credentials/tokens in output);
- whether branch has upstream;
- whether local branch is ahead/behind remote after `git fetch`;
- whether `state/recovery_reports` directory exists locally;
- whether bridge target exists locally;
- whether bridge target exists remotely;
- whether there are unrelated tracked/untracked/staged changes;
- whether local working tree permits creating a single new file without touching unrelated files;
- whether git identity is configured enough to commit;
- whether authentication/push capability is mechanically available (do not create a test commit and do not push a test file);
- inspect any available stderr/stdout/log from the blocked bridge run if present;
- recover the exact blocker category and exact error text where possible.

Allowed blocker categories:
- `SOURCE_REPORT_HASH_MISMATCH_OR_MISSING`
- `TARGET_CONFLICT`
- `WRONG_LOCAL_REPOSITORY_OR_BRANCH`
- `WORKTREE_DIRTY_SCOPE_RISK`
- `STAGING_SCOPE_VIOLATION`
- `GIT_IDENTITY_UNAVAILABLE`
- `REMOTE_OR_UPSTREAM_UNAVAILABLE`
- `AUTH_OR_PUSH_UNAVAILABLE`
- `NON_FAST_FORWARD_OR_REMOTE_CONFLICT`
- `PATH_OR_DIRECTORY_CREATION_BLOCKER`
- `OTHER_MECHANICAL_BLOCKER`
- `UNKNOWN`

Do not infer beyond evidence.

## Output

If private root is accessible, write exactly one diagnostic JSON:
`E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_REPORT_BRIDGE_DIAGNOSTIC_V1.json`

It must include:
- task/status/diagnosis;
- source hash verification;
- repo root/current branch/upstream;
- working tree summary counts, without dumping unrelated file contents;
- bridge target local/remote existence;
- remote divergence state;
- commit identity availability;
- push/auth availability when mechanically knowable without side effects;
- exact blocker/error text if available;
- `retry_safe` boolean;
- if retry_safe=true, `required_retry_fix` limited to a mechanical fix;
- all safety flags false for literary/source/packet/project-state mutation.

Stop after diagnostic. Do not retry bridge in the same task.
