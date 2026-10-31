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
