#!/usr/bin/env python3
"""Dependency-free structural validation for STEP-01 card schemas."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = (
    ROOT / "schemas" / "scene_card.schema.json",
    ROOT / "schemas" / "story_card.schema.json",
)
VALID_TYPES = {"null", "boolean", "object", "array", "number", "string", "integer"}


def _resolve_local_ref(schema: dict[str, Any], reference: str) -> Any:
    if not reference.startswith("#/"):
        raise ValueError(f"只允许本地 Schema 引用: {reference}")
    current: Any = schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"无法解析 Schema 引用: {reference}")
        current = current[part]
    return current


def validate_schema(schema: dict[str, Any]) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("$schema 必须是 Draft 2020-12。")
    if schema.get("type") != "object":
        raise ValueError("Schema 根节点必须是 object。")

    def walk(node: Any, location: str) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{location}/{index}")
            return
        if not isinstance(node, dict):
            return

        if "$ref" in node:
            _resolve_local_ref(schema, node["$ref"])
        declared_type = node.get("type")
        if isinstance(declared_type, str) and declared_type not in VALID_TYPES:
            raise ValueError(f"{location}: 非法 type {declared_type}")
        if isinstance(declared_type, list):
            invalid = set(declared_type) - VALID_TYPES
            if invalid:
                raise ValueError(f"{location}: 非法 types {sorted(invalid)}")
        if "required" in node:
            properties = node.get("properties", {})
            missing = set(node["required"]) - set(properties)
            if missing:
                raise ValueError(f"{location}: required 未定义属性 {sorted(missing)}")
        if "pattern" in node:
            re.compile(node["pattern"])
        for key, value in node.items():
            walk(value, f"{location}/{key}")

    walk(schema, "#")


def main() -> int:
    for path in SCHEMAS:
        schema = json.loads(path.read_text(encoding="utf-8"))
        validate_schema(schema)
        print(f"PASS {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
