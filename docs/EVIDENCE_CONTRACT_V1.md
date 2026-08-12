# Evidence Contract V1

## Coordinate space

未来 Scene/Story Card 的 `EvidenceRef.source_span` 只允许指向私有结构化章节 TXT，不指向整本书、原始字节、EPUB XML 或 DOCX XML。

固定语义：

```text
span_scope = "chapter_text"
start_char = 0-based inclusive
end_char = 0-based exclusive
字符单位 = Python 对结构化章节字符串的切片单位
quote = chapter_text[start_char:end_char]
quote_sha256 = SHA-256(quote UTF-8 bytes)
```

EvidenceRef 必需字段：

```json
{
  "work_id": "wrk_...",
  "chapter_id": "ch_...",
  "chapter_text_sha256": "64 lowercase hex characters",
  "span_scope": "chapter_text",
  "source_span": {"start_char": 0, "end_char": 10},
  "quote_sha256": "64 lowercase hex characters"
}
```

公开 Card 不保存大段小说原文，只保存 Hash 和位置。`scripts/validate_evidence_refs.py` 会在 `_private\02_结构化文本` 中定位章节，验证章节 Hash、非空且不越界的坐标、引用切片 Hash，并完成 round-trip。

## Epistemic status

重要解释性 claim 必须携带：

- `claim_type`
- `epistemic_status`
- `confidence`
- `evidence_refs`

枚举语义：

- `observed`：结构化章节文本可以直接支持的事实或结构现象；
- `inferred`：根据证据作出的解释，例如人物目标、动机或情绪；
- `hypothesis`：跨场景或机制层面尚待更多证据验证的假设。

Scene Card 的人物目标/动机、情绪解释、setup/payoff，以及 Story Card 的因果解释、情绪曲线、可复用机制、失败模式和反例解释都受此约束。Schema 不会把简单 ID、标题或纯统计字段强行包装为 claim。

## Validation commands

```powershell
python scripts/validate_card_schemas.py
python scripts/validate_evidence_refs.py --private-root E:\蒸馏小说\_private card.json
```

JSON Schema 验证负责字段、枚举和基本类型；Evidence semantic validator 负责坐标先后、章节长度和实际 Hash，因此两者不能互相替代。
