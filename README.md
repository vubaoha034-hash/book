# Novel Writing Master V2

这是给中文小说创作准备的 Agent Skill，仓库地址：`vubaoha034-hash/book`。

V2 不再采用“一个大提示词同时负责构思、写作、审稿、逻辑和润色”的方式，而是改成：

> **总控路由 + 分阶段写作 + 独立读者反应 + 独立逻辑审查 + 最后行文精修。**

目标是解决 AI 小说最常见的问题：主线模糊、事件只用“然后”连接、人物为反转降智、规则临时补充、开头看似刺激却留不住人、节奏越改越碎、语言很顺但没有真实阅读欲望。

## V2 核心能力

### 1. 故事总控

先建立故事契约：

- 一句话读者承诺
- 一句话主线
- 主角欲望
- 持续阻力
- 失败代价
- 为什么必须现在解决
- 核心关系
- 不可逆事件
- 结局兑现

主线没有成立前，不直接扩写完整正文。

### 2. 发展性编辑

检查：

- 故事脊柱
- 结构
- 节奏
- 人物弧光
- 风险与代价
- 场景因果

不是罗列几十条问题，而是定位 2—5 个根部问题。

### 3. 开篇留存冷读

分别检查：

- 前 30—60 字
- 前 150—300 字
- 第一场戏
- 读者轻微滑读点
- 明显走神点
- 精确停止阅读句

它不会笼统说“开头不够吸引”，而是告诉你读者最可能在哪一句离开。

### 4. 独立读者面板

默认四种互补读者：

- 手机沉浸读者
- 类型承诺读者
- 人物情感读者
- 怀疑与逻辑读者

每个读者先独立阅读，最后才汇总。多人共同滑读的位置是高优先级问题；单一口味不强制修改。

### 5. 连续性与逻辑审查

检查：

- 人物事实
- 时间线
- 物件来源和状态
- 人物知识状态
- 空间和交通
- 世界规则的条件、限制和成本
- 为什么人物不用更简单办法

报告区分：确定性冲突、高风险疑点和解释缺口。

### 6. 人物压力测试

关键选择必须回答：

```text
人物现在想要什么？
害怕什么？
知道什么？
还有哪些现实方案？
最简单的方案是什么？
为什么没有使用？
当前选择付出了什么代价？
```

避免主角突然开挂、反派突然降智、关系一句道歉就恢复。

### 7. 行文精修与去 AI 味

只有结构稳定后才运行。

它采用 Pattern-first 方法：先找最反复、最伤读感的 2—4 类语言习惯，再处理典型位置，而不是把全文机械改写成统一网文腔。

重点处理：

- 过度解释
- 情绪翻译
- 意义尾巴
- 万能微动作
- 说明书式对话
- 句长单一
- 人物声音趋同
- 监控摄像头式动作清单

同时防止另一种错误：为了“快节奏”把所有句子压短、把必要心理和情绪余波全部删掉。

## 完整生产流程

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

详细流程：

```text
workflows/06-novel-master-pipeline.md
```

## 质量闸门

机器可读规则：

```text
config/novel-quality-gates.v2.json
```

人工记录模板：

```text
templates/novel-quality-gate-template.md
```

严重等级：

- `BLOCKER`：主线、动机、因果、规则或连续性无法成立。
- `MAJOR`：明显伤害节奏、情绪、可信度或结局兑现。
- `MINOR`：局部问题，不破坏整体。
- `STYLE`：语言层问题，最后处理。

**总分不能覆盖一个仍然存在的 BLOCKER。**

## 目录结构

```text
book/
├── SKILL.md
├── AGENTS.md
├── README.md
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
│   ├── books/
│   └── notes/
├── library/
└── scripts/
    └── ingest.py
```

## 深度拆书能力保留

V2 没有删除原有技巧库和深度拆书能力，仍然支持：

- 故事核与主线
- 开头钩子
- 悬疑地图
- 伏笔账本
- 反转公平度
- 读者奖励节拍
- 爽点与前置压迫
- 人物发动机
- 冲突发动机
- 事件、选择、代价和新限制构成的因果链
- 章节留存
- 去 AI 味来源

但拆文只学习抽象技法，不复制第三方文本，不模仿在世作者的可识别个人风格。

## 安装

### Codex / 通用 Agent Skills 路径

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.agents/skills/novel-writing-master
```

### Claude Code

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.claude/skills/novel-writing-master
```

### GitHub Copilot CLI

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.copilot/skills/novel-writing-master
```

## 更新

已经安装过时：

```bash
cd ~/.agents/skills/novel-writing-master
git pull
```

安装在其他目录时，进入对应目录执行 `git pull`。

## 建立个人技巧库

先检查依赖：

```bash
python3 scripts/ingest.py --check
```

把用户合法拥有或有权使用的资料放进：

```text
sources/books/
sources/notes/
```

再运行：

```bash
python3 scripts/ingest.py sources/books sources/notes
```

原书和完整提取文本默认不应公开提交。

## 推荐调用方式

### 完整创作

```text
/novel-writing-master 按总控流程完成这篇小说。先确定主线和人物选择，再写正文；完成后做开篇冷读、独立读者面板、连续性审查、发展性复审和去 AI 味，直到没有阻断级问题。
```

### 全部推倒重写

```text
/novel-writing-master 保留我指定的核心关系和结局，其余旧稿全部作为失败案例。重新建立故事契约、场景因果和人物动机，通过质量闸门后再写。
```

### 开篇检查

```text
/novel-writing-master 只做开篇留存冷读。检查前 60 字、前 300 字和第一场戏，给出精确停止句，不要直接替我改。
```

### 读者视角检查

```text
/novel-writing-master 用四个独立读者读这篇：手机沉浸、类型承诺、人物情感、逻辑怀疑。先分别锁定反应，再汇总共同划走点。
```

### 逻辑审查

```text
/novel-writing-master 检查人物知道什么、道具从哪里来、时间是否成立、规则是否有成本，以及人物为什么不用更简单办法。
```

### 发展性编辑

```text
/novel-writing-master 不要润色句子。先做发展性编辑，只找 2—5 个根部问题，按阻断级、重大级排序。
```

### 去 AI 味

```text
/novel-writing-master 在剧情和逻辑不变的前提下做最后行文精修。先找反复出现的语言习惯，最小修改，不要把所有句子改短，不要把人物声音改成一样。
```

### 深度拆书

```text
/novel-writing-master 深度拆解这篇小说：读者承诺、主线、悬疑锁钥、伏笔、反转公平度、情绪和奖励节拍、人物发动机、因果链，以及可复用动作规则。
```

## 使用原则

- 逻辑先于语言。
- 诊断先于修复。
- 读者反应与编辑判断分开。
- 写作者不能自我验收。
- 每次只加载当前阶段需要的规则。
- 快节奏不是通篇短句。
- 悬疑不是单纯扣住信息。
- 反转不能依赖前文没有的事实。
- 关系变化必须付出代价。
- 结尾优先让场景产生余波，不让作者总结主题。

## 方法来源说明

V2 参考并重新抽象了小说发展性编辑、读者反应、连续性编辑、人物压力测试和行文编辑的通行方法，也吸收了开源 Agent Skills 社区中的模块化思路。仓库内规则均针对本项目重新编写，不复制第三方 Skill 正文。

## 版权提醒

这个 Skill 用于个人学习和原创写作。不要公开提交受版权保护的原书、完整提取文本或可还原原作的大段内容。分析应聚焦抽象技法、结构和可执行规则。
