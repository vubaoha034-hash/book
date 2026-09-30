# 小说项目接管入口

权威仓库：`vubaoha034-hash/book`，分支：`main`。新聊天先读取远端最新 HEAD，再依次读取 `AGENTS.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json` 和检查点指向的最新真人回执。聊天摘要和旧 phase 文档不能覆盖当前状态。

执行前运行 `python3 scripts/verify_current_state.py`。检查失败时先修复状态冲突，停止生成、送审或自动进入下一阶段。执行后在同一次变更中更新当前状态与检查点，回读远端文件和 HEAD。

当前人审结论：`RJ-OE408-I《第二套过去》` Phase422 V4 与唯一 post-V4 opening trial 均已真人否决；题材/核心 premise 保留，同一 V4 与该 opening trial 均关闭，仍无自动全文 V5 许可。

Phase423 已完成一次真实正文对照诊断，durable receipt 为 `state/review_receipts/PHASE423_RJ_OE408_I_EMOTIONAL_PROSE_REGRESSION_DIAGNOSIS_V1.json`。实际正例 A 固定为 `novel-distill-v1:state/calibration/PHASE370_B_MOTIVE_CLARITY_REPAIR_V1.txt` blob `7be11d5d669250b77292c5181e4f2b9c2251d0c8`；其真人范围仅为即时动机清晰 YES、剩余未知是 suspense、愿意继续 YES，且 AI smell=SAME，不是整部文风 PASS。失败原件 B 固定为 `delivery/phase422/07-opening-scene-trial-after-v4.md` blob `d0591031e85b790d04e9b6c84eadb59ac995b31f`，真人结论为 `FAIL_EMOTIONLESS_ROBOTIC_DIALOGUE`。

本轮定位的具体回退是：B 重新把人物变成谜题/制度信息接口——对白主要顺序确认事实，动作多为信息承载或情绪伴奏，人物各自要保住的利益与边界很少互相卡住，因此关系、行动权限与风险没有随着每个节拍被持续改写；A 的局部有效处来自目标冲突、由压力触发的后果性动作、人物不完全配合以及信息先通过行为后果暴露，而不是来自追杀、箭、刀、木牌等表面高强度元素。

Phase424 / `SP414-S02-V1` / blob `6200d891b1585ed9d333e325080227ad78a91e05` 已被刘先生真人明确否决为严重 AI 味回退；题材/核心 premise 未被否决，同一场景原样重投关闭。

Phase425 已从真实历史较好 prose 证据回退修复：直接读取 Phase396 候选原文及真人回执、Phase363 真人正向回执与其在 Phase396 renderer 中保留的两段实际正向 prose 参照，产出 exactly 1 个修复场景 `delivery/phase425/09-sp414-s02-best-known-prose-rollback-repair-v1.md`，版本 `SP414-S02-REPAIR-V1`，blob `f285de3da19bbbd4f33c0343020b664f29d618e6`。durable task/receipt 为 `state/review_receipts/PHASE425_RJ_OE408_I_BEST_KNOWN_PROSE_ROLLBACK_SP414_S02_REPAIR_V1.json`，blob `98940d7bf2716d5647c929c87505bd1e28bdcff6`。只执行了一次与 Phase424 + 历史较好 prose anchor 的明显回退筛查；机器筛查不构成文学质量 PASS。

唯一下一动作：`RETURN_EXACT_ONE_REPAIRED_SP414_S02_TO_UNIFIED_COMMAND_FOR_LIU_XIANSHENG_ACTUAL_READING`。在刘先生真人阅读前，不得生成第二版本、第二场景、best-of-N 或全文 V5。

本入口只定位当前事实。它不代表小说质量通过，也不代替真人审美验收。
