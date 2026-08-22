# MICROCRAFT Anti-Template Hardening V1.3

Status: DEVELOPMENTAL / FRESH REGRESSION REQUIRED
Phase: 343

## Trigger

A correctly bound Fresh G6D V1.2 regression successfully rediscovered the pre-registered temporal semantic-chain failure and the exact public-background mouthpiece failure, while preserving legitimate social anecdotes. However, it again missed the pre-registered empty rhetorical ladder even though that exact block had been harvested into `rhetorical_ladder_candidates`.

Observed pattern:

- candidate harvesting succeeded;
- the suspicious ladder was present in the inventory;
- no dedicated anti-template record was emitted for that candidate;
- the final report still stated `per_turn_template_failures: 0`.

Therefore the remaining defect is not primarily candidate discovery. It is **judgment coverage and discriminator weakness inside rhetorical-ladder audit**.

## V1.3 hardening

### 1. Rhetorical-ladder record parity

Every harvested rhetorical-ladder candidate must receive an explicit anti-template record.

For PRE_DELIVERY / REGRESSION:

`rhetorical_ladder_candidate_count == anti_template_record_count`

If not, final G6D cannot PASS.

### 2. Self-cancelling assertion test

When a retort introduces or strongly implies proposition P, then the next turns immediately reveal that the speaker has no basis for P, audit whether P served any supported bluff, concealment, deterrence, face-saving, relationship or task goal.

A temporary false/unsupported state created only to induce the next question is not a meaningful knowledge delta.

### 3. Induced-follow-up dependency

For each turn record whether the following turn exists mainly because the current turn manufactured an uncertainty or false premise.

If:

- retort creates uncertainty;
- follow-up is induced by that uncertainty;
- punchline retracts/nullifies the uncertainty;
- no independent scene goal is evidenced;

then flag `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`.

### 4. Counterfactual turn-deletion test

Remove the suspicious retort and the induced follow-up mentally.

If the scene can move directly to the truthful/useful line with no loss of task state, knowledge required for action, relationship pressure, concealment, negotiation or character-specific history—and the only loss is a generic punchline cadence—the deleted turns are template-risk.

Humor is not forbidden. The test asks whether the humor is character/relationship-specific or a portable scaffold.

### 5. Portability test

A joke/retort is higher risk when it could be transferred to unrelated characters and situations with almost no semantic change.

Portable generic wit does not count as character motive by itself.

Relationship-specific banter may PASS when it depends on shared history, a current object/task, prior grievance, status asymmetry, or later relationship action.

### 6. False-positive protection

Do not fail:

- strategic bluff that changes enemy behavior;
- negotiation between characters with conflicting concrete goals;
- shared-history banter where each correction changes the relationship model;
- teasing that leads to permission, refusal, reconciliation or another relationship state change;
- absurd humor arising from the current physical task rather than a generic Q-retort-Q-punchline scaffold.

## Acceptance

V1.3 may advance only if a new fresh/no-hint manuscript regression:

- uses immutable V1.3 machinery;
- keeps benchmark cases hidden;
- uses the unchanged historical manuscript;
- exactly rediscovers all three pre-registered failures;
- preserves the V1.2 public-background success;
- does not reintroduce the social-anecdote false positive;
- explicitly audits every harvested rhetorical ladder.

Repeated fresh attempts on unchanged V1.3 machinery until a favorable result appears are forbidden.
