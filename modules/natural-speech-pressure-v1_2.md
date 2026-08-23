# Natural Speech Under Pressure V1.2

## Purpose

V1.1 introduced priority, turn segmentation and shared-context subtraction. V1.2 prevents an evaluator from excusing a polished live-information packet merely because every clause is relevant.

## 1. Earliest-sufficient-warning test

Identify the earliest clause that already gives the listener enough information to react or ask a question.

Then inspect every later clause in the same uninterrupted turn.

For each later clause ask:

- does the speaker need to say this before seeing the listener's reaction?
- would the listener's likely reaction change what the speaker says next?
- is the clause evidence the listener could directly perceive or ask for?
- is the clause mainly orienting the reader?

If the answer supports natural interruption but the speech continues as a polished packet, record risk.

## 2. Information-role stack test

Classify each clause as one of:

- urgent warning;
- shared background;
- meta-information about spread/reputation;
- incentive/reward amount;
- physical evidence / arrival evidence;
- conclusion / interpretation;
- instruction.

A live utterance that stacks several different information roles in a rhetorically ordered sequence requires stronger scene support than a single-role warning.

`all facts are useful` is not sufficient support.

## 3. Listener-turn counterfactual

At every independently reactable boundary, imagine the listener giving the most plausible immediate reaction.

If that reaction would naturally interrupt, redirect, challenge or make later clauses redundant, an uninterrupted original turn needs a located reason.

Do not rewrite the passage during audit; only record whether the original turn organization is plausible.

## 4. Visible-evidence subtraction

If part of the packet reports something visible/audible in the current environment, ask why speech must carry it instead of the scene.

This is not a demand for action beats. It is a carrier-allocation test.

## Failure codes

Inherited V1/V1.1 codes remain active.

`EARLIEST_SUFFICIENT_WARNING_IGNORED_FOR_READER_PACKET`
: the speaker already delivers the urgent fact, but continues through multiple reader-orienting information roles before allowing a plausible listener turn.

`MULTI_ROLE_INFORMATION_STACK_FEELS_COMPOSED`
: one live turn neatly packages several distinct information roles without briefing/testimony/confession/rehearsed-persuasion support.

`PLAUSIBLE_LISTENER_REACTION_SUPPRESSED`
: a likely listener reaction would naturally occur before the end of the packet and would affect subsequent speech, but the original passage suppresses that turn for exposition convenience.

## False-positive controls

- Formal briefing/testimony/confession/public persuasion may stack roles when uninterrupted delivery is scene-supported.
- Urgent emergency warnings may contain multiple short facts if delay itself is dangerous.
- Some people do speak in complete bursts; do not fail merely for grammatical completeness.
- Do not repair by adding filler, fake interruptions or slang. The issue is information priority and turn structure.
