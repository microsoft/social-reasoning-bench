"""Tests for sage_llm.schema_utils ref-resolution behavior."""

import pytest
from sage_llm.schema_utils import ensure_strict_openai_schema, inline_refs


class TestInlineRefs:
    def test_inlines_known_ref(self):
        schema = {
            "$defs": {"Foo": {"type": "object", "properties": {"x": {"type": "integer"}}}},
            "$ref": "#/$defs/Foo",
        }
        out = inline_refs(schema)
        assert out["type"] == "object"
        assert out["properties"]["x"]["type"] == "integer"
        assert "$defs" not in out

    def test_raises_on_missing_ref(self):
        schema: dict = {"$defs": {}, "$ref": "#/$defs/Missing"}
        with pytest.raises(KeyError, match="Missing"):
            inline_refs(schema)

    def test_raises_on_missing_ref_no_defs_block(self):
        schema: dict = {"$ref": "#/$defs/Missing"}
        with pytest.raises(KeyError, match="Missing"):
            inline_refs(schema)

    def test_raises_on_nested_missing_ref(self):
        schema = {
            "$defs": {},
            "type": "object",
            "properties": {"foo": {"$ref": "#/$defs/Gone"}},
        }
        with pytest.raises(KeyError, match="Gone"):
            inline_refs(schema)


class TestEnsureStrictOpenAISchema:
    def test_adds_required_and_additional_properties_false(self):
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }
        out = ensure_strict_openai_schema(schema)
        assert out["additionalProperties"] is False
        assert sorted(out["required"]) == ["age", "name"]

    def test_raises_on_missing_ref(self):
        schema: dict = {"$defs": {}, "$ref": "#/$defs/Missing"}
        with pytest.raises(KeyError, match="Missing"):
            ensure_strict_openai_schema(schema)
