"""Tests for experiment collection with --and group semantics.

Verifies that:
- Within a group, -k patterns are AND'd
- Across --and groups, results are OR'd (unioned)
- --set overrides apply per-group
- Deduplication works across groups
"""

import pytest

from sage_benchmark.experiments.collect import _matches_patterns, collect_all


# ---------------------------------------------------------------------------
# Helpers: create a minimal experiment file on disk
# ---------------------------------------------------------------------------


def _write_experiment_file(tmp_path, configs: dict[str, dict]):
    """Write a synthetic experiment.py that yields named configs.

    Args:
        tmp_path: pytest tmp_path fixture
        configs: mapping of variant_name -> config field overrides
    """
    lines = [
        "from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig",
        "",
        "def experiment():",
    ]
    for name, fields in configs.items():
        field_str = ", ".join(f'{k}="{v}"' if isinstance(v, str) else f"{k}={v}" for k, v in fields.items())
        lines.append(f'    yield CalendarRunConfig(variant="{name}", {field_str})')

    exp_file = tmp_path / "experiment.py"
    exp_file.write_text("\n".join(lines))
    return exp_file


def _make_distinct_configs() -> dict[str, dict]:
    """Generate 6 configs with distinct _config_key values.

    Uses model + system_prompt + max_rounds to ensure uniqueness after
    variant/output_dir are excluded from the key.
    """
    return {
        "calendar_gpt-4.1_normal": {"model": "gpt-4.1", "system_prompt": "none", "max_rounds": 10},
        "calendar_gpt-4.1_privacy": {"model": "gpt-4.1", "system_prompt": "privacy", "max_rounds": 10},
        "calendar_gpt-5.4_normal": {"model": "gpt-5.4", "system_prompt": "none", "max_rounds": 10},
        "calendar_gpt-5.4_privacy": {"model": "gpt-5.4", "system_prompt": "privacy", "max_rounds": 10},
        "marketplace_gpt-4.1_normal": {"model": "gpt-4.1", "system_prompt": "none", "max_rounds": 20},
        "marketplace_gpt-5.4_normal": {"model": "gpt-5.4", "system_prompt": "none", "max_rounds": 20},
    }


# ---------------------------------------------------------------------------
# Tests: _matches_patterns
# ---------------------------------------------------------------------------


class TestMatchesPatterns:
    def test_empty_patterns_matches_everything(self):
        assert _matches_patterns("calendar_gpt-4.1_normal", [])

    def test_single_pattern_match(self):
        assert _matches_patterns("calendar_gpt-4.1_normal", ["calendar"])

    def test_single_pattern_no_match(self):
        assert not _matches_patterns("calendar_gpt-4.1_normal", ["marketplace"])

    def test_multiple_patterns_all_match(self):
        assert _matches_patterns("calendar_gpt-4.1_normal", ["calendar", "gpt-4.1"])

    def test_multiple_patterns_partial_match_fails(self):
        # AND logic: all must match
        assert not _matches_patterns("calendar_gpt-4.1_normal", ["calendar", "gpt-5.4"])


# ---------------------------------------------------------------------------
# Tests: collect_all with pattern_groups
# ---------------------------------------------------------------------------


@pytest.fixture
def experiment_dir(tmp_path):
    """Create a directory with a synthetic experiment file with 6 distinct configs."""
    _write_experiment_file(tmp_path, _make_distinct_configs())
    return tmp_path


class TestCollectAllPatternGroups:
    def test_no_patterns_returns_all(self, experiment_dir):
        """No filtering returns everything."""
        results = collect_all(experiment_dir)
        names = {name for _, name, _ in results}
        assert len(names) == 6

    def test_single_group_single_pattern(self, experiment_dir):
        """Single group with one pattern filters correctly."""
        results = collect_all(experiment_dir, pattern_groups=[["calendar"]])
        names = {name for _, name, _ in results}
        assert all("calendar" in n for n in names)
        assert len(names) == 4

    def test_single_group_and_logic(self, experiment_dir):
        """Multiple patterns in one group are AND'd."""
        results = collect_all(experiment_dir, pattern_groups=[["calendar", "gpt-4.1"]])
        names = {name for _, name, _ in results}
        assert all("calendar" in n and "gpt-4.1" in n for n in names)
        assert len(names) == 2

    def test_multiple_groups_or_logic(self, experiment_dir):
        """Multiple groups are OR'd (unioned)."""
        # Group 1: calendar AND gpt-4.1 -> 2 results
        # Group 2: marketplace AND gpt-5.4 -> 1 result
        # Union: 3 results
        results = collect_all(
            experiment_dir,
            pattern_groups=[["calendar", "gpt-4.1"], ["marketplace", "gpt-5.4"]],
        )
        names = {name for _, name, _ in results}
        assert len(names) == 3
        assert "calendar_gpt-4.1_normal" in names
        assert "calendar_gpt-4.1_privacy" in names
        assert "marketplace_gpt-5.4_normal" in names

    def test_groups_deduplicate(self, experiment_dir):
        """Overlapping groups don't produce duplicates."""
        # Both groups match calendar_gpt-4.1_normal
        results = collect_all(
            experiment_dir,
            pattern_groups=[["calendar", "gpt-4.1"], ["gpt-4.1", "normal"]],
        )
        names = [name for _, name, _ in results]
        # Should have no duplicates
        assert len(names) == len(set(names))

    def test_empty_pattern_group_matches_all(self, experiment_dir):
        """An empty pattern list in a group matches everything."""
        results = collect_all(experiment_dir, pattern_groups=[[]])
        names = {name for _, name, _ in results}
        assert len(names) == 6

    def test_mixed_empty_and_filtered_groups(self, experiment_dir):
        """An empty group + a filtered group unions to everything."""
        results = collect_all(
            experiment_dir,
            pattern_groups=[["calendar", "gpt-4.1"], []],
        )
        names = {name for _, name, _ in results}
        # Empty group matches all 6, so union is 6
        assert len(names) == 6


# ---------------------------------------------------------------------------
# Tests: collect_all with per-group overrides
# ---------------------------------------------------------------------------


class TestCollectAllOverrideGroups:
    def test_per_group_overrides_applied(self, experiment_dir):
        """Each group's --set overrides are applied to that group's matches."""
        results = collect_all(
            experiment_dir,
            pattern_groups=[["gpt-4.1"], ["gpt-5.4"]],
            override_groups=[
                {"system_prompt": "privacy"},
                {"system_prompt": "oo"},
            ],
        )
        # Each group's configs get their respective override
        for _, name, config in results:
            if "gpt-4.1" in name:
                assert config.system_prompt == "privacy"
            elif "gpt-5.4" in name:
                assert config.system_prompt == "oo"
