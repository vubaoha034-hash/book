# Scene Re-entry Decision Delta V1

## Purpose

Harden scene-entry motivation when a character explicitly chose to withdraw, leave, refuse, or remain outside the active conflict and later reverses that choice.

Spatial feasibility and old relationship motives are not enough. If those facts already existed at the time of withdrawal, they cannot by themselves explain the reversal.

## Required record for explicit reversal

- prior explicit withdrawal / exit choice;
- motives and information already present when that choice was made;
- new post-withdrawal perception, report, loss, request, obligation change, threat, opportunity or remembered fact;
- why the new delta changes the decision;
- cost of reversing course;
- first consequential action after re-entry.

## Failure codes

`REENTRY_REVERSAL_HAS_NO_DECISION_DELTA`
: a character reverses an explicit prior exit/withdrawal decision without any located new condition after that decision.

`OLD_MOTIVE_REUSED_AS_POST_HOC_REENTRY_CAUSE`
: the audit justifies the reversal using a relationship, desire or obligation that was already active when the character chose to leave.

## False-positive controls

No new trigger is required when:

- the prior movement was not actually a withdrawal decision;
- the character only moved position while maintaining the same active task;
- the earlier scene explicitly established a continuing obligation whose next scheduled action naturally occurs later.

## Core test

Ask:

`What changed after the character decided to leave?`

If the answer is only `they still cared`, `they were nearby`, or `the scene needed them`, the reversal is not causally dramatized.
