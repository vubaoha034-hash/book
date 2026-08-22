# Dialogue Trigger Anchor Module V1

## Purpose

Audit whether important dialogue is produced by the live scene and the speaker's purpose rather than by the author's need to brief, entertain, or transition the reader.

This module does **not** require an action beat before every utterance.

## Unit of analysis

Audit dialogue starts and high-information turns, not every quotation mark mechanically.

A dialogue start includes:

- first utterance after a scene/beat transition;
- a new topic introduced inside an existing exchange;
- a line that transfers critical backstory/rule/plan information;
- an emotionally decisive admission, refusal, accusation, promise or request.

## Required record

For each audited turn:

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
verdict:
failure_code:
```

## Three mandatory tests

### Test A — Why now?

The line must have a credible current trigger. A generic desire to “explain context” is not a trigger.

### Test B — No-reader counterfactual

Imagine no reader exists. Would the speaker still choose to say approximately this information, at this time, to this listener?

- YES: continue.
- NO: `AUTHOR_INFORMATION_MOUTHPIECE_FAIL` unless a strong in-scene carrier exists.
- UNCERTAIN: HOLD and inspect speaker goal/listener knowledge.

### Test C — Aftereffect

What changes because the listener heard it?

Valid effects include knowledge, action, choice, relationship pressure, permission, risk, negotiation position, misdirection, refusal, or deliberate non-change that itself has dramatic meaning.

If nothing changes and the main payoff is reader orientation or a tidy joke, flag it.

## Listener-knowledge test

Do not let characters explain shared background to one another solely for the reader.

When listener already knows most of a fact bundle, ask whether the speaker is:

- accusing;
- reminding as leverage;
- testing loyalty/memory;
- reframing shared facts;
- deliberately humiliating;
- issuing a warning whose force depends on restating the fact.

If none apply, compress, relocate, or delete.

## Non-speech alternatives

Before writing or accepting a reply, explicitly consider:

- silence;
- delayed answer;
- incomplete answer;
- interruption;
- deflection;
- visible action;
- change of subject;
- lie;
- refusal to explain.

Do not force non-speech behavior. Record `NONE` when direct speech is genuinely the best choice.

## Anti-template check

Flag a multi-line exchange if it follows a neat conversational scaffold while producing no state change. Common warning form:

`Q -> clever retort -> Q -> punchline`

Do not ban banter. Ban **banter that exists only because the writer wants a polished exchange**.

## Repair order

1. Delete the unnecessary line.
2. Move information to an actual trigger/evidence moment.
3. Change the speaker's in-scene goal so the information has a reason to be said.
4. Let the listener discover/ask from evidence.
5. Use silence/partial answer/deflection if character pressure supports it.
6. Only then consider wording.

## Anti-fix

Never repair lack of grounding by adding generic gestures before each quote. `ACTION_BEAT_SPAM_AS_FAKE_GROUNDING` is itself a failure.
