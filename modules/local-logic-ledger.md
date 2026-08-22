# Local Logic Ledger V1

## Purpose

Catch local contradictions that survive ordinary continuity review because the conflicting fact is carried implicitly through a semantic relation rather than repeated literally.

Primary targets:

- relative time and date scope;
- money and spending scope;
- object ownership/transfer;
- injury/body state;
- location and movement;
- knowledge acquisition;
- pronoun/list/reference scope;
- promises and conditions whose scope continues into later clauses.

## Core distinction

A normal timeline records isolated facts:

```text
event A = last night
event B = two days ago
```

A semantic-time ledger additionally records whether B is asserted as a member, consequence, explanation, or continuation of A.

## Required chain record

```text
chain_id:
anchor_location:
anchor_fact:
anchor_time_or_state:
semantic_relation:
inherited_scope:
scope_break_present: true | false | ambiguous
linked_clause_or_item:
later_explicit_fact:
verdict: CONSISTENT | CONTRADICTION | AMBIGUOUS
confidence: HIGH | MEDIUM | LOW
repair_target:
```

## Deterministic contradiction rule

Return `TEMPORAL_SEMANTIC_CHAIN_FAIL` when all are true:

1. a time/state anchor is explicit;
2. grammar or discourse makes a later item inherit that scope;
3. no explicit scope break intervenes;
4. a later explicit fact places that same item outside the inherited scope;
5. both cannot be true under the intended reading.

Do not soften a deterministic contradiction into “maybe the reader can infer another timeline”. Repair the wording or event.

## Ambiguity rule

Use HOLD, not FAIL, if multiple plausible scope readings remain and none is textually dominant. The audit must state what wording would disambiguate it.

## Semantic relations to track

- `CAUSE_OR_CONSEQUENCE`
- `MEMBER_OF_LIST`
- `SPENDING_OF_MONEY`
- `OWNERSHIP_OR_TRANSFER`
- `KNOWLEDGE_FROM_SOURCE`
- `INJURY_STATE_CONTINUATION`
- `LOCATION_CONTINUATION`
- `PROMISE_OR_CONDITION_SCOPE`
- `PRONOUN_OR_REFERENT`
- `EXPLANATION_OF_PRIOR_CLAUSE`

## Money example abstraction

If a character establishes that money was obtained last night, is immediately asked where that money went, and answers with a list, each list member normally inherits the spending event's temporal scope unless the text explicitly changes topic/time.

A later claim that one listed expenditure occurred before the money existed is a hard contradiction.

## Dialogue interaction

Run this ledger before stylistic dialogue polishing. Natural-sounding banter does not excuse a broken semantic chain.

## Repair discipline

Repair the smallest false link:

- correct the time expression;
- break the inherited scope explicitly;
- separate unrelated information from the list;
- change the object/money relationship;
- remove a misleading connective.

Do not rewrite the surrounding scene merely to hide the contradiction.
