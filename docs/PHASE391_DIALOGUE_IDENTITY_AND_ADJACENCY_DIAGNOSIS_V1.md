# PHASE391 — Dialogue Identity / Adjacency Diagnosis V1

Status: COMPLETE DIAGNOSIS / NO FICTION GENERATED  
Project: novel-distillation / 《一命过桥》  
Highest accepted promotion checkpoint: Phase320（不变）

## 1. Human evidence boundary

Binding actual-human evidence comes from Phase390:

- overall: FAIL;
- AI smell: VERY HEAVY;
- user-located problem: dialogue is mechanical;
- speaker identity is not carried strongly by character voice itself;
- the reader can often infer who is speaking only because of turn order, role or nearby narration.

This report does not convert any model preference into human evidence.

## 2. Comparison basis

Rejected sample:

- Phase390 frozen output.

Human-positive comparison:

- Phase363 Round3 fusion pack, which the actual target reader had previously accepted as materially better and as a useful prose direction.
- Phase369/370 are supporting positive bounded evidence, not final quality standards.

Important boundary:

Character voice is NOT defined as “every isolated sentence must be uniquely attributable with no context.”

Human dialogue identity can come from:

- conversational strategy;
- what the person refuses;
- what they notice;
- what they do instead of answering;
- relationship permissions;
- action priority;
- social position;
- rhythm of interruption and silence.

The test therefore evaluates both isolated wording and scene-integrated speech behavior.

## 3. TEST 1 — Masked-speaker identifiability

### Phase390

Located sequence:

- “刘叔。”
- “又怎么了？”
- “你还欠我五文。”
- “记账。”
- “你每次都这么说。”
- “那说明我没赖账。”

If names and explicit attributions are removed, the roles “creditor / debtor” are recoverable, but the language itself does not strongly identify 小泥鳅 versus 刘还山.

The exchange is readable because the turns alternate cleanly.

That is different from character voice.

Another located sequence:

- “你怕他认出我。”
- “他又不是衙门里的画像师。”
- “你更怕他因为你出事。”

The speakers can be inferred from the immediately preceding situation, but the second speaker is functioning as a generic deflector and the first as a generic psychological reader.

There is little wording or conversational behavior unique to 顾承岳 / 刘还山.

### Phase363 positive comparison

In the Chu Shisan sample, 刘还山 says:

- “你回来干什么。”

楚十三 does not answer the question.

He hands over the arrow bag, changes tactical position, and says what he has noticed about the battlefield.

The speaker identity is carried by:

- refusal to accept Liu’s conversational agenda;
- combat competence;
- automatic coordination;
- the fact that his priority is the current threat, not Liu’s emotional demand.

In the Huo Jiuweng sample, “霍叔” is not answered with an explanatory line. Huo continues his physical objective. Much later he says:

- “别用他的名字拦我。”

The line belongs to him not because of a catchphrase, but because only this relationship and this grief produce that refusal.

### Result

Phase390: FAIL / weak character identity, strong turn-order dependence.  
Phase363 positive reference: materially stronger scene-integrated identity.

## 4. TEST 2 — Dialogue swap / interchangeability

The test is not “can two characters literally exchange every sentence with zero factual edits.”

It asks:

> If the proposition is preserved and only role words are adjusted, could another character plausibly say the line in the same generic AI voice?

### Phase390 high-interchangeability examples

- “又怎么了？”
- “记账。”
- “你每次都这么说。”
- “少废话。”
- “我哪天不出事？”
- “你怕他认出我。”
- “你更怕他因为你出事。”

These lines carry function more strongly than personal history.

Small changes to address terms are enough to move many of them to another bantering or perceptive character.

### Phase390 lower-interchangeability examples

Not every line fails.

For example, 刘还山 pushing 小泥鳅 away because four children are waiting has relationship-specific content.

But even there, the prose immediately explains the protective function cleanly.

Therefore the scene has some relationship specificity without having robust voice differentiation.

### Phase363 positive comparison

Important lines are harder to swap because the speech act is bound to a character-specific decision:

- Chu refuses Liu’s emotional question by giving tactical information.
- Huo refuses the use of his dead son’s name while continuing to attempt access to Gu.
- “车往前” only becomes meaningful after Huo’s physical decision has changed.

The words themselves may be simple. The ownership comes from behavior.

### Result

Phase390: FAIL / substantial proposition-level interchangeability.  
Phase363: stronger character-bound speech acts.

## 5. TEST 3 — Adjacency geometry / ping-pong completion

### Phase390 recurrent geometry

Several sequences have the same underlying machine:

A statement or question  
→ exact relevant reply  
→ follow-up  
→ exact reply  
→ small witty closure.

Examples include:

- 羊汤：想吃 / 不想吃 / 继续拆穿；
- 欠钱：欠五文 / 记账 / 每次如此 / 所以没赖账；
- fear inference: 怕认出 / deflect / 更深一层正确心理判断；
- 顾承岳 autonomy: “我不是你的犯人” followed by a clean verbal negotiation of autonomy.

The problem is not short dialogue.

The problem is adjacency precision.

Each turn appears designed to make the next turn maximally obvious and useful.

### Phase363 positive comparison

Dialogue adjacency is repeatedly broken:

- a question is not answered;
- action changes the current problem;
- listener acts before speaking;
- battle interrupts;
- character uses a different priority;
- physical coordination itself answers relationship questions.

The scene does not wait for each conversational unit to close before proceeding.

### Result

Phase390: FAIL / strong exact-adjacency ladder.  
Phase363: materially more interrupted, asymmetric conversational geometry.

## 6. TEST 4 — Author-function-per-line audit

Phase390 contains multiple lines that directly instantiate writer-packet properties.

### Direct packet-to-dialogue echoes

Writer packet:

- 刘还山“真正害怕或心里没底的时候，反而会比平时话多。”

Generated prose:

- 小泥鳅 explicitly says 刘还山“今天话真多.”

Writer packet:

- 刘还山“不愿随便把镇上的熟人拖进麻烦.”

Generated prose:

- 刘还山 explicitly orders 小泥鳅 not to run errands, carry messages or get involved.

Writer packet:

- 顾承岳“不愿被刘还山当成一件货物摆布.”

Generated prose:

- 顾承岳 explicitly states he is not Liu’s prisoner-object and that he has legs.

Writer packet:

- 顾承岳 is observant and understands Liu’s motives.

Generated prose:

- 顾承岳 performs the “deeper psychological read”: “你更怕他因为你出事。”

These are not continuity errors.

They are evidence of a generation process:

> character-card property → dialogue demonstration → reader receives proof that the property was used.

Current diagnosis label:

**DF391-01 CHARACTER-CARD-TO-DIALOGUE COMPILATION**

This is the strongest new finding.

## 7. Root-cause stack

### ROOT-1 — CHARACTER-CARD-TO-DIALOGUE COMPILATION

The writer does not merely know character facts.

It behaves as if each declarative personality property must be demonstrated on-page.

This turns background into a hidden checklist.

### ROOT-2 — EXACT ADJACENCY COMPLETION

The generator strongly prefers a cooperative conversational chain in which each line is the most relevant response to the preceding one.

This creates clean ping-pong even when the content is witty.

### ROOT-3 — VOICE AS LABEL, NOT BEHAVIOR

The packet differentiates people using labels such as:

- joking familiar hero;
- teasing street boy;
- observant proud former official.

The generated scene then gives each one the expected “flavor,” but their underlying conversational machine remains the same.

Character voice becomes tone assignment rather than different decision behavior.

### ROOT-4 — SUBTEXT EXPLICITATION

The model repeatedly turns relational subtext into correct spoken diagnosis:

- fear is named;
- protection is named;
- autonomy is named;
- old resentment is raised cleanly.

The reader is given the intended interpretation rather than having to experience it through unequal knowledge and behavior.

## 8. Why “more rich context” did not solve voice

Phase389 successfully increased lived-world material.

That helped:

- ordinary setting;
- local familiarity;
- food and money texture;
- relationship continuity.

But the same packet also included declarative personality statements.

The model treated those statements as deliverables.

Therefore:

> RICH CONTEXT is useful,
> but DECLARATIVE CHARACTER TRAITS can become dialogue-generation instructions even when no explicit writing rule is present.

This explains why Phase390 can feel more inhabited and simultaneously more mechanically authored.

## 9. What Phase363 positive evidence actually suggests

Do NOT simplify the lesson to:

- add more action;
- interrupt every dialogue;
- ban direct answers;
- require unique slang;
- make every character recognizable from one sentence.

Those would become another checklist.

The stronger difference is:

> In the positive sample, characters own different actions, priorities, refusals and permissions while speaking.

Speech is a byproduct of what each person is doing.

In Phase390, speech is often the mechanism used to demonstrate who the character supposedly is.

## 10. Next process correction

Do not write another prose candidate yet.

The next input-layer experiment should redesign writer-visible character context.

Recommended successor:

**PHASE392_FACTS_ONLY_CHARACTER_CONTEXT_REDESIGN_V1**

Its job:

- keep concrete history;
- keep relationship events;
- keep present physical/social obligations;
- keep knowledge boundaries;
- keep who owes whom and what has actually happened;
- REMOVE or quarantine easy-to-demonstrate personality labels such as:
  - “怕的时候话多”;
  - “善于观察别人”;
  - “不愿被当货物摆布”;
  - generalized “嘴贫 / 自尊强 / 不摆架子” descriptions when they can be compiled directly into dialogue.

The future writer should receive evidence from which personality may emerge, not a checklist of personality properties to prove.

Phase392 must still generate no fiction.

Only after that redesign is audited should a new fresh-blind prose test be considered.

## 11. Settlement

- Phase390 human rejection: preserved.
- Mechanical dialogue: confirmed as located actual-human failure.
- Character voice collapse: confirmed.
- Primary process hypothesis: CHARACTER-CARD-TO-DIALOGUE COMPILATION.
- Rich-context idea: not discarded, but current representation is unsafe.
- No prose repair authorized.
- No new pilot authorized in Phase391.
- Highest accepted checkpoint remains Phase320.
