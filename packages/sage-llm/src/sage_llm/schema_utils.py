"""JSON schema utilities for LLM structured-output compatibility.

Most LLM APIs impose restrictions on JSON schemas that Pydantic's
``model_json_schema()`` does not satisfy out of the box.  This module
provides helpers to transform raw schemas into API-compatible forms.
"""

from __future__ import annotations

from typing import Any


def inline_refs(
    schema: dict[str, Any],
    defs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Recursively inline all ``$ref`` pointers in a JSON schema.

    Pydantic emits ``$ref`` nodes for nested models, often alongside
    sibling keywords like ``description``.  Many LLM APIs (OpenAI, Gemini)
    reject this.  This function resolves every ``$ref`` by copying the
    referenced definition inline, merging any sibling keys on top.

    The top-level ``$defs`` block is consumed during resolution and removed
    from the returned schema.

    Args:
        schema: A JSON schema dict (e.g. from ``BaseModel.model_json_schema()``).
        defs: Definitions dict.  If *None*, extracted from ``schema["$defs"]``.

    Returns:
        A new schema dict with all ``$ref`` nodes replaced by their
        definitions and ``$defs`` removed.
    """
    if defs is None:
        defs = schema.get("$defs", {})

    result = _inline_node(schema, defs)

    # Strip the top-level $defs since everything is now inlined.
    result.pop("$defs", None)
    return result


def _inline_node(
    node: dict[str, Any],
    defs: dict[str, Any],
) -> dict[str, Any]:
    """Resolve a single schema node, recursing into children.

    Args:
        node: A JSON schema node dict.
        defs: Top-level ``$defs`` definitions for resolving ``$ref`` pointers.

    Returns:
        A new schema dict with ``$ref`` nodes resolved and children inlined.
    """
    # Resolve $ref: inline the definition and merge sibling keys.
    if "$ref" in node:
        ref_name = node["$ref"].rsplit("/", 1)[-1]
        resolved = defs.get(ref_name, {})
        # Sibling keys (e.g. description) override the resolved def.
        merged = {**resolved, **{k: v for k, v in node.items() if k != "$ref"}}
        return _inline_node(merged, defs)

    result = dict(node)

    # Recurse into object properties.
    if "properties" in result and isinstance(result["properties"], dict):
        result["properties"] = {
            name: _inline_node(prop, defs)
            for name, prop in result["properties"].items()
            if isinstance(prop, dict)
        }

    # Recurse into array items.
    if "items" in result and isinstance(result["items"], dict):
        result["items"] = _inline_node(result["items"], defs)

    # Recurse into anyOf / oneOf.
    for key in ("anyOf", "oneOf"):
        if key in result and isinstance(result[key], list):
            result[key] = [_inline_node(s, defs) if isinstance(s, dict) else s for s in result[key]]

    # Remove nested $defs that may appear after inlining.
    result.pop("$defs", None)

    return result


def ensure_strict_openai_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Make a JSON schema compatible with OpenAI strict structured output.

    Applies three transformations on top of :func:`inline_refs`:

    1. Inlines all ``$ref`` nodes (via :func:`inline_refs`).
    2. Adds ``additionalProperties: false`` to every object node.
    3. Ensures ``required`` lists every property on every object node.

    Args:
        schema: A JSON schema dict (e.g. from ``BaseModel.model_json_schema()``).

    Returns:
        A cleaned schema dict ready for OpenAI's ``response_format``.
    """
    defs = schema.get("$defs", {})
    return _strict_node(schema, defs)


def _strict_node(
    node: dict[str, Any],
    defs: dict[str, Any],
) -> dict[str, Any]:
    """Resolve + strictify a single schema node, recursing into children.

    Args:
        node: A JSON schema node dict.
        defs: Top-level ``$defs`` definitions for resolving ``$ref`` pointers.

    Returns:
        A new schema dict with ``$ref`` resolved, ``additionalProperties: false``
        added, and ``required`` listing all properties on every object.
    """
    # Resolve $ref first.
    if "$ref" in node:
        ref_name = node["$ref"].rsplit("/", 1)[-1]
        resolved = defs.get(ref_name, {})
        merged = {**resolved, **{k: v for k, v in node.items() if k != "$ref"}}
        return _strict_node(merged, defs)

    result = dict(node)

    # Recurse into object properties + enforce strict constraints.
    if "properties" in result and isinstance(result["properties"], dict):
        result["properties"] = {
            name: _strict_node(prop, defs)
            for name, prop in result["properties"].items()
            if isinstance(prop, dict)
        }
        result["required"] = list(result["properties"].keys())
        result["additionalProperties"] = False

    # Recurse into array items.
    if "items" in result and isinstance(result["items"], dict):
        result["items"] = _strict_node(result["items"], defs)

    # Recurse into anyOf / oneOf.
    for key in ("anyOf", "oneOf"):
        if key in result and isinstance(result[key], list):
            result[key] = [_strict_node(s, defs) if isinstance(s, dict) else s for s in result[key]]

    # Strip $defs from output.
    result.pop("$defs", None)

    return result
