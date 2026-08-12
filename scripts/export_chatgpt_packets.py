#!/usr/bin/env python3
"""Create private, offline, manually-uploaded ChatGPT source packets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from novel_preprocessor.packets import (  # noqa: E402
    DEFAULT_MAX_CHARS_PER_PART,
    PacketExportError,
    available_work_ids,
    export_packets,
)


def _selection_file(path: Path) -> list[str]:
    if not path.is_file():
        raise PacketExportError(f"选择文件不存在: {path}")
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="离线生成供用户手工上传的 ChatGPT 私有结构化小说包。")
    parser.add_argument("--private-root", required=True, type=Path)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--work-id", action="append", dest="work_ids")
    selection.add_argument("--all", action="store_true")
    selection.add_argument("--selection-file", type=Path)
    parser.add_argument("--max-chars-per-part", type=int, default=DEFAULT_MAX_CHARS_PER_PART)
    args = parser.parse_args()
    private_root = args.private_root.resolve()
    if args.all:
        work_ids = available_work_ids(private_root)
    elif args.selection_file:
        work_ids = _selection_file(args.selection_file)
    else:
        work_ids = args.work_ids or []
    try:
        outputs = export_packets(private_root, work_ids, args.max_chars_per_part)
    except (OSError, PacketExportError) as exc:
        print(f"生成失败：{exc}")
        return 1
    print("ChatGPT 私有蒸馏包生成完成（仅本地，未上传）")
    print(f"选择作品：{len(outputs)}")
    for output in outputs:
        print(f"- {output}")
    print("网络上传：NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
