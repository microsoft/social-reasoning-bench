import json
from pathlib import Path

from .schemas import TaskExecutionResult


def append_batch_to_json_list(path: Path, items: list[dict]):
    """Atomically append multiple items to JSON array.

    Args:
        path: Path to JSON file
        items: List of items to append
    """
    if path.exists():
        with open(path) as f:
            data = json.load(f)
    else:
        data = []

    data.extend(items)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_json_list(path: Path) -> list[dict]:
    """Load JSON array from file."""
    with open(path) as f:
        return json.load(f)


def load_prior_results(task_results_path: str | None, tasks) -> list[TaskExecutionResult]:
    """Load results from prior run from file."""

    if not task_results_path:
        raise ValueError("task_results_path is required for eval mode")

    print(f"Loading task results from: {task_results_path}")
    task_results_data = load_json_list(Path(task_results_path))

    # Reconstruct TaskExecutionResult objects
    task_map = {task.task_id: task for task in tasks}

    execution_results: list[TaskExecutionResult] = []

    for task_result_data in task_results_data:
        exec_data = task_result_data["execution"]
        task_id = task_result_data["task_id"]

        if task_id not in task_map:
            print(f"Warning: Task {task_id} not found, skipping")
            continue

        exec_result = TaskExecutionResult.model_validate({**exec_data, "task": task_map[task_id]})
        execution_results.append(exec_result)
    return execution_results
