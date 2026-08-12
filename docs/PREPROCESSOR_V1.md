# Novel Preprocessor V1

## 边界

本程序只做确定性的本地工程处理：文件发现、格式提取、机械清洗、章节定位、Hash、ID、基础去重、结构化输出、Manifest 和证据地址。它不阅读或判断文学内容，不调用 OpenAI、付费 API、在线 LLM 或其他网络服务。

## 固定目录

```text
E:\蒸馏小说
├─ 01_导入并预处理小说.bat
├─ 02_生成ChatGPT蒸馏包.bat
├─ repo\                         Git 仓库
└─ _private\                    永不进入 Git
   ├─ 01_原始小说\              用户输入
   ├─ 02_结构化文本\            work.json / chapters.jsonl / text
   ├─ cache\                    增量状态
   ├─ temp\                     原子写入暂存
   ├─ logs\                     每次运行的机器日志
   ├─ manifests\                真实私有书库 Manifest
   ├─ 03_ChatGPT蒸馏包\         用户手工上传包
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
front_matter.txt                 可选；仅在首章前存在材料时生成
chapters.jsonl
text\0001.txt
text\0002.txt
...
```

`work_id` 来自标准化正文 SHA-256，代表 **normalized work content version**，不是脱离版本的永久作品身份。`chapter_id` 同时绑定作品正文 Hash、章节序号、章节正文 Hash、全书边界和 processing fingerprint。相同契约、相同章节文本和相同边界会得到相同 ID；章节正文、边界或处理契约改变时，章节 ID 改变。

真实书库 Manifest 默认写入 `_private\manifests\library_manifest.jsonl`，不会让 Git 工作树随导入发生变化。仓库内只保留空模板 `manifests\library_manifest.jsonl`、合成 example 和 Schema。

## Processing Contract

`processing_contract_version` 与 `processing_fingerprint` 覆盖 extraction、normalization、chapter segmentation、ID contract 和 structured output schema。只有源文件 SHA-256 相同、处理指纹相同，而且 `work.json`、`chapters.jsonl`、所有章节文件及 Hash 全部完整时才允许增量跳过。处理指纹变化或 artifact 缺失会原子重建结构化目录。

处理指纹不是源代码自动探测器。以后只要修改 `extractors.py`、`cleaning.py`、`chapters.py`、ID 生成契约或结构化输出字段，就必须同步提升 `ProcessingContract` 中相应 component；忘记提升 component 时，fingerprint 不会自动发现代码变化。

## 章节标题与 front matter

章节检测区分强标题和弱标题：

- 强标题：整行的 `第N章`、`第N回`、`Chapter N` 及其紧凑标题形式。
- 弱标题：`第N节`、`第N部`、卷标、番外、后记、附录、外传等。弱标题只有在短标题、合法分隔符且不呈现完整自然语言句子时才可成为候选。
- 当作品中存在强章标题时，卷标题作为结构 marker 保留在文本中，不单独切成 chapter。
- 只有弱标题体系时可以保守 fallback，但必须 `needs_review=true`。

第一个已接受章节标题之前的标准化文本不再拼入第一章，也不会删除；它完整保存为私有 `front_matter.txt`。`work.json` 记录其相对路径、字符数和 SHA-256。

## Source Integrity Gate V1

结构化成功不等于书源完整。每个 processed work 都会获得 `source_integrity_status`、`distillation_allowed` 和可审计的 `source_integrity` 摘要。完整判定方法、阈值与限制见 `docs/SOURCE_INTEGRITY_V1.md`。只有 `PASS` 允许进入 ChatGPT Packet；`WARNING`、`FAIL`、`UNKNOWN` 默认全部禁止蒸馏。

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

- 路径、原文件 Hash、处理指纹均未变化且 artifact 完整：跳过。
- 文件内容发生变化：重新提取并生成对应版本的确定性 work ID。
- 原文件 SHA-256 相同：`exact_file`。
- 标准化正文 SHA-256 相同：`normalized_text`。
- 重复只标记，不自动删除任何源文件或结构化版本。

## 安全验证

```powershell
python scripts/validate_private_boundaries.py
python scripts/validate_step01.py
```

验证会检查 Git tracked 与 staged 集合；任何 `_private`、小说归档格式、`sources/books` 原书、完整结构化章节正文或 ChatGPT Packet 路径都会导致 FAIL。传入 `--private-root` 时还会对 `01_原始小说` 和 `02_结构化文本/*/text/*.txt` 建立 SHA-256 集合，与 tracked/staged 内容做逐字节相同检查。该保护准确称为 **exact-content leakage protection**：它不承诺识别轻微修改或改写后的泄漏。Benchmark 私有 2190 文件不在此 Hash 扫描范围。

EvidenceRef 坐标与 ChatGPT 私有 Packet 详见 `docs/EVIDENCE_CONTRACT_V1.md` 和 `docs/CHATGPT_PACKET_EXPORT.md`。
