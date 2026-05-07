"""Generic feature-based stratified sampling for validation tasks."""

from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def quantile_bucket(value: float, thresholds: Sequence[float]) -> int:
    """Return bucket index (0 .. len(thresholds)) for *value*.

    Args:
        value: The value to bucket.
        thresholds: Sorted boundary values. A list of N thresholds produces
            N+1 buckets: ``[..t0), [t0..t1), ..., [tN..)``.

    Returns:
        Integer bucket index.
    """
    for i, t in enumerate(thresholds):
        if value < t:
            return i
    return len(thresholds)


def compute_tertile_thresholds(values: Sequence[float]) -> list[float]:
    """Compute tertile boundaries from a list of values.

    Args:
        values: Non-empty sequence of numeric values.

    Returns:
        Two-element list ``[t33, t66]`` splitting *values* into thirds.
        Returns ``[]`` if fewer than 3 values.
    """
    if len(values) < 3:
        return []
    s = sorted(values)
    n = len(s)
    return [s[n // 3], s[2 * n // 3]]


def stratified_round_robin_sample(
    tasks: list[T],
    feature_fn: Callable[[T], tuple],
    limit: int | None,
    rng: random.Random,
) -> list[T]:
    """Sample tasks via round-robin across feature-tuple buckets.

    Groups *tasks* by the tuple returned by *feature_fn*, then picks one
    task from each bucket in sorted key order, cycling until *limit* is
    reached.  This guarantees broad coverage across the feature space.

    Args:
        tasks: Full pool of tasks to sample from.
        feature_fn: Extracts a hashable feature tuple from a task.
        limit: Maximum tasks to return, or *None* for all.
        rng: Seeded random generator for within-bucket shuffling.

    Returns:
        Sampled list of tasks, shuffled.
    """
    if limit is None or limit >= len(tasks):
        return list(tasks)

    # Group by feature tuple.
    buckets: dict[tuple, list[T]] = {}
    for task in tasks:
        buckets.setdefault(feature_fn(task), []).append(task)

    # Shuffle within each bucket, sort keys for determinism.
    bucket_keys = sorted(buckets, key=lambda k: tuple(str(v) for v in k))
    for k in bucket_keys:
        rng.shuffle(buckets[k])

    # Round-robin.
    picked: list[T] = []
    idx = {k: 0 for k in bucket_keys}
    while len(picked) < limit:
        added = False
        for k in bucket_keys:
            if len(picked) >= limit:
                break
            if idx[k] < len(buckets[k]):
                picked.append(buckets[k][idx[k]])
                idx[k] += 1
                added = True
        if not added:
            break

    rng.shuffle(picked)
    return picked
