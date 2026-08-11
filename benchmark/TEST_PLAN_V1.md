# Benchmark Test Plan V1

## 0. 验收对象

Benchmark 比较的是“系统在同一任务上的实际结果”，不是 README、Star 数、Agent 数量或代码行数。

第一波基线：

1. `AI-Novel-Writing-Assistant`
2. `oh-story-claudecode`
3. `Persona-Story-Gen` 方法链
4. `InkOS`

其中不同项目的产品定位不同，因此允许出现“某项目只能参加部分维度”的结果；禁止为了让它参加所有项目而重写其核心逻辑。

## 1. Corpus 规则

### 1.1 Smoke Corpus

第一轮只验证 Benchmark 能否工作：

- 1 部用户合法持有/可测试的中文小说；
- 30–50 个连续章节或等量场景；
- 只放本地 `benchmark/_private/`；
- 建立源文件 SHA-256 清单；
- 不提交原文到公开仓库。

Smoke 结果只用于发现流程 Bug，不用于宣布“最佳系统”。

### 1.2 Promotion Corpus

进入“母体选择”至少需要：

- 2 部不同作者或不同类型的中文长篇；
- 每部都具有 development / style holdout / future holdout；
- 至少一部不是系统开发过程中反复调参的主样本。

### 1.3 Final Blind Corpus

在版本接近满分时启用新的隐藏作品或此前从未用于调参的隐藏段落。开发者在冻结版本前不能读取其评价答案。

## 2. 数据切分

### 2.1 Development

允许蒸馏、调试、建立 DNA、RAG、状态和统计。

### 2.2 Style Holdout

从开篇、中段、后段分层留出，用于测试：

- 句长与段落节奏；
- 对白特征；
- 叙述距离与 POV；
- 信息密度；
- 情绪推进；
- 可迁移文风规则。

不得把 Style Holdout 的正文、摘要、人工笔记或派生特征输入蒸馏系统。

### 2.3 Future Holdout

保留连续的未来章节，用于测试：

- 人物下一步选择；
- 关系变化方向；
- 伏笔是否被正确识别；
- 情节因果预测；
- 信息释放方式。

Future Holdout 之后的章节也不得进入训练侧，否则会通过后文反向泄露隐藏事件。

## 3. Baseline 公平性

直接比较必须保持：

- 同一源文本；
- 同一可用上下文范围；
- 同一基础模型/模型版本，若上游强制模型不同则标记为“ecosystem comparison”，不得伪装成纯方法比较；
- 同一最大上下文预算；
- 同一输出任务；
- 同一人工信息；
- 同一是否允许联网/工具；
- 记录上游 commit SHA。

允许使用“中性 Adapter”完成格式转换，但 Adapter 只能：

- 文件格式转换；
- 章节编号映射；
- 字段名称映射；
- 运行日志采集。

Adapter 不得：

- 增加新的文学分析；
- 替某一个上游补 Prompt；
- 替某一个上游额外摘要；
- 偷看 Holdout。

## 4. P1 Baseline Tasks

每个可参赛系统执行相同任务集。

### T1 Source Notes

输出关键事件、人物、关系、世界规则、时间、伏笔、读者预期、风格技巧，并要求定位证据。

### T2 Character Counterfactual

给出未出现过的新情境，让系统预测主要人物会怎么选、为什么、什么选择最不可能。

目标：区分“人物标签总结”和“行为模型”。

### T3 Style Generalization

只使用 Development 建立风格资产，再对 Style Holdout 做特征预测/匹配。

目标：检测是否只是复述见过的句子。

### T4 Future Narrative Prediction

只使用 Future Holdout 之前的信息，预测下一阶段的冲突、人物选择、关系变化、伏笔回收方向。

### T5 New Scene Writing

统一给定：

- 相同人物状态；
- 相同场景目标；
- 相同冲突；
- 相同字数；
- 相同禁止复制要求。

每个系统生成匿名版本 `X/Y/Z/...`。

### T6 Long-memory Retrieval

故意询问相距较远的事实、物件、关系、秘密和伏笔，检查召回与错误自信。

### T7 Cost and Failure

记录：

- 输入/输出 token；
- 运行时间；
- 重试次数；
- 失败单元；
- 需要人工修复的步骤；
- 上下文大小；
- 缓存命中情况。

## 5. 评价层

### 5.1 Deterministic Metrics

只计算适合机器确定的指标：

- 章节覆盖率；
- 证据定位有效率；
- 实体/时间线一致性；
- 句长、段落、对白比例；
- 重复率；
- n-gram/长片段重合，用于抄袭风险而非简单“越像越好”；
- token、时间、失败率。

禁止让 LLM 猜这些数值。

### 5.2 Independent Judge

Judge 不得看到系统真实名称；只看到匿名结果和固定 rubric。

Judge 负责：

- 人物可信度；
- 因果；
- 情绪；
- 节奏；
- 信息释放；
- 文风机制；
- 阅读欲望。

同一写作模型给自己的输出打分不能单独作为独立证据。

### 5.3 Human Blind Review

进入 preferred/production 前必须进行人工匿名比较。

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

如果结果：

- 小于阈值：`INCONCLUSIVE`，重复；
- 提升且无受保护指标明显回退：`ACCEPT`；
- 总分下降、目标维度不升、Gate 失败：`REJECT/REVERT`。

写了多少代码、花了多少时间、架构是否漂亮，不进入接受条件。

## 7. Long-book Stress

只有 preferred 候选进入整本压力测试。

生产态“理解整本”必须满足：

```text
successful_source_units == total_source_units
```

任何失败章节必须：

- 显式记录；
- 重试或人工判定；
- 未恢复前禁止声称完整覆盖。

长书测试额外检查：

- 人物状态漂移；
- 关系漂移；
- 时间线；
- 物件状态；
- 已知/未知信息；
- 世界规则；
- 伏笔与 reader expectation；
- 早期知识是否能在远距离写作时正确检索。

## 8. ChatGPT Compiler 验收

重计算完成后，最终资产必须能编译为轻量 Novel Brain，而不是要求普通 ChatGPT 每次加载全部数据库。

按任务动态加载：

- Character DNA
- Dialogue DNA
- Scene DNA
- Emotion DNA
- Rhythm/Style DNA
- Hook/Canon state
- 必要证据示例

验收条件：

- 不加载无关模块时，质量不得显著下降；
- 上下文成本明显低于全量加载；
- 关键事实召回不下降；
- 普通 ChatGPT 能在不依赖 Codex 全量运行的情况下完成写作阶段。

## 9. “100 分”规则

100 分只表示当前冻结 Benchmark 的满分，不表示文学意义上的完美。

如果开发集达到 100，而 Final Blind Corpus 明显下降：

- 公开分数回退到隐藏集表现；
- 记录为 benchmark overfitting；
- 禁止把开发集 100 分作为生产质量宣传。
