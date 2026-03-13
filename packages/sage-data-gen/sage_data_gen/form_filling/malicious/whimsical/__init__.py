"""Whimsical adversarial strategy generation for form filling tasks.

Generates adversarial strategies using WhimsyGen for use by malicious
interviewer agents in the form filling benchmark. Unlike calendar scheduling,
form filling injects strategies at benchmark runtime (into the interviewer's
system prompt), not into task YAML files.
"""

import random
from pathlib import Path

import yaml
from whimsygen.core.models import Strategy

from whimsygen import WhimsyGen


class StrategyProvider:
    """Provides adversarial strategies for form filling tasks using WhimsyGen."""

    def __init__(
        self,
        *,
        model: str,
        seeds: Path | str | None = None,
        task: str | None = None,
        strategies: Path | str | None = None,
        topics: list[str] | None = None,
        chunk_size: int = 5000,
        max_chunks_per_seed: int | None = None,
        max_strategies_per_chunk: int | None = None,
        max_strategies_per_seed: int | None = None,
        prefetch_seeds: int | None = None,
        prefetch_strategies: int | None = None,
    ):
        self.model = model
        self.seeds = Path(seeds) if seeds else None
        self.task = task or ""
        self.strategies = Path(strategies) if strategies else None
        self.topics = topics
        self.chunk_size = chunk_size
        self.max_chunks_per_seed = max_chunks_per_seed
        self.max_strategies_per_chunk = max_strategies_per_chunk
        self.max_strategies_per_seed = max_strategies_per_seed
        self.prefetch_seeds = prefetch_seeds
        self.prefetch_strategies = prefetch_strategies
        self._strategies_list: list[Strategy] = []
        self._index = 0
        self._wg: WhimsyGen | None = None

    def _get_whimsygen(self) -> WhimsyGen:
        if self._wg is None:
            self._wg = WhimsyGen(model=self.model, seeds=self.seeds, task=self.task)
        return self._wg

    async def load_or_generate(self, count: int) -> list[Strategy]:
        wg = self._get_whimsygen()
        if self.strategies and self.strategies.exists():
            self._strategies_list = wg.strategies.load(self.strategies)
            if len(self._strategies_list) >= count:
                print(f"Loaded {len(self._strategies_list)} strategies from {self.strategies}")
                return self._strategies_list[:count]
            print(
                f"Cache has {len(self._strategies_list)} strategies, need {count}. Generating more..."
            )

        print(f"Generating {count} strategies using {self.model}...")
        sample_kwargs: dict = {
            "n": count,
            "topics": self.topics,
            "chunk_size": self.chunk_size,
            "max_chunks_per_seed": self.max_chunks_per_seed,
            "max_strategies_per_chunk": self.max_strategies_per_chunk,
            "max_strategies_per_seed": self.max_strategies_per_seed,
        }
        if self.prefetch_seeds is not None:
            sample_kwargs["prefetch_seeds"] = self.prefetch_seeds
        if self.prefetch_strategies is not None:
            sample_kwargs["prefetch_strategies"] = self.prefetch_strategies
        self._strategies_list = await wg.sample(**sample_kwargs)

        if self.strategies:
            self.strategies.parent.mkdir(parents=True, exist_ok=True)
            wg.strategies.save(self.strategies)
            print(f"Saved {len(self._strategies_list)} strategies to {self.strategies}")

        return self._strategies_list

    def get_next(self) -> Strategy:
        if not self._strategies_list:
            raise ValueError("No strategies loaded. Call load_or_generate() first.")
        strategy = self._strategies_list[self._index % len(self._strategies_list)]
        self._index += 1
        return strategy

    def get_random(self, rng: random.Random | None = None) -> Strategy:
        if not self._strategies_list:
            raise ValueError("No strategies loaded. Call load_or_generate() first.")
        r = rng or random
        return r.choice(self._strategies_list)

    def __len__(self) -> int:
        return len(self._strategies_list)


def save_strategies_yaml(strategies: list[Strategy], output_path: Path) -> None:
    """Save strategies to a flat YAML file consumable by the benchmark."""
    strategy_strings = [s.game_strategies for s in strategies]
    output_data = {"strategies": strategy_strings}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(
            output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
        )


def build_arg_parser(description: str):
    """Build the shared CLI argument parser for whimsical strategy generation scripts."""
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output strategies YAML file"
    )
    parser.add_argument("-m", "--model", required=True, help="Model for strategy generation")
    parser.add_argument(
        "-n", "--count", type=int, default=20, help="Number of strategies to generate"
    )
    parser.add_argument("--seeds-dir", type=Path, help="Directory containing seed YAML files")
    parser.add_argument("--topics", nargs="+")
    parser.add_argument("--seed-chunk-size", type=int, default=5000)
    parser.add_argument("--max-chunks-per-seed", type=int)
    parser.add_argument("--max-strategies-per-chunk", type=int)
    parser.add_argument("--max-strategies-per-seed", type=int)
    parser.add_argument("--prefetch-seeds", type=int)
    parser.add_argument("--prefetch-strategies", type=int)
    parser.add_argument(
        "--strategies-file", type=Path, help="Cache file for strategies (load if exists)"
    )
    return parser


async def run_strategy_generation(args, task_description: str) -> None:
    """Shared CLI runner for whimsical strategy generation scripts."""
    output_path = args.output
    strategies_file = args.strategies_file or output_path

    strategy_provider = StrategyProvider(
        model=args.model,
        seeds=args.seeds_dir,
        task=task_description,
        strategies=strategies_file,
        topics=args.topics,
        chunk_size=args.seed_chunk_size,
        max_chunks_per_seed=args.max_chunks_per_seed,
        max_strategies_per_chunk=args.max_strategies_per_chunk,
        max_strategies_per_seed=args.max_strategies_per_seed,
        prefetch_seeds=args.prefetch_seeds,
        prefetch_strategies=args.prefetch_strategies,
    )

    print(f"Generating strategies (model: {args.model})...")
    strategies = await strategy_provider.load_or_generate(args.count)

    print(f"Saving {len(strategies)} strategies to {output_path}")
    save_strategies_yaml(strategies, output_path)
    print(f"\nDone! Generated {len(strategies)} strategies -> {output_path}")
