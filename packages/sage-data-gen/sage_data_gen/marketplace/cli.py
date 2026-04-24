import argparse
import asyncio
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv
from sage_benchmark.benchmarks.marketplace.types import MarketplaceTask
from sage_llm import SageModelClient

from .assemble import assemble_tasks
from .config import MarketplacePipelineConfig
from .generate_catalog import generate_catalog
from .generate_reservation_contexts import generate_reservation_contexts
from .stats import compute_stats
from .validate import validate_tasks


def _outputs_dir(config: MarketplacePipelineConfig) -> Path:
    return Path(config.output_dir) / "_pipeline_outputs"


def _save_step(outputs_dir: Path, step: int, name: str, data: dict | list) -> None:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    path = outputs_dir / f"{step}_{name}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _write_tasks_yaml(tasks: list[MarketplaceTask], path: Path) -> None:
    payload = {"tasks": [task.model_dump(mode="json") for task in tasks]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(payload, f, sort_keys=False, allow_unicode=True)


def _remove_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def _subset(tasks: list[MarketplaceTask], n: int) -> list[MarketplaceTask]:
    if n >= len(tasks):
        return list(tasks)
    return list(sorted(tasks, key=lambda t: t.id)[:n])


async def run_pipeline(
    config: MarketplacePipelineConfig,
) -> None:
    output_dir = Path(config.output_dir)
    debug_dir = _outputs_dir(config)
    client = SageModelClient()

    print("Step 1: Generating catalog...")
    catalog = await generate_catalog(
        client=client,
        model=config.catalog_model,
        catalog_size=config.catalog_size,
        max_retries=config.max_retries_per_item,
    )
    _save_step(debug_dir, 1, "catalog", {"catalog": [c.model_dump() for c in catalog]})

    print("Step 2: Generating reservation contexts...")
    contexts = await generate_reservation_contexts(
        client=client,
        model=config.context_model,
        catalog=catalog,
        total_tasks=config.total_tasks,
        max_retries=config.max_retries_per_item,
        max_concurrency=config.max_concurrency,
        seed=config.random_seed,
    )
    _save_step(
        debug_dir, 2, "reservation_contexts", {"contexts": [c.model_dump() for c in contexts]}
    )

    print("Step 3: Assembling tasks...")
    tasks = assemble_tasks(catalog=catalog, contexts=contexts, max_rounds=config.max_rounds)

    _save_step(
        debug_dir,
        3,
        "assembled_tasks_preview",
        {"tasks_preview": [t.model_dump(mode="json") for t in tasks[:10]]},
    )

    print("Step 4: Validating tasks...")
    validation = validate_tasks(tasks=tasks)
    _save_step(debug_dir, 4, "validation_report", validation)
    if not validation["validation"]["passed"]:
        errors = validation["validation"]["errors"]
        print(f"  Warning: {len(errors)} validation error(s), filtering invalid tasks:")
        for err in errors:
            print(f"    - {err}")
        bad_ids = {int(m.group(1)) for e in errors if (m := re.search(r"Task (\d+):", e))}
        tasks = [t for t in tasks if t.id not in bad_ids]
        print(f"  Continuing with {len(tasks)} valid tasks.")

    print("Step 5: Computing stats...")
    stats = compute_stats(tasks)
    _save_step(debug_dir, 5, "stats", stats)

    print(f"Step 6: Writing {output_dir / 'large.yaml'} ({len(tasks)} tasks)...")
    _write_tasks_yaml(tasks, output_dir / "large.yaml")

    small_tasks = _subset(tasks, config.small_size)
    print(f"Step 7: Writing {output_dir / 'small.yaml'} ({len(small_tasks)} tasks)...")
    _write_tasks_yaml(small_tasks, output_dir / "small.yaml")

    # Keep marketplace outputs as small+large only.
    _remove_if_exists(output_dir / "medium.yaml")

    print(f"Done. Output: {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sagegen marketplace",
        description="Generate marketplace benchmark task datasets.",
    )
    parser.add_argument("--output-dir", default="data/marketplace")
    parser.add_argument("--total-tasks", type=int, default=280)
    parser.add_argument("--small-size", type=int, default=21)
    parser.add_argument("--max-rounds", type=int, default=6)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--catalog-size", type=int, default=24)
    parser.add_argument("--catalog-model", required=True, help="Model for catalog generation")
    parser.add_argument("--context-model", required=True, help="Model for context generation")
    parser.add_argument("--max-retries-per-item", type=int, default=3)
    parser.add_argument("--max-concurrency", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    config = MarketplacePipelineConfig(
        output_dir=args.output_dir,
        total_tasks=args.total_tasks,
        small_size=args.small_size,
        max_rounds=args.max_rounds,
        random_seed=args.seed,
        catalog_size=args.catalog_size,
        catalog_model=args.catalog_model,
        context_model=args.context_model,
        max_retries_per_item=args.max_retries_per_item,
        max_concurrency=args.max_concurrency,
    )
    asyncio.run(run_pipeline(config))
