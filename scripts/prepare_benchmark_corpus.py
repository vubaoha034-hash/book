#!/usr/bin/env python3
"""Prepare isolated private corpora for Novel Distillation Benchmark.

Creates two independent experiment states from one local novel source:
1) style: development chapters with stratified style holdouts removed;
2) narrative: contiguous context followed by a future holdout suffix.

The two states must not share derived caches or model state. The script writes
source text only to the selected private output directory; it never writes to
tracked benchmark directories by itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

CHAPTER_RE = re.compile(r"(?m)^\s*第\s*([^\s章]{1,16})\s*章\s*([^\r\n]*)")


def read_text(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode source as UTF-8/UTF-8-SIG/GB18030")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_chapters(text: str) -> list[dict]:
    matches = list(CHAPTER_RE.finditer(text))
    if not matches:
        raise ValueError("No chapter headings matched pattern '第…章'.")
    chapters: list[dict] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip() + "\n"
        encoded = body.encode("utf-8")
        chapters.append(
            {
                "seq": index + 1,
                "source_label": match.group(1),
                "text": body,
                "chars": len(body),
                "bytes": len(encoded),
                "sha256": sha256_bytes(encoded),
            }
        )
    return chapters


def parse_seq_list(value: str | None) -> list[int] | None:
    if not value:
        return None
    result = sorted({int(part.strip()) for part in value.split(",") if part.strip()})
    return result or None


def choose_even_holdouts(cutoff: int, count: int) -> list[int]:
    if count <= 0:
        return []
    if cutoff < count + 2:
        raise ValueError("Not enough development chapters for requested style holdouts.")
    interior = list(range(2, cutoff))
    if count >= len(interior):
        return interior
    positions = []
    for i in range(count):
        idx = round((i + 1) * (len(interior) + 1) / (count + 1)) - 1
        idx = max(0, min(idx, len(interior) - 1))
        positions.append(interior[idx])
    selected = []
    for seq in positions + interior:
        if seq not in selected:
            selected.append(seq)
        if len(selected) == count:
            break
    return sorted(selected)


def write_state(root: Path, relative: str, seqs: list[int], chapters: list[dict]) -> None:
    directory = root / relative
    directory.mkdir(parents=True, exist_ok=True)
    for seq in seqs:
        chapter = chapters[seq - 1]
        (directory / f"{seq:03d}.txt").write_text(chapter["text"], encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--corpus-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smoke-chapters", type=int, default=50)
    parser.add_argument("--future-holdout", type=int, default=8)
    parser.add_argument("--style-holdout-count", type=int, default=6)
    parser.add_argument(
        "--style-holdout-seqs",
        default=None,
        help="Optional comma-separated explicit chapter seqs, e.g. 5,12,19,26,33,40",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"Source not found: {source}")
    if args.smoke_chapters <= 0 or args.future_holdout <= 0:
        raise SystemExit("smoke-chapters and future-holdout must be positive")
    if args.future_holdout >= args.smoke_chapters:
        raise SystemExit("future-holdout must be smaller than smoke-chapters")

    source_bytes = source.read_bytes()
    text, encoding = read_text(source)
    chapters = parse_chapters(text)
    if len(chapters) < args.smoke_chapters:
        raise SystemExit(
            f"Need at least {args.smoke_chapters} chapters; detected {len(chapters)}"
        )

    cutoff = args.smoke_chapters - args.future_holdout
    explicit = parse_seq_list(args.style_holdout_seqs)
    style_holdout = explicit or choose_even_holdouts(cutoff, args.style_holdout_count)
    if any(seq < 1 or seq > cutoff for seq in style_holdout):
        raise SystemExit(f"Style holdout must be within 1..{cutoff}: {style_holdout}")

    style_train = [seq for seq in range(1, cutoff + 1) if seq not in style_holdout]
    narrative_context = list(range(1, cutoff + 1))
    future_holdout = list(range(cutoff + 1, args.smoke_chapters + 1))

    root = args.output.resolve() / args.corpus_id
    if root.exists():
        if not args.overwrite:
            raise SystemExit(f"Output exists; pass --overwrite to replace: {root}")
        shutil.rmtree(root)
    root.mkdir(parents=True)

    write_state(root, "style/train", style_train, chapters)
    write_state(root, "style/holdout", style_holdout, chapters)
    write_state(root, "narrative/context", narrative_context, chapters)
    write_state(root, "narrative/future_holdout", future_holdout, chapters)

    manifest = {
        "schema_version": "1.0.0",
        "corpus_id": args.corpus_id,
        "source": {
            "sha256": sha256_bytes(source_bytes),
            "bytes": len(source_bytes),
            "encoding": encoding,
            "detected_chapters_total": len(chapters),
            "source_filename_stored": False,
        },
        "smoke_scope": {
            "start_seq": 1,
            "end_seq": args.smoke_chapters,
            "count": args.smoke_chapters,
            "chars": sum(
                chapters[i - 1]["chars"] for i in range(1, args.smoke_chapters + 1)
            ),
        },
        "protocols": {
            "style": {
                "state_namespace": f"{args.corpus_id}-style-v1",
                "train": style_train,
                "style_holdout": style_holdout,
                "derived_cache_namespace": "style-only",
                "cross_protocol_artifact_reuse": False,
            },
            "narrative": {
                "state_namespace": f"{args.corpus_id}-narrative-v1",
                "context": narrative_context,
                "future_holdout": future_holdout,
                "derived_cache_namespace": "narrative-only",
                "cross_protocol_artifact_reuse": False,
            },
        },
        "integrity": {
            "generated_text_allowed_in_source": False,
            "public_repo_upload_allowed": False,
            "style_holdout_not_visible_in_style_state": True,
            "future_holdout_not_visible_in_narrative_state": True,
            "cross_protocol_cache_reuse_allowed": False,
        },
        "chapters": {
            str(seq): {
                "sha256": chapters[seq - 1]["sha256"],
                "chars": chapters[seq - 1]["chars"],
                "bytes": chapters[seq - 1]["bytes"],
            }
            for seq in range(1, args.smoke_chapters + 1)
        },
    }
    (root / "manifest.private.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "corpus_id": args.corpus_id,
                "output": str(root),
                "source_sha256": manifest["source"]["sha256"],
                "detected_chapters_total": len(chapters),
                "smoke_chapters": args.smoke_chapters,
                "style_train_count": len(style_train),
                "style_holdout": style_holdout,
                "narrative_context_count": len(narrative_context),
                "future_holdout": future_holdout,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
