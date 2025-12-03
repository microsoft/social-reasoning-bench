#!/usr/bin/env python3
"""
Batch process Wikipedia YAML files to generate strategies in parallel.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from generate_strategies import generate_strategies


def process_file(yaml_file: Path, output_dir: Path, overwrite: bool = False, provider: str = "gemini"):
    """Process a single YAML file."""
    try:
        result = generate_strategies(yaml_file, output_dir, overwrite=overwrite, provider=provider)
        if result:
            return f"✓ {yaml_file.name}"
        else:
            return f"⊘ {yaml_file.name} (skipped)"
    except Exception as e:
        return f"✗ {yaml_file.name}: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate strategies from all Wikipedia YAML files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_generate.py pages/ strategies/ --workers 10
  python batch_generate.py pages/ strategies/ --workers 5 --overwrite
  python batch_generate.py pages/ strategies/ --workers 10 --provider openai
        """
    )
    parser.add_argument("pages_dir", type=Path, help="Directory containing Wikipedia YAML files")
    parser.add_argument("output_dir", type=Path, help="Output directory for strategies")
    parser.add_argument("--workers", type=int, default=10,
                       help="Number of parallel workers (default: 10)")
    parser.add_argument("--overwrite", action="store_true",
                       help="Overwrite existing strategy files")
    parser.add_argument("--provider", type=str, default="gemini",
                       choices=["gemini", "openai", "trapi"],
                       help="LLM provider to use (default: gemini)")

    args = parser.parse_args()

    # Find all YAML files
    yaml_files = list(args.pages_dir.glob("*.yaml"))
    print(f"Found {len(yaml_files)} YAML files in {args.pages_dir}")
    print(f"Using {args.workers} parallel workers")
    print(f"LLM provider: {args.provider}")
    print(f"Output directory: {args.output_dir}")
    print("-" * 80)

    # Process files in parallel
    completed = 0
    failed = 0
    skipped = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_file, yaml_file, args.output_dir, args.overwrite, args.provider): yaml_file
            for yaml_file in yaml_files
        }

        # Process results as they complete
        for future in as_completed(futures):
            result = future.result()
            print(result)

            if result.startswith("✓"):
                completed += 1
            elif result.startswith("⊘"):
                skipped += 1
            else:
                failed += 1

    # Summary
    print("-" * 80)
    print("Summary:")
    print(f"  Completed: {completed}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(yaml_files)}")


if __name__ == "__main__":
    main()
