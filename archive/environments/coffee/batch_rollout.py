"""
Batch rollout script for running multiple simulations.

Usage:
    # Sequential (default)
    uv run python batch_rollout.py --num-runs 10

    # Parallel with 8 workers
    uv run python batch_rollout.py --num-runs 10 --workers 8

    # With custom config
    uv run python batch_rollout.py --num-runs 5 --config config/config-4.yaml --prefix exp

    # With directory of configs
    uv run python batch_rollout.py --num-runs 5 --config-dir ../data/negotiation_configs/

    # With regex pattern filter
    uv run python batch_rollout.py --num-runs 5 --config-dir ../data/negotiation_configs/ --pattern "neg2[0-5]"
"""

import argparse
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


def run_simulation(run_id, config_file, prefix, output_dir, working_dir=None):
    """Run a single simulation with a unique experiment name."""
    experiment_name = f"{prefix}_{run_id}"

    cmd = [
        sys.executable,  # python
        "main.py",
        "--config",
        config_file,
        "--experiment",
        experiment_name,
    ]

    print(f"\n{'=' * 60}")
    print(f"Running simulation {run_id}: {experiment_name}")
    print(f"{'=' * 60}")

    # Set environment variable to tell main.py where to save results
    env = os.environ.copy()
    env["RESULTS_DIR"] = str(output_dir)

    result = subprocess.run(cmd, capture_output=False, env=env, cwd=working_dir)

    if result.returncode == 0:
        print(f"✓ Simulation {run_id} completed successfully")
        return True
    else:
        print(f"✗ Simulation {run_id} failed with return code {result.returncode}")
        return False


def run_batch_rollout(config_files, num_runs, prefix, start_from=1, workers=None):
    """
    Run batch rollouts and return the output directory.

    Args:
        config_files: List of Path objects pointing to config files
        num_runs: Number of runs per config
        prefix: Prefix for experiment names
        start_from: Starting run number
        workers: Number of parallel workers (None = sequential)

    Returns:
        output_dir: Path to the directory containing all results
    """
    # Create output directory for this batch
    output_dir = Path("results") / prefix
    output_dir.mkdir(parents=True, exist_ok=True)

    # Pre-generate all (config, run_id, batch_prefix, output_dir) tuples
    task_queue = []
    for config_file in config_files:
        config_name = config_file.stem
        batch_prefix = f"{prefix}_{config_name}"
        for i in range(start_from, start_from + num_runs):
            task_queue.append((i, str(config_file), batch_prefix, output_dir))

    total_tasks = len(task_queue)

    print(f"\n{'=' * 60}")
    print("BATCH ROLLOUT")
    print(f"{'=' * 60}")
    print(f"Number of config files: {len(config_files)}")
    print(f"Runs per config: {num_runs}")
    print(f"Total simulations: {total_tasks}")
    print(f"Mode: {'Parallel (' + str(workers) + ' workers)' if workers else 'Sequential'}")
    print(f"Output directory: {output_dir}")
    print(f"{'=' * 60}\n")

    # Run simulations
    total_successful = 0
    total_failed = 0

    if workers:
        # Parallel execution across all tasks
        with ProcessPoolExecutor(max_workers=workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(
                    run_simulation, run_id, config_file, batch_prefix, output_dir, "."
                ): (run_id, config_file, batch_prefix)
                for run_id, config_file, batch_prefix, output_dir in task_queue
            }

            # Process results as they complete
            completed = 0
            for future in as_completed(futures):
                completed += 1
                run_id, config_file, batch_prefix = futures[future]
                try:
                    success = future.result()
                    if success:
                        total_successful += 1
                        print(f"[{completed}/{total_tasks}] ✓ {batch_prefix}_{run_id}")
                    else:
                        total_failed += 1
                        print(f"[{completed}/{total_tasks}] ✗ {batch_prefix}_{run_id} (failed)")
                except Exception as e:
                    total_failed += 1
                    print(f"[{completed}/{total_tasks}] ✗ {batch_prefix}_{run_id} (exception: {e})")
    else:
        # Sequential execution
        for idx, (run_id, config_file, batch_prefix, output_dir) in enumerate(task_queue, 1):
            success = run_simulation(run_id, config_file, batch_prefix, output_dir, ".")
            if success:
                total_successful += 1
                print(f"[{idx}/{total_tasks}] ✓ {batch_prefix}_{run_id}")
            else:
                total_failed += 1
                print(f"[{idx}/{total_tasks}] ✗ {batch_prefix}_{run_id} (failed)")

    # Summary
    print(f"\n{'=' * 60}")
    print("BATCH ROLLOUT SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total configs: {len(config_files)}")
    print(f"Runs per config: {num_runs}")
    print(f"Total simulations: {total_tasks}")
    print(f"Successful: {total_successful}")
    print(f"Failed: {total_failed}")
    print(f"\nResults saved in: {output_dir}")
    print(f"Database pattern: {output_dir}/marketplace_{prefix}_*.db")
    print(f"{'=' * 60}\n")

    return output_dir


def main():
    parser = argparse.ArgumentParser(description="Run multiple simulations in batch")
    parser.add_argument(
        "--num-runs", type=int, default=10, help="Number of simulations to run (default: 10)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration YAML file (default: config/config.yaml)",
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        default=None,
        help="Directory containing multiple config files to run (overrides --config)",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=None,
        help="Prefix for experiment names (default: timestamp-based)",
    )
    parser.add_argument(
        "--start-from", type=int, default=1, help="Starting run number (default: 1)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers (default: None, runs sequentially)",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default=None,
        help="Regex pattern to filter config files (e.g., 'neg22' or 'neg2[0-5]')",
    )

    args = parser.parse_args()

    # Determine config files to run
    if args.config_dir:
        config_dir = Path(args.config_dir)
        config_files = sorted(config_dir.glob("*.yaml"))

        # Apply pattern filter if provided
        if args.pattern:
            import re

            pattern = re.compile(args.pattern)
            config_files = [f for f in config_files if pattern.search(f.stem)]

        if not config_files:
            print(
                f"Error: No .yaml files found in {args.config_dir}"
                + (f" matching pattern '{args.pattern}'" if args.pattern else "")
            )
            sys.exit(1)
    else:
        config_files = [Path(args.config)]

    # Generate prefix if not provided
    if args.prefix is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_prefix = f"batch_{timestamp}"
    else:
        base_prefix = args.prefix

    # Call the main function
    run_batch_rollout(
        config_files=config_files,
        num_runs=args.num_runs,
        prefix=base_prefix,
        start_from=args.start_from,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
