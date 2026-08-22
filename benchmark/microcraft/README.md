# Microcraft Dialogue Regression — Calibrated

This is a permanent privacy-safe regression layer for V3-G6D and G8 dialogue quality.

It is separate from the 100-point mother-candidate benchmark. It does not produce an overall literary score and does not prove general writing quality.

## Historical suites

`dialogue-regression.v1.json` through `dialogue-regression.v4.json` remain immutable historical development evidence.

They preserve the original three seed abstractions and the rules used by Fresh Attempts 1–5. Their historical outcomes are not rewritten.

After repeated correctly-bound fresh disagreement and three-book contrastive evidence, Phase344 determined that the old future `3/3` promotion contract was overfitting two context-dependent labels.

Therefore:

- `MC-R001` remains a hard deterministic semantic regression;
- `MC-R002` is no longer a mandatory single-instance mouthpiece FAIL; future audits must model epistemic scope;
- `MC-R003` is no longer a mandatory single-instance template FAIL; portable recurrence is evaluated at manuscript-level pattern-family density unless the local exchange independently fails grounding.

## Current calibration and active regression

```text
benchmark/microcraft/label-calibration.v1.json
benchmark/microcraft/epistemic-pattern-regression.v1.json
```

The active suite checks:

- inherited temporal semantic contradiction remains hard FAIL;
- object fact vs public/reported knowledge distinction;
- unsupported public-knowledge claims HOLD rather than receiving invented evidence;
- pure shared-background mouthpiece still FAILs;
- single context-supported banter is not hard-failed solely for removability;
- repeated portable cadence across separated scenes/characters is routed to G8 `DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK`;
- varied relationship-specific humor is protected;
- no universal numeric density threshold is frozen from the current purposive sample.

No user manuscript text or copyrighted source-book passages are committed in these suites.

## Validation

```bash
python scripts/validate_microcraft_regression.py
```

The validator checks historical preservation, calibration state, active case structure, privacy flags and calibrated layer semantics. It does not semantically classify arbitrary manuscript prose.

Manuscript G6D evidence uses:

```text
modules/dialogue-epistemic-scope.md
templates/microcraft-dialogue-audit-template.md
```

G8 dialogue-density evidence uses:

```text
modules/dialogue-pattern-family-density.md
templates/dialogue-pattern-family-audit-template.md
```

## Acceptance discipline

- historical fresh results remain historical;
- current architecture must be validated against the calibrated contract, not forced to reproduce retired labels;
- schema PASS is not literary-quality proof;
- a future fresh manuscript audit must hide calibration case answers and prior manuscript findings;
- human blind validation and broader manuscripts are still required before universal production claims.
