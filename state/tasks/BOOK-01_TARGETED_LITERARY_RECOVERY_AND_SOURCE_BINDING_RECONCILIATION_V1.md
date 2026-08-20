# BOOK-01 TARGETED LITERARY RECOVERY + SOURCE BINDING RECONCILIATION V1

Status: READY_FOR_LOCAL_EXECUTOR

## Goal

Recover any existing BOOK-01《射雕英雄传》 literary result artifacts/receipts and determine which source each artifact actually binds to. Do not generate new literary analysis.

## Authoritative anchors

Repaired formal source:
- work_id: `wrk_5724415a203a194f1c9a481c`
- normalized/source SHA-256: `5724415a203a194f1c9a481cb6a47b0d67807a89fa8c51b52b48afcafd410d14`
- chapter_count: 40
- repaired Packet binding: VERIFIED

Base pre-repair source:
- work_id: `wrk_526edfd2ac1057236a866131`
- normalized SHA-256: `526edfd2ac1057236a866131a745e4248fb68de606ddc01e6bf31f3fbd790efe`
- known chapter-30 internal defect

Donor-only source:
- work_id: `wrk_ecadf1440d73d61ef31ec5ed`
- normalized SHA-256: `ecadf1440d73d61ef31ec5ed38fcad76e77fb16792e4da46221951faa0bd51d7`
- systematic chapter-tail truncation
- NOT eligible as formal distillation source

Sanitized V2 recovery report:
`state/recovery_reports/BOOK-01_PARITY_RECOVERY_SCAN_V2_SANITIZED.json`

## Two required gaps to resolve

1. Targeted recovery of any existing BOOK-01 literary result artifacts or receipts for Phase 50–80. Do not rerun book-wide extraction/synthesis/validation/freeze.
2. Reconcile source binding for every recovered literary artifact because historical upload selection may bind DONOR while the verified repaired Packet binds repaired work.

## Search scope

Read-only search within the project only:
- `E:\蒸馏小说\_private`
- `E:\蒸馏小说\repo`
- all project subdirectories including StoryCards / 单篇蒸馏 / 跨作品蒸馏 / NovelDNA / 质量复盘 / Benchmark / logs / manifests / recovery / upload-selection metadata / prior exports
- Git history and local refs for `E:\蒸馏小说\repo`: all branches/tags/remotes/reflog entries where mechanically accessible

May use Git commands such as `git log --all --name-only`, `git rev-list --all --objects`, targeted `git log -S/-G`, `git show`, and reflog inspection. Do not modify history.

Do not search unrelated user directories/drives.

## Identity search keys

Use combinations of:
- BOOK-01
- 射雕英雄传
- repaired/base/donor work IDs and hashes
- STEP-02A packet names
- StoryCard / Evidence / ledger / candidate registry / Formal / Supporting / Novel DNA / validation / freeze / application / review / receipt / acceptance

Filename similarity alone is weak evidence.

## Source-binding classes

For every recovered literary artifact classify exactly one:

- `REPAIRED_VERIFIED`: explicitly binds repaired work_id/hash or verified repaired Packet.
- `BASE_PRE_REPAIR`: explicitly binds base work/source. Preserve as historical output; not automatically parity-equivalent because chapter 30 is defective. Flag `CH30_IMPACT_REVIEW_REQUIRED` unless artifact explicitly excludes chapter 30 and this is mechanically proven.
- `DONOR_INELIGIBLE`: binds donor work/source/Packet. Preserve as historical output but it cannot satisfy current formal parity.
- `UNKNOWN_BINDING`: literary artifact recovered but source binding cannot be established.
- `CONFLICTING_BINDING`: artifact contains contradictory bindings.

Never silently rebind an old artifact to repaired work.

## Phase mapping

Map recovered artifacts to Phase 50/60/70/80, but only `REPAIRED_VERIFIED` artifacts may directly establish `RECOVERED_EQUIVALENT` without further semantic review.

BASE_PRE_REPAIR may establish that historical work existed, but must not be promoted to repaired-source parity without a later targeted impact review.

DONOR_INELIGIBLE cannot establish current parity.

Allowed phase statuses:
- `RECOVERED_EQUIVALENT`
- `PARTIAL_EVIDENCE`
- `UNKNOWN`
- `CONFLICT`

Never use NOT_STARTED merely because nothing is found.

## No-literary-generation rule

Forbidden:
- rereading the full novel to generate new evidence
- generating new StoryCards / Formal / Supporting / DNA
- validating or freezing DNA
- summarizing the novel
- deciding literary quality
- using any LLM

This task is recovery + binding only.

## Private output

Create exactly one private full report:

`E:\蒸馏小说\_private\recovery\BOOK-01_TARGETED_LITERARY_RECOVERY_BINDING_V1.json`

Include:
- search inventory and roots checked
- Git refs/history searches performed
- recovered artifact metadata/hash/path
- artifact source-binding class and evidence
- phase mapping
- explicit count by binding class
- unresolved conflicts
- minimal semantic follow-up actions, if any
- safety flags

Do not copy novel text or detailed distillation bodies into the report.

## Sanitized bridge in same execution

After the private report is complete, create a metadata-only sanitized report:

`state/recovery_reports/BOOK-01_TARGETED_LITERARY_RECOVERY_BINDING_V1_SANITIZED.json`

Use an isolated temporary worktree created from the latest `origin/novel-distill-v1`, not the diverged local branch. Commit and fast-forward push only this sanitized file.

If remote advances during push, refetch and retry from the new remote head up to 3 attempts. Never merge/rebase/reset/force-push the existing local branch.

Sanitized report may contain paths, hashes, work IDs, phase/source-binding metadata, search coverage, and minimal gaps. It must not contain novel text or detailed literary distillation bodies.

## Stop conditions

After private report + sanitized bridge are verified, stop.
Do not execute any semantic gap repair or Phase 50–80 literary work in this task.
