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
    ROOT / "schemas" / "evidence_ref.schema.json",
    ROOT / "schemas" / "library_manifest.schema.json",
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


def validate_instance(schema: dict[str, Any], instance: Any) -> None:
    """Validate the JSON-Schema subset used by the frozen V1 contracts."""

    def matches_type(value: Any, expected: str) -> bool:
        return {
            "null": value is None,
            "boolean": isinstance(value, bool),
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "string": isinstance(value, str),
        }[expected]

    def walk(node: dict[str, Any], value: Any, location: str) -> None:
        if "$ref" in node:
            walk(_resolve_local_ref(schema, node["$ref"]), value, location)
            return
        declared = node.get("type")
        if declared is not None:
            choices = [declared] if isinstance(declared, str) else declared
            if not any(matches_type(value, choice) for choice in choices):
                raise ValueError(f"{location}: type 不匹配，期望 {choices}")
        if "enum" in node and value not in node["enum"]:
            raise ValueError(f"{location}: 值不在 enum 中")
        if "const" in node and value != node["const"]:
            raise ValueError(f"{location}: 值不等于 const")
        if isinstance(value, str):
            if len(value) < node.get("minLength", 0):
                raise ValueError(f"{location}: 字符串过短")
            if "pattern" in node and not re.search(node["pattern"], value):
                raise ValueError(f"{location}: pattern 不匹配")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in node and value < node["minimum"]:
                raise ValueError(f"{location}: 小于 minimum")
            if "maximum" in node and value > node["maximum"]:
                raise ValueError(f"{location}: 大于 maximum")
        if isinstance(value, dict):
            properties = node.get("properties", {})
            missing = set(node.get("required", [])) - set(value)
            if missing:
                raise ValueError(f"{location}: 缺少字段 {sorted(missing)}")
            if node.get("additionalProperties") is False:
                extras = set(value) - set(properties)
                if extras:
                    raise ValueError(f"{location}: 未允许字段 {sorted(extras)}")
            for key, item in value.items():
                if key in properties:
                    walk(properties[key], item, f"{location}/{key}")
        if isinstance(value, list) and "items" in node:
            for index, item in enumerate(value):
                walk(node["items"], item, f"{location}/{index}")
            if node.get("uniqueItems"):
                serialized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
                if len(serialized) != len(set(serialized)):
                    raise ValueError(f"{location}: 数组元素不唯一")

    walk(schema, instance, "#")


def main() -> int:
    for path in SCHEMAS:
        schema = json.loads(path.read_text(encoding="utf-8"))
        validate_schema(schema)
        print(f"PASS {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
