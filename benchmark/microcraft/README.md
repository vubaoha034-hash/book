# Microcraft Dialogue Regression V1

This is a permanent regression sub-suite for `V3-G6D`.

It is separate from the 100-point mother-candidate benchmark. It does not produce an overall literary score and does not prove general writing quality.

## What it locks

The suite permanently includes three real-failure abstractions discovered after a manuscript had been falsely frozen as final:

- `MC-R001 TEMPORAL_SEMANTIC_CHAIN_FAIL`
- `MC-R002 AUTHOR_INFORMATION_MOUTHPIECE_FAIL`
- `MC-R003 DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`

The cases are privacy-safe abstractions. No user manuscript text or copyrighted source-book passages are committed here.

## Additional counterexamples

The suite also contains positive and boundary cases for:

- environment/evidence-triggered speech;
- visible-reaction follow-up;
- silence as relationship pressure;
- action before rule explanation;
- meaningful nonresponse;
- legitimate restatement of shared facts as leverage;
- action-beat spam as a false repair;
- ambiguous semantic-time scope;
- banter that actually changes relationship permission.

## Validation

```bash
python scripts/validate_microcraft_regression.py
```

This validates the benchmark contract only. It does not semantically classify arbitrary manuscript prose.

A manuscript audit must still cite located evidence using:

```text
templates/microcraft-dialogue-audit-template.md
```

## Acceptance rule

Architecture regression is not accepted unless the unchanged known-failure manuscript is re-audited and all three mandatory failures are independently rediscovered by the new G6D procedure before any fixes are shown to that audit pass.
