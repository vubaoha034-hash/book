# MICROCRAFT + DIALOGUE + LOCAL LOGIC UPGRADE V1

Status: DEVELOPMENT / TWO-BOOK RAW EVIDENCE / BOOK-01 RAW REVALIDATION HOLD

## Why this exists

The previous V3 stack could validate macro causality, continuity, emotion/payoff and de-AI patterns while still missing local prose failures that a human reader immediately notices. A real-manuscript freeze was invalidated after three failures survived multiple reviews:

- a relative-time contradiction carried through a semantic spending list;
- dialogue whose main beneficiary was the reader rather than the addressed character;
- a neat question/retort/follow-up/punchline exchange with no character-motive or state change.

The fix is not a larger list of stylistic advice. This upgrade adds evidence-bearing microcraft gates.

## Evidence basis and limitation

Private source analysis currently contains 30 abstract Scene-to-Speech samples from BOOK-02 and 30 from BOOK-03. The canonical repaired BOOK-01 source remains proven by work ID/hash but is not readable in the current private access plane; therefore V1 may be integrated as a two-book-evidence architecture but MUST NOT be described as full three-book raw microcraft validation.

No copyrighted source-book passages are stored in this public repository.

## Core model

Dialogue is not required to have an action beat before every line. The required question is whether the speech is grounded in the live scene.

Preferred reasoning chain:

`SCENE STATE -> TRIGGER -> PERCEPTION -> NON-SPEECH REACTION -> SPEECH -> AFTEREFFECT`

Steps may be implicit or skipped. The hard requirement is that important speech can answer: **why this person says this now, to this listener, for an in-scene purpose**.

## Seven V1 microcraft mechanisms

### MC-C01 Dialogue Trigger Anchor

For important dialogue starts, locate at least one legitimate trigger:

- event/change;
- perception or evidence;
- current task;
- relationship pressure;
- silence/avoidance;
- misunderstanding;
- object/resource state;
- newly received information.

A trigger is not decoration. Adding a glance, sigh or hand movement solely to satisfy the gate is a failure.

### MC-C02 Scene-to-Speech Chain

Audit the causal path from the scene to the utterance. If the line could be dropped into a different scene without changing its reason for being said, it may be generic exposition or dialogue scaffolding.

### MC-C03 Non-Speech Decision

Before writing a reply, test whether the character would more credibly:

- stay silent;
- delay;
- interrupt;
- deflect;
- answer only part of the question;
- act instead of answer;
- leave something unsaid because the listener already knows it or because saying it has a cost.

Complete verbal answers are not the default.

### MC-C04 Information Must Have an In-Scene Carrier

Background information is legitimate when the speaker has a scene-level reason to deliver it: persuade, warn, test, accuse, request, negotiate, deceive, teach because action requires it, or respond to evidence.

High-risk mouthpiece conditions:

1. listener already knows the information;
2. speaker gains nothing in-scene by stating it;
3. the line bundles multiple background facts for reader orientation;
4. deleting it mostly deprives the reader, not the characters;
5. the next action does not depend on the listener receiving it.

### MC-C05 Dialogue Ping-Pong Is Not Scene Progress

Flag tidy sequences such as:

`question -> retort -> follow-up question -> neat punchline`

when the sequence changes none of:

- information state;
- decision;
- relationship pressure;
- access/permission;
- risk;
- immediate task.

Banter is allowed. Empty symmetry is not.

### MC-C06 Local Semantic Time Chain

Timeline checking must propagate time through semantic relations, not only literal adjacent sentences.

For every important time-bearing chain record:

- anchor event/time;
- relation to the next clause/list/action;
- inherited time scope;
- explicit scope break if any;
- later fact;
- contradiction status.

Example abstraction: if a scene establishes `last night: money acquired`, then asks where that money went and begins a spending list, list items inherit the last-night spending scope unless the text explicitly opens a different scope. A later statement that one listed item happened two days earlier is a deterministic contradiction.

### MC-C07 Do Not Action-Beat Spam

A failed dialogue anchor is NOT repaired by mechanically inserting `looked`, `sighed`, `touched`, `paused` or similar beats. The repair must change one of:

- actual trigger;
- speaker goal;
- information carrier;
- omission/silence choice;
- sequence/state change;
- semantic time relation.

If no credible repair exists, delete the line or redesign the exchange.

## Production audit record

For each high-information or high-emotion dialogue start, the audit records:

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
semantic_time_scope:
verdict: PASS | FAIL | HOLD
failure_code:
```

## Hard questions

1. Why exactly now?
2. If there were no reader, would the character still say this?
3. Does the line materially affect the addressed character or scene, or mainly inform the reader?
4. Could silence, partial answer, deflection or action be more character-true?
5. Does any relative-time phrase inherit into a list, pronoun, money/object chain or later explanation?

## Failure codes

V1 locks at least:

- `TEMPORAL_SEMANTIC_CHAIN_FAIL`
- `AUTHOR_INFORMATION_MOUTHPIECE_FAIL`
- `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`
- `CRITICAL_DIALOGUE_HAS_NO_TRIGGER_OR_GOAL`
- `ACTION_BEAT_SPAM_AS_FAKE_GROUNDING`

## Relationship to existing V3 gates

This upgrade does not replace macro causality or continuity. It adds a dedicated `V3-G6D` gate between continuity evidence and final revision/de-AI delivery.

- G1 asks whether events follow causal logic.
- G6 asks whether facts/time/objects/knowledge/rules remain consistent.
- **G6D asks whether local semantic scope and dialogue are grounded in the live scene.**
- G8 de-AI cannot compensate for a G6D failure.

## Copyright and style boundary

Source-book analysis transfers abstract mechanisms only. Do not copy source dialogue, plot chains, signature objects, scene order, or author-specific prose style into generation context.

## Promotion boundary

V1 architecture may be used developmentally on the strength of current evidence plus regression failures. Full claim that the mechanism has been independently revalidated across all three canonical source books remains blocked until the canonical repaired BOOK-01 source is readable and sampled with the same protocol.
