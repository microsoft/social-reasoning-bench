"""Loader for interviewer tasks from YAML and form_filling formats."""

from pathlib import Path

import yaml

from .schemas import AssistantInfo, Fact, FormInfo, FormQuestion, InterviewTask
from .task import FormFillingTaskAdapter, InterviewTaskInterface, YAMLTaskAdapter


def load_tasks(yaml_path: str | Path) -> list[InterviewTask]:
    """Load interview tasks from YAML file.

    Args:
        yaml_path: Path to tasks.yaml file

    Returns:
        List of InterviewTask objects
    """
    yaml_path = Path(yaml_path)

    with open(yaml_path, encoding="utf-8") as f:
        raw_tasks = yaml.safe_load(f)

    tasks = []
    for raw_task in raw_tasks:
        # Parse facts
        facts = [Fact(**fact) for fact in raw_task["assistant"]["facts"]]

        # Parse questions
        questions = [FormQuestion(**q) for q in raw_task["form"]["questions"]]

        # Build task
        task = InterviewTask(
            id=raw_task["id"],
            assistant=AssistantInfo(persona=raw_task["assistant"]["persona"], facts=facts),
            form=FormInfo(title=raw_task["form"]["title"], questions=questions),
        )
        tasks.append(task)

    return tasks


def detect_task_format(data_path: Path) -> str:
    """Detect whether data_path is YAML or form_filling directory.

    Args:
        data_path: Path to check

    Returns:
        'yaml' or 'form_filling'

    Raises:
        ValueError: If format cannot be determined
    """
    if data_path.is_file() and data_path.suffix in [".yaml", ".yml"]:
        return "yaml"
    elif data_path.is_dir():
        # Check for form_filling structure (directories named form_XXXX)
        subdirs = [d for d in data_path.iterdir() if d.is_dir()]
        if any(d.name.startswith("form_") for d in subdirs):
            return "form_filling"

    raise ValueError(f"Cannot determine task format for: {data_path}")


def load_tasks_unified(data_path: str | Path) -> list[InterviewTaskInterface]:
    """Load tasks from either YAML or form_filling format.

    Automatically detects the format and returns appropriate adapters.

    Args:
        data_path: Path to tasks.yaml OR directory of form_filling tasks

    Returns:
        List of task adapters implementing InterviewTaskInterface

    Raises:
        ValueError: If format cannot be determined
    """
    data_path = Path(data_path)
    format_type = detect_task_format(data_path)

    if format_type == "yaml":
        # Use existing YAML loader
        raw_tasks = load_tasks(data_path)
        return [YAMLTaskAdapter(t) for t in raw_tasks]

    elif format_type == "form_filling":
        # Import and use form_filling loader
        from sage_benchmark.form_filling.loader import load_all_form_tasks

        raw_tasks = load_all_form_tasks(str(data_path))
        return [FormFillingTaskAdapter(t) for t in raw_tasks]

    else:
        raise ValueError(f"Unknown format: {format_type}")
