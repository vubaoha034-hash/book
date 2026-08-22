# Scene-to-Speech Microcraft V1.3

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

## Candidate-harvest pass — required before verdict

A pre-delivery or regression audit must first build a candidate inventory before judging any dialogue.

The inventory must include every located turn/block that meets any of these conditions:

1. one utterance contains 3 or more independently checkable factual claims;
2. one utterance bundles current-event facts such as target/event, listener role, reward/price, timing, rumor spread, location, quantity, arrivals, routes, rules or consequences;
3. one character tells another facts about the listener's own mission/role that the listener is likely to already know;
4. a neat rhetorical ladder appears, especially `Q -> retort -> Q -> punchline`;
5. a new topic is introduced mainly through dialogue;
6. a high-information line appears in ordinary early/mid-scene banter, not only at a climax.

The audit must record:

- `candidate_inventory_count`;
- `candidate_audited_count`;
- `candidate_omitted_count`;
- omission reason for every omitted candidate;
- `rhetorical_ladder_candidate_count`.

Sampling is not sufficient for these candidate classes. If the inventory is incomplete, the G6D verdict cannot be PASS.

## Rhetorical-ladder judgment parity — V1.3 hard gate

Harvesting a rhetorical ladder is not enough. Every item in `rhetorical_ladder_candidates` must receive a dedicated anti-template record.

For PRE_DELIVERY / REGRESSION:

`rhetorical_ladder_candidate_count == anti_template_record_count`

If counts differ, return `RHETORICAL_LADDER_AUDIT_INCOMPLETE` and G6D cannot PASS.

Do not claim `per_turn_template_failures = 0` when any harvested ladder lacks an explicit turn-by-turn judgment.

## Textual-evidence burden for speaker goals

Do not pass a line merely because the reviewer can imagine a plausible reason for speaking.

For every high-information or high-impact turn, the claimed in-scene goal must have located textual evidence in the current beat, nearby relationship state, or current task.

Invalid reviewer inventions include unsupported claims such as:

- “the speaker is probably trying to lighten the mood”;
- “the speaker may be showing confidence”;
- “the speaker could be bluffing”;
- “the speaker wants to explain what happened”.

If a PASS depends on a goal that exists only in the reviewer’s imagination, use HOLD or FAIL according to the remaining evidence.

## Exact-bundle no-reader counterfactual

Do not ask only whether this person would say something here.

Ask:

> If no reader existed, would this person say this approximate bundle of information, with this level of completeness, to this listener, now?

Distinguish:

- `WOULD_SAY_THIS_BUNDLE`;
- `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE`;
- `WOULD_NOT_SAY`;
- `UNCERTAIN`.

`WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE` is not a PASS for reader-orientation exposition.

## Atomic information-bundle test

For any line that transfers multiple background facts, split it into atomic claims.

For each claim record:

1. does the listener already know it?
2. does the listener need it for an immediate choice, task, risk, negotiation, accusation, warning, test, or relationship action?
3. what textual evidence shows the speaker wants this listener to know it now?
4. what changes because this specific claim is heard?

If a public-background/current-mission bundle contains several claims whose main beneficiary is the reader, and the listener already knows multiple claims or has no current use for them, flag `AUTHOR_INFORMATION_MOUTHPIECE_FAIL` even when one claim is scene-grounded.

A legitimate warning may contain several facts, but the warning purpose must be visible in the scene and the facts must serve that warning.

## Social-anecdote carveout — do not over-prune living speech

Listener need is not the only valid reason to speak. Real conversation includes gossip, amusement, shared memory and firsthand anecdote.

A social anecdote may PASS even when not every detail changes the listener's task, when all are true:

- it directly answers or naturally expands a question about a person/event;
- the speaker personally witnessed or plausibly owns the anecdote;
- the speaker-listener relationship supports casual sharing, gossip, teasing or recollection;
- the anecdote is not mainly restating the listener's own mission, role, public reward, rule or already-known setup;
- the scene is not under such immediate pressure that excess detail becomes implausible;
- the detail creates character/relationship texture rather than covertly carrying a reader orientation packet.

Do not fail a colorful firsthand anecdote merely because a shorter answer could satisfy the listener's practical need.

Record bundle type as one of:

- `TASK_OR_CONFLICT_INFORMATION`;
- `PUBLIC_BACKGROUND_ORIENTATION`;
- `SOCIAL_ANECDOTE_OR_RELATIONSHIP_STORY`;
- `MIXED`;
- `UNCERTAIN`.

## Public-background bundle high-risk pattern

Mandatory full audit is required when a single turn combines several of:

- what the central event is;
- when it will happen;
- what the listener is doing in it;
- the reward/price/stakes already known to the listener;
- how widely the news has spread;
- how many outsiders/armed people have arrived;
- route/location facts that orient a first-time reader.

If the listener already knows the event and their own role, and only one trailing fact is genuinely new/actionable, the new fact does not automatically justify repeating the entire bundle.

## Listener knowledge

Shared facts do not need to be restated unless the act of restating has a scene function such as leverage, accusation, warning, mockery, ritual, reframing, testing memory, or forcing a choice.

This rule does not ban social anecdotes whose value is relationship, amusement or recollection rather than factual briefing.

## Non-speech is an option

A character may remain silent, delay, answer partially, interrupt, change subject, lie, perform an action, or refuse because the relationship makes the question costly.

Do not make every exchange complete and cooperative.

## Dialogue-template warning: per-turn delta

When several turns form a neat rhetorical ladder, audit every turn and emit a dedicated anti-template record.

Especially inspect:

`question -> clever retort -> follow-up -> punchline`

For every turn record what changed in:

- knowledge;
- decision;
- task state;
- risk;
- relationship permission/pressure;
- concealment or misdirection;
- negotiation position.

Humor, rhythm, personality color, or “keeping the conversation going” do not count by themselves.

### Self-cancelling assertion test

If a retort creates or strongly implies proposition P, and later turns immediately reveal the speaker has no basis for P, then the temporary belief in P is **not** a meaningful state delta unless it serves a text-supported bluff, concealment, deterrence, face-saving, provocation, protection, relationship or task goal.

A false/unsupported assertion created only to manufacture the next question is scaffold, not grounding.

### Induced-follow-up dependency

Record whether the next turn exists mainly because the current turn manufactured uncertainty or a false premise.

If:

- a retort creates uncertainty;
- the next question is induced by that uncertainty;
- the punchline retracts/nullifies it;
- no independent scene goal is evidenced;

flag `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`.

### Counterfactual turn-deletion test

Mentally remove the suspicious retort and the follow-up it induces.

If the scene can move directly to the truthful/useful line with no loss of task information, necessary knowledge, relationship pressure, concealment, negotiation, or character-specific history—and the only loss is generic punchline cadence—the removed turns are template-risk.

Humor is not forbidden. The question is whether the humor is character/relationship-specific or merely portable scaffolding.

### Portability test

A joke/retort is higher risk when it could be transferred to unrelated characters and situations with almost no semantic change.

Portable generic wit is not character motive by itself.

Relationship-specific banter may PASS when it depends on shared history, a current object/task, prior grievance, status asymmetry, or later relationship action.

A later useful line does not retroactively justify empty scaffold turns.

## Bluff / deflection evidence

A seemingly false, evasive, or swaggering line can be natural when it serves a real goal such as deterrence, concealment, face-saving, provocation, or protecting someone.

The manuscript must support that goal through scene pressure, later behavior, or relationship context. Do not invent “bluffing” merely to rescue a polished retort.

## Information-carrier rule

Important exposition should arrive through a legitimate carrier: physical evidence, changed environment, current problem, accusation/conflict, negotiation, misunderstanding, a practical question whose answer is required, a discovered record/message, or a relationship-specific reminder.

Long dialogue is not inherently bad. A long explanation can PASS when required by interrogation, negotiation, teaching, persuasion, testimony, command, confession, identity verification, dispute resolution, or a natural social anecdote.

## Semantic-time cross-check

Before accepting a dialogue block, check relative-time words and the semantic structures they govern: lists, continuations, pronouns, spending/accounting explanations, object handoffs and retrospective explanations.

A time scope can survive across several lines even when the time word is not repeated.

## Anti-action-beat-spam

Generic gestures are not grounding. Do not repair an ungrounded exchange by inserting glances, frowns, sighs or object touches unless those actions materially change reading, information, goal, risk or relationship.

## Fresh-audit discipline

A fresh reviewer must not use “I can imagine a reason” as evidence. PASS requires manuscript evidence.

Candidate harvesting precedes judgment. Every harvested rhetorical ladder must then receive explicit turn-by-turn judgment before final verdict.

## Audit priority

Run this rule after macro scene causality exists but before final prose/de-AI acceptance. Fix factual/semantic failures before wording taste.
