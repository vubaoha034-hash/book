# Benchmark Test Plan V1

## 0. 验收对象

Benchmark 比较的是“系统在同一任务上的实际结果”，不是 README、Star 数、Agent 数量或代码行数。

第一波基线：

1. `AI-Novel-Writing-Assistant`
2. `oh-story-claudecode`
3. `Persona-Story-Gen` 方法链
4. `InkOS`

不同项目产品定位不同，允许某项目只参加其原生支持的维度；禁止为了让它参加所有项目而重写其核心逻辑。

## 1. Corpus 规则

### 1.1 Smoke Corpus

第一轮只验证 Benchmark 能否稳定运行：

- 1 部合法持有/可测试的中文小说；
- 30–50 个连续章节或等量场景；
- 只放本地私有目录；
- 建立源文件和章节 SHA-256 清单；
- 不提交原文到公开仓库。

Smoke 结果用于发现流程 Bug，不用于宣布“最佳系统”。

标准准备命令：

```bash
python scripts/prepare_benchmark_corpus.py SOURCE.txt \
  --corpus-id SMOKE-CN-001 \
  --output benchmark/_private/corpus \
  --smoke-chapters 50 \
  --future-holdout 8 \
  --style-holdout-count 6
```

### 1.2 Promotion Corpus

进入“母体选择”至少需要：

- 2 部不同作者或不同类型的中文长篇；
- 每部都生成独立的 Style Protocol State 与 Narrative Protocol State；
- 至少一部不是开发过程中反复调参的主样本。

### 1.3 Final Blind Corpus

版本接近满分时启用新的隐藏作品或此前从未参与调参的隐藏段落。冻结候选版本之前，不得读取其评价答案来继续调参。

## 2. 数据切分：必须使用两套隔离状态

**Style Holdout 和 Future Holdout 不能共享同一个已蒸馏状态、RAG、缓存或派生资产。**

原因：如果为了 Style Holdout 从故事中段删除章节，Narrative 测试会被人为制造剧情缺口；如果 Narrative 状态读取这些章节，再把同一派生资产用于 Style 测试，则 Style Holdout 已泄漏。

因此同一个源文件必须构建两个独立协议状态。

### 2.1 Style Protocol State

用途：T3 Style Generalization，以及只依赖风格机制的测试。

做法：

- 先确定 Future Holdout 起点；
- 只在 Future Holdout 之前的章节中分层抽取 Style Holdout；
- Style 状态只能看到其余 Development 章节；
- Style Holdout 正文、摘要、embedding、统计特征、人工笔记、模型记忆均不得进入该状态。

建议目录：

```text
<corpus>/style/train/
<corpus>/style/holdout/
```

### 2.2 Narrative Protocol State

用途：T1 Source Notes、T2 Character Counterfactual、T4 Future Narrative Prediction、T5 New Scene Writing、T6 Long-memory Retrieval。

做法：

- Context 必须是从开篇到 cutoff 的完整连续章节；
- Future Holdout 必须是 cutoff 后连续的一段未来章节；
- Future Holdout 之后的任何章节也不能进入 Context，否则会通过后文反向泄露隐藏事件。

建议目录：

```text
<corpus>/narrative/context/
<corpus>/narrative/future_holdout/
```

### 2.3 Cross-state Isolation Gate

Style 与 Narrative 两套状态必须分别拥有：

- `state_namespace`；
- RAG/embedding 索引；
- LLM/Agent 会话状态；
- 摘要和派生卡片；
- cache namespace；
- run manifest。

禁止跨协议复用任何由源文本派生、且可能含隐藏信息的资产。

允许跨协议共享的只有：

- 原始源文件的不可变 SHA-256；
- 章节边界/编号映射本身；
- 与正文内容无关的程序代码和 Schema；
- Benchmark 配置。

## 3. Baseline 公平性

直接比较必须保持：

- 同一协议状态；
- 同一可见源文本；
- 同一基础模型/模型版本；若上游强制模型不同，标记为 `ecosystem comparison`，不得伪装成纯方法比较；
- 同一最大上下文/输出预算；
- 同一输出任务；
- 同一人工补充信息；
- 同一联网/工具权限；
- 记录精确上游 commit SHA。

允许“中性 Adapter”做：

- 文件格式转换；
- 章节编号映射；
- 字段名称映射；
- 运行日志与 token/时间采集。

Adapter 禁止：

- 增加新的文学分析；
- 给某个上游额外补 Prompt；
- 额外摘要、额外 RAG 或额外记忆；
- 偷看对应协议的 Holdout。

## 4. P1 Baseline Tasks

### T1 Source Notes

使用 Narrative State，输出关键事件、人物、关系、世界规则、时间、伏笔、读者预期、风格技巧，并要求定位证据。

### T2 Character Counterfactual

使用 Narrative State。给出原文未出现过的新情境，让系统预测主要人物会怎么选、为什么、什么选择最不可能。

目标：区分“人物标签总结”和“人物行为模型”。

### T3 Style Generalization

使用独立 Style State。只能用 Style Train 建风格资产，然后在 Style Holdout 上验证特征预测与匹配。

目标：检测系统是否学到可泛化规律，而不是复述见过的文本。

### T4 Future Narrative Prediction

使用 Narrative State。只看 Context，预测 Future Holdout 阶段的冲突、人物选择、关系变化、伏笔回收和信息释放方向。

### T5 New Scene Writing

使用 Narrative State。统一给定：

- 相同人物状态；
- 相同场景目标；
- 相同冲突；
- 相同字数；
- 相同禁止复制要求。

每个系统只输出匿名版本 `X/Y/Z/...`。

### T6 Long-memory Retrieval

使用 Narrative State。故意询问相距较远的事实、物件、关系、秘密和伏笔，检查召回率、矛盾率和错误自信。

### T7 Cost and Failure

每个协议状态分别记录：

- 输入/输出 token；
- 运行时间；
- 重试次数；
- 失败单元；
- 需要人工修复的步骤；
- 上下文大小；
- 缓存命中；
- state/cache namespace。

## 5. 评价层

### 5.1 Deterministic Metrics

只计算适合机器确定的指标：

- 章节覆盖率；
- 证据定位有效率；
- 实体/时间线一致性；
- 句长、段落、对白比例；
- 重复率；
- n-gram/长片段重合，用于抄袭风险，不把“越像”简单视为“越好”；
- token、时间、失败率。

禁止让 LLM 猜这些数值。

### 5.2 Independent Judge

Judge 不得看到系统真实名称，只能看到匿名结果和冻结 rubric。

Judge 负责：

- 人物可信度；
- 因果；
- 情绪；
- 节奏；
- 信息释放；
- 文风机制；
- 阅读欲望。

同一个写作模型给自己的输出打分不能单独作为独立证据。

### 5.3 Human Blind Review

进入 `preferred` / `production` 前必须人工匿名比较。

至少回答：

1. 哪篇最想继续读？
2. 哪篇人物最像真人？
3. 哪篇对白最好？
4. 哪篇 AI 味最低？
5. 哪篇节奏最好？
6. 哪篇最像学到了“方法”而不是复制？
7. 哪篇有明显逻辑漏洞或人物失真？

## 6. Patch 实验规则

只有 Baseline 完成后才允许 Patch。

一个 Patch 必须写明：

- 当前最大短板；
- 目标维度；
- 借鉴哪个上游的哪个具体方法；
- 为什么现有母体缺这个能力；
- 只改变一个主要变量；
- 哪些指标必须保护不下降。

默认接受规则见 `config/scoring.v1.json`。

结果处理：

- 小于阈值：`INCONCLUSIVE`，重复；
- 提升且无受保护指标明显回退：`ACCEPT`；
- 总分下降、目标维度不升、Gate 失败：`REJECT/REVERT`。

代码量、开发时间、架构漂亮程度都不进入接受条件。

## 7. Long-book Stress

只有 `preferred` 候选进入整本压力测试。

生产态声称“理解整本”必须满足：

```text
successful_source_units == total_source_units
```

任何失败章节必须显式记录并重试/人工判定，未恢复前禁止声称完整覆盖。

额外检查：

- 人物状态漂移；
- 关系漂移；
- 时间线；
- 物件状态；
- 已知/未知信息；
- 世界规则；
- 伏笔与 reader expectation；
- 早期知识能否在远距离写作时正确检索。

## 8. ChatGPT Compiler 验收

重计算结束后，最终资产必须编译成轻量 Novel Brain，而不是要求普通 ChatGPT 每次加载全部数据库。

按任务动态加载：

- Character DNA
- Dialogue DNA
- Scene DNA
- Emotion DNA
- Rhythm/Style DNA
- Hook/Canon state
- 必要证据示例

验收条件：

- 不加载无关模块时质量不得显著下降；
- 上下文成本明显低于全量加载；
- 关键事实召回不下降；
- 普通 ChatGPT 在不依赖 Codex 全量运行的情况下能完成写作阶段。

## 9. “100 分”规则

100 分只表示当前冻结 Benchmark 的满分，不表示文学意义上的完美。

如果开发集达到 100，而 Final Blind Corpus 明显下降：

- 公开结果回退到隐藏集表现；
- 记录为 `benchmark overfitting`；
- 禁止把开发集 100 分作为生产质量结论。
