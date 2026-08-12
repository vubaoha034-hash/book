# Novel Writing Master V3

这是一个面向中文小说、公众号短篇、网文和短剧化故事的 Agent Skill。

V3 不再用“阶段很多、清单很多、自评分很高”证明小说好看，而是要求四类可核查证据：

1. **因果证明**：每个关键场景由前置事实和人物选择逼出，并解释为什么不用更简单办法。
2. **情绪欠账与兑现**：读者被压了什么、在等什么、最后什么真实改变。
3. **恨感与共情**：伤害者是否主动、明知、获益并加码；主角是否有普通欲望、真实缺点和有代价选择。
4. **个人审美指纹**：认可样本、拒绝样本和当前稿三方比较；没有样本时不冒充已经学会用户文风。

V2 文件继续保留，旧调用方式仍可使用；新任务默认走 V3。

原有的资料导入、技巧库和深度拆书能力继续保留；V3 主要重做新故事生产、审稿证据和去 AI 终审。

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

## Novel Distillation Benchmark V1

新增的 `benchmark/` 是独立验收层，不替换 V3，也不允许在 Baseline 阶段重写蒸馏核心。

它用于把现成小说分析/蒸馏方案放进同一考场，固定：

- 100 分评分维度；
- Source / Coverage / Evidence / Holdout / Reproducibility / Experiment / Review / License 硬门禁；
- Development、Style Holdout、Future Holdout 三类数据隔离；
- 同输入、同模型、同预算的直接比较；
- 一次只改一个主要变量；
- 匿名新章盲测；
- 不提升就回滚的 Regression Gate。

入口：

```text
benchmark/README.md
benchmark/TEST_PLAN_V1.md
benchmark/config/scoring.v1.json
benchmark/config/upstreams.v1.json
```

结构验证：

```bash
python scripts/validate_benchmark.py
```

Benchmark 的 100 分只代表冻结测试体系内的满分；隐藏集明显下降时，必须按隐藏集结果回退，不能拿开发集满分冒充真实能力。

## Novel Preprocessor V1（本地预处理）

STEP-01 新增了一个与文学分析严格分离的本地预处理层。它只负责：

- TXT、EPUB、DOCX、Markdown 与可提取文本 PDF 的本地解析；
- 保守的机械清洗、章节候选检测、低置信 fallback 和人工复核标记；
- 绑定 processing fingerprint 的作品/章节确定性 ID、SHA-256 与基础去重；
- 私有结构化章节输出、版本失效增量状态和 private-first Manifest；
- Scene Card / Story Card 空 Schema 与 Git 私有资料防泄漏检查。

新的固定工作目录是 `E:\蒸馏小说`。Git 仓库位于 `E:\蒸馏小说\repo`，原书、结构化全文、缓存和日志位于仓库外的 `E:\蒸馏小说\_private`。把有权使用的文件放入 `E:\蒸馏小说\_private\01_原始小说`，然后双击根目录的 `01_导入并预处理小说.bat`。

命令行入口：

```powershell
python scripts/preprocess_novels.py --repo-root E:\蒸馏小说\repo --private-root E:\蒸馏小说\_private
```

工程与隐私验证：

```powershell
python -m unittest discover -s tests -v
python scripts/validate_private_boundaries.py
python scripts/validate_step01.py
```

Evidence Contract V1 固定为章节相对、0-based、end-exclusive 坐标，并要求章节/引用 Hash；重要解释性 claim 区分 `observed`、`inferred` 与 `hypothesis`。本地导出桥可按显式 work ID 生成私有、可分块重组的手工上传包：

```powershell
python scripts/export_chatgpt_packets.py --private-root E:\蒸馏小说\_private --work-id wrk_xxx
```

导出前执行 Source Integrity Gate V1：只有 `source_integrity_status=PASS` 且 `distillation_allowed=true` 的结构化作品允许生成 Packet；非 PASS 作品默认阻断，本版本没有强制绕过。

详细说明见 `docs/PREPROCESSOR_V1.md`、`docs/EVIDENCE_CONTRACT_V1.md` 和 `docs/CHATGPT_PACKET_EXPORT.md`。所有程序均不调用在线 AI/API，也不会生成摘要、评分、人物分析、情绪曲线或 Novel DNA。

## 安装

```bash
git clone https://github.com/vubaoha034-hash/book.git ~/.agents/skills/novel-writing-master
```

Claude Code 可安装到 `~/.claude/skills/novel-writing-master`，GitHub Copilot CLI 可安装到 `~/.copilot/skills/novel-writing-master`。

## 验证

```bash
python scripts/validate_skill.py
```

这个脚本只验证技能结构、V3 配置和关键交叉引用。它会明确说明：**结构验证通过不等于小说质量通过**。小说质量仍必须由具体文本证据证明。

## 版权与隐私

- 只学习抽象技法，不复制第三方作品。
- 不模仿在世作者可识别的个人风格。
- 不把私有原书、完整提取文本或个人审美样本提交到公开仓库。
