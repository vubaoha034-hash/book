# Reader Propulsion Ledger V1

## Purpose

Detect causally valid prose that does not create a reason to continue reading.

## Core distinction

`EVENT_PROGRESS != READER_PROPULSION`.

For every material scene/beat record:

- reader_question_before
- current_pressure
- expected_reward_or_fear
- concrete_new_information_or_choice
- reward_delivered
- cost_or_complication
- reader_question_after
- next_scene_pull
- skimmable_without_loss: LOW | MEDIUM | HIGH
- verdict: PASS | HOLD | FAIL

## Failure

Use `READER_PROPULSION_COLLAPSE` when a meaningful span advances events but repeatedly fails to strengthen curiosity, emotional anticipation, conflict pressure, reward expectation or consequential choice.

Do not use a numeric interval threshold. Evidence must name the span and explain what a reader is waiting for and why the text stops feeding that desire.

## False-positive controls

Do not fail quiet scenes merely for low action. A quiet scene may pass if intimacy, dread, grief, expectation, understanding or choice pressure grows.

Do not equate more events, more enemies, more names or more reveals with propulsion.

## Revision rule

Prefer changing the scene's reader promise/reward/complication, not adding cliffhanger phrases.
