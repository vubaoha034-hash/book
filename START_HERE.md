# 小说项目接管入口

<!-- UNIFIED_USER_INSTRUCTION_20261003 -->
## 最新用户执行偏好与总审核权限（2026-10-03）

- 本项目与统一指挥管理的其他项目一样，尽量使用 **GPT-6.1 Sol，Max 思考强度**。这项当前用户偏好优先于旧模型/思考强度默认值；实际模型与强度须从可观察的执行设置核对，无法使用时如实记录原因，不得只在提示词写名称就宣称已切换。
- 统一指挥负责审核、验收、调度和推进既有授权任务。**只有刘先生明确要求，才可改变项目主线目标或既定主线路线。** 测试失败、审稿意见、新资料、旧任务结束和审核者的个人判断，均不单独授权总审核者改主线；原协议内已经授权的有界修订继续按原范围执行。
- 该回执只更新上述执行偏好与审核权限；其后本轮Codex接入授权见下方当前检查点。当前任务、唯一下一动作、候选身份、已认可成果、预算、真人门和自动化暂停状态仍以本项目原生状态为准。模型偏好本身不要求切换 Chat/Work，也不启动或重跑业务。
- 本次指令与接续定位：`state/review_receipts/UNIFIED_COMMAND_USER_INSTRUCTION_20261003.json`。此回执不是第二个任务索引，也不宣称五个运行会话已经切换模型。
<!-- END_UNIFIED_USER_INSTRUCTION_20261003 -->

权威仓库：`vubaoha034-hash/book`，分支：`main`。项目：`novel-distillation`。先读取远端最新 HEAD，并把本次相关读取固定到同一提交。

依次读取 `AGENTS.md`、`MAINLINE.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json`、状态指向的当前主线任务、锁定回执和最新真人反馈。历史阶段文件不能覆盖这个顺序。

执行前运行 `python scripts/verify_current_state.py`；失败时先核对状态冲突，停止生成、重投或晋级。执行后在同一次变更中同步状态、检查点及任务回执，回读远端 HEAD 与实际文件。

唯一主线：`NOVEL-IMPROVEMENT-MAINLINE-V1`。保留原故事方向、契约和有效证据，停用冻结八步动作作为新写作者硬约束。方法变化依据冻结测试失败或用户明确范围变更；参见 `MAINLINE.md`。本次用户已明确授权项目外日常证据评审，见 `external_review_state`及其绑定协议/回执；不能把AI意见写成真人FAIL。

当前位置：检查点200。刘先生对390字稿实际否决：不愿继续，AI味从开头就很重，文笔特别别扭。已另存[原话及正确稿件绑定](state/review_receipts/NOVEL_AUTONOMOUS_OPENING_390_HUMAN_FAIL_20261003.json)，不编造精确停止句或新增情绪/机器人判决；前检查点199的UNKNOWN和AI报告保持原件。

本轮 `NOVEL-OPENING-PROSE-REPAIR-AFTER-HUMAN-FAIL-20261003-01` 沿用连续执行授权，完成一次独立已知失败后语言诊断、三项根因证据及范围核对、精简事实输入、一次独立写作的[唯一375字新稿](delivery/prose-repair-20261003/short-a1.md)，以及三个不同上下文的语言编辑、匿名AI读者、事实审查。[当前任务](state/tasks/NOVEL_OPENING_PROSE_REPAIR_AFTER_HUMAN_FAIL_20261003.json)、[实际结果及来源](docs/NOVEL_OPENING_PROSE_REPAIR_RESULT_20261003.md)、[结算](state/reviews/prose-repair-20261003/coordinator-settlement.json)、[待真人记录](state/reviews/prose-repair-20261003/pending-human-review.json)。五次实际Sol / Max已核对，35条引文定位、9项事实核对，原正文和报告未改写；内部修订0。AI审核放过前稿的事实已记录，新稿真人UNKNOWN，不认证已经改好。

当前唯一下一动作：`AWAIT_ACTUAL_HUMAN_READING_OF_ONE_PROSE_REPAIRED_OPENING`。只交375字正文并收是否愿继续、开头和文笔是否仍别扭。常规中间步骤不再问授权；旧稿、旧197字保护、旧RC3额度0、旧真人FAIL、404未知、方法4及故事目标/世界/结局保持。完整场景和V5未授权。读取与校验不会调用模型，当前五次run已消费，不能重跑或循环求赞成。[验证](state/review_receipts/NOVEL_OPENING_PROSE_REPAIR_VALIDATION_20261003.json)与[原生远端回读](state/review_receipts/NOVEL_OPENING_PROSE_REPAIR_REMOTE_SAVE_VERIFIED_20261003.json)分别记录实际证据。

上一检查点199：本轮 `NOVEL-AUTONOMOUS-REVIEWED-OPENING-TO-HUMAN-20261003-01` 已依据刘先生“你能不能不要停，直到我人工审核的时候再给我看就行。其他时候不用我授权。”连续完成一个已准备的新开头：一次独立主写、390字，三个其他独立上下文编辑/匿名读者/事实审核，实际Sol / Max已核对。报告直接回收，31条引用及9项冻结事实核对，原正文和报告未改写；内部修订0。新稿真人结果UNKNOWN，所有既有真人FAIL、404未知、旧197字保护、旧RC3额度0和方法4保留。常规中间准备与保存不重复索要授权。

当时的[原生任务](state/tasks/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_20261003.json)、[执行授权](state/review_receipts/NOVEL_AUTONOMOUS_TO_HUMAN_AUTHORIZATION_20261003.json)、[结果与限制](docs/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_RESULT_20261003.md)、[逐项结算](state/authoring/autonomous-opening-20261003/coordinator-settlement.json)和[待真人记录](state/authoring/autonomous-opening-20261003/pending-human-review.json)为历史快照。这份[390字稿](delivery/autonomous-opening-20261003/a1.md)已收到检查点200的实际否决，不原样重投；AI赞成不提前写成人工通过。

当时唯一下一动作：`AWAIT_ACTUAL_HUMAN_READING_OF_ONE_REVIEWED_NEW_OPENING`。下一项是实际人工阅读，无需再次问中间写作授权；[连续执行方式](modules/autonomous-to-human-review.md)与[机器偏好](rules/autonomy-until-human-review.json)已保存。读取结果和状态校验不调用模型，原四次run均已消费一次锁；未来有界同主线环节仍保存新具体任务，不重跑旧运行或循环寻求赞成。此权限不授权改变故事目标/世界/结局、新生活事实、V5、多个可见候选或后台任务，也不提供人工质量判决。

上一检查点198：本轮 `NOVEL-TWO-ROLE-OPENING-REVIEW-20261003-01` 按刘先生新要求完成两个独立AI上下文：专业编辑为已知失败后的局部诊断，匿名普通读者仅看正文。实际均为GPT-6.1 Sol / Max，分别约10.2/4.5分钟；报告互不传递。编辑REVISE，AI读者YES与刘先生明确没有续读欲望不一致，保留为诊断漏检，不能认证好看或口味。20处引文记录已定位，原报告未改；当前395字真人FAIL，不原样重投。

接续读[新任务](state/tasks/NOVEL_TWO_ROLE_OPENING_REVIEW_20261003.json)、[真实留存补充](state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_RETENTION_SUPPLEMENT_20261003.json)、[两份评审及范围结果](docs/NOVEL_TWO_ROLE_OPENING_REVIEW_RESULT_20261003.md)、[编辑原报告](state/reviews/two-role-opening-20261003/editor.raw.txt)、[AI读者原报告](state/reviews/two-role-opening-20261003/reader.raw.txt)和[逐项结算](state/reviews/two-role-opening-20261003/coordinator-settlement.json)。已取用固定提交的story-review与reader-sim，读者反应与编辑诊断分开；[来源及实际阅读范围](state/learning/two-role-opening-20261003/sources.json)、[可执行方式与限制](modules/two-role-opening-review.md)。读取这些文件和校验不调用模型，原两次run均已消费。

当时唯一下一动作：`AWAIT_ONE_NEW_BOUNDED_WRITING_BUDGET_FOR_REVIEWED_OPENING_REENTRY_INPUT`。审核后已完成[一个入口与输入](delivery/two-role-opening-20261003/prepared-opening-input.json)：从现有合同姓名被罗钧看到的时刻进入，同一第二场、无新生活事实；[唯一短稿提案](state/tasks/NOVEL_REVIEWED_OPENING_ONE_SHORT_PROPOSAL_20261003.json)拟一份300—500字。新预算当前0，评审完成不自动授权写作；以后仅发writer_packet字段，不发报告、失败标签或答案。旧RC3额度0、旧197字原稿不解锁、V5与后台任务不授权。原404未知、旧448原否决范围、方法4与故事目标保留。当前认可的连续前场正文未建立，精确停止句仍未知。

上一检查点197：本轮 `NOVEL-EMOTION-REACTION-AND-PACING-LEARNING-20261003-01` 已保存刘先生对395字稿的实际否决：AI味重、情绪平、互动像机器人。已主动阅读专业作者课程实录、网文作者访谈、官方讲座笔记、书籍公开引言和固定提交的场景/文字技能，完成一次独立GPT-6.1 Sol / Max的已知失败后诊断、8处引文及3个窗口引文核对、方法与精简创作原则准备。方法4、原故事与全部旧锁/额度保持；本轮没有新正文。

接续先读[完整真人反馈](state/review_receipts/NOVEL_R2_ENTRY_SHORT_A1_HUMAN_FAIL_20261003.json)、[学习授权](state/review_receipts/NOVEL_EMOTION_PACING_LEARNING_AUTHORIZATION_20261003.json)、[原生任务](state/tasks/NOVEL_EMOTION_PACING_LEARNING_20261003.json)、[专业学习及实际阅读范围](docs/NOVEL_EMOTION_PACING_PROFESSIONAL_STUDY_20261003.md)、[两个根因与结果](docs/NOVEL_EMOTION_REACTION_DIAGNOSIS_RESULT_20261003.md)、[原始诊断](state/reviews/emotion-learning-20261003/diagnosis.raw.txt)、[协调者结算](state/reviews/emotion-learning-20261003/coordinator-settlement.json)及[结果回执](state/review_receipts/NOVEL_EMOTION_PACING_LEARNING_RESULT_20261003.json)。可复用[人物反应与节奏](modules/emotion-reaction-and-pacing.md)供本阶段参考，未来写作者只取[三条原则](delivery/emotion-learning-20261003/craft-capsule.json)和冻结事实，不加载失败分析或审核答案。

当时唯一下一动作：`AWAIT_NEW_EXPLICIT_BOUNDED_WRITING_BUDGET_FOR_PREPARED_EMOTION_REACTION_TRIAL`。[唯一具体后续提案](state/tasks/NOVEL_EMOTION_REACTION_ONE_SHORT_PROPOSAL_20261003.json)为同一场的一份300—500字短段，处理私人冲击怎样改变回应及当前信息节拍；提案预算未授权，当前0。395字真实FAIL、旧448字原有FAIL、原404字UNKNOWN分别保留，精确停止句和继续欲望直接答复不补造。资料阅读与AI解释均不能证明质量改善；没有新正文、替换句、旧额度恢复、旧197字解锁、V5或后台任务。

上一检查点196：`NOVEL-R2-REENTRY-ONE-SHORT-TRIAL-20261003-01` 当时完成[唯一395字正文](delivery/r2-entry-trial-20261003/short-a1.md)、不同上下文事实审查与协调者核对；FACT_CLEAR和真人UNKNOWN是当时的冻结快照，不改写。见[原结果](docs/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_RESULT_20261003.md)。当时唯一动作 `AWAIT_ACTUAL_HUMAN_READING_OF_R2_ENTRY_SHORT_A1` 已由本次实际反馈结清，当前不再等首次判决，也不原样重投。新一次预算已用尽；旧稿、原报告、运行记录与[远端保存回执](state/review_receipts/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_REMOTE_SAVE_VERIFIED_20261003.json)原样保留。

上一检查点195：`NOVEL-R2-REENTRY-FACT-PREPARATION-20261003-01` 已核对12处前场/冻结事实证据，完成唯一入口与最小事实准备，未写正文。见[准备结果](docs/NOVEL_R2_REENTRY_FACT_PREPARATION_RESULT_20261003.md)、[证据](delivery/r2-reentry-facts-20261003/preparation-evidence.json)、[事实投影](delivery/r2-reentry-facts-20261003/writer-context.json)。当时唯一动作 `AWAIT_LIU_AUTHORIZATION_OF_ONE_NEW_300_500_CHAR_R2_ENTRY_TRIAL_WITH_OPENING_SCOPE` 已由本轮另存的新授权推进；[旧短段提案](state/tasks/NOVEL_R2_REENTRY_ONE_SHORT_TRIAL_PROPOSAL_20261003.json)保持当时未授权原件。方法4、448字真人FAIL、原404字UNKNOWN、旧预算与旧197字保护均保持。

上一检查点194：`NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01` 已完成四个独立GPT-6.1 Sol/Max会话、原始报告回收及证据核对。[诊断与证据](docs/NOVEL_R2_EMOTION_RETENTION_DIAGNOSIS_RESULT_20261003.md)、[逐条结算](state/reviews/codex-20261003/coordinator-settlement.json)、[可执行接入附录](docs/NOVEL_CODEX_REVIEW_INTEGRATION_20261003.md)、[原结果回执](state/review_receipts/NOVEL_CODEX_REVIEW_INTEGRATION_AND_R2_DIAGNOSIS_RESULT_20261003.json)原样保留。校准漏检2/2、留出验证漏检1/1，不能认证好看或个人口味；44处原文引文已定位。原[验证](state/review_receipts/NOVEL_CODEX_REVIEW_VALIDATION_20261003.json)和[远端回执](state/review_receipts/NOVEL_CODEX_REVIEW_REMOTE_SAVE_VERIFIED_20261003.json)只证明该次冻结记录。该时唯一动作 `AWAIT_LIU_AUTHORIZATION_OF_ONE_BOUNDED_R2_REENTRY_FACT_PREPARATION_TASK_NO_PROSE` 已由本轮新授权推进；[旧准备提案](state/tasks/NOVEL_R2_REENTRY_FACT_PREPARATION_PROPOSAL_20261003.json)仍保留当时未授权原件，不伪造旧callback或旧任务重试。

读取这些已保存结果及运行 `python scripts/verify_current_state.py` 不会再次调用模型。重新评测须有新的明确任务、冻结清单与独立结果目录，详见接入附录。入口不保证所有聊天自动加载，也没有后台持续运行或跨聊天自动推送。

上一检查点193的浏览器阻塞记录（保留，当前执行已由独立新任务接续）：当前448字稿（blob f0545b15cf01dd6de83e105003e3af34b22cf4db）仍维持刘先生实际否决：没有情绪、没有继续阅读欲望；题材未否定，具体停止句与机器人对白判决仍未知，原404字真人仍UNKNOWN。R2情绪/留存项目外编辑诊断在发送前发生精确composer阻塞：已打开项目外全新Chat并实际核验为Chat、Latest、Pro（第5/5档；无GPT-6.1可选），但一次完整装填后逐字/哈希比对失败——composer在callback URL前多出一个换行，同时末尾换行被去除；期望SHA-256 947cff4a65eb6774d1df53b2cb14e47909ea291107a60217603bb5c585be7909，实际composer SHA-256 439a41253361cf2423953c05645b339b665339b75f46ce13485b0caa40e18c57。按本轮硬规则未点击发送（send_click_count=0）、未产生reviewer /c/ URL、外审未启动、无callback、无新正文；不得拆段补发、Retry或另开同任务。阻塞回执：`state/review_receipts/NOVEL_R2_EMOTION_RETENTION_DIAGNOSIS_PRE_SEND_BLOCKED_20261003.json`。当时唯一下一动作：`AWAIT_NEW_UNIFIED_COMMAND_AFTER_R2_DIAGNOSIS_PRE_SEND_COMPOSER_MISMATCH_NO_RETRY`。旧RC3两轮仍用尽，旧197字保护与主线方法4保持不变。

方法1已失败原稿：`delivery/mainline-v1/test-01-sp414-s02-a1.md`，Git blob `d3796f41e10f90c6197211213bd2f4b96f18d196`。原始冻结执行回执保留：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_READING_20261001.json`。方法1真人失败回执：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_HUMAN_FAIL_20261001.json`；主要失败定位与局部修订范围：`docs/NOVEL_MAINLINE_TEST01_A1_FAILURE_DIAGNOSIS_20261001.md`。本次写作者使用不继承历史的独立上下文，只带入 `delivery/mainline-v1/test-01-writer-input.md`；协调者核对事实，未改写输出。历史新聊天执行入口不再用于重投本测试。`MAINLINE.md`中的初始位置描述保持为锁定当时的记录，实时进度以当前状态和检查点为准。

执行偏好已保存：已授权环节连续完成，不在例行步骤反复请求确认。用户本次明确要求几百字即可判断，下一次先做300–500字起始短段；未经请求不再内联整场长稿。短段通过只证明短段，不等于完整场景通过。方法4已绑定方法3实际留存FAIL并冻结新测试输入。短段通过后仍需同一场完整验证，才能进入不同压力的 TEST-02。

《第二套过去》方向保留。Phase422 V4 与 opening trial 的原有真人否决继续有效；Phase428 的重 AI 味反馈保留；Phase430 的机器人式反复问答反馈已另存回执，来源覆盖为 PARTIAL，原聊天定位不可用，不扩张为题材否决。旧正文与执行回执不覆盖，不原样重投。

写作者只读单独冻结的写作输入，不读本入口、失败反馈、诊断、验收答案或历史全部规则。通过一场只能证明一场；完整稿 V5、历史已关闭任务与自动晋级继续关闭。尚未取得真人反馈时保持 UNKNOWN。

当前脚本验证主线与状态的一致性，保留旧稿拒绝边界。它不评判文学质量，也不构成平台级硬锁。

本轮审核由Codex冻结材料、创建无工具无继承的独立评审上下文、直接回收结构报告、核对事实与范围并原生保存。历史Opera Neon协议、外审赞扬及漏检结果保留审计；新的 `codex_review_integration` 只替代本轮执行接入，不伪造旧任务回调或真人认可。检查点194接入任务当时不执行旧浏览器派发、写作或自动复审；最新短稿见检查点200，真人UNKNOWN。
