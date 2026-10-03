检查点199：刘先生明确要求连续完成直到实际人工审核，常规中间环节不再询问授权。已完成唯一390字新开头与不同上下文的AI编辑、匿名AI读者及事实审查，原报告/证据/状态已保存。实际Sol / Max经运行核对；主写1、内部修订0，新稿真人UNKNOWN。接续[当前结果](docs/NOVEL_AUTONOMOUS_REVIEWED_OPENING_TO_HUMAN_RESULT_20261003.md)及[执行方式](modules/autonomous-to-human-review.md)，交付这份正文后收实际阅读反馈；AI赞成不晋级质量门。旧稿、197字保护、旧额度0、方法4、故事目标、既有真人FAIL和404未知保持。读取不重跑，不继续生成或扩到完整场景/V5。

历史检查点197。395字新短段已被刘先生明确否决：AI味重、情绪平、互动像机器人。已主动读取专业资料并完成一次独立Sol / Max的已知失败后诊断、证据核对及[人物反应与快节奏方法准备](docs/NOVEL_EMOTION_PACING_PROFESSIONAL_STUDY_20261003.md)。写作预算0，方法4与原故事/旧锁保留；未来一份短段的具体范围已准备，尚需新预算。学习不等于质量改善，原404字仍UNKNOWN。接续见[入口](START_HERE.md)和[结果](docs/NOVEL_EMOTION_REACTION_DIAGNOSIS_RESULT_20261003.md)。

检查点198已按刘先生新要求接入两个实际独立AI角色：编辑读取必要事实和已知失败，匿名读者只看正文；原报告互不传递。实际Sol/Max已核对。编辑REVISE、AI读者YES与真人不想继续的FAIL不一致，不能晋级质量门。见[当前结果](docs/NOVEL_TWO_ROLE_OPENING_REVIEW_RESULT_20261003.md)及[调用方式](modules/two-role-opening-review.md)。取用固定提交的story-review/reader-sim，未安装整套规则。已推进一份既有姓名错位入口和冻结输入准备；当前预算零，后续写作者只读prepared_input.writer_packet。新版本开头重排须新的一次范围和预算，旧稿/197字保护和旧额度不变。读取不重跑，原评审各一次已消费。

# Novel Writing Master V3

这是一个面向中文小说、公众号短篇、网文和短剧化故事的 Agent Skill。

V3 不再用“阶段很多、清单很多、自评分很高”证明小说好看，而是要求四类可核查证据：

1. **因果证明**：每个关键场景由前置事实和人物选择逼出，并解释为什么不用更简单办法。
2. **情绪欠账与兑现**：读者被压了什么、在等什么、最后什么真实改变。
3. **恨感与共情**：伤害者是否主动、明知、获益并加码；主角是否有普通欲望、真实缺点和有代价选择。
4. **个人审美指纹**：认可样本、拒绝样本和当前稿三方比较；没有样本时不冒充已经学会用户文风。

V2 文件继续保留，旧调用方式仍可使用；新任务默认走 V3。

原有的资料导入、技巧库和深度拆书能力继续保留；V3 主要重做新故事生产、审稿证据和去 AI 终审。

## 当前项目唯一主线

《第二套过去》当前按 [MAINLINE.md](MAINLINE.md) 执行：保留故事契约、因果与连续性证据，补齐具体生活事实，解除八步动作对新正文的硬约束，先测一场，再测不同压力类型。只有冻结测试的实际失败才修改对应方法；新聊天从 [START_HERE.md](START_HERE.md) 继续，不按旧阶段号重开。

主线与入口已保存不等于文风有效。真人阅读结果、结构检查、单场通过和长篇验证分别记录。

2026-10-01：方法1 TEST-01 已被真人否决：不想读、拖拉、机器人问答。见 [原稿](delivery/mainline-v1/test-01-sp414-s02-a1.md)、[实际失败回执](state/review_receipts/NOVEL_MAINLINE_TEST01_A1_HUMAN_FAIL_20261001.json) 和 [主要失败定位](docs/NOVEL_MAINLINE_TEST01_A1_FAILURE_DIAGNOSIS_20261001.md)。[方法修订2](docs/NOVEL_MAINLINE_METHOD_V2_20261001.md)的[唯一短段](delivery/mainline-v2/test-01-sp414-s02-short-a1.md)也被真人否决：无情绪、僵尸对话。见 [实际反馈](state/review_receipts/NOVEL_MAINLINE_V2_TEST01_SHORT_A1_HUMAN_FAIL_20261001.json)和[两版对照](docs/NOVEL_MAINLINE_METHOD02_EMOTIONAL_RESPONSE_FAILURE_20261001.md)。原件全部保留。方法3随后获得明确开头留存否决；当前修订号4，唯一短段保持冻结，已完成外部证据审稿但真人结果UNKNOWN；其后的旧RC3两轮已用尽，448字稿实际情绪/留存FAIL；检查点194完成接入与诊断，检查点195完成唯一事实/入口准备，检查点196另获一次新短段授权并已完成395字正文与独立事实核对。该快照后来由检查点197的395字实际FAIL接续；完整场景和TEST-02仍不可执行。

## V3 解决什么

- 逻辑表面通顺，实际一问就能解决。
- 主角只会受苦，没有主动选择。
- 反派只靠标签变坏，读者恨不起来。
- 所谓爽点只是旁人震惊、反派脸色难看。
- 情绪一直压，却没有对应的偿还。
- 自己写、自己审、自己给高分，形成假通过。
- 去 AI 时机械增加动作、物件、短句，反而产生新型 AI 腔。
- 一轮同时改剧情、逻辑、节奏和文风，越改漏洞越多。

## 完整流程

```text
故事契约
→ 因果证明
→ 情绪欠账与兑现
→ 恨感 / 共情
→ 场景计划
→ 分场正文
→ 开篇冷读
→ 读者镜头
→ 连续性审查
→ 高影响修改
→ 个人文风与去 AI
→ 最终复核
```

详细流程：

```text
workflows/07-novel-master-pipeline-v3.md
```

机器可读闸门：

```text
config/novel-quality-gates.v3.json
```

证据模板：

```text
templates/v3-evidence-packet-template.md
```

## 四个新增核心模块

### 因果证明器

每场回答：

```text
前置事实 → 人物选择 → 未选简单方案及原因
→ 立即后果 → 新限制 → 逼出的下一场
```

### 情绪与兑现账本

每笔情绪债回答：

```text
谁让读者压抑 → 读者在等什么 → 何时部分偿还
→ 最终如何偿还 → 权力/关系/选择/利益/代价发生什么变化
```

### 恨感与共情测试

恨感依赖主动伤害、获益、推责和加码，不依赖旁白骂人。共情依赖普通欲望、缺点、代价和选择，不依赖悲惨履历堆叠。

### 个人审美指纹

个人样本必须保存在私有环境；这个公开仓库只提供方法和空白模板。样本为空时，Skill 必须明确说明尚未学到个人声音。

## 真实的读者复核

只有新上下文、子代理或真人反馈才可称为“独立读者”。同一上下文中扮演四个人，只能称为“模拟读者镜头”，不得用四份高分证明作品通过。

## 去 AI 原则

去 AI 默认最后执行，每轮最多处理五个高影响模式。具体物件和动作不是越多越真实；没有人物专属性、场景压力或后果的动作，同样是模板。

## 安装

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.agents/skills/novel-writing-master
```

Claude Code 可安装到 `~/.claude/skills/novel-writing-master`，GitHub Copilot CLI 可安装到 `~/.copilot/skills/novel-writing-master`。

## 验证

```bash
python scripts/validate_skill.py
python scripts/verify_current_state.py
python -m unittest discover -s tests -p 'test_*.py'
```

这个脚本只验证技能结构、V3 配置和关键交叉引用。它会明确说明：**结构验证通过不等于小说质量通过**。小说质量仍必须由具体文本证据证明。

## 版权与隐私

- 只学习抽象技法，不复制第三方作品。
- 不模仿在世作者可识别的个人风格。
- 不把私有原书、完整提取文本或个人审美样本提交到公开仓库。
