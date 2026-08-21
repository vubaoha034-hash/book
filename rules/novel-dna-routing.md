# Novel DNA Routing V1

Status: OPTIONAL / DEFAULT_OFF
Scope: V3 structural diagnosis and planning only
Frozen Global input: `state/frozen_dna/GLOBAL_NOVEL_DNA_FREEZE_V1.json`
Routing readiness contract: `docs/NOVEL_DNA_ROUTING_INTEGRATION_READINESS_V1.md`

This router decides whether a proven story problem should invoke a frozen Novel DNA mechanism. It does not generate premises from DNA templates, does not replace ordinary V3 craft fixes, and does not change any frozen Book-level, Cross-Book, or Global DNA semantics.

## 1. Non-negotiable routing order

Use this order every time:

1. Locate concrete `problem_evidence` in the current story or draft.
2. Try the simpler V3 repair first.
3. Only if the simpler repair is insufficient, test a relevant DNA invocation gate.
4. Remove same-lineage ancestors/successors so one causal mechanism is not counted twice.
5. Select the minimum necessary DNA scope for the proven problem.
6. Check both the shared cross-layer budget and the selected DNA's own frozen limits; the stricter limit wins.
7. Record expected change, complexity cost, formula risk, protected elements, and exit criteria.
8. Return `REJECT` or `HOLD` when evidence is incomplete.

No `problem_evidence` => `DNA_CALL = REJECT`.

No credible explanation of why the simpler repair is insufficient => `DNA_CALL = REJECT`.

No `exit_criteria` => the call cannot be `APPLIED`.

## 2. Simpler-fix precedence

DNA is not a prestige layer and must not replace ordinary craft repairs. Prefer the existing V3 machinery when it is sufficient, including:

- causal repair;
- continuity repair;
- ordinary callback;
- ordinary setup/payoff;
- scene-function repair;
- emotion-debt/payoff repair;
- character-choice repair.

If one of these solves the actual problem without breaking the reader promise, do not invoke DNA.

## 3. Layer semantics

The available layers are:

- `GLOBAL`
- `CROSS_BOOK`
- `BOOK_LEVEL`

Layer name is evidence scope, not automatic priority. A Global DNA does not override a distinct Book-level or Cross-Book mechanism merely because it is more abstract.

### Same-lineage supersession

If multiple approved IDs describe the same causal lineage, only the current highest approved successor may be used for application.

Current locked lineage rule:

- `GN-VDNA-01` is the system-level application successor of `CBDNA-C02-V2`.
- Application records use `GN-VDNA-01`.
- `CBDNA-C02-V2` remains provenance and must not be counted as a second simultaneous DNA call.
- A Book-level ancestor subcore already fully absorbed by `GN-VDNA-01` must not be double-counted.

A residual mechanism may still be used if it solves a distinct causal problem not covered by the Global core.

## 4. Shared cross-layer budget

Budgets are shared across all DNA layers; each layer does not receive a separate quota.

System-wide ceilings:

- Scene: max 1 Primary DNA total.
- Scene: optional max 1 Secondary diagnostic check.
- Chapter / arc: max 2 Primary DNA total.
- Book: max 3 Primary DNA total.
- Short story: default max 1 Primary; Global DNA stays OFF unless there is clear cross-stage recurrence.

These are ceilings, not permissions. Every selected DNA's own frozen application limits still apply, and the stricter limit always wins.

Current `GN-VDNA-01` V1 limits from `GLOBAL_NOVEL_DNA_FREEZE_V1.json` are stricter:

- Scene Primary: default `OFF`.
- Scene Secondary diagnosis: max 1.
- Chapter Primary: max 1.
- Arc Primary: max 1.
- Book Global Primary: max 1.
- Short story: `OFF` unless clear cross-stage recurrence exists.

Do not fill unused quota for completeness.

## 5. GN-VDNA-01 invocation gate

`GN-VDNA-01 | RECURRING_NARRATIVE_ASSET_GAINS_CAUSAL_MEANING`

The V1 semantics are frozen. All of the following are required:

1. The asset was previously established.
2. It is a high-weight narrative asset for the current story.
3. It recurs across stages.
4. The recurrence gains new causal meaning.
5. It changes at least one of: understanding, choice, risk, relationship, goal.
6. It retains prior memory value.
7. Callback / continuity fix / ordinary setup-payoff is insufficient.

Reject this DNA for:

- repeated motif without causal change;
- same-function reuse;
- one-shot setup/payoff;
- background-only exposition;
- retcon that erases prior meaning;
- late万能 asset insertion;
- all-details-are-foreshadowing overdesign.

`Global` here means the highest-level reusable mechanism currently frozen inside this novel-distillation system. It is not a mandatory universal law for all good fiction and is not a claim of statistical universality.

## 6. Candidate discovery discipline

Do not load the full DNA registry by default.

- First classify the proven problem.
- Load only the manifest or contract needed for plausible candidates.
- Do not browse Book-level DNA merely to find something to apply.
- Do not convert source-book surface similarity into a DNA match.
- Cross-Book and Book-level frozen semantics remain immutable unless their own versioning path authorizes a new validation/freeze cycle.

## 7. V3 integration position

### New creation

- Phase 0 / 1: DNA OFF. Do not generate premise, protagonist, world, or ending from a DNA template.
- Phase 2: finish causal, emotion-payoff, and hate/empathy evidence first.
- After Phase 2: run this optional Router only if a structural problem remains concretely proven.
- Phase 4: only already-approved `APPLIED` DNA calls may constrain scene planning.
- Phase 5: prose generation receives only the minimal active DNA instruction needed for the current scene; never load the full registry.
- Phase 8: validate only DNA calls explicitly declared as applied.
- Phase 10: DNA OFF. DNA does not govern sentence style or de-AI editing.

### Existing-draft diagnosis

First locate the upstream failure using the V3 order:

`promise -> causality -> character choice -> emotional debt -> scene function -> continuity -> prose`

Only after the upstream failure is located may this router test a structural DNA mechanism.

## 8. Required call record

Use `templates/dna-call-record-template.md`.

Every call must record at least:

```text
dna_layer: GLOBAL | CROSS_BOOK | BOOK_LEVEL
dna_id:
mode: DIAGNOSE | PLAN | REWRITE | VALIDATE
story_scope: SCENE | CHAPTER | ARC | BOOK
problem_evidence:
trigger_condition_met:
why_simpler_fix_is_insufficient:
lineage_supersession_check:
selected_action:
protected_story_elements:
expected_change:
complexity_cost:
formula_risk:
exit_criteria:
result: APPLIED | REJECTED | HOLD | ROLLED_BACK
```

No `problem_evidence`, no `why_simpler_fix_is_insufficient`, or no `exit_criteria` => cannot be `APPLIED`.

## 9. Prose-context rule

When a DNA call is active, prose generation receives only:

- active DNA ID;
- one-sentence problem evidence;
- selected action;
- protected story elements;
- expected change;
- exit criteria.

Do not inject source-book examples, full provenance, full registry, all invocation gates, or frozen analysis documents into prose context.

## 10. Copyright and style boundary

Novel DNA transfers abstract causal structure only.

Forbidden:

- copying source-book plot chains, characters, settings, organizations, signature objects, or scene order;
- imitating a living author's identifiable style;
- replacing names while preserving recognizably equivalent source-book plot architecture;
- using source text as prose-generation context.

## 11. Result semantics

- `APPLIED`: gate passed, simpler fix insufficient, budget available under both shared and DNA-specific limits, and exit criteria defined.
- `REJECTED`: evidence or gate does not justify the DNA, a simpler fix is sufficient, or a frozen application limit forbids the call.
- `HOLD`: evidence is incomplete or the mechanism boundary is ambiguous.
- `ROLLED_BACK`: an applied DNA did not produce the expected change or introduced unacceptable complexity/formula risk.

An `APPLIED` record is a controlled experiment inside the current story, not proof that the story is good.
