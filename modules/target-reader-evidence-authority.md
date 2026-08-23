# Target Reader Evidence Authority V1

## Purpose

Prevent an AI evaluator from overriding concrete located feedback from an actual target reader merely because the AI can rationalize the same text as functional or coherent.

## Evidence classes

1. `LOCATED_HUMAN_TARGET_READER_FAILURE`
   - exact or bounded location;
   - reader effect (skim, boredom, disbelief, emotional non-response, artificial speech, weak suspense, etc.);
   - reason connected to the text rather than a bare numeric score.

2. `FRESH_AI_READER_EVIDENCE`
   - useful for independent detection, hypothesis generation and false-positive control;
   - not equivalent to human target-reader evidence.

3. `NUMERIC_PREFERENCE_ONLY`
   - a score without located reasons is not sufficient as a blocker by itself.

## Authority rule

`LOCATED_HUMAN_TARGET_READER_FAILURE > FRESH_AI_PASS` for final-freeze governance while the located failure remains unresolved.

An AI pass may show that a complaint is not caused by the mechanism first suspected. It may not erase the reader failure itself.

Example:

- human reader: climax feels flat;
- AI audit: options objectively compress;

Correct conclusion:

`OPTION_COMPRESSION_PRESENT` and `EXPERIENTIAL_VOLTAGE_FAILURE_STILL_OPEN` may both be true.

Incorrect conclusion:

`OPTION_COMPRESSION_PRESENT -> HUMAN_FLATNESS_REPORT_INVALID`.

## Closure requirements

An open located human failure closes only when one of the following is documented:

1. the manuscript changes in the affected scope and post-change target-reader evidence no longer reproduces the failure; or
2. coordinator adjudication demonstrates that the complaint is outside the declared target-reader / genre / product contract, with explicit rationale.

Fresh AI agreement is supporting evidence, not the closure event.

## Failure codes

`OPEN_LOCATED_TARGET_READER_FAILURE`
: a located human reader failure remains unresolved on the current manuscript SHA.

`AI_PASS_IMPROPERLY_OVERRIDES_HUMAN_READER_EVIDENCE`
: a final-quality or freeze decision treats fresh AI approval as sufficient to erase an unresolved located human failure.

## Final freeze rule

If the project has an open target-reader evidence ledger bound to the current manuscript SHA, final freeze is blocked until that ledger is settled.
