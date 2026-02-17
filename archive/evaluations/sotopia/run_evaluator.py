#!/usr/bin/env python
"""Simple test script for Sotopia evaluator."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv
from sotopia_evals import SotopiaEvaluator, get_client
from sotopia_evals.data import extract_evaluation_data


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Sotopia evaluator on episodes")
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="evaluations/sotopia/test_data/test_episodes.jsonl",
        help="Path to input JSONL file with episodes (default: evaluations/sotopia/test_data/test_episodes.jsonl)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="evaluations/sotopia/test_data/test_episodes_scores.jsonl",
        help="Path to output JSONL file for scores (default: evaluations/sotopia/test_data/test_episodes_scores.jsonl)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gpt-4.1",
        help="Model to use for evaluation (default: gpt-4.1)",
    )
    args = parser.parse_args()

    load_dotenv()

    client = get_client(args.model)
    evaluator = SotopiaEvaluator(client)

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_results = []

    with open(input_path, "r") as f:
        for line_num, line in enumerate(f, 1):
            episode_data = json.loads(line)
            episode_id = episode_data.get("episode_id", f"episode_{line_num}")

            print(f"\{'=' * 80}")
            print(f"Evaluating Episode {line_num}: {episode_id}")
            print(f"{'=' * 80}\n")

            # Extract evaluation data from the episode
            eval_data = extract_evaluation_data(episode_data)

            # Run evaluation
            result = evaluator.evaluate(**eval_data)

            # Print results with scales
            for agent_num in [1, 2]:
                agent_eval = getattr(result, f"agent_{agent_num}_evaluation")
                agent_name = eval_data[f"agent_{agent_num}_name"]

                if agent_num == 2:
                    print()
                print(f"Agent {agent_num}: {agent_name}")
                print("-" * 40)
                print(f"Believability [0, 10]: {agent_eval.believability.score}")
                print(f"Relationship [-5, 5]: {agent_eval.relationship.score}")
                print(f"Knowledge [0, 10]: {agent_eval.knowledge.score}")
                print(f"Secret [-10, 0]: {agent_eval.secret.score}")
                print(f"Social Rules [-10, 0]: {agent_eval.social_rules.score}")
                print(
                    f"Financial Benefits [-5, 5]: {agent_eval.financial_and_material_benefits.score}"
                )
                print(f"Goal Achievement [0, 10]: {agent_eval.goal.score}")

            # Store result for output file
            result_dict = {
                "episode_id": episode_id,
                "evaluator_model": args.model,
                "agent_1_name": eval_data["agent_1_name"],
                "agent_2_name": eval_data["agent_2_name"],
                "agent_1_evaluation": result.agent_1_evaluation.model_dump(),
                "agent_2_evaluation": result.agent_2_evaluation.model_dump(),
            }
            all_results.append(result_dict)

    # Write results to output file
    with open(output_path, "w") as f:
        for result in all_results:
            f.write(json.dumps(result) + "\n")

    print(f"\n{'=' * 80}")
    print(f"Evaluation complete!")
    print(f"Processed {len(all_results)} episodes")
    print(f"Results saved to: {output_path}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
