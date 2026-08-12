from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from novel_preprocessor.chapters import segment_chapters
from novel_preprocessor.cleaning import normalize_text
from novel_preprocessor.contract import DEFAULT_PROCESSING_CONTRACT, ProcessingContract
from novel_preprocessor.extractors import extract_text
from novel_preprocessor.hashing import sha256_text
from novel_preprocessor.integrity import analyze_source_integrity
from novel_preprocessor.packets import PacketExportError, export_packets
from novel_preprocessor.pipeline import PreprocessorConfig, run_preprocessor
from validate_private_boundaries import validate_repo


FIXTURE_DIR = ROOT / "tests" / "fixtures" / "golden"
GOLDEN = FIXTURE_DIR / "novel_preprocessor_golden_v1.txt"
EXPECTED = json.loads((FIXTURE_DIR / "novel_preprocessor_golden_v1.expected.json").read_text(encoding="utf-8"))
OLD_PROCESSING_FINGERPRINT = "85eb4cfd8351876bdab7e60dc2dd3b5a6ebe5082707d989f489c4ae72514538f"


class Layout:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.repo = root / "repo"
        self.private = root / "_private"
        self.config = PreprocessorConfig.from_roots(self.repo, self.private)
        self.config.ensure_layout()

    def close(self) -> None:
        self.temp.cleanup()

    def source(self, name: str, text: str) -> None:
        (self.config.input_dir / name).write_text(text, encoding="utf-8")

    def work(self) -> tuple[dict[str, object], Path]:
        manifest = [
            json.loads(line)
            for line in self.config.manifest_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        work_dir = self.config.output_dir / str(manifest[0]["work_id"])
        return json.loads((work_dir / "work.json").read_text(encoding="utf-8")), work_dir


class GoldenDetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = Layout()
        shutil.copyfile(GOLDEN, self.layout.config.input_dir / "synthetic-golden.txt")
        result = run_preprocessor(self.layout.config)
        self.assertEqual(result.processed, 1)
        self.work, self.work_dir = self.layout.work()
        self.chapters = [
            json.loads(line)
            for line in (self.work_dir / "chapters.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def tearDown(self) -> None:
        self.layout.close()

    def test_fixture_hash_and_normalized_identity(self) -> None:
        self.assertEqual(hashlib.sha256(GOLDEN.read_bytes()).hexdigest(), EXPECTED["source_sha256"])
        normalized = normalize_text(extract_text(GOLDEN).text)
        self.assertEqual(sha256_text(normalized), EXPECTED["normalized_sha256"])
        self.assertEqual(self.work["work_id"], EXPECTED["work_id"])

    def test_exact_fifty_titles_without_split_or_numbering_anomaly(self) -> None:
        titles = [chapter["chapter_title"] for chapter in self.chapters]
        self.assertEqual(titles, EXPECTED["titles"])
        self.assertEqual(len(titles), EXPECTED["chapter_count"])
        self.assertEqual(len(set(titles) - set(EXPECTED["titles"])), EXPECTED["false_splits"])
        self.assertEqual(len(set(EXPECTED["titles"]) - set(titles)), EXPECTED["missed_splits"])
        integrity = self.work["source_integrity"]
        anomaly_count = (
            integrity["gap_event_count"]
            + integrity["duplicate_number_count"]
            + integrity["backward_number_count"]
        )
        self.assertEqual(anomaly_count, EXPECTED["numbering_anomalies"])
        self.assertEqual(self.work["needs_review"], EXPECTED["needs_review"])

    def test_front_matter_is_separate_and_complete(self) -> None:
        self.assertTrue(self.work["front_matter_present"])
        front_path = self.work_dir / str(self.work["front_matter_relative_path"])
        front = front_path.read_text(encoding="utf-8")
        self.assertEqual(len(front), self.work["front_matter_character_count"])
        self.assertEqual(sha256_text(front), self.work["front_matter_sha256"])
        self.assertIn(EXPECTED["chapter1_forbidden_text"], front)
        normalized = normalize_text(extract_text(GOLDEN).text)
        self.assertEqual(front, normalized[:normalized.index(EXPECTED["titles"][0])])
        chapter1 = (self.work_dir / self.chapters[0]["relative_path"]).read_text(encoding="utf-8")
        self.assertTrue(chapter1.startswith(EXPECTED["titles"][0]))
        self.assertNotIn(EXPECTED["chapter1_forbidden_text"], chapter1)

    def test_all_traps_are_preserved_inside_chapter_text(self) -> None:
        chapter_text = "\n".join(
            (self.work_dir / chapter["relative_path"]).read_text(encoding="utf-8")
            for chapter in self.chapters
        )
        for trap in EXPECTED["trap_sentences"]:
            self.assertEqual(chapter_text.count(trap), 1, trap)

    def test_golden_integrity_and_packet_export_pass(self) -> None:
        self.assertEqual(self.work["source_integrity_status"], EXPECTED["source_integrity_status"])
        self.assertIs(self.work["distillation_allowed"], EXPECTED["distillation_allowed"])
        [packet] = export_packets(self.layout.private, [str(self.work["work_id"])], 20_000)
        self.assertTrue((packet / "packet_manifest.json").is_file())


class DetectorMutationTests(unittest.TestCase):
    def test_differently_worded_natural_language_traps_do_not_split(self) -> None:
        chapters: list[str] = []
        traps = [
            "第三节灯光熄灭以后，门房才想起那是值班表里的时段。",
            "第三卷：这个城市的人把收据按颜色归档，但那只是工作习惯。",
            "后记不是标题，只是海报角落里褪色的印刷字。",
            "番外两个字被盖在票根背面，并不代表故事另起一篇。",
        ]
        for number in range(1, 6):
            body = [f"第{number}章 合成场次{number:02d}", "合成正文沿走廊向前延伸。" * 12]
            if number <= len(traps):
                body.extend([traps[number - 1], "陷阱之后仍然属于同一章。" * 12])
            chapters.append("\n".join(body))
        result = segment_chapters("合成书名前置材料\n" + "\n".join(chapters))
        self.assertEqual([chapter.title for chapter in result.chapters], [f"第{i}章 合成场次{i:02d}" for i in range(1, 6)])
        self.assertFalse(result.needs_review)

    def test_compact_weak_titles_are_supported_conservatively(self) -> None:
        result = segment_chapters("番外 小雨\n" + "合成番外。" * 30 + "\n后记：写在最后\n" + "合成后记。" * 30)
        self.assertEqual([chapter.title for chapter in result.chapters], ["番外 小雨", "后记：写在最后"])
        self.assertTrue(result.needs_review)


class SourceIntegrityGateTests(unittest.TestCase):
    def _titles(self, numbers: list[int]) -> list[str]:
        return [f"第{number}章 合成标题" for number in numbers]

    def test_continuous_numbering_passes(self) -> None:
        result = analyze_source_integrity(self._titles(list(range(1, 51))))
        self.assertEqual(result.source_integrity_status, "PASS")
        self.assertTrue(result.distillation_allowed)

    def test_isolated_gap_warns(self) -> None:
        result = analyze_source_integrity(self._titles([1, 2, 4, 5]))
        self.assertEqual(result.source_integrity_status, "WARNING")
        self.assertFalse(result.distillation_allowed)

    def test_duplicate_warns(self) -> None:
        result = analyze_source_integrity(self._titles([1, 2, 2, 3]))
        self.assertEqual(result.source_integrity_status, "WARNING")
        self.assertEqual(result.duplicate_number_count, 1)

    def test_backward_warns(self) -> None:
        result = analyze_source_integrity(self._titles([1, 2, 1, 2]))
        self.assertEqual(result.source_integrity_status, "WARNING")
        self.assertEqual(result.backward_number_count, 1)

    def test_repeated_regular_gaps_fail(self) -> None:
        numbers = [*range(1, 31), *range(51, 81), *range(101, 131), *range(151, 181)]
        result = analyze_source_integrity(self._titles(numbers))
        self.assertEqual(result.source_integrity_status, "FAIL")
        self.assertTrue(result.systematic_gap_detected)
        self.assertEqual(result.estimated_missing_chapters, 60)

    def test_unnumbered_system_is_unknown(self) -> None:
        result = analyze_source_integrity(["序幕", "雨夜", "终场"])
        self.assertEqual(result.source_integrity_status, "UNKNOWN")
        self.assertFalse(result.distillation_allowed)

    def test_special_structure_does_not_fail_by_itself(self) -> None:
        result = analyze_source_integrity(["第1章 开始", "番外 小雨", "第2章 结束"])
        self.assertEqual(result.source_integrity_status, "PASS")

    def test_packet_export_blocks_systematically_incomplete_source(self) -> None:
        layout = Layout()
        try:
            numbers = [1, 2, 3, 10, 11, 12, 19, 20, 21, 28, 29]
            text = "\n".join(f"第{number}章 合成标题\n" + "合成正文。" * 30 for number in numbers)
            layout.source("incomplete.txt", text)
            run_preprocessor(layout.config)
            work, _ = layout.work()
            self.assertEqual(work["source_integrity_status"], "FAIL")
            self.assertFalse(work["distillation_allowed"])
            with self.assertRaisesRegex(PacketExportError, "书源完整性门禁拒绝导出"):
                export_packets(layout.private, [str(work["work_id"])])
        finally:
            layout.close()

    def test_packet_batch_preflight_prevents_partial_export(self) -> None:
        layout = Layout()
        try:
            layout.source("complete.txt", "\n".join(f"第{n}章 完整\n" + "完整正文。" * 30 for n in [1, 2, 3]))
            layout.source("incomplete.txt", "\n".join(f"第{n}章 残缺\n" + "合成正文。" * 30 for n in [1, 2, 3, 10, 11, 12, 19, 20, 21, 28]))
            run_preprocessor(layout.config)
            manifest = [
                json.loads(line)
                for line in layout.config.manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            complete = next(str(item["work_id"]) for item in manifest if item["source_integrity_status"] == "PASS")
            incomplete = next(str(item["work_id"]) for item in manifest if item["source_integrity_status"] == "FAIL")
            with self.assertRaises(PacketExportError):
                export_packets(layout.private, [complete, incomplete])
            self.assertFalse((layout.private / "03_ChatGPT蒸馏包" / complete).exists())
        finally:
            layout.close()


class ProcessingContractStep01CTests(unittest.TestCase):
    def test_processing_fingerprint_changed(self) -> None:
        self.assertNotEqual(DEFAULT_PROCESSING_CONTRACT.fingerprint, OLD_PROCESSING_FINGERPRINT)
        self.assertEqual(DEFAULT_PROCESSING_CONTRACT.chapter_segmentation, "chapter-v4-sequenced-compact-inline-hui")
        self.assertEqual(DEFAULT_PROCESSING_CONTRACT.structured_output_schema, "structured-v3-source-integrity")

    def test_old_default_contract_reprocesses_under_step01c_contract(self) -> None:
        layout = Layout()
        try:
            layout.source("contract-upgrade.txt", "第1章 起点\n" + "甲沿走廊前行。" * 20 + "\n第2章 终点\n" + "乙关上木门。" * 20)
            old_contract = ProcessingContract(
                version="1.0.0",
                extraction="extract-v1",
                normalization="normalize-v1",
                chapter_segmentation="chapter-v2-conservative",
                id_contract="artifact-id-v2",
                structured_output_schema="structured-v2",
            )
            old_config = PreprocessorConfig.from_roots(layout.repo, layout.private, old_contract)
            self.assertEqual(run_preprocessor(old_config).processed, 1)
            upgraded = run_preprocessor(layout.config)
            self.assertEqual(upgraded.processed, 1)
            work, _ = layout.work()
            self.assertEqual(work["processing_fingerprint"], DEFAULT_PROCESSING_CONTRACT.fingerprint)
        finally:
            layout.close()

    def test_production_code_has_no_golden_special_case(self) -> None:
        forbidden = [
            "小说蒸馏预处理_GOLDEN_TEST_V1",
            EXPECTED["work_id"],
            EXPECTED["source_sha256"],
            EXPECTED["normalized_sha256"],
            "59改50",
        ]
        production = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src" / "novel_preprocessor").glob("*.py"))
        for marker in forbidden:
            self.assertNotIn(marker, production)

    def test_declared_synthetic_golden_is_the_only_exact_content_exception(self) -> None:
        temp = tempfile.TemporaryDirectory()
        try:
            root = Path(temp.name)
            repo = root / "repo"
            private = root / "_private"
            target_dir = repo / "tests" / "fixtures" / "golden"
            raw_dir = private / "01_原始小说"
            target_dir.mkdir(parents=True)
            raw_dir.mkdir(parents=True)
            shutil.copyfile(GOLDEN, raw_dir / "source.txt")
            shutil.copyfile(GOLDEN, target_dir / GOLDEN.name)
            shutil.copyfile(FIXTURE_DIR / "novel_preprocessor_golden_v1.expected.json", target_dir / "novel_preprocessor_golden_v1.expected.json")
            import subprocess
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "tests/fixtures/golden"], check=True)
            self.assertEqual(validate_repo(repo, private)["status"], "PASS")
            copied = repo / "docs" / "innocent.txt"
            copied.parent.mkdir()
            shutil.copyfile(GOLDEN, copied)
            subprocess.run(["git", "-C", str(repo), "add", "docs/innocent.txt"], check=True)
            self.assertEqual(validate_repo(repo, private)["status"], "FAIL")
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
