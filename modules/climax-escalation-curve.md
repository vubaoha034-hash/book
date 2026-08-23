# Climax Escalation Curve V1

## Purpose

Detect climaxes that contain many events but little increase in pressure, meaning, or irreversible choice.

## Core principle

`EVENT_VOLUME != CLIMAX`.

## Required escalation ledger

For each major escalation step record:

- available_options_before
- option_removed_or_made_costlier
- new_personal_stake
- prior_relationship_or_asset_reactivated
- reader_model_change
- protagonist_choice
- immediate_cost
- irreversible_change
- pressure_after

## Failure codes

`CLIMAX_HAS_EVENT_VOLUME_WITHOUT_OPTION_COMPRESSION`
: attacks, arrivals, reveals, or reversals accumulate while meaningful options and stakes remain essentially flat.

`CLIMAX_LACKS_PERSONAL_CONVERGENCE`
: large external action does not force earlier relationships, promises, losses, or values into the protagonist's immediate choice.

`CLIMAX_RELEASE_HAS_NO_PAYOFF_OR_AFTERSHOCK`
: the main pressure ends without a proportionate visible payoff, loss, changed relationship, or new irreversible state.

## False-positive controls

A quiet climax may pass if it forces an irreversible choice with high accumulated stakes. A large battle may fail if it only increases spectacle.

## Revision rule

Escalate by narrowing choices and making earlier narrative assets expensive, not by adding more combatants or explanations.
