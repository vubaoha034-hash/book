# Novel DNA Bounded Production Governance V1

Status: OPTIONAL_BOUNDED_PRODUCTION
Default: OFF
Source benchmark: `state/review_receipts/GLOBAL_NOVEL_DNA_V1_INTEGRATION_REGRESSION_BENCHMARK_V1.json`
Router: `rules/novel-dna-routing.md`
Call record: `templates/dna-call-record-template.md`
Frozen Global DNA: `GN-VDNA-01`

This contract promotes the already-integrated Novel DNA Router only to optional bounded production use. It does not change any frozen Novel DNA semantics, does not enable the Router by default, and does not claim universal production improvement.

## 1. Production status

Allowed status:

`OPTIONAL_BOUNDED_PRODUCTION`

Meaning:

- the normal V3 workflow remains the default;
- the Router may be invoked only after ordinary V3 diagnosis identifies a concrete structural problem;
- every `APPLIED` production call is an auditable controlled intervention;
- the Router remains removable from a manuscript when its expected structural benefit is not observed.

Not authorized:

- default-on routing;
- automatic DNA application to every story;
- premise generation from DNA;
- full DNA registry injection into prose context;
- any new Global DNA promotion;
- any semantic broadening of `GN-VDNA-01`;
- claims that Phase 310 proves all production writing improves.

## 2. Entry gate for real manuscripts

A real manuscript may enter the Router only when all of the following are true:

1. a concrete `problem_evidence` location or scope exists;
2. the upstream V3 failure has already been classified;
3. a simpler causal / continuity / callback / setup-payoff / scene-function / emotion-payoff / character-choice repair is insufficient;
4. a frozen DNA invocation gate is actually satisfied;
5. same-lineage duplication has been removed;
6. shared and DNA-specific application limits both pass, with the stricter limit winning;
7. expected change, protected elements, complexity cost, formula risk and exit criteria are recorded before rewriting.

Failure of any gate => `REJECTED` or `HOLD`, never forced `APPLIED`.

## 3. Mandatory production call record

Every real-manuscript `APPLIED` call must use `templates/dna-call-record-template.md` and must additionally bind to an opaque production-use ID.

Required production metadata:

```text
production_use_id:
private_manuscript_ref:
pre_change_snapshot_ref:
post_change_snapshot_ref:
real_manuscript: true
user_or_reader_outcome: POSITIVE | NEUTRAL | NEGATIVE | NOT_AVAILABLE
reader_evidence_type: INDEPENDENT | SIMULATED_LENS | USER_FEEDBACK | NONE
privacy_safe_summary:
```

Do not put manuscript text, protected source-book text, personal style samples, or private plot details into the public production ledger. Use opaque/private references plus a short privacy-safe outcome summary.

## 4. Post-use validation is mandatory

An `APPLIED` production call is incomplete until post-use validation records:

- observed structural change;
- whether the expected change was met;
- continuity regression;
- formula risk observed;
- complexity introduced;
- whether protected story elements survived;
- exit criteria result;
- user/reader outcome when available;
- final disposition: `KEEP | REVISE | ROLL_BACK | HOLD`.

A production call cannot be counted as successful merely because the Router recommended it.

## 5. Rollback and pause rules

### Local call rollback

Set the call to `ROLL_BACK` when any of the following is true:

- the expected structural change is absent and the change adds complexity;
- continuity or character-knowledge regression is introduced;
- formula risk becomes materially worse than the pre-change version;
- the intervention damages a protected story element;
- a simpler fix becomes clearly sufficient after comparison;
- the manuscript is worse at the target problem after the intervention.

### System pause

Set production Router status to `PAUSED_PENDING_REVIEW` when a real-use event reveals a severe governance failure, including:

- source-book plot/style leakage;
- privacy leakage;
- frozen-semantic broadening;
- automatic/default-on application outside the gate;
- a strong counterexample that calls the current Global boundary into question;
- a repeated real-use regression pattern suggesting the Phase 310 synthetic result does not transfer.

A system pause does not delete historical evidence or lower accepted book/DNA checkpoints. It only stops new production Router applications pending review.

## 6. Real-use evidence ledger

Metadata-only production outcomes are appended to:

`state/production/NOVEL_DNA_REAL_USE_LEDGER_V1.jsonl`

Each event should include:

```text
event_id
production_use_id
recorded_at
dna_id
story_scope
router_result
post_use_disposition
expected_change_met
formula_risk_level
complexity_cost_level
continuity_regression
user_or_reader_outcome
private_artifact_ref
privacy_safe_summary
```

The ledger must not contain manuscript text.

## 7. Evidence maturity

Current evidence supports only this claim:

> The optional Router passed the Phase 310 synthetic structure-level regression benchmark and is eligible for bounded, default-off real-manuscript use with audit and rollback.

Current evidence does not support:

- external independent blind validation;
- statistical universality;
- stable improvement across real user manuscripts;
- default-on production use.

Real-manuscript evidence must accumulate before any stronger production claim is considered.

## 8. GN-VDNA-01 remains frozen

`GN-VDNA-01` keeps its Phase 280 V1 semantics and limits unchanged.

Production promotion changes the Router maturity/status only. Any semantic change to `GN-VDNA-01` requires a new version and revalidation/freeze path.

## 9. Next evidence stage

After this governance promotion, the next evidence track is real-manuscript use and outcome accumulation. It is event-driven: do not invent a manuscript or force a DNA call merely to advance the project.
