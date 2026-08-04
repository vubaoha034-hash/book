# AGENTS.md

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
