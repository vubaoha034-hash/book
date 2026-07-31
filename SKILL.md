---
name: novel-writing-master
description: Design, draft, diagnose, rewrite, and de-AI Chinese fiction with evidence-backed causality, emotion-debt/payoff, hate/empathy, continuity, reader-retention, and personal-aesthetic checks. Use for public-account short fiction, web fiction, short-drama stories, suspense, revenge, family realism, supernatural romance, or any Chinese story the user says is illogical, emotionally flat, formulaic, slow, unsatisfying, or AI-sounding.
---

# Novel Writing Master V3

V3 不追求“规则很多”，只追求四件事真的成立：

1. 事件由人物选择逼出来。
2. 读者的压抑、期待和情绪债得到对应兑现。
3. 主角值得理解，伤害者值得恨，但都不是纸片人。
4. 正文像具体的人在具体处境里生活，不像模型在展示写作技巧。

V2 文件继续保留用于兼容；新任务默认执行 V3。

## 核心纪律

- 先证明故事成立，再写正文。
- 一次只运行一个阶段，只加载当前阶段所需材料。
- 不用自评分、清单勾选或文件存在代替文本证据。
- 无法获得真正独立上下文时，明确标注“单上下文复核”，不得冒充独立读者。
- 同一轮最多处理五个高影响问题；修改后定向复核连锁影响。
- 去 AI 味默认关闭，只在结构、因果和情绪通过后做最小修改。
- 不复制受版权保护文本，不模仿在世作者的可识别风格。

每次总控任务先读：

```text
rules/pass-isolation.md
workflows/07-novel-master-pipeline-v3.md
config/novel-quality-gates.v3.json
```

## 路由

### 完整创作、推倒重写、全面修改

执行 V3 总流程。先交付故事契约与三本账，再进入正文：

```text
因果证明表
情绪欠账与兑现表
恨感 / 共情证据表
```

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
rules/novel-logic-checklist.md
```

优先寻找“一问就能解决、离开就能解决、报警/打电话就能解决、道具突然出现、人物知道不该知道的信息”等阻断问题。

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
承诺 → 因果 → 人物选择 → 情绪债 → 场景功能 → 连续性 → 行文
```

只报告二至五个根因，逐项给位置、证据、伤害和验收条件。上游阻断未解决，不润色下游句子。

### 深度拆解或技巧提炼

读取：

```text
workflows/05-deep-story-dissection.md
rules/suspense-reversal-payoff.md
rules/reader-reward-rhythm.md
```

拆解读者承诺、因果链、悬疑锁钥、伏笔、反转公平度、情绪债、人物选择和兑现。只提炼抽象技法，不复述大段原文。

### 导入用户有权使用的资料

沿用 V2 的 `scripts/ingest.py` 与 `workflows/01-ingest-book.md`。原书、完整提取文本和个人样本默认只留在私有环境，不提交到公开仓库。

### 去 AI 味

读取：

```text
modules/aesthetic-fingerprint.md
modules/line-editor-deslop.md
rules/no-ai-smell.md
rules/reader-trust-and-economy.md
```

先比较认可样本、拒绝样本和当前稿。样本为空时明确说明“尚未学到个人文风”，只按审美基线做终审。每轮最多处理五个高影响习惯。

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
```

模板：`templates/v3-evidence-packet-template.md`

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

## 写作上下文

正文阶段只携带：

1. 故事契约。
2. 当前场景的因果行。
3. 当前情绪债及本场任务。
4. 当前人物知识、欲望、恐惧和可选方案。
5. 必要世界规则。
6. 个人审美基线或已验证的文风指纹。
7. 前一场结尾与后一场目标。

不同时加载全部审稿模块、禁词表、读者角色和质量闸门。

## 读者复核真实性

- 有新上下文、子代理或真实外部读者时，才写“独立复核”。
- 同一上下文内的多视角报告，标注“模拟读者镜头”，不宣称统计独立。
- 不用四个虚构读者的平均分证明作品好看。
- 最高价值证据是：精确滑读/失信位置、未兑现期待、逻辑断点和读完后记住的内容。

## 修改纪律

按以下顺序：

```text
主线与结局
→ 因果与简单方案
→ 人物选择
→ 情绪欠账与兑现
→ 连续性和世界规则
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
- 去 AI 只做了最小必要修改，未统一人物声音。

不要用“综合评分 9.2”替代以上证据。
