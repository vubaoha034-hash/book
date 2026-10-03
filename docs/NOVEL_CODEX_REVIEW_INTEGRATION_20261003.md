# Codex 独立评审接入（2026-10-03）

本轮任务：`NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01`。
来源 main 固定在 `122739a8c6f0ffa47ee77726865c06f8cb2c566a`、检查点193。
这是执行方式与评测接入变更，小说主线仍为方法4。既有专业协议继续适用：
[专业评审协议](NOVEL_EXTERNAL_REVIEW_PROTOCOL_V1_20261001.md)。

协调者是唯一业务状态写作者。`scripts/codex_review.py` 在本地调用已安装的
Codex app-server，使用已有 ChatGPT 登录，不新建付费服务或 API 凭据。
每份报告启用全新进程、临时配置目录与全新 ephemeral thread；只复制现有登录，
不复制用户配置、MCP、插件、技能、记忆或聊天历史。临时凭据不进入仓库或输出，
进程结束后删除临时目录。评审无环境与仓库入口，工具关闭，readOnly、联网关闭、
approvalPolicy=never。模型目录、thread/start 实际返回设置和报告终态另存 runtime。
只在提示词写模型名不算已核验。

评审分为三个用途，分别新建上下文：

| 用途 | 输入 | 可以得出的结论 |
| --- | --- | --- |
| 冷读筛查 | 匿名冻结正文、媒介、摘录位置 | 编辑对摘录的阅读期待假设；须经标签检验 |
| 事实审查 | 正文、必要冻结事实 | 是否存在确定矛盾；FACT_CLEAR 不等于好看 |
| 已知失败后的编辑诊断 | 正文、必要事实、真人失败及边界 | 二至三个上游根因假设；不能冒充盲读 |

本轮 C61 的两个历史负例只用于校准；V83 的448字稿为另一版本的留出验证。
二者仍是同一故事的小样本，不构成跨题材泛化实验。C61 报告及证据冻结后才生成
标签揭示回执。提示词不因结果改写，不追加调用追求通过。
本轮校准漏检2/2，故接入只能用于证据审查和编辑诊断，不能作为独立质量放行门。
没有已建立的同类真人认可正例，误杀率未知，总体准确率不可估计。

## 冻结、回收和核验

`config/codex-review-run-20261003.json` 是协调者清单，包含来源、材料哈希与标签，
不提交给评审。`delivery/codex-review-20261003/*.packet.json` 才是评审数据。
冷读包采用字段允许名单，不靠删除几个失败关键词掩盖泄漏。历史 writer-input 的
“只返回正文”等命令只在诊断包中作为历史来源保留，明确不适用于本次评审。
无源文本、错哈希、额外标签或写作字段均阻断。

回收原始 `.raw.txt` 后写入其 blob、SHA-256 和实际运行记录，再逐项核对引文、
行号、稿件身份、事实与建议范围。原始报告采用排他创建，不覆盖。位置纠正写入
`.evidence.json`，事实误读和越界建议另存协调结算；不得改写原报告制造一致。
无报告、失败终态、材料不足均不产生质量通过，也不授权修订或新正文。
`scripts/verify_codex_review.py` 接在原生校验器全部历史门之后，保留真人否决、
旧额度用尽及禁止自动晋级检查。

本轮启动配置和宿主网络曾失败，分别保存在 preflight/transport 原始运行记录与
修复回执中。失败时没有报告或判定；只有证明没有评审输出的基础设施修复可继续。
宿主传输联网与模型的工具权限分开：获准联网的是协调传输，评审仍无工具、只读。
这些修复不是旧浏览器任务重试，也没有收到旧 callback。

## 读取结果与重新运行

ChatGPT 接管时先从 [START_HERE](../START_HERE.md) 读取最新 main 和检查点，运行
`python scripts/verify_current_state.py`，再读结果回执、诊断文档、原始报告及协调结算。
这仅核验保存的结果，不再次调用模型。仓库入口不能保证所有聊天自动加载，也没有
后台持续运行、跨聊天推送或定时任务。

本轮实际执行次序如下。已有 attempt / evidence / reveal 文件的命令会拒绝重复执行：

```text
python scripts/codex_review.py prepare
python scripts/codex_review.py run calibration
python scripts/codex_review.py audit calibration
python scripts/codex_review.py reveal calibration
python scripts/codex_review.py run validation
python scripts/codex_review.py audit validation
python scripts/codex_review.py reveal validation
python scripts/codex_review.py run facts
python scripts/codex_review.py audit facts
python scripts/codex_review.py run diagnosis
python scripts/codex_review.py audit diagnosis
```

独立的 validation 与 facts 可以并行；诊断只在事实报告冻结及核对后运行，但不接收
事实报告或冷读报告，只接收自己的分配材料。每一项只完成一次评审报告。
`run` 需要可用的本地 Codex、已有登录与获准的宿主模型传输联网；缺少时如实阻断，
不能用角色扮演或同上下文复核冒充独立调用。

复用适配器进行后续评测时，先取得一个新的明确任务授权，冻结新的允许名单包、
新的 task_id、来源 HEAD 和独立结果目录；不得重用本轮已消费 ID。
新清单在现有字段之外增加 `result_dir` 和绑定授权回执的 `authorization` 引用。
授权回执必须记录 `authority.source=ACTUAL_CURRENT_USER_INSTRUCTION`、与清单相同
的 task_id、明确的三种 `authorized_work_kinds`，以及新正文未授权、旧RC3剩余0轮、
旧197字保护未解除。按 `--manifest config/<新清单>.json` 调用 run/audit/reveal。
协调者负责冻结新清单及人工核对，脚本不自动创建授权、不生成新稿、不修订业务状态。

专业资料与公开技能的实际读取、采用点和限制见
[专业学习记录](NOVEL_REVIEW_PROFESSIONAL_LEARNING_20261003.md)。外部技能未安装到
评审配置，也未作为自动钩子执行。
