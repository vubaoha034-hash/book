# BOOK-01 PARITY RECOVERY SCAN V1

Status: READY_FOR_LOCAL_EXECUTOR
Purpose: recover durable evidence for BOOK-01《射雕英雄传》 without redoing completed work.

## Non-negotiable constraints

This is a read-only forensic recovery task.

Do NOT:
- rerun Source Gate;
- rerun Packet generation unless an existing packet is found corrupt and a later explicit repair task authorizes regeneration;
- rerun literary Evidence Extraction;
- summarize or analyze the novel;
- generate Formal/Supporting rules;
- generate Novel DNA;
- modify the novel source;
- modify repo code;
- commit/push;
- use network or web search;
- call any LLM.

Missing evidence means UNKNOWN, not NOT_STARTED.
Existing completed work must be preserved.

## Known historical anchors to use only for recovery

BASE work:
- work_id: `wrk_526edfd2ac1057236a866131`
- normalized_text_sha256: `526edfd2ac1057236a866131a745e4248fb68de606ddc01e6bf31f3fbd790efe`
- 40 chapters
- globally more complete source
- historical defect: chapter 30 internal copy/mis-splice

DONOR work:
- work_id: `wrk_ecadf1440d73d61ef31ec5ed`
- normalized_text_sha256: `ecadf1440d73d61ef31ec5ed38fcad76e77fb16792e4da46221951faa0bd51d7`
- 40 chapters
- systematic chapter-tail truncation; donor-only, never valid as full distillation source

Historical repair task expected artifacts:
- `E:\蒸馏小说\_private\01_原始小说\射雕英雄传_融合修复候选.TXT`
- `E:\蒸馏小说\_private\repair_provenance\射雕英雄传_ch30_repair.json`
- `STEP-02A_射雕英雄传_内部修复源_ChatGPT蒸馏包.zip`

Historical repair rules required chapter 30-only semantic change and no imported donor tail defect.

## Scan roots

Read-only recursively inspect, where present:

- `E:\蒸馏小说\_private`
- `E:\蒸馏小说\repo\03_StoryCards`
- `E:\蒸馏小说\repo\04_单篇蒸馏`
- `E:\蒸馏小说\repo\05_跨作品蒸馏`
- `E:\蒸馏小说\repo\06_NovelDNA`
- `E:\蒸馏小说\repo\08_质量复盘`
- `E:\蒸馏小说\repo\09_Benchmark`

Do not assume these directories contain BOOK-01 artifacts merely because they exist.

## Recovery objectives

### A. Repair/provenance recovery

Find and hash:
- repaired candidate TXT;
- `射雕英雄传_ch30_repair.json`;
- any repair report/result;
- repaired structured work directory and `work.json`/`chapters.jsonl`;
- source integrity report bound to repaired work.

If repair provenance exists, report exact fields including:
- repaired_work_id;
- changed_chapters;
- alignment uniqueness;
- generated_text_used;
- network_source_used;
- source_integrity_status;
- distillation_allowed;
- processing_fingerprint.

Do not reconstruct missing provenance from memory.

### B. Packet recovery

Find candidate packet/ZIP artifacts whose manifests bind to BOOK-01 repaired work.
Prefer exact historical name if present:
`STEP-02A_射雕英雄传_内部修复源_ChatGPT蒸馏包.zip`

For each candidate, report:
- path;
- SHA-256;
- size;
- internal manifest filename;
- work_id/source hash binding;
- chapter count;
- manifest/hash verification result if mechanically verifiable without modification.

Do not regenerate a packet in this task.

### C. Literary-output recovery

Search by metadata/filenames/content headers only for existing BOOK-01 artifacts such as:
- Evidence Extraction results;
- chapter/batch evidence ledgers;
- Story Cards;
- single-book distillation;
- Formal/Supporting candidate registries;
- Novel DNA / rule candidates;
- review receipts / acceptance notes;
- cross-book preparation notes.

The scan may read these existing outputs for identification and metadata extraction. Do NOT create new literary judgments.

For every recovered item record:
- path;
- SHA-256;
- modified timestamp;
- declared book/work ID;
- declared stage/status;
- evidence coverage if explicitly stated;
- counts only if explicitly stated;
- whether source binding can be verified.

### D. Parity mapping

Map only recovered evidence into:
- Phase 50 — Evidence Settlement / Candidate Registry;
- Phase 60 — DNA Synthesis;
- Phase 70 — DNA Validation;
- Phase 80 — Freeze/Application Contract.

Each phase must be one of:
- `RECOVERED_EQUIVALENT`
- `PARTIAL_EVIDENCE`
- `UNKNOWN`
- `CONFLICT`

Never use `NOT_STARTED` merely because no file is found.

### E. Minimal-gap plan

If parity is not complete, output the smallest missing review action(s), e.g.:
- normalize existing registry only;
- validate already-existing DNA only;
- freeze already-validated DNA only;
- recover a missing receipt only.

Forbidden minimal-gap action:
- full-book literary rerun unless a separate future authorization proves no usable prior evidence exists.

## Output

Write exactly one machine-readable recovery report to a PRIVATE local location:

`E:\蒸馏小说\_private\recovery\BOOK-01_PARITY_RECOVERY_SCAN_V1.json`

Do not place private paths/content in Git except later through a sanitized ChatGPT review receipt.

Minimum schema:

```json
{
  "task": "BOOK-01_PARITY_RECOVERY_SCAN_V1",
  "status": "PASS | PARTIAL | BLOCKED",
  "scan_mode": "READ_ONLY",
  "book": "BOOK-01",
  "work_title": "射雕英雄传",
  "known_anchors_verified": {},
  "repair_artifacts": [],
  "packet_artifacts": [],
  "literary_artifacts": [],
  "parity": {
    "phase50": "RECOVERED_EQUIVALENT | PARTIAL_EVIDENCE | UNKNOWN | CONFLICT",
    "phase60": "RECOVERED_EQUIVALENT | PARTIAL_EVIDENCE | UNKNOWN | CONFLICT",
    "phase70": "RECOVERED_EQUIVALENT | PARTIAL_EVIDENCE | UNKNOWN | CONFLICT",
    "phase80": "RECOVERED_EQUIVALENT | PARTIAL_EVIDENCE | UNKNOWN | CONFLICT"
  },
  "minimal_gaps": [],
  "regression_performed": false,
  "literary_analysis_performed": false,
  "network_used": false,
  "llm_used": false
}
```

## Stop condition

After writing the recovery report, stop.
Do not execute any gap repair or literary normalization in the same task.
ChatGPT must review the report first.
