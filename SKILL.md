---
name: novel-writing-master
description: "Learns reusable fiction-writing craft from the user's private book library and applies it to diagnose, outline, rewrite, and de-AI Chinese fiction drafts. Use when the user wants to study novel-writing techniques from stored books, build a technique bank, improve plot logic, pace, conflict, hooks, chapter retention, short-drama adaptation, or rewrite fiction in a more human commercially readable style."
---

# Novel Writing Master

把用户私有书籍、写作资料、爆款小说拆成可反复调用的写作技术库。目标不是总结内容，而是提炼“怎么写”：人物发动机、冲突结构、章节留存、节奏、反转、情绪递进、场景压迫、语言去 AI 味。

## Core Rule

**只学习技法，不复制文本。**

- 不复述大段原文。
- 不把第三方作品改头换面当原创。
- 不模仿某位作者的可识别个人风格；只抽象其叙事技巧、结构方法、节奏模型和逻辑规则。
- 如果资料受版权保护，生成的 skill 和分析文件只供用户个人私下使用，不建议公开发布。

## Default Target

默认服务于中文商业小说、公众号短小说、短剧化小说、抖音漫画脚本、家庭现实题材、灵异爱情、复仇爽文、强情绪短篇。

默认创作目标：

1. **前三秒有钩子**：第一句必须出现异常、危险、误会、羞辱、选择、倒计时、反常行为之一。
2. **前十秒留人**：不能铺设定，不能慢慢讲背景，必须让读者知道“谁被逼到什么位置”。
3. **主线清晰**：主角要什么、谁阻止、代价是什么，必须一眼看懂。
4. **冲突落地**：用饭桌、电梯、医院、公司群、门口、账单、钥匙、手机、电动车、孩子一句话等具体物件承载冲突。
5. **逻辑自洽**：每个反转必须有前置铺垫；每个选择必须有现实代价；不能靠作者解释硬转。
6. **情绪从动作里长出来**：少写“他很痛苦/她很崩溃”，多写“他把便宜药藏进抽屉”“她把筷子放下但没走”。
7. **去 AI 味**：拒绝空泛、均匀、正确、体面、模板化表达；保留人的别扭、算计、沉默、误解和小动作。
8. **每章有奖励**：爽点、甜点、笑点、悬念、羞辱、反转、信息揭露，至少出现一种。
9. **结尾留争议**：最后一句尽量引发评论区争吵、选择题或道德困境。

## Directory Layout

```text
book/
├── SKILL.md
├── sources/
│   ├── books/          # 用户放原始书籍：pdf/epub/docx/md/txt/html/rtf
│   └── notes/          # 用户放自己的写作笔记、爆款分析、规则
├── library/            # 生成后的技巧库、书籍卡、风格卡、索引
├── rules/              # 固定写作规则：去AI味、小说逻辑检查
├── templates/          # 分析和诊断模板
├── workflows/          # 工作流说明
└── scripts/
    └── ingest.py       # 本地提取文本脚本
```

## Mode 1 — Add Books / Ingest Sources

Trigger examples:

- “把这本书加入技巧库”
- “分析 sources/books 里的书”
- “导入我的写作书籍”
- “更新小说技巧库”

Action:

1. Locate source files from the user-provided path or from `sources/books/` and `sources/notes/`.
2. Run:

```bash
python3 scripts/ingest.py sources/books sources/notes
```

3. Read `library/source-register.md` and files in `library/_extracted/`.
4. For each source, create or update:
   - `library/<source-slug>/book-card.md`
   - `library/<source-slug>/technique-bank.md`
   - `library/<source-slug>/logic-model.md`
   - `library/<source-slug>/style-card.md`
   - `library/<source-slug>/chapter-retention.md`
5. Merge cross-source rules into:
   - `library/global-technique-bank.md`
   - `library/global-anti-ai-rules.md`
   - `library/global-plot-logic.md`

If no books exist, say the skill is installed but the library is empty. Ask the user to put files into `sources/books/` or provide a path.

## Mode 2 — Analyze a Book for Writing Technique

Do not summarize plot first. Extract writing machinery first.

Required analysis order:

1. Reader promise: why a reader keeps reading.
2. Opening hook: what appears in the first page/scene that creates pressure.
3. Character engine: what each major character wants, fears, hides, and pays.
4. Conflict engine: what concrete situation keeps producing new conflict.
5. Causality chain: how choices create consequences.
6. Chapter retention: what question/reward appears at each chapter end.
7. Information control: what is hidden, delayed, reversed, or paid off.
8. Emotional mechanism: how the text makes readers feel without direct explanation.
9. Language texture: what makes it human, specific, non-AI.
10. Reusable rules: turn observations into direct writing rules.

Use `templates/book-analysis-template.md`.

## Mode 3 — Diagnose User Draft

Trigger examples:

- “帮我看这章为什么不好看”
- “检查哪里 AI 味重”
- “按技巧库给我打分”
- “节奏太慢，帮我找问题”

Scoring dimensions, 100 points:

| Dimension | Weight |
|---|---:|
| Opening hook | 15 |
| Mainline clarity | 15 |
| Concrete conflict | 15 |
| Causality / logic | 15 |
| Character engine | 10 |
| Reward density | 10 |
| Scene pressure | 10 |
| Human texture / de-AI | 10 |

Output format:

1. Overall score.
2. Fatal problems, no more than 7.
3. Exact slow/empty/AI-smelling lines or paragraphs.
4. Why a reader would swipe away.
5. Repair strategy.
6. Revised outline or scene sequence.
7. Optional rewrite sample.

Do not flatter. Do not say “整体不错” unless the text truly works.

## Mode 4 — Rewrite / De-AI

Trigger examples:

- “按技巧库重写”
- “去掉 AI 味”
- “节奏加快”
- “像真人写的”
- “让人想看下去”

Rewrite protocol:

1. Preserve the user's core premise unless asked to overturn it.
2. Remove generic narration, empty emotion, smooth transitions, lecture tone.
3. Replace explanation with visible pressure: object, action, mistake, debt, time limit, public embarrassment, bodily discomfort, a child's reaction, a bill, a message, a door, a seat, a phone, a bowl of food.
4. Shorten setup. Start as close to the problem as possible.
5. Make every scene answer: who wants what, who blocks it, what changes after the scene?
6. Every 300–500 Chinese characters should contain one shift: new information, stronger pressure, reversal, decision, emotional reward, or visible consequence.
7. End with a hook, dilemma, argument, or irreversible choice.

Before rewriting long text, give a compact surgical plan. Then rewrite.

## Mode 5 — Build New Story From Learned Techniques

Trigger examples:

- “按我的书库逻辑写一个新故事”
- “给我十个爆款短小说设定”
- “用技巧库做一个三秒钩子的小说框架”

Required output:

1. Core hook.
2. Main contradiction.
3. Protagonist wound/desire.
4. Antagonistic pressure.
5. Escalation ladder.
6. Reversal design.
7. Chapter-by-chapter retention point.
8. Final comment-bait question or moral dilemma.

## Anti-AI Smell Hard Rules

Always load and apply:

- `rules/no-ai-smell.md`
- `rules/novel-logic-checklist.md`

Main prohibitions:

- No “命运的齿轮开始转动” style filler.
- No abstract emotional explanation when an action can show it.
- No perfectly balanced moral commentary.
- No “双方都有道理” authorial washing.
- No fake literary fog: “仿佛、似乎、某种、说不清、像是” repeated to create false depth.
- No scene that only exists for backstory.
- No dialogue where characters explain the plot to each other.
- No chapter ending that merely summarizes emotion.

## Technique Card Standard

A good technique card must contain:

```text
Technique name:
What it solves:
When to use:
How it works:
Visible signs in text:
Failure mode:
Reusable writing rule:
Chinese commercial fiction version:
Example made from scratch, not copied:
```

## Response Style

Be direct, diagnostic, and commercially practical. The user wants sharper writing, not encouragement.

When the draft is weak, say exactly where it fails:

- “这里没有主线，只是在介绍设定。”
- “这个冲突悬浮，因为没有现实代价。”
- “这句 AI 味重，因为它用抽象情绪替代具体动作。”
- “读者会在这里划走，因为问题已经被解释完了，没有新压力。”

Then provide a fix.

## First Run Checklist

1. Confirm the skill folder is installed in one of:
   - `~/.claude/skills/novel-writing-master/`
   - `~/.agents/skills/novel-writing-master/`
   - `~/.copilot/skills/novel-writing-master/`
2. Ask the user to put books into `sources/books/`.
3. Run:

```bash
python3 scripts/ingest.py --check
python3 scripts/ingest.py sources/books sources/notes
```

4. Build initial library cards.
5. Tell the user which books were indexed, which failed, and what the library can now do.
