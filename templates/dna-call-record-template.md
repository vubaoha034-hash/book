# Novel DNA Call Record Template

Use this record only after a concrete story problem has been located. DNA is default OFF.

```text
dna_layer: GLOBAL | CROSS_BOOK | BOOK_LEVEL
dna_id:
mode: DIAGNOSE | PLAN | REWRITE | VALIDATE
story_scope: SCENE | CHAPTER | ARC | BOOK

problem_evidence:

trigger_condition_met:
- condition_1:
- condition_2:
- condition_3:

why_simpler_fix_is_insufficient:

lineage_supersession_check:
- same_lineage_ids_seen:
- current_application_successor:
- double_count_removed: true | false

budget_check:
- shared_cross_layer_limit:
- dna_specific_frozen_limit:
- effective_limit_used:

selected_action:

protected_story_elements:
- 

expected_change:

complexity_cost:

formula_risk:

exit_criteria:

result: APPLIED | REJECTED | HOLD | ROLLED_BACK
```

## Hard rules

- No `problem_evidence` => cannot be `APPLIED`.
- If callback, continuity repair, ordinary setup/payoff, causal repair, scene-function repair, emotion-payoff repair, or character-choice repair is sufficient => `REJECTED`.
- No credible `why_simpler_fix_is_insufficient` => cannot be `APPLIED`.
- No `exit_criteria` => cannot be `APPLIED`.
- Shared cross-layer budget applies, but it never loosens a selected DNA's own frozen application limits; the stricter limit wins.
- For current `GN-VDNA-01` V1: Scene Primary defaults OFF; Scene Secondary diagnosis max 1; Chapter Primary max 1; Arc Primary max 1; Book Global Primary max 1; short story stays OFF unless clear cross-stage recurrence exists.
- Same-lineage ancestors and successors cannot be counted as separate simultaneous DNA calls.
- For the current frozen lineage, use `GN-VDNA-01` for application; `CBDNA-C02-V2` is provenance only.
- Prose context receives only the minimal active call information, not the full DNA registry or source-book analysis.
- DNA does not control line style or de-AI editing.
- Do not copy source-book plot, scene order, characters, setting systems, signature objects, or identifiable author style.

## Post-use validation

After the target scope is written or revised, record:

```text
observed_change:
expected_change_met: true | false | partial
new_complexity_introduced:
continuity_regression:
formula_risk_observed:
exit_criteria_met: true | false
final_disposition: KEEP | REVISE | ROLL_BACK | HOLD
```

If the expected structural change is absent, or the DNA introduces more formula/complexity cost than benefit, roll it back rather than preserving it because it is Global or previously validated elsewhere.
