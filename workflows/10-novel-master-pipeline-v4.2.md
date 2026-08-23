# Novel Master Pipeline V4.2 — Target-Profile + Holdout Validation

## Purpose

V4.2 fixes a failure mode exposed by Phase357: a fresh AI can be internally consistent, follow V4.1 correctly, and still substitute its own taste for the declared target reader while rationalizing known reader failures.

V4.2 therefore separates four questions:

1. Is the manuscript logically/causally valid?
2. Is reader-experience craft structurally present?
3. Does a fresh evaluator calibrated to the declared target-reader profile experience the intended effect?
4. Are previously located human target-reader failures actually closed on the new candidate?

No one layer substitutes for another.

## Phase A — Preflight / continuity

Read:

- `state/project_state.json`
- `state/continuity/LATEST_CHECKPOINT.json`
- `rules/pass-isolation.md`

Never roll back to a historical freeze or historical AI PASS.

## Phase B — Target-reader profile calibration

Before a fresh target-fit read, load only the non-answer-key reader profile appropriate to the project.

For YMGQ:

- `state/reader_profiles/YMGQ_TARGET_READER_PROFILE_V1.json`

Do not load:

- exact failure locations;
- quoted failed passages;
- prior evaluator reports;
- regression expected answers;
- repair ledgers.

The reader profile defines taste and experience requirements, not where defects are.

## Phase C — Blind profile-calibrated immersion

Bind manuscript SHA first.

Then read the manuscript completely before quality-rule files.

Freeze evidence for:

- genuine skim/stop points;
- manuscript-level surface repetition after mentally abstracting names/props;
- live-speech turns that feel composed rather than spoken;
- mysteries where danger is interesting but the answer itself is not;
- subjective climax voltage;
- actual willingness to continue/recommend under the declared reader profile.

Freeze the trace before formal rule loading.

## Phase D — Formal V4.2 audit

Load V4.2 plus inherited V4.1/V4/V3.

Mandatory hardening tests:

### D1 — Re-entry textual anchor

A new scene condition is not a valid re-entry delta unless the text makes it available to the returning character before return.

Never infer motive from post-return function.

### D2 — Dramatization functional mask

For separated high-stakes scenes:

1. mask names, props, factions and lore labels;
2. record the remaining surface sequence;
3. test whether unique carriers actively change behavior/timing/subtext/consequence;
4. test whether available dramatic pressure was actually used.

### D3 — Natural speech counterfactual turn

For each high-information live utterance:

1. identify earliest sufficient warning/payload;
2. classify later information roles;
3. place likely listener reaction boundaries;
4. test whether later clauses would naturally be redirected or made redundant;
5. require located support for uninterrupted multi-role delivery.

### D4 — Suspense answer-value ablation

For each material mystery, separately test:

- danger/action pull;
- desire for the answer itself.

Counterfactual: if the answer were revealed now but danger remained, would material reader pull disappear?

### D5 — Climax structural vs experiential curve

Retain V4.1 G7C/G7V separation.

## Phase E — Hidden holdout comparison

Only after the fresh evaluator returns may the coordinator load:

- located human reader failures;
- regression answer keys;
- prior failed evaluator reports.

Build a recall matrix:

- direct hit;
- same-class partial hit but wrong location/mechanism;
- miss;
- false positive.

Architecture validation fails if a material hidden holdout failure remains undetected or is explicitly rationalized as PASS.

## Phase F — Rewrite authorization

Do not rewrite merely because an evaluator says FAIL.

Rewrite becomes eligible only when:

- architecture has demonstrated adequate hidden-holdout recall;
- the coordinator can translate each open target-reader failure into a bounded repair objective;
- protected strengths are listed;
- no answer-key leakage is needed during authoring.

## Phase G — Post-rewrite validation

After a new candidate is created:

1. re-run inherited logic/continuity/microcraft checks;
2. fresh profile-calibrated immersion on the new SHA;
3. formal V4.2 audit;
4. human target-reader closure of previously located failures.

Final freeze is forbidden while any located human target-reader failure remains open.

## Non-negotiable distinctions

`fresh context != calibrated taste`

`unique props != unique scene surface`

`all clauses useful != natural live utterance`

`danger interest != mystery answer interest`

`structural climax != experienced climax`

`fresh AI recommendation != human target-reader acceptance`
