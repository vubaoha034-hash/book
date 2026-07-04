# Workflow 01 — Ingest Book

## Goal

把用户放入 `sources/books/` 和 `sources/notes/` 的资料提取成可读文本，并建立索引。

## Steps

1. Check dependencies:

```bash
python3 scripts/ingest.py --check
```

2. Extract sources:

```bash
python3 scripts/ingest.py sources/books sources/notes
```

3. Read generated files:

```text
library/source-register.md
library/source-register.json
library/_extracted/*.md
```

4. Report:

```text
成功导入：
失败文件：
格式：
字数：
下一步建议：分析技巧 / 建立技巧库 / 诊断用户稿件
```

## Failure Handling

- PDF 失败：提示安装 `pypdf` 或系统 `pdftotext`。
- DOCX 失败：提示安装 `python-docx`。
- EPUB 失败：提示安装 `beautifulsoup4`，或改用 txt/md。
- 文件太大：分章节分析，不一次读完整本。
