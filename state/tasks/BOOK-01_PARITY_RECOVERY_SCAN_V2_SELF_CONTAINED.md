# BOOK-01 PARITY RECOVERY SCAN V2 — SELF-CONTAINED

Status: READY_FOR_EXTERNAL_LOCAL_EXECUTION

Purpose: perform the same read-only forensic recovery as V1, but do not depend on runtime access to GitHub task-contract files. The execution prompt must embed this contract in full.

## Root cause carried forward

V1 result: BLOCKED.
Access diagnostic: PASS.
Execution plane: LOCAL_WINDOWS.
E: visible: true.
`E:\蒸馏小说`: visible: true.
`E:\蒸馏小说\_private`: visible: true.
Canonical V1 report exists and SHA matched reported SHA.
Verified V1 block reason: `TASK_CONTRACT_UNAVAILABLE`.

Therefore V2 fixes only contract delivery. It does not authorize literary rerun, source modification, packet regeneration, or project-state mutation.

## Execution rules

V2 is a read-only forensic recovery task.

Do not require any GitHub task file to exist locally before executing. If repository files are available, they may be read as supplemental context only; their absence must not block V2 because the contract is embedded in the prompt.

Do NOT:
- rerun Source Gate;
- rerun Source Integrity pipeline;
- regenerate packet;
- rerun whole-book preprocessing;
- rerun literary Evidence Extraction;
- perform new literary analysis;
- create new Formal/Supporting candidates;
- synthesize or validate Novel DNA;
- modify source, repaired source, provenance, existing packets, existing literary artifacts, GitHub state, receipts, or code;
- commit/push/open PR;
- use network/web/LLM.

Missing evidence = UNKNOWN, not NOT_STARTED.

## Historical anchors

BASE work_id: `wrk_526edfd2ac1057236a866131`
BASE normalized_text_sha256: `526edfd2ac1057236a866131a745e4248fb68de606ddc01e6bf31f3fbd790efe`
BASE chapter_count: 40
Known BASE defect: chapter 30 internal copy/mis-splice.

DONOR work_id: `wrk_ecadf1440d73d61ef31ec5ed`
DONOR normalized_text_sha256: `ecadf1440d73d61ef31ec5ed38fcad76e77fb16792e4da46221951faa0bd51d7`
DONOR chapter_count: 40
Known DONOR defect: systematic chapter-tail truncation; donor-only.

Expected historical repair artifacts, if they already exist:
- `E:\蒸馏小说\_private\01_原始小说\射雕英雄传_融合修复候选.TXT`
- `E:\蒸馏小说\_private\repair_provenance\射雕英雄传_ch30_repair.json`
- `STEP-02A_射雕英雄传_内部修复源_ChatGPT蒸馏包.zip`

## Scan roots

Read-only recursively inspect existing paths:
- `E:\蒸馏小说\_private`
- `E:\蒸馏小说\repo\03_StoryCards`
- `E:\蒸馏小说\repo\04_单篇蒸馏`
- `E:\蒸馏小说\repo\05_跨作品蒸馏`
- `E:\蒸馏小说\repo\06_NovelDNA`
- `E:\蒸馏小说\repo\08_质量复盘`
- `E:\蒸馏小说\repo\09_Benchmark`
- other existing manifest/work/packet/evidence/receipt/result/provenance/report artifacts under `E:\蒸馏小说` that are mechanically bindable to BOOK-01.

## Recovery targets

A. Existing repair/provenance artifacts, including repaired work ID and source integrity binding.
B. Existing packet artifacts and manifest/hash binding.
C. Existing literary outputs only for identification/metadata recovery; do not create new judgments.
D. Map recovered outputs to Phase 50/60/70/80 using only:
`RECOVERED_EQUIVALENT | PARTIAL_EVIDENCE | UNKNOWN | CONFLICT`.
E. Produce only minimal gap actions; never propose a full-book rerun merely because evidence is missing.

## Output

Create only:
`E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V2.json`

Do not overwrite V1.

Include at least:
- task/status/scan_mode/book/work_title;
- V1 root-cause carry-forward;
- known_anchors_verified;
- repair_artifacts;
- packet_artifacts;
- literary_artifacts;
- parity.phase50..phase80;
- minimal_gaps;
- regression_performed=false;
- literary_analysis_performed=false;
- source_modified=false;
- packet_regenerated=false;
- network_used=false;
- llm_used=false.

Compute SHA-256 of V2 report.

After writing the V2 report, STOP. Do not execute any normalization/gap repair/Phase 50-80 work in the same task.
