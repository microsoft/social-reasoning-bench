#!/usr/bin/env python3
"""
MMLU Evaluation - Evaluate GPT-5.1 on multitask language understanding.

Usage:
    uv run python evaluate.py --sample 10
    uv run python evaluate.py --sample 100 --output results.json
"""

import argparse
import json
import os
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


def evaluate_mmlu(sample_size=10, output_file=None):
    """Evaluate GPT-5.1 on MMLU test set."""

    # Load test data (using small version - 1,140 questions across 57 subjects)
    data_path = Path(__file__).parent / "data" / "mmlu_small.json"
    with open(data_path) as f:
        data = json.load(f)

    problems = data["test"][:sample_size]

    # Define structured output schema
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "multiple_choice_answer",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "reasoning": {"type": "string"},
                    "answer": {"type": "string", "enum": ["A", "B", "C", "D"]},
                },
                "required": ["reasoning", "answer"],
                "additionalProperties": False,
            },
        },
    }

    # Evaluate
    results = []
    correct = 0

    for i, problem in enumerate(problems, 1):
        # Format question with choices
        question = problem["question"]
        choices = problem["choices"]
        choices_text = "\n".join([f"{chr(65 + j)}. {choice}" for j, choice in enumerate(choices)])

        ground_truth_idx = problem["answer"]
        ground_truth = chr(65 + ground_truth_idx)  # 0->A, 1->B, etc.

        # Get prediction
        prompt = f"{question}\n\n{choices_text}\n\nWhat is the correct answer? Respond with just A, B, C, or D."
        result = call_llm(prompt, schema)
        prediction = result["answer"]

        # Check correctness
        is_correct = prediction == ground_truth

        if is_correct:
            correct += 1

        results.append(
            {
                "question": question,
                "subject": problem["subject"],
                "choices": choices,
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
    parser = argparse.ArgumentParser(description="Evaluate GPT-5.1 on MMLU")
    parser.add_argument("--sample", type=int, default=10, help="Number of problems (default: 10)")
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    args = parser.parse_args()

    evaluate_mmlu(args.sample, args.output)
