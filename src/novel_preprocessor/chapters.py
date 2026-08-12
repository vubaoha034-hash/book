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


def _heading_view(line: str) -> str:
    value = line.strip()
    markdown = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", value)
    if markdown:
        value = markdown.group(1).strip()
    return value


def _classify_heading(line: str) -> tuple[str, str] | None:
    title = _heading_view(line)
    if not title or len(title) > 64 or "\t" in title:
        return None
    for kind, pattern in _PATTERNS:
        if pattern.fullmatch(title):
            return title, kind
    return None


def detect_heading_candidates(text: str) -> list[HeadingCandidate]:
    candidates: list[HeadingCandidate] = []
    offset = 0
    for line_index, line_with_ending in enumerate(text.splitlines(keepends=True)):
        line = line_with_ending.rstrip("\r\n")
        classified = _classify_heading(line)
        if classified is not None:
            title, kind = classified
            left_trim = len(line) - len(line.lstrip())
            candidates.append(
                HeadingCandidate(
                    start=offset + left_trim,
                    end=offset + len(line),
                    line_index=line_index,
                    title=title,
                    kind=kind,
                )
            )
        offset += len(line_with_ending)

    if text and not text.endswith(("\n", "\r")) and not text.splitlines(keepends=True):
        classified = _classify_heading(text)
        if classified:
            title, kind = classified
            candidates.append(HeadingCandidate(0, len(text), 0, title, kind))
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
    short_segments = 0
    for index, heading in enumerate(candidates, start=1):
        start = 0 if index == 1 else heading.start
        end = candidates[index].start if index < len(candidates) else len(text)
        segment = text[start:end].strip("\n")
        content_after_heading = text[heading.end:end].strip()
        if len(content_after_heading) < 8:
            short_segments += 1
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
    if len(candidates) >= 2 and short_segments <= max(1, len(chapters) // 4):
        confidence = "high"
        needs_review = False
    elif len(candidates) == 1 and len(chapters[0].text) >= 16:
        confidence = "medium"
        needs_review = False
    else:
        confidence = "medium"
        needs_review = True
        warnings.append("chapter_segments_unusually_short")

    for chapter in chapters:
        chapter.detection_confidence = confidence
        if len(chapter.text) < 8:
            chapter.warnings.append("chapter_text_unusually_short")

    return SegmentationResult(
        chapters=chapters,
        detection_confidence=confidence,
        needs_review=needs_review,
        warnings=warnings,
    )
