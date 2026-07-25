# Novel Writing Master Skill

这是一个给中文小说创作准备的 Agent Skill。目标不是“总结书”，而是把你的写作书籍、小说案例、写作笔记沉淀成一个可反复调用的写作技巧库。

它现在升级为 **深度拆书系统**：不仅看主线、节奏、AI 味，还要拆出悬疑在哪里、伏笔怎么埋、最后怎么开锁、反转是否公平、爽点在哪里、读者多久获得一次奖励。

## 核心效果

- 导入你自己的写作书、小说案例、爆款分析、写作笔记。
- 提炼可复用技巧：开头钩子、人物发动机、冲突递进、悬疑锁钥、伏笔回收、反转、爽点节拍、章节留存、情绪机制。
- 建立长期技巧库：每本资料一个分析卡，全局一个方法库。
- 帮你诊断小说：主线是否清晰、冲突是否落地、节奏是否拖、悬疑是否有钥匙、反转是否作弊、爽点是否有效、逻辑是否断、AI味是否重。
- 帮你重写：更像真人写，更有现实摩擦，更有商业阅读感。

## 新增深度分析维度

### 1. 悬疑地图

必须拆：

```text
第一个悬疑在哪里出现？
读者第一个问题是什么？
作者给了哪些真线索？
给了哪些误导？
什么时候第一次开锁？
开锁后是否打开更大的锁？
最终真相回收了哪些细节？
```

### 2. 伏笔账本

```text
伏笔 / 表层意义 / 真实意义 / 回收位置 / 是否公平
```

### 3. 反转账本

```text
反转前读者以为：
反转后读者发现：
它改变了什么：理解 / 选择 / 代价 / 权力 / 情绪
是否有提前铺垫：
是否带来新压力：
```

### 4. 爽点和读者奖励节拍

```text
多少字/多少场出现一个小奖励？
多少字/多少场出现一个大转折？
奖励类型分别是什么？
读者最爽的一刻来自哪里？
前面压了多久？
主角付出了什么成本？
```

## 目录结构

```text
book/
├── SKILL.md
├── README.md
├── sources/
│   ├── books/        # 放你的书籍资料，本仓库默认不提交原书
│   └── notes/        # 放你的写作笔记、爆款拆解
├── library/          # 沉淀出来的技巧库
├── rules/            # 固定写作规则
├── templates/        # 分析模板
├── workflows/        # 工作流说明
└── scripts/          # 本地导入脚本
```

## 重点规则文件

```text
rules/no-ai-smell.md
rules/novel-logic-checklist.md
rules/suspense-reversal-payoff.md
rules/reader-reward-rhythm.md
```

## 重点模板文件

```text
templates/book-analysis-template.md
templates/suspense-reversal-map-template.md
templates/reader-reward-map-template.md
templates/chapter-diagnosis-template.md
templates/technique-card-template.md
```

## 安装到本地 Agent

如果你用 Claude Code：

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.claude/skills/novel-writing-master
```

如果你用 Copilot CLI / Amp 共用路径：

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.agents/skills/novel-writing-master
```

如果你用 GitHub Copilot CLI：

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.copilot/skills/novel-writing-master
```

## 已经安装过的更新方式

如果你之前已经 clone 过，进入本地目录后执行：

```bash
cd ~/.claude/skills/novel-writing-master
git pull
```

如果你装在 `~/.agents/skills/novel-writing-master` 或 `~/.copilot/skills/novel-writing-master`，进入对应目录再 `git pull`。

## 第一次使用

先检查依赖：

```bash
python3 scripts/ingest.py --check
```

然后把你的书放进本地目录：

```text
sources/books/
```

支持：txt、md、markdown、html、htm、docx、pdf、epub、rtf。

再运行：

```bash
python3 scripts/ingest.py sources/books sources/notes
```

它会生成：

```text
library/_extracted/
library/source-register.md
library/source-register.json
```

## 推荐调用方式

```text
/novel-writing-master 分析 sources/books 里的书，建立我的小说技巧库。
```

```text
/novel-writing-master 深度拆解这本小说：悬疑在哪里，如何布置，最后如何打开；反转在哪里，是否公平；爽点在哪里，读者多久获得一次奖励。
```

```text
/novel-writing-master 用技巧库检查我这一章，重点看主线、冲突、悬疑锁钥、伏笔回收、反转、爽点密度、逻辑、节奏、AI味。
```

```text
/novel-writing-master 按我的技巧库重写这段，要求三秒钩子、十秒留人、悬疑有锁有钥匙、反转有铺垫、爽点有前置压迫、冲突落地、去AI味、最后一句让人想评论。
```

```text
/novel-writing-master 从书库里提炼“短小说爆款开头”的规则，给我20条可执行规则。不要空话，每条都要能直接操作。
```

## 版权提醒

这个 Skill 是给你个人学习和写作使用的。不要把受版权保护的原书、提取文本或完整分析库公开发布。本仓库已经设置 `.gitignore`，默认不提交 `sources/books/` 里的原书和 `library/_extracted/` 里的提取文本。
