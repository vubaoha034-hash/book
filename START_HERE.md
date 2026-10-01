# 小说项目接管入口

权威仓库：`vubaoha034-hash/book`，分支：`main`。项目：`novel-distillation`。先读取远端最新 HEAD，并把本次相关读取固定到同一提交。

依次读取 `AGENTS.md`、`MAINLINE.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json`、状态指向的当前主线任务、锁定回执和最新真人反馈。历史阶段文件不能覆盖这个顺序。

执行前运行 `python scripts/verify_current_state.py`；失败时先核对状态冲突，停止生成、重投或晋级。执行后在同一次变更中同步状态、检查点及任务回执，回读远端 HEAD 与实际文件。

唯一主线：`NOVEL-IMPROVEMENT-MAINLINE-V1`。保留原故事方向、契约和有效证据，停用冻结八步动作作为新写作者硬约束。方法变化须先有对应冻结测试的实际失败记录；参见 `MAINLINE.md`。

当前位置：检查点153，锁定主线V1的步骤1、2已完成，步骤3的 TEST-01 唯一第二场已生成并冻结。唯一下一动作：`AWAIT_ACTUAL_HUMAN_READING_OF_TEST_01`。事实核对 CLEAR，真人结果 UNKNOWN；TEST-02 尚未开始，没有文风通过结论。

冻结正文：`delivery/mainline-v1/test-01-sp414-s02-a1.md`，Git blob `d3796f41e10f90c6197211213bd2f4b96f18d196`。执行及阅读回执：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_READING_20261001.json`。本次写作者使用不继承历史的独立上下文，只带入 `delivery/mainline-v1/test-01-writer-input.md`；协调者核对事实，未改写输出。历史新聊天执行入口不再用于重投本测试。`MAINLINE.md`中的初始位置描述保持为锁定当时的记录，实时进度以当前状态和检查点为准。

执行偏好已保存：已授权的准备、写作、检查、冻结、保存与交付连续完成，不在例行步骤反复请求确认。只有取得该冻结正文的实际真人阅读反馈，才判定是否进入 TEST-02；这仍是同一锁定主线。

《第二套过去》方向保留。Phase422 V4 与 opening trial 的原有真人否决继续有效；Phase428 的重 AI 味反馈保留；Phase430 的机器人式反复问答反馈已另存回执，来源覆盖为 PARTIAL，原聊天定位不可用，不扩张为题材否决。旧正文与执行回执不覆盖，不原样重投。

写作者只读单独冻结的写作输入，不读本入口、失败反馈、诊断、验收答案或历史全部规则。通过一场只能证明一场；完整稿 V5、历史已关闭任务与自动晋级继续关闭。尚未取得真人反馈时保持 UNKNOWN。

当前脚本验证主线与状态的一致性，保留旧稿拒绝边界。它不评判文学质量，也不构成平台级硬锁。
