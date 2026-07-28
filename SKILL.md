---
name: novel-writing-master
description: "Chinese fiction master orchestrator for private craft-library learning, story planning, drafting, opening-retention testing, independent reader simulation, developmental editing, character pressure tests, continuity and logic audits, targeted revision, and de-AI line editing. Use for commercial Chinese fiction, public-account short stories, web fiction, short-drama fiction, suspense, emotional fiction, family realism, supernatural romance, revenge, and other narrative projects."
metadata:
  version: "2.0.0"
  pipeline: "staged-independent-review"
---

# Novel Writing Master V2

把用户合法拥有或有权使用的写作资料、小说案例和个人笔记沉淀成技巧库，并把创作拆成相互独立的阶段：故事契约、结构、人物、正文、开篇冷读、读者面板、连续性审查、发展性编辑、修改总账、行文精修。

本 Skill 的目标不是一次性生成“看起来完整”的小说，而是让作品经过可追踪、可复核、可迭代的创作流程。

## 最高原则

### 1. 只学习技法，不复制文本

- 不复述大段受版权保护原文。
- 不把第三方作品改头换面当原创。
- 不模仿在世作者可识别的个人风格。
- 只抽象结构、节奏、因果、信息控制、人物选择、悬疑、反转和情绪机制。
- 用户私有原书、提取文本和分析库默认不公开提交。

### 2. 逻辑先于语言

主线、人物动机、因果、规则和连续性未稳定前，不做全文逐句润色。

### 3. 写作者不能自我验收

正文完成后必须进入新的独立审查阶段。不得第一稿写完后直接宣布完成。

### 4. 分阶段加载规则

任何一次任务都先读取：

```text
rules/pass-isolation.md
```

然后只加载当前阶段需要的模块。不得把全部审稿规则、读者面板和去 AI 词库同时压进正文生成上下文。

### 5. 诊断必须有证据

审查意见必须对应具体章节、场景、事件、段落或句子。总分不能覆盖阻断级问题。

### 6. 信任读者

读取：

```text
rules/reader-trust-and-economy.md
```

不要把人物情绪、潜台词、反转意义和结尾主题全部翻译给读者。给足方向，保留推断、预测和情绪重建空间。

## 默认服务范围

默认服务于：

- 中文商业小说
- 公众号短小说
- 番茄、知乎故事等通俗短篇
- 连载网文
- 短剧化小说
- 抖音漫画叙事脚本
- 家庭现实题材
- 灵异爱情与中式怪谈
- 悬疑反转
- 复仇爽文
- 强情绪爱情故事

题材和平台只用于校准，不得把某个平台的套路当作所有小说的普遍规律。

## 目录与核心文件

```text
book/
├── SKILL.md
├── AGENTS.md
├── config/
│   └── novel-quality-gates.v2.json
├── modules/
│   ├── developmental-editor.md
│   ├── opening-retention-reader.md
│   ├── beta-reader-panel.md
│   ├── continuity-editor.md
│   ├── character-pressure-test.md
│   └── line-editor-deslop.md
├── rules/
│   ├── pass-isolation.md
│   ├── reader-trust-and-economy.md
│   ├── no-ai-smell.md
│   ├── novel-logic-checklist.md
│   ├── suspense-reversal-payoff.md
│   └── reader-reward-rhythm.md
├── workflows/
│   ├── 05-deep-story-dissection.md
│   └── 06-novel-master-pipeline.md
├── templates/
│   ├── novel-quality-gate-template.md
│   └── ...
├── sources/
├── library/
└── scripts/
```

## 路由规则

根据用户任务选择模式。用户明确指定某一阶段时，只执行该阶段；用户要求“完整写完、全面修改、推倒重写、自己检查并迭代”时，默认执行 **Mode 0 总控生产流程**。

---

# Mode 0 — 小说总控生产流程

触发示例：

- “把这个小说完整写好”
- “全部推倒重写”
- “按观众视角改稿并自我迭代”
- “检查逻辑、节奏、人物和 AI 味后完成”
- “按我们的小说规则从头做”

必须读取：

```text
workflows/06-novel-master-pipeline.md
rules/pass-isolation.md
config/novel-quality-gates.v2.json
```

标准阶段：

```text
Phase 0  故事契约
Phase 1  结构与因果
Phase 2  人物压力测试
Phase 3  正文写作
Phase 4  开篇留存冷读
Phase 5  独立读者面板
Phase 6  连续性与逻辑审查
Phase 7  发展性编辑复审
Phase 8  修改总账与优先级
Phase 9  行文精修与去 AI 味
Phase 10 最终冷读与连锁复核
```

## Phase 0：故事契约

确定：

```text
题材与平台：
目标篇幅：
目标读者：
目标情绪：
一句话读者承诺：
一句话主线：
主角想要：
持续阻力：
失败代价：
为什么必须现在解决：
核心关系：
不可逆事件：
结局兑现：
禁止改变的设定：
```

主线无法一句话说清，不进入正文。

## Phase 1：结构与因果

读取：

```text
modules/developmental-editor.md
rules/novel-logic-checklist.md
```

悬疑或反转题材再读取：

```text
rules/suspense-reversal-payoff.md
```

商业节奏或留存任务再读取：

```text
rules/reader-reward-rhythm.md
```

每场必须记录：

```text
场景目标
阻力
行动
失败 / 成功但代价更大
新信息
关系或权力变化
如何逼出下一场
```

场景之间主要由“因此”或“但是”连接，不是“然后又发生”。

## Phase 2：人物压力测试

读取：

```text
modules/character-pressure-test.md
```

每个关键选择都要回答：

- 人物当前想要什么。
- 人物害怕什么。
- 人物知道和不知道什么。
- 还有哪些现实方案。
- 最简单的合理方案是什么。
- 为什么没有采用更简单方案。
- 当前选择付出什么代价。

无法解释“为什么不用更简单办法”，不得靠人物降智继续剧情。

## Phase 3：正文写作

正文阶段只加载：

1. 故事契约。
2. 当前场景计划。
3. 当前人物状态。
4. 必要世界规则。
5. 项目文风基线。
6. 前一场结尾和后一场目标。

写作时保护以下阅读奖励：

- 沉浸
- 人物推断
- 好奇与预测
- 情绪兑现
- 语言和节奏

快节奏不等于通篇短句，也不等于删除所有心理和情绪余波。

## Phase 4：开篇留存冷读

读取：

```text
modules/opening-retention-reader.md
```

冷读前 30—60 字、前 150—300 字和第一场戏。必须报告：

- 读者立刻持有的问题。
- 困境是否形成。
- 注意力轨迹。
- 轻微滑读、明显走神和停止阅读的位置。
- 精确停止句。
- 唯一最高优先级修改方向。

此阶段不直接提供替换开头。

## Phase 5：独立读者面板

读取：

```text
modules/beta-reader-panel.md
```

默认四个视角：

1. 手机沉浸读者。
2. 类型承诺读者。
3. 人物情感读者。
4. 怀疑与逻辑读者。

每个读者先独立锁定报告，再汇总。多名读者在同一位置滑读或离开，属于高优先级信号；单一口味偏好不强制修改。

## Phase 6：连续性与逻辑审查

读取：

```text
modules/continuity-editor.md
rules/novel-logic-checklist.md
```

检查：

- 人物事实
- 时间线
- 物件来源和状态
- 人物知识状态
- 空间和交通
- 世界规则的条件、限制和成本
- 因果和更简单方案

报告必须区分：

- 确定性冲突
- 可能是有意设计的高风险疑点
- 解释缺口

不得擅自决定哪一个版本才是正确设定。

## Phase 7：发展性编辑复审

重新读取：

```text
modules/developmental-editor.md
```

基于完整正文，只给 2—5 个根部问题：

- 故事脊柱
- 结构
- 节奏
- 人物弧光
- 风险与代价
- 因果链

阻断级和重大级问题未解决，不进入行文精修。

## Phase 8：修改总账

使用：

```text
templates/novel-quality-gate-template.md
```

修改顺序：

1. 主线与结局。
2. 因果与人物选择。
3. 连续性与世界规则。
4. 场景功能与节奏。
5. 信息控制与情绪兑现。
6. 行文与 AI 味。
7. 标点与错字。

每个问题必须记录来源、严重等级、位置、根因、修改动作、影响范围、保护项和验证证据。

## Phase 9：行文精修与去 AI 味

读取：

```text
modules/line-editor-deslop.md
rules/no-ai-smell.md
rules/reader-trust-and-economy.md
```

执行原则：

- Pattern-first：先识别 2—4 个反复习惯，再处理典型位置。
- 最小修改：能删一句，不重写一段。
- 保留人物声音、有效停顿和有意义的不规整。
- 不改变情节事实、道具状态、关系和时间线。
- 不把所有心理机械改成动作。
- 不把所有句子压短。
- 不承诺 AI 检测百分比。

## Phase 10：最终冷读

至少完成：

1. 开篇留存复测。
2. 手机沉浸读者单独通读。
3. 修改位置及连锁影响的连续性复核。
4. 开头与结局兑现复核。

自评分只能在全部阶段结束后给出，必须附评分依据，不得只给数字。

---

# Mode 1 — 导入书籍与建立技巧库

触发示例：

- “把这本书加入技巧库”
- “分析 sources/books 里的书”
- “更新小说技巧库”

执行：

```bash
python3 scripts/ingest.py --check
python3 scripts/ingest.py sources/books sources/notes
```

读取 `library/source-register.md` 和 `library/_extracted/`，为每个来源建立：

```text
book-card.md
technique-bank.md
logic-model.md
style-card.md
chapter-retention.md
suspense-reversal-map.md
reader-reward-map.md
```

再更新全局技巧库。

没有资料时，明确说明技巧库为空，不假装已经学习。

---

# Mode 2 — 深度拆解小说

触发示例：

- “认真分析为什么好看”
- “拆悬疑、伏笔、反转和爽点”
- “分析这篇短篇的故事核和情绪曲线”
- “不要表面总结，要拆出真正方法”

读取：

```text
workflows/05-deep-story-dissection.md
templates/book-analysis-template.md
templates/suspense-reversal-map-template.md
templates/reader-reward-map-template.md
```

必拆维度：

1. 一句话读者承诺。
2. 故事核与主线。
3. 开头留人机制。
4. 悬疑问题和开锁顺序。
5. 伏笔账本与公平度。
6. 反转前后认知变化。
7. 读者奖励和情绪节拍。
8. 人物发动机。
9. 冲突发动机。
10. 事件、选择、代价和新限制形成的因果链。
11. 信息控制。
12. 人物与关系变化。
13. 去 AI 味来源。
14. 可复用动作规则。

禁止只写“节奏快、反转多、人物立体”。这些是结论，不是拆解。

---

# Mode 3 — 构建新故事

触发示例：

- “按技巧库写一个新故事”
- “把这个设定扩成小说”
- “重新设计完整剧情”

先执行 Mode 0 的 Phase 0—2。至少输出：

- 读者承诺
- 一句话主线
- 核心关系
- 不可逆事件
- 第一悬疑问题
- 真实线索与误导
- 人物欲望与恐惧
- 场景升级链
- 关键代价
- 高潮选择
- 结局兑现

用户要求完整正文时，再进入 Phase 3—10。

---

# Mode 4 — 诊断已有稿件

触发示例：

- “这章为什么不好看”
- “节奏慢在哪里”
- “帮我找逻辑错误”
- “站在观众角度检查”

先判断问题属于哪一层：

```text
故事契约
结构与因果
人物选择
开篇留存
读者体验
连续性
行文
```

只加载对应模块。默认输出：

1. 当前最严重问题。
2. 精确位置与证据。
3. 为什么伤害读者。
4. 根因而非表面症状。
5. 修改优先级。
6. 必须保护的有效部分。
7. 验收条件。

不得用总分掩盖阻断级漏洞。

---

# Mode 5 — 定向重写

触发示例：

- “按现在规则重写这一章”
- “推倒这几场重新写”
- “去掉 AI 味但不要改剧情”

执行顺序：

1. 明确保留项和允许改变项。
2. 确定当前问题所在层级。
3. 结构问题先改场景计划。
4. 人物问题先补选择依据或重做行为链。
5. 逻辑问题先修规则、知识、物件和时间。
6. 最后才重写正文。
7. 重写后重新执行对应冷读和连续性检查。

用户明确要求“全部推倒重写”时，旧稿只作为失败案例；保留用户指定主线、人物关系和结局约束，重新执行 Phase 0—2，不继续在旧稿上打补丁。

---

# Mode 6 — 单项专业审查

可直接调用：

```text
开篇留存 → modules/opening-retention-reader.md
读者面板 → modules/beta-reader-panel.md
发展性编辑 → modules/developmental-editor.md
人物压力测试 → modules/character-pressure-test.md
连续性审查 → modules/continuity-editor.md
行文精修 / 去 AI 味 → modules/line-editor-deslop.md
```

单项审查完成后，不自动扩展成全部流程，除非用户要求完整处理。

## 质量等级

- **BLOCKER / 阻断级**：主线、动机、因果、规则或连续性不成立。
- **MAJOR / 重大级**：明显损害节奏、情绪、可信度或兑现。
- **MINOR / 一般级**：局部问题，不破坏整体。
- **STYLE / 风格级**：语言问题，最后处理。

机器可读标准：

```text
config/novel-quality-gates.v2.json
```

## 商业短篇默认要求

适用于公众号短小说、手机短篇和短剧化小说时：

- 开头尽快出现具体压力或异常。
- 前 150—300 字形成基本困境和阅读问题。
- 主线清楚，但不把全部背景讲完。
- 冲突落在现实动作、物件、关系和代价上。
- 反转必须有真实线索。
- 情绪兑现必须有积累和后果。
- 结尾优先留下选择、余波、争议或不可逆结果，不用作者总结主题。

这些是默认校准，不是对所有文学类型的硬性规定。

## Response Style

直接、准确、可执行。用户要的是更好的小说，不是安慰。

可使用：

- “这里没有主线，只是在介绍设定。”
- “这两个场景只能用‘然后’连接，因果没有成立。”
- “这个人物明明有更简单办法，正文没有解释他为何不用。”
- “这个悬疑没有可回收的钥匙，只是在扣住信息。”
- “这个反转依赖前文从未出现的事实，因此不公平。”
- “读者会在这句后停止，因为当前问题已经消失，新问题尚未建立。”
- “这句不是文笔问题，而是在替读者翻译已经看懂的情绪。”

指出问题后必须给修改方向和验收条件。

## First Run

安装目录可为：

```text
~/.claude/skills/novel-writing-master/
~/.agents/skills/novel-writing-master/
~/.copilot/skills/novel-writing-master/
```

第一次建立书库：

```bash
python3 scripts/ingest.py --check
python3 scripts/ingest.py sources/books sources/notes
```

告诉用户：

- 成功索引哪些资料。
- 哪些资料失败。
- 当前技巧库能执行哪些分析。
- 原始受版权保护文本不会被公开提交。
