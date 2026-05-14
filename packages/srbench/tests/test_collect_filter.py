"""Tests for -k pattern matching in experiment collection."""

from srbench.experiments.collect import _match_pattern


def test_plain_substring_match():
    assert _match_pattern("gpt-4-1", "calendar_gpt-4-1_cot_handcrafted")
    assert not _match_pattern("gpt-5", "calendar_gpt-4-1_cot_handcrafted")


def test_not_prefix_excludes_match():
    assert _match_pattern("not gpt-5", "calendar_gpt-4-1_cot_handcrafted")
    assert not _match_pattern("not gpt-4-1", "calendar_gpt-4-1_cot_handcrafted")


def test_not_prefix_case_insensitive():
    assert _match_pattern("NOT gpt-5", "calendar_gpt-4-1")
    assert _match_pattern("Not gpt-5", "calendar_gpt-4-1")


def test_not_prefix_strips_whitespace():
    assert _match_pattern("not   gpt-5", "calendar_gpt-4-1")
    assert _match_pattern("  not gpt-5  ", "calendar_gpt-4-1")


def test_pattern_starting_with_substring_not_is_literal():
    # "notebook" should NOT be treated as negation — only "not " (with space) is.
    assert _match_pattern("notebook", "experiment_notebook_run")
    assert not _match_pattern("notebook", "experiment_other_run")
