# Microcraft Dialogue / Local Logic Audit

## Scope

Manuscript / scene:
Audit mode: DEVELOPMENT | PRE_DELIVERY | REGRESSION
Reviewer context: SAME_CONTEXT | FRESH_CONTEXT | HUMAN

## Dialogue Trigger Anchor records

### DTA-001

```text
location:
speaker:
listener:
scene_state:
immediate_trigger:
speaker_perception:
non_speech_reaction_or_NONE:
why_speak_now:
speaker_in_scene_goal:
listener_already_knows:
information_carrier:
withheld_or_unsaid:
aftereffect:
no_reader_counterfactual: WOULD_STILL_SAY | WOULD_NOT_SAY | UNCERTAIN
non_speech_option_checked:
verdict: PASS | FAIL | HOLD
failure_code:
```

Duplicate for each high-impact dialogue start/turn.

## Local Semantic Logic records

### LSL-001

```text
anchor_location:
anchor_fact:
anchor_time_or_state:
semantic_relation:
inherited_scope:
scope_break_present: true | false | ambiguous
linked_clause_or_item:
later_explicit_fact:
verdict: CONSISTENT | CONTRADICTION | AMBIGUOUS
confidence: HIGH | MEDIUM | LOW
failure_code:
repair_target:
```

## Anti-template scan

```text
sequence_location:
sequence_shape:
state_change_per_turn:
character_goal_per_turn:
relationship_or_information_change:
verdict: PASS | FAIL | HOLD
failure_code:
```

## Action-beat-spam check

```text
location:
added_or_existing_beats:
which_beat_changes_reading:
which_beat_is_decoration_only:
verdict:
```

## Final G6D verdict

```text
V3-G6D: PASS | FAIL | HOLD
open_blockers:
open_majors:
protected_strengths:
next_action:
```

A numeric score is not evidence. A schema-complete form is not evidence. Every PASS must cite located manuscript evidence.
