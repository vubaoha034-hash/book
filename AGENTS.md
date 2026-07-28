# AGENTS.md

## Repository purpose

This repository contains the `novel-writing-master` Agent Skill for Chinese fiction creation, deep story dissection, drafting, diagnosis, revision, continuity checking, reader simulation, and line editing.

## Primary operating rule

Use a staged workflow. Do not combine drafting, structural review, reader simulation, continuity checking, and de-AI editing into one undifferentiated pass.

Always read:

- `SKILL.md`
- `rules/pass-isolation.md`

Then load only the files relevant to the current phase.

## Phase routing

### Source ingestion and technique extraction

Read:

- `SKILL.md` Mode 1–3
- `workflows/05-deep-story-dissection.md`
- relevant templates under `templates/`

Learn abstract craft only. Never copy protected prose or imitate a living author's identifiable style.

### New story planning

Read:

- `workflows/06-novel-master-pipeline.md`
- `modules/developmental-editor.md`
- `modules/character-pressure-test.md`
- `rules/reader-trust-and-economy.md`

Do not draft the full story before Gate 0–2 are satisfied.

### Drafting

Use only:

- story contract
- current scene plan
- current character state
- necessary world rules
- style baseline
- previous scene ending and next scene target

Do not load all review modules while generating prose.

### Opening review

Read:

- `modules/opening-retention-reader.md`

Cold-read without future plot knowledge. Report the exact stop point.

### Reader review

Read:

- `modules/beta-reader-panel.md`

Keep reader lenses independent. Lock individual reactions before synthesis.

### Logic and continuity

Read:

- `modules/continuity-editor.md`
- `rules/novel-logic-checklist.md`

Separate confirmed contradictions, possible intentional devices, and explanation gaps.

### Developmental review

Read:

- `modules/developmental-editor.md`

Return 2–5 ranked root diagnoses with located evidence. Do not begin with line-level polish.

### Line edit and de-AI pass

Read:

- `modules/line-editor-deslop.md`
- `rules/no-ai-smell.md`
- `rules/reader-trust-and-economy.md`

Run only after structural gates pass. Preserve plot facts and author voice.

## Quality gates

Machine-readable gate definitions live at:

- `config/novel-quality-gates.v2.json`

Human recording template:

- `templates/novel-quality-gate-template.md`

A numeric score cannot override an open BLOCKER.

## Review discipline

- Diagnose before rewriting.
- Logic before language.
- Cite scenes, paragraphs, events, or exact lines.
- Separate fact from inference.
- Preserve intentional genre and voice choices.
- Do not force every work into the same commercial template.
- Do not confuse short sentences with fast pacing.
- Do not confuse hidden information with valid suspense.
- Do not resolve relationship damage without earned cost.
- Do not declare a first draft finished before independent review.

## GitHub changes

When modifying this repository:

1. Preserve backward compatibility with the root `SKILL.md` entrypoint.
2. Add specialized methods as modules, rules, workflows, templates, or config rather than creating another competing root skill.
3. Update `README.md` when adding user-facing capabilities.
4. Keep examples original and short.
5. Never commit copyrighted source books or extracted full text.
