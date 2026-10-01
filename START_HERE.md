# 小说项目接管入口

权威仓库：`vubaoha034-hash/book`，分支：`main`。项目：`novel-distillation`。先读取远端最新 HEAD，并把本次相关读取固定到同一提交。

依次读取 `AGENTS.md`、`MAINLINE.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json`、状态指向的当前主线任务、锁定回执和最新真人反馈。历史阶段文件不能覆盖这个顺序。

执行前运行 `python scripts/verify_current_state.py`；失败时先核对状态冲突，停止生成、重投或晋级。执行后在同一次变更中同步状态、检查点及任务回执，回读远端 HEAD 与实际文件。

唯一主线：`NOVEL-IMPROVEMENT-MAINLINE-V1`。保留原故事方向、契约和有效证据，停用冻结八步动作作为新写作者硬约束。方法变化须先有对应冻结测试的实际失败记录；参见 `MAINLINE.md`。

当前位置：检查点152，锁定主线V1的步骤1、2已完成，TEST-01 和 TEST-02 均未开始。唯一下一动作：`RUN_ONE_FRESH_WRITER_TEST_01_THEN_ACTUAL_HUMAN_READING`。本次完成事实和输入准备，不代表已写出新场景或已改善文风。

当前独立写作输入：`delivery/mainline-v1/test-01-writer-input.md`，Git blob `cb5bcc42ef070810fd8b5af113d38df3417f36d5`。新聊天执行入口：`delivery/mainline-v1/START_TEST01_IN_NEW_CHAT.txt`。事实及原著研究由协调者核对，写作者只读该写作输入。`MAINLINE.md`中的初始位置描述保持为锁定当时的记录，实时进度以当前状态和检查点为准。

《第二套过去》方向保留。Phase422 V4 与 opening trial 的原有真人否决继续有效；Phase428 的重 AI 味反馈保留；Phase430 的机器人式反复问答反馈已另存回执，来源覆盖为 PARTIAL，原聊天定位不可用，不扩张为题材否决。旧正文与执行回执不覆盖，不原样重投。

写作者只读单独冻结的写作输入，不读本入口、失败反馈、诊断、验收答案或历史全部规则。通过一场只能证明一场；完整稿 V5、历史已关闭任务与自动晋级继续关闭。尚未取得真人反馈时保持 UNKNOWN。

当前脚本验证主线与状态的一致性，保留旧稿拒绝边界。它不评判文学质量，也不构成平台级硬锁。
