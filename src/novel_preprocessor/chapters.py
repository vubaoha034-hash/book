"""Conservative strong/weak chapter-heading detection with explicit fallback."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_CN_NUMBER = r"[〇零一二三四五六七八九十百千万两0-9０-９]{1,16}"
_STRONG_CHINESE = re.compile(rf"^第({_CN_NUMBER})(章|回)(.*)$", re.IGNORECASE)
_STRONG_ENGLISH = re.compile(
    r"^(chapter|chap\.?)\s+([0-9０-９]+|[ivxlcdm]+)(.*)$",
    re.IGNORECASE,
)
_WEAK_NUMBERED = re.compile(rf"^第({_CN_NUMBER})(节|部)(.*)$", re.IGNORECASE)
_WEAK_VOLUME = re.compile(rf"^(?:第({_CN_NUMBER})卷|卷({_CN_NUMBER}))(.*)$", re.IGNORECASE)
_WEAK_ENGLISH_PART = re.compile(
    r"^(part)\s+([0-9０-９]+|[ivxlcdm]+)(.*)$",
    re.IGNORECASE,
)
_WEAK_SPECIAL = re.compile(r"^(序章|序言|前言|楔子|引子|终章|尾声|后记|番外(?:篇)?|外传|附录)(.*)$", re.IGNORECASE)
_TITLE_SEPARATOR = re.compile(r"^(?:\s+|\s*[：:、.．\-–—]{1,2}\s*)(\S.*)$")
_SENTENCE_PUNCTUATION = re.compile(r"[，,。！？!?；;…]")
_MAX_STRONG_SUFFIX = 48
_MAX_WEAK_SUFFIX = 24
_COMPACT_HUI_MIN_TITLE = 2
_COMPACT_HUI_MAX_TITLE = 12
_COMPACT_HUI_MIN_SEQUENCE = 3
_COMPACT_HUI_PREFIX = re.compile(rf"第({_CN_NUMBER})回", re.IGNORECASE)
_COMPACT_HUI_SEPARATOR_PREFIX = frozenset(" \t\u3000：:、.．-–—")


@dataclass(frozen=True)
class HeadingCandidate:
    start: int
    end: int
    line_index: int
    title: str
    kind: str
    strength: str
    ordinal: int | None
    markdown_level: int | None
    candidate_type: str = "line_heading"


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
    front_matter: str = ""


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


def _strong_suffix_valid(suffix: str) -> bool:
    if not suffix:
        return True
    match = _TITLE_SEPARATOR.fullmatch(suffix)
    return bool(match and 0 < len(match.group(1).strip()) <= _MAX_STRONG_SUFFIX)


def _weak_suffix_valid(suffix: str) -> bool:
    if not suffix:
        return True
    match = _TITLE_SEPARATOR.fullmatch(suffix)
    if not match:
        return False
    title = match.group(1).strip()
    return bool(title and len(title) <= _MAX_WEAK_SUFFIX and not _SENTENCE_PUNCTUATION.search(title))


def _classify_heading(line: str) -> tuple[str, str, str, int | None, int | None] | None:
    title, markdown_level = _heading_view(line)
    if not title or len(title) > 80 or "\t" in title:
        return None

    match = _STRONG_CHINESE.fullmatch(title)
    if match and _strong_suffix_valid(match.group(3)):
        return title, "chapter", "strong", _number_value(match.group(1)), markdown_level

    match = _STRONG_ENGLISH.fullmatch(title)
    if match and _strong_suffix_valid(match.group(3)):
        raw_number = match.group(2)
        ordinal = _number_value(raw_number) if not re.fullmatch(r"[ivxlcdm]+", raw_number, re.IGNORECASE) else None
        return title, "chapter", "strong", ordinal, markdown_level

    match = _WEAK_NUMBERED.fullmatch(title)
    if match and _weak_suffix_valid(match.group(3)):
        return title, "section", "weak", None, markdown_level

    match = _WEAK_VOLUME.fullmatch(title)
    if match and _weak_suffix_valid(match.group(3)):
        return title, "volume", "weak", None, markdown_level

    match = _WEAK_ENGLISH_PART.fullmatch(title)
    if match and _weak_suffix_valid(match.group(3)):
        return title, "part", "weak", None, markdown_level

    match = _WEAK_SPECIAL.fullmatch(title)
    if match and _weak_suffix_valid(match.group(2)):
        return title, "special", "weak", None, markdown_level
    return None


def _detect_line_heading_candidates(text: str) -> list[HeadingCandidate]:
    candidates: list[HeadingCandidate] = []
    offset = 0
    for line_index, line_with_ending in enumerate(text.splitlines(keepends=True)):
        line = line_with_ending.rstrip("\r\n")
        classified = _classify_heading(line)
        if classified is not None:
            title, kind, strength, ordinal, markdown_level = classified
            left_trim = len(line) - len(line.lstrip())
            candidates.append(
                HeadingCandidate(
                    start=offset + left_trim,
                    end=offset + len(line),
                    line_index=line_index,
                    title=title,
                    kind=kind,
                    strength=strength,
                    ordinal=ordinal,
                    markdown_level=markdown_level,
                )
            )
        offset += len(line_with_ending)
    return candidates


def _compact_hui_title_valid(title: str) -> bool:
    """Accept only an unseparated, short, non-sentence title at physical line end."""

    if not (_COMPACT_HUI_MIN_TITLE <= len(title) <= _COMPACT_HUI_MAX_TITLE):
        return False
    if title != title.strip() or any(char.isspace() for char in title):
        return False
    if title[0] in _COMPACT_HUI_SEPARATOR_PREFIX:
        return False
    return not _SENTENCE_PUNCTUATION.search(title)


def _detect_compact_inline_hui_candidates(text: str) -> list[HeadingCandidate]:
    """Scan line-ending ``第N回短标题`` forms without accepting them yet."""

    candidates: list[HeadingCandidate] = []
    offset = 0
    for line_index, line_with_ending in enumerate(text.splitlines(keepends=True)):
        line = line_with_ending.rstrip("\r\n")
        for match in _COMPACT_HUI_PREFIX.finditer(line):
            short_title = line[match.end():]
            if not _compact_hui_title_valid(short_title):
                continue
            candidates.append(
                HeadingCandidate(
                    start=offset + match.start(),
                    end=offset + len(line),
                    line_index=line_index,
                    title=line[match.start():],
                    kind="chapter",
                    strength="strong",
                    ordinal=_number_value(match.group(1)),
                    markdown_level=None,
                    candidate_type="compact_inline_hui",
                )
            )
        offset += len(line_with_ending)
    return candidates


def _sequenced_compact_hui_candidates(candidates: list[HeadingCandidate]) -> list[HeadingCandidate]:
    """Enable only monotonically consecutive compact-hui runs of three or more."""

    accepted: list[HeadingCandidate] = []
    run: list[HeadingCandidate] = []
    for candidate in candidates:
        previous_ordinal = run[-1].ordinal if run else None
        if (
            previous_ordinal is not None
            and candidate.ordinal is not None
            and candidate.ordinal == previous_ordinal + 1
        ):
            run.append(candidate)
            continue
        if len(run) >= _COMPACT_HUI_MIN_SEQUENCE:
            accepted.extend(run)
        run = [candidate]
    if len(run) >= _COMPACT_HUI_MIN_SEQUENCE:
        accepted.extend(run)
    return accepted


def detect_heading_candidates(text: str) -> list[HeadingCandidate]:
    line_candidates = _detect_line_heading_candidates(text)
    compact_candidates = _sequenced_compact_hui_candidates(
        _detect_compact_inline_hui_candidates(text)
    )
    return sorted([*line_candidates, *compact_candidates], key=lambda item: (item.start, item.end))


def _select_candidates(candidates: list[HeadingCandidate]) -> list[HeadingCandidate]:
    """Treat volumes as structure markers when real chapter headings exist."""

    if any(item.strength == "strong" for item in candidates):
        return [item for item in candidates if item.kind != "volume"]
    return candidates


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
        front_matter="",
    )


def segment_chapters(text: str) -> SegmentationResult:
    candidates = _select_candidates(detect_heading_candidates(text))
    if not candidates:
        return _fallback(text, "chapter_heading_not_detected")

    if len(candidates) == 1:
        only = candidates[0]
        meaningful_prefix = text[:only.start].strip()
        prefix_limit = max(200, int(len(text) * 0.20))
        if meaningful_prefix and only.start > prefix_limit:
            return _fallback(text, "single_heading_ambiguous_in_body")

    front_matter = text[:candidates[0].start]
    chapters: list[ChapterSegment] = []
    content_lengths: list[int] = []
    for index, heading in enumerate(candidates, start=1):
        start = heading.start
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
    if any(candidate.strength == "weak" for candidate in candidates):
        warnings.append("weak_heading_boundary_needs_review")
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
        front_matter=front_matter,
    )
