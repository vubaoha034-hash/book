# Microcraft Regression Test Plan V1

## Question

Can the V3-G6D procedure detect local semantic-time contradictions and scene-ungrounded dialogue that previous V3/fresh-reader reviews missed?

## Development evidence

- Two canonical source books currently provide raw Scene-to-Speech evidence in a private evidence document: 30 abstract samples from BOOK-02 and 30 from BOOK-03.
- BOOK-01 canonical repaired source is not currently readable in the connected private plane; full three-book raw microcraft validation is HOLD.
- Three privacy-safe real-manuscript failure abstractions are locked as mandatory negatives.

## Protocol isolation

### A. Contract validation

Run:

```bash
python scripts/validate_microcraft_regression.py
```

This only validates suite structure and expected labels.

### B. Known-failure semantic audit

Input: the unchanged historical manuscript candidate that produced the three failures.

The audit pass receives:

- manuscript only;
- `V3-G6D` rules/modules/template;
- NO description of where the three known failures occur;
- NO corrected wording;
- NO previous user diagnosis.

Pass condition:

- rediscovers `TEMPORAL_SEMANTIC_CHAIN_FAIL` at the known money/time chain;
- rediscovers `AUTHOR_INFORMATION_MOUTHPIECE_FAIL` at the known reader-briefing dialogue;
- rediscovers `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE` at the known tidy exchange;
- does not propose generic action-beat insertion as the fix.

Failure to rediscover any mandatory case = architecture regression FAIL. Do not repair the manuscript first and then claim success.

### C. Positive counterexample audit

The procedure must not reject every dialogue without a preceding action. Positive cases pass when speech is grounded by evidence, task, silence, relationship pressure, current goal, or another legitimate scene carrier.

## Evidence classification

- Schema/script PASS = engineering contract evidence only.
- Known-failure rediscovery = developmental semantic regression evidence.
- Fresh-context AI review = independent context, not human validation.
- Full three-book microcraft claim requires BOOK-01 raw-source sampling with the same protocol.

## No score laundering

This suite has no 100-point score. It cannot be averaged into the mother-candidate benchmark to compensate for hidden-set or literary failures.
