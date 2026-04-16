"""Checkpoint persistence for resumable benchmark runs."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Generic

from pydantic import BaseModel

from .types import (
    BaseRunConfig,
    CheckpointData,
    TEvalResult,
    TExecResult,
)

logger = logging.getLogger(__name__)


class CheckpointManager(Generic[TExecResult, TEvalResult]):
    """Checkpoint manager used internally by :class:`Benchmark`.

    Receives the concrete ``CheckpointData`` Pydantic model (with resolved
    type parameters) so deserialization produces the right result types.
    """

    def __init__(
        self,
        path: Path,
        checkpoint_model: type[BaseModel],
    ) -> None:
        self.path = path
        self._checkpoint_model = checkpoint_model
        self._data: CheckpointData[TExecResult, TEvalResult] | None = None
        self._exec_keys: set[str] = set()
        self._eval_keys: set[str] = set()

    # -- persistence --

    def load(self) -> bool:
        if not self.path.exists():
            return False
        try:
            self._data = self._checkpoint_model.model_validate_json(  # type: ignore[assignment]  # ty:ignore[invalid-assignment]
                self.path.read_text()
            )
            self._exec_keys = set(self._data.completed_task_keys)  # ty:ignore[unresolved-attribute]
            self._eval_keys = set(self._data.completed_eval_keys)  # ty:ignore[unresolved-attribute]
            return True
        except Exception as exc:
            logger.warning("Stale checkpoint deleted (failed to load: %s)", exc)
            self._data = None
            self._exec_keys = set()
            self._eval_keys = set()
            self.path.unlink(missing_ok=True)
            return False

    def initialize(
        self,
        config: BaseRunConfig | None = None,
        file_hashes: dict[str, str] | None = None,
        prior_exec_results: list[TExecResult] | None = None,
        prior_eval_results: list[TEvalResult] | None = None,
    ) -> None:
        exec_results = list(prior_exec_results or [])
        eval_results = list(prior_eval_results or [])
        exec_keys = [r.task.hash for r in exec_results]
        eval_keys = [r.execution.task.hash for r in eval_results]
        self._data = CheckpointData(
            config=config,
            source_file_hashes=file_hashes or {},
            execution_results=exec_results,
            evaluation_results=eval_results,
            completed_task_keys=exec_keys,
            completed_eval_keys=eval_keys,
        )
        self._exec_keys = set(exec_keys)
        self._eval_keys = set(eval_keys)

    def save(self) -> None:
        if self._data is None:
            return
        self._data.last_updated = datetime.now().isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = self._data.model_dump_json(indent=2)
        except Exception as exc:
            logger.warning("Checkpoint serialization failed (task still succeeded): %s", exc)
            return
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(data)
        tmp.rename(self.path)

    def cleanup(self) -> None:
        if self.path.exists():
            self.path.unlink()

    # -- mutations --

    def add_execution_result(self, result: TExecResult, key: str) -> None:
        if self._data is None:
            return
        self._data.execution_results.append(result)
        self._data.completed_task_keys.append(key)
        self._exec_keys.add(key)
        self.save()

    def add_evaluation_result(self, result: TEvalResult, key: str) -> None:
        if self._data is None:
            return
        self._data.evaluation_results.append(result)
        self._data.completed_eval_keys.append(key)
        self._eval_keys.add(key)
        self.save()

    # -- reads --

    @property
    def completed_exec_keys(self) -> set[str]:
        return self._exec_keys.copy()

    @property
    def completed_eval_keys(self) -> set[str]:
        return self._eval_keys.copy()

    @property
    def execution_results(self) -> list[TExecResult]:
        if self._data is None:
            return []
        return list(self._data.execution_results)

    @property
    def evaluation_results(self) -> list[TEvalResult]:
        if self._data is None:
            return []
        return list(self._data.evaluation_results)

    @property
    def source_file_hashes(self) -> dict[str, str]:
        if self._data is None:
            return {}
        return dict(self._data.source_file_hashes)
