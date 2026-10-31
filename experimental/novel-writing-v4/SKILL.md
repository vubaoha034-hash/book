---
name: novel-writing-master
description: 中文小说创作与去AI味的候选 V4 路由。优先执行最新小说项目状态和真人阅读门；仅在明确授权的隔离测试中调用短而可执行的“人物决策→场景冲突→干净初稿→三层诊断→冷读”链。来源：wgwtest/novel-writing 的轻适配设计，Oh Story按需参考。
---

# 小说写作候选 V4｜Thin Adapter

**身份：** `CANDIDATE_ONLY`，尚未通过真人A/B，不得覆盖仓库根目录生产版 `SKILL.md`，不接管既有任务或在真实会话声称已安装。最新权威仍是 `START_HERE.md`、`AGENTS.md`、`MAINLINE.md`、`state/project_state.json` 与 `state/continuity/LATEST_CHECKPOINT.json`；同提交锁定后运行 `scripts/verify_current_state.py`。新历史/研究文件绝不重置业务检查点。

## 一句话目标
让具体人物因自己的利益、知识和关系而选择行动；真实行动改变下一步安排；读者自然想知道接下来如何，而不是AI照大纲传话。

## 路由（只按需加载）
- 设计：只读 `modules/character-pressure-test.md` 的目标、底线、知识与方案，`modules/causal-proof-engine.md` 的因果风险；必要时参照 `modules/continuity-editor.md`。
- 写作：只读冻结的单场 `writer_packet` 和至多一段同类且已被真人认可的原创正例。**严禁**接收审稿结论、禁止词表、Phase失败摘要、全套研究技巧、八步固定动作。
- 审查：独立上下文调用 `modules/opening-retention-reader.md`；事实审查检查连续性；审稿人才可以按需调用 `modules/line-editor-deslop.md`。
- 收束：保存原始提示、正文版本/哈希、评审报告和准确的真人反馈。模型评分只算诊断，不等于真人认可。

## 最小写作步骤
1. **故事承诺（编辑）**：说清读者会关心谁、等待什么事，以及失败会失去什么；不以套路和反转数量代替故事。
2. **人物决策（编辑）**：每个关键人物仅写 `眼前想要/私下顾虑/手上筹码/知道与误解/底线/不选最容易办法的原因`。信息缺失可报告，不凭空加故事核心事实。
3. **场景冲突（编辑）**：写清起因→两种相反打算相撞→必要行动→一方的决定或关系/权限/安排真实变化→后果。事件可不完全预先排列；不要冻结镜头动作与台词。
4. **独立写作（writer）**：只给下方一页作家包；保持人物说话的意图，不做一问一答设定播报。不强制每句话配动作；允许自然的长短句、沉默、内心反应和日常细节。只生成一份正文并冻结。
5. **三级修稿（editor）**：先核人物选择与因果→再核详略/叙事重心→最后去机械语言。不能靠删除词汇、堆物件或制造口语碎句伪装真人；若结构不足，退回第2/3步，不偷偷增加证据和世界规则。所有改稿有父本、差异及保护项。
6. **冷读（reader）**：评审不看作者意图/结局/旧失败标签。找第一处想继续、第一处困惑和停读位置。AI冷读仅提供诊断；真人愿不愿继续、人物像不像人是晋升依据。
7. **结算（coordinator）**：版本绑定的 `PASS/PARTIAL/FAIL/UNKNOWN`，停止位置、实际调用、保护的接受范围、下一合法动作写入血统。不得以 `9.0`、AI多数票、技术校验或新文件存在替代文学认可。

## Writer packet
最小格式在 `writer-packet-template.md`。写作人只见 `[世界与前场事实][每人当下目标与知识][对立意图][本场真实限制][必须保持的终点][输出范围]`，其余内容都在编辑/协调者上下文。

## 不能进入生产的模块
以 `module-routing.json` 作为候选唯一路由清单；无授权或缺证据时使用 `REFERENCE_ONLY`，不得从历史快照自动升级。旧任务强制八步、万能禁词、段长百分比、朱雀检测分数、同上下文多AI虚拟读者投票均 `EXCLUDED_FROM_WRITER`。旧文件保留审计，不物理删除当前权威依赖。

## 上游与知识产权
主参考 `wgwtest/novel-writing@838729695148008d42c01bd7c3c0c1a5c15de830` MIT；按需研究 `zenstory-ai/oh-story-claudecode@cc6397f2b07179262287f4ca358d281b16205765` MIT；`huahuakandaima/human-novel-writer@3e74b95d014923525e0bd19a38203e724152fe54` MIT 仅借鉴人物卡，不采纳检测器/机械阈值为文学门。本文是自写薄适配，不直接复制受保护正文；实际拷贝上游源码时必须带许可证和原著作权声明。

## 晋升与回滚
先让原版最小方案和现有V3在同事实、同限制下做有界比较，两种压力场景分别复测。旧方法是控制条件，不能凭预期改写。真人有定位的持续偏好、事实无阻断，才给范围内 `PROMOTE_CANDIDATE`；失败则 `REJECT` 并关闭候选路由，原文/回执不擦除。跨聊天运行需要安装/选择并验证实读本Skill，不保证宿主自动注入。

执行合同：`docs/NOVEL_METHOD_UPSTREAM_LINEAGE_EXECUTION_CONTRACT_20261031.md`
血统：`state/lineage/NOVEL_METHOD_UPSTREAM_20261031.json`
