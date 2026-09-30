# 小说项目接管入口

权威仓库：`vubaoha034-hash/book`，分支：`main`。新聊天先读取远端最新 HEAD，再依次读取 `AGENTS.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json` 和检查点指向的最新真人回执。聊天摘要和旧 phase 文档不能覆盖当前状态。

执行前运行 `python3 scripts/verify_current_state.py`。检查失败时先修复状态冲突，停止生成、送审或自动进入下一阶段。执行后在同一次变更中更新当前状态与检查点，回读远端文件和 HEAD。

当前人审结论：`RJ-OE408-I《第二套过去》` Phase422 V4 与唯一 post-V4 opening trial 均已真人否决；题材/核心 premise 保留，同一 V4 与该 opening trial 均关闭，仍无自动全文 V5 许可。

Phase423 已完成一次真实正文对照诊断，durable receipt 为 `state/review_receipts/PHASE423_RJ_OE408_I_EMOTIONAL_PROSE_REGRESSION_DIAGNOSIS_V1.json`。实际正例 A 固定为 `novel-distill-v1:state/calibration/PHASE370_B_MOTIVE_CLARITY_REPAIR_V1.txt` blob `7be11d5d669250b77292c5181e4f2b9c2251d0c8`；其真人范围仅为即时动机清晰 YES、剩余未知是 suspense、愿意继续 YES，且 AI smell=SAME，不是整部文风 PASS。失败原件 B 固定为 `delivery/phase422/07-opening-scene-trial-after-v4.md` blob `d0591031e85b790d04e9b6c84eadb59ac995b31f`，真人结论为 `FAIL_EMOTIONLESS_ROBOTIC_DIALOGUE`。

本轮定位的具体回退是：B 重新把人物变成谜题/制度信息接口——对白主要顺序确认事实，动作多为信息承载或情绪伴奏，人物各自要保住的利益与边界很少互相卡住，因此关系、行动权限与风险没有随着每个节拍被持续改写；A 的局部有效处来自目标冲突、由压力触发的后果性动作、人物不完全配合以及信息先通过行为后果暴露，而不是来自追杀、箭、刀、木牌等表面高强度元素。

Phase424 已完成 exactly 1 个 SP414-S02 单场景候选，原件为 `delivery/phase424/08-sp414-s02-first-xucheng-relational-pressure-scene-v1.md`，版本 `SP414-S02-V1`；durable task 为 `state/tasks/PHASE424_RJ_OE408_I_FIRST_XUCHENG_RELATIONAL_PRESSURE_SCENE_V1.json`，执行回执为 `state/review_receipts/PHASE424_RJ_OE408_I_FIRST_XUCHENG_RELATIONAL_PRESSURE_SCENE_V1.json`。本轮没有第二场景、第二版本、best-of-N 或全文 V5，也没有机器最终文学质量 PASS。该候选现在只等待刘先生真人阅读。

唯一下一动作：`RETURN_EXACT_ONE_SP414_S02_SCENE_TO_UNIFIED_COMMAND_FOR_LIU_XIANSHENG_ACTUAL_READING`。在真人回执前，不得生成第二候选、第二场景或全文 V5。

本入口只定位当前事实。它不代表小说质量通过，也不代替真人审美验收。
