from pathlib import Path

import pytest
from sage_benchmark.form_filling.loader import load_single_form_task
from sage_benchmark.form_filling.schemas import FormTask

# Path to data directory relative to project root
TASKS_DIR = Path(__file__).parent.parent.parent / "data" / "form-filling" / "tasks"


def get_task_dirs() -> list[Path]:
    """Get all task directories in the form-filling data directory."""
    if not TASKS_DIR.exists():
        return []
    return sorted([d for d in TASKS_DIR.iterdir() if d.is_dir() and d.name.startswith("form_")])


@pytest.mark.parametrize("task_dir", get_task_dirs(), ids=lambda p: p.name)
def test_form_filling_data_loads(task_dir: Path) -> None:
    """Test that each form task directory can be loaded by the form filling loader."""
    task = load_single_form_task(task_dir)

    # Validate return type
    assert isinstance(task, FormTask)

    # Validate task has required fields
    assert task.form_id is not None
    assert task.form_title is not None
    assert task.instruction is not None
    assert task.persona is not None
    assert task.artifacts is not None
    assert len(task.artifacts) > 0
    assert task.secrets is not None
    assert task.ground_truth is not None
    assert len(task.ground_truth) > 0
    assert task.field_coverage is not None
    assert task.form_class is not None
