"""Tests for CLI --and group splitting and per-group arg extraction."""

from sage_benchmark.cli import _parse_k_patterns, _parse_set_overrides, _split_on_and, _strip_group_args


class TestSplitOnAnd:
    def test_no_and(self):
        argv = ["experiments/", "-k", "calendar", "--set", "model=gpt-4.1"]
        assert _split_on_and(argv) == [argv]

    def test_single_and(self):
        argv = ["experiments/", "-k", "cal", "--and", "-k", "mkt"]
        assert _split_on_and(argv) == [
            ["experiments/", "-k", "cal"],
            ["-k", "mkt"],
        ]

    def test_multiple_ands(self):
        argv = ["-k", "a", "--and", "-k", "b", "--and", "-k", "c"]
        assert _split_on_and(argv) == [
            ["-k", "a"],
            ["-k", "b"],
            ["-k", "c"],
        ]


class TestParseKPatterns:
    def test_no_k(self):
        assert _parse_k_patterns(["experiments/", "--collect"]) == []

    def test_single_k(self):
        assert _parse_k_patterns(["-k", "calendar"]) == ["calendar"]

    def test_multiple_k(self):
        assert _parse_k_patterns(["-k", "calendar", "-k", "gpt-4.1"]) == [
            "calendar",
            "gpt-4.1",
        ]

    def test_k_mixed_with_other_args(self):
        argv = ["experiments/", "-k", "cal", "--set", "model=X", "-k", "gpt"]
        assert _parse_k_patterns(argv) == ["cal", "gpt"]


class TestStripGroupArgs:
    def test_strips_k_and_set(self):
        argv = ["experiments/", "-k", "cal", "--set", "model=X", "--collect"]
        assert _strip_group_args(argv) == ["experiments/", "--collect"]

    def test_preserves_other_args(self):
        argv = ["experiments/", "--batch-size", "50", "--logger", "verbose"]
        assert _strip_group_args(argv) == argv

    def test_strips_multiple_k(self):
        argv = ["-k", "a", "-k", "b", "path/"]
        assert _strip_group_args(argv) == ["path/"]


class TestParseSetOverrides:
    def test_no_set(self):
        assert _parse_set_overrides(["-k", "calendar"]) == {}

    def test_single_set(self):
        assert _parse_set_overrides(["--set", "model=gpt-4.1"]) == {"model": "gpt-4.1"}

    def test_multiple_set(self):
        result = _parse_set_overrides(["--set", "model=gpt-4.1", "--set", "system_prompt=oo"])
        assert result == {"model": "gpt-4.1", "system_prompt": "oo"}
