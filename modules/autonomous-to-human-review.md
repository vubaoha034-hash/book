# 直接推进到人工阅读

刘先生最新指令：“你能不能不要停，直到我人工审核的时候再给我看就行。其他时候不用我授权。” 已另存[当前执行授权](../state/review_receipts/NOVEL_AUTONOMOUS_TO_HUMAN_AUTHORIZATION_20261003.json)及[持续执行偏好](../rules/autonomy-until-human-review.json)。它推进已准备的同主线300—500字新版本开头，允许常规准备、独立写作、审核、必要范围内修订和原生保存，不再把每项工作结束变成授权请求。故事目标、世界与结局及真人验收仍保持。

本次具体任务选择一个可审计上限：一次独立初稿，最多一次有证据的必要修订，同一候选只展示一个最终版本。修订只由确定事实/长度/格式问题或已核实的主要编辑问题触发；普通读者AI的赞成或否决不自动触发继续抽稿。此上限是协调者对本次工作的范围安排，不能改写成刘先生给了无限额度。旧RC3和旧197字保护不会重置。未来同主线下一有界任务依据本执行授权另存范围；不重复要求用户批准常规中间步骤。

独立写作者只取检查点198已准备的writer_packet：同一场事实、姓名被看到的进入时刻、输出范围和三条正向原则，不读真人失败、旧稿、编辑报告或总控诊断。每份返回正文直接冻结，不由协调者改写。必要修订若发生，用新上下文接收当前待修稿和一个经核对的目标，不继承聊天或整套审稿答案；原稿与报告保持原件。

事实审查只看正文和必要事实；新稿编辑只看正文、必要事实和局部范围，当前没有真人结果，不能称已知失败后的诊断；匿名读者只看正文、媒介和摘录位置。三个上下文彼此独立，也不同于写作者。仍用已验证的无工具Codex运输：新进程、新临时线程，环境/仓库/技能发现/记忆/网络/插件关闭，实际核对Sol/Max、线程与完成记录。协调者唯一写入业务状态。

新工种EDITORIAL_REVIEW补充到原协议的严格字段允许表，没有删除冷读隔离、历史否决、耗尽预算和禁止晋级检查。EDITORIAL_CLEAR是局部编辑未发现阻塞，FACT_CLEAR只表示没有确定事实矛盾，读者YES只是一个AI反应，三者均不等于真人PASS。历史校准漏检与不适用的人群结论继续保留。原文定位、窗口引文、事实、保护项和未知均另行结算，纠错不能改写原报告。

本次运行顺序（当前任务一次消费锁已使用）：

```powershell
python -X utf8 scripts/novel_autonomous_opening.py prepare
python -X utf8 scripts/novel_autonomous_opening.py run --role writer
python -X utf8 scripts/novel_autonomous_opening.py prepare-reviews
python -X utf8 scripts/novel_autonomous_opening.py run --role facts
python -X utf8 scripts/novel_autonomous_opening.py run --role editor
python -X utf8 scripts/novel_autonomous_opening.py run --role reader
python -X utf8 scripts/novel_autonomous_opening.py audit --role facts
python -X utf8 scripts/novel_autonomous_opening.py audit --role editor
python -X utf8 scripts/novel_autonomous_opening.py audit --role reader
python -X utf8 scripts/verify_current_state.py
```

三审在正文冻结后可并行。当前结果应直接读取，不得重跑已消费的prepare/run；读取与状态检查不会调用模型。将来重新写作/评审要有新的具体任务、来源HEAD、清单、结果目录及受控次数。没有后台任务、跨聊天自动加载或远程持续运行。

最后只交一份已原生保存的新稿，请刘先生判断是否想继续读、人物是否仍像机器人。实际阅读反馈没有收到时，该新稿保持UNKNOWN；历史395字及448字FAIL绑定各自原稿，不迁移到新稿，也不被AI意见覆盖。人工短段通过仍不足以自动授权整场、TEST-02或V5。
