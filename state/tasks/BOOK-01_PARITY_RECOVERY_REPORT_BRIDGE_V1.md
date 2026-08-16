# BOOK-01 PARITY RECOVERY REPORT BRIDGE V1

Status: READY_FOR_EXTERNAL_LOCAL_EXECUTION

Purpose: bridge the already-completed local `BOOK-01_PARITY_RECOVERY_SCAN_V2.json` into a sanitized metadata-only GitHub artifact so ChatGPT can review exact minimal gaps without copying private novel/distillation bodies.

## Source report

Expected canonical path:
`E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V2.json`

Reported alternate path string:
`E:\蒸馏小说_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V2.json`

Expected SHA-256:
`88f94e664adc65482a5e944983c09f7960d9ad445756a7e1d3024e62c9db6652`

Use whichever existing path matches this exact SHA. If neither matches, STOP with `SOURCE_REPORT_HASH_MISMATCH_OR_MISSING`.

## Allowed action

Read the V2 JSON and create exactly one sanitized repository file:
`state/recovery_reports/BOOK-01_PARITY_RECOVERY_SCAN_V2_SANITIZED.json`

The sanitized file may contain only:
- task/status/scan mode/book/work title;
- execution environment metadata;
- known anchor verification results;
- repair artifact metadata: paths, filenames, hashes, sizes, timestamps, IDs, binding/status fields;
- packet artifact metadata and verification results;
- literary artifact metadata only (path/name/hash/size/time/stage/status/counts/binding); NO literary body/text excerpts;
- parity phase50–80 values;
- `minimal_gaps` exactly as present in V2;
- safety flags;
- source report SHA-256;
- sanitization declaration.

Forbidden content:
- novel text;
- chapter text;
- detailed distillation prose;
- extracted scenes;
- long literary summaries;
- hidden/private creative analysis bodies.

## Repository mutation boundary

Only the sanitized JSON may be added.
Do NOT modify:
- `state/project_state.json`;
- any review receipt;
- any existing artifact;
- source code;
- source files;
- packet files.

One commit is allowed solely for the sanitized file. Push to existing branch `novel-distill-v1` is allowed.

Network is allowed only for Git repository fetch/status/push required to publish this one metadata file. No web browsing/search/API/LLM use.

## Idempotency

If the target sanitized file already exists:
- fetch/read it;
- if its `source_report_sha256` equals the expected V2 SHA and sanitization declaration is present, do not rewrite; return `EXISTING_SANITIZED_BRIDGE_REUSED`;
- otherwise STOP with `TARGET_CONFLICT`.

## Completion

After push, return only:

BOOK-01 PARITY RECOVERY REPORT BRIDGE COMPLETE

status: <PASS | BLOCKED | EXISTING_SANITIZED_BRIDGE_REUSED>
source_report_sha256: <sha>
target: state/recovery_reports/BOOK-01_PARITY_RECOVERY_SCAN_V2_SANITIZED.json
commit: <sha | UNKNOWN>
pushed: <true | false>
minimal_gaps: <count>
novel_text_in_bridge: false
detailed_distillation_body_in_bridge: false
project_state_modified: false
literary_analysis_performed: false
source_modified: false
packet_regenerated: false
llm_used: false
STOPPED: true
