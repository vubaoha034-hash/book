# AGENTS.md

For any new chat or task continuation, start at `START_HERE.md` and run its current-state check before using historical phase instructions.

## Locked current novel mainline

For this project's current work, read `MAINLINE.md` and the task referenced by `state/project_state.json`. They define the single active improvement route. Preserve the original story and evidence; do not revive a historical phase or change the locked method without a recorded failed frozen test or an explicit scoped user change. Writer-only isolated contexts read their declared packet only; the coordinator settles state before and after that isolated run. The current mainline amends unfinished execution scope, not historical receipts or accepted research checkpoints.

## Highest-priority execution-surface routing

Current scoped override (2026-10-03): task
`NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01` explicitly authorizes
Codex coordination and independent review sessions. Follow
`docs/NOVEL_CODEX_REVIEW_INTEGRATION_20261003.md` and the live checkpoint. Prefer
GPT-6.1 Sol / Max, verified from actual runtime settings. Only the coordinator
writes business state; reviewers receive their assigned packet only, with no
tools, repository access, inherited chat, or other reports. This supersedes the
old browser transport for this round, without retrying its blocked task or
claiming an old callback. Cold screening failed its limited calibration and
cannot certify literary quality or the user's taste. This override supplies no
new prose budget, no V5, and no release of the old 197-character protection.

Current checkpoint196 continuation: after the completed reentry/fact preparation, the user approved its concrete proposal and required direct completion. One fresh writer generated the only 395-character new opening short; a different fresh context returned FACT_CLEAR, with evidence settled by the coordinator. Read `docs/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_RESULT_20261003.md` and its native authorization/task/result. The single new budget is spent. New-version opening organization was authorized; old artifacts, locks, exhausted RC3 budget and human rejections remain intact. Next: actual human reading of this frozen short. No automatic A2, full scene, TEST-02, V5 or new life facts. FACT_CLEAR cannot become a human PASS.

This section selects the execution surface only. It does not override V3 content/phase routing, quality gates, or human gates. If an execution-route preference conflicts with a content or human gate, the gate wins.

- Default execution mode: `CHAT`.
- Every newly opened Chat execution uses `thinking_effort = EXTREME_HIGH`.
- CHAT covers story design/diagnosis/review/rewrite, ordinary web search and source reading, ordinary browser navigation/clicking, human-review-card preparation/handling, ordinary repository/connector reads, and small canonical writes that do not require a local runtime.
- Ordinary web or browser work does **not** imply Work.
- Use Work only when it is materially better: an unusually long autonomous workflow, many-step coordination across multiple apps/sites, Chat becoming materially slower/fragmented/unstable, or a genuinely Work-only capability.
- Use Codex local for local engineering: full repository access, shell/Python, tests, dependency installation, build/compilation, bulk file processing, or large-scale local Git.
- Execution routing never authorizes crossing a quality gate, phase gate, or human gate, and never supplies a required human verdict on the user's behalf.
- Reusable machine-readable policy: `rules/execution-routing-v1.json`.

## Repository purpose

This repository contains `novel-writing-master`, an evidence-driven Chinese-fiction Skill.

## Default version

Use V3 for new work. V2 files remain for backward compatibility.

Always read:

- `SKILL.md`
- `rules/pass-isolation.md`
- `workflows/07-novel-master-pipeline-v3.md` for full-production tasks

Load only the current phase files.

## Phase routing

### Source ingestion and story dissection

Use the existing V2 ingestion and dissection assets:

- `workflows/01-ingest-book.md`
- `workflows/05-deep-story-dissection.md`
- `scripts/ingest.py`

Extract abstract craft only. Do not publish protected source text or private personal samples.

### Story design and rewrite

Read:

- `modules/causal-proof-engine.md`
- `modules/emotion-payoff-ledger.md`
- `modules/hate-empathy-test.md`
- `modules/character-pressure-test.md`

Do not draft the full story until the story contract, causal chain, emotional debt, and character-choice evidence exist.

### Drafting

Use only the story contract, current causal row, current emotional-debt task, current character state, necessary rules, aesthetic baseline, previous ending, and next target.

Do not load all review modules during prose generation.

### Logic and continuity

Read:

- `modules/causal-proof-engine.md`
- `modules/developmental-editor.md` when the spine, structure, or pacing is in doubt
- `modules/continuity-editor.md`
- `rules/novel-logic-checklist.md`

Treat an unexplained simpler solution as a blocker when it can dissolve the core conflict without meaningful cost.

### Emotion, hate, empathy, and payoff

Read:

- `modules/emotion-payoff-ledger.md`
- `modules/hate-empathy-test.md`
- `rules/reader-reward-rhythm.md`

Do not count shock reactions, facial expressions, apologies, or narration as payoff unless power, relationship, choice, interest, or cost changes.

### Reader checks

Use `modules/opening-retention-reader.md` and `modules/beta-reader-panel.md`.

Call a review independent only when it actually runs in a fresh context or comes from an external reader. Otherwise label it a simulated reader lens.

### Line edit and de-AI

Read:

- `modules/aesthetic-fingerprint.md`
- `modules/line-editor-deslop.md`
- `rules/no-ai-smell.md`
- `rules/reader-trust-and-economy.md`

Run last. Change no plot facts. Handle at most five high-impact patterns per pass.

## Quality evidence

Use `config/novel-quality-gates.v3.json` and `templates/v3-evidence-packet-template.md`.

A gate requires located textual evidence. A checked box, self-score, role-played reader count, or existing file is not quality evidence.

## Review discipline

- Diagnose before rewriting.
- Logic before language.
- Causality before pacing cosmetics.
- Emotional debt before isolated “爽点”.
- Concrete choice before backstory explanation.
- Preserve effective awkwardness, subtext, and voice.
- After a change, recheck its downstream facts, knowledge, objects, rules, and relationships.

## Repository changes

1. Preserve the root `SKILL.md` entrypoint.
2. Keep V2 assets for compatibility unless a migration explicitly removes them.
3. Add specialized methods as modules, workflows, templates, or config.
4. Update `README.md` for user-facing changes.
5. Run `python scripts/validate_skill.py`.
6. Never commit private source books, complete copyrighted text, or personal style samples to this public repository.
