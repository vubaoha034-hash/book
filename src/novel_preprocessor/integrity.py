"""Mechanical Source Integrity Gate V1 based on reliable chapter numbering."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable


SOURCE_INTEGRITY_METHOD_VERSION = "source-integrity-v1"
MIN_NUMBERED_CHAPTERS = 2
MIN_NUMBERED_SHARE = 0.60
SYSTEMATIC_GAP_EVENT_MIN = 3
SYSTEMATIC_MISSING_PER_GAP_MIN = 5
SYSTEMATIC_REPEATED_GAP_SHARE = 0.60
SYSTEMATIC_MISSING_RATIO_MIN = 0.10

_CN_NUMBER = r"[〇零一二三四五六七八九十百千万两0-9０-９]{1,16}"
_CHINESE_STRONG = re.compile(rf"^第({_CN_NUMBER})(?:章|回)(?:$|\s|[：:、.．\-–—])", re.IGNORECASE)
_ENGLISH_STRONG = re.compile(r"^(?:chapter|chap\.?)\s+([0-9０-９]+)(?:$|\s|[：:、.．\-–—])", re.IGNORECASE)


@dataclass(frozen=True)
class SourceIntegrityResult:
    method_version: str
    confidence: str
    numbered_chapter_count: int
    estimated_missing_chapters: int
    gap_event_count: int
    duplicate_number_count: int
    backward_number_count: int
    systematic_gap_detected: bool
    reason_codes: list[str]
    source_integrity_status: str
    distillation_allowed: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _number_value(raw: str) -> int | None:
    raw = raw.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    if raw.isdigit():
        return int(raw)
    digits = {"〇": 0, "零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    units = {"十": 10, "百": 100, "千": 1000, "万": 10000}
    if not raw or any(char not in digits and char not in units for char in raw):
        return None
    total = section = number = 0
    for char in raw:
        if char in digits:
            number = digits[char]
        else:
            unit = units[char]
            if unit == 10000:
                total += (section + number) * unit
                section = number = 0
            else:
                section += (number or 1) * unit
                number = 0
    return total + section + number


def strong_chapter_number(title: str | None) -> int | None:
    if not title:
        return None
    match = _CHINESE_STRONG.match(title.strip())
    if match:
        return _number_value(match.group(1))
    match = _ENGLISH_STRONG.match(title.strip())
    return _number_value(match.group(1)) if match else None


def unknown_integrity(reason_code: str = "numbering_not_reliable") -> SourceIntegrityResult:
    return SourceIntegrityResult(
        method_version=SOURCE_INTEGRITY_METHOD_VERSION,
        confidence="low",
        numbered_chapter_count=0,
        estimated_missing_chapters=0,
        gap_event_count=0,
        duplicate_number_count=0,
        backward_number_count=0,
        systematic_gap_detected=False,
        reason_codes=[reason_code],
        source_integrity_status="UNKNOWN",
        distillation_allowed=False,
    )


def analyze_source_integrity(titles: Iterable[str | None]) -> SourceIntegrityResult:
    title_list = list(titles)
    numbers = [number for title in title_list if (number := strong_chapter_number(title)) is not None]
    numbered_share = len(numbers) / len(title_list) if title_list else 0.0
    if len(numbers) < MIN_NUMBERED_CHAPTERS or numbered_share < MIN_NUMBERED_SHARE:
        result = unknown_integrity()
        return SourceIntegrityResult(
            **{**result.as_dict(), "numbered_chapter_count": len(numbers)}
        )

    gap_sizes: list[int] = []
    duplicates = 0
    backwards = 0
    for previous, current in zip(numbers, numbers[1:]):
        delta = current - previous
        if delta > 1:
            gap_sizes.append(delta - 1)
        elif delta == 0:
            duplicates += 1
        elif delta < 0:
            backwards += 1

    estimated_missing = sum(gap_sizes)
    denominator = len(numbers) + estimated_missing
    missing_ratio = estimated_missing / denominator if denominator else 0.0
    mode_size = mode_count = 0
    if gap_sizes:
        mode_size, mode_count = Counter(gap_sizes).most_common(1)[0]
    systematic = bool(
        len(gap_sizes) >= SYSTEMATIC_GAP_EVENT_MIN
        and mode_size >= SYSTEMATIC_MISSING_PER_GAP_MIN
        and mode_count >= SYSTEMATIC_GAP_EVENT_MIN
        and mode_count / len(gap_sizes) >= SYSTEMATIC_REPEATED_GAP_SHARE
        and missing_ratio >= SYSTEMATIC_MISSING_RATIO_MIN
    )

    reasons: list[str] = []
    if systematic:
        status = "FAIL"
        confidence = "high"
        reasons.append("systematic_numbering_gaps")
    elif gap_sizes or duplicates or backwards:
        status = "WARNING"
        confidence = "medium"
        if gap_sizes:
            reasons.append("isolated_numbering_gap")
        if duplicates:
            reasons.append("duplicate_chapter_number")
        if backwards:
            reasons.append("backward_chapter_number")
    else:
        status = "PASS"
        confidence = "high"

    return SourceIntegrityResult(
        method_version=SOURCE_INTEGRITY_METHOD_VERSION,
        confidence=confidence,
        numbered_chapter_count=len(numbers),
        estimated_missing_chapters=estimated_missing,
        gap_event_count=len(gap_sizes),
        duplicate_number_count=duplicates,
        backward_number_count=backwards,
        systematic_gap_detected=systematic,
        reason_codes=reasons,
        source_integrity_status=status,
        distillation_allowed=status == "PASS",
    )
