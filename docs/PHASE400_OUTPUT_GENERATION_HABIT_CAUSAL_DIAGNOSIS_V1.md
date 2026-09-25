# PHASE400 Output Generation Habit Causal Diagnosis V1

Status: ARCHITECTURE DESIGN / NO PROSE GENERATION

Task: PHASE400_OUTPUT_GENERATION_HABIT_CAUSAL_REDESIGN_V1

## 1. Why Phase400 exists

Phase398 changed the writer input from ordered event material to an unordered scene-field representation.

Phase399 then tested that representation with one fresh isolated writer. The result preserved hard source facts, but failed in four independent ways:

- writer-output contract: BLOCK;
- deterministic mechanical dialogue: BLOCK;
- semantic mechanical dialogue: BLOCK;
- anti-storyboard / immersion precheck: BLOCK.

The important consequence is that removing explicit event order was not enough. The prose generator rebuilt a visible completion machine on its own.

Phase400 therefore does not add more anti-AI wording. It diagnoses the generation process and changes what a prose writer is allowed to know and how much of the scene it is asked to finish at once.

## 2. What Phase399 actually proved

Phase399 did prove several things:

1. Source/world modeling can remain correct while prose behavior fails.
2. An unordered input packet does not guarantee unordered prose behavior.
3. Mechanical dialogue can reappear even when the writer never sees the mechanical-dialogue blocker.
4. One-line paragraphs are not, by themselves, the root cause.

The contrast with the actual-human-positive Phase370 bounded span is decisive.

Phase399:
- 658 paragraphs;
- 631 at one sentence or less: 95.9%;
- 547 at 16 characters or less: 83.13%;
- deterministic dialogue: 21 blocked runs out of 43.

Phase370 positive span:
- 144 paragraphs;
- 136 at one sentence or less: 94.44%;
- 106 at 16 characters or less: 73.61%;
- deterministic dialogue: 0 blocked runs out of 14.

The paragraph geometry is surprisingly similar. The dialogue geometry is not.

Therefore the next mechanism must not be based on “make paragraphs longer”, “ban short dialogue”, “ask fewer questions”, or “insert action between every line”.

## 3. Primary diagnosis

### 3.1 Omniscient coverage pressure

The Phase398 scene-field packet removed explicit sequence, but one prose generator could still see:

- every major character’s immediate objective;
- every major character’s emotional pressure;
- every major character’s private knowledge;
- every major character’s uncertainty;
- relationship residues;
- all active environmental processes;
- all active pressure fields;
- information asymmetries;
- mystery boundaries;
- terminal world-state requirements.

This is structurally unordered, but cognitively it is still a complete answer key for the whole scene.

A model that sees all of it can optimize globally: it knows what everyone wants, what everyone knows, what must remain unknown, and what state the scene must reach.

That makes “cover the whole packet efficiently” an attractive hidden objective.

### 3.2 Shared-agenda collapse during dialogue

Once dialogue begins, the model repeatedly chooses the most relevant semantic continuation to the immediately previous line.

That produces:

question → answer → narrower question → narrower answer → clarification → answer.

The characters stop behaving like agents with independent physical and social priorities and become cooperating processors of one shared topic.

This is not solved by adding gestures between turns. Phase399 already had gestures, movement, water, boxes and objects around many dialogue chains; the underlying adjacency geometry still remained mechanical.

### 3.3 Whole-scene completion pressure

The writer was asked for one complete bounded scene in one generation.

That creates pressure to:

- surface enough of the packet to justify its existence;
- advance every major pressure;
- use the relationship details;
- reveal the important film clue;
- advance the municipal handover;
- leave the family mystery unresolved;
- move the father-daughter relationship;
- settle the current night.

Even without an event list, those obligations can become a new invisible checklist.

The model then serializes them into paragraph-sized completion units.

### 3.4 Editor-mode leakage

Phase399 ended the fiction and then emitted three editorial directives:

- 强化许雯离开的核心谜团
- 压缩重复的搬运清理段落
- 让胶卷线索更晚更狠地落下

This is preserved as a real failure, not cleaned away.

It shows that the one-shot generation can drift from narrator mode into planning/editor mode near the end of the completion.

This may be a downstream symptom of global scene-completion pressure rather than the primary cause, but it reinforces the need to reduce the writer’s global planning burden.

## 4. What Phase400 rejects

The following are explicitly rejected as primary fixes:

- minimum paragraph length;
- maximum number of one-line paragraphs;
- maximum number of questions;
- mandatory action between dialogue turns;
- forced refusal or interruption quotas;
- sentence-length templates;
- copying Phase370 or Phase394 surface rhythm;
- showing AS-F01 / AI-smell / dialogue-blocker labels to the writer;
- repairing Phase399 A1.

Those interventions either target symptoms or expose the evaluator’s answer key to the generator.

## 5. Selected successor architecture

Architecture ID:

FOCAL_OPAQUE_LOCAL_HORIZON_WRITER_V1

This is one architecture with two coupled changes:

1. focalized / opaque visibility;
2. local generation horizon.

The point is not to make prose artificially indirect. The point is to prevent one prose generator from owning the whole scene’s hidden state and solving it all at once.

## 6. Visibility partition

### 6.1 Coordinator-only world model

The coordinator retains the full frozen scene-field world model.

Coordinator-only information includes:

- non-focal characters’ private knowledge;
- non-focal characters’ hidden objectives;
- non-focal mistaken beliefs not knowable by the focal character;
- full information-asymmetry table;
- terminal world-state boundary;
- evaluator rules and thresholds;
- future-window decisions;
- the reason any later gate blocked.

This layer is never copied wholesale into a prose-writer prompt.

### 6.2 Writer-visible focal projection

A prose writer receives:

- the focal character’s identity;
- the focal character’s current physical objective;
- the focal character’s current emotional pressure;
- the focal character’s private knowledge and uncertainty;
- what the focal character can currently observe;
- public/observable state of non-focal characters;
- relationship residues the focal character can actually know or feel now;
- currently active environmental processes;
- immediate pressures observable from the focal position;
- immutable facts the writer must not contradict;
- mystery boundaries that must not be resolved.

The prose writer does NOT receive the hidden reason another character is acting a certain way unless the focal character actually knows it.

Non-focal characters are therefore allowed to remain partially opaque.

## 7. Local horizon

The writer is not asked to complete the entire scene.

The writer is asked for one bounded continuous passage beginning from the current situation.

The writer is not told:

- how the whole scene must end;
- which clue must appear before which other clue;
- which relationship detail must be used;
- how many packet fields must appear;
- which event must happen next;
- how many paragraphs or dialogue turns to use.

The writer is explicitly free to leave many available facts off-page.

This is a material difference from Phase399.

Phase399 said, in effect: here is the entire scene world; now write the scene.

The successor architecture says: here is what this focal consciousness can currently live through; write this local passage only.

## 8. Why the terminal world-state is hidden

The full terminal world-state was useful for system validation but creates global completion pressure when shown to the prose generator.

Under the successor architecture:

- the coordinator retains the terminal boundary;
- the prose writer does not receive the whole terminal checklist;
- after a frozen local passage, the coordinator checks whether any hard boundary was violated;
- the coordinator may update the world state;
- a later local window requires separate authorization under a future pilot contract.

The writer therefore does not write toward an explicit end-state checklist.

## 9. Why non-focal private objectives are hidden

If a writer knows exactly what every participant privately wants, it can coordinate all dialogue and action toward a globally efficient solution.

Human scene experience is often asymmetric.

A focal character may see:

- another person delaying;
- another person moving an object;
- a pause before an answer;
- a refusal to answer;
- a change in pace;
- a socially awkward detour.

But the focal character does not automatically possess the hidden explanation.

FOCAL_OPAQUE_LOCAL_HORIZON_WRITER_V1 makes that asymmetry structural rather than stylistic.

## 10. Why Phase400 does not select the full actor-simulator pipeline yet

A separate actor-driver + narrator architecture remains plausible.

It is not selected as the first successor because it adds several new moving parts at once and can accidentally recreate an external beat scheduler.

The Phase400 selection uses the smallest material mechanism change that directly targets the strongest current hypotheses:

- remove omniscient hidden-state visibility;
- remove whole-scene completion obligation.

If that later fails prospectively, a separately authorized task may escalate to independent actor drivers.

## 11. Future execution shape

Phase400 itself generates no fiction.

A future separately authorized pilot would have to:

1. choose a genuinely new bounded test story or an explicitly authorized frozen world model;
2. select one focal consciousness before prose generation;
3. build a writer-visible focal projection from the coordinator-only world state;
4. audit the projection for hidden-state leakage;
5. freeze the writer entry;
6. use exactly one fresh isolated writer for one local passage;
7. store and freeze the output verbatim;
8. run source fidelity and existing hidden post-generation gates;
9. only if gates clear, reach actual-human review.

No automatic second window is implied.

## 12. Acceptance boundary for Phase400

Phase400 passes as an architecture-design task only if:

- the failure diagnosis distinguishes paragraph shortness from dialogue/agency geometry;
- the positive human counterexample is preserved;
- writer-visible and coordinator-only information are machine-separable;
- the writer no longer receives non-focal private state wholesale;
- the writer no longer receives the full terminal scene checklist;
- the writer is asked for a local passage rather than whole-scene completion;
- evaluator metrics remain hidden;
- no fiction is generated.

A Phase400 design PASS does not prove that the architecture produces good prose.

It only means the next experiment is materially different from Phase399.
