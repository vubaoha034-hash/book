# Microcraft Dialogue / Local Logic Audit V1.1

## Scope

Manuscript / scene:
Audit mode: DEVELOPMENT | PRE_DELIVERY | REGRESSION
Reviewer context: SAME_CONTEXT | FRESH_CONTEXT | HUMAN
Machinery commit / rule version:

## Coverage declaration

```text
full_manuscript_scanned: true | false
ordinary_dialogue_starts_sampled:
high_information_turns_sampled:
rhetorical_ladders_sampled:
known_answers_or_regression_cases_read: true | false
```

Do not sample only climaxes. Casual early/mid-scene exposition and banter must be represented.

## Dialogue Trigger Anchor records

### DTA-001

```text
location:
speaker:
listener:
scene_state:
immediate_trigger:
trigger_textual_evidence:
speaker_perception:
non_speech_reaction_or_NONE:
why_speak_now:
speaker_in_scene_goal:
speaker_goal_textual_evidence:
listener_already_knows:
atomic_information_claims:
  - claim:
    listener_knows: YES | NO | PARTIAL
    listener_needs_now: YES | NO | UNCERTAIN
    speaker_reason_to_transmit_now:
    information_carrier:
    aftereffect:
reader_only_claim_count:
withheld_or_unsaid:
exact_bundle_no_reader_counterfactual: WOULD_SAY_THIS_BUNDLE | WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE | WOULD_NOT_SAY | UNCERTAIN
bluff_or_deflection_claimed: true | false
bluff_or_deflection_evidence_or_NONE:
non_speech_option_checked:
verdict: PASS | FAIL | HOLD
failure_code:
```

A PASS may not rely on an invented speaker goal. `speaker_goal_textual_evidence` is mandatory for high-information turns.

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

### ATS-001

```text
sequence_location:
sequence_shape:
turns:
  - turn:
    speaker_goal:
    speaker_goal_textual_evidence:
    state_delta:
    delta_type: KNOWLEDGE | CHOICE | TASK | RISK | RELATIONSHIP | CONCEALMENT | NEGOTIATION | NONE
    bluff_or_deflection_evidence_or_NONE:
block_level_aftereffect:
empty_scaffold_turn_count:
verdict: PASS | FAIL | HOLD
failure_code:
```

Do not let a useful final line rescue empty middle turns. Humor/rhythm alone is not `state_delta`.

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
exact_bundle_mouthpiece_failures:
per_turn_dialogue_template_failures:
semantic_chain_failures:
protected_strengths:
next_action:
```

A numeric score is not evidence. A schema-complete form is not evidence. Every PASS must cite located manuscript evidence; every claimed speaker goal must cite textual support.
