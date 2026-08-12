"""Local text extraction for V1 source formats."""

from __future__ import annotations

import html
import re
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Iterable
from xml.etree import ElementTree as ET


SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".epub", ".docx", ".pdf"}
DEFERRED_EXTENSIONS = {".mobi", ".azw", ".azw3"}
DISCOVERABLE_EXTENSIONS = SUPPORTED_EXTENSIONS | DEFERRED_EXTENSIONS

_MAX_ARCHIVE_MEMBER = 32 * 1024 * 1024
_MAX_ARCHIVE_TOTAL = 256 * 1024 * 1024


class ExtractionError(RuntimeError):
    """A local source could not be safely extracted."""


class DeferredFormatError(ExtractionError):
    """The format is recognized but intentionally deferred in V1."""


@dataclass
class ExtractionResult:
    text: str
    source_format: str
    title: str | None = None
    author: str | None = None
    encoding: str | None = None
    warnings: list[str] = field(default_factory=list)


def _safe_metadata(value: str | None) -> str | None:
    if value is None:
        return None
    clean = " ".join(value.split()).strip()
    return clean[:500] or None


def decode_text_bytes(data: bytes) -> tuple[str, str, list[str]]:
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig"), "utf-8-sig", []

    attempts = ("utf-8", "gb18030", "gbk", "big5")
    for encoding in attempts:
        try:
            text = data.decode(encoding)
            warnings = [] if encoding == "utf-8" else [f"source_encoding:{encoding}"]
            return text, encoding, warnings
        except UnicodeDecodeError:
            continue
    raise ExtractionError("无法以 UTF-8、GB18030、GBK 或 Big5 严格解码文本。")


def _validated_members(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    members: dict[str, zipfile.ZipInfo] = {}
    total = 0
    for info in archive.infolist():
        path = PurePosixPath(info.filename.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            raise ExtractionError(f"压缩包包含不安全路径: {info.filename}")
        if info.file_size > _MAX_ARCHIVE_MEMBER:
            raise ExtractionError(f"压缩包成员过大: {info.filename}")
        total += info.file_size
        if total > _MAX_ARCHIVE_TOTAL:
            raise ExtractionError("压缩包解压后总大小超过 V1 安全上限。")
        members[path.as_posix()] = info
    return members


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _xml_text(element: ET.Element | None) -> str | None:
    if element is None:
        return None
    return _safe_metadata("".join(element.itertext()))


class _HTMLTextExtractor(HTMLParser):
    _BLOCKS = {
        "address", "article", "aside", "blockquote", "br", "div", "figcaption",
        "figure", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header",
        "hr", "li", "main", "p", "section", "table", "td", "th", "tr",
    }
    _SKIP = {"script", "style", "nav", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self._SKIP:
            self._skip_depth += 1
        elif not self._skip_depth and tag in self._BLOCKS:
            self.parts.append("\n")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if not self._skip_depth and tag.lower() in self._BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif not self._skip_depth and tag in self._BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _html_to_text(raw: bytes) -> str:
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        source = raw.decode("utf-8", errors="replace")
    parser = _HTMLTextExtractor()
    parser.feed(source)
    parser.close()
    return html.unescape(parser.text())


def _extract_plain(path: Path) -> ExtractionResult:
    text, encoding, warnings = decode_text_bytes(path.read_bytes())
    return ExtractionResult(
        text=text,
        source_format="markdown" if path.suffix.lower() in {".md", ".markdown"} else "txt",
        encoding=encoding,
        warnings=warnings,
    )


def _paragraph_text(paragraph: ET.Element) -> str:
    pieces: list[str] = []
    for element in paragraph.iter():
        name = _local_name(element.tag)
        if name == "t" and element.text:
            pieces.append(element.text)
        elif name == "tab":
            pieces.append("\t")
        elif name in {"br", "cr"}:
            pieces.append("\n")
    return "".join(pieces)


def _extract_docx(path: Path) -> ExtractionResult:
    try:
        with zipfile.ZipFile(path) as archive:
            members = _validated_members(archive)
            if "word/document.xml" not in members:
                raise ExtractionError("DOCX 缺少 word/document.xml。")
            document = ET.fromstring(archive.read(members["word/document.xml"]))
            paragraphs = [
                _paragraph_text(element)
                for element in document.iter()
                if _local_name(element.tag) == "p"
            ]
            title = author = None
            if "docProps/core.xml" in members:
                core = ET.fromstring(archive.read(members["docProps/core.xml"]))
                for element in core.iter():
                    name = _local_name(element.tag)
                    if name == "title" and title is None:
                        title = _xml_text(element)
                    elif name == "creator" and author is None:
                        author = _xml_text(element)
    except zipfile.BadZipFile as exc:
        raise ExtractionError("DOCX 不是有效的 ZIP/OpenXML 文件。") from exc
    except ET.ParseError as exc:
        raise ExtractionError("DOCX XML 无法解析。") from exc
    return ExtractionResult(
        text="\n".join(paragraphs),
        source_format="docx",
        title=_safe_metadata(title),
        author=_safe_metadata(author),
    )


def _resolve_archive_path(base: str, href: str) -> str:
    combined = PurePosixPath(base).parent / PurePosixPath(href)
    parts: list[str] = []
    for part in combined.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                raise ExtractionError(f"EPUB href 越出压缩包根目录: {href}")
            parts.pop()
        else:
            parts.append(part)
    return PurePosixPath(*parts).as_posix()


def _find_first(root: ET.Element, local_name: str) -> ET.Element | None:
    return next((item for item in root.iter() if _local_name(item.tag) == local_name), None)


def _epub_spine(archive: zipfile.ZipFile, members: dict[str, zipfile.ZipInfo]) -> tuple[list[str], str | None, str | None, list[str]]:
    warnings: list[str] = []
    container_name = "META-INF/container.xml"
    if container_name not in members:
        raise ExtractionError("EPUB 缺少 META-INF/container.xml。")
    container = ET.fromstring(archive.read(members[container_name]))
    rootfile = next(
        (item for item in container.iter() if _local_name(item.tag) == "rootfile"),
        None,
    )
    if rootfile is None or not rootfile.attrib.get("full-path"):
        raise ExtractionError("EPUB container.xml 缺少 OPF 路径。")
    opf_name = PurePosixPath(rootfile.attrib["full-path"]).as_posix()
    if opf_name not in members:
        raise ExtractionError(f"EPUB 缺少 OPF 文件: {opf_name}")
    opf = ET.fromstring(archive.read(members[opf_name]))

    title = author = None
    for element in opf.iter():
        name = _local_name(element.tag)
        if name == "title" and title is None:
            title = _xml_text(element)
        elif name == "creator" and author is None:
            author = _xml_text(element)

    manifest: dict[str, tuple[str, str, str]] = {}
    for item in opf.iter():
        if _local_name(item.tag) != "item":
            continue
        item_id = item.attrib.get("id")
        href = item.attrib.get("href")
        if item_id and href:
            manifest[item_id] = (
                _resolve_archive_path(opf_name, href),
                item.attrib.get("media-type", ""),
                item.attrib.get("properties", ""),
            )

    ordered: list[str] = []
    spine = _find_first(opf, "spine")
    if spine is not None:
        for itemref in spine:
            if _local_name(itemref.tag) != "itemref":
                continue
            entry = manifest.get(itemref.attrib.get("idref", ""))
            if not entry:
                continue
            name, media_type, properties = entry
            lower_name = PurePosixPath(name).name.lower()
            is_nav = "nav" in properties.split() or lower_name in {"nav.xhtml", "toc.xhtml", "toc.html"}
            if media_type in {"application/xhtml+xml", "text/html"} and not is_nav:
                ordered.append(name)
    if not ordered:
        warnings.append("epub_spine_fallback")
        ordered = sorted(
            name for name in members
            if name.lower().endswith((".xhtml", ".html", ".htm"))
            and PurePosixPath(name).name.lower() not in {"nav.xhtml", "toc.xhtml", "toc.html"}
        )
    return ordered, _safe_metadata(title), _safe_metadata(author), warnings


def _extract_epub(path: Path) -> ExtractionResult:
    try:
        with zipfile.ZipFile(path) as archive:
            members = _validated_members(archive)
            ordered, title, author, warnings = _epub_spine(archive, members)
            texts = []
            for name in ordered:
                info = members.get(name)
                if info is not None:
                    text = _html_to_text(archive.read(info))
                    if text:
                        texts.append(text)
    except zipfile.BadZipFile as exc:
        raise ExtractionError("EPUB 不是有效的 ZIP 文件。") from exc
    except ET.ParseError as exc:
        raise ExtractionError("EPUB XML 无法解析。") from exc
    if not texts:
        raise ExtractionError("EPUB 未找到可提取的正文 HTML/XHTML。")
    return ExtractionResult(
        text="\n\n".join(texts),
        source_format="epub",
        title=title,
        author=author,
        warnings=warnings,
    )


def _extract_pdf(path: Path) -> ExtractionResult:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:
        raise ExtractionError("PDF 文本提取需要本地安装 pypdf；V1 不会调用在线服务。") from exc
    try:
        reader = PdfReader(str(path))
        pages = [(page.extract_text() or "") for page in reader.pages]
    except Exception as exc:
        raise ExtractionError(f"PDF 文本提取失败: {exc}") from exc
    text = "\n\n".join(pages).strip()
    if not text:
        raise ExtractionError("PDF 没有可提取文本，可能是扫描/图片 PDF；V1 不做 OCR。")
    metadata = reader.metadata or {}
    title = _safe_metadata(getattr(metadata, "title", None) or metadata.get("/Title"))
    author = _safe_metadata(getattr(metadata, "author", None) or metadata.get("/Author"))
    return ExtractionResult(text=text, source_format="pdf", title=title, author=author)


def extract_text(path: Path) -> ExtractionResult:
    extension = path.suffix.lower()
    if extension in DEFERRED_EXTENSIONS:
        raise DeferredFormatError(f"{extension} 在 V1 标记为 unsupported/deferred。")
    if extension in {".txt", ".md", ".markdown"}:
        return _extract_plain(path)
    if extension == ".docx":
        return _extract_docx(path)
    if extension == ".epub":
        return _extract_epub(path)
    if extension == ".pdf":
        return _extract_pdf(path)
    raise ExtractionError(f"不支持的扩展名: {extension}")


def iter_source_files(input_dir: Path) -> Iterable[Path]:
    if not input_dir.exists():
        return
    for path in sorted(input_dir.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if path.is_file() and path.suffix.lower() in DISCOVERABLE_EXTENSIONS:
            yield path
