---
name: novel-writing-master
description: Design, draft, diagnose, rewrite and audit Chinese fiction with evidence-backed causality, emotion, suspense, reader propulsion, natural speech, dramatization surface, scene motivation, climax experience, continuity, microcraft and de-AI controls.
---

# Novel Writing Master V4.1

V4.1 exists because two stronger statements are now proven necessary:

1. a manuscript can pass logic, G6D, G8 and even structural V4 checks while still reading poorly;
2. a fresh AI reader can rationalize text that an actual target reader has already located as weak.

New tasks default to V4.1. V4 and V3 remain inherited historical layers; do not rewrite their old verdicts.

## Mandatory preflight

For any continuing project task read, in order:

```text
state/project_state.json
state/continuity/LATEST_CHECKPOINT.json
rules/pass-isolation.md
workflows/09-novel-master-pipeline-v4.1.md
config/novel-quality-gates.v4.1.json
library/reader-experience-technique-bank.v1.md
```

If a current-manuscript target-reader evidence ledger exists, coordinator/delivery work must also read it. A fresh blind evaluator must not read it until its blind trace is frozen.

V4.1 remains DEVELOPMENTAL until the current fresh real-manuscript validation task is coordinator-accepted. While developmental validation is pending, final freeze is forbidden.

## Core non-equivalences

```text
LOCAL_DIALOGUE_GROUNDING != DRAMATIZED_SCENE
VALID_SPEAKER_GOAL != NATURAL_UTTERANCE_PACKAGING
OLD_RELATIONSHIP_MOTIVE != POST_WITHDRAWAL_REENTRY_TRIGGER
WORKING_HYPOTHESIS != CURIOSITY_CHARGE
OPTION_COMPRESSION != EXPERIENCED_CLIMAX_VOLTAGE
EVENT_PROGRESS != READER_PROPULSION
FRESH_AI_PASS != HUMAN_TARGET_READER_PASS
```

Never infer final quality from a downstream pass.

## V4.1 reader-experience modules

```text
modules/scene-entry-motivation.md
modules/scene-reentry-decision-delta.md
modules/reader-propulsion-ledger.md
modules/suspense-hypothesis-engine.md
modules/suspense-curiosity-charge.md
modules/emotional-staging-ledger.md
modules/dramatization-surface-density.md
modules/natural-speech-pressure-v1_1.md
modules/climax-escalation-curve.md
modules/climax-experiential-voltage.md
modules/target-reader-evidence-authority.md
```

Inherited V3/V4 integrity modules remain required where applicable.

## Reader evidence authority

A numeric score alone is not a blocker.

A located human target-reader failure is different: it names a text scope and a concrete reader effect. While that failure remains open on the same manuscript SHA:

```text
fresh AI PASS cannot erase it
final freeze is blocked
```

The AI may show that the originally suspected mechanism was wrong. Then repair the mechanism diagnosis, not the existence of the reader failure.

## Manuscript-level dramatization check

Do not audit only isolated dialogue exchanges.

If separated high-stakes scenes repeatedly use terse functional turns + thin generic blocking, build a cross-scene surface-family ledger. One short exchange may be excellent; repeated event-skeleton realization across unrelated scenes may still fail.

Do not fix by adding padding, decorative description, generic gestures or longer dialogue.

## Natural speech V1.1

For high-information speech, test:

1. first urgent payload;
2. independently reactable information segments;
3. where the listener would naturally interrupt or infer;
4. shared-context subtraction;
5. what a human would omit;
6. whether the scene truly supports uninterrupted briefing/testimony/confession.

A real reason to speak is not proof that the exact sentence is natural.

## Re-entry reversal

When a character explicitly withdraws and later returns, ask:

```text
What changed after the decision to leave?
```

An old relationship, ongoing affection or nearby location that already existed at withdrawal time cannot by itself explain the reversal.

## Suspense

Run both:

```text
working hypothesis ledger
curiosity charge ledger
```

A mystery may be fair and guessable yet boring. Reader desire to resolve must be justified by prediction tension, operational stakes, relationship consequence or another concrete cared-about outcome.

## Climax

Run both:

```text
structural option-compression curve
fresh-reader experiential-voltage curve
```

Many events are not a climax. Correct option compression is also not proof that the reader experiences a crescendo.

## Source-book technique use

Reader-experience techniques extracted from 《射雕英雄传》《诛仙》《盗墓笔记》 remain production-visible through:

```text
library/reader-experience-technique-bank.v1.md
```

Supporting classification does not make a technique second-class and does not require promotion into Novel DNA.

Do not copy source prose, plot, characters or recognizable author style.

Novel DNA remains default OFF and only routes structural problems that survive simpler fixes.

## Regression governance

Historical V4 regression remains immutable:

```text
state/benchmarks/READER_EXPERIENCE_V4_REGRESSION_V1.json
```

Future V4.1 validation uses calibrated:

```text
state/benchmarks/READER_EXPERIENCE_V4_1_REGRESSION_V2.json
```

Do not show regression cases or known manuscript failure locations to a fresh blind evaluator. Coordinator compares the returned blind report to them afterward.

## Delivery tiers

```text
MECHANICALLY_VALIDATED
FRESH_AI_READER_VALIDATED
TARGET_READER_VALIDATED
FINAL_FREEZE_ELIGIBLE
```

Do not call a manuscript final/top-tier merely because a fresh AI reader would continue reading.

`FINAL_FREEZE_ELIGIBLE` requires no open located target-reader failure on the current manuscript SHA.

## Continuity and history

- Read durable state first; never roll back because an old chat or old receipt appears.
- Historical failures/freezes remain immutable; new evidence supersedes forward, never rewrites history.
- Public GitHub stores only abstract rules, hashes and privacy-safe evidence; manuscript/source prose stays private.
