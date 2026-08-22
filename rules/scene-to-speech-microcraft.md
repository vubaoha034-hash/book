# Scene-to-Speech Microcraft V1.4

## Principle

Do not write dialogue as a self-contained sequence of clever lines. Ground important speech in the scene that produces it.

Useful model:

`scene state -> trigger -> perception -> non-speech reaction -> speech -> aftereffect`

This is a reasoning model, not a prose template. Any step may be implicit when the scene remains intelligible.

## Layer separation after Phase344 calibration

Use two different questions:

```text
G6D: does this exchange make semantic / epistemic / character sense here?
G8: does the manuscript repeat the same portable dialogue machine too often across scenes/characters?
```

Do not force a G8 density/style concern into a false local G6D failure.

## Candidate-harvest pass

Before verdict, inventory every located turn/block that meets any of these conditions:

1. one turn contains 3+ independently checkable factual claims;
2. one turn bundles current event, timing, listener role, reward/stakes, rumor spread, arrival count, route, rule or consequence information;
3. a speaker tells the listener facts about the listener's own mission/role;
4. a rhetorical ladder appears, especially `Q -> retort -> follow-up -> punchline`;
5. a new topic is introduced mainly through dialogue;
6. a high-information line appears in ordinary early/mid-scene conversation;
7. a line may carry meta-information about who else knows a fact, what rumor says, or how exposure changes risk.

Record candidate counts and omissions. In PRE_DELIVERY / REGRESSION mode, incomplete harvest means G6D cannot PASS.

## Epistemic-scope test — required before mouthpiece verdict

Read `modules/dialogue-epistemic-scope.md`.

Do not collapse these into one proposition:

```text
OBJECT_FACT
LISTENER_KNOWS_OBJECT_FACT
PUBLIC_KNOWLEDGE_OF_OBJECT_FACT
REPORTED_RUMOR_CONTENT
EVIDENCE_OF_EXPOSURE_OR_SPREAD
ACTIONABLE_RISK_FROM_PUBLIC_KNOWLEDGE
```

Knowing X is not the same as knowing that outsiders know X.

A warning may legitimately repeat the wording of a known object fact because that fact is embedded in a new meta-proposition such as “people outside are saying X about you.”

Before `AUTHOR_INFORMATION_MOUTHPIECE_FAIL`, record:

- what object-level facts the listener already knows;
- what public/reported knowledge is new;
- what evidence shows spread/exposure;
- what risk/action changes because outsiders know it;
- whether repeated known facts are necessary to identify the rumor/meta-claim;
- what, if anything, remains reader-only residue.

Unsupported “everyone knows” claims are HOLD unless contradicted. Pure shared-background restatement with no new scene or epistemic payload remains FAIL.

## Exact-bundle no-reader counterfactual

Ask:

> If no reader existed, would this person say approximately this bundle to this listener now?

Record:

- `WOULD_SAY_THIS_BUNDLE`;
- `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE`;
- `WOULD_NOT_SAY`;
- `UNCERTAIN`.

For public-background exposition, `WOULD_SAY_SOMETHING_BUT_NOT_THIS_BUNDLE` is failure evidence only after epistemic-scope analysis shows the extra material has no real meta-knowledge / warning / relationship / task payload.

## Atomic information-bundle test

For a multi-fact bundle, record per claim:

1. listener object-level knowledge;
2. listener knowledge of public/reported knowledge;
3. immediate listener need or relationship purpose;
4. speaker's text-supported transmission goal;
5. aftereffect;
6. whether the claim is embedded content needed to identify a rumor/meta-proposition.

One actionable fact does not rescue unrelated reader-only setup. Conversely, known object facts embedded in a genuinely new exposure report are not automatically reader-only.

## Social-anecdote carveout

Listener practical need is not the only valid reason to speak. Gossip, amusement, shared memory and first-hand anecdote may PASS when:

- they directly answer or naturally expand a person/event question;
- the speaker plausibly owns the story;
- the relationship supports sharing;
- the scene has room for it;
- the anecdote does not mainly restate current mission/setup;
- the detail creates voice, relationship texture, memory pressure or shared reaction.

Do not fail living speech merely because a shorter task answer exists.

## Rhetorical-ladder audit parity

Every harvested rhetorical ladder still requires an explicit ATS record. For PRE_DELIVERY / REGRESSION:

`rhetorical_ladder_candidate_count == anti_template_record_count`

If not, use `RHETORICAL_LADDER_AUDIT_INCOMPLETE`.

## Calibrated local anti-template judgment

Audit every turn for:

- knowledge change;
- choice/action change;
- risk;
- relationship permission/pressure;
- concealment/misdirection;
- negotiation position;
- text-supported bluff/deflection/status goal.

Use self-cancelling assertion, induced-follow-up, turn-deletion and portability as diagnostics.

However:

**A single locally plausible/removable joke is not automatically a hard G6D failure merely because it can be shortened.**

Local `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE` requires independent evidence that the exchange is actually ungrounded or materially misleading in this scene—for example no supported goal/relationship pressure, critical information is delayed behind empty scaffolding, or a false premise is manufactured solely to drive the next turn.

If the exchange is locally plausible but looks portable/generic, mark it as a `G8_PATTERN_FAMILY_CANDIDATE` and defer manuscript-level repetition judgment to `modules/dialogue-pattern-family-density.md`.

## Bluff / deflection evidence

A false, evasive or swaggering line may be natural when it serves deterrence, concealment, face-saving, provocation, protection or a relationship goal supported by the scene or later behavior.

Do not invent bluffing to rescue a polished line.

## Non-speech is an option

Characters may remain silent, delay, answer partially, interrupt, change subject, lie, perform an action or refuse. Do not make every exchange complete and cooperative.

## Information carriers

Important information may arrive through physical evidence, changed environment, current problem, accusation/conflict, negotiation, misunderstanding, practical question, discovered record/message, relationship-specific reminder, or public/exposure evidence.

Long dialogue is not inherently bad when the scene requires interrogation, negotiation, teaching, testimony, command, confession, identity verification, dispute resolution or natural social storytelling.

## Semantic-time cross-check

Relative-time words may govern lists, continuations, pronouns, spending explanations, object handoffs and retrospective explanations across several lines.

A time/state scope survives until a real scope break. Explicit incompatible later facts remain hard `TEMPORAL_SEMANTIC_CHAIN_FAIL`.

## Anti-action-beat-spam

Generic gestures are not grounding. Do not repair a weak exchange by inserting glances, frowns, sighs or object touches unless those actions materially change information, goal, risk, relationship or reading.

## Fresh-audit discipline

A fresh reviewer must not use “I can imagine a reason” as evidence. PASS/HOLD/FAIL must cite located manuscript evidence.

Candidate harvesting precedes judgment. Epistemic level precedes mouthpiece verdict. Local G6D verdict precedes any G8 density interpretation.

## Audit priority

Run this rule after macro scene causality exists but before final prose/de-AI acceptance. Fix deterministic semantic failures before style density or wording taste.
