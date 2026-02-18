"""Loader for directory-based form filling tasks."""

import json
from pathlib import Path

from .schemas import (
    ArtifactData,
    FieldCoverageInfo,
    FormTask,
    GroundTruthAnswer,
    PersonaInfo,
    SecretInfo,
)
from .utils import import_form_model_from_file


def load_single_form_task(task_dir: Path) -> FormTask:
    """Load a single form task from its directory.

    Args:
        task_dir: Path to the task directory (e.g., form_1520/)

    Returns:
        Validated FormTask object

    Directory structure expected:
        form_1520/
            task.json          # Persona, instruction, secrets
            form_model.py      # Pydantic form model
            artifacts.json     # Digital artifacts
            ground_truth.json  # Expected answers
    """
    # Load task.json
    task_json_path = task_dir / "task.json"
    if not task_json_path.exists():
        raise FileNotFoundError(f"task.json not found in {task_dir}")

    with open(task_json_path, encoding="utf-8") as f:
        task_json = json.load(f)

    # Load artifacts.json
    artifacts_json_path = task_dir / "artifacts.json"
    if not artifacts_json_path.exists():
        raise FileNotFoundError(f"artifacts.json not found in {task_dir}")

    with open(artifacts_json_path, encoding="utf-8") as f:
        artifacts_json = json.load(f)
        # Handle nested structure from JSONL
        if "artifacts" in artifacts_json:
            artifacts_list = artifacts_json["artifacts"]
        else:
            artifacts_list = artifacts_json
        artifacts = [ArtifactData(**a) for a in artifacts_list]

    # Load ground_truth.json
    gt_json_path = task_dir / "ground_truth.json"
    if not gt_json_path.exists():
        raise FileNotFoundError(f"ground_truth.json not found in {task_dir}")

    with open(gt_json_path, encoding="utf-8") as f:
        gt_json = json.load(f)
        # Handle nested structure from JSONL
        if "answers" in gt_json:
            answers_list = gt_json["answers"]
        else:
            answers_list = gt_json
        ground_truth = [GroundTruthAnswer(**a) for a in answers_list]

    # Verify form_model.py exists and import it
    form_model_path = task_dir / "form_model.py"
    if not form_model_path.exists():
        raise FileNotFoundError(f"form_model.py not found in {task_dir}")

    # Import the pydantic form class
    _, form_class = import_form_model_from_file(form_model_path)

    # Parse secrets
    secrets = [SecretInfo(**s) for s in task_json["secrets"]]
    field_coverage = [FieldCoverageInfo(**fc) for fc in task_json["field_coverage"]]

    return FormTask(
        form_id=task_json["form_id"],
        form_title=task_json["form_title"],
        instruction=task_json["instruction"],
        persona=PersonaInfo(**task_json["persona"]),
        artifacts=artifacts,
        secrets=secrets,
        ground_truth=ground_truth,
        field_coverage=field_coverage,
        form_model_path=str(form_model_path),
        form_class=form_class,
    )


def load_all_form_tasks(data_dir: str | Path) -> list[FormTask]:
    """Load all form tasks from a directory of task directories.

    Args:
        data_dir: Path to directory containing task directories
                 (e.g., sage-benchmark/data/form-filling/tasks/)

    Returns:
        List of validated FormTas objects sorted by form ID

    Expected directory structure:
        data_dir/
            form_350/
                task.json
                form_model.py
                artifacts.json
                ground_truth.json
            form_626/
                ...
            [... 60 task directories total]
    """
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_path}")

    # Get all subdirectories that start with "form_"
    task_dirs = sorted(
        [d for d in data_path.iterdir() if d.is_dir() and d.name.startswith("form_")]
    )

    if not task_dirs:
        raise ValueError(f"No task directories found in {data_path}")

    # Load each task
    tasks = []
    for task_dir in task_dirs:
        try:
            task = load_single_form_task(task_dir)
            tasks.append(task)
        except Exception as e:
            print(f"Warning: Failed to load task from {task_dir.name}: {e}")

    # Sort by form_id
    tasks.sort(key=lambda t: t.form_id)

    return tasks
