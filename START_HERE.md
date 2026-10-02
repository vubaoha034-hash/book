# 小说项目接管入口

权威仓库：`vubaoha034-hash/book`，分支：`main`。项目：`novel-distillation`。先读取远端最新 HEAD，并把本次相关读取固定到同一提交。

依次读取 `AGENTS.md`、`MAINLINE.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json`、状态指向的当前主线任务、锁定回执和最新真人反馈。历史阶段文件不能覆盖这个顺序。

执行前运行 `python scripts/verify_current_state.py`；失败时先核对状态冲突，停止生成、重投或晋级。执行后在同一次变更中同步状态、检查点及任务回执，回读远端 HEAD 与实际文件。

唯一主线：`NOVEL-IMPROVEMENT-MAINLINE-V1`。保留原故事方向、契约和有效证据，停用冻结八步动作作为新写作者硬约束。方法变化依据冻结测试失败或用户明确范围变更；参见 `MAINLINE.md`。本次用户已明确授权项目外日常证据评审，见 `external_review_state`及其绑定协议/回执；不能把AI意见写成真人FAIL。

当前位置：检查点178。A2准备回传 `NO_LOCATED_BLOCKERS` 已核对并只处理一次；仅准备输入进入写作，不代表RC3关闭。当前唯一执行为 `state/tasks/NOVEL_RC3_LOCAL_REVISION_R1_WRITER_20261002.json` 与独立执行锁；下一动作 `EXECUTE_ONE_FRESH_CONTEXT_RC3_LOCAL_REVISION`。新聊天仅接收批准的A2输入，输出唯一300–500字局部稿，保护197字符开头。原方法4稿真人UNKNOWN、旧锁及完整场景/全文禁止边界不变。

方法1已失败原稿：`delivery/mainline-v1/test-01-sp414-s02-a1.md`，Git blob `d3796f41e10f90c6197211213bd2f4b96f18d196`。原始冻结执行回执保留：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_READING_20261001.json`。方法1真人失败回执：`state/review_receipts/NOVEL_MAINLINE_TEST01_A1_HUMAN_FAIL_20261001.json`；主要失败定位与局部修订范围：`docs/NOVEL_MAINLINE_TEST01_A1_FAILURE_DIAGNOSIS_20261001.md`。本次写作者使用不继承历史的独立上下文，只带入 `delivery/mainline-v1/test-01-writer-input.md`；协调者核对事实，未改写输出。历史新聊天执行入口不再用于重投本测试。`MAINLINE.md`中的初始位置描述保持为锁定当时的记录，实时进度以当前状态和检查点为准。

执行偏好已保存：已授权环节连续完成，不在例行步骤反复请求确认。用户本次明确要求几百字即可判断，下一次先做300–500字起始短段；未经请求不再内联整场长稿。短段通过只证明短段，不等于完整场景通过。方法4已绑定方法3实际留存FAIL并冻结新测试输入。短段通过后仍需同一场完整验证，才能进入不同压力的 TEST-02。

《第二套过去》方向保留。Phase422 V4 与 opening trial 的原有真人否决继续有效；Phase428 的重 AI 味反馈保留；Phase430 的机器人式反复问答反馈已另存回执，来源覆盖为 PARTIAL，原聊天定位不可用，不扩张为题材否决。旧正文与执行回执不覆盖，不原样重投。

写作者只读单独冻结的写作输入，不读本入口、失败反馈、诊断、验收答案或历史全部规则。通过一场只能证明一场；完整稿 V5、历史已关闭任务与自动晋级继续关闭。尚未取得真人反馈时保持 UNKNOWN。

当前脚本验证主线与状态的一致性，保留旧稿拒绝边界。它不评判文学质量，也不构成平台级硬锁。

日常审核分工已按用户要求改变：助手负责冻结版本、通过Opera Neon发送到项目外评审、读取原始报告、核对证据、局部修订与复审；用户不逐轮审失败稿。初始负例0/2、未见材料负例0/1均漏检，所以该评审已实际改为EVIDENCE_AUDITOR，不认证好看或个人文风；原AI赞扬不翻案，实际认可仍UNKNOWN。完整任务及私有浏览器快照不公开。不能声称有后台跨聊天自动推送。
