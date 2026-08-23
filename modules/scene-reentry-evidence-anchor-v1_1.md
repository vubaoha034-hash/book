# Scene Re-entry Evidence Anchor V1.1

## Purpose

Prevent an evaluator from inventing a plausible new reason for a return after the fact.

V4.1 requires a post-withdrawal decision delta. V1.1 adds a strict evidence-anchor rule: the new delta must be textually available to the returning character, not merely useful to the scene.

## Required evidence for a material re-entry after withdrawal

Record:

- prior explicit withdrawal/leave/refusal choice;
- exact motives and information already active then;
- exact later textual event alleged to change the choice;
- evidence that the returning character perceived, learned, remembered or was obligated by that event before re-entry;
- why that new information/condition changes the decision;
- re-entry cost;
- first consequential action.

## Core prohibition

Do not infer a post-choice trigger from the character's new function after they reappear.

Examples of invalid reasoning:

- `there are now wounded people, therefore the healer must have returned because of them` when the text never shows the healer learning this before return;
- `the battle got worse, therefore the friend came back` when no report/perception reaches the friend;
- `the character still cared` when that care existed at the moment of withdrawal.

## Failure codes

`REENTRY_DELTA_NOT_TEXTUALLY_AVAILABLE_TO_CHARACTER`
: the audit names a changed scene condition but cannot locate evidence that the returning character perceived/learned it before reversing course.

`POST_REENTRY_FUNCTION_BACKFILLED_AS_PRE_REENTRY_MOTIVE`
: the evaluator infers why a character returned from what they do after returning, rather than from a prior decision-changing trigger.

Inherited V4.1 re-entry codes remain active:
- `REENTRY_REVERSAL_HAS_NO_DECISION_DELTA`
- `OLD_MOTIVE_REUSED_AS_POST_HOC_REENTRY_CAUSE`

## False-positive controls

No new trigger is required when the earlier movement was not a genuine withdrawal or when a continuing obligation with an already-established schedule naturally carries into the later scene.

## Core question

`What exact text proves this character had a new reason before they re-entered?`

If there is no answer, do not rescue the re-entry with scene utility.
