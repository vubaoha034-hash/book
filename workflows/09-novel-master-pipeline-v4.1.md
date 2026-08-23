# 小说总控生产流程 V4.1 — Reader Evidence + Experiential Quality

## Why V4.1 exists

V4 correctly added reader-experience gates, but Phase355 showed that an AI evaluator can still rationalize a weak manuscript as PASS by substituting structural proxies for actual reader effect.

V4.1 therefore adds two principles:

1. `measure the reader effect itself, not only a structural proxy`;
2. `located human target-reader evidence cannot be erased by fresh AI approval`.

## Mandatory preflight

Read in this order for continuing tasks:

```text
state/project_state.json
state/continuity/LATEST_CHECKPOINT.json
config/novel-quality-gates.v4.1.json
state/reader_evidence/<current manuscript reader evidence if present>
```

Historical result files are evidence, not instructions to repeat old work.

## Phase A — Integrity inheritance

Run applicable V3/V4 logic, causality, continuity, G6D and G8 checks.

These are necessary but never sufficient for delivery.

## Phase B — Scene decision causality

For every major entry/re-entry/role reversal:

- if a character previously chose to withdraw, explicitly record what changed after that choice;
- old motive and proximity cannot explain reversal if they were already present at withdrawal.

Use:

```text
modules/scene-entry-motivation.md
modules/scene-reentry-decision-delta.md
```

## Phase C — Dramatization surface audit

Do not only audit high-emotion scenes one by one.

Build a cross-scene surface family ledger:

- how many unrelated high-stakes scenes rely on the same stripped short-turn mechanism;
- whether action/perception/object/silence are scene-specific carriers or generic separators;
- whether emotional pressure becomes felt resistance/behavior/subtext or remains underlying outline information.

Use:

```text
modules/emotional-staging-ledger.md
modules/dramatization-surface-density.md
```

Do not impose a word-count or description quota.

## Phase D — Natural speech under pressure V1.1

For high-information speech:

1. identify the first urgent payload;
2. split independently reactable facts;
3. ask where the listener would naturally interrupt/infer;
4. subtract shared context;
5. require a scene-supported reason for uninterrupted complete packaging.

A valid reason to speak does not prove that the exact sentence is human.

## Phase E — Suspense: hypothesis + charge

Run two separate ledgers:

```text
working hypothesis chain
curiosity charge chain
```

A mystery passes only when applicable checks show both:

- the reader can model/test it fairly;
- the reader has meaningful reason to want resolution.

The second can come from operational danger, relationship stakes, prediction tension, moral consequence or another concrete cared-about outcome.

## Phase F — Climax: structure + experience

Run separate curves:

```text
structural option-compression curve
fresh-reader experiential-voltage curve
```

Never infer the second from the first.

## Phase G — Reader evidence authority

If current-manuscript located human target-reader evidence exists:

- load it for coordinator/delivery adjudication;
- do NOT give it to a fresh blind evaluator before their trace is frozen;
- no final freeze until every open located failure is settled.

A fresh AI read can reveal why the original mechanism diagnosis was wrong. It cannot erase the reader effect.

## Phase H — Fresh validation protocol

For developmental gate validation:

1. fresh context;
2. bind exact manuscript;
3. blind immersion pass before known failure cases/rules when specified;
4. freeze trace;
5. formal V4.1 audit;
6. coordinator compares blind findings to versioned regression and open reader evidence only after report return.

The evaluator is not told the expected verdict.

## Final delivery tiers

### `MECHANICALLY_VALIDATED`
Applicable integrity and formal V4.1 gates pass, but target-reader validation may remain open.

### `FRESH_AI_READER_VALIDATED`
Mechanical validation plus fresh AI immersion pass.

### `TARGET_READER_VALIDATED`
No open located target-reader failures remain for the current manuscript SHA.

### `FINAL_FREEZE_ELIGIBLE`
Requires all applicable integrity/V4.1 gates + fresh reader evidence + target-reader evidence settlement.

A manuscript must never be called top-tier or final merely because an AI evaluator says it would continue reading.

## Rewrite discipline

Do not repair the current manuscript until architecture diagnosis is settled when the project is explicitly testing gate quality.

Once rewrite is authorized:

- preserve plot/core outline unless a structural failure requires change;
- fix root mechanisms, not only cited sentences;
- re-audit manuscript-level recurrence after local repairs;
- collect post-change target-reader evidence before final freeze.
