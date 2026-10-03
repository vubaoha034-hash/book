# 独立编辑与首次读者的接入

本模块沿用既有专业评审协议和Codex隔离运输，取用固定提交的 `story-review`、`reader-sim`，保留出处于[来源清单](../state/learning/two-role-opening-20261003/sources.json)。这是两个真实独立的AI调用，不是协调者扮演两个角色，也不是真人编辑或读者研究。

编辑先读完整摘录，再区分进入时刻、事实输入和呈现；按读者成本给二至三个根因。读者只记录首次阅读感受、持有的问题和愿不愿继续，不给技法评分或改稿方案。只审第二场起始短段；不从局部推断整本书的结构、市场效果或读者普遍反应。

协调者冻结同一正文，以匿名ID和SHA发送给两角色。读者只带媒介和摘录位置；编辑可带必要事实和真实反馈，必须标记已知失败后的诊断。两角色用不同进程与新临时线程，没有历史、文件、技能自动发现、MCP、工具、网络和仓库权限；协调者是唯一状态写作者。模型与思考强度核对目录、thread/start与回执，不靠提示词自报。

取用技能的部分：先找主导问题，结构先于润色，结论逐字定位，保护有效部分；首次读者报告关注、走神、好奇和人物可信度。未取用的部分：在短段上判断全书结构、四人虚拟投票、外部脚本、整套写作规则或自动把评审意见变成新正文。外部技能与教程是参考，未验证对刘先生口味有效。

本次实际命令（每个run只有一次消费锁）：

```powershell
python -X utf8 scripts/novel_two_role_review.py prepare
python -X utf8 scripts/novel_two_role_review.py run --role reader
python -X utf8 scripts/novel_two_role_review.py run --role editor
python -X utf8 scripts/novel_two_role_review.py audit --role reader
python -X utf8 scripts/novel_two_role_review.py audit --role editor
python -X utf8 scripts/verify_current_state.py
```

prepare及两个run已经消费，不得重跑本任务。读取原始报告、audit和状态检查不调用模型；audit也采用排他创建避免覆盖原证据。未来重评须由新任务绑定新的稿件/清单/结果目录与一次预算，再复用此运输方式。不会自动加载所有聊天，也不在后台持续运行。

原报告先冻结，纠错另存；主要引文、阅读窗口、事实和范围由协调者逐项结算。原文不存在、误读时间或越界建议应拒绝或收窄，不能自动进入写作。评审失败、缺报告和材料不足保持阻塞/未知；AI读者的YES不能覆盖真人FAIL。

旧筛查已漏检校准2/2、留出1/1；同类认可正例缺失，无法估计误杀率。新角色用于局部诊断，当前旧失败样本不成为新的留出集，不能宣称校准泛化、准确率或“符合刘先生口味”。两报告之后只准备一份有界开头范围与输入，不供应新写作预算；旧RC3额度、197字保护、原404未知、人物世界结局保持。
