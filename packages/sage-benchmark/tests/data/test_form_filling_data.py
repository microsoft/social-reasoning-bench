from pathlib import Path

import pytest
from sage_benchmark.benchmarks.form_filling.loader import load_tasks
from sage_benchmark.benchmarks.form_filling.types import FormTask

# Path to data directory relative to project root
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "form-filling"


def get_yaml_files() -> list[Path]:
    """Get all task YAML files in the form-filling data directory.

    Returns:
        Sorted list of Paths to ``*.yaml`` files, or an empty list if the
        data directory does not exist.
    """
    if not DATA_DIR.exists():
        return []
    return sorted(DATA_DIR.glob("*.yaml"))


@pytest.mark.parametrize("yaml_file", get_yaml_files(), ids=lambda p: p.name)
def test_form_filling_data_loads(yaml_file: Path) -> None:
    """Test that each form-filling YAML file can be loaded.

    Args:
        yaml_file: Path to the YAML task file provided by parametrize.
    """
    loaded = load_tasks([yaml_file])
    tasks = loaded.all_tasks
    assert len(tasks) > 0

    for task in tasks:
        assert isinstance(task, FormTask)
        assert task.id is not None
        assert task.form_info.title is not None
        assert task.persona is not None
        assert task.artifacts is not None
        assert len(task.artifacts) > 0
        assert task.secrets is not None
        assert task.ground_truth is not None
        assert len(task.ground_truth) > 0
        assert task.validation is not None
