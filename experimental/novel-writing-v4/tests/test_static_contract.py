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
    if errors:
        print("FAIL\n" + "\n".join(errors))
        raise SystemExit(1)
    print("PASS: candidate structural/lineage routing; NOT writer efficacy, deployment, or human acceptance")

if __name__ == "__main__":
    main()
