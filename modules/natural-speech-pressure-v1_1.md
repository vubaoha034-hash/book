# Natural Speech Under Pressure V1.1

## Purpose

Extend V1 so that a valid scene goal cannot automatically rescue author-shaped speech packaging.

## Required tests for high-information speech

### 1. First-priority utterance test
What is the first thing this speaker most urgently needs the listener to understand or do right now?

If the sentence begins by restating lower-priority shared background mainly so the reader can follow, record risk.

### 2. Turn-segmentation test
Split the speech at every independently actionable fact or conclusion.

For each segment ask:
- would the listener plausibly react, interrupt, infer, object or act here?
- if yes, why does the speaker continue through later segments without a turn?

A polished one-breath package requires scene support such as briefing duty, testimony, confession, rehearsed persuasion or uninterrupted time.

### 3. Shared-context subtraction test
Remove information the listener already knows.

If most of the polished sentence disappears while the actual new urgent payload is small, check whether known information is genuinely needed to quote a rumor, frame an accusation or mark public exposure. Do not assume repetition is justified merely because it is meta-information.

### 4. Human omission test
Given pressure and relationship, what would this speaker naturally leave unsaid because the listener can infer it?

### 5. Environmental carrier test
Can visible arrival, sound, crowding, injury, object or interruption carry part of the information more naturally than a complete spoken packet?

## Failure codes

`LIVE_SPEECH_OVERSEGMENTATION_SUPPRESSED`
: several independently reactable facts are compressed into one polished turn without a scene-supported reason for uninterrupted delivery.

`SHARED_CONTEXT_RESTATED_FOR_READER_ORIENTATION`
: known context is repeated mainly to orient the reader and is not required by the speaker's immediate goal.

`VALID_GOAL_BUT_AUTHOR_SHAPED_UTTERANCE`
: the speaker has a real reason to speak, but the exact organization of the speech remains implausibly writer-shaped.

Inherited V1 codes remain active:
- `SPEECH_PACKAGE_DOES_NOT_MATCH_HUMAN_PRESSURE`
- `CHARACTER_SPEAKS_IN_AUTHOR_SUMMARY_UNITS`
- `DIALOGUE_HAS_NO_HUMAN_OMISSION_OR_INFERENCE`

## False-positive controls

Formal briefing, testimony, public speech, deliberate persuasion and confession may be complete when the scene supports continuous delivery.

Do not repair with filler particles, slang, fake stammering or generic gestures. Repair information order and turn-taking logic.
