# MICROCRAFT Dialogue Grounding Hardening V1.1

## Why this hardening exists

A correctly bound fresh/no-hint G6D regression on the preserved historical manuscript rediscovered the pre-registered local semantic-time failure but missed both pre-registered dialogue failures:

- author-information mouthpiece in an ordinary early dialogue bundle;
- rhetorical question/retort/follow-up scaffold without a supported character motive.

The same evaluator successfully found an additional non-seed execution-time contradiction. Therefore the evidence does **not** support abandoning G6D. It supports a narrower conclusion:

- local semantic-chain reasoning has real fresh evidence;
- dialogue grounding discrimination is too permissive;
- reviewers can rescue weak dialogue by inventing plausible speaker motives or by evaluating only the conversation's final effect.

Do not repeat fresh attempts until one happens to pass. Fix the discriminator first.

## V1.1 corrections

### 1. Textual speaker-goal evidence

A PASS may not rely on an imagined motive. High-information turns must cite manuscript evidence for the claimed scene goal.

### 2. Exact-bundle no-reader counterfactual

Replace “would the speaker say something?” with “would the speaker say approximately this entire bundle, with this completeness, to this listener now?”

### 3. Atomic information claims

Split multi-fact exposition. One legitimate warning or new fact does not rescue several listener-unneeded facts packaged around it.

### 4. Per-turn state delta

Rhetorical ladders are audited turn by turn. A useful final line cannot retroactively justify an empty clever retort that exists only to manufacture the next question.

### 5. Bluff/deflection evidence

Do not rescue swaggering or evasive lines by saying “maybe bluffing” unless the scene provides pressure or later behavior that supports deterrence, concealment, face-saving, provocation, or protection.

### 6. Ordinary-dialogue coverage

Regression and pre-delivery G6D must inspect casual early/mid-scene exposition and banter, not only climaxes and high-drama dialogue.

## Files changed

- `rules/scene-to-speech-microcraft.md` -> V1.1
- `modules/dialogue-trigger-anchor.md` -> V1.1
- `templates/microcraft-dialogue-audit-template.md` -> V1.1
- `config/novel-quality-gates.v3.json` -> schema 3.0.1
- `rules/pass-isolation.md` -> hardened G6D isolation rules
- `benchmark/microcraft/dialogue-regression.v2.json` -> 20 adversarial cases

## What this does not prove

These changes do not prove literary quality and do not prove the two missed manuscript instances will be rediscovered in a new fresh context.

The next valid evidence must come from a new fresh/no-hint regression bound to an immutable post-hardening machinery commit. The historical manuscript must remain unchanged until that result is preserved.
