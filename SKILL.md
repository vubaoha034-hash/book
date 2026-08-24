---
name: novel-writing-master
description: Design, draft, diagnose, rewrite and audit Chinese fiction with evidence-backed causality, reader propulsion, target-reader calibration, suspense charge, natural speech, dramatization surface, scene motivation, climax experience, continuity, microcraft and de-AI controls.
---

# Novel Writing Master V4.2

V4.2 is the default project writing/audit system.

It exists because:

1. logical correctness does not prove readability;
2. fresh context does not calibrate taste;
3. a fresh AI reader may genuinely like text that the declared target reader rejects;
4. unique props or backstory can disguise repeated thin scene surfaces;
5. every clause in a speech can be relevant while the turn still sounds writer-composed;
6. danger can be compelling even when the mystery answer itself is not;
7. a structurally terminal climax can still feel flatter than earlier emotional peaks.

V4.1, V4 and V3 remain inherited historical layers. Do not rewrite prior verdicts.

## Mandatory continuity preflight

For any continuing project task read first:

```text
state/project_state.json
state/continuity/LATEST_CHECKPOINT.json
rules/pass-isolation.md
```

For complete writing, rewrite, diagnosis or final-quality judgment then read:

```text
workflows/10-novel-master-pipeline-v4.2.md
config/novel-quality-gates.v4.2.json
library/reader-experience-technique-bank.v1.md
```

Also obey:

```text
rules/holdout-contamination-and-repair-separation.md
rules/human-aesthetic-rejection-blank-page-reauthoring-trigger.md
```

If the project defines a non-answer-key target-reader profile, use it for target-fit evaluation. For current YMGQ:

```text
state/reader_profiles/YMGQ_TARGET_READER_PROFILE_V1.json
```

A fresh target-reader simulation may read the profile before the manuscript, but must not read exact failure locations, prior reports, repair history or regression answer keys.

V4.2 remains DEVELOPMENTAL for architecture promotion. Final freeze is forbidden while located human failures remain open.

A developmental architecture may still authorize a bounded repair of a labelled manuscript after coordinator adjudication when located human reader evidence is already valid. Do not require the AI to rediscover every human aesthetic failure before repair.

## Core non-equivalences

```text
FRESH_CONTEXT != CALIBRATED_TASTE
FRESH_AI_READER != TARGET_READER
LOCAL_LOGIC_PASS != DRAMATIZED_SCENE
UNIQUE_PROP != UNIQUE_SCENE_SURFACE
VALID_SPEAKER_GOAL != NATURAL_LIVE_TURN
ALL_FACTS_RELEVANT != NATURAL_INFORMATION_PACKET
WORKING_HYPOTHESIS != CURIOSITY_CHARGE
DANGER_INTEREST != MYSTERY_ANSWER_INTEREST
OPTION_COMPRESSION != EXPERIENCED_CLIMAX_VOLTAGE
EVENT_PROGRESS != PAGE_TURN_COMPULSION
FRESH_AI_RECOMMENDATION != HUMAN_TARGET_READER_ACCEPTANCE
CURRENT_MANUSCRIPT_REPAIR_AUTHORIZATION != ARCHITECTURE_PROMOTION
LABELLED_CALIBRATION_CASE != FRESH_GENERALIZATION_HOLDOUT
LOCAL_SCENE_SPECIFICITY != MANUSCRIPT_LEVEL_VOICE_VARIETY
HUMAN_GLOBAL_AESTHETIC_REJECTION != LOCAL_PATCH_QUEUE
```

## Human aesthetic rejection hard stop

If the actual target reader reports that the manuscript has no meaningful desire-to-continue, feels like an event outline/transcript, contains many mechanically generated dialogue exchanges, or would not be recommended, then:

1. the actual human result controls the labelled manuscript;
2. prior AI PASS / PASS_WITH_FRICTION may not rescue the candidate;
3. bounded line repair and same-prose preservation stop immediately;
4. invoke `rules/human-aesthetic-rejection-blank-page-reauthoring-trigger.md`;
5. rebuild from a minimal story kernel rather than paraphrasing the failed prose;
6. merging/deleting/reordering scenes, characters, factions, subplots, suspense devices and reveals is allowed when it improves the reading experience;
7. do not draft the entire replacement manuscript before actual human approval of representative prose pilots.

A local object, shared-history anchor, causal correctness, new-information payload, or character-specific noun does not automatically rescue a recurring portable dialogue cadence that the human target reader experiences as mechanical.

## Mandatory V4.2 hardening modules

```text
modules/target-reader-profile-calibration.md
modules/dramatization-surface-density-v1_1.md
modules/natural-speech-pressure-v1_2.md
modules/scene-reentry-evidence-anchor-v1_1.md
modules/suspense-curiosity-charge-v1_1.md
```

Also load inherited V4.1 modules as applicable:

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

Inherited V3 microcraft/continuity remains required where relevant.

## Target-reader profile rule

A target-reader profile defines the audience contract, not the answer key.

It may contain preferences such as:

- tolerated dramatization density;
- accepted minimalism conditions;
- speech naturalness expectations;
- suspense appetite;
- climax voltage expectations;
- reader-propulsion expectations.

It must not contain exact failed locations or quoted known failures for a fresh evaluator.

If no target profile exists, do not call a fresh AI read `target-reader validated`; call it generic fresh AI evidence only.

## Dramatization surface V1.1

For separated high-stakes scenes, perform a functional-mask audit:

1. temporarily abstract names, props, factions and lore labels;
2. record the remaining surface sequence;
3. ask whether unique carriers actively change behavior, timing, resistance, subtext or consequence;
4. ask whether available dramatic pressure actually entered the scene.

Different props cannot automatically rescue the same thin event machine.

Do not require padding, long dialogue, interior monologue or decorative description.

## Natural speech V1.2

For high-information live speech:

1. identify the earliest sufficient warning/payload;
2. classify later clauses by information role;
3. identify plausible listener reaction boundaries;
4. perform shared-context subtraction;
5. test what the speaker would naturally omit;
6. test whether visible environment can carry part of the packet;
7. require a located reason for uninterrupted multi-role delivery.

`all facts are useful` is not a PASS condition.

## Re-entry evidence anchor

If a character explicitly withdraws and later returns:

```text
What exact text proves this character had a new reason before re-entry?
```

Do not infer motive from what the character does after returning.

Old affection, spatial proximity or scene utility cannot substitute for a post-choice delta.

## Suspense curiosity V1.1

Run an answer-value ablation:

```text
If the mystery answer were revealed now but current danger/action remained, how much reader pull disappears?
```

Separate:

```text
threat ownership
answer ownership
model delta
desire delta
```

A dangerous hidden force may create excellent action tension but weak mystery appetite.

## Climax

Run both inherited curves:

```text
structural option-compression curve
experiential-voltage curve
```

Do not require the highest peak to be the largest battle. Require the intended climax architecture to produce the target-reader experience it promises.

## Source-book craft

Reader-experience techniques extracted from 《射雕英雄传》《诛仙》《盗墓笔记》 remain production-visible through:

```text
library/reader-experience-technique-bank.v1.md
```

Do not copy prose, plot, characters or recognizable author style.

Novel DNA remains default OFF and only routes structural problems that survive simpler fixes.

## Hidden-holdout architecture validation

Fresh evaluators must not see:

```text
state/reader_evidence/*
state/benchmarks/READER_EXPERIENCE_*.json
prior evaluator reports
repair ledgers
known bad locations
```

After a fresh report returns, coordinator compares it to hidden human evidence/regression cases.

Architecture promotion fails if a material hidden holdout defect is missed or explicitly rationalized as PASS.

### Holdout contamination stop rule

Once a manuscript's human feedback has materially shaped gates, target profiles, regressions, prompts or acceptance criteria, that manuscript is a labelled calibration case rather than a valid architecture-promotion holdout.

Do not continue same-manuscript fresh reruns until every known defect is reproduced. That is overfitting, not generalization.

Use the labelled manuscript for repair and regression development. Test architecture generalization later on a genuinely new, pre-registered holdout that did not supply calibration evidence.

## Repair authorization versus architecture promotion

A current manuscript may enter bounded repair when:

1. located human target-reader evidence is valid and bound to its SHA;
2. the required coordinator adjudication cycle has completed;
3. the failures remain inside the declared target-reader contract.

Repair may use the located human evidence directly. It does not require a fresh AI evaluator to independently reproduce 100% of those aesthetic failures first.

Repair does not promote V4.2, does not close human failures, and does not authorize final freeze. Closure requires post-change validation.

## Representative human pilot before full reauthoring

After a human-aesthetic rejection hard stop, full-manuscript reauthoring is gated by an actual-human pilot.

The pilot must include representative prose from at least:

- opening / ordinary human interaction;
- high-pressure relationship dialogue;
- suspense or reveal;
- climax-adjacent pressure.

If the actual target reader rejects the pilot voice/surface, discard or redesign the approach before writing the full manuscript. Do not accumulate another full-length draft on an unvalidated prose engine.

## Delivery tiers

```text
MECHANICALLY_VALIDATED
GENERIC_FRESH_AI_VALIDATED
PROFILE_CALIBRATED_FRESH_AI_VALIDATED
TARGET_READER_VALIDATED
FINAL_FREEZE_ELIGIBLE
```

`FINAL_FREEZE_ELIGIBLE` requires no open located human target-reader failure on the current manuscript SHA.

## Continuity / history

- Read durable state before task execution.
- Never roll back because an older chat/receipt appears.
- Historical failures/freezes remain immutable; new evidence supersedes forward.
- Public GitHub stores abstract rules/hashes/privacy-safe evidence only; manuscript/source prose remains private.
