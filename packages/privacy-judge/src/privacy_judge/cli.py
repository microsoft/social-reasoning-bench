"""CLI for Privacy Judge - unified interface for leakage and CI evaluation."""

import asyncio
import json
import random
import sys
from pathlib import Path

import click
import yaml
from sage_llm import ModelClient

from .ci import CIFlowAnalysis, CIFlowExample, CIJudge, CIVerdictExample
from .executor import TaskPoolExecutor
from .leakage import LeakageExample, LeakageJudge


def load_domain(value: str) -> str:
    """Load domain from string or file (if prefixed with @)."""
    if value.startswith("@"):
        path = Path(value[1:])
        return path.read_text().strip()
    return value


def load_yaml_file(path: str) -> dict:
    """Load a YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def resolve_batch_files(batch: str) -> list[Path]:
    """Resolve batch path to list of YAML files.

    If batch is a directory, globs for *.yaml and *.yml files.
    If batch is a file, returns it as a single-item list.
    """
    batch_path = Path(batch)
    if batch_path.is_dir():
        files = sorted(batch_path.glob("*.yaml")) + sorted(batch_path.glob("*.yml"))
        if not files:
            click.echo(f"Error: No YAML files found in {batch_path}", err=True)
            sys.exit(1)
        return files
    return [batch_path]


def write_output(output: str, output_path: str | None) -> None:
    """Write output to file or stdout."""
    if output_path:
        Path(output_path).write_text(output)
        click.echo(f"Results written to {output_path}", err=True)
    else:
        click.echo(output)


# ============================================================================
# Main CLI group
# ============================================================================


@click.group()
@click.version_option()
def cli():
    """Privacy Judge - Evaluate information disclosure.

    Two evaluation modes:

    \b
      leakage  Binary leak detection with majority voting
      ci       Contextual Integrity flow analysis (exhaustive)
    """
    pass


# ============================================================================
# Leakage subcommand
# ============================================================================


def parse_leakage_examples(data: list[dict]) -> list[LeakageExample]:
    """Parse leakage examples from YAML data."""
    return [
        LeakageExample(
            secret=ex["secret"],
            input=ex["input"],
            leaked=ex["leaked"],
            reasoning=ex["reasoning"],
            evidence=ex.get("evidence", []),
        )
        for ex in data
    ]


async def run_leakage_batch(
    batch_paths: list[Path],
    model: str,
    n_judges: int,
    concurrency: int,
    sampling: str = "sequential",
    limit: int | None = None,
    random_seed: int | None = None,
) -> list[dict]:
    """Run batch leakage evaluation across one or more YAML files."""
    all_cases = []
    all_defaults = {}

    for batch_path in batch_paths:
        batch_data = load_yaml_file(str(batch_path))
        defaults = batch_data.get("defaults", {})
        cases = batch_data.get("cases", [])

        # Merge defaults (later files override earlier)
        all_defaults.update(defaults)

        # Tag cases with their source file for relative path resolution
        for case in cases:
            case["_batch_dir"] = batch_path.parent
        all_cases.extend(cases)

    if not all_cases:
        click.echo("Error: No cases found in batch file(s)", err=True)
        sys.exit(1)

    # Apply sampling
    if sampling == "random":
        if random_seed is not None:
            random.seed(random_seed)
        random.shuffle(all_cases)

    # Apply limit after sampling
    if limit is not None:
        all_cases = all_cases[:limit]

    defaults = all_defaults
    cases = all_cases
    batch_dir = batch_paths[0].parent  # Fallback for default examples
    total_cases = len(cases)

    # Progress tracking
    progress = {"completed": 0}

    def on_complete(_result: dict) -> None:
        progress["completed"] += 1
        pct = progress["completed"] / total_cases * 100
        click.echo(
            f"\rProgress: {progress['completed']}/{total_cases} ({pct:.0f}%)",
            nl=False,
            err=True,
        )

    # Load default domain and examples
    default_domain = ""
    if defaults.get("domain"):
        default_domain = load_domain(defaults["domain"])

    default_examples = None
    if defaults.get("examples"):
        ex_path = defaults["examples"]
        if not Path(ex_path).is_absolute():
            ex_path = str(batch_dir / ex_path)
        ex_data = load_yaml_file(ex_path)
        default_examples = parse_leakage_examples(ex_data.get("examples", []))

    client = ModelClient()

    async def process_case(case: dict, case_idx: int) -> dict:
        case_id = case.get("id", f"case_{case_idx}")
        input_text = case.get("input", "")
        secret = case.get("secret", "")
        context = case.get("context")
        case_batch_dir = case.get("_batch_dir", batch_dir)

        # Use case-level domain or default
        domain = default_domain
        if "domain" in case:
            domain = load_domain(case["domain"])

        # Use case-level examples or default
        examples = default_examples
        if "examples" in case:
            ex_path = case["examples"]
            if not Path(ex_path).is_absolute():
                ex_path = str(case_batch_dir / ex_path)
            ex_data = load_yaml_file(ex_path)
            examples = parse_leakage_examples(ex_data.get("examples", []))

        judge = LeakageJudge(
            model=model,
            client=client,
            domain=domain,
            examples=examples,
            n_judges=n_judges,
        )

        try:
            judgment = await judge.aevaluate(input=input_text, secret=secret, context=context)
            return {
                "id": case_id,
                "input": input_text,
                "secret": secret,
                "judgment": judgment.model_dump(),
            }
        except Exception as e:
            return {
                "id": case_id,
                "input": input_text,
                "secret": secret,
                "error": str(e),
            }

    executor = TaskPoolExecutor(batch_size=concurrency, on_task_complete=on_complete)
    results = await executor.run(process_case(case, idx) for idx, case in enumerate(cases))
    click.echo("", err=True)  # Newline after progress

    # Compute ground truth statistics if available
    # Build lookup by case ID since results are in completion order, not original order
    case_by_id = {case.get("id", f"case_{i}"): case for i, case in enumerate(cases)}

    results_with_gt = []
    for result in results:
        case = case_by_id.get(result.get("id"))
        if case and "leaked" in case:
            result["_expected"] = case["leaked"]
            results_with_gt.append(result)

    if results_with_gt:
        tp = fp = tn = fn = 0
        for r in results_with_gt:
            predicted = r.get("judgment", {}).get("leaked", False)
            actual = r["_expected"]
            if predicted and actual:
                tp += 1
            elif predicted and not actual:
                fp += 1
            elif not predicted and not actual:
                tn += 1
            else:
                fn += 1

        total = tp + fp + tn + fn
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / total if total > 0 else 0

        click.echo("\n--- Ground Truth Statistics ---", err=True)
        click.echo(f"Total: {total} | TP: {tp} | FP: {fp} | TN: {tn} | FN: {fn}", err=True)
        click.echo(
            f"Precision: {precision:.1%} | Recall: {recall:.1%} | F1: {f1:.1%} | Accuracy: {accuracy:.1%}",
            err=True,
        )

    return results


@cli.command()
@click.option("-m", "--model", required=True, help="Model to use (e.g., gpt-4.1)")
@click.option("--domain", help="Domain context (string or @filepath)")
@click.option("--examples", help="Path to YAML file with few-shot examples")
@click.option("--secret", help="Secret information to check (required for single mode)")
@click.option("--context", help="Additional context")
@click.option("--n-judges", type=int, default=5, help="Number of parallel judges (default: 5)")
@click.option("--batch", help="Path to YAML file or directory with batch cases")
@click.option(
    "--concurrency", type=int, default=10, help="Max concurrent requests for batch (default: 10)"
)
@click.option(
    "--sampling",
    type=click.Choice(["sequential", "random"]),
    default="sequential",
    help="Case ordering: sequential or random (default: sequential)",
)
@click.option("--limit", "-n", type=int, help="Limit number of cases to evaluate")
@click.option("--random-seed", type=int, help="Random seed for reproducible sampling")
@click.option("-o", "--output", help="Output file path (default: stdout)")
@click.argument("input", required=False)
def leakage(
    model,
    domain,
    examples,
    secret,
    context,
    n_judges,
    batch,
    concurrency,
    sampling,
    limit,
    random_seed,
    output,
    input,
):
    """Detect if input leaks secret information.

    Uses majority voting across multiple parallel judges for robust evaluation.

    \b
    Examples:
      # Single evaluation
      privacy-judge leakage -m gpt-4.1 --secret "Doctor visit" "I have a medical appointment"

      # Batch evaluation
      privacy-judge leakage -m gpt-4.1 --batch cases.yaml -o results.json
    """
    if batch:
        batch_files = resolve_batch_files(batch)
        click.echo(f"Loading {len(batch_files)} batch file(s)...", err=True)
        results = asyncio.run(
            run_leakage_batch(
                batch_paths=batch_files,
                model=model,
                n_judges=n_judges,
                concurrency=concurrency,
                sampling=sampling,
                limit=limit,
                random_seed=random_seed,
            )
        )
        output_str = json.dumps(results, indent=2)
        write_output(output_str, output)
        return

    # Single mode
    if not input:
        input = sys.stdin.read()
    if not input.strip():
        click.echo("Error: No input provided", err=True)
        sys.exit(1)
    if not secret:
        click.echo("Error: --secret is required for single evaluation", err=True)
        sys.exit(1)

    # Load domain and examples
    domain_str = load_domain(domain) if domain else ""
    examples_list = None
    if examples:
        ex_data = load_yaml_file(examples)
        examples_list = parse_leakage_examples(ex_data.get("examples", []))

    client = ModelClient()
    judge = LeakageJudge(
        model=model,
        client=client,
        domain=domain_str,
        examples=examples_list,
        n_judges=n_judges,
    )

    judgment = judge.evaluate(input=input, secret=secret, context=context)
    output_str = judgment.model_dump_json(indent=2)
    write_output(output_str, output)


# ============================================================================
# CI subcommand
# ============================================================================


def parse_ci_examples(data: list[dict]) -> list[CIFlowExample | CIVerdictExample]:
    """Parse CI examples from YAML data.

    Supports two formats:
    - CIFlowExample: has 'flow' field with full flow analysis
    - CIVerdictExample: has 'verdict' field with just the verdict
    """
    examples: list[CIFlowExample | CIVerdictExample] = []
    for ex in data:
        if "flow" in ex:
            examples.append(
                CIFlowExample(
                    input=ex["input"],
                    context=ex.get("context"),
                    flow=CIFlowAnalysis(**ex["flow"]),
                )
            )
        elif "verdict" in ex:
            examples.append(
                CIVerdictExample(
                    input=ex["input"],
                    context=ex.get("context"),
                    verdict=ex["verdict"],
                )
            )
    return examples


async def run_ci_batch(
    batch_paths: list[Path],
    model: str,
    max_iterations: int,
    concurrency: int,
    reasoning_effort: str | None,
    sampling: str = "sequential",
    limit: int | None = None,
    random_seed: int | None = None,
) -> list[dict]:
    """Run batch CI evaluation across one or more YAML files."""
    all_cases = []
    all_defaults = {}

    for batch_path in batch_paths:
        batch_data = load_yaml_file(str(batch_path))
        defaults = batch_data.get("defaults", {})
        cases = batch_data.get("cases", [])

        all_defaults.update(defaults)
        for case in cases:
            case["_batch_dir"] = batch_path.parent
        all_cases.extend(cases)

    if not all_cases:
        click.echo("Error: No cases found in batch file(s)", err=True)
        sys.exit(1)

    # Apply sampling
    if sampling == "random":
        if random_seed is not None:
            random.seed(random_seed)
        random.shuffle(all_cases)

    # Apply limit after sampling
    if limit is not None:
        all_cases = all_cases[:limit]

    defaults = all_defaults
    cases = all_cases
    batch_dir = batch_paths[0].parent
    total_cases = len(cases)

    # Progress tracking
    progress = {"completed": 0}

    def on_complete(_result: dict) -> None:
        progress["completed"] += 1
        pct = progress["completed"] / total_cases * 100
        click.echo(
            f"\rProgress: {progress['completed']}/{total_cases} ({pct:.0f}%)",
            nl=False,
            err=True,
        )

    # Load default domain and examples
    default_domain = ""
    if defaults.get("domain"):
        default_domain = load_domain(defaults["domain"])

    default_examples = None
    if defaults.get("examples"):
        ex_path = defaults["examples"]
        if not Path(ex_path).is_absolute():
            ex_path = str(batch_dir / ex_path)
        ex_data = load_yaml_file(ex_path)
        default_examples = parse_ci_examples(ex_data.get("examples", []))

    client = ModelClient()

    async def process_case(case: dict, case_idx: int) -> dict:
        case_id = case.get("id", f"case_{case_idx}")
        input_text = case.get("input", "")
        context = case.get("context")
        case_batch_dir = case.get("_batch_dir", batch_dir)

        domain = default_domain
        if "domain" in case:
            domain = load_domain(case["domain"])

        examples = default_examples
        if "examples" in case:
            ex_path = case["examples"]
            if not Path(ex_path).is_absolute():
                ex_path = str(case_batch_dir / ex_path)
            ex_data = load_yaml_file(ex_path)
            examples = parse_ci_examples(ex_data.get("examples", []))

        judge = CIJudge(
            model=model,
            client=client,
            domain=domain,
            examples=examples,
            reasoning_effort=reasoning_effort,  # type: ignore[arg-type]
        )

        try:
            judgment = await judge.aevaluate(
                input=input_text,
                context=context,
                max_iterations=max_iterations,
            )
            return {
                "id": case_id,
                "input": input_text,
                "judgment": judgment.model_dump(),
            }
        except Exception as e:
            return {
                "id": case_id,
                "input": input_text,
                "error": str(e),
            }

    executor = TaskPoolExecutor(batch_size=concurrency, on_task_complete=on_complete)
    results = await executor.run(process_case(case, idx) for idx, case in enumerate(cases))
    click.echo("", err=True)  # Newline after progress

    # Compute ground truth statistics if available
    # Build lookup by case ID since results are in completion order, not original order
    case_by_id = {case.get("id", f"case_{i}"): case for i, case in enumerate(cases)}

    results_with_gt = []
    for result in results:
        case = case_by_id.get(result.get("id"))
        if case and "verdict" in case:
            result["_expected"] = case["verdict"]
            results_with_gt.append(result)

    if results_with_gt:
        # Collect predictions and labels
        predictions = []
        labels = []
        for r in results_with_gt:
            predicted = r.get("judgment", {}).get("overall_verdict")
            expected = r["_expected"]
            predictions.append(predicted)
            labels.append(expected)

        # Get all classes
        all_classes = sorted(set(labels) | set(predictions))
        total = len(results_with_gt)
        correct = sum(1 for p, l in zip(predictions, labels) if p == l)
        accuracy = correct / total if total > 0 else 0

        click.echo("\n--- Ground Truth Statistics ---", err=True)
        click.echo(f"Total: {total} | Correct: {correct} | Accuracy: {accuracy:.1%}", err=True)

        # Per-class metrics (one-vs-rest)
        click.echo("\nPer-class metrics:", err=True)
        click.echo(
            f"{'Class':<15} {'TP':>5} {'TN':>5} {'FP':>5} {'FN':>5} "
            f"{'Prec':>7} {'Recall':>7} {'F1':>7} {'Acc':>7}",
            err=True,
        )
        click.echo("-" * 70, err=True)

        for cls in all_classes:
            # One-vs-rest: cls is positive, everything else is negative
            tp = sum(1 for p, l in zip(predictions, labels) if p == cls and l == cls)
            tn = sum(1 for p, l in zip(predictions, labels) if p != cls and l != cls)
            fp = sum(1 for p, l in zip(predictions, labels) if p == cls and l != cls)
            fn = sum(1 for p, l in zip(predictions, labels) if p != cls and l == cls)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            cls_acc = (tp + tn) / total if total > 0 else 0

            click.echo(
                f"{cls:<15} {tp:>5} {tn:>5} {fp:>5} {fn:>5} "
                f"{precision:>6.1%} {recall:>6.1%} {f1:>6.1%} {cls_acc:>6.1%}",
                err=True,
            )

    return results


@cli.command()
@click.option("-m", "--model", required=True, help="Model to use (e.g., gpt-4.1)")
@click.option("--domain", help="Domain context (string or @filepath)")
@click.option("--examples", help="Path to YAML file with few-shot examples")
@click.option("--context", help="Additional context (e.g., calendar JSON)")
@click.option(
    "--max-iterations", type=int, default=50, help="Max LLM calls for flow discovery (default: 50)"
)
@click.option(
    "--reasoning-effort",
    type=click.Choice(["none", "minimal", "low", "medium", "high", "xhigh", "default"]),
    help="Reasoning effort level for supported models",
)
@click.option("--batch", help="Path to YAML file or directory with batch cases")
@click.option(
    "--concurrency", type=int, default=10, help="Max concurrent requests for batch (default: 10)"
)
@click.option(
    "--sampling",
    type=click.Choice(["sequential", "random"]),
    default="sequential",
    help="Case ordering: sequential or random (default: sequential)",
)
@click.option("--limit", "-n", type=int, help="Limit number of cases to evaluate")
@click.option("--random-seed", type=int, help="Random seed for reproducible sampling")
@click.option("-o", "--output", help="Output file path (default: stdout)")
@click.argument("input", required=False)
def ci(
    model,
    domain,
    examples,
    context,
    max_iterations,
    reasoning_effort,
    batch,
    concurrency,
    sampling,
    limit,
    random_seed,
    output,
    input,
):
    """Analyze ALL information flows using Contextual Integrity.

    Performs exhaustive iterative analysis to discover every information flow
    in the input.

    \b
    Examples:
      # Single evaluation
      privacy-judge ci -m gpt-4.1 "Alice told Bob about Charlie's salary"

      # With context
      privacy-judge ci -m gpt-4.1 --context @calendar.json "email thread..."

      # Batch evaluation
      privacy-judge ci -m gpt-4.1 --batch cases.yaml -o results.json
    """
    if batch:
        batch_files = resolve_batch_files(batch)
        click.echo(f"Loading {len(batch_files)} batch file(s)...", err=True)
        results = asyncio.run(
            run_ci_batch(
                batch_paths=batch_files,
                model=model,
                max_iterations=max_iterations,
                concurrency=concurrency,
                reasoning_effort=reasoning_effort,
                sampling=sampling,
                limit=limit,
                random_seed=random_seed,
            )
        )
        output_str = json.dumps(results, indent=2)
        write_output(output_str, output)
        return

    # Single mode
    if not input:
        input = sys.stdin.read()
    if not input.strip():
        click.echo("Error: No input provided", err=True)
        sys.exit(1)

    # Load domain and examples
    domain_str = load_domain(domain) if domain else ""
    examples_list = None
    if examples:
        ex_data = load_yaml_file(examples)
        examples_list = parse_ci_examples(ex_data.get("examples", []))

    # Load context from file if prefixed with @
    context_str = None
    if context:
        if context.startswith("@"):
            context_str = Path(context[1:]).read_text()
        else:
            context_str = context

    client = ModelClient()
    judge = CIJudge(
        model=model,
        client=client,
        domain=domain_str,
        examples=examples_list,
        reasoning_effort=reasoning_effort,  # type: ignore[arg-type]
    )

    judgment = judge.evaluate(
        input=input,
        context=context_str,
        max_iterations=max_iterations,
    )
    output_str = judgment.model_dump_json(indent=2)
    write_output(output_str, output)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
