"""CLI for running meeting match judge evaluation."""

import argparse
import asyncio
import logging
import math
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field, computed_field
from pydantic_core import to_json
from sage_llm import ModelClient

from sage_benchmark.calendar_scheduling.types import Attendee, Meeting
from sage_benchmark.shared.executors import TaskPoolExecutor

from .meeting_scheduled import MeetingMatchJudge

logger = logging.getLogger(__name__)


# Test case models


class MeetingMatchTestCase(BaseModel):
    """A single meeting match test case.

    Each test case compares a requested meeting against a single candidate meeting.
    """

    id: str = Field(description="Unique identifier for the test case")
    requested: Meeting = Field(description="The meeting being requested")
    candidate: Meeting = Field(description="A single calendar meeting to compare against")
    expected_matched: bool = Field(description="Whether we expect a match")
    category: str = Field(description="Category of the test case")
    notes: str | None = Field(default=None, description="Optional explanation")


class MeetingMatchTestDataset(BaseModel):
    """Dataset of meeting match test cases."""

    test_cases: list[MeetingMatchTestCase]


class MeetingMatchTestResult(BaseModel):
    """Result of evaluating a single test case."""

    test_case_id: str
    category: str
    expected_matched: bool
    actual_matched: bool
    correct: bool
    reasoning: str


class RoundResult(BaseModel):
    """Results from a single evaluation round."""

    round_number: int
    total_cases: int
    correct: int
    accuracy: float
    results: list[MeetingMatchTestResult]


class DistributionalStats(BaseModel):
    """Distributional statistics for a metric."""

    mean: float
    std: float
    min: float
    max: float
    values: list[float] = Field(description="Individual values from each round")

    @classmethod
    def from_values(cls, values: list[float]) -> "DistributionalStats":
        """Compute stats from a list of values."""
        n = len(values)
        if n == 0:
            return cls(mean=0.0, std=0.0, min=0.0, max=0.0, values=[])

        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n if n > 0 else 0.0
        std = math.sqrt(variance)

        return cls(
            mean=mean,
            std=std,
            min=min(values),
            max=max(values),
            values=values,
        )


class CategoryStats(BaseModel):
    """Statistics for a single category."""

    category: str
    total_cases: int
    accuracy: DistributionalStats


class MeetingMatchEvalOutput(BaseModel):
    """Complete output of meeting match evaluation with multiple rounds."""

    timestamp: str
    model: str
    num_rounds: int
    total_cases_per_round: int

    # Aggregate statistics across rounds
    accuracy: DistributionalStats
    category_stats: list[CategoryStats]

    # Per-round detailed results
    rounds: list[RoundResult]

    @computed_field
    @property
    def summary(self) -> str:
        """Human-readable summary."""
        return (
            f"Accuracy: {self.accuracy.mean:.1%} +/- {self.accuracy.std:.1%} "
            f"(min={self.accuracy.min:.1%}, max={self.accuracy.max:.1%}) "
            f"over {self.num_rounds} rounds"
        )


def parse_meeting(data: dict) -> Meeting:
    """Parse a meeting from YAML data, handling attendees."""
    attendees = []
    for att in data.get("attendees", []):
        if isinstance(att, dict):
            attendees.append(Attendee(**att))
        else:
            attendees.append(att)
    return Meeting(
        uid=data["uid"],
        title=data["title"],
        description=data.get("description", ""),
        organizer=data["organizer"],
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        attendees=attendees,
    )


def load_dataset(path: Path) -> MeetingMatchTestDataset:
    """Load test cases from YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)

    test_cases = []
    for tc_data in data["test_cases"]:
        requested = parse_meeting(tc_data["requested"])
        candidate = parse_meeting(tc_data["candidate"])

        test_cases.append(
            MeetingMatchTestCase(
                id=tc_data["id"],
                requested=requested,
                candidate=candidate,
                expected_matched=tc_data["expected_matched"],
                category=tc_data["category"],
                notes=tc_data.get("notes"),
            )
        )

    return MeetingMatchTestDataset(test_cases=test_cases)


async def evaluate_test_case(
    test_case: MeetingMatchTestCase,
    judge: MeetingMatchJudge,
) -> MeetingMatchTestResult:
    """Evaluate a single test case."""
    result = await judge.evaluate(test_case.requested, test_case.candidate)

    correct = result.matched == test_case.expected_matched

    return MeetingMatchTestResult(
        test_case_id=test_case.id,
        category=test_case.category,
        expected_matched=test_case.expected_matched,
        actual_matched=result.matched,
        correct=correct,
        reasoning=result.reasoning,
    )


async def run_single_round(
    dataset: MeetingMatchTestDataset,
    judge: MeetingMatchJudge,
    round_number: int,
    batch_size: int,
) -> RoundResult:
    """Run a single evaluation round."""
    executor = TaskPoolExecutor(batch_size=batch_size, task_logger=logger)
    results = await executor.run(evaluate_test_case(tc, judge) for tc in dataset.test_cases)

    correct = sum(1 for r in results if r.correct)
    accuracy = correct / len(results) if results else 0.0

    return RoundResult(
        round_number=round_number,
        total_cases=len(results),
        correct=correct,
        accuracy=accuracy,
        results=results,
    )


def compute_category_stats(rounds: list[RoundResult]) -> list[CategoryStats]:
    """Compute per-category statistics across rounds."""
    # Gather all categories
    all_categories: set[str] = set()
    for round_result in rounds:
        for result in round_result.results:
            all_categories.add(result.category)

    category_stats = []
    for category in sorted(all_categories):
        # Compute accuracy for this category in each round
        accuracies = []
        total_cases = 0
        for round_result in rounds:
            cat_results = [r for r in round_result.results if r.category == category]
            if cat_results:
                total_cases = len(cat_results)  # Same across rounds
                cat_correct = sum(1 for r in cat_results if r.correct)
                accuracies.append(cat_correct / len(cat_results))

        category_stats.append(
            CategoryStats(
                category=category,
                total_cases=total_cases,
                accuracy=DistributionalStats.from_values(accuracies),
            )
        )

    return category_stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate meeting match judge on test dataset",
    )
    parser.add_argument(
        "dataset",
        help="Path to evaluation YAML file",
    )
    parser.add_argument(
        "--model",
        default="gpt-4.1",
        help="Model to use for evaluation (default: gpt-4.1)",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Base URL for OpenAI-compatible API",
    )
    parser.add_argument(
        "--api-version",
        default=None,
        help="API version for the model",
    )
    parser.add_argument(
        "--reasoning-effort",
        "-r",
        choices=["none", "minimal", "low", "medium", "high", "xhigh", "default"],
        default=None,
        help="Reasoning effort level (gpt-5.x, gemini)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output JSON file (default: meeting_match_eval_TIMESTAMP.json)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Number of evaluation rounds to run (default: 5)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of evaluations to run in parallel (default: 50)",
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Logging level (default: info)",
    )
    return parser.parse_args()


async def run():
    args = parse_args()

    # Configure logging
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
    )

    load_dotenv()

    # Load dataset
    dataset_path = Path(args.dataset)
    logger.info(f"Loading dataset from {dataset_path}...")
    dataset = load_dataset(dataset_path)
    logger.info(f"Loaded {len(dataset.test_cases)} test cases")

    # Create judge
    model_client = ModelClient(
        base_url=args.base_url,
        api_version=args.api_version,
        reasoning_effort=args.reasoning_effort,
    )
    judge = MeetingMatchJudge(
        model=args.model,
        model_client=model_client,
    )

    # Run multiple rounds
    rounds: list[RoundResult] = []
    for round_num in range(1, args.rounds + 1):
        logger.info(f"Running round {round_num}/{args.rounds} with {args.model}...")
        round_result = await run_single_round(
            dataset=dataset,
            judge=judge,
            round_number=round_num,
            batch_size=args.batch_size,
        )
        rounds.append(round_result)
        logger.info(f"Round {round_num} accuracy: {round_result.accuracy:.1%}")

    # Compute aggregate statistics
    accuracies = [r.accuracy for r in rounds]
    accuracy_stats = DistributionalStats.from_values(accuracies)
    category_stats = compute_category_stats(rounds)

    output = MeetingMatchEvalOutput(
        timestamp=datetime.now().isoformat(),
        model=args.model,
        num_rounds=args.rounds,
        total_cases_per_round=len(dataset.test_cases),
        accuracy=accuracy_stats,
        category_stats=category_stats,
        rounds=rounds,
    )

    # Save results
    output_path = Path(
        args.output or f"meeting_match_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(to_json(output, indent=2))
    logger.info(f"Saved results to {output_path}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("MEETING MATCH EVALUATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Model:              {args.model}")
    print(f"Rounds:             {args.rounds}")
    print(f"Cases per round:    {len(dataset.test_cases)}")
    print()
    print(
        "The meeting-match judge takes (candidate meeting, requested meeting) pairs as input and predicts true/false if the candidate meeting is the requested meeting"
    )
    print(
        "Accuracy measures if predicted meeting match (i.e. is match, vs no match) matches the expected meeting match."
    )
    print()
    print(f"Overall Accuracy:   {accuracy_stats.mean:.1%} +/- {accuracy_stats.std:.1%}")
    print(f"  Min: {accuracy_stats.min:.1%}  Max: {accuracy_stats.max:.1%}")
    print()

    # Print per-category breakdown
    print("Per-Category Accuracy:")
    for cat_stat in category_stats:
        acc = cat_stat.accuracy
        print(f"  {cat_stat.category} (n={cat_stat.total_cases}):")
        print(f"    {acc.mean:.1%} +/- {acc.std:.1%} (min={acc.min:.1%}, max={acc.max:.1%})")
    print()

    # Print per-round summary
    print("Per-Round Results:")
    for round_result in rounds:
        print(
            f"  Round {round_result.round_number}: {round_result.accuracy:.1%} ({round_result.correct}/{round_result.total_cases})"
        )
    print()

    # Collect all incorrect cases across rounds (with frequency)
    incorrect_counts: dict[str, int] = {}
    incorrect_details: dict[str, MeetingMatchTestResult] = {}
    for round_result in rounds:
        for result in round_result.results:
            if not result.correct:
                incorrect_counts[result.test_case_id] = (
                    incorrect_counts.get(result.test_case_id, 0) + 1
                )
                incorrect_details[result.test_case_id] = result  # Keep latest

    if incorrect_counts:
        print(f"{'=' * 60}")
        print(f"INCORRECT CASES (frequency across {args.rounds} rounds)")
        print(f"{'=' * 60}")
        for test_id, count in sorted(incorrect_counts.items(), key=lambda x: -x[1]):
            r = incorrect_details[test_id]
            expected = "MATCH" if r.expected_matched else "NO MATCH"
            actual = "MATCH" if r.actual_matched else "NO MATCH"
            print(f"\n  {test_id} [{r.category}] - wrong {count}/{args.rounds} times")
            print(f"    Expected: {expected}, Got: {actual}")
            print(f"    Reasoning: {r.reasoning[:100]}...")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
