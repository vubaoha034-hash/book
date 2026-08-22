# Microcraft Dialogue / Local Logic Audit V1.2

## Scope

Manuscript / scene:
Audit mode: DEVELOPMENT | PRE_DELIVERY | REGRESSION
Reviewer context: SAME_CONTEXT | FRESH_CONTEXT | HUMAN
Machinery version / commit:

## Pass 1 — Candidate inventory

```text
candidate_inventory_count:
candidate_audited_count:
candidate_omitted_count:
omitted_candidates_and_reason:
public_background_bundle_candidates:
social_anecdote_candidates:
rhetorical_ladder_candidates:
ordinary_early_mid_candidates:
coverage_complete: true | false
```

Inventory every turn/block that meets the frozen candidate-harvest criteria before judging any candidate.

A PRE_DELIVERY or REGRESSION audit cannot PASS with `coverage_complete=false`.

## Dialogue Trigger Anchor records

### DTA-001

```text
location:
speaker:
listener:
scene_state:
bundle_type: TASK_OR_CONFLICT_INFORMATION | PUBLIC_BACKGROUND_ORIENTATION | SOCIAL_ANECDOTE_OR_RELATIONSHIP_STORY | MIXED | UNCERTAIN
immediate_trigger:
trigger_textual_evidence:
speaker_perception:
non_speech_reaction_or_NONE:
why_speak_now:
speaker_in_scene_goal:
speaker_goal_textual_evidence:
listener_already_knows:
atomic_information_claims:
listener_need_per_claim:
information_carrier_per_claim:
reader_only_claim_count:
social_value_or_NONE:
social_value_textual_evidence_or_NONE:
withheld_or_unsaid:
aftereffect_per_claim_or_turn:
exact_bundle_no_reader_counterfactual: WOULD_SAY_THIS_BUNDLE | WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE | WOULD_NOT_SAY | UNCERTAIN
bluff_or_deflection_claimed: true | false
bluff_or_deflection_evidence_or_NONE:
non_speech_option_checked:
verdict: PASS | FAIL | HOLD
failure_code:
```

Duplicate for each harvested candidate.

## Public-background bundle audit

For any turn combining several of event/time/listener-role/reward/rumor/outsider-count/route/rule facts:

```text
location:
claim_count:
claims_listener_already_knows:
claims_listener_needs_now:
claims_with_text_supported_transmission_goal:
claims_whose_main_beneficiary_is_reader:
one_new_claim_rescuing_bundle_attempted: true | false
exact_bundle_verdict:
verdict:
failure_code:
```

## Social anecdote audit

For a possible anecdote/gossip/relationship story:

```text
location:
directly_responsive_to_person_or_event_question:
firsthand_or_owned_story:
relationship_supports_social_sharing:
scene_has_room_for_social_detail:
mainly_restates_listener_own_mission_or_setup:
voice_or_relationship_value:
reader_orientation_payload_present:
verdict:
```

Do not fail social detail merely because it is not task-essential.

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
turn_1_state_delta:
turn_2_state_delta:
turn_3_state_delta:
turn_4_state_delta:
character_goal_per_turn:
bluff_or_deflection_evidence_or_NONE:
relationship_or_information_change:
empty_scaffold_turn_count:
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
coverage_complete:
candidate_inventory_count:
candidate_audited_count:
public_background_bundle_failures:
social_anecdote_false_positive_risks:
per_turn_template_failures:
semantic_chain_failures:
open_blockers:
open_majors:
protected_strengths:
next_action:
```

A numeric score is not evidence. A schema-complete form is not evidence. Every PASS must cite located manuscript evidence.
