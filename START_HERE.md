# 小说项目接管入口

权威仓库：`vubaoha034-hash/book`，分支：`main`。新聊天先读取远端最新 HEAD，再依次读取 `AGENTS.md`、`state/project_state.json`、`state/continuity/LATEST_CHECKPOINT.json` 和检查点指向的最新真人回执。聊天摘要和旧 phase 文档不能覆盖当前状态。

执行前运行 `python3 scripts/verify_current_state.py`。检查失败时先修复状态冲突，停止生成、送审或自动进入下一阶段。执行后在同一次变更中更新当前状态与检查点，回读远端文件和 HEAD。

当前人审结论：`RJ-OE408-I《第二套过去》` Phase422 V4 的文风与可读性严重不通过；题材方向保留。同一 V4 不再送审，也没有自动全文 V5 的许可。已核对两种不同的人审范围：Phase363 认可短场景推进机制，未证明长篇迁移；Phase370 只通过局部动机清晰度，AI 味没有进一步改善。对照 V4 失败的依据见 `state/diagnoses/PHASE422_V4_REPAIR_BASIS_CORRECTION_20260929.md`。下一动作是另立一次有界开头场景试写、供真人阅读；不自动全文 V5，不把局部通过说成文风完成。

本入口只定位当前事实。它不代表小说质量通过，也不代替真人审美验收。
