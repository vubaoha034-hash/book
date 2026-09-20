#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DIALOGUE_RE = re.compile(r"“([^”]+)”")
STRIP_PUNCT_RE = re.compile(r"[，。！？；：、“”‘’…—\s!?.,;:]")

@dataclass
class Block:
    index: int
    text: str
    turns: list[str]
    chars: int


def split_blocks(text: str) -> list[Block]:
    raw = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    out: list[Block] = []
    for i, block in enumerate(raw):
        compact = re.sub(r"\s+", " ", block)
        turns = [x.strip() for x in DIALOGUE_RE.findall(compact)]
        chars = len(re.sub(r"\s+", "", compact))
        out.append(Block(i, compact, turns, chars))
    return out


def turn_len(turn: str) -> int:
    return len(STRIP_PUNCT_RE.sub("", turn))


def is_question(turn: str) -> bool:
    return "？" in turn or "?" in turn


def dialogue_runs(blocks: list[Block]) -> list[dict]:
    runs: list[dict] = []
    i = 0
    while i < len(blocks):
        if not blocks[i].turns:
            i += 1
            continue

        turns: list[str] = []
        source_blocks: list[int] = []
        gap_chars: list[int] = []
        last_dialogue: int | None = None
        j = i

        while j < len(blocks):
            if blocks[j].turns:
                if last_dialogue is not None:
                    between = blocks[last_dialogue + 1:j]
                    if len(between) > 2:
                        break
                    chars = sum(x.chars for x in between)
                    if chars > 60:
                        break
                    gap_chars.append(chars)
                for turn in blocks[j].turns:
                    turns.append(turn)
                    source_blocks.append(j)
                last_dialogue = j
                j += 1
                continue

            k = j
            while k < len(blocks) and not blocks[k].turns and k - j < 3:
                k += 1
            if k >= len(blocks) or not blocks[k].turns:
                break
            between = blocks[last_dialogue + 1:k] if last_dialogue is not None else []
            if len(between) > 2 or sum(x.chars for x in between) > 60:
                break
            j = k

        if turns:
            lengths = [turn_len(x) for x in turns]
            short_ratio = sum(x <= 14 for x in lengths) / len(lengths)
            question_count = sum(is_question(x) for x in turns)
            avg_gap_chars = sum(gap_chars) / len(gap_chars) if gap_chars else 0.0

            reasons: list[str] = []

            if len(turns) >= 6 and short_ratio >= 0.75 and avg_gap_chars <= 18:
                reasons.append("RAPID_SHORT_TURN_LADDER")

            if (
                len(turns) >= 5
                and question_count >= 2
                and short_ratio >= 0.60
                and avg_gap_chars <= 25
            ):
                reasons.append("QUESTION_ANSWER_LADDER")

            for z in range(len(turns) - 3):
                q = [is_question(turns[z + k]) for k in range(4)]
                if q == [True, False, True, False]:
                    reasons.append("ALTERNATING_QA_CHAIN")
                    break

            runs.append(
                {
                    "start_block": i,
                    "end_block": max(i, j - 1),
                    "turns": turns,
                    "turn_count": len(turns),
                    "short_turn_ratio": round(short_ratio, 4),
                    "question_count": question_count,
                    "average_interturn_narration_chars": round(avg_gap_chars, 2),
                    "reasons": sorted(set(reasons)),
                }
            )

        i = max(j, i + 1)

    return runs


def analyze_text(text: str) -> dict:
    blocks = split_blocks(text)
    runs = dialogue_runs(blocks)
    blocked = [r for r in runs if r["reasons"]]
    return {
        "verdict": "BLOCK" if blocked else "CLEAR",
        "note": "CLEAR is a structural tripwire result only, never literary approval.",
        "blocked_run_count": len(blocked),
        "blocked_runs": blocked,
        "run_count": len(runs),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_dialogue_adjacency.py <candidate.txt>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    result = analyze_text(path.read_text(encoding="utf-8-sig"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["verdict"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
