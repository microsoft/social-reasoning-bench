"""Main evaluation logic for Contextual Integrity dataset."""

import json
from pathlib import Path
from typing import Any

from contextual_integrity_eval.client import ModelClient
from contextual_integrity_eval.grader import compute_score, extract_answer
from contextual_integrity_eval.prompt import format_prompt


class EvaluationResult:
    """Container for evaluation results."""

    def __init__(self):
        self.results: list[dict[str, Any]] = []

    def add_result(
        self,
        index: int,
        prompt: str,
        response: str,
        score: float,
        dataset_item: dict[str, Any],
    ):
        """Add a single evaluation result."""
        self.results.append(
            {
                "index": index,
                "prompt": prompt,
                "response": response,
                "score": score,
                "answer_extracted": extract_answer(response) is not None,
                "user_task": dataset_item["dataset_item"]["user_task"],
                "allowed_keywords": dataset_item["dataset_item"]["annotation"]["allowed"],
                "disallowed_keywords": dataset_item["dataset_item"]["annotation"]["disallowed"],
                "num_allowed": len(dataset_item["dataset_item"]["annotation"]["allowed"]),
                "num_disallowed": len(dataset_item["dataset_item"]["annotation"]["disallowed"]),
            }
        )

    def get_summary(self) -> dict[str, Any]:
        """Compute summary statistics."""
        if not self.results:
            return {}

        scores = [r["score"] for r in self.results]
        valid_scores = [s for s in scores if s != -1.0]

        return {
            "total_samples": len(self.results),
            "valid_responses": len(valid_scores),
            "invalid_responses": len(scores) - len(valid_scores),
            "mean_score": sum(valid_scores) / len(valid_scores) if valid_scores else 0.0,
            "positive_scores": sum(1 for s in valid_scores if s > 0),
            "negative_scores": sum(1 for s in valid_scores if s < 0),
            "zero_scores": sum(1 for s in valid_scores if s == 0),
            "perfect_scores": sum(1 for s in valid_scores if s == 1.0),
        }


def load_dataset(dataset_path: str | Path, split: str = "train") -> list[dict[str, Any]]:
    """
    Load the Contextual Integrity dataset.

    Args:
        dataset_path: Path to dataset.json
        split: Which split to load ('train', 'val', or 'test')

    Returns:
        List of dataset items
    """
    with open(dataset_path, "r") as f:
        data = json.load(f)

    if split not in data:
        raise ValueError(f"Split '{split}' not found in dataset. Available: {list(data.keys())}")

    return data[split]


def run_evaluation(
    client: ModelClient,
    dataset_path: str | Path,
    num_samples: int = 5,
    split: str = "train",
) -> EvaluationResult:
    """
    Run Contextual Integrity evaluation.

    Args:
        client: ModelClient instance to use for generation
        dataset_path: Path to dataset.json
        num_samples: Number of samples to evaluate
        split: Which dataset split to use
        seed: Random seed for reproducibility

    Returns:
        EvaluationResult with all results and summary statistics
    """
    # Load dataset
    dataset = load_dataset(dataset_path, split=split)

    # Limit to num_samples
    if num_samples > 0:
        dataset = dataset[:num_samples]

    result = EvaluationResult()

    # Run evaluation
    for i, item in enumerate(dataset):
        print(f"Evaluating sample {i + 1}/{len(dataset)}...")

        # Format prompt
        prompt = format_prompt(item)

        # Get model response
        response = client.llm_completion(prompt)

        # Compute score
        score = compute_score(response, item)

        # Store result
        result.add_result(
            index=i,
            prompt=prompt,
            response=response,
            score=score,
            dataset_item=item,
        )

        print(f"  Score: {score:.3f}")

    return result
