"""TaskManager - Manage task definitions for strategy extraction."""

from pathlib import Path


class TaskManager:
    """Manages task definitions for WhimsyGen.

    Example:
        manager = TaskManager("task.txt")  # Load from file
        manager = TaskManager("Do something...")  # Or set as text
        print(manager.current)
    """

    def __init__(self, task: Path | str | None = None):
        """Initialize the task manager.

        Args:
            task: Task file path or task text (None for no task)
        """
        self._task: str | None = None

        # If task provided, try to load as file path first, else treat as text
        if task is not None:
            task_path = Path(task)
            try:
                if task_path.exists():
                    self.load(task_path)
                else:
                    self.set(str(task))
            except OSError:
                # Path too long or invalid - treat as task text
                self.set(str(task))

    @property
    def current(self) -> str | None:
        """Get the current task definition."""
        return self._task

    def load(self, path: Path | str) -> str:
        """Load a task from a file.

        Args:
            path: Path to task file

        Returns:
            Task content
        """
        path = Path(path)
        self._task = path.read_text().strip()
        return self._task

    def set(self, text: str) -> None:
        """Set the task from a string.

        Args:
            text: Task definition text
        """
        self._task = text.strip()

    def save(self, path: Path | str) -> Path:
        """Save the current task to a file.

        Args:
            path: Output path

        Returns:
            Path to saved file
        """
        if self._task is None:
            raise ValueError("No task to save. Call load() or set() first.")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self._task)
        return path

    def clear(self) -> None:
        """Clear the current task."""
        self._task = None
