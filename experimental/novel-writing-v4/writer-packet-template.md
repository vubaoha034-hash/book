# 单场独立写作者输入｜模板（候选）

> 模板由 EDITOR 填写。只把【交给写作者】以内的字段送给新鲜写作上下文。设计诊断、上轮差评、评分表和模式禁令禁止混入。未填的重大事实标明未知并退回编辑，不能让模型自补核心设定。

## 【编辑侧保管，不交给写作者】
- run_id：
- source_commit / task_contract：
- parent_manuscript / sha256：
- original_human_positive_anchor / scope / hash（可空）：
- historical_negative_examples（不共享给作者）：
- review_map_secret：
- user_authorization / protected_story_facts：
- model settings / execution receipts：

## 【交给写作者】
### 本场环境与上场结束时的事实
- 时间、地点、人物关系、公开限制：
- 已经发生的事（只写可核对事实，不作作者讲解）：
- 此场之前读者知道什么：

### 每个人正在考虑什么
| 人物 | 眼前想做的事 | 不想让对方知道的顾虑 | 要保住的利益/关系 | 此刻知道/误解 | 最简单办法为何不选 |
|---|---|---|---|---|---|
| A |  |  |  |  |  |
| B |  |  |  |  |  |

### 本场必须成立的事件
- 为什么此刻碰上：
- 两个眼前打算在哪里相抵触：
- 哪个安排/权利/关系将在本场真正改变：
- 没解决而带往下一场的压力：
- 必须遵守的固定事实与不允许新增的大设定：
- 可自由决定的情节动作、对白、心理与叙事节奏：

### 交付
- 只写一个场景；目标长度：
- 允许自然长短句、适度心理和有功能的细节。
- 对白必须出自角色意图、知识和关系，不是替读者逐条解释信息。
- 不必每段都有反转，不强制一问一答、动作伴奏、物件象征或意义收尾。
- 写到上面实际变化发生的位置便停止；不要私自增加下一场/新秘密。
- 直接交付正文，不把故事设计说明写进小说。

## 【写后由编辑填写】
- frozen_output_sha256：
- factual/continuity gate：
- narrative gate（具体引文）：
- AI-smell located evidence（三层：因果/主次/语言）：
- revision child sha256 + diff：
- cold-reader independent context verified：
- human exact verdict bound to version：UNKNOWN / PARTIAL / PASS / FAIL
- next legal action：
