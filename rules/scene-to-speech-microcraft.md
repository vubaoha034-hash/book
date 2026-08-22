# Scene-to-Speech Microcraft V1.1

## Principle

Do not write dialogue as a self-contained sequence of clever lines. Ground important speech in the scene that produces it.

Useful model:

`scene state -> trigger -> perception -> non-speech reaction -> speech -> aftereffect`

This is a reasoning model, not a prose template. Any step may be implicit or absent when the scene remains intelligible.

## Dialogue Trigger Anchor

An important line should normally have at least one of these anchors:

- a new event or change;
- something seen/heard/felt;
- a current practical task;
- a relationship pressure or social risk;
- a silence or refusal that has become meaningful;
- a misunderstanding;
- an object/resource state;
- new information or evidence.

Do not invent empty action beats solely to manufacture an anchor.

## Textual-evidence burden for speaker goals

Do not pass a line merely because the reviewer can imagine a plausible reason for speaking.

For every high-information or high-impact turn, the claimed in-scene goal must have **located textual evidence** in the current beat, nearby relationship state, or current task.

Invalid reviewer inventions include unsupported claims such as:

- “the speaker is probably trying to lighten the mood”;
- “the speaker may be showing confidence”;
- “the speaker could be bluffing”;
- “the speaker wants to explain what happened”;

unless the manuscript provides evidence for that goal.

If a PASS depends on a goal that exists only in the reviewer’s imagination, use HOLD or FAIL according to the remaining evidence.

## Exact-bundle no-reader counterfactual

Do not ask only:

> Would this person say something here?

Ask instead:

> If no reader existed, would this person say **this approximate bundle of information, with this level of completeness, to this listener, now**?

A character may have a reason to speak but no reason to deliver every fact the author packed into the line.

Distinguish:

- `WOULD_SAY_THIS_BUNDLE`;
- `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE`;
- `WOULD_NOT_SAY`;
- `UNCERTAIN`.

`WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE` is not a PASS for exposition.

## Atomic information-bundle test

For any line that transfers multiple background facts, split it into atomic claims.

For each claim record:

1. does the listener already know it?
2. does the listener need it for an immediate choice, task, risk, negotiation, accusation, warning, test, or relationship action?
3. what textual evidence shows the speaker wants this listener to know it now?
4. what changes because this specific claim is heard?

If a bundle contains multiple claims whose main beneficiary is the reader, and the listener has no current need for them, flag `AUTHOR_INFORMATION_MOUTHPIECE_FAIL` even when one claim in the bundle is scene-grounded.

A legitimate warning may contain several facts, but the warning purpose must be visible in the scene and the facts must serve that warning.

## Listener knowledge

Shared facts do not need to be restated unless the act of restating has a scene function such as leverage, accusation, warning, mockery, ritual, reframing, testing memory, or forcing a choice.

“Both characters know it, but the reader does not” is evidence **against** a natural exposition line unless a real scene purpose is present.

## Non-speech is an option

A character may:

- remain silent;
- delay;
- answer partially;
- interrupt;
- change subject;
- lie;
- perform an action;
- fail to answer because the relationship makes the question costly.

Do not make every exchange complete and cooperative.

## Dialogue-template warning: per-turn delta

When several turns form a neat rhetorical ladder, do not evaluate only the block-level aftereffect. Audit **each turn**.

Especially inspect:

`question -> clever retort -> follow-up -> punchline`

For every turn ask what changed in:

- knowledge;
- decision;
- task state;
- risk;
- relationship permission/pressure;
- concealment or misdirection;
- negotiation position.

Humor, rhythm, personality color, or “keeping the conversation going” do not count by themselves.

If an intermediate retort exists mainly to manufacture the next question or punchline, and has no supported bluff/deflection/relationship goal, flag `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`.

A later useful line does not retroactively justify empty scaffold turns.

## Bluff / deflection evidence

A seemingly false, evasive, or swaggering line can be natural when it serves a real goal such as deterrence, concealment, face-saving, provocation, or protecting someone.

But the manuscript must support that goal through scene pressure, later behavior, or relationship context. Do not invent “bluffing” merely to rescue a polished retort.

## Information-carrier rule

Important exposition should arrive through a legitimate carrier:

- physical evidence;
- changed environment;
- current problem;
- accusation/conflict;
- negotiation;
- misunderstanding;
- a practical question whose answer is required;
- a discovered record/message;
- a relationship-specific reminder.

Do not force all carriers into dialogue. Sometimes the best carrier is action, silence, a document, or a visible consequence.

Long dialogue is not inherently bad. A long explanation can PASS when it is required by an in-scene activity such as interrogation, negotiation, teaching, persuasion, testimony, command, confession, identity verification, or dispute resolution.

## Semantic-time cross-check

Before accepting a dialogue block, check relative-time words and the semantic structures they govern:

- lists;
- “also / and / another” continuations;
- pronouns;
- spending/accounting explanations;
- object handoffs;
- retrospective explanations.

A time scope can survive across several lines even when the time word is not repeated.

## Anti-action-beat-spam

Do not transform:

```text
A: line
B: line
A: line
```

into:

```text
A looks up: line
B frowns: line
A touches object: line
```

unless those actions matter. Generic gestures are not grounding.

## Fresh-audit discipline

A fresh reviewer must not use “I can imagine a reason” as evidence. PASS requires manuscript evidence.

When a pre-delivery or regression audit evaluates high-information dialogue, it must sample the **ordinary early/mid-scene exchanges**, not only climax speeches and obviously important scenes. Author-mouthpiece and ping-pong failures often hide in casual exposition and banter.

## Audit priority

Run this rule after macro scene causality exists but before final prose/de-AI acceptance. Fix factual/semantic failures before wording taste.
