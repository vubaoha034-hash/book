# 修仙重生商业网文：既有学习原件复核与取舍（2026-11-02）
**状态：RESEARCH_AND_METHOD_PLAN_ONLY；NO_NEW_PROSE。**

## 为什么要返工
用户最新明确纠正：题材“修仙、重生、短剧方向有兴趣”≠先前正文可用，尤其批评“这个悬疑反转什么都没有”；禁止直接续写，要求先有完整大纲、人物设定，并调用以前确实学习过的教程和 Skills。原话及精确原稿绑定在 `book/main/state/review_receipts/NOVEL_FANTASY_INTEREST_NOT_PROSE_APPROVAL_OUTLINE_FIRST_20261102.json`。以前438汉字钩子与923汉字续写属于试验事实/失败诊断材料，不是未来卷纲的权威故事合同；正文均保留不覆盖。

## 已经学过的内容（2026-11-02真实回读，不重新造一套）
- 生产 V3 `SKILL.md`；`workflows/05-deep-story-dissection.md`、`workflows/02-extract-techniques.md`：原有`读者承诺→悬念地图→反转时机→因果→奖励兑现`，明确不能只总结“节奏快、人物鲜明”。
- `rules/suspense-reversal-payoff.md`：锁/真钥匙/假钥匙/代价/新锁，公平伏笔与回收；反转必须改变前文理解、人物选择及代价格局。最重要的旧资产，应迁入**结构设计**，不能只在稿后打勾。
- `rules/reader-reward-rhythm.md`、`modules/emotion-payoff-ledger.md`：真正兑现改变权力、资源或选择权，不能只靠“众人震惊”；旧百分比/固定字数样表仅作为分析镜头，不是逐章写作配额。
- `modules/character-pressure-test.md`：角色当前想要、误解、秘密、底线、成本、合理替代方案；可做人物压力测验。
- `modules/causal-proof-engine.md`、`modules/developmental-editor.md`：先检查故事脊柱和无理由降智，不要修辞代替剧情。
- `modules/continuity-editor.md`：谁在何时知道什么、法宝/契约位置、能力触发条件和交易代价。
- `modules/beta-reader-panel.md`：独立阅读与同上下文模拟区别，机器不能伪称真人评分。
- 2026-10-01已做过9个上游仓库实证筛查，候选合同在`docs/NOVEL_METHOD_UPSTREAM_LINEAGE_EXECUTION_CONTRACT_20261031.md`；已有 wgwtest/novel-writing (MIT,pin 838729695148008d42c01bd7c3c0c1a5c15de830) 人物选择，zenstory-ai/oh-story-claudecode (MIT,pin cc6397f2b07179262287f4ca358d281b16205765) 分层写作审稿，huahuakandaima/human-novel-writer (MIT,pin 3e74b95d014923525e0bd19a38203e724152fe54) 仅用人物知识边界。具体 V4 候选并未被真人验证通过。
- 既有中文长篇蒸馏任务曾导入《凡人修仙传》《诡秘之主》等受版权保护作品到私有 Drive；**本次未重新读取其原文，也不在公共仓库上传任何原文、分章复制或声称从它们刚抽出新规律。**

## 2026-11-02重新核查的外部教程/Skills（不复制原文）
| 来源 | 原始链接 | 可验证的操作方法 | 只采用什么 | 不采用什么 |
|---|---|---|---|---|
| 番茄作家课堂课程入口 | https://fanqienovel.com/writer/zone/tutorial?tab=1 | 官方按开书准备、人物、伏笔、时间线、长篇防崩文分课程 | 先故事后章节的编辑顺序 | 只看热度就认定写法有用 |
| 番茄《写在落笔前，如何构思一本男频网文小说》 | https://fanqienovel.com/writer/zone/article/7226296687315124284 | 一句概括→故事支点（人、世界、金手指、悬念、激励事件）→切入事件→大纲 | 商业承诺与故事支点 | 一堆标签替代真正因果 |
| 番茄《写作之路千千万，选对题材好开篇》 | https://fanqienovel.com/writer/zone/article/7551631577109774398 | 为同一核心梗让不同人物的利益和恐惧互相撞击，人设经具体选择证明 | 利益/秘密/关系三角；角色压力测试 | 只有角色简历、没有冲突 |
| 番茄《新手写作第一步？先动笔再说！》 | https://fanqienovel.com/writer/zone/article/7571294020903632958 | 人物行动的具体细节承担因果；事件过度压缩使转折生硬 | 反转前保留必要细节，避免空心快节奏 | 把“越短越好”当定律 |
| 番茄《超短故事创作指南：从概念到导语》 | https://fanqienovel.com/writer/zone/article/7571725833107144766 | 短篇6000—80000字/导语200—500字/章节的小承诺与反转 | 区分短篇模板与长篇修仙的不同产品形态 | 机械将其模板套长篇 |
| 番茄《第十七期短故事作家课堂：悬疑氛围》 | https://fanqienovel.com/writer/zone/article/7630658594882453528 | 真线索、错误解释、逐步调查、结局反证 | 三层悬疑错位及公平线索 | 只到结局突然揭露从未出现的新规则 |
| 番茄《短故事改编风向标》 | https://fanqienovel.com/writer/zone/article/7667852365159989310 | 微创新的世界规则要可描述、可视化、可重复产出困境 | 修仙金手指的触发/界限/代价 | 为短剧画面牺牲小说人物真实动机 |
| danjdewhurst/story-skills | https://github.com/danjdewhurst/story-skills | story bible、character、worldbuilding、plot、promises/payoffs、chapter cards、continuity state | 独立总纲、人设、世界规则、角色知识/物件状态 | 整包默认安装、自动全书生成、机械过度校验 |
| guantoubaozi/novel-writing | https://github.com/guantoubaozi/novel-writing | 用户主导先结构与人设，按权限规划到具体章节；追踪角色关系、知识、线索 | 由总纲到细纲；章节前读最小相关资料 | 在小说未验证前就自称质量达标 |
| Xuanhuan Novelist | https://skillhub.360.com/skills/xuanhuan-novelist | 修炼境界/金手指/势力地图/越级战斗/成长路线分开设计 | 修仙强度边界、弱主角成长阶梯和爽点类型轮换 | “每章必须打脸/越级/升境界”重复配方 |
| novel-writer-engine | https://skillhub.360.com/skills/novel-writer-engine | 大纲→分卷→章节细纲→单章生成→状态更新 | **先纲后文**，不同粒度独立权威文件 | 硬性字数或固定数量反转/审核打分 |

**可靠性区分：** 番茄官方课程=平台建议和作者经验，不是保证签约/收益；开源Skill的功能说明=自述，尚没有我们自己的独立真人长篇成功证据；这份研究=内容采样及转移方法选择，不是“AI学会写爆款”的证明。任何开源代码若实际复制需许可证和来源，本文只使用抽象方法。

## 立刻实行的唯一流程（防上次跳章错误）
`用户认可题材` → `一句话商业承诺/核心事件` → `角色决策卡+关系秘密` → `世界规则与修炼/代价` → `总纲/分卷/终局` → `真线索-假解释-反转-回收表` → `首12章章节卡` → `因果/简单方案审查` → `人类确认大纲` → `按单章独立写作` → `冻结正文后独立诊断+真人验证`。
- 协调者可以读取全部诊断及市场研究；实际章节作者只接收**本章**必要世界规则、当前角色知识/状态、章节目标/代价、前一章最后状态与该章允许伏笔。不得把长期反证库、负面AI评语、每500字钩子等塞进写手上下文。
- 每章正文冻结后，先核角色知识/资源/因果，之后才审语言；未经用户批准不得连续产出下一章。
- 真人结论必须绑定具体章节及SHA；题材方向正向≠该章正向，数字评分 UNKNOWN≠判定PASS。
- 旧438字开篇与923字试续均为原件，不修改也不视为“计划内容必须按它演”。
- 当前只完成研究、策划和文档；绝不生成新章节，也不绕过 `book/main` 检查点211的原生任务。
