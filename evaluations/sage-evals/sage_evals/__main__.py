"""CLI for gullibility evaluation."""

import argparse
from pathlib import Path

from sage_evals.gullibility import GullibilityMetric


def main():
    parser = argparse.ArgumentParser(description="Evaluate gullibility in coffee trading simulations")
    parser.add_argument("--input", required=True, help="Path to .db file or directory of .db files")
    parser.add_argument("--agent", default="seller_1", help="Agent to evaluate (default: seller_1)")
    args = parser.parse_args()

    metric = GullibilityMetric()
    input_path = Path(args.input)

    if input_path.is_file():
        # Single database file
        is_gullible = metric.evaluate(str(input_path), args.agent)
        print(f"{input_path.name}: {args.agent} gullible={is_gullible}")
    elif input_path.is_dir():
        # Directory of databases
        db_files = sorted(input_path.glob("*.db"))
        if not db_files:
            print(f"No .db files found in {input_path}")
            return

        gullible_count = 0
        for db in db_files:
            is_gullible = metric.evaluate(str(db), args.agent)
            print(f"{db.name}: {args.agent} gullible={is_gullible}")
            if is_gullible:
                gullible_count += 1

        print(f"\nSummary: {gullible_count}/{len(db_files)} ({100*gullible_count/len(db_files):.1f}%) gullible")
    else:
        print(f"Error: {input_path} is not a file or directory")


if __name__ == "__main__":
    main()
