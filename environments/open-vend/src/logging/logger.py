"""Logging infrastructure for OpenVend simulations."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.simulation.state import GameState


class SimulationLogger:
    """Manages logging and state persistence for simulation runs."""

    def __init__(self, output_dir: Path | str | None = None):
        """Initialize the logger.

        Args:
            output_dir: Output directory path. If None, creates timestamped dir.
        """
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = Path(".open_vend_outputs") / f"run_{timestamp}"
        else:
            self.output_dir = Path(output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # File paths
        self.state_file = self.output_dir / "state.json"
        self.messages_file = self.output_dir / "messages.jsonl"
        self.tool_calls_file = self.output_dir / "tool_calls.jsonl"
        self.daily_summary_file = self.output_dir / "daily_summaries.jsonl"
        self.run_info_file = self.output_dir / "run_info.json"

        self._message_count = 0
        self._tool_call_count = 0

    def log_run_start(
        self,
        provider: str,
        model: str,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Log the start of a simulation run.

        Args:
            provider: LLM provider name
            model: Model name
            config: Additional configuration
        """
        run_info = {
            "start_time": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "config": config or {},
            "output_dir": str(self.output_dir),
        }
        with open(self.run_info_file, "w") as f:
            json.dump(run_info, f, indent=2)

    def log_run_end(
        self,
        state: GameState,
        reason: str,
        token_usage: dict[str, int] | None = None,
    ) -> None:
        """Log the end of a simulation run.

        Args:
            state: Final game state
            reason: Reason for ending (completed, bankrupt, max_messages, error)
            token_usage: Optional token usage statistics
        """
        # Update run info
        if self.run_info_file.exists():
            with open(self.run_info_file) as f:
                run_info = json.load(f)
        else:
            run_info = {}

        run_info["end_time"] = datetime.now().isoformat()
        run_info["end_reason"] = reason
        run_info["final_day"] = state.current_day
        run_info["final_net_worth"] = state.calculate_net_worth()
        run_info["total_messages"] = state.total_messages
        run_info["token_usage"] = token_usage

        with open(self.run_info_file, "w") as f:
            json.dump(run_info, f, indent=2)

        # Save final state
        self.save_state(state)

    def save_state(self, state: GameState) -> None:
        """Save current game state.

        Args:
            state: Current game state
        """
        state.save(self.state_file)

    def load_state(self) -> GameState | None:
        """Load game state if it exists.

        Returns:
            GameState or None if not found
        """
        from src.simulation.state import GameState

        if self.state_file.exists():
            return GameState.load(self.state_file)
        return None

    def log_message(
        self,
        role: str,
        content: str | None,
        tool_calls: list[dict[str, Any]] | None = None,
        day: int = 0,
    ) -> None:
        """Log a conversation message.

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            tool_calls: Optional tool calls
            day: Current simulation day
        """
        self._message_count += 1
        entry = {
            "message_id": self._message_count,
            "timestamp": datetime.now().isoformat(),
            "day": day,
            "role": role,
            "content": content,
            "tool_calls": tool_calls,
        }
        with open(self.messages_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_tool_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: str,
        day: int = 0,
    ) -> None:
        """Log a tool call and its result.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            result: Tool result
            day: Current simulation day
        """
        self._tool_call_count += 1
        entry = {
            "call_id": self._tool_call_count,
            "timestamp": datetime.now().isoformat(),
            "day": day,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
        }
        with open(self.tool_calls_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_daily_summary(self, summary: dict[str, Any]) -> None:
        """Log a daily summary.

        Args:
            summary: Daily summary data
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            **summary,
        }
        with open(self.daily_summary_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_run_summary(self) -> dict[str, Any]:
        """Get a summary of the current run.

        Returns:
            Run summary dictionary
        """
        summary = {
            "output_dir": str(self.output_dir),
            "messages_logged": self._message_count,
            "tool_calls_logged": self._tool_call_count,
        }

        if self.run_info_file.exists():
            with open(self.run_info_file) as f:
                summary["run_info"] = json.load(f)

        return summary


def load_existing_run(output_dir: str | Path) -> tuple[SimulationLogger, GameState | None]:
    """Load an existing simulation run.

    Args:
        output_dir: Path to the run's output directory

    Returns:
        Tuple of (logger, state) where state may be None if not found
    """
    logger = SimulationLogger(output_dir)
    state = logger.load_state()
    return logger, state
