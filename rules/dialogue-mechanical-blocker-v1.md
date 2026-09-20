# Dialogue Mechanical Blocker V1

Status: POST-FREEZE DELIVERY BLOCKER  
Scope: 《一命过桥》 bounded prose candidates  
Writer visibility: FORBIDDEN

## 1. Purpose

This rule exists because the actual target reader has repeatedly rejected prose when dialogue falls into visible turn-by-turn machinery.

The blocker is NOT a writing recipe.

It runs only after a candidate has been generated and frozen.

The writer must never receive this document, its labels, its thresholds, or its located failures.

## 2. Two independent blocker layers

### Layer A — deterministic structural tripwire

Run:

`python scripts/check_dialogue_adjacency.py <candidate.txt>`

The script may only identify obvious high-risk dialogue geometry.

It may output:

- CLEAR
- BLOCK

A BLOCK is sufficient to reject the candidate.

A CLEAR is NOT sufficient to approve literary quality.

### Layer B — semantic mechanical-dialogue blocker

A separate evaluator reads the frozen candidate and asks only whether the candidate contains located stretches where dialogue functions mainly as an exact response-completion machine.

The evaluator must ignore whether the lines are witty, short, realistic in isolation, or surrounded by gestures.

Block when a located stretch strongly shows at least two of the following:

1. **Exact adjacency completion**  
   Each turn is primarily the most relevant response to the immediately previous turn.

2. **Single shared conversational agenda**  
   Characters keep cooperating with the same question/topic rather than pursuing independent priorities.

3. **Turn-order speaker identity**  
   If names and attributions are masked, speaker identity is recoverable mainly from alternation or role, not from character-owned behavior/relationship.

4. **Subtext explicitation**  
   One character cleanly states the hidden motive, emotion, relationship meaning, or thematic interpretation that the scene has just implied.

5. **Gesture padding without geometry change**  
   Small actions appear between turns but the underlying sequence is still question -> answer -> follow-up -> answer.

## 3. Hard settlement rule

If Layer A returns BLOCK OR Layer B returns BLOCK:

- candidate status = REJECT_MECHANICAL_DIALOGUE;
- do not show it as an accepted prose candidate;
- do not locally patch the dialogue;
- do not feed the blocker feedback to the same writer;
- do not preserve “good lines” by splicing them into a repair;
- any replacement requires a genuinely fresh writer context and a separately authorized attempt.

## 4. What this blocker does NOT ban

Do not infer any universal rule such as:

- questions are bad;
- direct answers are bad;
- short dialogue is bad;
- banter is bad;
- two people may not exchange several lines;
- action must interrupt every sentence.

The target is repeated visible conversation machinery, not a surface form.

## 5. Positive comparison boundary

Historically human-positive Phase363 prose often contains simple dialogue.

Its difference is not a quota.

Characters frequently continue their own physical objective, refuse the conversational premise, infer information without asking, or let action change the situation before an answer arrives.

The blocker must not reward imitation of those exact devices.

## 6. Delivery gate

A candidate may reach actual-human review only if:

- frozen bytes exist;
- deterministic tripwire is CLEAR;
- semantic blocker is CLEAR;
- no repair occurred after freeze.

Passing this gate means only “not blocked for this known recurrent failure.”

It does not mean the prose is good, accepted, low-AI, or ready to scale.
