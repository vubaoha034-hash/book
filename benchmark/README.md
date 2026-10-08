# Novel Distillation Benchmark V1

本目录是 `novel-writing-master` 的独立验收层。

## 目标

不是证明“我们自己的系统更复杂”，而是回答四个可验证问题：

1. 哪个现成方案在同一输入、同一模型、同一预算下表现最好？
2. 每个方案真正强在哪里、弱在哪里？
3. 我们移植一个能力后，是否产生可重复的净提升？
4. 最终生成的新章节是否比基线更好，而不是分析报告更漂亮？

## 核心原则

- **Benchmark First**：P0/P1 阶段禁止重写蒸馏核心。
- **Upstream First**：成熟上游已有实现时先原样测，未经对照证明不重写。
- **One Major Variable**：一次实验只允许一个主要改动。
- **Protocol Isolation**：Style 与 Narrative 隐藏集使用两套独立状态、缓存和派生资产。
- **No Hidden Leakage**：对应协议的隐藏集不能进入蒸馏、摘要、RAG、提示词、人工笔记或缓存。
- **No Source Contamination**：AI 生成稿永远不能进入原作者语料。
- **Evidence over Self-score**：模型自评分、文件存在、清单打勾都不是质量证据。
- **Blind Writing Test**：最终必须比较匿名化的新章成品，不只比较拆书报告。
- **Regression Gate**：新模块不提升或造成受保护指标下降就回滚，不因投入成本保留。

## 目录

```text
benchmark/
├─ README.md
├─ TEST_PLAN_V1.md
├─ config/
│  ├─ scoring.v1.json
│  ├─ upstreams.v1.json
│  └─ upstream-lock.v1.json
└─ templates/
   └─ experiment-manifest.template.json

scripts/
├─ prepare_benchmark_corpus.py
└─ validate_benchmark.py
```

`upstreams.v1.json` 记录候选项目和职责；`upstream-lock.v1.json` 锁定一个 Benchmark Wave 实际测试的精确 commit 与许可证边界。上游更新不能静默替换锁定版本，必须开新 Wave。

## 私有数据结构

原始小说、隐藏集、派生缓存、运行产物和上游 checkout 不得提交到这个公开仓库。

推荐：

```text
benchmark/_private/
├─ corpus/
│  └─ <CORPUS-ID>/
│     ├─ style/
│     │  ├─ train/
│     │  └─ holdout/
│     ├─ narrative/
│     │  ├─ context/
│     │  └─ future_holdout/
│     └─ manifest.private.json
├─ upstream_checkouts/
├─ cache/
├─ runs/
└─ blind_packets/
```

## 两套隐藏协议

### Style Protocol State

从 Future Holdout 之前的故事阶段中分层留出章节，只验证句法、对白、节奏、叙述距离、信息密度等可迁移风格规律。

Style State 不得读取 Style Holdout 的正文、摘要、embedding、统计特征、人工笔记或任何源文本派生物。

### Narrative Protocol State

使用从开篇到 cutoff 的完整连续 Context，并把 cutoff 后一段连续章节作为 Future Holdout，用来测试人物行为、关系变化、因果、伏笔与信息释放预测。

Future Holdout 后面的章节同样不能提前读，否则会通过后文反向泄漏隐藏事件。

### 为什么不能共用一个状态

如果 Style Holdout 从中间挖走章节，Narrative 测试会被人为制造剧情缺口；如果 Narrative State 已读过那些章节，又把其摘要/RAG/缓存给 Style 测试，则 Style Holdout 已泄漏。

所以两套状态必须具有独立 `state_namespace`、RAG、cache namespace、Agent/LLM 状态和派生卡片，禁止跨协议复用。

## 准备私有语料

```bash
python scripts/prepare_benchmark_corpus.py SOURCE.txt \
  --corpus-id SMOKE-CN-001 \
  --output benchmark/_private/corpus \
  --smoke-chapters 50 \
  --future-holdout 8 \
  --style-holdout-count 6
```

脚本会：

- 自动识别 `第…章` 章节边界；
- 记录源文件和每章 SHA-256；
- 生成 Style / Narrative 两套隔离目录；
- 生成私有 manifest；
- 默认拒绝覆盖已存在 Corpus，除非显式传 `--overwrite`。

## 开发阶段

1. **P0 Benchmark Contract**：冻结评分、门禁、输入规范、版本锁和实验记录格式。
2. **P1 Baselines**：原样跑候选上游，不做自研修补。
3. **P2 Mother Selection**：按结果选母体，不按 Star、README 或主观偏好。
4. **P3 Gap Analysis**：只选择前三个最大、可定位短板。
5. **P4 Single Patch Experiments**：一次只移植一个能力。
6. **P5 Long-book Stress**：进入生产候选后才要求整本 100% Coverage。
7. **P6 Blind Writing Test**：匿名成品盲测。
8. **P7 ChatGPT Compiler**：把重资产编译成普通 ChatGPT 可按需消费的 Novel Brain。
9. **P8 Regression Suite**：之后任何升级必须重跑受影响基准。

## 重要边界

Benchmark 不允许：

- 为“融合所有 Skill”同时引入多个状态系统、多个 Reviewer 或多个风格引擎；
- 用抽样分析冒充整本覆盖；
- 用同一上下文扮演多个读者冒充独立盲评；
- 把第三方完整版权小说提交到公开 GitHub；
- 未核许可证就复制上游代码；
- 因为某个补丁写了很多代码就降低回滚标准。

## 验证

```bash
python scripts/validate_benchmark.py
```

该脚本只验证 Benchmark 契约、配置、版本锁和隔离规则；**结构验证通过不等于小说质量通过。**
