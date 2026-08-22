# Dialogue Trigger Anchor Module V1.3

## Purpose

Audit whether important dialogue is produced by the live scene and the speaker's purpose rather than by the author's need to brief, entertain, or transition the reader.

This module does **not** require an action beat before every utterance.

## Two-pass audit structure

### Pass 1 — candidate harvest

Before judging any dialogue, inventory every located candidate that meets at least one trigger:

- a turn contains 3+ independently checkable factual claims;
- a turn combines current event, timing, listener role, reward/stakes, rumor spread, arrival count, route, rule or consequence information;
- a speaker tells the listener facts about the listener's own mission or role;
- a new topic is opened mainly through dialogue;
- a rhetorical ladder resembles `Q -> retort -> follow-up -> punchline`;
- an ordinary early/mid-scene line carries plot setup while appearing casual;
- a high-information line may be a social anecdote rather than exposition.

Record every candidate before deciding PASS/FAIL/HOLD.

Required coverage fields:

```text
candidate_inventory_count:
candidate_audited_count:
candidate_omitted_count:
omitted_candidates_and_reason:
public_background_bundle_candidates:
social_anecdote_candidates:
rhetorical_ladder_candidates:
rhetorical_ladder_candidate_count:
```

For PRE_DELIVERY / REGRESSION, selective sampling is not allowed for these candidate classes.

### Pass 2 — candidate judgment

Only after Pass 1 is complete, run the tests below.

Every harvested rhetorical ladder must receive an explicit anti-template record. Final G6D cannot PASS unless:

`rhetorical_ladder_candidate_count == anti_template_record_count`

If not, use `RHETORICAL_LADDER_AUDIT_INCOMPLETE`.

## Unit of analysis

Audit dialogue starts, high-information turns, suspicious rhetorical ladders, harvested ordinary exposition candidates, and possible social anecdotes. Do not only inspect climax speeches.

## Required DTA record

For each audited information/dialogue candidate:

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
exact_bundle_no_reader_counterfactual:
bluff_or_deflection_claimed: true | false
bluff_or_deflection_evidence_or_NONE:
non_speech_option_checked:
verdict:
failure_code:
```

## Required anti-template record — one per harvested rhetorical ladder

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
portable_generic_joke_risk: true | false
relationship_or_task_specificity_evidence_or_NONE:
bluff_or_deflection_evidence_or_NONE:
empty_scaffold_turn_count:
verdict: PASS | FAIL | HOLD
failure_code:
```

## Test A — Why now, with textual evidence?

The line must have a credible current trigger. A reviewer must cite evidence for trigger and speaker goal. A plausible but unsupported motive is not evidence.

## Test B — Exact-bundle no-reader counterfactual

Ask whether the speaker would say approximately this complete bundle to this listener at this moment if no reader existed.

For `PUBLIC_BACKGROUND_ORIENTATION`, `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE` is strong failure evidence.

For `SOCIAL_ANECDOTE_OR_RELATIONSHIP_STORY`, practical listener need is not required claim-by-claim; use the social-anecdote test.

## Test C — Atomic information bundle

Split multi-fact exposition into atomic claims. For every claim, identify listener knowledge, listener need, text-supported transmission goal, and actual aftereffect.

For public-background/current-mission bundles, one legitimate trailing fact does not rescue several reader-orientation facts.

## Test D — Social anecdote / relationship story

A social anecdote may PASS when there is located evidence that it naturally answers/expands a person-event question, is owned by the speaker, fits the relationship and scene pressure, does not mainly restate the listener's own mission/setup, and creates voice/relationship texture rather than reader orientation.

## Test E — Per-turn state delta

For every harvested rhetorical ladder, evaluate every turn and emit the dedicated anti-template record.

A valid state delta changes or deliberately manipulates knowledge, choice, task/action state, risk, relationship permission/pressure, concealment/misdirection, or negotiation position.

“Sounds like the character”, “is funny”, “keeps rhythm”, “made the listener briefly wonder”, or “sets up the next question” are not sufficient by themselves.

### E1 — Self-cancelling assertion

If a retort introduces or strongly implies proposition P and later turns immediately reveal the speaker has no basis for P, do not count the temporary belief in P as a meaningful delta unless a text-supported bluff, concealment, deterrence, face-saving, provocation, protection, relationship or task goal exists.

### E2 — Induced-follow-up dependency

Flag when the next question exists mainly because the retort manufactured an uncertainty/false premise that the punchline immediately retracts or nullifies, with no independent scene goal.

### E3 — Counterfactual turn deletion

Mentally remove the suspicious retort and its induced follow-up.

If the scene can move directly to the truthful/useful line with no loss of task information, necessary knowledge, relationship pressure, concealment, negotiation or character-specific history—and only generic joke cadence is lost—the removed turns are template-risk.

### E4 — Portability

If a retort/punchline could be moved to unrelated characters and situations nearly unchanged, mark portable-joke risk. Portability alone is not automatic FAIL, but it cannot substitute for character motive.

Relationship-specific banter may PASS when shared history, current object/task, prior grievance, status asymmetry or later relationship action is located.

## Test F — Aftereffect

Block-level aftereffect cannot retroactively justify empty scaffold turns. A later useful line does not rescue an earlier turn that existed only to manufacture the next question.

## Listener-knowledge test

Do not let characters explain shared plot background to one another solely for the reader. Do not apply this mechanically to first-hand social anecdotes.

## Bluff / deflection test

Bluff/deflection is valid only when scene pressure or later behavior supports deterrence, concealment, face-saving, provocation or protection. Unsupported “maybe bluffing” is reviewer rescue.

## Non-speech alternatives

Before accepting a reply, explicitly consider silence, delayed answer, incomplete answer, interruption, deflection, visible action, change of subject, lie or refusal to explain.

## Repair order

1. Confirm candidate harvest and rhetorical-ladder record parity.
2. Delete empty scaffold turns before rewriting wording.
3. Separate reader-only public-background claims from legitimate lines.
4. Preserve legitimate social anecdote/relationship texture.
5. Move information to a real trigger/evidence moment.
6. Use silence/partial answer/deflection where pressure supports it.
7. Only then consider wording.

## Anti-fix

Never repair lack of grounding by adding generic gestures before each quote. `ACTION_BEAT_SPAM_AS_FAKE_GROUNDING` is itself a failure.
