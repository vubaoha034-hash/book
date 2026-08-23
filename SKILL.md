---
name: novel-writing-master
description: Design, draft, diagnose, rewrite and audit Chinese fiction with evidence-backed causality, emotion, suspense, reader propulsion, natural speech, scene motivation, climax escalation, continuity, microcraft and de-AI controls.
---

# Novel Writing Master V4

V4 exists because a manuscript can be logically correct, locally grounded and de-AI compliant while still being boring.

New tasks default to V4. V3 remains an inherited integrity layer and historical contract; V4 does not rewrite old V3 results.

## Mandatory preflight

For any continuing project task, read current durable state first and obey anti-rollback:

```text
state/project_state.json
state/continuity/LATEST_CHECKPOINT.json
rules/pass-isolation.md
```

For complete writing, rewrite, diagnosis or final-quality judgment, then read:

```text
workflows/08-novel-master-pipeline-v4.md
config/novel-quality-gates.v4.json
library/reader-experience-technique-bank.v1.md
```

V4 currently has developmental status until its active fresh real-manuscript validation is accepted. While developmental validation is pending, **final freeze is forbidden**.

## What V4 must prove

A deliverable manuscript must prove all applicable inherited V3 integrity gates plus these reader-experience dimensions:

1. **Scene-entry motivation** — important characters enter, return, leave or switch roles because something caused the choice, not because the author now needs their function.
2. **Reader propulsion** — every material span changes not only story state but reader desire: curiosity, dread, expectation, emotional debt, reward or consequential choice.
3. **Suspense hypothesis engine** — meaningful mysteries let the reader form/test/update a model. Repeated oddity plus later explanation is not enough.
4. **Emotional staging** — important emotion is dramatized through pressure, conflicting wants, behavior/subtext, consequential turns and aftershock. Correct short dialogue can still fail if it is only an event skeleton.
5. **Natural speech under pressure** — G6D truth/motive is not proof that a human would package the information that way. Check urgency, relationship, omission, inference and sentence completeness.
6. **Climax escalation** — event volume is not climax. Options must narrow, personal stakes rise, earlier assets/relationships return, irreversible choices occur and payoff/aftershock is visible.
7. **Fresh immersion reader** — before final freeze, a fresh reader must produce an untouched reading trace with real stop/skim points, desire-to-continue drivers, suspense hypotheses, emotional experience and written-vs-spoken dialogue evidence.

## Mandatory modules

```text
modules/scene-entry-motivation.md
modules/reader-propulsion-ledger.md
modules/suspense-hypothesis-engine.md
modules/emotional-staging-ledger.md
modules/natural-speech-pressure.md
modules/climax-escalation-curve.md
```

Inherited V3 microcraft remains required where applicable:

```text
config/novel-quality-gates.v3.json
workflows/07-novel-master-pipeline-v3.md
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/dialogue-epistemic-scope.md
modules/local-logic-ledger.md
rules/no-ai-smell.md
modules/dialogue-pattern-family-density.md
```

## Non-negotiable distinction

```text
EVENT_PROGRESS != READER_PROPULSION
G6D_PASS != NATURAL_SPEECH_PASS
G8_PASS != READER_IMMERSION_PASS
MYSTERY_OBJECT_PRESENT != SUSPENSE_ENGINE_PRESENT
MANY_EVENTS != CLIMAX
FUNCTIONAL_DIALOGUE != DRAMATIZED_DIALOGUE
```

Never infer:

```text
ready_to_freeze = G6D_PASS && G8_PASS
```

Final freeze requires the complete V4 delivery contract in `config/novel-quality-gates.v4.json`.

## Reader Experience Technique Bank

The three source-book evidence pipelines extracted many valuable suspense, emotion, pacing and reward techniques that were historically classified as Supporting. Supporting status must no longer make them invisible to production.

Use:

```text
library/reader-experience-technique-bank.v1.md
```

This bank is separate from Novel DNA. Do not promote craft techniques into DNA merely to make them usable.

Novel DNA remains default OFF and is only invoked through the existing evidence-based DNA Router when a specific structural problem survives simpler fixes.

## Permanent V4 regressions

Read during architecture/regression work, but **not as an answer key in a fresh evaluator context**:

```text
state/benchmarks/READER_EXPERIENCE_V4_REGRESSION_V1.json
```

The system must detect these failure classes:

```text
SKELETONIZED_DIALOGUE_WITHOUT_EMOTIONAL_STAGING
OVERCOMPLETE_AUTHOR_SHAPED_SPEECH_PACKAGE
UNMOTIVATED_MAJOR_SCENE_REENTRY
LOW_READER_REWARD_AND_CLIMAX_VOLTAGE
STIFF_SUSPENSE_WITHOUT_HYPOTHESIS_ENGINE
```

And must preserve false-positive controls for:

- short task dialogue that directly changes action;
- memorial/relationship dialogue tied to unique shared history or objects;
- quiet scenes that increase intimacy, dread or choice pressure;
- complete formal briefing when duty, time and audience need genuinely support it.

## Diagnosis order

When a manuscript is bad, do not start by polishing sentences. Locate the highest upstream failure:

```text
reader promise
→ scene-entry causality
→ causal/choice structure
→ reader propulsion/reward
→ suspense model
→ emotional staging
→ climax escalation
→ continuity/local semantics
→ dialogue grounding
→ natural speech packaging
→ de-AI/aesthetic finish
```

A downstream PASS never cancels an upstream failure.

## Writing discipline

Before drafting a material scene, keep only the minimum active context:

- current scene cause and entry trigger;
- what each present character wants now and what conflicts with it;
- current reader question/expectation;
- current suspense model/anomaly if applicable;
- current emotional debt and scene voltage target;
- character knowledge and what they would naturally omit;
- scene choice, consequence and next pull;
- active Novel DNA call only if explicitly APPLIED.

Do not load every audit rule while drafting prose.

## Fresh reader protocol

For final-quality work, the fresh reader must first read the bound manuscript **before** loading V4/V3 rule files and freeze an immersion trace. Only afterward may the same fresh context run formal gates. This prevents checklist compliance from substituting for actual reading experience.

## Safety / provenance

- Do not copy source-book prose, plots, characters or recognizable living-author style.
- Store real manuscript/source prose privately; public repository receives only abstract rules, hashes, ledgers and privacy-safe evidence.
- Historical failures and freezes are immutable. New evidence creates a new forward settlement; never rewrite history.
- Highest global promotion checkpoint and manuscript quality/freeze status are separate state dimensions.
