# Holdout Contamination & Repair Separation V1

## Purpose

Prevent repeated architecture tuning on one labelled manuscript from being mistaken for generalization.

## Core distinctions

```text
CURRENT_MANUSCRIPT_REPAIR_AUTHORIZATION != ARCHITECTURE_PROMOTION
LABELLED_CALIBRATION_CASE != FRESH_GENERALIZATION_HOLDOUT
HUMAN_LOCATED_FAILURE != REQUIREMENT_THAT_AI_REDISCOVER_100_PERCENT_BEFORE_REPAIR
```

## Holdout contamination rule

A manuscript stops being eligible as an independent architecture-promotion holdout once its human reader feedback has materially shaped any of:

- gate definitions;
- target-reader profile;
- regression cases;
- detector hardening;
- evaluator prompt design;
- coordinator acceptance criteria.

The manuscript may still be used for:

- diagnosis;
- repair;
- regression development;
- human evidence closure;
- post-repair validation of the manuscript itself.

It may NOT by itself prove architecture generalization.

## Current YMGQ status

`一命过桥` SHA-256 `3765e4396afbc15c5e3cf2d0aa34ea581a22c4dad648dc2bc59dd020fd31cebf` is now a labelled calibration/repair case.

V4/V4.1/V4.2 were materially hardened from located target-reader feedback on this manuscript. Therefore further same-SHA fresh runs cannot promote the architecture even if they eventually reproduce every known failure.

## Repair authorization rule

Once:

1. the human target-reader failure is located and bound to the current manuscript SHA;
2. the coordinator has completed the required fresh/hidden-holdout adjudication cycle;
3. the failure remains inside the explicit target-reader contract;

repair may be authorized directly from the human evidence.

The repair does NOT require a fresh AI evaluator to independently rediscover every human aesthetic failure first.

This prevents an infinite loop in which the project trains the evaluator on the same manuscript instead of improving the manuscript.

## Architecture promotion rule

A developmental architecture may only move toward promotion using a genuinely new holdout that did not supply the calibration evidence.

Preferred evidence:

- another real manuscript from the project not used to design the current detectors;
- or a pre-registered new sample/section whose target-reader evidence is collected only after predictions are frozen.

Static regression cases remain necessary but are not sufficient.

## Human evidence authority

A located human target-reader failure remains open until:

- the manuscript changes in a way intended to address it; and
- post-change validation determines whether the reader effect is actually resolved.

A fresh AI PASS cannot erase it.

## Final-freeze rule

Architecture maturity and manuscript final-freeze eligibility remain separate dimensions.

A manuscript cannot be final-frozen while located human failures remain open.

A manuscript may undergo bounded repair while the architecture remains developmental.
