# Synthetic fixtures only

V1 tests generate tiny TXT, EPUB, DOCX, Markdown, encoding, duplicate, and chapter-heading fixtures at runtime.
No real novel text, private sample, benchmark holdout, or generated benchmark run belongs in this directory.

`golden/novel_preprocessor_golden_v1.txt` 是完全合成、可公开提交的章节检测 Golden，不含真实小说正文。其字节级 SHA-256 和预期章节契约固定在同目录 expected JSON；测试禁止修改 fixture 内容迁就算法。
