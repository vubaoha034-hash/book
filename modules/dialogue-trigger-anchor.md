# Dialogue Trigger Anchor Module V1.2

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
```

For these candidate classes, a regression/pre-delivery audit is not allowed to sample selectively. If candidate harvesting is incomplete, final G6D cannot be PASS.

### Pass 2 — candidate judgment

Only after Pass 1 is complete, run the tests below.

## Unit of analysis

Audit dialogue starts, high-information turns, suspicious rhetorical ladders, and harvested ordinary exposition candidates. Do not only inspect climax speeches.

A dialogue audit target includes:

- first utterance after a scene/beat transition;
- a new topic introduced inside an existing exchange;
- a line that transfers critical backstory/rule/plan information;
- an emotionally decisive admission, refusal, accusation, promise or request;
- an ordinary-looking line that bundles several facts for the listener;
- a neat multi-turn exchange whose middle turns may exist only to set up a joke or reveal;
- a first-hand anecdote whose purpose may be social/relationship rather than task information.

## Required record

For each audited candidate:

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

## Test A — Why now, with textual evidence?

The line must have a credible current trigger.

A reviewer must cite evidence for the trigger and speaker goal. A plausible but unsupported motive invented by the reviewer is not evidence.

If the only reason is “the author needs this information now”, fail or hold.

## Test B — Exact-bundle no-reader counterfactual

Do not ask whether the speaker would say *something*.

Ask whether the speaker would say approximately **this complete bundle** to this listener at this moment if no reader existed.

Record one of:

- `WOULD_SAY_THIS_BUNDLE`
- `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE`
- `WOULD_NOT_SAY`
- `UNCERTAIN`

For `PUBLIC_BACKGROUND_ORIENTATION`, `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE` is strong failure evidence.

For `SOCIAL_ANECDOTE_OR_RELATIONSHIP_STORY`, practical listener need is not required claim-by-claim; use the social-anecdote test below.

## Test C — Atomic information bundle

Split multi-fact exposition into atomic claims.

For every claim, identify:

- listener already knows / does not know;
- listener currently needs / does not need;
- speaker has a text-supported reason / no supported reason to transmit it now;
- actual aftereffect.

For public-background/current-mission bundles, one legitimate trailing fact does not rescue several reader-orientation facts.

Mandatory high-risk pattern:

- central event or timing;
- listener's own role;
- reward/stakes already known to listener;
- rumor spread;
- number/location of outsiders;

When several appear in one turn, audit the entire turn even if it looks like casual warning or gossip.

## Test D — Social anecdote / relationship story

Do not classify ordinary human storytelling as mouthpiece merely because the listener could function with a shorter answer.

A social anecdote may PASS when there is located evidence that:

- it directly answers or naturally expands a question about a person/event;
- the speaker personally witnessed or plausibly owns the story;
- the relationship supports gossip, teasing, recollection or amusement;
- the scene has room for that social behavior;
- the anecdote does not mainly restate the listener's own mission/setup;
- the details produce voice, relationship texture or a shared reaction rather than covert reader orientation.

A social anecdote does **not** need each factual atom to change task state.

If the candidate is partly anecdote and partly plot orientation, classify `MIXED` and audit the plot-orientation claims separately.

## Test E — Per-turn state delta

For a neat exchange, evaluate every turn instead of only the conversation's final effect.

A turn passes when it changes or deliberately manipulates:

- knowledge;
- choice;
- action/task state;
- risk;
- relationship permission or pressure;
- concealment/misdirection;
- negotiation position.

“Sounds like the character”, “is funny”, “keeps rhythm”, or “sets up the next question” are not state deltas by themselves.

If a retort mainly manufactures the next follow-up or punchline, flag `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE` unless a supported bluff/deflection/relationship goal is present.

A later useful line does not retroactively justify empty scaffold turns.

## Test F — Aftereffect

What changes because this listener heard this specific line or claim?

Block-level aftereffect cannot retroactively justify empty scaffold turns.

For a social anecdote, valid aftereffect may be a relationship reaction, shared amusement, revised impression, embarrassment, memory pressure or permission—not only task change.

## Listener-knowledge test

Do not let characters explain shared plot background to one another solely for the reader.

When the listener already knows most of a **public-background/current-mission** fact bundle, PASS requires a text-supported scene purpose such as:

- accusation;
- leverage;
- warning;
- testing loyalty or memory;
- reframing;
- humiliation;
- command;
- testimony;
- teaching required for immediate action.

Do not apply this rule mechanically to a first-hand anecdote whose purpose is social rather than briefing.

## Bluff / deflection test

Do not automatically excuse a contradictory or evasive line as bluffing.

Bluff/deflection is valid only when scene pressure or later behavior supports a goal such as deterrence, concealment, face-saving, provocation, or protection.

Unsupported “maybe bluffing” is a reviewer rescue, not manuscript evidence.

## Non-speech alternatives

Before accepting a reply, explicitly consider:

- silence;
- delayed answer;
- incomplete answer;
- interruption;
- deflection;
- visible action;
- change of subject;
- lie;
- refusal to explain.

Do not force non-speech behavior. Record `NONE` when direct speech is genuinely best.

## Repair order

1. Confirm the candidate was harvested correctly.
2. For public-background bundles, delete or separate unnecessary claims.
3. Move plot information to an actual trigger/evidence moment.
4. Let the listener discover/ask from evidence.
5. Give the speaker a scene goal only if the story already supports it.
6. Preserve legitimate social anecdote/relationship texture unless it also carries reader-only setup.
7. Use silence/partial answer/deflection where pressure supports it.
8. Only then consider wording.

## Anti-fix

Never repair lack of grounding by adding generic gestures before each quote. `ACTION_BEAT_SPAM_AS_FAKE_GROUNDING` is itself a failure.
