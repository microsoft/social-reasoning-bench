#!/usr/bin/env python3
"""
HumanEval Evaluation - Evaluate GPT-5.1 on code generation.

Usage:
    uv run python evaluate.py --sample 10
    uv run python evaluate.py --sample 50 --output results.json
"""

import argparse
import contextlib
import json
import os
import sys
from io import StringIO
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
        "reasoning_effort": "medium"
    }

    if schema:
        kwargs["response_format"] = schema

    response = client.chat.completions.create(**kwargs)
    return json.loads(response.choices[0].message.content)


def evaluate_humaneval(sample_size=10, output_file=None):
    """Evaluate GPT-5.1 on HumanEval test set."""

    # Load test data
    data_path = Path(__file__).parent / "test.json"
    with open(data_path) as f:
        problems = json.load(f)[:sample_size]

    # Define structured output schema
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "code_solution",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"}
                },
                "required": ["code"],
                "additionalProperties": False
            }
        }
    }

    # Evaluate
    results = []
    correct = 0

    for i, problem in enumerate(problems, 1):
        # Get prediction
        prompt = f"Complete this Python function. Include all necessary imports and the complete function:\n\n{problem['prompt']}\n\nReturn the complete, runnable code."
        result = call_llm(prompt, schema)
        generated_code = result["code"]

        # Test the code
        is_correct, error_msg = test_code(problem, generated_code)

        if is_correct:
            correct += 1

        results.append({
            "task_id": problem["task_id"],
            "prompt": problem["prompt"],
            "generated_code": generated_code,
            "correct": is_correct,
            "error": error_msg if not is_correct else None
        })

        print(f"[{i}/{len(problems)}] {'✓' if is_correct else '✗'}")

    # Print summary
    accuracy = correct / len(problems)
    print(f"\nAccuracy: {correct}/{len(problems)} ({accuracy:.1%})")

    # Save results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump({
                "accuracy": accuracy,
                "correct": correct,
                "total": len(problems),
                "results": results
            }, f, indent=2)
        print(f"Results saved to {output_file}")

    return accuracy


def test_code(problem, generated_code):
    """Test generated code against test cases."""
    try:
        # Create test program
        test_program = f"{generated_code}\n\n{problem['test']}\n\ncheck({problem['entry_point']})"

        # Execute in isolated namespace
        namespace = {}
        exec(test_program, namespace)

        return True, None
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate GPT-5.1 on HumanEval")
    parser.add_argument("--sample", type=int, default=10, help="Number of problems (default: 10)")
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    args = parser.parse_args()

    evaluate_humaneval(args.sample, args.output)
