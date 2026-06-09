import logging
from pathlib import Path

import yaml
from finding1 import main as finding1
from finding3 import main as finding3
from finding4 import main as finding4
from finding5 import main as finding5
from utils import loader

logger = logging.getLogger()


def _load_task_ids(path: Path) -> set[int]:
    return {task["id"] for task in yaml.safe_load(path.read_text())["tasks"]}


def _apply_subset_filter() -> None:
    """Restrict every run's task pool to the small-calendar / medium-marketplace
    subsets that the Qwen3-4B run was evaluated on, for an apples-to-apples
    comparison against the larger baseline runs."""
    data_dir = Path(__file__).resolve().parents[3] / "data"
    loader.TASK_ID_ALLOWLIST = {
        "calendar": _load_task_ids(data_dir / "calendar-scheduling" / "small.yaml"),
        "marketplace": _load_task_ids(data_dir / "marketplace" / "medium.yaml"),
    }
    logger.info(
        "task-id subset filter active: calendar=%d, marketplace=%d",
        len(loader.TASK_ID_ALLOWLIST["calendar"]),
        len(loader.TASK_ID_ALLOWLIST["marketplace"]),
    )


if __name__ == "__main__":
    _apply_subset_filter()
    for i, finding in enumerate([finding1, finding3, finding4, finding5]):
        try:
            finding()
        except Exception:
            logger.exception(f"Failed to plot finding {finding.__name__}")
