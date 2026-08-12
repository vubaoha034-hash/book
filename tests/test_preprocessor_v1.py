from __future__ import annotations

import html
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from novel_preprocessor.chapters import segment_chapters
from novel_preprocessor.cleaning import normalize_text
from novel_preprocessor.extractors import extract_text
from novel_preprocessor.hashing import make_chapter_id, make_work_id, sha256_file, sha256_text
from novel_preprocessor.contract import DEFAULT_PROCESSING_CONTRACT
from novel_preprocessor.pipeline import PreprocessorConfig, run_preprocessor
from validate_card_schemas import validate_schema
from validate_private_boundaries import validate_repo


def make_docx(path: Path, paragraphs: list[str], title: str = "测试作品", author: str = "测试作者") -> None:
    body = "".join(
        f"<w:p><w:r><w:t>{html.escape(paragraph)}</w:t></w:r></w:p>"
        for paragraph in paragraphs
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    core = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f"<dc:title>{html.escape(title)}</dc:title><dc:creator>{html.escape(author)}</dc:creator>"
        "</cp:coreProperties>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)
        archive.writestr("docProps/core.xml", core)


def make_epub(path: Path) -> None:
    container = (
        '<?xml version="1.0"?>'
        '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
        "</rootfiles></container>"
    )
    opf = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<dc:title>本地测试书</dc:title><dc:creator>测试者</dc:creator></metadata>'
        '<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        '<item id="c1" href="c1.xhtml" media-type="application/xhtml+xml"/>'
        '<item id="c2" href="c2.xhtml" media-type="application/xhtml+xml"/></manifest>'
        '<spine><itemref idref="nav"/><itemref idref="c1"/><itemref idref="c2"/></spine>'
        "</package>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr("META-INF/container.xml", container)
        archive.writestr("OEBPS/content.opf", opf)
        archive.writestr("OEBPS/nav.xhtml", "<html><body><nav>目录垃圾</nav></body></html>")
        archive.writestr("OEBPS/c1.xhtml", "<html><body><h1>第一章 出发</h1><p>甲推开了门。</p></body></html>")
        archive.writestr("OEBPS/c2.xhtml", "<html><body><h1>第二章 抵达</h1><p>乙点亮了灯。</p></body></html>")


class TemporaryPipeline:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.repo = root / "repo"
        self.private = root / "_private"
        self.config = PreprocessorConfig.from_roots(self.repo, self.private)
        self.config.ensure_layout()

    def close(self) -> None:
        self.temp.cleanup()


class ExtractorTests(unittest.TestCase):
    def test_utf8_txt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "utf8.txt"
            path.write_text("第一章\n这是本地测试。", encoding="utf-8")
            result = extract_text(path)
            self.assertIn("本地测试", result.text)
            self.assertEqual(result.encoding, "utf-8")

    def test_utf8_bom_txt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bom.txt"
            path.write_bytes(b"\xef\xbb\xbf" + "第一章\n带 BOM。".encode("utf-8"))
            result = extract_text(path)
            self.assertFalse(result.text.startswith("\ufeff"))
            self.assertEqual(result.encoding, "utf-8-sig")

    def test_common_chinese_encoding_txt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gb.txt"
            path.write_bytes("第一章\n常见中文编码。".encode("gb18030"))
            result = extract_text(path)
            self.assertIn("中文编码", result.text)
            self.assertIn(result.encoding, {"gb18030", "gbk"})

    def test_epub_spine_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.epub"
            make_epub(path)
            result = extract_text(path)
            self.assertEqual(result.title, "本地测试书")
            self.assertEqual(result.author, "测试者")
            self.assertIn("第一章", result.text)
            self.assertNotIn("目录垃圾", result.text)
            self.assertLess(result.text.index("第一章"), result.text.index("第二章"))

    def test_docx_xml_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.docx"
            make_docx(path, ["第一章", "自行生成的短文本。"])
            result = extract_text(path)
            self.assertEqual(result.title, "测试作品")
            self.assertEqual(result.author, "测试作者")
            self.assertIn("自行生成", result.text)

    def test_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_text("# 第一章 开门\n\n这里是 Markdown。", encoding="utf-8")
            result = extract_text(path)
            self.assertEqual(result.source_format, "markdown")
            self.assertIn("Markdown", result.text)

    def test_cleaning_is_mechanical(self) -> None:
        raw = "\ufeff原句，标点不改。\x00\n\n\n\n下一句！"
        self.assertEqual(normalize_text(raw), "原句，标点不改。\n\n下一句！")


class ChapterTests(unittest.TestCase):
    def _titles(self, text: str) -> list[str | None]:
        return [chapter.title for chapter in segment_chapters(text).chapters]

    def test_chinese_first_chapter(self) -> None:
        titles = self._titles("第一章 出发\n这是第一段测试文字。\n第二章 到达\n这是第二段测试文字。")
        self.assertEqual(titles, ["第一章 出发", "第二章 到达"])

    def test_numeric_chapter(self) -> None:
        titles = self._titles("第1章 出发\n这是第一段测试文字。\n第2章 到达\n这是第二段测试文字。")
        self.assertEqual(titles, ["第1章 出发", "第2章 到达"])

    def test_chinese_hui(self) -> None:
        titles = self._titles("第一回 相遇\n这是第一段测试文字。\n第十二回 告别\n这是第二段测试文字。")
        self.assertEqual(titles, ["第一回 相遇", "第十二回 告别"])

    def test_volume_plus_chapter(self) -> None:
        titles = self._titles("卷一\n第一章 起点\n这是第一段测试文字。\n第二章 转折\n这是第二段测试文字。")
        self.assertEqual(titles, ["第一章 起点", "第二章 转折"])

    def test_english_chapter(self) -> None:
        titles = self._titles("Chapter 1 Start\nSynthetic body text.\nChapter 2 End\nMore synthetic text.")
        self.assertEqual(titles, ["Chapter 1 Start", "Chapter 2 End"])

    def test_special_headings_fanwai_and_afterword(self) -> None:
        titles = self._titles("番外 小雨\n这是番外测试文字。\n后记\n这是后记测试文字。")
        self.assertEqual(titles, ["番外 小雨", "后记"])

    def test_no_chapter_fallback(self) -> None:
        result = segment_chapters("没有章节标题的自行生成短文本。")
        self.assertEqual(len(result.chapters), 1)
        self.assertEqual(result.detection_confidence, "low")
        self.assertTrue(result.needs_review)

    def test_body_mention_not_misdetected(self) -> None:
        text = "他在纸上写下‘第一章’三个字，但这只是正文中的一句话。\n随后他合上本子。"
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 1)
        self.assertIsNone(result.chapters[0].title)

    def test_ambiguous_single_heading_in_body_falls_back(self) -> None:
        prefix = "这是一段开头。" * 80
        result = segment_chapters(prefix + "\n第一章\n这只是正文里单独出现的词。")
        self.assertEqual(result.detection_confidence, "low")
        self.assertTrue(result.needs_review)


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = TemporaryPipeline()

    def tearDown(self) -> None:
        self.layout.close()

    def _write(self, name: str, text: str, encoding: str = "utf-8") -> Path:
        path = self.layout.config.input_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding=encoding)
        return path

    def _manifest(self) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in self.layout.config.manifest_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_empty_file_fails_without_output(self) -> None:
        self._write("empty.txt", "")
        summary = run_preprocessor(self.layout.config)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.processed, 0)

    def test_exact_duplicate_file_detection(self) -> None:
        body = "第一章\n这是足够长的自制测试正文。"
        first = self._write("a.txt", body)
        second = self.layout.config.input_dir / "b.txt"
        second.write_bytes(first.read_bytes())
        summary = run_preprocessor(self.layout.config)
        self.assertEqual(summary.duplicates, 1)
        self.assertEqual(len(self._manifest()), 1)
        self.assertIn("exact_file", self._manifest()[0]["duplicate_kinds"])

    def test_same_text_different_encoding_is_normalized_duplicate(self) -> None:
        body = "第一章\n这是不同编码但正文相同的测试。"
        self._write("a.txt", body, "utf-8")
        path = self.layout.config.input_dir / "b.txt"
        path.write_bytes(body.encode("gb18030"))
        summary = run_preprocessor(self.layout.config)
        self.assertEqual(summary.duplicates, 1)
        self.assertIn("normalized_text", self._manifest()[0]["duplicate_kinds"])

    def test_repeat_run_skips_unchanged(self) -> None:
        self._write("repeat.txt", "第一章\n这是重复运行测试正文。")
        first = run_preprocessor(self.layout.config)
        second = run_preprocessor(self.layout.config)
        self.assertEqual(first.processed, 1)
        self.assertEqual(second.skipped, 1)
        self.assertEqual(second.processed, 0)

    def test_modified_file_is_reprocessed(self) -> None:
        path = self._write("change.txt", "第一章\n这是修改前的测试正文。")
        run_preprocessor(self.layout.config)
        first_work = self._manifest()[0]["work_id"]
        path.write_text("第一章\n这是修改后的测试正文。", encoding="utf-8")
        summary = run_preprocessor(self.layout.config)
        second_work = self._manifest()[0]["work_id"]
        self.assertEqual(summary.processed, 1)
        self.assertNotEqual(first_work, second_work)

    def test_deterministic_ids_and_hashes_across_clean_runs(self) -> None:
        body = "第一章\n这是确定性测试的第一段。\n第二章\n这是确定性测试的第二段。"
        self._write("stable.txt", body)
        run_preprocessor(self.layout.config)
        first_manifest = self._manifest()[0]
        work_dir = self.layout.config.output_dir / str(first_manifest["work_id"])
        first_chapters = (work_dir / "chapters.jsonl").read_text(encoding="utf-8")

        second_layout = TemporaryPipeline()
        try:
            (second_layout.config.input_dir / "renamed.txt").write_text(body, encoding="utf-8")
            run_preprocessor(second_layout.config)
            second_manifest = [json.loads(line) for line in second_layout.config.manifest_path.read_text(encoding="utf-8").splitlines()][0]
            second_chapters = (second_layout.config.output_dir / str(second_manifest["work_id"]) / "chapters.jsonl").read_text(encoding="utf-8")
            self.assertEqual(first_manifest["work_id"], second_manifest["work_id"])
            first_ids = [json.loads(line)["chapter_id"] for line in first_chapters.splitlines()]
            second_ids = [json.loads(line)["chapter_id"] for line in second_chapters.splitlines()]
            self.assertEqual(first_ids, second_ids)
            self.assertEqual(first_manifest["hash"], second_manifest["hash"])
        finally:
            second_layout.close()

    def test_hash_fields_match_source_and_normalized_text(self) -> None:
        path = self._write("hash.txt", "\ufeff第一章\r\n这是哈希测试正文。\r\n")
        run_preprocessor(self.layout.config)
        record = self._manifest()[0]
        work = json.loads((self.layout.config.output_dir / str(record["work_id"]) / "work.json").read_text(encoding="utf-8"))
        self.assertEqual(work["original_file_sha256"], sha256_file(path))
        self.assertEqual(work["normalized_text_sha256"], sha256_text(normalize_text(extract_text(path).text)))

    def test_manifest_contains_metadata_not_body(self) -> None:
        marker = "绝不应进入清单的正文标记"
        self._write("manifest.txt", f"第一章\n{marker}。")
        run_preprocessor(self.layout.config)
        content = self.layout.config.manifest_path.read_text(encoding="utf-8")
        self.assertNotIn(marker, content)
        self.assertIn("private_location_id", content)
        self.assertNotIn(str(self.layout.private), content)

    def test_structured_work_has_evidence_location_fields(self) -> None:
        self._write("evidence.txt", "第一章\n这是第一段定位测试文字。\n第二章\n这是第二段定位测试文字。")
        run_preprocessor(self.layout.config)
        record = self._manifest()[0]
        work_dir = self.layout.config.output_dir / str(record["work_id"])
        chapters = [json.loads(line) for line in (work_dir / "chapters.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(chapters[0]["relative_path"], "text/0001.txt")
        self.assertEqual(chapters[0]["span_scope"], "chapter_text")
        self.assertEqual(chapters[0]["source_span"]["start_char"], 0)
        self.assertEqual(chapters[0]["source_span"]["end_char"], chapters[0]["character_count"])
        self.assertIn("work_text_span", chapters[0])
        self.assertEqual(len(chapters[0]["chapter_text_sha256"]), 64)

    def test_mobi_is_deferred_not_failed(self) -> None:
        (self.layout.config.input_dir / "legacy.mobi").write_bytes(b"synthetic-mobi-placeholder")
        summary = run_preprocessor(self.layout.config)
        self.assertEqual(summary.deferred, 1)
        self.assertEqual(summary.failed, 0)
        self.assertEqual(self._manifest()[0]["processing_status"], "deferred")

    def test_txt_metadata_is_not_guessed(self) -> None:
        self._write("文件名不是可靠书名.txt", "第一章\n这是元数据测试正文。")
        run_preprocessor(self.layout.config)
        record = self._manifest()[0]
        self.assertIsNone(record["title"])
        self.assertIsNone(record["author"])


class SafetyAndSchemaTests(unittest.TestCase):
    def test_private_directory_git_leak_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            secret = repo / "_private" / "secret.txt"
            secret.parent.mkdir()
            secret.write_text("synthetic secret", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "-f", "_private/secret.txt"], check=True)
            report = validate_repo(repo)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["private"], 1)

    def test_schemas_are_valid_json_schema(self) -> None:
        schemas = [
            json.loads((ROOT / "schemas" / "scene_card.schema.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "schemas" / "story_card.schema.json").read_text(encoding="utf-8")),
        ]
        for schema in schemas:
            validate_schema(schema)
        try:
            from jsonschema.validators import Draft202012Validator
        except ImportError:
            for schema in schemas:
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
        else:
            for schema in schemas:
                Draft202012Validator.check_schema(schema)

    def test_id_helpers_are_deterministic(self) -> None:
        digest = sha256_text("自行生成的确定性文本")
        chapter_digest = sha256_text("章节正文")
        fingerprint = DEFAULT_PROCESSING_CONTRACT.fingerprint
        self.assertEqual(make_work_id(digest), make_work_id(digest))
        self.assertEqual(
            make_chapter_id(digest, 1, chapter_digest, fingerprint, 0, 4),
            make_chapter_id(digest, 1, chapter_digest, fingerprint, 0, 4),
        )
        self.assertNotEqual(
            make_chapter_id(digest, 1, chapter_digest, fingerprint, 0, 4),
            make_chapter_id(digest, 2, chapter_digest, fingerprint, 0, 4),
        )


if __name__ == "__main__":
    unittest.main()
