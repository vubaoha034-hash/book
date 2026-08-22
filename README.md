# Novel Writing Master V3

这是一个面向中文小说、公众号短篇、网文和短剧化故事的 Agent Skill。

V3 不再用“阶段很多、清单很多、自评分很高”证明小说好看，而要求可定位证据：因果、情绪债与兑现、恨感/共情、连续性与局部语义、对白真实动机、独立读者反应和个人审美指纹。

V2 资产继续保留兼容；新任务默认走 V3。

## 完整流程

```text
故事契约
→ 因果证明
→ 情绪欠账与兑现
→ 恨感 / 共情
→ 人物 / 连续性 / 局部语义账本
→ 场景计划 + 高影响对白触发计划
→ 分场正文
→ 开篇冷读
→ 读者证据
→ V3-G6D 局部真值审查
→ 定向修改
→ G8 个人文风 / Pattern Family / 去 AI
→ 最终复核
```

详细流程：`workflows/07-novel-master-pipeline-v3.md`

机器闸门：`config/novel-quality-gates.v3.json`

## MICROCRAFT + DIALOGUE + LOCAL LOGIC

真实稿件曾经过旧 V3、去 AI 和 fresh cold read 后仍出现局部时间语义错误、信息载体争议和重复问答节拍，说明“Fresh context + 检查清单”不能替代更细的证据模型。

三本原著已用同 schema 完成 90 个 raw-derived abstract Scene-to-Speech 样本：

- BOOK-01《射雕英雄传》30；
- BOOK-02《诛仙》30；
- BOOK-03《盗墓笔记【壹】》30。

这些证据支持“对白来自场内刺激/任务/关系/感知/沉默/物件”，但**不支持“每句闲聊都必须改变任务状态”**。

### Phase344 校准：停止追错误的 3/3

Fresh Attempts 2–5 的历史结果全部保留，不事后改分。连续 fresh disagreement + 三书对照说明旧回归中的两个标签过强，因此未来合同已校准：

- `MC-R001`：确定性 inherited time/state contradiction，继续是 G6D 硬 FAIL；
- `MC-R002`：不再是 mandatory single-instance mouthpiece FAIL，改为 **epistemic-scope/context-dependent**；
- `MC-R003`：不再是 mandatory single-instance template FAIL，改为**局部语境判断 + 全文 pattern-family density 风险**。

校准合同：

```text
benchmark/microcraft/label-calibration.v1.json
benchmark/microcraft/epistemic-pattern-regression.v1.json
```

历史 `dialogue-regression.v1-v4.json` 保留为审计证据，不再作为未来 3/3 晋级标准。

## V3-G6D V1.4：认知层级先于嘴替判断

核心文件：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/dialogue-epistemic-scope.md
modules/local-logic-ledger.md
templates/microcraft-dialogue-audit-template.md
```

G6D 必须区分：

```text
OBJECT_FACT
LISTENER_KNOWS_OBJECT_FACT
PUBLIC_KNOWLEDGE_OF_OBJECT_FACT
REPORTED_RUMOR_CONTENT
EVIDENCE_OF_EXPOSURE_OR_SPREAD
ACTIONABLE_RISK_FROM_PUBLIC_KNOWLEDGE
```

关键原则：

> 人物知道 X，不等于人物知道“外界也已经知道 X”。

因此，已知 object fact 被重新说出，不自动等于作者嘴替；它可能是为了传达新的 rumor/public-knowledge/exposure proposition。

但“外界知道”必须有消息、来人、环境变化、目击、记录等证据。没有证据时 HOLD。

`AUTHOR_INFORMATION_MOUTHPIECE_FAIL` 继续保留，但收窄到真正的情况：双方共享背景，没有新的 object/meta-knowledge/risk/关系/任务 payload，主要受益者只有读者。

确定性局部时间/状态链仍是硬门禁：

`anchor → semantic relation → inherited scope → later explicit fact`

## 局部 anti-template：不再逐句猎杀笑话

所有 rhetorical ladder 仍必须逐项审计并满足 ATS parity。

self-cancelling assertion、induced follow-up、turn deletion、portability 仍是诊断信号，但**单个 locally plausible/removable joke 不因可删就自动 FAIL G6D**。

只有本场独立失真时，才使用：

`DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE`

例如关键事实被空转拖住、无任何文本支持的目标/关系压力、或纯为制造下一问而构造假前提。

局部成立但很通用/可移植的节拍，转入 G8。

## G8：Dialogue Pattern Family Density

读取：

```text
modules/dialogue-pattern-family-density.md
templates/dialogue-pattern-family-audit-template.md
rules/no-ai-smell.md
modules/line-editor-deslop.md
```

G8 检查的是全文：

- 相隔很远的场景是否重复同一种 cadence skeleton；
- 不同人物和不同关系是否都使用相似的问答/回避/包袱机器；
- 是否缺乏当前物件、任务、旧账、身份的特异性；
- 对白能否几乎原样平移给无关人物；
- 是否最终形成“所有人物像同一个模型”的声音同质化。

风险码：

`DIALOGUE_TEMPLATE_FAMILY_DENSITY_RISK`

**没有统一数字阈值。** 当前三书 purposive evidence 不支持“出现 N 次就失败”。

幽默多本身不是 AI 味；同一人物的固定习惯、running joke、具体关系暗号可以 PASS/HOLD。

## Optional Novel DNA Router

Novel DNA Router 继续 DEFAULT OFF。只有存在具体结构问题、普通 V3 修复不足、且有退出条件时才允许调用。

当前首个 Global Novel DNA：

```text
GN-VDNA-01
RECURRING_NARRATIVE_ASSET_GAINS_CAUSAL_MEANING
```

Global 是证据层级，不是普遍文学定律。生产只到 `OPTIONAL_BOUNDED_PRODUCTION`；公开 GitHub 只记录脱敏元数据，不保存真实稿件正文。

治理：

```text
docs/NOVEL_DNA_BOUNDED_PRODUCTION_GOVERNANCE_V1.md
state/production/NOVEL_DNA_ROUTER_PRODUCTION_GOVERNANCE_V1.json
state/production/NOVEL_DNA_REAL_USE_LEDGER_V1.jsonl
```

## Novel Distillation Benchmark V1

`benchmark/` 是独立验收层，不替换 V3。它固定 Source / Coverage / Evidence / Holdout / Reproducibility / Experiment / Review / License 门禁、Style/Future Holdout 隔离、同输入同预算比较和 Regression Gate。

入口：

```text
benchmark/README.md
benchmark/TEST_PLAN_V1.md
benchmark/config/scoring.v1.json
benchmark/config/upstreams.v1.json
```

Microcraft regression 是独立局部回归子套件，不与 100 分 Benchmark 相加。

## Novel Preprocessor V1

本地预处理只负责 TXT、EPUB、DOCX、Markdown、可提取文本 PDF 的解析、保守清洗、章节检测、确定性 ID/SHA-256、去重和私有结构化输出，不调用在线 AI/API，也不生成文学分析。

固定工作目录：`E:\蒸馏小说`。Git 仓库：`E:\蒸馏小说\repo`；私有资料：`E:\蒸馏小说\_private`。

## 验证

```bash
python scripts/validate_skill.py
python scripts/validate_benchmark.py
python scripts/validate_microcraft_regression.py
python scripts/validate_private_boundaries.py
```

结构验证通过不等于小说质量通过；语义和文学判断仍必须由具体文本证据证明。

## 版权与隐私

- 只学习抽象技法，不复制第三方作品。
- 不模仿在世作者可识别的个人风格。
- 不把私有原书、完整提取文本、真实稿件正文或个人审美样本提交到公开仓库。
