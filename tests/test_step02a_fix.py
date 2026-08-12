from __future__ import annotations

from dataclasses import replace
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from novel_preprocessor.chapters import detect_heading_candidates, segment_chapters
from novel_preprocessor.contract import DEFAULT_PROCESSING_CONTRACT
from novel_preprocessor.integrity import analyze_source_integrity
from novel_preprocessor.pipeline import PreprocessorConfig, run_preprocessor


class CompactInlineHuiTests(unittest.TestCase):
    @staticmethod
    def _body(marker: str) -> str:
        return f"合成正文{marker}沿走廊向前延伸。" * 20

    def _valid_text(self) -> tuple[str, list[str], list[str]]:
        front = "合成书名前置说明\n"
        titles = ["第一回雨夜来客", "第二回旧城钟声", "第三回河岸灯火", "第四回山门旧事"]
        bodies = [self._body(letter) for letter in "ABCD"]
        text = front + titles[0] + "\n" + bodies[0]
        for title, body in zip(titles[1:], bodies[1:]):
            text += title + "\n" + body
        return text, titles, bodies

    def test_sequenced_compact_inline_hui_splits_at_heading_start(self) -> None:
        text, titles, bodies = self._valid_text()
        result = segment_chapters(text)

        self.assertEqual([chapter.title for chapter in result.chapters], titles)
        self.assertEqual(result.front_matter, "合成书名前置说明\n")
        self.assertFalse(result.needs_review)
        self.assertEqual(result.warnings, [])
        for index, chapter in enumerate(result.chapters):
            self.assertEqual(chapter.start_char, text.index(titles[index]))
            self.assertTrue(chapter.text.startswith(titles[index] + "\n"))
            self.assertIn(bodies[index], chapter.text)
            if index:
                self.assertNotIn(bodies[index - 1], chapter.text)

        candidates = detect_heading_candidates(text)
        self.assertEqual([candidate.candidate_type for candidate in candidates], ["compact_inline_hui"] * 4)
        integrity = analyze_source_integrity(chapter.title for chapter in result.chapters)
        self.assertEqual(integrity.source_integrity_status, "PASS")
        self.assertTrue(integrity.distillation_allowed)
        self.assertEqual(integrity.numbered_chapter_count, 4)

    def test_single_body_like_compact_hui_is_rejected(self) -> None:
        text = self._body("A") + "他读到第八回风波再起\n" + self._body("B")
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 1)
        self.assertIsNone(result.chapters[0].title)

    def test_two_consecutive_compact_hui_candidates_are_rejected(self) -> None:
        text = self._body("A") + "第八回风波再起\n" + self._body("B") + "第九回旧事重提\n" + self._body("C")
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 1)
        self.assertIsNone(result.chapters[0].title)

    def test_two_nonconsecutive_compact_hui_candidates_are_rejected(self) -> None:
        text = self._body("A") + "第八回风波再起\n" + self._body("B") + "第十五回旧事重提\n" + self._body("C")
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 1)
        self.assertIsNone(result.chapters[0].title)

    def test_sentence_punctuation_is_rejected(self) -> None:
        text = "".join(
            f"{self._body(str(number))}第{number}回风波再起，他推开门\n"
            for number in range(1, 5)
        )
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 1)
        self.assertIsNone(result.chapters[0].title)

    def test_overlong_compact_titles_are_rejected(self) -> None:
        long_title = "这是明显超过限制长度的合成标题文字"
        text = "".join(
            f"{self._body(str(number))}第{number}回{long_title}\n"
            for number in range(1, 5)
        )
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 1)
        self.assertIsNone(result.chapters[0].title)

    def test_work_specific_markers_are_absent_from_production_code(self) -> None:
        production = "\n".join(
            (ROOT / "src" / "novel_preprocessor" / name).read_text(encoding="utf-8")
            for name in ("chapters.py", "integrity.py")
        )
        for forbidden in (
            "射雕英雄传",
            "wrk_ecadf1440d73d61ef31ec5ed",
            "风雪惊变",
            "华山论剑",
            "range(1, 41)",
        ):
            self.assertNotIn(forbidden, production)


class CompactInlineHuiContractTests(unittest.TestCase):
    def test_v3_fingerprint_reprocesses_under_compact_hui_contract(self) -> None:
        temp = tempfile.TemporaryDirectory()
        try:
            root = Path(temp.name)
            repo = root / "repo"
            private = root / "_private"
            old_contract = replace(
                DEFAULT_PROCESSING_CONTRACT,
                chapter_segmentation="chapter-v3-strong-weak-front-matter",
            )
            old_config = PreprocessorConfig.from_roots(repo, private, old_contract)
            old_config.ensure_layout()
            source = old_config.input_dir / "synthetic-contract.txt"
            source.write_text(
                "第1章 起点\n" + self._body("A") + "\n第2章 终点\n" + self._body("B"),
                encoding="utf-8",
            )
            self.assertEqual(run_preprocessor(old_config).processed, 1)

            new_config = PreprocessorConfig.from_roots(repo, private)
            self.assertNotEqual(old_contract.fingerprint, DEFAULT_PROCESSING_CONTRACT.fingerprint)
            self.assertEqual(run_preprocessor(new_config).processed, 1)
            manifest = [
                json.loads(line)
                for line in new_config.manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(manifest[0]["processing_fingerprint"], DEFAULT_PROCESSING_CONTRACT.fingerprint)
        finally:
            temp.cleanup()

    @staticmethod
    def _body(marker: str) -> str:
        return f"合成正文{marker}保持足够长度。" * 20


if __name__ == "__main__":
    unittest.main()
