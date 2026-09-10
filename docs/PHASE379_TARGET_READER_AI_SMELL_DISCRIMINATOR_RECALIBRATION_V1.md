# PHASE379 — Target Reader AI-Smell Discriminator Recalibration V1

Status: ACCEPT_DIAGNOSTIC_RECALIBRATION / GENERATION_REPAIR_UNPROVEN

## 1. Trigger

Phase378 produced a blinded actual-human result that contradicted the sealed pre-human model evaluator.

Sealed mappings revealed only after verdict:
- A = R1 = PROCESS
- B = R2 = CONTROL

Actual human:
- questions 1–6: B on every comparison;
- A AI smell: very heavy;
- B AI smell: some, but clearly lighter;
- first located A AI-smell example: `你要那个？ / 他说过给我。 / 什么时候？`;
- A also felt messy enough to create a skim/stop urge.

The sealed evaluator had predicted the opposite direction: R1 lower AI smell than R2.

Therefore the Phase377 evaluator failed this replicate and cannot be used as a quality gate.

## 2. What Phase377 got right, and what it missed

Phase377 correctly rejected several crude rules:
- short sentence != AI;
- explanation != AI;
- concrete object density != AI.

Its global diagnosis, `GLOBAL_AUTHORIAL_OPTIMIZATION_REGULARITY`, remains supported as a plausible family: machine prose can feel constructed when every anomaly, observation, inference and next action is too efficiently organized.

But Phase378 proves that reducing that global regularity is not sufficient. The PROCESS arm lowered several Phase377 signatures according to the model evaluator yet became substantially worse for the target reader.

The missing high-weight layer is local conversational geometry.

## 3. New high-priority discriminator candidate

### AS-F01 — FUNCTIONALLY_EXACT_DIALOGUE_ADJACENCY_LADDER

High-risk form:

`useful question -> exactly sufficient answer -> exactly useful follow-up -> exactly sufficient answer`

The defect is not shortness. It is functional precision and repeated information extraction.

In the human-located A passage:

- one speaker asks whether the other wants the toolbox;
- the reply supplies exactly the ownership claim;
- the next question asks exactly the timing needed to advance the conflict.

Each turn behaves like one node in a state machine.

By contrast, CONTROL/B presents the same story facts with more embedding: the apprentice states the object and promise in his own longer utterance; the brother physically handles the box and gives a socially loaded response; environmental action and viewpoint reaction intervene before the next factual interrogation. B later still contains short Q/A, which proves that short Q/A itself is not the rule.

Real-source contrast points the same way. 《盗墓笔记》 can contain rapid short turns, but dialect, hierarchy, irritation, bad judgment and physical action contaminate pure information extraction. 《诛仙》 uses questions and answers inside gambling jokes, seniority, embarrassment and group teasing. The exchange belongs to people before it belongs to plot logistics.

## 4. Why the PROCESS protocol failed

Phase378 PROCESS attempted to avoid visible authorial optimization by instructing the generator to:
- avoid beat-by-beat planning;
- follow the viewpoint person's immediate social/private attention;
- allow incomplete speech;
- avoid making every detail pay immediate plot function.

The result demonstrates a critical non-equivalence:

`LESS AUTHORIAL OPTIMIZATION != MORE HUMAN PROSE`

The model appears to have converted those abstract process constraints into a synthetic minimalist surface: clipped adjacency pairs, locally fragmented transitions and more loosened attention. The target reader experienced this not as lived spontaneity but as stronger AI smell plus messier flow.

This is the same class of mistake seen earlier in Phase373: a valid diagnosis cannot simply be inverted into a positive generation instruction.

## 5. Revised discriminator architecture

The next evaluator must be layered, not scalar.

### Layer A — target-reader local blockers
High priority:
- repeated functionally exact dialogue adjacency ladders;
- repeated neat setup/retort/follow-up conversational machines;
- locally concentrated Q/A that extracts plot facts turn by turn;
- dialogue whose pragmatic purpose is almost entirely authorial information retrieval.

### Layer B — global organizational signatures
Retain Phase377:
- reader-facing inference closure cadence;
- maximized functional density;
- clue/inference/action cycles;
- character-as-task-processor cognition;
- executive-summary narrator;
- low social idiosyncrasy;
- engineered reveal escalation.

### Layer C — coherence / reading viability
Must remain separate:
- local semantic continuity;
- character motive legibility;
- desire to continue;
- skim/stop urge.

A candidate cannot be called better because Layer B improves while Layer A or C materially worsens.

No numeric weights are promoted from one replicate. For now, an actual-human located high-severity blocker can veto a model's aggregate preference.

## 6. Human-vs-model authority

Phase378 is an explicit directional false positive:

- model evaluator: R1/PROCESS lower AI smell;
- blinded target reader: R2/CONTROL lower AI smell by a wide margin.

Therefore:

`MODEL_AI_SMELL_EVALUATOR = DIAGNOSTIC_ONLY`

until it correctly predicts multiple independent fresh human comparisons.

It may not authorize:
- rewriting;
- span growth;
- long-form scale;
- architecture promotion;
- accepted checkpoint advance.

## 7. What is now rejected

Rejected as current repair strategies:
- repeating the Phase378 PROCESS protocol;
- using `less optimization` as a positive writing recipe;
- deleting explanation as the main AI-smell fix;
- using short-sentence counts as an AI-smell gate;
- relying on a single global evaluator score.

## 8. What remains unproven

Still unproven:
- a reliable automatic AI-smell evaluator for this target reader;
- a generation protocol that consistently reduces AI smell;
- stable short-form transfer;
- long-form transfer;
- any right to reconstruct 《一命过桥》 at scale.

## 9. Next step

Do not write another large sample.

Next phase should test the recalibrated discriminator first on fresh, already-frozen candidate pairs or a new fresh pair with evaluator prediction sealed before human review. The evaluator must prove directional calibration before its diagnosis is used to change generation again.

Highest accepted promotion checkpoint remains Phase320.
