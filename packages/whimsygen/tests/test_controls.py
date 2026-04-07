"""Integration tests for WhimsyGen max_* controls.

These tests use real LLM calls to verify the controls work correctly.
"""

import pytest

from whimsygen import WhimsyGen

# Test configuration
MODEL = "trapi/msraif/shared/gpt-4.1"
SEEDS_DIR = "data/seeds/"
TASK = "Test task: Generate strategies for testing AI assistants."


@pytest.fixture
def wg():
    """Create a WhimsyGen instance for testing.

    Returns:
        A ``WhimsyGen`` instance configured with test defaults.
    """
    return WhimsyGen(model=MODEL, seeds=SEEDS_DIR, task=TASK)


@pytest.mark.asyncio
async def test_sample_returns_n_strategies(wg):
    """sample(n) should return exactly n strategies.

    Args:
        wg: WhimsyGen fixture instance.
    """
    n = 2
    strategies = await wg.sample(n)
    assert len(strategies) == n


@pytest.mark.asyncio
async def test_max_strategies_limits_total(wg):
    """max_strategies should limit the total number of strategies returned.

    Args:
        wg: WhimsyGen fixture instance.
    """
    max_strategies = 2

    strategies = [s async for s in wg.isample(max_strategies=max_strategies)]

    assert len(strategies) == max_strategies


@pytest.mark.asyncio
async def test_max_seeds_limits_seeds_processed(wg):
    """max_seeds should limit how many seeds are processed.

    Args:
        wg: WhimsyGen fixture instance.
    """
    max_seeds = 1
    max_strategies = 10  # High enough to not be the limiting factor

    strategies = [s async for s in wg.isample(max_seeds=max_seeds, max_strategies=max_strategies)]

    # All strategies should come from the same seed
    seed_titles = {s.source_seed for s in strategies}
    assert len(seed_titles) == 1


@pytest.mark.asyncio
async def test_max_strategies_per_seed_limits_per_seed(wg):
    """max_strategies_per_seed should limit strategies extracted from each seed.

    Args:
        wg: WhimsyGen fixture instance.
    """
    max_strategies_per_seed = 1
    max_seeds = 3
    max_strategies = 10  # High enough to not be the limiting factor

    strategies = [
        s
        async for s in wg.isample(
            max_seeds=max_seeds,
            max_strategies_per_seed=max_strategies_per_seed,
            max_strategies=max_strategies,
        )
    ]

    # Should have at most max_strategies_per_seed from each seed
    seed_counts: dict[str, int] = {}
    for s in strategies:
        seed_counts[s.source_seed] = seed_counts.get(s.source_seed, 0) + 1

    for seed, count in seed_counts.items():
        assert count <= max_strategies_per_seed, (
            f"Seed {seed} has {count} strategies, expected <= {max_strategies_per_seed}"
        )


@pytest.mark.asyncio
async def test_max_strategies_stops_iteration_early(wg):
    """Iteration should stop as soon as max_strategies is reached.

    Args:
        wg: WhimsyGen fixture instance.
    """
    max_strategies = 1

    count = 0
    async for _ in wg.isample(max_strategies=max_strategies):
        count += 1

    assert count == max_strategies


@pytest.mark.asyncio
async def test_combined_controls(wg):
    """Multiple controls should work together correctly.

    Args:
        wg: WhimsyGen fixture instance.
    """
    max_seeds = 2
    max_strategies_per_seed = 2
    max_strategies = 3  # Less than max_seeds * max_strategies_per_seed

    strategies = [
        s
        async for s in wg.isample(
            max_seeds=max_seeds,
            max_strategies_per_seed=max_strategies_per_seed,
            max_strategies=max_strategies,
        )
    ]

    # max_strategies should be the limiting factor
    assert len(strategies) == max_strategies

    # Should have strategies from at most max_seeds seeds
    seed_titles = {s.source_seed for s in strategies}
    assert len(seed_titles) <= max_seeds


@pytest.mark.asyncio
async def test_no_limits_returns_multiple_strategies(wg):
    """Without limits, should return multiple strategies.

    Args:
        wg: WhimsyGen fixture instance.
    """
    # Use a small max to avoid long test runs
    max_strategies = 5

    strategies = [s async for s in wg.isample(max_strategies=max_strategies)]

    assert len(strategies) == max_strategies
    # Verify we got actual Strategy objects
    for s in strategies:
        assert s.game_strategies is not None
        assert len(s.game_strategies) > 0
