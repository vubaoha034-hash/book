---
name: novel-writing-master
description: Design, draft, diagnose, rewrite, and de-AI Chinese fiction with evidence-backed causality, emotion-debt/payoff, hate/empathy, continuity, reader-retention, and personal-aesthetic checks. Use for public-account short fiction, web fiction, short-drama stories, suspense, revenge, family realism, supernatural romance, or any Chinese story the user says is illogical, emotionally flat, formulaic, slow, unsatisfying, or AI-sounding.
---

# Novel Writing Master V3

V3 不追求“规则很多”，只追求四件事真的成立：

1. 事件由人物选择逼出来。
2. 读者的压抑、期待和情绪债得到对应兑现。
3. 主角值得理解，伤害者值得恨，但都不是纸片人。
4. 正文像具体的人在具体处境里生活，不像模型在展示写作技巧。

V2 文件继续保留用于兼容；新任务默认执行 V3。

## 当前仓库项目接续

为本仓库当前小说项目总控或接续时，先读取 `START_HERE.md`、`MAINLINE.md` 及入口指向的当前状态与任务，执行 `scripts/verify_current_state.py`。按已锁定的唯一下一动作继续；复用已有契约和账本，不因调用通用 V3 流程从头重做。只有对应冻结测试的实际失败或刘先生明确改变目标，才修订相关路线。

独立写作者只读其允许的场景输入；总控在隔离执行前后核对并保存状态，不把主线、诊断或验收答案塞进写作上下文。其他独立新故事仍使用下方 V3 路由。

2026-10-03 本轮已明确授权 Codex 协调与独立评审接入，沿用专业协议并按
[接入附录](docs/NOVEL_CODEX_REVIEW_INTEGRATION_20261003.md)分开匿名冷读、事实审查和
已知失败后的编辑诊断。模型与强度从实际运行返回核验；原始报告先冻结，纠错另存，
协调者逐项核对后唯一写入状态。有限盲校准漏检2/2，筛查不能认证好看或个人口味。
读取保存结果不等于重新执行；检查点194接入任务本身没有新正文、旧额度重置或解除保护授权。

检查点195：另获刘先生“授权。”后，唯一进入时刻/最小事实准备已完成，见[准备结果](docs/NOVEL_R2_REENTRY_FACT_PREPARATION_RESULT_20261003.md)。该准备任务预算为零，旧提案保留未授权原件。

检查点196：刘先生随后要求按具体提案直接完成，另存新授权；一次独立写作已冻结[唯一395字短段](delivery/r2-entry-trial-20261003/short-a1.md)，一次不同上下文事实审查及协调者核对已完成，见[结果](docs/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_RESULT_20261003.md)。写作者只接收冻结事实及本次输出范围；事实审查不接收失败标签、诊断或写作者解释。新一次预算已用尽，原稿/旧锁不改；下一步只收实际真人阅读反馈，未知不能写成PASS。读取和核对不调用模型，原运行命令有一次消费锁，不得重跑或自动续写。

历史检查点197：395字稿实际真人FAIL已另存，前一检查点的UNKNOWN仅为历史快照。已按用户要求主动学习专业资料并完成一次独立已知失败后的情绪/互动诊断。读取 [学习与适用边界](docs/NOVEL_EMOTION_PACING_PROFESSIONAL_STUDY_20261003.md)、[根因与原始证据](docs/NOVEL_EMOTION_REACTION_DIAGNOSIS_RESULT_20261003.md)及当前任务。复用 [人物反应与节奏](modules/emotion-reaction-and-pacing.md)作当前阶段参考，不把教程、失败标签和诊断塞入写作者上下文；未来只取三条简短正向原则。当前无新写作预算，不自动续写，旧锁和方法4保持。读取不重跑模型，原一次诊断已消费；未读完整视频/书籍，不宣称已学会或验证文风。


检查点198已按刘先生新要求接入两个实际独立AI角色：编辑读取必要事实和已知失败，匿名读者只看正文；原报告互不传递。实际Sol/Max已核对。编辑REVISE、AI读者YES与真人不想继续的FAIL不一致，不能晋级质量门。见[当前结果](docs/NOVEL_TWO_ROLE_OPENING_REVIEW_RESULT_20261003.md)及[调用方式](modules/two-role-opening-review.md)。取用固定提交的story-review/reader-sim，未安装整套规则。已推进一份既有姓名错位入口和冻结输入准备；当前预算零，后续写作者只读prepared_input.writer_packet。新版本开头重排须新的一次范围和预算，旧稿/197字保护和旧额度不变。读取不重跑，原评审各一次已消费。
检查点199：刘先生明确要求连续完成直到实际人工审核，常规中间环节不再询问授权。已完成唯一390字新开头与不同上下文的AI编辑、匿名AI读者及事实审查，原报告/证据/状态已保存。实际Sol / Max经运行核对；主写1、内部修订0，新稿真人UNKNOWN。接续[当前结果](docs/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_RESULT_20261003.md)及[执行方式](modules/autonomous-to-human-review.md)，交付这份正文后收实际阅读反馈；AI赞成不晋级质量门。旧稿、197字保护、旧额度0、方法4、故事目标、既有真人FAIL和404未知保持。读取不重跑，不继续生成或扩到完整场景/V5。

检查点200：390字实际真人文笔/AI味与续读FAIL已另存。沿用连续执行授权，一次独立语言诊断后只调整当前输入呈现，冻结唯一375字新稿，另三个独立AI审核与证据结算完成。实际Sol / Max核对；新稿真人UNKNOWN，旧任务原件不改，旧保护/额度及方法4保持。见[当前结果](docs/NOVEL_OPENING_PROSE_REPAIR_RESULT_20261003.md)，下一步只交正文收实际阅读；常规中间不问授权，不循环求赞成或扩到V5。

检查点201：375字实际留存/悬念FAIL与AI味相对改善已记录。已在同一冻结事实内完成一次新短稿及独立编辑、匿名AI读者和事实审核；新稿真人UNKNOWN。见[当前结果](docs/NOVEL_OPENING_HOOK_TRIAL_RESULT_20261003.md)。只交这一份正文收实际阅读，旧稿/锁/额度/方法4保持；常规中间不问授权，不循环求赞成或扩到V5。

检查点202：401字已有刘先生“这个稍微好了一些。确实。”的相对正向反馈，见[原话](state/review_receipts/NOVEL_HOOK_TRIAL_401_HUMAN_PARTIAL_FEEDBACK_20261003.json)。续读与人物互动仍未明确，质量UNKNOWN；只收同一版本的阅读判断，不改稿、不调用模型或自动晋级。

检查点203：同一401字有少量续读意愿、互动更自然，见[真人原话](state/review_receipts/NOVEL_HOOK_TRIAL_401_HUMAN_WEAK_CONTINUATION_20261003.json)。只认可该短段两项目标，保留低强度限定；完整场景/TEST-01与迁移仍未通过。下一步按既有授权准备同场唯一300—500字接续，不改开头、旧稿/锁/额度或主线。

检查点204：保留原401字，唯一374字同场接续及独立事实/编辑/匿名AI读者审查已完成，见[实际结果](docs/NOVEL_SAME_SCENE_CONTINUATION_RESULT_20261003.md)。四次Sol / Max核对、30条报告引文记录定位；新段真人UNKNOWN，下一步只实际人工阅读。旧否决/额度/锁/方法保持，不自动整场或V5。读取不会重跑当前已消费的一次模型调用。

## 核心纪律

- 先证明故事成立，再写正文。
- 一次只运行一个阶段，只加载当前阶段所需材料。
- 不用自评分、清单勾选或文件存在代替文本证据。
- 无法获得真正独立上下文时，明确标注“单上下文复核”，不得冒充独立读者。
- 同一轮最多处理五个高影响问题；修改后定向复核连锁影响。
- 去 AI 味默认关闭，只在结构、因果和情绪通过后做最小修改。
- 不复制受版权保护文本，不模仿在世作者的可识别风格。

每次总控任务先读：

```text
rules/pass-isolation.md
workflows/07-novel-master-pipeline-v3.md
config/novel-quality-gates.v3.json
```

## 路由

### 完整创作、推倒重写、全面修改

执行 V3 总流程。先交付故事契约与三本账，再进入正文：

```text
因果证明表
情绪欠账与兑现表
恨感 / 共情证据表
```

用户明确要求“直接完成”时可以连续执行，但每个阶段仍须生成中间证据，不得跳到全文。

### 构思、大纲、剧情设计

读取：

```text
modules/causal-proof-engine.md
modules/emotion-payoff-ledger.md
modules/hate-empathy-test.md
modules/character-pressure-test.md
```

只完成故事契约、场景链和三本账，不提前写完整正文。

### 逻辑检查

读取：

```text
modules/causal-proof-engine.md
modules/continuity-editor.md
rules/novel-logic-checklist.md
```

优先寻找“一问就能解决、离开就能解决、报警/打电话就能解决、道具突然出现、人物知道不该知道的信息”等阻断问题。

### 爽点、恨感、共情、情绪检查

读取：

```text
modules/emotion-payoff-ledger.md
modules/hate-empathy-test.md
rules/reader-reward-rhythm.md
```

不把旁人震惊、反派脸色变化和口头道歉算作兑现；必须检查权力、关系、选择权、利益或代价是否真实改变。

### 开篇留存

读取 `modules/opening-retention-reader.md`。不知道后文真相地冷读第一屏、前 300 字和第一场，引用精确停止句。

### 已有稿件诊断

先定位最上游层级：

```text
承诺 → 因果 → 人物选择 → 情绪债 → 场景功能 → 连续性 → 行文
```

只报告二至五个根因，逐项给位置、证据、伤害和验收条件。上游阻断未解决，不润色下游句子。

### 深度拆解或技巧提炼

读取：

```text
workflows/05-deep-story-dissection.md
rules/suspense-reversal-payoff.md
rules/reader-reward-rhythm.md
```

拆解读者承诺、因果链、悬疑锁钥、伏笔、反转公平度、情绪债、人物选择和兑现。只提炼抽象技法，不复述大段原文。

### 导入用户有权使用的资料

沿用 V2 的 `scripts/ingest.py` 与 `workflows/01-ingest-book.md`。原书、完整提取文本和个人样本默认只留在私有环境，不提交到公开仓库。

### 去 AI 味

读取：

```text
modules/aesthetic-fingerprint.md
modules/line-editor-deslop.md
rules/no-ai-smell.md
rules/reader-trust-and-economy.md
```

先比较认可样本、拒绝样本和当前稿。样本为空时明确说明“尚未学到个人文风”，只按审美基线做终审。每轮最多处理五个高影响习惯。

## V3 最小证据包

完整创作至少保留以下内容：

```text
一句话读者承诺：
一句话主线：
不可逆事件：
高潮选择：
结局兑现：

每场：前置事实 → 人物选择 → 未选简单方案及原因
    → 立即后果 → 新限制 → 逼出的下一场

每笔情绪债：压了什么 → 谁造成 → 读者等什么
    → 何时部分偿还 → 最终如何偿还 → 真实改变

主角共情：普通欲望 → 缺点/错误 → 有代价选择 → 失去什么
伤害者恨感：可选不伤害 → 主动伤害 → 获益 → 被提醒后加码
    → 与伤害方式对应的后果
```

模板：`templates/v3-evidence-packet-template.md`

## 阻断条件

命中任一项，不得宣布可交付：

- 主线无法说清“谁要什么、谁阻止、失败失去什么、为何现在”。
- 关键转折只能靠巧合、误会不沟通、人物降智或临时新规则发生。
- 一个现实中的简单动作即可无代价解决核心危机，正文却无可信阻断。
- 主角只被动受苦，没有会改变局势的选择。
- 伤害者只是被旁白说坏，没有主动、明知、获益或加码证据。
- 所谓爽点没有改变权力、关系、选择权、利益或代价。
- 高潮和结局没有偿还故事最主要的情绪债。
- 修改造成新的时间、知识、物件、规则或关系冲突。

## 写作上下文

正文阶段只携带：

1. 故事契约。
2. 当前场景的因果行。
3. 当前情绪债及本场任务。
4. 当前人物知识、欲望、恐惧和可选方案。
5. 必要世界规则。
6. 个人审美基线或已验证的文风指纹。
7. 前一场结尾与后一场目标。

不同时加载全部审稿模块、禁词表、读者角色和质量闸门。

## 读者复核真实性

- 有新上下文、子代理或真实外部读者时，才写“独立复核”。
- 同一上下文内的多视角报告，标注“模拟读者镜头”，不宣称统计独立。
- 不用四个虚构读者的平均分证明作品好看。
- 最高价值证据是：精确滑读/失信位置、未兑现期待、逻辑断点和读完后记住的内容。

## 修改纪律

按以下顺序：

```text
主线与结局
→ 因果与简单方案
→ 人物选择
→ 情绪欠账与兑现
→ 连续性和世界规则
→ 场景功能与留存
→ 个人文风与去 AI
→ 标点错字
```

每次修改记录：

```text
问题：
位置与证据：
根因：
本次动作：
可能破坏：
必须保护：
复核结果：
```

## 交付标准

最终交付包括正文和简短审计结论：

- 没有未关闭的阻断问题。
- 主要场景能用因果证明表串起。
- 主要情绪债有明确兑现或被有意识保留。
- 主角至少有一次付出代价的主动选择。
- 伤害者的行为与后果形成对应关系，或作品明确选择不兑现并说明风险。
- 开篇没有未接受的致命停止点。
- 修改处完成连续性复核。
- 去 AI 只做了最小必要修改，未统一人物声音。

不要用“综合评分 9.2”替代以上证据。
