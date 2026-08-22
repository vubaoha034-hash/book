# Novel Writing Master V3

这是一个面向中文小说、公众号短篇、网文和短剧化故事的 Agent Skill。

V3 不再用“阶段很多、清单很多、自评分很高”证明小说好看，而是要求五类可核查证据：

1. **因果证明**：每个关键场景由前置事实和人物选择逼出，并解释为什么不用更简单办法。
2. **情绪欠账与兑现**：读者被压了什么、在等什么、最后什么真实改变。
3. **恨感与共情**：伤害者是否主动、明知、获益并加码；主角是否有普通欲望、真实缺点和有代价选择。
4. **对白与局部语义**：人物为什么偏偏此刻开口、听者是否需要这段信息、没有读者时人物还会不会说，以及时间/钱/物件/知识作用域是否跨句连续。
5. **个人审美指纹**：认可样本、拒绝样本和当前稿三方比较；没有样本时不冒充已经学会用户文风。

V2 文件继续保留，旧调用方式仍可使用；新任务默认走 V3。

原有的资料导入、技巧库和深度拆书能力继续保留；V3 主要重做新故事生产、审稿证据、局部对白逻辑和去 AI 终审。

## V3 解决什么

- 逻辑表面通顺，实际一问就能解决。
- 主角只会受苦，没有主动选择。
- 反派只靠标签变坏，读者恨不起来。
- 所谓爽点只是旁人震惊、反派脸色难看。
- 情绪一直压，却没有对应的偿还。
- 自己写、自己审、自己给高分，形成假通过。
- 时间线单句都对，但“昨晚 / 前天 / 花销清单 / 物件”等语义作用域跨句后发生硬冲突。
- 人物为了给读者交代背景，说出对当前听者没有场内必要的信息。
- 对白变成“问 → 机灵反问 → 追问 → 包袱”的整齐节拍，但人物目标和场景状态没有变化。
- 去 AI 时机械增加动作、物件、短句，反而产生新型 AI 腔。
- 一轮同时改剧情、逻辑、节奏和文风，越改漏洞越多。

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
→ 读者镜头
→ 连续性审查
→ V3-G6D 对白 grounding / 局部语义审查
→ 高影响修改
→ 个人文风与去 AI
→ 最终复核
```

详细流程：`workflows/07-novel-master-pipeline-v3.md`

机器可读闸门：`config/novel-quality-gates.v3.json`

证据模板：

```text
templates/v3-evidence-packet-template.md
templates/microcraft-dialogue-audit-template.md
```

## MICROCRAFT + DIALOGUE + LOCAL LOGIC V1.2

真实稿件在经过旧 V3、去 AI 与 fresh cold read 后仍曾被误判为“最终冻结”，随后人工发现三类确定问题：跨句时间语义冲突、作者嘴替式说明对白、以及无人物动机的整齐对白 ping-pong。因此 V3 增加独立 `V3-G6D`。

核心文件：

```text
rules/scene-to-speech-microcraft.md
modules/dialogue-trigger-anchor.md
modules/local-logic-ledger.md
templates/microcraft-dialogue-audit-template.md
```

Scene-to-Speech 的基础模型是：

```text
scene state
→ trigger
→ perception / non-speech reaction
→ why speak now
→ in-scene goal
→ listener knowledge
→ information carrier
→ speech
→ aftereffect
```

### Fresh regression 的真实结果

- Phase340 V1：有效能力主要集中在 local semantic logic，fresh promotion 未通过。
- Phase341 V1.1：固定 machinery、6 个规则 blob 与正文 hash 全部命中的 fresh/no-hint 实稿回归，将预注册三类失败提升到 **2/3**：时间语义链和空转 ping-pong 被独立抓到，但预注册的公共背景作者嘴替信息包仍漏掉。
- 同一 V1.1 evaluator 还把一个直接回答问题的第一手人物趣闻判成 mouthpiece，说明仅靠 listener practical need 会误杀真实闲聊。

因此 V1.1 没有晋级，也禁止通过重复 fresh 尝试碰运气。

### V1.2：候选全量收集 + 社交趣闻保护

V1.2 增加两条关键机制。

**一、先收集全部高风险候选，再判断。** PRE_DELIVERY / REGRESSION 模式必须 inventory：

- 3+ 独立事实信息包；
- 当前事件 + 时间 + 听者本人角色 + 奖励/价格 + 传闻 + 外来者数量/位置等公共背景包；
- 对听者本人任务/身份的重复说明；
- `问 → 反问 → 追问 → 包袱` 修辞梯子；
- 普通前段/中段的设定交代；
- 可能属于第一手趣闻/关系闲聊的对白。

这些候选不能只抽样。候选清单不完整，G6D 不能 PASS。

**二、区分公共背景嘴替与活人会讲的趣闻。**

必须区分：

```text
PUBLIC_BACKGROUND_ORIENTATION
SOCIAL_ANECDOTE_OR_RELATIONSHIP_STORY
TASK_OR_CONFLICT_INFORMATION
MIXED
```

人物被问到某个熟人后，讲一段亲眼见过的趣事，即使细节不是任务必需，也可以因为闲聊、共同印象、人物声音和关系而成立；不能因为“listener 不需要每个细节”就自动判 mouthpiece。

反过来，如果一句话把“今天发生什么、你在里面做什么、奖励多少、消息传多广、来了多少外人”等当前剧情设定打包告诉一个已经知道自己任务的听者，则必须逐项检查 exact-bundle no-reader counterfactual；一条真正的新信息不能自动救活周围几条读者科普。

V1.2 继续保留：speaker goal 必须有正文证据、atomic information claims、per-turn state delta、unsupported bluff 不得救场、action-beat spam 不是 grounding。

高优先失败码：

```text
DIALOGUE_CANDIDATE_HARVEST_INCOMPLETE
TEMPORAL_SEMANTIC_CHAIN_FAIL
AUTHOR_INFORMATION_MOUTHPIECE_FAIL
DIALOGUE_PINGPONG_TEMPLATE_WITHOUT_CHARACTER_MOTIVE
CRITICAL_DIALOGUE_HAS_NO_TRIGGER_OR_GOAL
ACTION_BEAT_SPAM_AS_FAKE_GROUNDING
```

回归套件：

```text
benchmark/microcraft/dialogue-regression.v1.json
benchmark/microcraft/dialogue-regression.v2.json
benchmark/microcraft/dialogue-regression.v3.json
```

V3 增加“公共背景 bundle 必抓”与“第一手社交趣闻不能误杀”的正反例。所有 JSON 只固定期望分类，不代表脚本已经自动理解任意小说语义。

当前 source-book microcraft 证据已完成三书同 schema 覆盖：BOOK-01《射雕英雄传》、BOOK-02《诛仙》、BOOK-03《盗墓笔记【壹】》各 30 个 raw-derived abstract Scene-to-Speech 样本。BOOK-01 上传源已与冻结 canonical repaired source 做 byte-exact SHA-256 校验并覆盖 40 回。三书证据支持 Scene-to-Speech 架构，但不能替代 fresh 实稿回归或外部真人盲测。

## Optional Novel DNA Router

V3 支持一个**默认关闭**的结构级 Novel DNA Router。它不是新的写作模板，也不会因为某条规则是 Global 就自动套到所有故事。

入口：

```text
rules/novel-dna-routing.md
templates/dna-call-record-template.md
```

Router 只在已经有具体 `problem_evidence`、而普通因果/连续性/局部语义/dialogue grounding/callback/setup-payoff/场景功能/情绪兑现/人物选择等更简单修复仍不足时才允许运行。Global / Cross-Book / Book-level 是证据层级，不是自动优先级；同一因果谱系只调用当前最高批准 successor，所有层级共享同一调用配额。

当前首个系统级 Global Novel DNA：

```text
GN-VDNA-01
RECURRING_NARRATIVE_ASSET_GAINS_CAUSAL_MEANING
```

它仍然 DEFAULT OFF。`Global` 只表示当前小说蒸馏系统内最高层级的可复用机制，不表示普遍文学定律。

Phase 310 的 12-case 合成结构回归为 `PASS_WITH_SCOPE_LIMITATION`；当前生产状态只到 **`OPTIONAL_BOUNDED_PRODUCTION`**。真实稿件调用仍必须保存 call record、脱敏 `production_use_id`、前后版本引用和 post-use validation；若复杂度/公式化风险上升或目标问题变差必须回滚。公开 GitHub 只记录脱敏元数据，不记录真实稿件正文。

生产治理：

```text
docs/NOVEL_DNA_BOUNDED_PRODUCTION_GOVERNANCE_V1.md
state/production/NOVEL_DNA_ROUTER_PRODUCTION_GOVERNANCE_V1.json
state/production/NOVEL_DNA_REAL_USE_LEDGER_V1.jsonl
```

## 核心模块

### 因果证明器

```text
前置事实 → 人物选择 → 未选简单方案及原因
→ 立即后果 → 新限制 → 逼出的下一场
```

### 情绪与兑现账本

```text
谁让读者压抑 → 读者在等什么 → 何时部分偿还
→ 最终如何偿还 → 权力/关系/选择/利益/代价发生什么变化
```

### 恨感与共情测试

恨感依赖主动伤害、获益、推责和加码，不依赖旁白骂人。共情依赖普通欲望、缺点、代价和选择，不依赖悲惨履历堆叠。

### Dialogue Trigger Anchor

V1.2 先建立 candidate inventory，再逐项检查 `why now / speaker goal evidence / listener knowledge / exact-bundle no-reader / atomic claims / per-turn delta`。公共背景说明与社交趣闻使用不同判别路径，避免既漏嘴替、又把人物生活感剪死。

### Local Logic Ledger

记录 `anchor → semantic relation → inherited scope → later fact`，用于抓跨列表、钱、物件、解释和代词传播的时间/状态冲突。

### 个人审美指纹

个人样本必须保存在私有环境；公开仓库只提供方法和空白模板。样本为空时不得冒充已学会个人声音。

## 真实的读者复核

只有新上下文、子代理或真人反馈才可称“独立读者”。同一上下文中扮演多人只能称“模拟读者镜头”。Fresh Independent Cold Read 提供阅读反应证据，但不能代替 G6D 的局部语义/对白真值审查。

## 去 AI 原则

去 AI 默认最后执行，每轮最多处理五个高影响模式。G6D 失败时不得进入去 AI：作者嘴替不能靠润色变成 PASS，无触发对白不能靠添加动作变成 PASS。

## Novel Distillation Benchmark V1

`benchmark/` 是独立验收层，不替换 V3。它固定 100 分评分维度、Source / Coverage / Evidence / Holdout / Reproducibility / Experiment / Review / License 硬门禁、Development / Style Holdout / Future Holdout 隔离、同输入同预算直接比较，以及不提升就回滚的 Regression Gate。

入口：

```text
benchmark/README.md
benchmark/TEST_PLAN_V1.md
benchmark/config/scoring.v1.json
benchmark/config/upstreams.v1.json
```

结构验证：`python scripts/validate_benchmark.py`

Microcraft regression 是该体系之外的局部永久回归子套件，不与 100 分评分相加。

## Novel Preprocessor V1（本地预处理）

STEP-01 是与文学分析严格分离的本地预处理层，负责 TXT、EPUB、DOCX、Markdown、可提取文本 PDF 的解析，保守机械清洗、章节候选检测、确定性 ID / SHA-256、基础去重、私有结构化章节输出和 private-first Manifest，不调用在线 AI/API，也不生成文学分析或 Novel DNA。

固定工作目录：`E:\蒸馏小说`。Git 仓库：`E:\蒸馏小说\repo`；私有原书/结构化全文/缓存/日志：`E:\蒸馏小说\_private`。

命令行入口：

```powershell
python scripts/preprocess_novels.py --repo-root E:\蒸馏小说\repo --private-root E:\蒸馏小说\_private
```

工程与隐私验证：

```powershell
python -m unittest discover -s tests -v
python scripts/validate_private_boundaries.py
python scripts/validate_step01.py
```

本地导出桥：

```powershell
python scripts/export_chatgpt_packets.py --private-root E:\蒸馏小说\_private --work-id wrk_xxx
```

详细说明见 `docs/PREPROCESSOR_V1.md`、`docs/EVIDENCE_CONTRACT_V1.md`、`docs/CHATGPT_PACKET_EXPORT.md`。

## 安装

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.agents/skills/novel-writing-master
```

Claude Code 可安装到 `~/.claude/skills/novel-writing-master`，GitHub Copilot CLI 可安装到 `~/.copilot/skills/novel-writing-master`。

## 验证

```bash
python scripts/validate_skill.py
python scripts/validate_microcraft_regression.py
```

结构验证通过不等于小说质量通过。小说质量和 G6D 语义判断仍必须由具体文本证据证明。

## 版权与隐私

- 只学习抽象技法，不复制第三方作品。
- 不模仿在世作者可识别的个人风格。
- 不把私有原书、完整提取文本、真实稿件正文或个人审美样本提交到公开仓库。
