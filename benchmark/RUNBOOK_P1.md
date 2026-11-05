# P1 Baseline Execution Runbook

本 Runbook 只执行现成上游 Baseline。**禁止在 P1 修改上游核心、补文学 Prompt、融合功能或写自研蒸馏引擎。**

## 0. P1 的真实目标

P1 不是选“功能最多”的仓库，而是先回答：

1. Benchmark 本身能不能稳定、公平、无泄漏地跑完？
2. 两个母体候选 `AI-Novel-Writing-Assistant` 与 `oh-story-claudecode` 在全栈任务上的真实表现如何？
3. `Persona-Story-Gen` 的 Delta 方法是否在 Style 维度产生增益？
4. `InkOS` 的长期状态/记忆是否在 Longform 维度产生增益？

组件挑战者不参与虚假的 100 分总排名。

## 1. 执行顺序：串行门禁

不要同时配置四套环境。

```text
P1-S0 Benchmark preflight
    ↓ PASS
P1-S1 oh-story smoke baseline
    ↓ Benchmark mechanics PASS
P1-S2 AI-Novel smoke baseline
    ↓ 两个母体基线齐全
P1-S3 Persona Delta component baseline
    ↓
P1-S4 InkOS memory component baseline
    ↓
P1-S5 Baseline Report + P2 mother selection
```

任何阶段发现 Benchmark 自身 Bug，先修 Benchmark，再继续后续项目。不要把同一个 Bug 的成本复制四遍。

## 2. 固定上游版本

以 `benchmark/config/upstream-lock.v1.json` 为唯一版本源。Wave 1 当前锁定：

```text
AI-Novel-Writing-Assistant
154cdfda58b865c3af7b11a6f222226ced922e30

oh-story-claudecode
70a834e88d1103f494f45667bab4b31472a83b58

Persona-Story-Gen
4a1d0c5fb0087471946666dfc2dad99bac7bdb46

InkOS
a6e05d4d4567df0efd5825e9b0037146a16e4f3e
```

**禁止用 `main` / `latest` 替代锁定 SHA。** 上游升级要开新的 Benchmark Wave。

## 3. 本地目录

Windows 示例：

```text
<BOOK_REPO>\benchmark\_private\
├─ corpus\SMOKE-CN-001\
├─ upstream_checkouts\
│  ├─ oh-story\
│  ├─ ai-novel\
│  ├─ persona\
│  └─ inkos\
├─ workspaces\
│  ├─ oh-story-style\
│  ├─ oh-story-narrative\
│  ├─ ai-novel-style\
│  ├─ ai-novel-narrative\
│  ├─ persona-style\
│  └─ inkos-narrative\
├─ cache\
├─ runs\
└─ blind_packets\
```

这些目录已被 `.gitignore` 保护，禁止强制 `git add -f`。

## 4. P1-S0：Benchmark preflight

在 `book` 仓库 `benchmark-v1` 分支：

```powershell
git status --short
git rev-parse --abbrev-ref HEAD
python scripts\validate_benchmark.py
```

必须满足：

```text
branch = benchmark-v1
validate_benchmark.py exit code = 0
```

然后准备私有 Corpus：

```powershell
python scripts\prepare_benchmark_corpus.py "<LOCAL_SOURCE_NOVEL.txt>" `
  --corpus-id SMOKE-CN-001 `
  --output benchmark\_private\corpus `
  --smoke-chapters 50 `
  --future-holdout 8 `
  --style-holdout-seqs 5,12,19,26,33,40
```

检查生成的 `manifest.private.json`，记录：

- source SHA-256；
- detected chapter count；
- Style state namespace；
- Narrative state namespace；
- Style Holdout；
- Future Holdout。

**不得把 manifest 中的私有源路径或小说正文提交到公开仓库。**

## 5. P1-S1：oh-story Baseline（先跑它）

### 5.1 固定 checkout

```powershell
cd benchmark\_private\upstream_checkouts
git clone https://github.com/worldwonderer/oh-story-claudecode.git oh-story
cd oh-story
git checkout 70a834e88d1103f494f45667bab4b31472a83b58
git rev-parse HEAD
```

最后一行必须严格等于锁定 SHA。

> 不要在 Baseline 使用 `npx skills add ...` 获取最新版，因为最新版可能已经超过冻结 commit。

### 5.2 Windows / Codex 部署边界

该仓库原生支持 Codex。若 `.agents/skills` symlink 在 Windows checkout 中失效，允许使用该仓库自己的 `story-setup` 部署机制把**同一冻结 commit** 的 skill 内容部署到私有测试 workspace；不允许手改 skill 文本。

Style 与 Narrative 必须部署到两个独立 workspace，不能共享 `.codex/`、追踪状态、RAG、摘要或生成资产。

### 5.3 Style State

输入只能来自：

```text
benchmark/_private/corpus/SMOKE-CN-001/style/train/
```

对应隐藏目录：

```text
benchmark/_private/corpus/SMOKE-CN-001/style/holdout/
```

运行原版长篇拆文/文风链。Codex 只允许读取冻结 checkout 和 Style Train；不要把 Holdout 路径放入工作区可见资料。

输出保存到：

```text
benchmark/_private/runs/<RUN-ID>/oh-story/style/
```

### 5.4 Narrative State

新开 Codex 会话、独立 workspace。输入只能来自：

```text
benchmark/_private/corpus/SMOKE-CN-001/narrative/context/
```

隐藏：

```text
benchmark/_private/corpus/SMOKE-CN-001/narrative/future_holdout/
```

运行原版拆文/导入链，并执行 T1/T2/T4/T5/T6。不要加载 Style State 生成的任何文件。

### 5.5 oh-story 门禁

P1-S1 只有同时满足以下条件才算通过：

- 固定 SHA；
- 上游文件未修改；
- 两套 state namespace 独立；
- Holdout 无泄漏；
- 所有输出有 run manifest；
- T1–T7 可被评分；
- 没有为了适配 Benchmark 给 oh-story 补文学 Prompt。

若失败：**先修 Benchmark/中性 Adapter，不进入 AI-Novel。**

## 6. P1-S2：AI-Novel Baseline

### 6.1 固定 checkout

```powershell
cd benchmark\_private\upstream_checkouts
git clone https://github.com/ExplosiveCoderflome/AI-Novel-Writing-Assistant.git ai-novel
cd ai-novel
git checkout 154cdfda58b865c3af7b11a6f222226ced922e30
git rev-parse HEAD
```

上游源码要求：

```text
pnpm 10.6.0+
Node ^20.19.0 || ^22.12.0 || >=24.0.0
```

源码常用启动：

```powershell
corepack enable
pnpm install
pnpm dev
```

普通桌面版也可用于 Native/Ecosystem Baseline，但必须确认实际版本能映射到冻结 source revision；无法证明时不得混入 Controlled Method Baseline。

### 6.2 两种比较标签

#### Native / Ecosystem Baseline

允许项目按它原生推荐的模型路由、RAG、数据库和 UI 方式运行。

它回答：

> “这个现成产品实际用起来有多强？”

#### Controlled Method Baseline

只有在能把 AI-Novel 与 oh-story 配置到同一基础模型、同一输入、同一预算时才运行。

它回答：

> “在模型因素尽量一致时，方法/工作流谁更强？”

如果做不到同模型，必须写 `NOT_COMPARABLE_CONTROLLED`，不能用 Native 分数冒充方法优劣。

### 6.3 隔离

AI-Novel 同样必须建立独立 Style / Narrative 项目或数据库状态。Qdrant 如启用，必须使用不同 collection/namespace；SQLite/项目数据库不能把两个协议状态混在一起。

## 7. P1-S3：Persona Delta 组件挑战

这个仓库不是母体候选，只参加 Style/Generalization 相关测试。

固定 checkout：

```powershell
cd benchmark\_private\upstream_checkouts
git clone https://github.com/Nish-19/Persona-Story-Gen.git persona
cd persona
git checkout 4a1d0c5fb0087471946666dfc2dad99bac7bdb46
git rev-parse HEAD
```

其 README 原生 Delta 流程是：

```text
1. 对 profiling set 生成 Average Author stories
2. 从真实作者文本与 baseline 差异中抽规则
3. 用 Delta 生成 personalized stories
```

本 Benchmark 只允许做**中性数据格式 Adapter**，不允许因为中文小说输入不同就额外增强 Delta Prompt。

当前许可证边界：检查时没有找到仓库根 `LICENSE` 文件，因此 P1 只运行/研究其方法；**禁止把仓库代码复制进 `book` 主仓库。**

## 8. P1-S4：InkOS 组件挑战

InkOS 重点参加：

- longform consistency；
- character/world/state recall；
- hook/reader-expectation state；
- T6 Long-memory Retrieval；
- 必要的 T5 新场景一致性测试。

固定 checkout：

```powershell
cd benchmark\_private\upstream_checkouts
git clone https://github.com/Narcooo/inkos.git inkos
cd inkos
git checkout a6e05d4d4567df0efd5825e9b0037146a16e4f3e
git rev-parse HEAD
```

该版本源码要求 Node `>=20`、pnpm `>=9`；发布版可通过 `npm i -g @actalk/inkos` 安装，但为了冻结版本，Baseline 优先使用固定 checkout 或明确匹配的发布包。

InkOS 原生已有章节导入命令，源码明确支持：

```text
inkos import chapters [book-id] --from <text-file-or-directory>
```

并会 reverse-engineer truth files。Narrative Context 目录可作为导入源；Future Holdout 不得进入项目。

InkOS 为 AGPL-3.0-only。P1 可原样运行和比较；后续若要复制/合并代码，必须另做许可证兼容决策。

## 9. Native vs Controlled：报告必须分开

每个结果必须标记：

```text
comparison_mode:
- native_ecosystem
- controlled_method
```

`native_ecosystem` 可以模型不同，评价的是“整套现成系统”。

`controlled_method` 必须：

- 同模型/版本；
- 同输入；
- 同 token/context 预算；
- 同工具权限；
- 同温度或等价采样设置。

做不到任何一项就降级为 Native，不能把差异归因到方法本身。

## 10. 实验记录

每一次运行复制：

```text
benchmark/templates/experiment-manifest.template.json
```

填入私有 `runs/<RUN-ID>/manifest.json`。

必须记录：

- upstream commit；
- protocol type；
- state namespace；
- visible/hidden partition；
- model/version；
- prompt/skill version；
- token/context budget；
- cache namespace；
-失败/重试；
- 输出路径。

## 11. P1 停止条件

以下任一发生，停止后续安装/测试，先修基础设施：

- Holdout 泄漏；
- 两个协议共享派生缓存；
- 无法固定上游版本；
- 为某个上游偷偷增加文学能力；
- 直接比较时模型或预算不一致却仍准备给出“方法排名”；
- 运行记录缺失；
- 私有小说有被提交到公开 GitHub 的风险；
- Benchmark 规则在看到结果后被改成有利于某个系统。

## 12. P1 完成输出

P1 结束只允许生成：

```text
BASELINE_REPORT_V1.md
FAILURE_CATALOG_V1.md
COST_REPORT_V1.md
MOTHER_SELECTION_EVIDENCE_V1.md
```

在这些证据完成以前，**不创建 Novel Distillation System V1，不修改现有 V3 核心。**
