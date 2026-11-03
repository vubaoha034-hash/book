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
        if len(re.findall(r"(?m)^\| \d{2}｜", latest)) != 12:
            errors.append("v03 no longer has twelve distinct chapter state transitions")
        for token in ("第8章", "软禁", "第9章", "押运", "T-60", "不强制筑基", "双榜"):
            if token not in latest and token != "双榜":
                errors.append("v03 missing required causality marker " + token)
        if "V0.3" not in outline_index or "12-minimal-causal-stabilization-v03-20261103.md" not in outline_index:
            errors.append("new chat outline entry cannot locate latest revision")
        if "2026-11-03 最新停止门" not in skill:
            errors.append("skill does not route to latest genre manuscript contract")
        if "BLOCKER" not in first_report or "PARTIAL" not in recheck:
            errors.append("unresolved AI editor verdict lost")
        if "NO PROSE" not in latest:
            errors.append("v03 incorrectly treated as authorized chapter prose")
    # Story candidate v0.4 remains only an outline, despite a separate blind structural review.
    v04path = C / "outline-first-20261102/15-12chapter-v04-adversary-arc-20261103.md"
    v04review = C / "outline-first-20261102/16-v04-blind-review-verdict-20261103.md"
    if not v04path.is_file() or not v04review.is_file():
        errors.append("latest v04 candidate/review missing")
    else:
        v04 = v04path.read_text("utf-8")
        v04note = v04review.read_text("utf-8")
        rows = [ln for ln in v04.splitlines() if ln.startswith("| ") and len(ln) > 5 and ln[2:4].isdigit() and ln[4] == " "]
        if len(rows) != 12 or [row[2:4] for row in rows] != [f"{n:02d}" for n in range(1,13)]:
            errors.append("v04 twelve chapter order drift")
        if "NO PROSE" not in v04 and "0新正文" not in v04:
            errors.append("v04 is not a planning-only candidate")
        if "PARTIAL_BLOCKED_LONGFORM" not in v04note or "B1" not in v04note:
            errors.append("v04 blind failure wrongly promoted")
        if "V0.4" not in outline_index or "15-12chapter-v04-adversary-arc-20261103.md" not in outline_index:
            errors.append("v04 missing from latest entrypoint")
        if "2026-11-03 最新停止门" not in skill:
            errors.append("candidate skill fails latest outline-first route")
    # V0.5 was tested and rejected: do not silently reactivate free-roam chapter production.
    v05plan = C / "outline-first-20261102/17-b1-b2-hard-adversary-test-and-v05-proposal-20261103.md"
    v05reject = C / "outline-first-20261102/18-v05-independent-cold-audit-and-stop-20261103.md"
    if not v05plan.is_file() or not v05reject.is_file():
        errors.append("latest V0.5 stress test or actual rejection record missing")
    else:
        v5 = v05plan.read_text("utf-8")
        verdict = v05reject.read_text("utf-8")
        if not all(term in v5 for term in ("T-40", "闻岐", "BRANCH_CAPTURED_STOP", "NO_NEW_PROSE")):
            errors.append("V0.5 causal branch not locked")
        if not all(term in verdict for term in ("V05=BLOCKED_LONGFORM", "B01", "B02", "B03", "B04")):
            errors.append("V0.5 blocked verdict not preserved")
        if "17-b1-b2-hard-adversary-test-and-v05-proposal-20261103.md" not in outline_index:
            errors.append("V0.5 missing from cold-start outline index")
        if "18-v05-independent-cold-audit-and-stop-20261103.md" not in skill:
            errors.append("V0.5 blind verdict missing from candidate Skill")
    # User's latest scoped commercial decision: current captivity engine rejected, no literary promotion.
    captive = C / "outline-first-20261102/19-captive-survival-kill-test-20261103.md"
    if not captive.is_file():
        errors.append("missing final captive survival evidence")
    else:
        blocked = captive.read_text("utf-8")
        if "BLOCKED_NEEDS_NEW_CORE_FACT" not in blocked or "REJECT_CURRENT_FREE_ADVENTURE_AND_CAPTIVE_SURVIVAL_ENGINE" not in blocked:
            errors.append("captivity blocker or explicit stop verdict lost")
        if "19-captive-survival-kill-test-20261103.md" not in outline_index:
            errors.append("cold-start routing can revive rejected story engine")
        if "当前第一优先：已淘汰受控求生发动机" not in skill:
            errors.append("skill still presents rejected story as a writing contract")
    # C02: only one original commercial seed, with no inherited approval from prior prose.
    seed_dir = C / "commercial-new-seed-20261103"
    seed = seed_dir / "01-original-core-and-3chapter-cards.md"
    seed_audit = seed_dir / "02-internal-causal-and-commercial-audit.md"
    if not seed.is_file() or not seed_audit.is_file():
        errors.append("C02 original concept or real editor audit absent")
    else:
        concept = seed.read_text("utf-8")
        audit = seed_audit.read_text("utf-8")
        for ch in ("| 01《", "| 02《", "| 03《"):
            if ch not in concept:
                errors.append("C02 missing first-three event card " + ch)
        for fact in ("折价2枚", "额外2枚", "只剩6枚", "第三天", "二十天后正式晋峰资格", "练气四层"):
            if fact not in concept:
                errors.append("C02 core fact/clock/expense drift: " + fact)
        if "INDEPENDENT_EDITOR=NOT_RUN_TOOL_429" not in audit or "NOVEL_PROSE_WORDS=0" not in concept:
            errors.append("C02 improperly claims independent or prose acceptance")
        if "commercial-new-seed-20261103/01-original-core-and-3chapter-cards.md" not in outline_index:
            errors.append("new chat project entry misses C02 concept")
        if "当前新商业种子C02" not in skill:
            errors.append("candidate skill does not route to C02")
    if errors:
        print("FAIL\n" + "\n".join(errors))
        raise SystemExit(1)
    print("PASS: candidate structural/lineage routing; NOT writer efficacy, deployment, or human acceptance")

if __name__ == "__main__":
    main()
