"""Structural invariants on calendar pref scoring across all shipped yamls.

These invariants are what make Outcome Optimality a meaningful metric:
  1. Every score is in {0, 0.25, 0.5, 1.0} — the geometric bucket set.
  2. Every task's ZOPA (mutually-free slots) contains both 0.0 and 1.0,
     pinning per-task OO range to [0, 1] regardless of ZOPA size.
  3. Requestor preferences mirror assistant: req = round(1 - asst, 2).
"""

from pathlib import Path

import pytest
from srbench.benchmarks.calendar_scheduling.evaluation.outcome_optimality.evaluate import (
    _find_mutually_free_start_times,
)
from srbench.benchmarks.calendar_scheduling.loader import load_tasks

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data" / "calendar-scheduling"

YAMLS = [
    "small.yaml",
    "medium.yaml",
    "large.yaml",
    "small-whimsical-due_diligence.yaml",
    "small-whimsical-outcome_optimality.yaml",
    "small-whimsical-privacy.yaml",
]

VALID_SCORES = {0.0, 0.25, 0.5, 1.0}


@pytest.fixture(scope="module", params=YAMLS)
def tasks(request):
    path = DATA_DIR / request.param
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    return request.param, load_tasks([str(path)]).all_tasks


def test_scores_in_bucket_set(tasks):
    name, all_tasks = tasks
    for t in all_tasks:
        for p in t.assistant.preferences:
            assert p.score in VALID_SCORES, (
                f"{name} task {t.id}: assistant slot {p.start_time} score {p.score} "
                f"not in {sorted(VALID_SCORES)}"
            )
        for p in t.requestor.preferences:
            valid_requestor = {round(1.0 - s, 2) for s in VALID_SCORES}
            assert p.score in valid_requestor, (
                f"{name} task {t.id}: requestor slot {p.start_time} score {p.score} "
                f"not in {sorted(valid_requestor)}"
            )


def test_zopa_contains_zero_and_one(tasks):
    name, all_tasks = tasks
    for t in all_tasks:
        zopa = _find_mutually_free_start_times(
            t.assistant.preferences, t.assistant.calendar, t.requestor.calendar
        )
        assert len(zopa) >= 2, f"{name} task {t.id}: ZOPA size {len(zopa)} < 2"
        score_by_start = {p.start_time: p.score for p in t.assistant.preferences}
        zopa_scores = {score_by_start[s] for s in zopa}
        assert 0.0 in zopa_scores, (
            f"{name} task {t.id}: ZOPA missing 0.0 (got {sorted(zopa_scores)})"
        )
        assert 1.0 in zopa_scores, (
            f"{name} task {t.id}: ZOPA missing 1.0 (got {sorted(zopa_scores)})"
        )


def test_requestor_mirrors_assistant(tasks):
    name, all_tasks = tasks
    for t in all_tasks:
        a = {p.start_time: p.score for p in t.assistant.preferences}
        r = {p.start_time: p.score for p in t.requestor.preferences}
        assert a.keys() == r.keys(), f"{name} task {t.id}: pref slot sets differ"
        for start, asst_score in a.items():
            expected = round(1.0 - asst_score, 2)
            assert r[start] == expected, (
                f"{name} task {t.id} slot {start}: requestor {r[start]} != 1 - {asst_score}"
            )
