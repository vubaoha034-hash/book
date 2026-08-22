# 分阶段独立审查规则

## 目的

小说写作不能把构思、写作、审稿、逻辑检查、读者反馈、对白微观逻辑和润色同时塞进一个提示词。每个阶段只承担一种职责，并输出可核查证据。

## 总原则

1. **逻辑先于语言。**
2. **诊断先于修复。**
3. **读者反应与编辑判断分开。**
4. **写作者不得自我验收。**
5. **每次只加载当前阶段需要的规则。**
6. **证据优先，所有结论必须定位。**
7. **根因优先，不平铺几十条表面修改。**
8. **Fresh context 不是万能审稿器。**
9. **G6D 候选收集与判定分开。**
10. **保护生活感：闲聊、趣闻、共同记忆不是天然错误。**
11. **候选被列出不等于审完：所有修辞梯子必须有独立 ATS。**
12. **认知层级先于嘴替判断：知道事实 X，不等于知道外界也知道 X。**
13. **局部真值与全文 AI 模板密度分层：G6D 审“这里成不成立”，G8 审“这种语言机器是不是到处重复”。**

## 标准阶段

### A. 故事契约

只确定读者承诺、主线、主角欲望、持续阻力、失败代价、为什么现在、核心关系、不可逆事件、高潮选择和结局兑现。禁止写完整正文。

### B. 结构设计

只检查场景目标、冲突升级、转折、因果、人物弧光、高潮与结局。禁止处理修辞和 AI 味。

### C. 人物压力测试

只检查人物知道什么、想要什么、害怕/隐瞒什么、为何选择、是否存在更简单方案。禁止为保剧情让人物降智。

### D. 正文写作

只加载故事契约、当前场景任务、人物状态、必要设定、高影响对白的最小 trigger / goal / listener-knowledge / information-carrier 约束和文风基线。不得同时加载完整审稿清单和去 AI 词库。

### E. 开篇留存测试

只报告第一屏、前 300 字和第一场的注意力、困惑、失信和停止位置，不替作者重写。

### F. 读者面板

不同视角先独立阅读再汇总。同一上下文多角色只能称模拟读者镜头，不能冒充独立读者。

### G. 连续性审查

只检查事实、时间、物件、空间、知识状态、规则和因果冲突。相对时间还必须沿列表、解释、代词、花销和物件转移传播作用域。

### H. 对白 grounding 与局部语义审查（V3-G6D V1.4）

只读取：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/dialogue-epistemic-scope.md
modules/local-logic-ledger.md
templates/microcraft-dialogue-audit-template.md
```

#### H1 — 候选收集

先扫描全文，建立完整候选清单。必须收集：

- 3 个以上独立事实的信息包；
- 当前事件 / 时间 / 听者角色 / 奖励 / 传闻 / 外来者数量等公共背景包；
- 对听者本人任务/身份的重复说明；
- `问 → 反问/机灵回答 → 追问 → 包袱` 等修辞梯子；
- 普通前中段承担设定交代的新话题；
- 第一手趣闻/闲聊；
- “谁知道什么、别人是否已经知道、传闻说了什么、暴露后风险怎样变化”的认知层级候选。

PRE_DELIVERY / REGRESSION 不得只抽样这些候选。

#### H2 — 认知层级先于嘴替判断

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

如果对白重复 X，是为了告诉听者“外面正在怎么传 X / 谁已经知道 X / 因此来了什么人、风险如何改变”，这可能是新的 meta-information，不能只因 X 本身已知就判嘴替。

但 public/exposure claim 必须有消息、来人、环境变化、目击、记录等场内证据；没有证据时 HOLD，不能替文本脑补。

只有以下条件同时成立，才使用 `AUTHOR_INFORMATION_MOUTHPIECE_FAIL`：

- object facts 双方已经知道；
- 没有新的 public/reported knowledge 或 exposure/risk payload；
- 没有 accusation、reframing、negotiation、teaching、misunderstanding、relationship/task purpose；
- 真正主要受益者只有读者。

有真实 epistemic payload、但说得过于完整/啰嗦，优先送到 G8 的 economy/naturalness 层，而不是伪造 G6D 硬错误。

#### H3 — 社交趣闻保护

第一手趣闻、闲聊、共同回忆可以因为关系、声音、尴尬、怀念、嘲弄等成立，不要求每个事实都改变任务状态。禁止把“更短也能回答”自动等同于“不自然”。

#### H4 — 修辞梯子强制逐轮记录

必须满足：

```text
rhetorical_ladder_candidate_count == anti_template_record_count
```

每个 ATS 检查逐轮 state delta、speaker goal 证据、自我撤销命题、诱导追问、删除测试、可移植性、关系/任务特异性和 bluff/deflection 证据。

但这些是**诊断信号，不是单句自动 FAIL 开关**。

一个局部合理、非关键、受恐惧/关系/地位/尴尬等场内压力支撑的笑话，即使可删短，也可以 PASS/HOLD G6D。

只有对白在本场独立失真时才用 `DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`，例如：

- 没有任何文本支持的目标/关系压力；
- 关键事实被空转回合故意拖住；
- 纯为制造下一问而构造假前提；
- 除通用包袱节拍外没有本场价值。

如果局部成立但很“通用、可移植”，标记 `g8_pattern_family_candidate=true`，交给 G8 判断全文是否反复出现同一语言机器。

#### H5 — 局部语义硬门禁

`TEMPORAL_SEMANTIC_CHAIN_FAIL`、确定知识冲突、关键对白无 trigger/goal、纯 reader-only shared background、action-beat 假 grounding 仍是 G6D 硬问题。

此阶段禁止：顺手全文润色、每句加动作、因为“像角色会说”而脑补动机、因为一条可删玩笑就宣布 AI 模板硬失败。

### I. 发展性编辑

重新从全局检查主线、结构、节奏、人物弧光、风险和因果，只提出 2—5 个根部问题。

### J. 修改排序

固定顺序：

```text
主线/结局
→ 因果/简单方案
→ 人物选择
→ 情绪兑现
→ 连续性/局部语义
→ 对白触发/信息载体
→ 语言/节奏/AI味
→ 标点错字
```

### K. 行文精修与 G8 去 AI

只有结构、连续性和 G6D 通过后，才读取：

```text
modules/aesthetic-fingerprint.md
modules/line-editor-deslop.md
rules/no-ai-smell.md
modules/dialogue-pattern-family-density.md
templates/dialogue-pattern-family-audit-template.md
```

G8 新增全文级 **Dialogue Pattern Family Ledger**。目标不是逐句猎杀笑话，而是检查：

- 相隔很远的场景是否反复出现同一种 cadence skeleton；
- 不同人物/关系是否都被同一种问答机器覆盖；
- 笑点是否高度可移植，几乎不依赖当前物件、任务、旧账和身份；
- 同一模式的 reveal timing、句长和应答策略是否过度一致；
- 多个人物是否因此听起来像同一个模型。

风险码：

`DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK`

当前证据**不允许冻结统一数字阈值**。不能规定“出现 N 次就失败”。必须根据跨场景、跨人物、低特异性、可移植性和机制重复的综合证据判断。

同一个人物有明确语言习惯、固定 ritual 或关系 running joke 时可以 PASS/HOLD；幽默多本身不是 AI 味证据。

修改只处理最伤读感的 2—5 个重复模式，保留最具体、最属于人物的实例，删/改最通用的重复实例，然后复核改动位置的 G6D。

## 独立性要求

读者、连续性、G6D、发展性编辑和 G8 不互相冒充。Fresh context 只证明隔离，不证明检测能力。最终汇总者不得反向美化已锁定报告。

## 禁止事项

- 禁止第一稿后直接宣布完成。
- 禁止用总分替代证据。
- 禁止把平台套路当普遍文学规律。
- 禁止为了快节奏删光心理和余波。
- 禁止“对白前加动作 = Scene-to-Speech”。
- 禁止“听者不需要每个细节 = 趣闻不自然”。
- 禁止候选入表却不审。
- 禁止把 object fact 与 public knowledge 混为一层。
- 禁止把单个可删笑话自动升级成 G6D blocker。
- 禁止用当前 purposive 三书样本冻结统一模板密度阈值。

## 最终通过标准

- 主线、因果、人物选择成立。
- 没有确定性连续性/局部语义冲突。
- G6D candidate inventory 与 ATS parity 完整。
- 关键 public-background 对白完成 epistemic-scope 审计。
- 纯 shared-background mouthpiece 已关闭。
- 合法社交趣闻未被误杀。
- 局部关键对白没有独立 grounding 失败。
- G8 已完成跨场景 dialogue pattern-family 检查，并处理高影响重复模板族。
- 独立读者与结构审查均完成。
- 最后才完成语言精修。
