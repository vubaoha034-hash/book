# Dialogue Trigger Anchor Module V1.4

## Purpose

Audit whether important dialogue is produced by the live scene and the speaker's purpose rather than by the author's need to brief, entertain or transition the reader.

This module does not require an action beat before every utterance.

## Two-pass structure

### Pass 1 — candidate harvest

Inventory every located candidate that meets at least one trigger:

- a turn contains 3+ independently checkable factual claims;
- a turn combines event/timing/listener role/reward/rumor spread/arrival count/route/rule/consequence information;
- a speaker tells the listener facts about the listener's own mission or role;
- a new topic is opened mainly through dialogue;
- a rhetorical ladder resembles `Q -> retort -> follow-up -> punchline`;
- an ordinary early/mid-scene line carries plot setup while appearing casual;
- a high-information line may be social anecdote rather than exposition;
- a line reports who else knows a fact, what rumor says, or how public exposure changes risk.

Record every candidate before deciding PASS/FAIL/HOLD.

### Pass 2 — judgment

Every harvested information/dialogue candidate gets a DTA record. Every harvested rhetorical ladder gets a dedicated ATS record.

For PRE_DELIVERY / REGRESSION:

`rhetorical_ladder_candidate_count == anti_template_record_count`

Otherwise use `RHETORICAL_LADDER_AUDIT_INCOMPLETE`.

## Required DTA record

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
listener_public_knowledge_before:
reported_rumor_content:
rumor_source_or_evidence:
exposure_or_spread_evidence:
actionable_risk_from_public_knowledge:
epistemic_payload_delta:
embedded_repetition_required_to_identify_meta_claim:
atomic_information_claims:
reader_only_residue:
social_value_or_NONE:
withheld_or_unsaid:
aftereffect_per_claim_or_turn:
exact_bundle_no_reader_counterfactual:
non_speech_option_checked:
g8_pattern_family_candidate: true | false
verdict: PASS | FAIL | HOLD
failure_code:
```

## Test A — Why now?

The trigger and speaker goal require located textual evidence. A plausible motive invented by the reviewer is not evidence.

## Test B — Epistemic scope before mouthpiece verdict

Read `modules/dialogue-epistemic-scope.md`.

Do not flatten:

```text
listener knows X
outsiders know X
listener knows outsiders know X
speaker reports what outsiders are saying about X
visible exposure/risk caused by outsiders knowing X
```

These can be different knowledge states.

A character may repeat X to identify the content of a rumor or warning. Do not count that embedded repetition as reader-only automatically.

If the public/exposure claim lacks evidence, use HOLD rather than inventing evidence.

## Test C — Pure shared-background mouthpiece

Use `AUTHOR_INFORMATION_MOUTHPIECE_FAIL` when:

- listener already knows the object facts;
- there is no new public/reported knowledge or exposure/risk payload;
- there is no accusation, reframing, negotiation, teaching, misunderstanding, relationship act or practical task purpose;
- the repeated facts mainly orient the reader.

If a real epistemic payload exists but the line is over-complete, route pure economy/naturalness residue to G8/de-AI unless the residue independently breaks information-carrier truthfulness.

## Test D — Social anecdote

A social anecdote may PASS when it naturally answers/expands a person-event question, is owned by the speaker, fits the relationship and scene pressure, and creates voice/relationship texture rather than covert reader orientation.

A social anecdote does not need each factual atom to change task state.

## Required ATS record — one per harvested rhetorical ladder

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
self_cancelling_assertion_present:
assertion_created:
next_turn_retracts_or_nullifies:
induced_followup_dependency:
counterfactual_turn_deletion_result:
portable_generic_joke_risk:
relationship_or_task_specificity_evidence_or_NONE:
bluff_or_deflection_evidence_or_NONE:
empty_scaffold_turn_count:
g8_pattern_family_candidate: true | false
verdict: PASS | FAIL | HOLD
failure_code:
```

## Calibrated ATS judgment

Turn deletion, portability and self-cancellation are diagnostic evidence, not automatic hard-fail switches.

A locally plausible, noncritical joke/deflection may PASS or HOLD G6D when scene pressure, fear, relationship permission, status or other textual evidence supports it—even if a shorter version exists.

Use `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE` only when the local exchange is independently ungrounded/materially misleading, such as:

- no supported goal or relationship pressure;
- critical information is delayed behind empty scaffold turns;
- a false premise exists solely to induce the next question;
- no independent scene value remains beyond portable cadence.

If local grounding is adequate but portability/generic cadence remains suspicious, set `g8_pattern_family_candidate=true` and defer density judgment to `modules/dialogue-pattern-family-density.md`.

## Non-speech alternatives

Before accepting a reply, consider silence, delayed answer, incomplete answer, interruption, deflection, visible action, change of subject, lie or refusal.

## Repair order

1. Resolve deterministic local semantic failures.
2. Confirm epistemic scope before deleting repeated known facts.
3. Remove pure reader-only shared setup.
4. Preserve legitimate social anecdote and locally grounded banter.
5. Route portable/generic but locally plausible cadence to G8 family analysis.
6. Only then consider wording.

## Anti-fix

Never repair lack of grounding by adding generic gestures before each quote. `ACTION_BEAT_SPAM_AS_FAKE_GROUNDING` remains a failure.
