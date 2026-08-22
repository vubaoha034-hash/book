# Dialogue Trigger Anchor Module V1.1

## Purpose

Audit whether important dialogue is produced by the live scene and the speaker's purpose rather than by the author's need to brief, entertain, or transition the reader.

This module does **not** require an action beat before every utterance.

## Unit of analysis

Audit dialogue starts, high-information turns, and suspicious rhetorical ladders. Do not only inspect climax speeches.

A dialogue audit target includes:

- first utterance after a scene/beat transition;
- a new topic introduced inside an existing exchange;
- a line that transfers critical backstory/rule/plan information;
- an emotionally decisive admission, refusal, accusation, promise or request;
- an ordinary-looking line that bundles several facts for the listener;
- a neat multi-turn exchange whose middle turns may exist only to set up a joke or reveal.

## Required record

For each audited high-impact or high-information turn:

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
listener_need_per_claim:
information_carrier_per_claim:
reader_only_claim_count:
withheld_or_unsaid:
aftereffect_per_claim_or_turn:
exact_bundle_no_reader_counterfactual:
bluff_or_deflection_claimed: true | false
bluff_or_deflection_evidence_or_NONE:
non_speech_option_checked:
verdict:
failure_code:
```

## Mandatory tests

### Test A — Why now, with textual evidence?

The line must have a credible current trigger.

A reviewer must cite evidence for the trigger and the speaker goal. A plausible but unsupported motive invented by the reviewer is not evidence.

If the only reason is “the author needs this information now”, fail or hold.

### Test B — Exact-bundle no-reader counterfactual

Do not ask whether the speaker would say *something*.

Ask whether the speaker would say approximately **this complete bundle** to this listener at this moment if no reader existed.

Record one of:

- `WOULD_SAY_THIS_BUNDLE`
- `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE`
- `WOULD_NOT_SAY`
- `UNCERTAIN`

If the result is `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE`, inspect for `AUTHOR_INFORMATION_MOUTHPIECE_FAIL`.

### Test C — Atomic information bundle

Split multi-fact exposition into atomic claims.

For every claim, identify:

- listener already knows / does not know;
- listener currently needs / does not need;
- speaker has a text-supported reason / no supported reason to transmit it now;
- actual aftereffect.

If several claims mainly orient the reader and are not needed by the listener, the existence of one legitimate claim does not rescue the full bundle.

### Test D — Per-turn state delta

For a neat exchange, evaluate every turn instead of only the conversation's final effect.

A turn passes when it changes or deliberately manipulates:

- knowledge;
- choice;
- action/task state;
- risk;
- relationship permission or pressure;
- concealment/misdirection;
- negotiation position.

“Sounds like the character”, “is funny”, “keeps rhythm”, or “sets up the next question” are not state deltas.

If a retort mainly manufactures the next follow-up or punchline, flag `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE` unless a supported bluff/deflection/relationship goal is present.

### Test E — Aftereffect

What changes because this listener heard this specific line or claim?

Block-level aftereffect cannot retroactively justify empty scaffold turns.

## Listener-knowledge test

Do not let characters explain shared background to one another solely for the reader.

When listener already knows most of a fact bundle, PASS requires a text-supported scene purpose such as:

- accusation;
- leverage;
- warning;
- testing loyalty or memory;
- reframing;
- humiliation;
- command;
- testimony;
- teaching required for immediate action.

If the listener knows the fact and no such purpose is evidenced, compress, relocate, or delete.

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

1. Delete the unnecessary turn or claim.
2. Separate unrelated information from a legitimate line.
3. Move information to an actual trigger/evidence moment.
4. Let the listener discover/ask from evidence.
5. Give the speaker a real scene goal only if the story already supports it.
6. Use silence/partial answer/deflection where pressure supports it.
7. Only then consider wording.

## Anti-fix

Never repair lack of grounding by adding generic gestures before each quote. `ACTION_BEAT_SPAM_AS_FAKE_GROUNDING` is itself a failure.
