#!/usr/bin/env python3
"""Candidate novel skill static validation only. NOT a literary quality test."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
C = ROOT / "experimental/novel-writing-v4"

def main() -> None:
    errors = []
    skill = (C / "SKILL.md").read_text("utf-8")
    template = (C / "writer-packet-template.md").read_text("utf-8")
    routing = json.loads((C / "module-routing.json").read_text("utf-8"))
    lineage = json.loads((ROOT / "state/lineage/NOVEL_METHOD_UPSTREAM_20261031.json").read_text("utf-8"))
    checkpoint = json.loads((ROOT / "state/continuity/LATEST_CHECKPOINT.json").read_text("utf-8"))
    project = json.loads((ROOT / "state/project_state.json").read_text("utf-8"))
    precedence = json.loads((C / "entrypoint-precedence.json").read_text("utf-8"))
    if not skill.startswith("---\nname: novel-writing-master\n"):
        errors.append("invalid skill frontmatter")
    if not routing.get("production") is False:
        errors.append("candidate accidentally promoted")
    if not lineage.get("candidate") or lineage.get("baseline",{}).get("actual_human_score") != "UNKNOWN":
        errors.append("internal score promoted to human")
    if checkpoint.get("sequence",0) < 211:
        errors.append("checkpoint regressed")
    if "NOVEL-IMPROVEMENT-MAINLINE-V1" not in (ROOT / "MAINLINE.md").read_text("utf-8"):
        errors.append("mainline unexpectedly missing")
    if project.get("next_required_action") != checkpoint.get("next_required_action"):
        errors.append("native state and checkpoint disagree on next action")
    if checkpoint.get("sequence") == 211 and project.get("next_required_action") != "AWAIT_ACTUAL_HUMAN_SCORE_OF_ONE_STANDALONE_COMPLETE_SHORT":
        errors.append("historic human score gate incorrectly bypassed")
    if precedence.get("production_route_unchanged") is not True:
        errors.append("candidate precedence unexpectedly mutates production")
    if precedence.get("version_namespace",{}).get("equivalence") is not False:
        errors.append("method4 and V4 incorrectly aliased")
    if precedence.get("legacy_locator",{}).get("legacy_next_action") == project.get("next_required_action") and checkpoint.get("sequence",0) > 200:
        errors.append("stale MAINLINE entry reactivated")
    if "entrypoint-precedence.json" not in skill:
        errors.append("candidate skill omits stale-entrypoint guard")
    mandatory = {"modules/character-pressure-test.md","modules/causal-proof-engine.md","rules/pass-isolation.md"}
    indexed = {m["path"]:m for m in routing["modules"]}
    if any(indexed.get(p,{}).get("status")!="ACTIVE" for p in mandatory):
        errors.append("mandatory editor/coordinator controls unavailable")
    excluded = [m for m in routing["modules"] if m["status"]=="EXCLUDED"]
    if len(excluded) < 3:
        errors.append("no concrete rejected methods")
    for m in routing["modules"]:
        if m.get("status") not in routing["statuses"]:
            errors.append("unknown status for "+m["path"])
        if m["status"] in {"ACTIVE","REVIEW_ONLY","REFERENCE_ONLY"} and m["path"].startswith(("modules/","rules/","workflows/")) and not (ROOT/m["path"]).is_file():
            errors.append("missing module "+m["path"])
    if routing.get("delete_policy",{}).get("immediate_files_to_physically_delete"):
        errors.append("historical deletion before readback and regression")
    if "history" in template.lower() and "不共享给作者" not in template:
        errors.append("missing clean writer isolation")
    if not all(token in skill for token in ["人物决策","独立写作","三级修稿","冷读","真人"]):
        errors.append("missing writer flow")
    if not all(x["license"]=="MIT" and len(x["sha"])==40 for x in lineage["candidate"]["upstreams"]):
        errors.append("unlocked upstream or license")
    # User's latest correction: genre interest is not literary approval.
    planning = C / "outline-first-20261102"
    files = [
        "00-READ-ME-FIRST.md", "01-method-learning-audit.md",
        "02-master-outline.md", "03-world-rules.md", "04-characters.md",
        "05-clue-reversal-payoff.md", "06-chapter-cards-01-12.md",
        "07-editorial-audit.md",
    ]
    if any(not (planning / p).is_file() for p in files):
        errors.append("outline-first planning artifact missing")
    else:
        index = (planning / files[0]).read_text("utf-8")
        character = (planning / files[4]).read_text("utf-8")
        clues = (planning / files[5]).read_text("utf-8")
        chapters = (planning / files[6]).read_text("utf-8")
        audit = (planning / files[7]).read_text("utf-8")
        if len(__import__("re").findall(r"(?m)^### 第\d{2}章", chapters)) != 12:
            errors.append("not exactly twelve chapter cards")
        if any(name not in character for name in ("叶渡", "谢临渊", "秦照月", "顾玄衡")):
            errors.append("main cast missing from character bible")
        if any("L%02d" % i not in clues for i in range(1, 9)):
            errors.append("main suspense locks not indexed")
        if "NO PROSE" not in index or "正文" not in audit:
            errors.append("planning-only instruction missing")
        if "题材" not in index or "438" not in index or "923" not in index:
            errors.append("genre interest incorrectly inherited as prose approval")
    if "2026-11-02 最新真人纠偏" not in skill or "outline-first-20261102" not in skill:
        errors.append("candidate route permits premature prose")
    correction = ROOT / "state/review_receipts/NOVEL_FANTASY_INTEREST_NOT_PROSE_APPROVAL_OUTLINE_FIRST_20261102.json"
    if correction.exists():
        j = json.loads(correction.read_text("utf-8"))
        if j.get("interpretation", {}).get("prior_opening_prose_approved") is not False:
            errors.append("latest human clarification not enforced")
    # November 3 commercial red-team: revision chain is append-only, not a prose approval.
    outline_index = (C / "outline-first-20261102/00-READ-ME-FIRST.md").read_text("utf-8")
    latest_v03 = C / "outline-first-20261102/12-minimal-causal-stabilization-v03-20261103.md"
    external_v01 = C / "outline-first-20261102/08-external-editor-rejection-20261103.md"
    external_v02 = C / "outline-first-20261102/13-same-ai-editor-v02-recheck-20261103.md"
    for pth in (latest_v03, external_v01, external_v02):
        if not pth.is_file():
            errors.append("missing red-team revision evidence " + pth.name)
    if all(x.is_file() for x in (latest_v03, external_v01, external_v02)):
        latest = latest_v03.read_text("utf-8")
        first_report = external_v01.read_text("utf-8")
        recheck = external_v02.read_text("utf-8")
        import re
        if len(re.findall(r"(?m)^\\| \\d{2}｜", latest)) != 12:
            errors.append("v03 no longer has twelve distinct chapter state transitions")
        for token in ("第8章", "软禁", "第9章", "押运", "T-60", "不强制筑基", "双榜"):
            if token not in latest and token != "双榜":
                errors.append("v03 missing required causality marker " + token)
        if "V0.3" not in outline_index or "12-minimal-causal-stabilization-v03-20261103.md" not in outline_index:
            errors.append("new chat outline entry cannot locate latest revision")
        if "2026-11-03 最新商业修仙大纲" not in skill:
            errors.append("skill does not route to latest genre manuscript contract")
        if "BLOCKER" not in first_report or "PARTIAL" not in recheck:
            errors.append("unresolved AI editor verdict lost")
        if "NO PROSE" not in latest:
            errors.append("v03 incorrectly treated as authorized chapter prose")
    if errors:
        print("FAIL\n" + "\n".join(errors))
        raise SystemExit(1)
    print("PASS: candidate structural/lineage routing; NOT writer efficacy, deployment, or human acceptance")

if __name__ == "__main__":
    main()
