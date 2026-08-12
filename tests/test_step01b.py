from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from novel_preprocessor.chapters import segment_chapters
from novel_preprocessor.contract import DEFAULT_PROCESSING_CONTRACT
from novel_preprocessor.evidence import EvidenceValidationError, validate_evidence_ref
from novel_preprocessor.hashing import make_chapter_id, sha256_text
from novel_preprocessor.packets import export_packets
from novel_preprocessor.pipeline import PreprocessorConfig, run_preprocessor
from validate_card_schemas import validate_instance
from validate_private_boundaries import classify_forbidden, validate_repo


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

    def source(self, name: str, text: str) -> Path:
        path = self.config.input_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def manifest(self) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in self.config.manifest_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]


class ProcessorContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = Layout()
        self.layout.source("contract.txt", "第一章\n" + "甲走过长廊。" * 20 + "\n第二章\n" + "乙推开木门。" * 20)

    def tearDown(self) -> None:
        self.layout.close()

    def test_same_source_and_contract_skips(self) -> None:
        self.assertEqual(run_preprocessor(self.layout.config).processed, 1)
        second = run_preprocessor(self.layout.config)
        self.assertEqual(second.skipped, 1)
        self.assertEqual(second.processed, 0)

    def test_contract_change_reprocesses_unchanged_source(self) -> None:
        run_preprocessor(self.layout.config)
        changed = replace(DEFAULT_PROCESSING_CONTRACT, extraction="extract-v1-test-change")
        config = PreprocessorConfig.from_roots(self.layout.repo, self.layout.private, changed)
        second = run_preprocessor(config)
        self.assertEqual(second.processed, 1)
        work_id = str(self.layout.manifest()[0]["work_id"])
        work = json.loads((config.output_dir / work_id / "work.json").read_text(encoding="utf-8"))
        self.assertEqual(work["processing_fingerprint"], changed.fingerprint)

    def test_segmentation_contract_change_rebuilds_chapter_artifact(self) -> None:
        run_preprocessor(self.layout.config)
        work_id = str(self.layout.manifest()[0]["work_id"])
        chapter_path = self.layout.config.output_dir / work_id / "chapters.jsonl"
        before = [json.loads(line) for line in chapter_path.read_text(encoding="utf-8").splitlines()]
        changed = replace(DEFAULT_PROCESSING_CONTRACT, chapter_segmentation="chapter-v2-test-change")
        config = PreprocessorConfig.from_roots(self.layout.repo, self.layout.private, changed)
        result = run_preprocessor(config)
        after = [json.loads(line) for line in chapter_path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(result.processed, 1)
        self.assertNotEqual(before[0]["chapter_id"], after[0]["chapter_id"])
        self.assertEqual(after[0]["processing_fingerprint"], changed.fingerprint)

    def test_incomplete_artifact_cannot_skip(self) -> None:
        run_preprocessor(self.layout.config)
        work_id = str(self.layout.manifest()[0]["work_id"])
        missing = self.layout.config.output_dir / work_id / "text" / "0001.txt"
        missing.unlink()
        result = run_preprocessor(self.layout.config)
        self.assertEqual(result.processed, 1)
        self.assertTrue(missing.is_file())

    def test_chapter_id_binds_text_boundary_and_contract(self) -> None:
        work_sha = sha256_text("整本正文")
        text_sha = sha256_text("章节正文")
        fingerprint = DEFAULT_PROCESSING_CONTRACT.fingerprint
        base = make_chapter_id(work_sha, 1, text_sha, fingerprint, 0, 4)
        self.assertEqual(base, make_chapter_id(work_sha, 1, text_sha, fingerprint, 0, 4))
        self.assertNotEqual(base, make_chapter_id(work_sha, 1, sha256_text("章节改文"), fingerprint, 0, 4))
        self.assertNotEqual(base, make_chapter_id(work_sha, 1, text_sha, fingerprint, 1, 5))

    def test_real_manifest_is_private_first(self) -> None:
        run_preprocessor(self.layout.config)
        self.assertEqual(self.layout.config.manifest_path, self.layout.private / "manifests" / "library_manifest.jsonl")
        self.assertTrue(self.layout.config.manifest_path.is_file())
        self.assertFalse((self.layout.repo / "manifests" / "library_manifest.jsonl").exists())
        self.assertEqual((ROOT / "manifests" / "library_manifest.jsonl").read_text(encoding="utf-8"), "")


class EvidenceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = Layout()
        self.layout.source("evidence.txt", "第一章\n" + "证据坐标只针对章节正文。" * 12)
        run_preprocessor(self.layout.config)
        work_id = str(self.layout.manifest()[0]["work_id"])
        self.work_dir = self.layout.config.output_dir / work_id
        self.chapter = json.loads((self.work_dir / "chapters.jsonl").read_text(encoding="utf-8").splitlines()[0])
        self.text = (self.work_dir / self.chapter["relative_path"]).read_text(encoding="utf-8")
        self.ref = {
            "work_id": work_id,
            "chapter_id": self.chapter["chapter_id"],
            "chapter_text_sha256": self.chapter["chapter_text_sha256"],
            "span_scope": "chapter_text",
            "source_span": {"start_char": 0, "end_char": 4},
            "quote_sha256": sha256_text(self.text[0:4]),
        }

    def tearDown(self) -> None:
        self.layout.close()

    def test_evidence_round_trip(self) -> None:
        report = validate_evidence_ref(self.ref, self.layout.private)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(self.text[report["start_char"]:report["end_char"]], self.text[0:4])

    def test_wrong_quote_hash_fails(self) -> None:
        invalid = {**self.ref, "quote_sha256": "0" * 64}
        with self.assertRaises(EvidenceValidationError):
            validate_evidence_ref(invalid, self.layout.private)

    def test_wrong_chapter_hash_fails(self) -> None:
        invalid = {**self.ref, "chapter_text_sha256": "0" * 64}
        with self.assertRaises(EvidenceValidationError):
            validate_evidence_ref(invalid, self.layout.private)

    def test_invalid_span_fails(self) -> None:
        invalid = {**self.ref, "source_span": {"start_char": 0, "end_char": len(self.text) + 1}}
        with self.assertRaises(EvidenceValidationError):
            validate_evidence_ref(invalid, self.layout.private)

    def _claim(self) -> dict[str, object]:
        return {
            "claim_type": "emotion_interpretation",
            "description": "合成测试解释",
            "epistemic_status": "inferred",
            "confidence": 0.7,
            "evidence_refs": [self.ref],
        }

    def _scene(self) -> dict[str, object]:
        return {
            "scene_id": "scene_001", "work_id": self.ref["work_id"],
            "chapter_id": self.ref["chapter_id"], "chapter_text_sha256": self.ref["chapter_text_sha256"],
            "span_scope": "chapter_text", "source_span": {"start_char": 0, "end_char": 4},
            "characters": ["甲"],
            "character_goals": [{
                "character": "甲", "goal": "开门", "claim_type": "character_goal",
                "epistemic_status": "observed", "confidence": 1.0, "evidence_refs": [self.ref]
            }],
            "constraints": [], "trigger": None, "conflict": None, "action": None,
            "outcome": None, "state_change": None, "reader_information_gain": [],
            "character_information_gain": [], "emotion_before": [self._claim()],
            "emotion_after": [], "setup": [], "payoff": [], "evidence_refs": [self.ref],
            "confidence": 0.8, "analyst_notes": None,
        }

    def _story(self) -> dict[str, object]:
        claim = self._claim()
        return {
            "work_id": self.ref["work_id"], "premise": None,
            "core_character_goals": [claim], "character_relations": [], "power_relations": [],
            "causal_chain": [], "conflict_chain": [], "emotion_curve": [claim],
            "information_release": [], "setup_payoff": [], "chapter_hooks": [],
            "reusable_mechanisms": [claim], "genre_specific_mechanisms": [],
            "failure_patterns": [claim], "counterexamples": [claim], "evidence_refs": [self.ref],
        }

    def test_scene_and_story_instances_pass(self) -> None:
        scene_schema = json.loads((ROOT / "schemas" / "scene_card.schema.json").read_text(encoding="utf-8"))
        story_schema = json.loads((ROOT / "schemas" / "story_card.schema.json").read_text(encoding="utf-8"))
        validate_instance(scene_schema, self._scene())
        validate_instance(story_schema, self._story())

    def test_missing_chapter_hash_fails_schema(self) -> None:
        scene = self._scene()
        del scene["chapter_text_sha256"]
        schema = json.loads((ROOT / "schemas" / "scene_card.schema.json").read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            validate_instance(schema, scene)

    def test_evidence_ref_missing_chapter_hash_fails_schema(self) -> None:
        scene = self._scene()
        del scene["evidence_refs"][0]["chapter_text_sha256"]
        schema = json.loads((ROOT / "schemas" / "scene_card.schema.json").read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            validate_instance(schema, scene)

    def test_invalid_span_scope_fails_schema(self) -> None:
        scene = self._scene()
        scene["span_scope"] = "whole_book"
        schema = json.loads((ROOT / "schemas" / "scene_card.schema.json").read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            validate_instance(schema, scene)

    def test_claim_missing_epistemic_status_fails(self) -> None:
        story = self._story()
        del story["reusable_mechanisms"][0]["epistemic_status"]
        schema = json.loads((ROOT / "schemas" / "story_card.schema.json").read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            validate_instance(schema, story)


class PrivacyExactContentTests(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        repo = root / "repo"
        private = root / "_private"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (private / "01_原始小说").mkdir(parents=True)
        (private / "02_结构化文本" / "wrk_test" / "text").mkdir(parents=True)
        return temp, repo, private

    def test_raw_novel_copied_to_innocent_path_fails(self) -> None:
        temp, repo, private = self._repo()
        try:
            content = "完全相同的合成原始小说内容。"
            (private / "01_原始小说" / "source.txt").write_text(content, encoding="utf-8")
            target = repo / "docs" / "innocent.txt"
            target.parent.mkdir()
            target.write_text(content, encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "docs/innocent.txt"], check=True)
            report = validate_repo(repo, private)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["raw_novel_exact_content"], 1)
        finally:
            temp.cleanup()

    def test_structured_chapter_copied_to_innocent_path_fails(self) -> None:
        temp, repo, private = self._repo()
        try:
            content = "完全相同的合成结构化章节。"
            chapter = private / "02_结构化文本" / "wrk_test" / "text" / "0001.txt"
            chapter.write_text(content, encoding="utf-8")
            target = repo / "docs" / "innocent.txt"
            target.parent.mkdir()
            target.write_text(content, encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "docs/innocent.txt"], check=True)
            report = validate_repo(repo, private)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["structured_chapter_exact_content"], 1)
        finally:
            temp.cleanup()

    def test_chatgpt_packet_path_is_private_artifact(self) -> None:
        reasons = classify_forbidden("_private/03_ChatGPT蒸馏包/wrk_test/parts/part_001.md")
        self.assertIn("private", reasons)
        self.assertIn("chatgpt_packet", reasons)


class ChapterConservativeRegressionTests(unittest.TestCase):
    def test_standalone_first_chapter_once_needs_review(self) -> None:
        result = segment_chapters("他说这是引用。\n第一章\n然后继续解释引用内容。")
        self.assertTrue(result.needs_review)

    def test_multiple_heading_quotes_need_review(self) -> None:
        result = segment_chapters("引用清单\n第一章\n解释一。\n第二章\n解释二。")
        self.assertTrue(result.needs_review)

    def test_long_preface_then_real_chapters(self) -> None:
        text = "前言内容。" * 120 + "\n第一章：起点\n" + "甲向前走。" * 30 + "\n第二章：终点\n" + "乙停下来。" * 30
        result = segment_chapters(text)
        self.assertEqual(len(result.chapters), 2)
        self.assertFalse(result.needs_review)

    def test_volume_with_long_preface_needs_review(self) -> None:
        text = "卷一\n" + "卷前说明。" * 30 + "\n第一章\n" + "正文。" * 30
        self.assertTrue(segment_chapters(text).needs_review)

    def test_punctuated_titles_detected(self) -> None:
        text = "第一章：雨夜\n" + "甲。" * 50 + "\n第二章——晴天\n" + "乙。" * 50
        self.assertEqual(len(segment_chapters(text).chapters), 2)

    def test_short_chapters_need_review(self) -> None:
        self.assertTrue(segment_chapters("第一章\n短。\n第二章\n也短。").needs_review)

    def test_extremely_long_chapter_needs_review(self) -> None:
        text = "第一章\n" + "甲" * 200_001 + "\n第二章\n" + "乙" * 100
        self.assertTrue(segment_chapters(text).needs_review)

    def test_skipped_number_needs_review(self) -> None:
        text = "第一章\n" + "甲。" * 50 + "\n第三章\n" + "乙。" * 50
        self.assertTrue(segment_chapters(text).needs_review)

    def test_duplicate_number_needs_review(self) -> None:
        text = "第一章\n" + "甲。" * 50 + "\n第一章\n" + "乙。" * 50
        self.assertTrue(segment_chapters(text).needs_review)

    def test_mixed_markdown_levels_need_review(self) -> None:
        text = "# 第一章\n" + "甲。" * 50 + "\n## 第二章\n" + "乙。" * 50
        self.assertTrue(segment_chapters(text).needs_review)


class PacketExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = Layout()
        text = "第一章\n" + "甲沿着长路前行。" * 80 + "\n第二章\n" + "乙在门前停下。" * 80
        self.layout.source("packet.txt", text)
        run_preprocessor(self.layout.config)
        self.work_id = str(self.layout.manifest()[0]["work_id"])

    def tearDown(self) -> None:
        self.layout.close()

    def test_packet_generation_and_round_trip(self) -> None:
        [output] = export_packets(self.layout.private, [self.work_id], max_chars_per_part=700)
        manifest = json.loads((output / "packet_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["work_id"], self.work_id)
        self.assertGreater(len(manifest["parts"]), 1)
        self.assertNotIn(str(self.layout.private), json.dumps(manifest, ensure_ascii=False))

        reconstructed: dict[str, list[tuple[int, str]]] = {}
        for part in manifest["parts"]:
            content = (output / part["relative_path"]).read_text(encoding="utf-8")
            self.assertLessEqual(len(content), 700)
            self.assertEqual(sha256_text(content), part["part_sha256"])
            self.assertIn("WORK:", content)
            self.assertIn("CHAPTER_ID:", content)
            self.assertIn("CHAPTER_TEXT_SHA256:", content)
            self.assertIn("PROCESSING_CONTRACT_VERSION:", content)
            for item in part["slices"]:
                piece = content[item["part_text_start_char"]:item["part_text_end_char"]]
                self.assertEqual(sha256_text(piece), item["slice_sha256"])
                reconstructed.setdefault(item["chapter_id"], []).append((item["slice_start_char"], piece))

        work_dir = self.layout.config.output_dir / self.work_id
        chapter_records = [json.loads(line) for line in (work_dir / "chapters.jsonl").read_text(encoding="utf-8").splitlines()]
        for chapter in chapter_records:
            original = (work_dir / chapter["relative_path"]).read_text(encoding="utf-8")
            rebuilt = "".join(piece for _, piece in sorted(reconstructed[chapter["chapter_id"]]))
            self.assertEqual(rebuilt, original)

    def test_export_requires_explicit_selection(self) -> None:
        with self.assertRaises(ValueError):
            export_packets(self.layout.private, [], max_chars_per_part=700)

    def test_cli_work_id_selection(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "export_chatgpt_packets.py"),
                "--private-root", str(self.layout.private),
                "--work-id", self.work_id,
                "--max-chars-per-part", "700",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertTrue((self.layout.private / "03_ChatGPT蒸馏包" / self.work_id / "packet_manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
