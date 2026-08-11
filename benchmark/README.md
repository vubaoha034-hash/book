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
- **Upstream First**：成熟上游已有实现时，先原样测；未经对照证明，不重写。
- **One Major Variable**：一次实验只允许一个主要改动。
- **No Hidden Leakage**：隐藏集不能进入蒸馏、摘要、RAG、提示词、人工笔记或缓存。
- **No Source Contamination**：AI 生成稿永远不能进入原作者语料。
- **Evidence over Self-score**：模型自评分、文件存在、清单打勾都不是质量证据。
- **Blind Writing Test**：最终必须比较匿名化的新章成品，不只比较拆书报告。
- **Regression Gate**：新模块不提升或造成受保护指标下降，回滚，不因投入成本保留。

## 目录约定

```text
benchmark/
├─ README.md
├─ TEST_PLAN_V1.md
├─ config/
│  ├─ scoring.v1.json
│  └─ upstreams.v1.json
└─ templates/
   └─ experiment-manifest.template.json
```

私有测试语料、隐藏集、缓存、上游仓库 checkout 和实际运行产物必须保存在本机忽略目录，不提交到这个公开仓库。

推荐本地结构：

```text
benchmark/_private/
├─ corpus/
│  ├─ train/
│  ├─ style_holdout/
│  └─ future_holdout/
├─ upstream_checkouts/
├─ cache/
├─ runs/
└─ blind_packets/
```

## 两种隐藏集，不可混淆

### Style Holdout

从不同故事阶段分层留出文本，用来验证句法、对白、节奏、叙事习惯等风格规律是否能泛化。

### Future Holdout

保留连续的末段章节，训练/蒸馏时不得读取其后续内容，用来测试人物行为、伏笔、因果和剧情预测是否真的学到了机制。

只留“随机章节”不能可靠测试剧情预测，因为后续章节可能反向泄露隐藏章节发生了什么。

## 开发阶段

1. **P0 Benchmark Contract**：冻结评分、门禁、输入规范和实验记录格式。
2. **P1 Baselines**：原样跑候选上游，不做自研修补。
3. **P2 Mother Selection**：按结果选母体；不按 Star、README 或主观偏好。
4. **P3 Gap Analysis**：只选择前三个最大、可定位短板。
5. **P4 Single Patch Experiments**：一次只移植一个能力。
6. **P5 Long-book Stress**：进入生产候选后才要求整本 100% Coverage。
7. **P6 Blind Writing Test**：匿名成品盲测。
8. **P7 ChatGPT Compiler**：把重资产编译成普通 ChatGPT 可按需消费的 Novel Brain。
9. **P8 Regression Suite**：之后任何升级必须重跑受影响基准。

## 重要边界

这个 Benchmark 不允许：

- 为了“融合所有 Skill”而同时引入多个状态系统、多个 Reviewer 或多个风格引擎；
- 用抽样分析冒充整本覆盖；
- 用同一上下文扮演多个读者冒充独立盲评；
- 把第三方完整版权小说提交到公开 GitHub；
- 未核许可证就复制上游代码；
- 因为某个补丁写了很多代码，就降低回滚标准。

## 验证

```bash
python scripts/validate_benchmark.py
```

该脚本只验证 Benchmark 契约、配置和隔离规则是否完整；它不会声称小说质量已经通过。
