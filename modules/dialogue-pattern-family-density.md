# Dialogue Pattern Family Density Module V1

## Purpose

Detect manuscript-level AI-smell caused by the same portable dialogue machine recurring across separated scenes, characters and relationships.

This module belongs to G8 / de-AI. It does not convert every locally removable joke into a G6D hard failure.

## Core principle

Local plausibility and manuscript-level repetition are different questions.

```text
G6D asks: does this exchange make sense here?
G8 asks: is this same dialogue machine appearing everywhere?
```

A single locally grounded joke may PASS G6D and still become evidence in a G8 pattern family.

## Candidate pattern families

Examples include but are not limited to:

- `Q -> clever retort -> follow-up -> punchline`;
- `question -> evasive tease -> induced question -> reveal`;
- `statement -> sarcastic correction -> counter-correction -> tag`;
- repeated exposition bundles with the same ordering;
- repeated “someone asks / speaker dodges twice / final meaningful line” cadence;
- repeated identical relationship-repair rhythm across unrelated characters.

Do not use a phrase blacklist. Cluster by dialogue function and cadence, not exact words.

## Required instance record

```text
instance_id:
location:
speakers:
relationship_type:
scene_task:
pattern_family_candidate:
cadence_skeleton:
character_specific_anchors:
current_object_or_task_anchor:
shared_history_anchor:
status_or_power_anchor:
independent_local_goal:
portable_to_unrelated_characters: LOW | MEDIUM | HIGH
local_G6D_verdict:
```

## Required family record

```text
family_id:
family_skeleton:
instance_ids:
separated_scene_evidence:
distinct_speaker_pairs:
distinct_relationship_types:
shared_character_specificity:
portable_instance_evidence:
mechanism_variation:
cadence_variation:
downstream_effect_variation:
homogenization_risk: LOW | MEDIUM | HIGH | UNCERTAIN
verdict: PASS | RISK | HOLD
risk_code:
```

## Density judgment without a universal threshold

Do not freeze a universal numeric cutoff from the current three-book purposive sample.

A family becomes stronger G8 risk evidence when several qualitative signals combine:

- recurrence in separated scenes rather than one sustained conversation;
- recurrence across different speaker pairs or relationship types;
- similar cadence and reveal timing;
- low dependence on current object, task or shared history;
- the exchange could be moved between characters with little semantic change;
- multiple characters acquire the same teasing/evasive voice;
- removing one instance does not matter locally, but the repeated family makes the manuscript feel model-authored.

A family may remain PASS/HOLD when recurrence is explained by one character's established habit, a recurring ritual, a running relationship joke, or materially different scene mechanisms.

## Risk code

Use:

`DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK`

This is a G8/de-AI risk code. It is not automatically a logic blocker.

## False-positive protection

Do not flag merely because:

- the manuscript contains many jokes;
- characters ask many questions;
- short exchanges recur;
- one scene contains several related lines;
- the same character has a supported verbal habit.

The target is cross-scene cadence homogenization with weak character/scene specificity.

## Revision rule

When risk is real, do not globally “make dialogue less funny.”

Prefer the smallest family-level intervention:

1. keep the strongest, most character-specific instances;
2. delete or flatten the most portable duplicates;
3. vary response strategy: silence, partial answer, direct answer, interruption, action, mishearing, refusal;
4. preserve factual and relationship state;
5. re-run G6D only on changed dialogue locations, then re-run the G8 family ledger.
