---
name: novel-writing-master
description: Design, draft, diagnose, rewrite, and de-AI Chinese fiction with evidence-backed causality, emotion-debt/payoff, hate/empathy, continuity, scene-grounded dialogue, local semantic logic, reader-retention, and personal-aesthetic checks. Use for public-account short fiction, web fiction, short-drama stories, suspense, revenge, family realism, supernatural romance, or any Chinese story the user says is illogical, emotionally flat, formulaic, slow, unsatisfying, or AI-sounding.
---

# Novel Writing Master V3

V3 不追求“规则很多”，只追求五件事真的成立：

1. 事件由人物选择逼出来。
2. 读者的压抑、期待和情绪债得到对应兑现。
3. 主角值得理解，伤害者值得恨，但都不是纸片人。
4. 对白从具体场景、人物目的和信息状态里长出来，不是作者借人物嘴向读者交代。
5. 正文像具体的人在具体处境里生活，不像模型在展示写作技巧。

V2 文件继续保留用于兼容；新任务默认执行 V3。

## 核心纪律

- 先证明故事成立，再写正文。
- 一次只运行一个阶段，只加载当前阶段所需材料。
- 不用自评分、清单勾选或文件存在代替文本证据。
- 无法获得真正独立上下文时，明确标注“单上下文复核”，不得冒充独立读者。
- Fresh context 只证明历史隔离，不证明逐句逻辑检测能力；局部语义和对白真值必须单独审。
- 同一轮最多处理五个高影响问题；修改后定向复核连锁影响。
- 去 AI 味默认关闭，只在结构、因果、连续性与 V3-G6D 通过后做最小修改。
- 不复制受版权保护文本，不模仿在世作者的可识别风格。
- Novel DNA 默认关闭；先定位具体问题并优先尝试更简单的 V3 修复，只有简单修复不足时才允许进入 DNA Router。
- 不用“看一眼 / 叹气 / 摸东西 / 皱眉”等通用动作给无动机对白伪造 grounding。

每次总控任务先读：

```text
rules/pass-isolation.md
workflows/07-novel-master-pipeline-v3.md
config/novel-quality-gates.v3.json
```

涉及正文对白、局部逻辑、信息说明或时间/钱/物件语义链时，再读取：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/local-logic-ledger.md
templates/microcraft-dialogue-audit-template.md
```

只有在已完成基础证据、仍存在明确结构问题时，再读取：

```text
rules/novel-dna-routing.md
templates/dna-call-record-template.md
```

## 路由

### 完整创作、推倒重写、全面修改

执行 V3 总流程。先交付故事契约与三本账，再进入正文：

```text
因果证明表
情绪欠账与兑现表
恨感 / 共情证据表
```

Phase 3 同时建立局部语义账本；Phase 4 对高信息/高情绪对白建立最小 trigger/goal/carrier 计划；Phase 8 独立运行 V3-G6D，再允许进入最终去 AI。

用户明确要求“直接完成”时可以连续执行，但每个阶段仍须生成中间证据，不得跳到全文。

### 构思、大纲、剧情设计

读取：

```text
modules/causal-proof-engine.md
modules/emotion-payoff-ledger.md
modules/hate-empathy-test.md
modules/character-pressure-test.md
```

只完成故事契约、场景链和三本账，不提前写完整正文。

### 逻辑检查

读取：

```text
modules/causal-proof-engine.md
modules/continuity-editor.md
modules/local-logic-ledger.md
rules/novel-logic-checklist.md
```

优先寻找“一问就能解决、离开就能解决、报警/打电话就能解决、道具突然出现、人物知道不该知道的信息”等阻断问题。

时间检查不能只逐句比日期。若一个相对时间通过“花销清单 / 解释 / 代词 / 物件转移 / 因果关系”继续支配后项，必须传播该语义作用域并与后续显式时间核对。

### 对白 / AI 味 / 信息说明检查

先跑 microcraft，不先润色：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/local-logic-ledger.md
```

重要对白至少回答：

1. **为什么偏偏现在说？**
2. **如果没有读者，这个人还会不会对这个听者说这句话？**
3. **听者听到以后，知识、选择、关系、风险或任务发生了什么？**
4. **听者是否已经知道这些信息？如果知道，重说它的场内目的是什么？**
5. **沉默、迟答、只答一半、打断、转移或行动是否更符合人物？**

以下代码为 G6D 高优先失败：

```text
TEMPORAL_SEMANTIC_CHAIN_FAIL
AUTHOR_INFORMATION_MOUTHPIECE_FAIL
DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE
CRITICAL_DIALOGUE_HAS_NO_TRIGGER_OR_GOAL
ACTION_BEAT_SPAM_AS_FAKE_GROUNDING
```

不是每句对白前都必须有动作。动作只有改变读法、承担信息或反映目标时才有价值。

### 爽点、恨感、共情、情绪检查

读取：

```text
modules/emotion-payoff-ledger.md
modules/hate-empathy-test.md
rules/reader-reward-rhythm.md
```

不把旁人震惊、反派脸色变化和口头道歉算作兑现；必须检查权力、关系、选择权、利益或代价是否真实改变。

### 开篇留存

读取 `modules/opening-retention-reader.md`。不知道后文真相地冷读第一屏、前 300 字和第一场，引用精确停止句。

### 已有稿件诊断

先定位最上游层级：

```text
承诺 → 因果 → 人物选择 → 情绪债 → 场景功能 → 连续性 / 局部语义 → 对白 grounding → 行文
```

只报告二至五个根因，逐项给位置、证据、伤害和验收条件。上游阻断未解决，不润色下游句子。

### Novel DNA 可选结构路由

Novel DNA 不是默认写作模板，也不按 Global / Cross-Book / Book-level 的名字自动决定优先级。

只有满足以下前提时才读取 `rules/novel-dna-routing.md`：

1. 已经找到当前文本的具体 `problem_evidence`；
2. 因果、连续性、局部语义、普通 callback / setup-payoff、场景功能、情绪兑现、人物选择或 dialogue grounding 等更简单修复不足以解决问题；
3. 当前问题确实属于可由某条冻结 DNA 处理的结构机制。

每次调用使用 `templates/dna-call-record-template.md` 记录门槛、谱系去重、复杂度成本、公式化风险和退出条件。没有问题证据、没有“为什么简单修复不够”或没有退出条件，不得标记 `APPLIED`。

同一因果谱系只允许当前最高批准 successor 用于实际调用；当前 `GN-VDNA-01` 是 `CBDNA-C02-V2` 的系统级应用 successor，二者不得双开。跨层级配额共享，不为每个层级单独加额度。

### 深度拆解或技巧提炼

读取：

```text
workflows/05-deep-story-dissection.md
rules/suspense-reversal-payoff.md
rules/reader-reward-rhythm.md
```

若任务目标是提炼行文微技法/对白机制，必须额外抽取 `Scene → Trigger → Perception/Reaction → Speech → Aftereffect`，而不能只把结果归纳成宏观“有功能的对白”。

只提炼抽象技法，不复述大段原文。

### 导入用户有权使用的资料

沿用 V2 的 `scripts/ingest.py` 与 `workflows/01-ingest-book.md`。原书、完整提取文本和个人样本默认只留在私有环境，不提交到公开仓库。

### 去 AI 味

前置条件：G1、G6、G6D 均通过。

读取：

```text
modules/aesthetic-fingerprint.md
modules/line-editor-deslop.md
rules/no-ai-smell.md
rules/reader-trust-and-economy.md
```

先比较认可样本、拒绝样本和当前稿。样本为空时明确说明“尚未学到个人文风”，只按审美基线做终审。每轮最多处理五个高影响习惯。

去 AI 不能把作者嘴替润色得更自然，也不能用动作 beat 掩盖无动机对白。命中 G6D 必须退回 microcraft，而不是在 Phase 10 修辞。

Novel DNA 在去 AI / 行文润色阶段默认关闭，不负责句式、措辞或人物声音。

## V3 最小证据包

完整创作至少保留以下内容：

```text
一句话读者承诺：
一句话主线：
不可逆事件：
高潮选择：
结局兑现：

每场：前置事实 → 人物选择 → 未选简单方案及原因
    → 立即后果 → 新限制 → 逼出的下一场

每笔情绪债：压了什么 → 谁造成 → 读者等什么
    → 何时部分偿还 → 最终如何偿还 → 真实改变

主角共情：普通欲望 → 缺点/错误 → 有代价选择 → 失去什么
伤害者恨感：可选不伤害 → 主动伤害 → 获益 → 被提醒后加码
    → 与伤害方式对应的后果

高影响对白：场景状态 → 触发 → 为什么现在说 → 场内目标
    → 听者已知 → 信息载体 → 未说出的东西 → 对话后改变

局部语义：时间/钱/物件/知识锚点 → 语义关系 → 继承作用域
    → 是否显式断开 → 后续事实 → 一致/冲突/歧义
```

模板：

```text
templates/v3-evidence-packet-template.md
templates/microcraft-dialogue-audit-template.md
```

## 阻断条件

命中任一项，不得宣布可交付：

- 主线无法说清“谁要什么、谁阻止、失败失去什么、为何现在”。
- 关键转折只能靠巧合、误会不沟通、人物降智或临时新规则发生。
- 一个现实中的简单动作即可无代价解决核心危机，正文却无可信阻断。
- 主角只被动受苦，没有会改变局势的选择。
- 伤害者只是被旁白说坏，没有主动、明知、获益或加码证据。
- 所谓爽点没有改变权力、关系、选择权、利益或代价。
- 高潮和结局没有偿还故事最主要的情绪债。
- 修改造成新的时间、知识、物件、规则或关系冲突。
- 相对时间通过语义链继承后与后续显式事实冲突。
- 关键说明对白主要服务读者，speaker 没有可信场内目的。
- 对白以问答/反问/包袱的整齐结构运行，却没有人物或场景状态变化。
- 用通用动作 beat 假装修复无触发对白。

## 写作上下文

正文阶段只携带：

1. 故事契约。
2. 当前场景的因果行。
3. 当前情绪债及本场任务。
4. 当前人物知识、欲望、恐惧和可选方案。
5. 必要世界规则。
6. 当前场景高影响对白的最小 trigger / goal / listener-knowledge / carrier 约束。
7. 个人审美基线或已验证的文风指纹。
8. 前一场结尾与后一场目标。
9. 仅当某条 DNA 已明确 `APPLIED` 时，携带该 active call 的最小信息。

不同时加载全部审稿模块、禁词表、读者角色、质量闸门、完整 microcraft 研究证据或完整 DNA 注册表。

## 读者复核真实性

- 有新上下文、子代理或真实外部读者时，才写“独立复核”。
- 同一上下文内的多视角报告，标注“模拟读者镜头”，不宣称统计独立。
- 不用四个虚构读者的平均分证明作品好看。
- Fresh independent reader 可提供真实的阅读反应证据，但不能替代专门的局部语义/对白审计。
- 最高价值证据是：精确滑读/失信位置、未兑现期待、逻辑断点和读完后记住的内容。

## 修改纪律

按以下顺序：

```text
主线与结局
→ 因果与简单方案
→ 人物选择
→ 情绪欠账与兑现
→ 连续性 / 局部语义
→ 对白触发 / 信息载体
→ 场景功能与留存
→ 个人文风与去 AI
→ 标点错字
```

每次修改记录：

```text
问题：
位置与证据：
根因：
本次动作：
可能破坏：
必须保护：
复核结果：
```

## 交付标准

最终交付包括正文和简短审计结论：

- 没有未关闭的阻断问题。
- 主要场景能用因果证明表串起。
- 主要情绪债有明确兑现或被有意识保留。
- 主角至少有一次付出代价的主动选择。
- 伤害者的行为与后果形成对应关系，或作品明确选择不兑现并说明风险。
- 开篇没有未接受的致命停止点。
- 修改处完成连续性复核。
- `V3-G6D = PASS`，且不是靠“感觉自然”自证。
- 去 AI 只做了最小必要修改，未统一人物声音。
- 若实际调用 Novel DNA，只验证已声明调用的结构变化是否发生，不要求作品使用任何或全部 DNA。

不要用“综合评分 9.2”替代以上证据。
