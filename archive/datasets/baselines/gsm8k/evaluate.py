#!/usr/bin/env python3
"""
GSM-8K Evaluation - Evaluate GPT-5.1 on grade school math problems.

Usage:
    uv run python evaluate.py --sample 10
    uv run python evaluate.py --sample 50 --output results.json
"""

import argparse
import json
import os
import re
from pathlib import Path

from openai import OpenAI


def call_llm(prompt: str, schema: dict | None = None, model: str = "gpt-5.1") -> dict:
    """Call LLM with the given prompt and optional structured output schema.

    Args:
        prompt: The input prompt/question
        schema: Optional JSON schema for structured output
        model: Model identifier (default: gpt-5.1)

    Returns:
        dict: Parsed JSON response
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "reasoning_effort": "medium",
    }

    if schema:
        kwargs["response_format"] = schema

    response = client.chat.completions.create(**kwargs)
    return json.loads(response.choices[0].message.content)


def evaluate_gsm8k(sample_size=10, output_file=None):
    """Evaluate GPT-5.1 on GSM-8K test set."""

    # Load test data
    data_path = Path(__file__).parent / "test.json"
    with open(data_path) as f:
        problems = json.load(f)[:sample_size]

    # Define structured output schema
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "math_solution",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {"reasoning": {"type": "string"}, "answer": {"type": "string"}},
                "required": ["reasoning", "answer"],
                "additionalProperties": False,
            },
        },
    }

    # Evaluate
    results = []
    correct = 0

    for i, problem in enumerate(problems, 1):
        # Get ground truth
        gt_match = re.search(r"####\s*(-?\d+(?:,\d+)*(?:\.\d+)?)", problem["answer"])
        ground_truth = gt_match.group(1).replace(",", "") if gt_match else None

        # Get prediction
        prompt = f"Solve this math problem:\n\n{problem['question']}\n\nShow your reasoning and provide the final numerical answer."
        result = call_llm(prompt, schema)
        prediction = re.sub(r"[^\d.-]", "", result["answer"])

        # Check correctness
        is_correct = (
            ground_truth and prediction and abs(float(ground_truth) - float(prediction)) < 0.01
        )

        if is_correct:
            correct += 1

        results.append(
            {
                "question": problem["question"],
                "ground_truth": ground_truth,
                "prediction": prediction,
                "reasoning": result["reasoning"],
                "correct": is_correct,
            }
        )

        print(f"[{i}/{len(problems)}] {'✓' if is_correct else '✗'}")

    # Print summary
    accuracy = correct / len(problems)
    print(f"\nAccuracy: {correct}/{len(problems)} ({accuracy:.1%})")

    # Save results
    if output_file:
        with open(output_file, "w") as f:
            json.dump(
                {
                    "accuracy": accuracy,
                    "correct": correct,
                    "total": len(problems),
                    "results": results,
                },
                f,
                indent=2,
            )
        print(f"Results saved to {output_file}")

    return accuracy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate GPT-5.1 on GSM-8K")
    parser.add_argument("--sample", type=int, default=10, help="Number of problems (default: 10)")
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    args = parser.parse_args()

    evaluate_gsm8k(args.sample, args.output)
