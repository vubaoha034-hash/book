#!/usr/bin/env python3
"""Local source ingester for novel-writing-master.

This script extracts text from local books/notes into library/_extracted/ and writes
library/source-register.md + library/source-register.json.

It is intentionally local-first. Do not commit copyrighted source books or extracted
raw text to a public repository.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable, List, Optional

ROOT = Path(__file__).resolve().parents[1]
SOURCES_BOOKS = ROOT / "sources" / "books"
SOURCES_NOTES = ROOT / "sources" / "notes"
LIBRARY_DIR = ROOT / "library"
EXTRACTED_DIR = LIBRARY_DIR / "_extracted"
REGISTER_MD = LIBRARY_DIR / "source-register.md"
REGISTER_JSON = LIBRARY_DIR / "source-register.json"

SUPPORTED = {
    ".txt", ".md", ".markdown", ".rst", ".adoc",
    ".html", ".htm", ".docx", ".pdf", ".epub", ".rtf",
}


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def has_module(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def slugify(path: Path, digest: str) -> str:
    stem = path.stem.lower()
    stem = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", stem).strip("-")
    return f"{stem or 'source'}-{digest[:8]}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def read_text_file(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "gb18030", "gbk", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def extract_txt(path: Path) -> str:
    return read_text_file(path)


def extract_html(path: Path) -> str:
    raw = read_text_file(path)
    try:
        from bs4 import BeautifulSoup  # type: ignore
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text("\n").strip()
    except Exception:
        return strip_html(raw)


def extract_docx(path: Path) -> str:
    try:
        import docx  # type: ignore
        doc = docx.Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        # Fallback: DOCX is a ZIP with document.xml.
        with zipfile.ZipFile(path) as zf:
            xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
        xml = re.sub(r"</w:p>", "\n", xml)
        xml = re.sub(r"<[^>]+>", "", xml)
        return html.unescape(xml).strip()


def extract_pdf(path: Path) -> str:
    if command_exists("pdftotext"):
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n\n".join(pages).strip()
    except Exception as e:
        raise RuntimeError("PDF extraction failed. Install poppler-utils or pypdf.") from e


def extract_epub(path: Path) -> str:
    # Good enough fallback: EPUB is a ZIP of XHTML/HTML files.
    texts: List[str] = []
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith((".xhtml", ".html", ".htm"))]
        for name in sorted(names):
            raw = zf.read(name).decode("utf-8", errors="ignore")
            texts.append(strip_html(raw))
    if not texts:
        raise RuntimeError("No readable HTML/XHTML files found in EPUB.")
    return "\n\n".join(t for t in texts if t.strip())


def extract_rtf(path: Path) -> str:
    try:
        from striprtf.striprtf import rtf_to_text  # type: ignore
        return rtf_to_text(read_text_file(path))
    except Exception:
        raw = read_text_file(path)
        raw = re.sub(r"\\'[0-9a-fA-F]{2}", " ", raw)
        raw = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", raw)
        raw = re.sub(r"[{}]", " ", raw)
        return re.sub(r"\s+", " ", raw).strip()


def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".txt", ".md", ".markdown", ".rst", ".adoc"}:
        return extract_txt(path)
    if ext in {".html", ".htm"}:
        return extract_html(path)
    if ext == ".docx":
        return extract_docx(path)
    if ext == ".pdf":
        return extract_pdf(path)
    if ext == ".epub":
        return extract_epub(path)
    if ext == ".rtf":
        return extract_rtf(path)
    raise RuntimeError(f"Unsupported extension: {ext}")


def iter_supported(path: Path) -> Iterable[Path]:
    if path.is_file() and path.suffix.lower() in SUPPORTED:
        yield path
    elif path.is_dir():
        for child in sorted(path.rglob("*")):
            if child.is_file() and child.suffix.lower() in SUPPORTED:
                yield child


def resolve_inputs(paths: List[str]) -> List[Path]:
    if not paths:
        paths = [str(SOURCES_BOOKS), str(SOURCES_NOTES)]
    out: List[Path] = []
    for raw in paths:
        expanded = Path(os.path.expanduser(raw))
        if any(ch in raw for ch in "*?["):
            import glob
            for match in glob.glob(os.path.expanduser(raw)):
                out.extend(iter_supported(Path(match)))
        else:
            out.extend(iter_supported(expanded))
    seen = set()
    unique: List[Path] = []
    for p in out:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def approx_words(text: str) -> int:
    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    western = len(re.findall(r"\b[a-zA-Z0-9]+\b", text))
    return chinese + western


def write_markdown_for_source(path: Path, text: str, digest: str) -> tuple[Path, dict]:
    slug = slugify(path, digest)
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    out = EXTRACTED_DIR / f"{slug}.md"
    clean = text.strip()
    out.write_text(
        f"# Extracted Source: {path.name}\n\n"
        f"- Original path: `{path}`\n"
        f"- Extension: `{path.suffix.lower()}`\n"
        f"- SHA256: `{digest}`\n"
        f"- Approx words/chars: `{approx_words(clean)}`\n\n"
        "---\n\n"
        f"{clean}\n",
        encoding="utf-8",
    )
    meta = {
        "filename": path.name,
        "path": str(path),
        "extension": path.suffix.lower(),
        "sha256": digest,
        "slug": slug,
        "extracted_file": str(out.relative_to(ROOT)),
        "approx_words": approx_words(clean),
        "chars": len(clean),
        "status": "ok",
    }
    return out, meta


def write_register(records: List[dict]) -> None:
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    REGISTER_JSON.write_text(json.dumps({"sources": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Source Register", ""]
    if not records:
        lines.append("当前没有导入任何书籍或资料。")
    else:
        lines.append("| File | Status | Words | Extracted |")
        lines.append("|---|---:|---:|---|")
        for r in records:
            lines.append(
                f"| {r.get('filename')} | {r.get('status')} | {r.get('approx_words', 0)} | {r.get('extracted_file') or '-'} |"
            )
    lines.append("")
    REGISTER_MD.write_text("\n".join(lines), encoding="utf-8")


def run_check() -> int:
    print("Novel Writing Master extractor check")
    print(f"Root: {ROOT}")
    checks = [
        ("TXT/MD", "built-in", True, "No install needed"),
        ("HTML", "bs4 optional", has_module("bs4"), "pip install beautifulsoup4"),
        ("DOCX", "python-docx optional", has_module("docx"), "pip install python-docx"),
        ("PDF", "pdftotext", command_exists("pdftotext"), "apt/brew install poppler"),
        ("PDF", "pypdf fallback", has_module("pypdf"), "pip install pypdf"),
        ("EPUB", "built-in ZIP parser", True, "No install needed"),
        ("RTF", "striprtf optional", has_module("striprtf"), "pip install striprtf"),
    ]
    for fmt, tool, ok, install in checks:
        status = "OK" if ok else "MISSING"
        print(f"{fmt:10} {tool:24} {status:8} {install}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Extract local books/notes for novel-writing-master skill.")
    parser.add_argument("paths", nargs="*", help="Files, folders, or glob patterns. Defaults to sources/books and sources/notes.")
    parser.add_argument("--check", action="store_true", help="Check available extractors and exit.")
    args = parser.parse_args(argv)

    if args.check:
        return run_check()

    files = resolve_inputs(args.paths)
    if not files:
        write_register([])
        print("No supported source files found.")
        print("Put books into sources/books/ or pass paths explicitly.")
        return 1

    records: List[dict] = []
    for path in files:
        digest = sha256_file(path)
        try:
            text = extract_text(path)
            out_path, meta = write_markdown_for_source(path, text, digest)
            records.append(meta)
            print(f"OK  {path.name} -> {out_path.relative_to(ROOT)}")
        except Exception as e:
            records.append({
                "filename": path.name,
                "path": str(path),
                "extension": path.suffix.lower(),
                "sha256": digest,
                "slug": slugify(path, digest),
                "extracted_file": None,
                "approx_words": 0,
                "chars": 0,
                "status": "failed",
                "error": str(e),
            })
            print(f"FAIL {path.name}: {e}", file=sys.stderr)

    write_register(records)
    ok = sum(1 for r in records if r.get("status") == "ok")
    failed = len(records) - ok
    print("")
    print(f"Done. OK={ok}, failed={failed}")
    print(f"Register: {REGISTER_MD.relative_to(ROOT)}")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
