# Target Reader Profile Calibration V1

## Purpose

A fresh AI reader is not automatically the actual target reader. Before using AI immersion evidence to judge commercial/readability quality, define the target-reader experience contract without exposing known failure locations or answer keys.

## Required profile fields

- target reading goal / market experience;
- preferred dramatization density;
- accepted minimalism conditions;
- speech naturalness expectations;
- suspense curiosity expectations;
- climax voltage expectations;
- reader-propulsion expectations;
- false-positive controls;
- prohibited style/plot imitation.

## Governance

The target-reader profile may be visible before a fresh blind read because it defines the audience, not the answer.

The following must remain hidden from a fresh evaluator:

- exact failed locations;
- exact quotations from known failed passages;
- prior evaluator verdicts;
- regression answer keys;
- repair history.

## Failure codes

`UNSPECIFIED_TARGET_READER_SIMULATION`
: an evaluator claims target-reader immersion while no target-reader experience contract is defined.

`FRESH_AI_DEFAULT_TASTE_SUBSTITUTED_FOR_TARGET_READER`
: a fresh model's own willingness to continue/recommend is treated as proof of target-reader fit despite material mismatch with the declared reader contract.

`KNOWN_FAILURE_LEDGER_LEAKED_INTO_TARGET_PROFILE`
: a reader profile contains exact locations or answer-key details that would contaminate fresh evaluation.

## Core distinction

`FRESH_AI_READER != TARGET_READER`.

Fresh context controls history leakage. It does not calibrate taste.

## Final-freeze rule

AI immersion evidence may support diagnosis and regression, but it cannot close unresolved located human target-reader evidence on the same manuscript SHA.
