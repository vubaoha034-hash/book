# Novel Preprocessor V1

## 边界

本程序只做确定性的本地工程处理：文件发现、格式提取、机械清洗、章节定位、Hash、ID、基础去重、结构化输出、Manifest 和证据地址。它不阅读或判断文学内容，不调用 OpenAI、付费 API、在线 LLM 或其他网络服务。

## 固定目录

```text
E:\蒸馏小说
├─ 01_导入并预处理小说.bat
├─ repo\                         Git 仓库
└─ _private\                    永不进入 Git
   ├─ 01_原始小说\              用户输入
   ├─ 02_结构化文本\            work.json / chapters.jsonl / text
   ├─ cache\                    增量状态
   ├─ temp\                     原子写入暂存
   ├─ logs\                     每次运行的机器日志
   └─ 09_Benchmark\             从旧项目保留的本地 Benchmark 私有资产
```

`repo\benchmark\_private` 是指向外部 `E:\蒸馏小说\_private\09_Benchmark` 的兼容目录联接；真实文件物理上不在 Git 仓库中。

## 支持状态

| 格式 | V1 状态 | 说明 |
|---|---|---|
| TXT | 支持 | UTF-8/BOM、GB18030、GBK、Big5 严格解码 |
| Markdown | 支持 | 保留 Markdown 正文；标题可作为章节候选 |
| EPUB | 支持 | 按 OPF spine 提取；跳过高置信 nav/toc |
| DOCX | 支持 | 直接解析 OpenXML；读取可靠 core metadata |
| PDF | 条件支持 | 本地 `pypdf` 可用且 PDF 含可提取文本 |
| 扫描/图片 PDF | 不支持 | V1 不做 OCR，明确失败并提示 |
| MOBI/AZW/AZW3 | 延后 | 记录 `unsupported/deferred`，不假装成功 |

## 输出契约

每个成功作品写入 `_private\02_结构化文本\<work_id>\`：

```text
work.json
chapters.jsonl
text\0001.txt
text\0002.txt
...
```

`work_id` 来自标准化正文 SHA-256；`chapter_id` 来自标准化正文 SHA-256 与章节序号。相同正文重复执行或改名后执行，ID 保持一致。每个输出保存原文件、标准化正文和章节正文 SHA-256。

仓库内的 `manifests\library_manifest.jsonl` 只含 ID、metadata、Hash、统计、状态与私有相对引用，不含正文或私有绝对路径。

## 章节策略

引擎先做整行标题候选检测，再处理卷标记与章标题关系，最后检查候选位置和分段长度。它支持“第一章”“第1章”“第一回”“第十二回”“Chapter 1”“卷一”“第一卷”“序章”“楔子”“番外”“后记”等形式。

无法可靠切分时只输出一个完整 fallback 章节，并写入：

```json
{
  "chapter_detection_confidence": "low",
  "needs_review": true
}
```

程序不会为了增加章节数而用单一正则暴力切分，也不会改写标点、句子或作者语言习惯。

## 增量与重复

- 路径与原文件 Hash 均未变化：跳过。
- 文件内容发生变化：重新提取并生成对应版本的确定性 work ID。
- 原文件 SHA-256 相同：`exact_file`。
- 标准化正文 SHA-256 相同：`normalized_text`。
- 重复只标记，不自动删除任何源文件或结构化版本。

## 安全验证

```powershell
python scripts/validate_private_boundaries.py
python scripts/validate_step01.py
```

验证会检查 Git tracked 与 staged 集合；任何 `_private`、小说归档格式、`sources/books` 原书或完整结构化章节正文都会导致 FAIL。测试素材均为运行时生成的极短合成文本。
