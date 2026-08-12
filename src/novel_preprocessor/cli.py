"""Command-line entrypoint for Novel Preprocessor V1."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .pipeline import PreprocessorConfig, run_preprocessor


def build_parser() -> argparse.ArgumentParser:
    default_repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="本地小说预处理：解析、分章、Hash、去重、Manifest。")
    parser.add_argument("--repo-root", type=Path, default=default_repo)
    parser.add_argument("--private-root", type=Path, default=default_repo.parent / "_private")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = PreprocessorConfig.from_roots(args.repo_root.resolve(), args.private_root.resolve())
    try:
        summary = run_preprocessor(config)
    except Exception as exc:
        print(f"预处理器启动失败：{exc}")
        return 2

    print("")
    print("小说预处理 V1 运行摘要")
    print(f"发现作品：{summary.discovered}")
    print(f"新处理：{summary.processed}")
    print(f"跳过未变化：{summary.skipped}")
    print(f"失败：{summary.failed}")
    print(f"可能重复：{summary.duplicates}")
    print(f"需要人工检查章节：{summary.needs_review}")
    print(f"延后格式（MOBI/AZW）：{summary.deferred}")
    print("书源完整性：")
    for status in ("PASS", "WARNING", "FAIL", "UNKNOWN"):
        print(f"{status}: {summary.source_integrity_counts[status]}")
    print(f"禁止蒸馏: {len(summary.distillation_blocked)}")
    if summary.distillation_blocked:
        print("非 PASS 作品：")
        for item in summary.distillation_blocked:
            reasons = ",".join(item["reason_codes"])
            print(f"- {item['work_id']} | {item['status']} | {reasons}")
    print(f"输出位置：{config.output_dir}")
    print(f"Manifest：{config.manifest_path}")
    if summary.errors:
        print("失败摘要：")
        for message in summary.errors:
            print(f"- {message}")
    return 1 if summary.failed else 0
