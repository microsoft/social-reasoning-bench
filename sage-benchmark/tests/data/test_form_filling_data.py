from pathlib import Path

import pytest
from sage_benchmark.form_filling.loader import load_form_tasks
from sage_benchmark.form_filling.schemas import FormTask

# Path to data directory relative to project root
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "form-filling"


def get_yaml_files() -> list[Path]:
    """Get all YAML files in the form-filling data directory."""
    return list(DATA_DIR.glob("*.yaml"))


@pytest.mark.parametrize("yaml_file", get_yaml_files(), ids=lambda p: p.name)
def test_form_filling_data_loads(yaml_file: Path) -> None:
    """Test that each YAML file can be loaded by the form filling loader."""
    tasks = load_form_tasks(yaml_file)

    # Validate return type
    assert isinstance(tasks, list)
    assert len(tasks) > 0, f"Expected at least one task in {yaml_file.name}"

    # Validate each task is a FormTask instance
    for task in tasks:
        assert isinstance(task, FormTask)
