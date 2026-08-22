# 小说总控生产流程 V3

## 目标

用可定位文本证据替代自评分和假独立审稿，完成从故事设计到最终正文的闭环。

V3 同时要求三层成立：

- **宏观层**：故事契约、因果、人物选择、情绪债、连续性；
- **局部真值层 G6D**：对白触发、认知层级、信息载体、时间/钱/物件/知识语义链；
- **全文行文层 G8**：跨场景重复模式、人物声音、对白模板族密度和去 AI。

## 建议项目文件

```text
作品名/
├── 00-story-contract.md
├── 01-causal-ledger.md
├── 02-emotion-payoff-ledger.md
├── 03-hate-empathy-evidence.md
├── 04-character-and-continuity-state.md
├── 04b-local-semantic-logic-ledger.md
├── 05-scene-plan.md
├── 05b-microcraft-dialogue-plan.md
├── 06-draft.md
├── dna-call-record.md        # 仅实际进入 DNA Router 时创建
├── reviews/
│   ├── opening-cold-read.md
│   ├── reader-evidence.md
│   ├── continuity-report.md
│   ├── microcraft-dialogue-audit.md
│   └── dialogue-pattern-family-audit.md
├── revision-ledger.md
└── final.md
```

## Phase 0：锁定任务边界

记录平台、篇幅、目标读者、目标情绪、用户指定保留项、允许改变项和禁止改变项。Novel DNA 关闭，不从 DNA 模板生成题材、主角、世界观或结局。

## Phase 1：故事契约

产出：读者承诺、主线、主角普通欲望、持续阻力、失败损失、为什么必须现在、核心关系、不可逆事件、高潮选择和结局兑现。主角没有主动选择时不通过。

## Phase 2：三本账

读取：

- `modules/causal-proof-engine.md`
- `modules/emotion-payoff-ledger.md`
- `modules/hate-empathy-test.md`

完成关键场景因果链、主要情绪债、主角共情和伤害者恨感证据。出现阻断项先改大纲，不写全文。

### Optional DNA Routing Gate

只有三本账完成后、且仍存在可定位结构问题时，才允许读取：

```text
rules/novel-dna-routing.md
templates/dna-call-record-template.md
```

执行：

```text
problem_evidence
→ 更简单 V3 修复是否足够
→ DNA invocation gate
→ 同谱系去重
→ 跨层级共享配额
→ expected_change / complexity_cost / formula_risk / exit_criteria
```

没有问题证据、简单修复已足够、没有退出条件、或只是因为 DNA 来自名作/Global，都不得进入 `APPLIED`。当前 `GN-VDNA-01` 继续 DEFAULT OFF。

## Phase 3：人物、连续性与局部语义状态

读取：

- `modules/character-pressure-test.md`
- `modules/continuity-editor.md`
- `modules/local-logic-ledger.md`

记录人物知识、欲望、恐惧、错误认知、现实方案、物件、时间、空间和世界规则。

另建局部语义链：

```text
anchor_fact
anchor_time_or_state
semantic_relation
inherited_scope
scope_break
linked_item
later_explicit_fact
verdict
```

不能只记 isolated timeline；必须追踪列表、代词、花销、物件转移等跨句作用域。

## Phase 4：场景计划 + 高影响对白触发计划

每场记录：要加重/偿还哪笔债、为何发生、人物目标、冲突、选择、后果、新限制和下一场压力。

高信息、高情绪、改变关系或启动新话题的对白读取：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/dialogue-epistemic-scope.md
```

只规划最小字段：

```text
scene_state
immediate_trigger
speaker_in_scene_goal
object_fact
listener_object_fact_knowledge
public_or_reported_knowledge_if_relevant
information_carrier
non_speech_option
expected_aftereffect
```

不要给每句对白硬配动作。没有可信触发时，应删句、换载体、允许沉默/延迟/打断，或重做交流目的。

## Phase 5：分场正文

每次只携带当前场景必要上下文。写完记录新事实、知识、物件、关系、规则和未回收问题。

正文只携带最小 microcraft 指令，不加载完整审稿清单和去 AI 模块。

正文纪律：

1. 不为了交代背景，让人物向没有理由听的人完整说明；
2. 不把“人物知道 X”误写成“人物当然知道外界也知道 X”；
3. 不用通用动作 beat 冒充真人感；
4. 不为了“有趣”让不同人物持续复用同一套问答包袱机器。

注意：第 4 条在正文阶段只是写作警报，不用逐句自审把所有笑话删掉；全文密度由 G8 独立检查。

## Phase 6：开篇冷读

读取 `modules/opening-retention-reader.md`，只检查第一屏、前 300 字和第一场的滑读、困惑、失信和停止位置。

## Phase 7：读者证据

读取 `modules/beta-reader-panel.md`。新上下文/子代理/真人才能标独立读者；同一上下文多镜头只能标模拟读者镜头。

Fresh context 只代表历史隔离，不代表逐句真值能力。局部语义和对白必须另跑 G6D。

## Phase 8：逻辑、连续性、局部对白与兑现复核

先核因果、简单方案、情绪债、人物代价、伤害者后果、知识/时间/空间/物件/规则。

然后独立运行 **V3-G6D V1.4**，只读取：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/dialogue-epistemic-scope.md
modules/local-logic-ledger.md
templates/microcraft-dialogue-audit-template.md
```

### G6D 执行顺序

1. 全文 candidate harvest；
2. rhetorical ladder ATS parity；
3. deterministic local semantic chain；
4. dialogue trigger / speaker goal；
5. **epistemic scope**；
6. exact-bundle / information carrier；
7. social anecdote carveout；
8. local-vs-G8 pattern routing。

### Epistemic scope

必须区分：

```text
OBJECT_FACT
LISTENER_KNOWS_OBJECT_FACT
PUBLIC_KNOWLEDGE_OF_OBJECT_FACT
REPORTED_RUMOR_CONTENT
EVIDENCE_OF_EXPOSURE_OR_SPREAD
ACTIONABLE_RISK_FROM_PUBLIC_KNOWLEDGE
```

`listener knows X` 不等于 `listener knows outsiders know X`。

如果重复 X 是为了明确“外面正在怎么传 X”或说明曝光风险，它可能是新的 meta-information。没有证据支持“外界已知”时 HOLD；双方共享背景且没有任何新场内/认知 payload 时仍可 `AUTHOR_INFORMATION_MOUTHPIECE_FAIL`。

### Calibrated anti-template

每个 harvested rhetorical ladder 仍要 ATS 记录，但**单个 locally plausible/removable joke 不因可删就自动成为 G6D blocker**。

只有本场独立失真时才硬 FAIL，例如：关键事实被空转拖住、无任何文本支持的目标/关系压力、纯为制造下一问而造假前提。

局部成立但可移植/通用的节拍，标记 `g8_pattern_family_candidate=true`，交给 Phase 10。

### G6D 硬门禁仍包括

```text
TEMPORAL_SEMANTIC_CHAIN_FAIL
pure shared-background AUTHOR_INFORMATION_MOUTHPIECE_FAIL
CRITICAL_DIALOGUE_HAS_NO_TRIGGER_OR_GOAL
locally ungrounded material dialogue pingpong
ACTION_BEAT_SPAM_AS_FAKE_GROUNDING
```

若存在 `APPLIED` DNA call，只验证其声明的 expected_change、复杂度、公式风险和 exit criteria。

## Phase 9：定向修改

一次最多开放五个高影响问题。顺序：

```text
主线/结局
→ 因果/简单方案
→ 人物选择
→ 情绪兑现
→ 连续性/局部语义
→ 对白触发/信息载体
→ 留存与场景功能
```

G6D 修复优先：确定语义冲突 → 纯嘴替/关键 grounding → 真实信息载体 → non-speech → 最后措辞。

不要在这一阶段因为 G8 可移植性怀疑就批量重写对白。

## Phase 10：个人审美与去 AI（G8）

只有 G1、G6、G6D 通过且场景顺序稳定后，读取：

```text
modules/aesthetic-fingerprint.md
modules/line-editor-deslop.md
rules/no-ai-smell.md
modules/dialogue-pattern-family-density.md
templates/dialogue-pattern-family-audit-template.md
```

### Dialogue Pattern Family Ledger

收集全文跨场景的可疑 cadence family，而不是逐句判“像 AI”。记录每个实例的：

```text
location
speakers / relationship
scene_task
cadence_skeleton
current object/task anchor
shared history/status anchor
independent local goal
portability
local G6D verdict
```

再按 family 比较：

- 是否出现在分离场景；
- 是否跨不同 speaker pair / relationship；
- cadence / reveal timing 是否同质；
- 是否缺乏人物/场景特异性；
- 是否可以在无关人物间平移；
- 是否造成多个人物“同一个模型声音”。

风险码：

`DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK`

**不冻结统一数字阈值。** 当前三书 purposive 证据不足以支持“出现 N 次就失败”。

幽默多本身不是风险；同一人物的固定习惯、running joke、依赖具体物件/旧账的关系笑话可 PASS/HOLD。

处理 family 时保留最具体、最属于人物的实例，优先删/改最通用重复实例，并对改动位置重新跑局部 G6D。

Novel DNA 在本阶段关闭，不控制句式、措辞和人物声音。

## Phase 11：最终复核

必须确认：

- 没有开放 blocker；
- 开篇问题与结局回答属于同一故事；
- 高潮由选择和代价逼出；
- 情绪债得到真实偿还或记录为有意风险；
- 修改未产生连锁冲突；
- `V3-G6D = PASS` 且完成 epistemic-scope 审计；
- 没有已知 deterministic semantic conflict；
- G8 已完成 dialogue pattern-family ledger；
- 高影响 `DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK` 已处理或明确保留理由；
- 去 AI 没有改变事实、抹平人物声音或删掉必要余波；
- 所有保留的 DNA 调用达到退出条件且无同谱系双计数。

最终不需要虚假的高分。交付正文，并简短说明关闭的问题和有意保留的风险。
