"""Conservative chapter-heading detection with explicit fallback."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_CN_NUMBER = r"[〇零一二三四五六七八九十百千万两0-9０-９]{1,16}"
_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "chapter",
        re.compile(
            rf"^第{_CN_NUMBER}[章回节篇部](?:\s*[：:、.．\-—]?\s*.{{0,48}})?$",
            re.IGNORECASE,
        ),
    ),
    (
        "volume",
        re.compile(
            rf"^(?:第{_CN_NUMBER}卷|卷{_CN_NUMBER})(?:\s*[：:、.．\-—]?\s*.{{0,48}})?$",
            re.IGNORECASE,
        ),
    ),
    (
        "chapter",
        re.compile(
            r"^(?:chapter|chap\.?|part)\s+(?:[0-9０-９]+|[ivxlcdm]+)(?:\s*[：:、.．\-—]?\s*.{0,48})?$",
            re.IGNORECASE,
        ),
    ),
    (
        "special",
        re.compile(
            r"^(?:序章|序言|前言|楔子|引子|终章|尾声|后记|番外(?:篇)?|外传|附录)(?:\s*[：:、.．\-—]?\s*.{0,48})?$",
            re.IGNORECASE,
        ),
    ),
)


@dataclass(frozen=True)
class HeadingCandidate:
    start: int
    end: int
    line_index: int
    title: str
    kind: str
    ordinal: int | None
    markdown_level: int | None


@dataclass
class ChapterSegment:
    index: int
    title: str | None
    text: str
    start_char: int
    end_char: int
    detection_confidence: str
    warnings: list[str] = field(default_factory=list)


@dataclass
class SegmentationResult:
    chapters: list[ChapterSegment]
    detection_confidence: str
    needs_review: bool
    warnings: list[str] = field(default_factory=list)


def _heading_view(line: str) -> tuple[str, int | None]:
    value = line.strip()
    markdown = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", value)
    if markdown:
        level = len(value) - len(value.lstrip("#"))
        value = markdown.group(1).strip()
        return value, level
    return value, None


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


def _heading_ordinal(title: str, kind: str) -> int | None:
    if kind != "chapter":
        return None
    match = re.match(rf"^第({_CN_NUMBER})[章回节篇部]", title, re.IGNORECASE)
    if match:
        return _number_value(match.group(1))
    match = re.match(r"^(?:chapter|chap\.?|part)\s+([0-9０-９]+)", title, re.IGNORECASE)
    return _number_value(match.group(1)) if match else None


def _classify_heading(line: str) -> tuple[str, str, int | None, int | None] | None:
    title, markdown_level = _heading_view(line)
    if not title or len(title) > 64 or "\t" in title:
        return None
    for kind, pattern in _PATTERNS:
        if pattern.fullmatch(title):
            return title, kind, _heading_ordinal(title, kind), markdown_level
    return None


def detect_heading_candidates(text: str) -> list[HeadingCandidate]:
    candidates: list[HeadingCandidate] = []
    offset = 0
    for line_index, line_with_ending in enumerate(text.splitlines(keepends=True)):
        line = line_with_ending.rstrip("\r\n")
        classified = _classify_heading(line)
        if classified is not None:
            title, kind, ordinal, markdown_level = classified
            left_trim = len(line) - len(line.lstrip())
            candidates.append(
                HeadingCandidate(
                    start=offset + left_trim,
                    end=offset + len(line),
                    line_index=line_index,
                    title=title,
                    kind=kind,
                    ordinal=ordinal,
                    markdown_level=markdown_level,
                )
            )
        offset += len(line_with_ending)

    if text and not text.endswith(("\n", "\r")) and not text.splitlines(keepends=True):
        classified = _classify_heading(text)
        if classified:
            title, kind, ordinal, markdown_level = classified
            candidates.append(HeadingCandidate(0, len(text), 0, title, kind, ordinal, markdown_level))
    return candidates


def _drop_volume_markers(candidates: list[HeadingCandidate], text: str) -> list[HeadingCandidate]:
    if not any(item.kind != "volume" for item in candidates):
        return candidates
    kept: list[HeadingCandidate] = []
    for index, item in enumerate(candidates):
        next_item = candidates[index + 1] if index + 1 < len(candidates) else None
        if item.kind == "volume" and next_item and next_item.kind == "chapter":
            between = text[item.end:next_item.start].strip()
            if len(between) <= 80:
                continue
        kept.append(item)
    return kept


def _fallback(text: str, warning: str) -> SegmentationResult:
    chapter = ChapterSegment(
        index=1,
        title=None,
        text=text,
        start_char=0,
        end_char=len(text),
        detection_confidence="low",
        warnings=[warning],
    )
    return SegmentationResult(
        chapters=[chapter],
        detection_confidence="low",
        needs_review=True,
        warnings=[warning],
    )


def segment_chapters(text: str) -> SegmentationResult:
    candidates = _drop_volume_markers(detect_heading_candidates(text), text)
    if not candidates:
        return _fallback(text, "chapter_heading_not_detected")

    if len(candidates) == 1:
        only = candidates[0]
        meaningful_prefix = text[:only.start].strip()
        prefix_limit = max(200, int(len(text) * 0.20))
        if meaningful_prefix and only.start > prefix_limit:
            return _fallback(text, "single_heading_ambiguous_in_body")

    chapters: list[ChapterSegment] = []
    content_lengths: list[int] = []
    for index, heading in enumerate(candidates, start=1):
        start = 0 if index == 1 else heading.start
        end = candidates[index].start if index < len(candidates) else len(text)
        segment = text[start:end].strip("\n")
        content_after_heading = text[heading.end:end].strip()
        content_lengths.append(len(content_after_heading))
        chapters.append(
            ChapterSegment(
                index=index,
                title=heading.title,
                text=segment,
                start_char=start,
                end_char=end,
                detection_confidence="pending",
            )
        )

    warnings: list[str] = []
    numbered = [candidate.ordinal for candidate in candidates if candidate.ordinal is not None]
    if len(numbered) >= 2 and any(current != previous + 1 for previous, current in zip(numbered, numbered[1:])):
        warnings.append("chapter_number_sequence_needs_review")
    markdown_levels = {candidate.markdown_level for candidate in candidates if candidate.markdown_level is not None}
    if len(markdown_levels) > 1:
        warnings.append("mixed_markdown_heading_levels")
    if any(candidate.kind == "volume" for candidate in candidates):
        warnings.append("volume_boundary_needs_review")
    if any(length < 80 for length in content_lengths):
        warnings.append("short_chapter_or_heading_quote_needs_review")
    if any(length > 200_000 for length in content_lengths):
        warnings.append("chapter_text_unusually_long")

    if len(candidates) >= 2 and not warnings:
        confidence = "high"
        needs_review = False
    elif len(candidates) == 1:
        confidence = "medium"
        needs_review = True
        warnings.append("single_heading_needs_review")
    else:
        confidence = "medium"
        needs_review = True

    for chapter in chapters:
        chapter.detection_confidence = confidence
        if len(chapter.text) < 80:
            chapter.warnings.append("chapter_text_unusually_short")

    return SegmentationResult(
        chapters=chapters,
        detection_confidence=confidence,
        needs_review=needs_review,
        warnings=warnings,
    )
