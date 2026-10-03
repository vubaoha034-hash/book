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

当前位置：检查点194。本轮任务 `NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01` 已完成Codex接入、四个独立GPT-6.1 Sol/Max会话、原始报告回收、证据核对和已知失败后的诊断。校准漏检2/2，留出验证漏检1/1；接入只能辅助证据审查与诊断，不能认证好看或个人口味。事实审查未发现确定矛盾，44处显式引文逐项定位，原报告未改写。448字真人FAIL仍有效，原404字真人UNKNOWN；主线方法4、旧RC3剩余0轮和旧197字保护不变。

接续先读[当前原生任务](state/tasks/NOVEL_CODEX_REVIEW_INTEGRATION_AND_R2_DIAGNOSIS_20261003.json)、[结果回执](state/review_receipts/NOVEL_CODEX_REVIEW_INTEGRATION_AND_R2_DIAGNOSIS_RESULT_20261003.json)、[三个编辑根因与证据](docs/NOVEL_R2_EMOTION_RETENTION_DIAGNOSIS_RESULT_20261003.md)、[原始报告及逐条结算](state/reviews/codex-20261003/coordinator-settlement.json)、[可执行接入附录](docs/NOVEL_CODEX_REVIEW_INTEGRATION_20261003.md)。本轮执行变更先单独保存，旧浏览器任务未重试、旧callback未收到。 [验证记录](state/review_receipts/NOVEL_CODEX_REVIEW_VALIDATION_20261003.json)保存27项原生状态检查、28文件结构验证、97项测试与已消费调用的拒绝记录；[远端保存回执](state/review_receipts/NOVEL_CODEX_REVIEW_REMOTE_SAVE_VERIFIED_20261003.json)在推送后读取实际main字节生成。

当前唯一下一动作：`AWAIT_LIU_AUTHORIZATION_OF_ONE_BOUNDED_R2_REENTRY_FACT_PREPARATION_TASK_NO_PROSE`。唯一[后续提案](state/tasks/NOVEL_R2_REENTRY_FACT_PREPARATION_PROPOSAL_20261003.json)尚未授权：核对前场、选一个进入时刻及已有私人利害、列必要事实缺口与授权边界；不写正文。涉及开头改变、旧197字范围、具体新生活事实及任何新写作预算都须另有明确授权，不能自动解除旧锁或续用旧额度。本轮保存核验后停止，无定时任务。

读取这些已保存结果及运行 `python scripts/verify_current_state.py` 不会再次调用模型。重新评测须有新的明确任务、冻结清单与独立结果目录，详见接入附录。入口不保证所有聊天自动加载，也没有后台持续运行或跨聊天自动推送。

上一检查点193的浏览器阻塞记录（保留，当前执行已由独立新任务接续）：当前448字稿（blob f0545b15cf01dd6de83e105003e3af34b22cf4db）仍维持刘先生实际否决：没有情绪、没有继续阅读欲望；题材未否定，具体停止句与机器人对白判决仍未知，原404字真人仍UNKNOWN。R2情绪/留存项目外编辑诊断在发送前发生精确composer阻塞：已打开项目外全新Chat并实际核验为Chat、Latest、Pro（第5/5档；无GPT-6.1可选），但一次完整装填后逐字/哈希比对失败——composer在callback URL前多出一个换行，同时末尾换行被去除；期望SHA-256 947cff4a65eb6774d1df53b2cb14e47909ea291107a60217603bb5c585be7909，实际composer SHA-256 439a41253361cf2423953c05645b339b665339b75f46ce13485b0caa40e18c57。按本轮硬规则未点击发送（send_click_count=0）、未产生reviewer /c/ URL、外审未启动、无callback、无新正文；不得拆段补发、Retry或另开同任务。阻塞回执：`state/review_receipts/NOVEL_R2_EMOTION_RETENTION_DIAGNOSIS_PRE_SEND_BLOCKED_20261003.json`。当时唯一下一动作：`AWAIT_NEW_UNIFIED_COMMAND_AFTER_R2_DIAGNOSIS_PRE_SEND_COMPOSER_MISMATCH_NO_RETRY`。旧RC3两轮仍用尽，旧197字保护与主线方法4保持不变。

方法1已失败原稿：`delivery/mainline-v1/test-01-sp414-s02-a1.md`，Git blob `d3796f41e10f90c6197211213bd2f4b96f18d196`。原始冻结执行回执保留：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_READING_20261001.json`。方法1真人失败回执：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_HUMAN_FAIL_20261001.json`；主要失败定位与局部修订范围：`docs/NOVEL_MAINLINE_TEST01_A1_FAILURE_DIAGNOSIS_20261001.md`。本次写作者使用不继承历史的独立上下文，只带入 `delivery/mainline-v1/test-01-writer-input.md`；协调者核对事实，未改写输出。历史新聊天执行入口不再用于重投本测试。`MAINLINE.md`中的初始位置描述保持为锁定当时的记录，实时进度以当前状态和检查点为准。

执行偏好已保存：已授权环节连续完成，不在例行步骤反复请求确认。用户本次明确要求几百字即可判断，下一次先做300–500字起始短段；未经请求不再内联整场长稿。短段通过只证明短段，不等于完整场景通过。方法4已绑定方法3实际留存FAIL并冻结新测试输入。短段通过后仍需同一场完整验证，才能进入不同压力的 TEST-02。

《第二套过去》方向保留。Phase422 V4 与 opening trial 的原有真人否决继续有效；Phase428 的重 AI 味反馈保留；Phase430 的机器人式反复问答反馈已另存回执，来源覆盖为 PARTIAL，原聊天定位不可用，不扩张为题材否决。旧正文与执行回执不覆盖，不原样重投。

写作者只读单独冻结的写作输入，不读本入口、失败反馈、诊断、验收答案或历史全部规则。通过一场只能证明一场；完整稿 V5、历史已关闭任务与自动晋级继续关闭。尚未取得真人反馈时保持 UNKNOWN。

当前脚本验证主线与状态的一致性，保留旧稿拒绝边界。它不评判文学质量，也不构成平台级硬锁。

本轮审核由Codex冻结材料、创建无工具无继承的独立评审上下文、直接回收结构报告、核对事实与范围并原生保存。历史Opera Neon协议、外审赞扬及漏检结果保留审计；新的 `codex_review_integration` 只替代本轮执行接入，不伪造旧任务回调或真人认可。当前不执行旧浏览器派发，也不启动新写作或自动复审。
