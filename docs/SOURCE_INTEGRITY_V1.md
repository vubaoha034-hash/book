# Source Integrity Gate V1

Source Integrity Gate 是独立于“文件已成功解析和分章”的机械门禁。它只根据可靠的强章节编号判断书源是否具备进入蒸馏阶段的最低完整性证据，不进行文学分析，也不猜测或补写缺章。

## 输出

每个 processed work 在 `work.json`、私有 state 和私有 manifest 中记录：

- `source_integrity_status`: `PASS | WARNING | FAIL | UNKNOWN`
- `distillation_allowed`: 仅 `PASS` 为 `true`
- `source_integrity`: 方法版本、置信度、数字章节数、估算缺章数、跳号/重号/倒退计数、规律性缺章标志和 reason codes

## 固定阈值

代码常量位于 `src/novel_preprocessor/integrity.py`：

- 最少可靠数字章节数：2
- 数字强标题占全部切分章节的最低比例：0.60
- 判定规律性缺章的最少 gap 事件：3
- 重复 gap 的单次最少缺章数：5
- 相同 gap 规模占全部 gap 的最低比例：0.60
- 估算缺章占“检测章节 + 估算缺章”的最低比例：0.10

只有以上规律性缺章条件同时成立才因系统性缺失判为 `FAIL`。单一跳号、重号或倒退只判 `WARNING`，不会因为一个异常直接 FAIL。数字标题不足或占比过低时为 `UNKNOWN`。番外、后记等特殊结构本身不触发 FAIL。

`estimated_missing_chapters` 是相邻强章节编号向前跳跃量减一的总和；它是机械估算，不证明缺失内容的具体文本或来源。

## 门禁策略

- `PASS`: `distillation_allowed=true`
- `WARNING`: 需要人工确认，禁止蒸馏
- `FAIL`: 存在强系统性缺失证据，禁止蒸馏
- `UNKNOWN`: 编号证据不足，禁止蒸馏

ChatGPT Packet 导出严格遵守该字段，本版本没有 force bypass。
