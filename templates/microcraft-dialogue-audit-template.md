# Microcraft Dialogue / Local Logic Audit V1.4

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
rhetorical_ladder_candidate_count:
epistemic_scope_candidates:
ordinary_early_mid_candidates:
coverage_complete: true | false
```

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
why_speak_now:
speaker_in_scene_goal:
speaker_goal_textual_evidence:
object_facts:
listener_object_fact_knowledge:
speaker_claim_about_public_knowledge:
listener_public_knowledge_before: KNOWN | UNKNOWN | UNCERTAIN | NOT_APPLICABLE
reported_rumor_content:
rumor_source_or_evidence:
exposure_or_spread_evidence:
actionable_risk_from_public_knowledge:
epistemic_payload_delta:
embedded_repetition_required_to_identify_meta_claim: true | false | uncertain
atomic_information_claims:
reader_only_residue:
social_value_or_NONE:
withheld_or_unsaid:
aftereffect_per_claim_or_turn:
exact_bundle_no_reader_counterfactual: WOULD_SAY_THIS_BUNDLE | WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE | WOULD_NOT_SAY | UNCERTAIN
non_speech_option_checked:
g8_pattern_family_candidate: true | false
verdict: PASS | FAIL | HOLD
failure_code:
```

Duplicate for each harvested candidate as required.

## Epistemic-scope audit

```text
location:
object_fact:
listener_object_fact_knowledge:
public_knowledge_proposition:
listener_public_knowledge_before:
reported_rumor_content:
rumor_source_or_evidence:
exposure_or_spread_evidence:
actionable_risk_from_public_knowledge:
epistemic_payload_delta:
embedded_repetition_required_to_identify_meta_claim:
reader_only_residue:
verdict: PASS | FAIL | HOLD
failure_code:
```

Do not treat `listener knows X` as equivalent to `listener knows outsiders know X`.

## Pure shared-background mouthpiece audit

```text
location:
claims_listener_already_knows:
new_object_fact_payload:
new_public_or_reported_knowledge_payload:
new_exposure_or_risk_payload:
other_scene_function:
claims_whose_main_beneficiary_is_reader:
verdict:
failure_code:
```

`AUTHOR_INFORMATION_MOUTHPIECE_FAIL` requires absence of a distinct scene/epistemic payload, not merely repetition of known object words.

## Social anecdote audit

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

## Anti-template scan — one record per harvested rhetorical ladder

Before final verdict:

```text
rhetorical_ladder_candidate_count:
anti_template_record_count:
rhetorical_ladder_record_parity: PASS | FAIL
```

If counts differ, use `RHETORICAL_LADDER_AUDIT_INCOMPLETE`.

### ATS-001

```text
candidate_id:
sequence_location:
sequence_shape:
turn_1_claim_or_function:
turn_1_state_delta:
turn_1_goal_textual_evidence:
turn_2_claim_or_function:
turn_2_state_delta:
turn_2_goal_textual_evidence:
turn_3_claim_or_function:
turn_3_state_delta:
turn_3_goal_textual_evidence:
turn_4_claim_or_function:
turn_4_state_delta:
turn_4_goal_textual_evidence:
self_cancelling_assertion_present: true | false
assertion_created:
next_turn_retracts_or_nullifies: true | false
induced_followup_dependency: true | false
counterfactual_turn_deletion_result:
portable_generic_joke_risk: LOW | MEDIUM | HIGH
relationship_or_task_specificity_evidence_or_NONE:
bluff_or_deflection_evidence_or_NONE:
empty_scaffold_turn_count:
g8_pattern_family_candidate: true | false
verdict: PASS | FAIL | HOLD
failure_code:
```

A removable turn is not automatically a hard G6D failure. Local hard FAIL requires independent evidence of ungrounded/materially misleading dialogue. Portable but locally plausible cadence should be routed to G8 family analysis.

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
epistemic_scope_candidate_count:
rhetorical_ladder_candidate_count:
anti_template_record_count:
rhetorical_ladder_record_parity:
pure_shared_background_mouthpiece_failures:
epistemic_scope_holds:
social_anecdote_false_positive_risks:
local_dialogue_template_failures:
g8_pattern_family_candidates:
semantic_chain_failures:
open_blockers:
open_majors:
protected_strengths:
next_action:
```

Numeric scores and schema completeness are not quality evidence. Every verdict requires located manuscript evidence.
