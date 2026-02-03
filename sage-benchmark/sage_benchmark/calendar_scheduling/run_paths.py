"""Run paths management for calendar scheduling benchmarks."""

from datetime import datetime
from pathlib import Path


def sanitize_model_name(model: str) -> str:
    """Sanitize model name for use in filenames (e.g., replace / with -)."""
    return model.replace("/", "-")


class RunPaths:
    """Manages all output paths for a benchmark run.

    Creates and manages a directory structure like:
        outputs/calendar_scheduling/
            20260203_104037-gpt-5.2-gpt-5.2-gpt-5.2/
                eval.json          # Main evaluation results
                checkpoint.json    # Progress checkpoint (removed on success)
                run.log            # Console log output
                traces.json        # LiteLLM traces
    """

    def __init__(self, output_dir: Path):
        """Initialize with an output directory path."""
        self.output_dir = output_dir

    @property
    def eval_path(self) -> Path:
        """Path to the main evaluation results file."""
        return self.output_dir / "eval.json"

    @property
    def checkpoint_path(self) -> Path:
        """Path to the checkpoint file."""
        return self.output_dir / "checkpoint.json"

    def get_log_path(self, timestamp: datetime | None = None) -> Path:
        """Get path to a run log file with timestamp.

        Args:
            timestamp: Timestamp to use for the log file. If None, uses current time.

        Returns:
            Path like run-20260203_144500.log
        """
        if timestamp is None:
            timestamp = datetime.now()
        ts_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"run-{ts_str}.log"

    @property
    def traces_path(self) -> Path:
        """Path to the LiteLLM traces file."""
        return self.output_dir / "traces.json"

    def ensure_dir(self) -> None:
        """Create the output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def create_for_run(
        cls,
        assistant_model: str,
        requestor_model: str,
        judge_model: str,
        base_dir: Path | None = None,
    ) -> "RunPaths":
        """Create a new run output directory with timestamp-based naming.

        Args:
            assistant_model: Model used for the assistant agent
            requestor_model: Model used for the requestor agent
            judge_model: Model used for the judge
            base_dir: Base directory for outputs (default: outputs/calendar_scheduling)

        Returns:
            RunPaths instance for the new run directory
        """
        if base_dir is None:
            base_dir = Path("outputs/calendar_scheduling")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = (
            f"{timestamp}-"
            f"{sanitize_model_name(assistant_model)}-"
            f"{sanitize_model_name(requestor_model)}-"
            f"{sanitize_model_name(judge_model)}"
        )
        return cls(base_dir / folder_name)

    @classmethod
    def from_path(cls, path: Path) -> "RunPaths":
        """Load from an existing run directory or checkpoint path.

        Args:
            path: Path to run directory, checkpoint file, or eval file

        Returns:
            RunPaths instance for the directory
        """
        if path.is_file():
            return cls(path.parent)
        return cls(path)
