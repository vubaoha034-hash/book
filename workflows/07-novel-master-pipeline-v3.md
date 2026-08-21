# 小说总控生产流程 V3

## 目标

用可定位的文本证据替代自评分和假独立审稿，完成从故事设计到最终正文的闭环。

## 建议项目文件

```text
作品名/
├── 00-story-contract.md
├── 01-causal-ledger.md
├── 02-emotion-payoff-ledger.md
├── 03-hate-empathy-evidence.md
├── 04-character-and-continuity-state.md
├── 05-scene-plan.md
├── 06-draft.md
├── dna-call-record.md        # 仅实际进入 DNA Router 时创建
├── reviews/
│   ├── opening-cold-read.md
│   ├── reader-evidence.md
│   └── continuity-report.md
├── revision-ledger.md
└── final.md
```

## Phase 0：锁定任务边界

记录平台、篇幅、目标读者、目标情绪、用户指定保留项、允许改变项和禁止改变项。

用户说“全部推倒”时，旧稿只作为失败证据，不沿用原场景顺序。

Novel DNA 在本阶段关闭，不从 DNA 模板生成题材、主角、世界观或结局。

## Phase 1：故事契约

产出：

```text
一句话读者承诺：
一句话主线：
主角普通欲望：
持续阻力：
失败具体损失：
为什么必须现在：
核心关系：
不可逆事件：
高潮选择：
结局兑现：
```

主线需包含“谁要什么、谁阻止、失败失去什么、为何现在”。主角没有主动选择时不通过。

Novel DNA 仍关闭；先让故事契约独立成立。

## Phase 2：三本账

分别读取：

- `modules/causal-proof-engine.md`
- `modules/emotion-payoff-ledger.md`
- `modules/hate-empathy-test.md`

完成：

1. 关键场景因果链。
2. 主要情绪债及偿还位置。
3. 主角共情和伤害者恨感证据。

三本账出现阻断项，先改大纲，不写全文。

### Optional DNA Routing Gate（不新增 Phase 编号）

只有三本账完成后、且仍存在可定位的结构问题时，才允许读取：

```text
rules/novel-dna-routing.md
templates/dna-call-record-template.md
```

执行顺序固定为：

```text
problem_evidence
→ 更简单的 V3 修复是否足够
→ DNA invocation gate
→ 同谱系去重
→ 跨层级共享配额
→ expected_change / complexity_cost / formula_risk / exit_criteria
```

以下任一情况直接不进入 `APPLIED`：

- 没有具体 `problem_evidence`；
- 因果、连续性、普通 callback / setup-payoff、场景功能、情绪兑现或人物选择等简单修复已经足够；
- 没有退出条件；
- 只是因为某条 DNA 是 Global 或来自名作而想套用。

Global / Cross-Book / Book-level 是证据层级，不是自动优先级。同一因果谱系只允许当前最高批准 successor 用于实际调用；当前 `GN-VDNA-01` 是 `CBDNA-C02-V2` 的应用 successor，二者不得同时计入调用配额。

未进入 Router 的任务不创建 `dna-call-record.md`。

## Phase 3：人物与连续性状态

读取：

- `modules/character-pressure-test.md`
- `modules/continuity-editor.md`

记录人物知识、欲望、恐惧、错误认知、现实方案、物件、时间、空间和世界规则。

规则必须在使用前建立触发条件、限制和成本。

若 Optional DNA Routing Gate 已有 `APPLIED` 记录，只保留该调用对人物/连续性状态真正需要保护的约束，不加载完整 DNA 注册表。

## Phase 4：场景计划

每场从三本账抽取：

```text
本场要偿还 / 加重哪笔债：
本场因何发生：
人物目标：
冲突双方要保住什么：
实际选择：
立即后果：
新限制：
下一场压力：
```

连续两场重复同类压力时，合并、删除或改变压力形态。

只有已经明确 `APPLIED` 的 DNA call 才可以进入场景计划，而且它只能约束被证明的问题，不得替代人物目标、冲突和因果设计。所有 DNA 层级共享总配额：单场 Primary 最多 1；章节/叙事弧 Primary 总计最多 2；整本 Primary 总计最多 3。

## Phase 5：分场正文

每次只携带当前场景必要上下文。写完立即记录新事实、知识、物件、关系、规则和未回收问题。

不要边写边运行去 AI 清单。不要为了显得有爽点临时加入强权人物、证据或能力。

若当前场景存在 active DNA call，正文上下文最多携带：DNA ID、问题证据、选定动作、必须保护项、预期变化和退出条件。禁止加载完整 DNA 注册表、来源书分析或全部 invocation gates。

## Phase 6：开篇冷读

读取 `modules/opening-retention-reader.md`。不知道后文解释地检查第一屏、前 300 字和第一场。

输出精确滑读、困惑、失信和停止位置。失败只改对应范围，再验证与后文的因果连接。

## Phase 7：读者证据

读取 `modules/beta-reader-panel.md`。

- 新上下文、子代理或真人：标注“独立读者”。
- 同一上下文多镜头：标注“模拟读者镜头”。

保留精确位置、未满足期待、记住的内容和必须保护的优点。删除平均分。

## Phase 8：逻辑、连续性与兑现复核

逐项核对：

- 因果表是否与正文一致。
- 简单方案阻断是否真正写进正文。
- 主要情绪债是否兑现。
- 主角是否实际付出代价。
- 伤害者后果是否对应其伤害。
- 人物知识、时间、空间、物件和规则是否连续。

若存在 `APPLIED` DNA call，只验证该记录声明的 `expected_change`、复杂度成本、公式化风险和 `exit_criteria`。没有声明调用的 DNA 不进入复核清单。若预期变化没有发生，或结构成本大于收益，允许 `ROLLED_BACK`，不能因为它是 Global 而强行保留。

## Phase 9：定向修改

修改总账一次最多开放五个高影响问题。顺序：

```text
主线 / 结局
→ 因果 / 简单方案
→ 人物选择
→ 情绪兑现
→ 连续性
→ 留存与场景功能
```

每改一处，复核它影响的后续事实和场景。不在同一轮顺手全文润色。

## Phase 10：个人审美与去 AI

结构稳定后读取 `modules/aesthetic-fingerprint.md` 与行文模块。

先识别当前稿相对认可/拒绝样本最明显的二至五个偏离，再做最小修改。样本为空则只执行审美基线并说明限制。

Novel DNA 在本阶段关闭，不控制句式、措辞、节奏表面特征或人物声音。

## Phase 11：最终复核

必须确认：

- 没有开放的阻断问题。
- 开篇读者问题与结局回答属于同一故事。
- 高潮由前文选择和代价逼出。
- 主要情绪债得到真实偿还或记录为有意风险。
- 修改位置没有产生连锁冲突。
- 去 AI 没有改变事实、抹平人物声音或删掉必要余波。
- 若调用 Novel DNA，所有保留的 `APPLIED` 记录都已达到退出条件，且没有同谱系双计数。

最终不需要虚假的高分。交付正文，并用简短证据说明哪些关键问题已经关闭、哪些风险被有意保留。
