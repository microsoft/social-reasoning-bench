"""Tests for the @safe_serializer decorator."""

import json

import pytest
from pydantic import BaseModel
from sage_benchmark.benchmarks.base.types import safe_serializer


@safe_serializer
class SimpleModel(BaseModel):
    name: str
    value: int


@safe_serializer
class NestedModel(BaseModel):
    label: str
    items: list[SimpleModel]


class CustomSerializerBase(BaseModel):
    """Model with a custom model_dump_json override."""

    data: str

    def model_dump_json(self, **kwargs) -> str:
        # Custom override that uppercases the output
        raw = self.model_dump()
        raw["data"] = raw["data"].upper()
        return json.dumps(raw, **{k: v for k, v in kwargs.items() if k in ("indent",)})


@safe_serializer
class DecoratedCustomSerializer(CustomSerializerBase):
    """Decorator should wrap the custom override, not BaseModel's."""

    pass


class TestSafeSerializerCleanInput:
    """Verify the decorator is transparent for normal (valid UTF-8) data."""

    def test_simple_model_round_trips(self):
        m = SimpleModel(name="hello", value=42)
        dumped = m.model_dump_json()
        restored = SimpleModel.model_validate_json(dumped)
        assert restored.name == "hello"
        assert restored.value == 42

    def test_nested_model_round_trips(self):
        m = NestedModel(
            label="test",
            items=[SimpleModel(name="a", value=1), SimpleModel(name="b", value=2)],
        )
        dumped = m.model_dump_json()
        restored = NestedModel.model_validate_json(dumped)
        assert len(restored.items) == 2
        assert restored.items[0].name == "a"

    def test_indent_kwarg_passed_through(self):
        m = SimpleModel(name="x", value=1)
        dumped = m.model_dump_json(indent=2)
        assert "\n" in dumped  # indented output has newlines


class TestSafeSerializerBadInput:
    """Verify the ftfy fallback kicks in for non-UTF-8 strings."""

    def test_non_utf8_is_fixed(self):
        m = SimpleModel(name="hello", value=1)
        # Surrogate characters crash Pydantic's Rust serializer — this is the
        # exact failure mode from production (non-UTF-8 LLM output).
        m.__dict__["name"] = "caf\udccce9"
        dumped = m.model_dump_json()
        parsed = json.loads(dumped)
        assert "caf" in parsed["name"]

    def test_nested_non_utf8_is_fixed(self):
        m = NestedModel(
            label="ok",
            items=[SimpleModel(name="clean", value=1)],
        )
        m.items[0].__dict__["name"] = "broken\udcccvalue"
        # Should not raise — the decorator catches the Rust serializer error
        dumped = m.model_dump_json()
        parsed = json.loads(dumped)
        # ftfy should have cleaned the string (exact replacement varies)
        assert "value" in parsed["items"][0]["name"]


class TestSafeSerializerPreservesCustomOverride:
    """Verify the decorator wraps the final class method, not BaseModel's."""

    def test_custom_override_is_called_on_clean_input(self):
        m = DecoratedCustomSerializer(data="hello")
        dumped = m.model_dump_json()
        parsed = json.loads(dumped)
        # The custom override uppercases — decorator should preserve that
        assert parsed["data"] == "HELLO"


class TestUndecorated:
    """Confirm undecorated models still crash on bad input (control group)."""

    def test_undecorated_model_raises_on_bad_bytes(self):
        class PlainModel(BaseModel):
            text: str

        m = PlainModel(text="ok")
        # Surrogate characters can't be encoded to UTF-8 and crash Pydantic's
        # Rust serializer.  This is the same failure mode as the original bug.
        m.__dict__["text"] = "bad\udcccbyte"
        with pytest.raises(Exception):
            m.model_dump_json()
