#!/usr/bin/env python3
"""CLI script to run Contextual Integrity evaluation."""

import argparse
import json
from pathlib import Path

from contextual_integrity_eval import OpenAIClient, run_evaluation
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description="Run Contextual Integrity evaluation on dataset")
    parser.add_argument(
        "--num-samples",
        type=int,
        default=5,
        help="Number of samples to evaluate (default: 5)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1",
        help="OpenAI model to use",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/dataset.json",
        help="Path to dataset.json (default: dataset.json)",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=["train", "val", "test"],
        help="Dataset split to use (default: train)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="contextual_integrity_results.json",
        help="Path to save detailed results as JSON (optional)",
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Resolve dataset path
    dataset_path = Path(args.dataset)

    print(f"Contextual Integrity Evaluation")
    print(f"=" * 50)
    print(f"Model: {args.model}")
    print(f"Dataset: {dataset_path}")
    print(f"Split: {args.split}")
    print(f"Samples: {args.num_samples}")
    print(f"=" * 50)
    print()

    # Initialize client
    client = OpenAIClient(model=args.model)

    # Run evaluation
    result = run_evaluation(
        client=client,
        dataset_path=dataset_path,
        num_samples=args.num_samples,
        split=args.split,
    )

    # Print summary
    print()
    print("=" * 50)
    print("Evaluation Summary")
    print("=" * 50)

    summary = result.get_summary()
    print(f"Total samples: {summary['total_samples']}")
    print(f"Valid responses: {summary['valid_responses']}")
    print(f"Invalid responses (missing tags): {summary['invalid_responses']}")
    print()
    print(f"Mean score: {summary['mean_score']:.3f}")
    print()
    print(f"Positive scores (> 0): {summary['positive_scores']}")
    print(f"Zero scores: {summary['zero_scores']}")
    print(f"Negative scores (< 0): {summary['negative_scores']}")
    print(f"Perfect scores (= 1.0): {summary['perfect_scores']}")
    print("=" * 50)

    # Save detailed results if requested
    if args.output:
        output_path = Path(args.output)
        output_data = {
            "summary": summary,
            "results": result.results,
            "config": {
                "model": args.model,
                "num_samples": args.num_samples,
                "split": args.split,
            },
        }

        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
