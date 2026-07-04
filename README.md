# Novel Writing Master Skill

这是一个给中文小说创作准备的 Agent Skill。目标不是“总结书”，而是把你的写作书籍、爆款小说、写作笔记沉淀成一个可反复调用的写作技巧库。

## 核心效果

- 导入你自己的写作书、小说案例、爆款分析、写作笔记。
- 提炼可复用技巧：开头钩子、人物发动机、冲突递进、章节留存、反转、节奏、情绪机制。
- 建立长期技巧库：每本资料一个分析卡，全局一个方法库。
- 帮你诊断小说：主线是否清晰、冲突是否落地、节奏是否拖、逻辑是否断、AI味是否重。
- 帮你重写：更像真人写，更有现实摩擦，更有商业阅读感。

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
/novel-writing-master 用技巧库检查我这一章，重点看主线、冲突、逻辑、节奏、AI味。
```

```text
/novel-writing-master 按技巧库重写这段，要求三秒钩子、十秒留人、冲突落地、去AI味、最后一句让人想评论。
```

```text
/novel-writing-master 从书库里提炼“短小说爆款开头”的规则，给我20条可执行规则。
```

## 版权提醒

这个 Skill 是给你个人学习和写作使用的。不要把受版权保护的原书、提取文本或完整分析库公开发布。本仓库已经设置 `.gitignore`，默认不提交 `sources/books/` 里的原书和 `library/_extracted/` 里的提取文本。
