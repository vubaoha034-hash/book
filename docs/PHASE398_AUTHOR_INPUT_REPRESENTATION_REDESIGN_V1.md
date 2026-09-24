# PHASE398 Author Input Representation Redesign V1

Status: ACTIVE DESIGN / NO PROSE GENERATION

Task: PHASE398_AUTHOR_INPUT_REPRESENTATION_REDESIGN_V1

## 1. Why Phase398 exists

Phase397 closed as a negative transfer result for narrative transportation. The A3 runner already told the writer not to translate substrate items into paragraphs, not to explain inferred meaning twice, and not to overuse one-line paragraphs. The failure nevertheless survived.

Therefore the next architecture cannot be "the same event substrate plus stronger wording".

The material change must be upstream: change what the writer receives.

## 2. Evidence boundary

Phase397 A2/A3 show that ordered or quasi-ordered scene substrates remain visible through prose. The renderer can satisfy the facts while still following an implicit beat ladder.

Historical human-positive Phase394 prose and the Phase370 positive bounded span show a different page-level reality:
- multiple physical objectives continue at once;
- characters do not exist only to reveal information;
- environment and danger continue independently of exposition;
- relationships appear through practiced behavior, hesitation, timing and material detail;
- meaning can remain inside action instead of being immediately restated.

These observations are evidence, not a style recipe. Phase398 must not turn them into sentence quotas, dialogue tricks, or mandatory surface devices.

## 3. New representation: SCENE_FIELD_AUTHOR_PACKET_V1

The writer receives a simultaneous dramatic field, not a route.

The packet describes what exists now, who wants what now, what each person knows or misreads, what the environment is already doing, which pressures are active, which facts are immutable, and what must still be true at the terminal boundary.

It does not tell the writer:
- what happens first;
- what clue appears second;
- when a relationship detail must surface;
- which paragraph carries which fact;
- how many short or long paragraphs to use;
- when to explain a mystery;
- how to imitate the positive anchor.

## 4. Required packet layers

### 4.1 Fixed world facts
Immutable facts only. No sequence semantics.

### 4.2 Character agents
Each important character is represented as an autonomous agent with:
- immediate physical objective;
- immediate emotional pressure;
- what they are trying to avoid;
- private knowledge;
- mistaken belief or uncertainty;
- current bodily condition;
- what they notice easily and what they are likely to miss.

The purpose is to let characters create events by colliding priorities rather than by serving a beat sheet.

### 4.3 Relationship residues
Only present-tense residues that can affect behavior now:
- habits;
- practiced coordination;
- avoided topics;
- material objects with lived use;
- asymmetries of trust;
- unfinished obligations.

No exposition paragraph is requested. No symbolic meaning is prescribed.

### 4.4 Environmental processes
Processes that continue whether or not the protagonist looks at them:
- people working;
- weather;
- traffic;
- ritual;
- crowd movement;
- physical hazards;
- institutional routines.

Environment must not wait for a clue to finish.

### 4.5 Pressure field
Simultaneous pressures and affordances, represented without ordering:
- danger;
- time pressure;
- social exposure;
- conflicting obligations;
- opportunities to move, hide, ask, refuse, observe or misread.

These are possibilities and constraints, not beats.

### 4.6 Information asymmetry
For each important fact:
- who knows it;
- who suspects it;
- who falsely believes the opposite;
- who does not know it.

This replaces reveal sequencing with a world-state model.

### 4.7 Mystery boundary
Facts that must remain unresolved or unspoken.

### 4.8 Terminal world-state boundary
Only state what must be true by the end of the bounded scene.

Example structure:
- character X is still alive;
- object Y remains unopened;
- relationship Z has materially changed;
- central mystery remains unresolved.

Do not specify the route.

## 5. Structural anti-leak rules

The packet itself must pass a representation audit before any writer sees it.

BLOCK if:
- event IDs imply chronological numbering;
- a field is named beats, steps, sequence, reveal_order, paragraph_plan or equivalent;
- the packet tells the writer when a clue must appear;
- a list can be read as "do item 1, then item 2";
- relationship details are assigned to a specific paragraph or reveal moment;
- evaluator diagnoses or threshold metrics appear in writer-visible content;
- the positive anchor is converted into explicit surface imitation rules.

Arrays may exist only when their semantics are explicitly unordered. Prefer keyed maps where possible.

## 6. Separation of authoring and evaluation

Writer-visible layer:
- scene-field packet;
- exact source/fact locks;
- bounded output request.

Writer-hidden layer:
- AI-smell diagnosis;
- anti-storyboard metrics;
- mechanical-dialogue blocker thresholds;
- source-fidelity evaluator;
- human-review rubric.

A writer must not receive the post-generation answer key.

## 7. Later execution protocol

Phase398 itself does not generate prose.

A future authorized pilot must:
1. build a story-specific scene-field packet;
2. audit it for sequence leakage;
3. freeze the packet;
4. create a fresh isolated writer context;
5. expose only the frozen writer entry;
6. freeze returned prose unchanged;
7. run source fidelity and structural gates;
8. only then reach actual-human review.

A successful architecture design does not prove prose transfer.

## 8. Acceptance for Phase398 design

PASS only if:
- representation is materially different from Phase396/397 event traces;
- no normative event order exists;
- independent character agency is representable;
- environment is independently active;
- relationship specificity is representable without a backstory dump;
- mystery can remain open without a reveal schedule;
- evaluator diagnostics remain hidden;
- no fiction is generated.

## 9. What Phase398 is not

It is not:
- A4;
- a rewrite of A3;
- a stronger anti-AI prompt;
- a sentence-length rule;
- a dialogue recipe;
- a guarantee that the next prose will be good;
- permission to advance the Phase320 accepted checkpoint.

The only claim at design completion is that a materially different author-input architecture exists and is ready for a separately authorized story-specific packet build.
