"""Run paths management for benchmark output directories.

Provides a unified RunPaths class that all benchmarks (calendar scheduling,
marketplace, form-filling) use to manage output file paths:
    - results/eval file
    - checkpoint file
    - log files (timestamped)
    - LLM trace files (timestamped)
"""

from datetime import datetime
from pathlib import Path


def sanitize_model_name(model: str) -> str:
    """Sanitize model name for use in filenames (e.g., replace / with -).

    Args:
        model: Raw model name that may contain path separators.

    Returns:
        Sanitized model name safe for use in filenames.
    """
    return model.replace("/", "-")


class RunPaths:
    """Manages all output paths for a benchmark run.

    Creates and manages a directory structure like:
        outputs/<benchmark>/
            20260203_104037-model-a-model-b/
                results.json                     # Main results (configurable filename)
                checkpoint.json                  # Progress checkpoint (removed on success)
                run-20260203_104037.log          # Console log output
                llm-traces-20260203_104037.json  # LiteLLM traces
    """

    def __init__(self, output_dir: Path, results_filename: str = "results.json"):
        """Initialize with an output directory path.

        Args:
            output_dir: Path to the run output directory.
            results_filename: Filename for the main results file (default: "results.json").
        """
        self.output_dir = output_dir
        self._results_filename = results_filename

    @property
    def results_path(self) -> Path:
        """Path to the main results file.

        Returns:
            Path to the results JSON file within the output directory.
        """
        return self.output_dir / self._results_filename

    @property
    def checkpoint_path(self) -> Path:
        """Path to the checkpoint file.

        Returns:
            Path to checkpoint.json within the output directory.
        """
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

    def get_traces_path(self, timestamp: datetime | None = None) -> Path:
        """Get path to an LLM traces file with timestamp.

        Args:
            timestamp: Timestamp to use for the traces file. If None, uses current time.

        Returns:
            Path like llm-traces-20260203_144500.json
        """
        if timestamp is None:
            timestamp = datetime.now()
        ts_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"llm-traces-{ts_str}.json"

    def ensure_dir(self) -> None:
        """Create the output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def create_for_run(
        cls,
        base_dir: Path,
        *,
        models: list[str] | None = None,
        label: str | None = None,
        results_filename: str = "results.json",
    ) -> "RunPaths":
        """Create a new run directory with timestamp-based naming.

        Directory name format: {timestamp}-{label_or_models}

        Args:
            base_dir: Base directory for outputs (e.g., outputs/calendar_scheduling).
            models: List of model names to include in the directory name.
            label: Optional label to use instead of model names.
            results_filename: Filename for the main results file (default: "results.json").

        Returns:
            RunPaths instance for the new run directory.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if label:
            folder_name = f"{timestamp}-{label}"
        elif models:
            sanitized = "-".join(sanitize_model_name(m) for m in models)
            folder_name = f"{timestamp}-{sanitized}"
        else:
            folder_name = timestamp
        return cls(base_dir / folder_name, results_filename=results_filename)

    @classmethod
    def find_latest_in(
        cls, output_dir: Path, results_filename: str = "results.json"
    ) -> "RunPaths | None":
        """Find the most recent run directory containing a checkpoint.

        Searches for checkpoint.json files in subdirectories of output_dir
        and returns a RunPaths for the most recently modified one.

        Args:
            output_dir: Base directory to search (e.g., outputs/marketplace).
            results_filename: Filename for the main results file.

        Returns:
            RunPaths for the latest run directory, or None if no checkpoints found.
        """
        candidates = list(output_dir.glob("*/checkpoint.json"))
        if not candidates:
            return None
        latest = max(candidates, key=lambda p: p.stat().st_mtime)
        return cls(latest.parent, results_filename=results_filename)

    @classmethod
    def from_path(cls, path: Path, results_filename: str = "results.json") -> "RunPaths":
        """Load from an existing run directory or checkpoint/results path.

        Args:
            path: Path to run directory, checkpoint file, or results file.
            results_filename: Filename for the main results file.

        Returns:
            RunPaths instance for the directory.
        """
        if path.is_file():
            return cls(path.parent, results_filename=results_filename)
        return cls(path, results_filename=results_filename)
