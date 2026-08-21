# Novel DNA Routing & Integration Readiness V1

Status: READY_FOR_BOUNDED_INTEGRATION
Source checkpoint: Phase 280 `GLOBAL_NOVEL_DNA_FREEZE_AND_GOVERNANCE`
Global registry: `GN-VDNA-01`

This document defines routing and integration boundaries only. It does not change any frozen Book-level, Cross-Book, or Global DNA semantics and does not auto-apply DNA to writing.

## 1. Core routing order

Use this order for all future DNA calls:

1. Locate concrete `problem_evidence` in the current story/draft.
2. Try a simpler V3 fix first.
3. Only if the simpler fix is insufficient, test DNA invocation gates.
4. Deduplicate same-lineage ancestors/successors.
5. Select the minimum necessary DNA scope for the proven problem.
6. Record expected change, complexity cost, formula risk, and exit criteria.
7. Default to `REJECT` or `HOLD` when evidence is incomplete.

No `problem_evidence` => no DNA call.

## 2. Simpler-fix precedence

DNA must not replace ordinary craft repairs. Prefer the existing V3 modules when they are sufficient, including:

- causal repair;
- continuity repair;
- ordinary callback;
- ordinary setup/payoff;
- scene-function repair;
- emotion-debt/payoff repair;
- character-choice repair.

If one of these solves the problem without breaking the reader promise, `DNA_CALL = REJECT`.

## 3. Layer semantics

`GLOBAL` does not mean automatic priority over every Cross-Book or Book-level DNA.

Different DNA may solve different causal problems. Selection is driven by evidence and invocation gates, not by layer name.

### Same-lineage supersession

When multiple layers describe the same causal lineage, use only the current highest approved successor for application.

Current rule:

- `GN-VDNA-01` is the system-level successor of `CBDNA-C02-V2`.
- Application records use `GN-VDNA-01`.
- `CBDNA-C02-V2` remains provenance and must not be counted as a second simultaneous DNA call.
- A Book-level ancestor subcore already fully absorbed by `GN-VDNA-01` must not be double-counted.

### Residual mechanisms

A Cross-Book or Book-level residual may still be used when it solves a distinct mechanism not covered by the Global DNA.

## 4. Cross-layer shared budget

Budgets are shared across all DNA layers; each layer does not get a separate quota.

- Scene: max 1 Primary DNA total; optional 1 Secondary diagnostic check.
- Chapter/arc: max 2 Primary DNA total.
- Book: max 3 Primary DNA total.
- Short story: default max 1; Global DNA remains OFF unless there is clear cross-stage recurrence.

## 5. GN-VDNA-01 gate

`GN-VDNA-01 | RECURRING_NARRATIVE_ASSET_GAINS_CAUSAL_MEANING`

All of the following are required:

1. The asset was previously established.
2. It is a high-weight narrative asset for the current story.
3. It recurs across stages.
4. The recurrence gains new causal meaning.
5. It changes at least one of: understanding, choice, risk, relationship, goal.
6. It retains prior memory value.
7. Callback / continuity fix / ordinary setup-payoff is insufficient.

Reject for:

- repeated motif without causal change;
- same-function reuse;
- one-shot setup/payoff;
- background-only exposition;
- retcon that erases prior meaning;
- late万能 asset insertion;
- all-details-are-foreshadowing overdesign.

## 6. V3 integration position

The canonical V3 entrypoints remain `SKILL.md` and `workflows/07-novel-master-pipeline-v3.md`.

### New creation

- Phase 0/1: DNA OFF. Do not generate the premise from a DNA template.
- Phase 2: finish causal/emotion/hate-empathy ledgers first.
- After Phase 2: optional DNA Routing Gate only if a structural problem remains proven.
- Phase 4: only already approved DNA calls may enter scene planning.
- Phase 5: prose generation loads only minimal information for an active DNA call; never load the whole registry.
- Phase 8: validate only DNA calls explicitly declared as applied.
- Phase 10: DNA OFF; DNA does not control line style or de-AI editing.

### Existing-draft diagnosis

First locate the upstream failure using the V3 order:

`promise -> causality -> character choice -> emotional debt -> scene function -> continuity -> prose`

Only then may a DNA router match a mechanism.

## 7. Required call record

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

## 8. Integration target and legacy boundary

Do not integrate `GN-VDNA-01` by adding it to `library/global-technique-bank.md` or by auto-loading it from legacy `workflows/03-apply-to-draft.md`.

Those files remain compatibility assets. The Global Novel DNA system must use a dedicated router so that versioning, provenance, invocation gates, and shared budgets are preserved.

## 9. Phase 300 bounded implementation

The next implementation may only:

- add a dedicated DNA routing rule/module;
- add a DNA call-record template;
- add a minimal optional routing entry in `SKILL.md`;
- add an optional DNA Routing Gate to `workflows/07-novel-master-pipeline-v3.md` without renumbering the V3 phases;
- update README for the user-facing integration change;
- run `scripts/validate_skill.py`;
- preserve all frozen DNA semantics;
- keep all DNA default OFF.

It must not:

- modify `GN-VDNA-01` semantics;
- auto-apply DNA to every story;
- load all DNA into prose generation;
- modify legacy Workflow 03 or `global-technique-bank.md` as the integration mechanism;
- promote `CBDNA-C01`, `CBDNA-C03`, or `CBDNA-C04` to Global;
- copy source-book plot or identifiable style.

After implementation, a separate integration regression/benchmark gate is still required before claiming the router improves production writing.
