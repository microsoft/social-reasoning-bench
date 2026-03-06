"""Run marketplace experiment with per-task metrics on the large dataset.

Usage:
    uv run experiments/3-2-marketplace-metrics/run_experiment.py
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

DATA_PATH = "data/marketplace/final/large.yaml"
OUTPUT_BASE = Path("outputs/marketplace/3-2-marketplace-metrics")
MAX_STEPS_PER_TURN = 3

VARIANTS = [
    {
        "name": "gpt-5.1-thinking",
        "buyer_model": "trapi/gpt-5.1",
        "seller_model": "trapi/gpt-5.1",
        "reasoning_effort": "medium",
    },
]


def _latest_results_path(output_dir: Path) -> Path:
    run_dirs = sorted(
        [p for p in output_dir.glob("run_*") if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
    )
    if not run_dirs:
        raise FileNotFoundError(f"No run_* directory found under {output_dir}")
    results = run_dirs[-1] / "results.json"
    if not results.exists():
        raise FileNotFoundError(f"Missing results.json at {results}")
    return results


def _run_one(variant: dict) -> dict:
    name = variant["name"]
    output_dir = OUTPUT_BASE / name
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "uv",
        "run",
        "--package",
        "sage-benchmark",
        "sagebench",
        "marketplace",
        "--data",
        DATA_PATH,
        "--buyer-model",
        variant["buyer_model"],
        "--seller-model",
        variant["seller_model"],
        "--max-steps-per-turn",
        str(MAX_STEPS_PER_TURN),
        "--output-dir",
        str(output_dir),
    ]
    if variant.get("reasoning_effort"):
        cmd.extend(["--reasoning-effort", str(variant["reasoning_effort"])])
    print(f"\n{'=' * 60}")
    print(f"Running variant: {name}")
    print(f"  buyer_model:      {variant['buyer_model']}")
    print(f"  seller_model:     {variant['seller_model']}")
    print(f"  reasoning_effort: {variant.get('reasoning_effort', 'none')}")
    print(f"{'=' * 60}")
    subprocess.run(cmd, check=True)

    results_path = _latest_results_path(output_dir)
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    return {
        "variant": name,
        "buyer_model": variant["buyer_model"],
        "seller_model": variant["seller_model"],
        "results_path": str(results_path),
        "summary": payload.get("summary", {}),
    }


def main() -> None:
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    runs: list[dict] = []

    for variant in VARIANTS:
        runs.append(_run_one(variant))

    summary_path = OUTPUT_BASE / "summary.json"
    summary_path.write_text(json.dumps({"runs": runs}, indent=2), encoding="utf-8")
    print(f"\nWrote summary to {summary_path}")

    for run in runs:
        s = run["summary"]
        print(f"  {run['variant']}: deal_rate={s.get('deal_rate', 0):.1%}")


if __name__ == "__main__":
    main()
