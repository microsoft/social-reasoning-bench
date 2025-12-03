"""Evaluation result types for needle-in-the-groupchat."""

from collections import defaultdict
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from ..models import NeedlePosition


class ConversationEvaluation(BaseModel):
    """Result of evaluating a single conversation."""

    conversation_id: str
    num_users: int
    max_tokens: int
    needle_position: NeedlePosition
    needle_user: str
    needle_message: str
    predicted_user: str | None = Field(default=None, description="User predicted by model")
    correct: bool = Field(description="Whether prediction was correct")
    model_response: str = Field(description="Full model response")
    error: str | None = Field(default=None, description="Error message if failed")


class DatasetEvaluation(BaseModel):
    """Aggregated evaluation results with breakdowns."""

    model: str
    total_evaluations: int
    overall_accuracy: float
    by_num_users: dict[int, float] = Field(description="Accuracy by number of users")
    by_max_tokens: dict[int, float] = Field(description="Accuracy by max tokens")
    by_position: dict[str, float] = Field(description="Accuracy by needle position")
    individual_results: list[ConversationEvaluation] = Field(description="All individual results")

    @classmethod
    def aggregate(cls, model: str, results: list[ConversationEvaluation]) -> "DatasetEvaluation":
        """Aggregate individual results into a DatasetEvaluation.

        Empty responses and other errors are excluded from accuracy calculations.

        Args:
            model: Model name that was evaluated
            results: List of individual conversation evaluations

        Returns:
            Aggregated DatasetEvaluation with breakdowns
        """
        # Filter out errors (including empty responses)
        valid_results = [r for r in results if r.error is None]

        total = len(valid_results)
        correct = sum(1 for r in valid_results if r.correct)
        overall_accuracy = correct / total if total > 0 else 0.0

        # Group by dimensions (excluding errors)
        by_num_users: dict[int, list[bool]] = defaultdict(list)
        by_max_tokens: dict[int, list[bool]] = defaultdict(list)
        by_position: dict[str, list[bool]] = defaultdict(list)

        for result in valid_results:
            by_num_users[result.num_users].append(result.correct)
            by_max_tokens[result.max_tokens].append(result.correct)
            by_position[result.needle_position.value].append(result.correct)

        # Calculate accuracies
        def calc_accuracy(values: list[bool]) -> float:
            return sum(values) / len(values) if values else 0.0

        return cls(
            model=model,
            total_evaluations=total,
            overall_accuracy=overall_accuracy,
            by_num_users={k: calc_accuracy(v) for k, v in by_num_users.items()},
            by_max_tokens={k: calc_accuracy(v) for k, v in by_max_tokens.items()},
            by_position={k: calc_accuracy(v) for k, v in by_position.items()},
            individual_results=results,
        )

    def save(self, path: str | Path) -> None:
        """Save aggregated results to YAML file.

        Args:
            path: Output file path
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict for YAML serialization
        results_dict = {
            "model": self.model,
            "total_evaluations": self.total_evaluations,
            "overall_accuracy": round(self.overall_accuracy, 4),
            "by_num_users": {k: round(v, 4) for k, v in sorted(self.by_num_users.items())},
            "by_max_tokens": {k: round(v, 4) for k, v in sorted(self.by_max_tokens.items())},
            "by_position": {k: round(v, 4) for k, v in sorted(self.by_position.items())},
            "individual_results": [
                {
                    "conversation_id": r.conversation_id,
                    "num_users": r.num_users,
                    "max_tokens": r.max_tokens,
                    "position": r.needle_position.value,
                    "needle_user": r.needle_user,
                    "predicted_user": r.predicted_user,
                    "correct": r.correct,
                    "error": r.error,
                }
                for r in self.individual_results
            ],
        }

        with open(output_path, "w") as f:
            yaml.dump(results_dict, f, default_flow_style=False, sort_keys=False)

    @classmethod
    def load(cls, path: str | Path) -> "DatasetEvaluation":
        """Load a DatasetEvaluation from a YAML file.

        Args:
            path: Path to YAML file

        Returns:
            Loaded DatasetEvaluation
        """
        with open(path) as f:
            data = yaml.safe_load(f)

        # Convert individual results back to ConversationEvaluation objects
        individual_results = []
        for r in data.get("individual_results", []):
            position_str = r.get("position", "middle")
            needle_position = NeedlePosition(position_str)

            individual_results.append(
                ConversationEvaluation(
                    conversation_id=r["conversation_id"],
                    num_users=r["num_users"],
                    max_tokens=r["max_tokens"],
                    needle_position=needle_position,
                    needle_user=r["needle_user"],
                    needle_message=r.get("needle_message", ""),
                    predicted_user=r.get("predicted_user"),
                    correct=r["correct"],
                    model_response=r.get("model_response", ""),
                    error=r.get("error"),
                )
            )

        return cls(
            model=data["model"],
            total_evaluations=data["total_evaluations"],
            overall_accuracy=data["overall_accuracy"],
            by_num_users=data.get("by_num_users", {}),
            by_max_tokens=data.get("by_max_tokens", {}),
            by_position=data.get("by_position", {}),
            individual_results=individual_results,
        )

    def print_summary(self) -> None:
        """Print a human-readable summary of results."""
        # Show error/exception counts if any were excluded
        total_attempted = len(self.individual_results)
        num_empty = sum(1 for r in self.individual_results if r.error == "empty_response")
        num_other_errors = sum(
            1 for r in self.individual_results if r.error and r.error != "empty_response"
        )
        if num_empty > 0:
            print(
                f"\nNote: {num_empty}/{total_attempted} empty responses "
                f"excluded from accuracy calculations"
            )
        if num_other_errors > 0:
            print(
                f"Note: {num_other_errors}/{total_attempted} evaluations had "
                f"errors and were excluded from accuracy calculations"
            )

        print(
            f"\nOverall Accuracy: {self.overall_accuracy:.2%} "
            f"({self.total_evaluations} valid evaluations)"
        )
        print("\nBy Number of Users:")
        for k, v in sorted(self.by_num_users.items()):
            print(f"  {k} users: {v:.2%}")
        print("\nBy Max Tokens:")
        for k, v in sorted(self.by_max_tokens.items()):
            print(f"  {k:,} tokens: {v:.2%}")
        print("\nBy Position:")
        for k, v in sorted(self.by_position.items()):
            print(f"  {k}: {v:.2%}")
