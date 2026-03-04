"""Loader for directory-based form filling tasks."""

import json
from pathlib import Path

from .schemas import (
    ArtifactData,
    FieldCoverageInfo,
    FieldFindabilityInfo,
    FileSystemArtifactData,
    FormTask,
    GroundTruthAnswer,
    NegativeInfoItem,
    NegativeInfoPoint,
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

    # Load ground_truth.json (data-gen format: {field_id: {answer, is_open_ended}})
    gt_json_path = task_dir / "ground_truth.json"
    if not gt_json_path.exists():
        raise FileNotFoundError(f"ground_truth.json not found in {task_dir}")

    with open(gt_json_path, encoding="utf-8") as f:
        gt_json = json.load(f)

    ground_truth = []
    for field_id, info in gt_json.items():
        ground_truth.append(
            GroundTruthAnswer(
                field_id=field_id,
                field_label=field_id.split(".")[-1].replace("_", " ").title(),
                value=info["answer"],
                is_open_ended=info.get("is_open_ended", False),
                reasoning="from ground truth",
            )
        )

    # Verify form_model.py exists and import it
    form_model_path = task_dir / "form_model.py"
    if not form_model_path.exists():
        raise FileNotFoundError(f"form_model.py not found in {task_dir}")

    # Import the pydantic form class
    _, form_class = import_form_model_from_file(form_model_path)

    # Parse secrets (flatten from question_secrets nested structure)
    secrets = []
    for qs in task_json["secrets"]["question_secrets"]:
        for s in qs["secrets"]:
            s["question_id"] = qs["question_id"]
            s["related_question"] = qs["question_text"]
            secrets.append(SecretInfo(**s))

    # Parse field coverage from validation results
    field_coverage = [FieldCoverageInfo(**fc) for fc in task_json["validation"]["field_coverage"]]

    # Load negative_info from task.json
    negative_info_items = []
    for item in task_json["negative_info"]["items"]:
        points = [NegativeInfoPoint(**p) for p in item["negative_info"]]
        negative_info_items.append(
            NegativeInfoItem(
                field_id=item["field_id"],
                field_label=item["field_label"],
                negative_info=points,
            )
        )

    # Load due_diligence_fields from task.json
    due_diligence_fields = task_json["due_diligence_fields"]

    # Load unmasked_ground_truth.json (if present, for oracle user)
    # Fall back to ground_truth.json so OracleUser always has data
    unmasked_gt_path = task_dir / "unmasked_ground_truth.json"
    if unmasked_gt_path.exists():
        with open(unmasked_gt_path, encoding="utf-8") as f:
            unmasked_ground_truth = json.load(f)
    else:
        unmasked_ground_truth = gt_json

    # Load file system artifacts (if present)
    filesystem_artifacts = []
    findability_info = []

    fs_artifacts_path = task_dir / "filesystem_artifacts.json"
    if fs_artifacts_path.exists():
        with open(fs_artifacts_path, encoding="utf-8") as f:
            fs_json = json.load(f)
        fs_list = fs_json.get("artifacts", fs_json) if isinstance(fs_json, dict) else fs_json
        filesystem_artifacts = [FileSystemArtifactData(**a) for a in fs_list]

    findability_path = task_dir / "findability.json"
    if findability_path.exists():
        with open(findability_path, encoding="utf-8") as f:
            find_json = json.load(f)
        # Build FieldFindabilityInfo list from both findable and unfindable fields
        for ff in find_json.get("findable_fields", []):
            findability_info.append(
                FieldFindabilityInfo(
                    field_id=ff["field_id"],
                    findability="findable",
                    search_terms=ff.get("suggested_search_terms", []),
                )
            )
        for uf_id in find_json.get("unfindable_field_ids", []):
            findability_info.append(
                FieldFindabilityInfo(
                    field_id=uf_id,
                    findability="unfindable",
                )
            )

    # Extract form purpose and recipient from form_summary (used for duty of care evaluation)
    form_summary = task_json.get("secrets", {}).get("form_summary", {})
    form_purpose = form_summary.get("form_purpose", "")
    form_recipient = form_summary.get("intended_recipient", "")

    return FormTask(
        form_id=task_json["form_id"],
        form_title=task_json["form_info"]["title"],
        instruction="Fill out this form for me",
        persona=PersonaInfo(**task_json["persona"]),
        artifacts=artifacts,
        secrets=secrets,
        ground_truth=ground_truth,
        field_coverage=field_coverage,
        negative_info=negative_info_items,
        due_diligence_fields=due_diligence_fields,
        unmasked_ground_truth=unmasked_ground_truth,
        form_model_path=str(form_model_path),
        form_purpose=form_purpose,
        form_recipient=form_recipient,
        form_class=form_class,
        filesystem_artifacts=filesystem_artifacts,
        findability=findability_info,
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
