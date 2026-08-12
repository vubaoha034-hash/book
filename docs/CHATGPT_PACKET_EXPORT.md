# ChatGPT Private Export Bridge

该桥只把本地结构化章节打包成用户可以手工上传的私有 Markdown 文件。它不联网、不调用 API、不自动上传，也不执行总结、评价、改写、爽点提取或 Novel DNA。

## Explicit selection

不得默认导出整个书库。命令行必须显式选择一种方式：

```powershell
python scripts/export_chatgpt_packets.py --private-root E:\蒸馏小说\_private --work-id wrk_xxx --work-id wrk_yyy
python scripts/export_chatgpt_packets.py --private-root E:\蒸馏小说\_private --all
python scripts/export_chatgpt_packets.py --private-root E:\蒸馏小说\_private --selection-file E:\蒸馏小说\_private\chatgpt_selection.txt
```

一键入口 `E:\蒸馏小说\02_生成ChatGPT蒸馏包.bat` 读取 `_private\chatgpt_selection.txt`；每行一个 `work_id`，`#` 开头和空行忽略。

## Output

每本作品输出到：

```text
_private\03_ChatGPT蒸馏包\<work_id>\
├─ packet_manifest.json
└─ parts\
   ├─ part_001.md
   └─ ...
```

Manifest 保存 work/chapter/`part_sha256`、processing contract、part 清单和 slice 坐标，不保存 Windows 私有绝对路径。每个 Markdown part 在正文前明确写出 WORK、CHAPTER、CHAPTER_ID、CHAPTER_TEXT_SHA256 和 PROCESSING_CONTRACT_VERSION。

默认 `--max-chars-per-part` 为 80,000，按生成后 Markdown 的 Python 字符数限制。优先把完整章节放在同一 part；只有单章连同必要元数据超过上限时才按章节相对字符坐标切片。每个 slice 保存 start/end 与 SHA-256，Manifest 还保存正文在 part 中的字符坐标，因此所有 slices 可无损重组成私有结构化章节，不会静默截断。

整个输出目录是私有上传材料，严禁进入 Git。生成完成只表示本地 Packet 已准备好；网络上传始终为 `NO`。
