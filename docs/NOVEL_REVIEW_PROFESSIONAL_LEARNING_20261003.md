# 本轮专业资料与成熟技能学习记录

任务：NOVEL-CODEX-REVIEW-INTEGRATION-AND-R2-DIAGNOSIS-20261003-01。依据刘先生本轮补充要求，遇到问题主动寻找成熟技能和专业知识。本轮已实际读取以下来源；没有安装外部插件、执行外部 hooks，或更换主线。

## 专业编辑依据

- [Editors Canada 结构编辑 B2.1/B2.2](https://editors.ca/publications/professional-editorial-standards/structural-editing/)：按读者、媒介和目的识别缺口，核查可疑事实。本轮落实为第二场摘录范围、来源绑定及事实审查，不把未展示内容判成矛盾。
- [Editors Canada 文体编辑 C1/C3.1/C5.1–5.4](https://editors.ca/publications/professional-editorial-standards/stylistic-editing/)：必要的最小改动、保护声音、核对实际阅读效果。本轮落实为引文、影响、最小目标、保护项与复验条件；动作存在不等于情绪成立。
- [CIEP 小说编辑能力 3.1，PDF第38–39页](https://www.ciep.uk/asset/3927EFC9-256D-4660-9F4687833A2A2FA7/)：尊重创作意图，区分编辑层级，检查人物、视角、对白及时间/设定一致性。本轮只做局部诊断，不据448字判断全书结构或否定题材。

这些标准已经是原协议的专业来源，本轮重新读取核对，沿用 `docs/NOVEL_EXTERNAL_REVIEW_PROTOCOL_V1_20261001.md`，不重建规则体系。手机首屏及刘先生口味由本项目真实反馈定义，不宣称是上述机构的通用字数公式。

## 实际读取的成熟技能

来源 `haowjy/creative-writing-skills`；读取时远端HEAD仍为 `0d5bf7fd987554e05db7e05d569736e648297722`。固定到该提交读取：

| 文件 | Git blob | 本轮采纳及限制 |
|---|---|---|
| [story-review/SKILL.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7fd987554e05db7e05d569736e648297722/skills/story-review/SKILL.md) | 84af4da8a6a42e67e80e59439e51acd61d82624a | 诊断与写作分开，先确定评审层级；冷读体验单独运行。 |
| [developmental-edit.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7fd987554e05db7e05d569736e648297722/skills/story-review/resources/developmental-edit.md) | df9407cefc95b8c70cc89e33533739c2b8c12244 | 区分场景选错与呈现不成立；上游问题不靠润色修复。其全稿前提限制本轮只能提出摘录层级假设。 |
| [reader-sim-signal.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7fd987554e05db7e05d569736e648297722/skills/story-review/resources/reader-sim-signal.md) | 0e36bfb3794149b010ee0ee1b039acdd419336ee | 区分读者体验的位置与编辑解释；单次体验有范围。该技能对AI体验可靠性的主张不作为本项目证明，AI不能替代真人或推翻真人否决。 |

本轮先冻结提示词，再回收结果及揭示标签。上述资料只帮助协调者核查和解释，不根据已揭示标签改提示词反复调用同批样本。没有同类真人认可正例，仍不能验证误杀率或学会个人文风。

## 工程问题的专业核查

按 OpenAI Docs 技能读取了[模型说明](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[CLI命令说明](https://learn.chatgpt.com/docs/developer-commands?surface=cli)、[配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)，并使用本机CLI生成的实际app-server接口schema。官方文档支持模型和参数形式，不证明本账号实际可运行；实际设置必须以本轮服务返回值和报告为准。

只读工程子代理使用独立 `fork_turns=none`、工具参数指定 `gpt-6.1-sol` / `max` 查接入故障，未承担文学评审。外层受限终端的账户路由发现失败；经自动审批允许宿主联网后，现有登录的只读 `account/read(refreshToken=false)` 成功。修复的是协调者宿主网络，评审仍为只读、禁用工具网络、不继承聊天。原始失败及探针分别保存，不能计为成功报告。
