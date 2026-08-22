# Dialogue Epistemic Scope Module V1

## Purpose

Prevent dialogue audits from flattening several different propositions into one generic idea of “the listener already knows this.”

The module is part of V3-G6D. It does not decide style density or general AI smell.

## Core distinction

These are different propositions:

```text
OBJECT_FACT
LISTENER_KNOWS_OBJECT_FACT
PUBLIC_KNOWLEDGE_OF_OBJECT_FACT
REPORTED_RUMOR_CONTENT
EVIDENCE_OF_EXPOSURE_OR_SPREAD
ACTIONABLE_RISK_FROM_PUBLIC_KNOWLEDGE
```

Example abstraction:

```text
X = the listener is escorting a prisoner today

listener knows X
!=
listener knows that outsiders know X
!=
listener knows what version of X the rumor contains
!=
listener knows outsiders have already gathered because of X
```

A dialogue line may repeat the words of X because X is embedded inside a new meta-proposition such as “people outside are saying X about you.” That repetition is not automatically reader-only exposition.

## Required epistemic record

For every public-background / current-mission information bundle record:

```text
object_fact:
listener_object_fact_knowledge: KNOWN | UNKNOWN | UNCERTAIN
speaker_claim_about_public_knowledge:
listener_public_knowledge_before: KNOWN | UNKNOWN | UNCERTAIN | NOT_APPLICABLE
reported_rumor_content:
rumor_source_or_evidence:
exposure_or_spread_evidence:
actionable_risk_from_public_knowledge:
epistemic_payload_delta:
embedded_repetition_required_to_identify_meta_claim: true | false | uncertain
reader_only_residue:
verdict: PASS | FAIL | HOLD
failure_code:
```

## Decision rules

### 1. Do not flatten object fact and meta-knowledge

If the listener knows X but does not know that other people know X, then “others know X” is new information.

Do not count the repeated words describing X as reader-only merely because the listener already knows X.

### 2. Public knowledge needs evidence

A claim that “everyone knows,” “word has spread,” or “people are coming because of it” must have a carrier such as:

- observed arrivals;
- intercepted messages;
- repeated rumor sources;
- a changed crowd or route;
- named reports;
- visible preparation or response by outsiders.

If the meta-knowledge claim is plausible but unsupported, use HOLD rather than inventing evidence.

### 3. Embedded repetition may be necessary

A rumor warning may need to state what the rumor actually says. Repeating a known object fact can be necessary to identify the content that has become public.

This is different from two characters calmly reciting shared setup to each other.

### 4. Pure shared-background mouthpiece still fails

Use `AUTHOR_INFORMATION_MOUTHPIECE_FAIL` when all are true:

- the listener already knows the object-level facts;
- no new public-knowledge, rumor-content, exposure, accusation, reframing, negotiation, teaching, misunderstanding, relationship or task payload is transmitted;
- the repeated facts are not needed to identify a new meta-proposition;
- the main beneficiary is the reader.

### 5. Over-completeness is not always a hard G6D failure

If a line has a legitimate epistemic payload but is wordier or more complete than necessary, record the redundant residue.

Route pure redundancy/naturalness concerns to G8/de-AI unless the extra claims create a separate hard information-carrier problem.

## Separation from social anecdote

First-hand gossip, teasing and shared memory remain governed by the social-anecdote carveout. They are not converted into epistemic-scope failures merely because the listener does not need each detail for a task.

## Separation from pattern density

A locally plausible line can still contribute to a repeated manuscript-level cadence family. That is G8 evidence, not a reason to falsify the local G6D verdict.
