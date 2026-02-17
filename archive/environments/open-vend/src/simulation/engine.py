"""Main simulation engine for OpenVend."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.agents.runner import get_runner
from src.logging.logger import SimulationLogger
from src.simulation.state import GameState


class SimulationEngine:
    """Main engine that runs the vending machine simulation."""

    def __init__(
        self,
        provider: str,
        model: str,
        api_key: str | None = None,
        output_dir: str | Path | None = None,
        max_days: int = 365,
        max_messages: int = 2000,
        max_consecutive_unpaid: int = 10,
    ):
        """Initialize the simulation engine.

        Args:
            provider: LLM provider ("openai", "anthropic", "gemini")
            model: Model name
            api_key: Optional API key
            output_dir: Output directory for logs
            max_days: Maximum simulation days
            max_messages: Maximum messages before termination
            max_consecutive_unpaid: Days of unpaid fees before bankruptcy
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.max_days = max_days
        self.max_messages = max_messages
        self.max_consecutive_unpaid = max_consecutive_unpaid

        # Initialize state
        self.state = GameState()

        # Initialize logger
        self.logger = SimulationLogger(output_dir)

        # Initialize runner
        self.runner = get_runner(provider, model, self.state, api_key, self.logger)

        # Track termination reason
        self.termination_reason: str | None = None

    def is_terminated(self) -> bool:
        """Check if simulation should terminate.

        Returns:
            True if simulation should end
        """
        if self.state.current_day > self.max_days:
            self.termination_reason = "completed"
            return True

        if self.state.total_messages >= self.max_messages:
            self.termination_reason = "max_messages"
            return True

        if self.state.consecutive_unpaid_days >= self.max_consecutive_unpaid:
            self.termination_reason = "bankrupt"
            return True

        return False

    def _create_daily_briefing(self) -> str:
        """Create the daily briefing message for the agent.

        Returns:
            Briefing message string
        """
        lines = [f"=== Day {self.state.current_day} Briefing ==="]
        lines.append(f"Bank Balance: ${self.state.bank_balance:.2f}")
        lines.append(f"Cash in Machine: ${self.state.machine_cash:.2f}")
        lines.append(f"Net Worth: ${self.state.calculate_net_worth():.2f}")

        # Check unread emails
        unread = [e for e in self.state.emails if not e.read]
        if unread:
            lines.append(f"\nYou have {len(unread)} unread email(s).")

        # Check warehouse
        if self.state.warehouse:
            total_items = self.state.get_warehouse_total_items()
            lines.append(f"\nWarehouse: {total_items} items in stock")

        # Check machine status
        filled_slots = sum(1 for s in self.state.machine_slots if s.quantity > 0)
        lines.append(f"Vending Machine: {filled_slots}/12 slots filled")

        # Check pending orders
        from src.simulation.state import OrderStatus

        pending = [o for o in self.state.orders if o.status == OrderStatus.PENDING]
        paid = [o for o in self.state.orders if o.status == OrderStatus.PAID]
        if pending:
            lines.append(f"\nPending orders (awaiting payment): {len(pending)}")
        if paid:
            lines.append(f"Orders in transit: {len(paid)}")

        # Progress update
        days_remaining = self.max_days - self.state.current_day + 1
        lines.append(f"\nDays remaining: {days_remaining}")

        lines.append("\nWhat would you like to do today?")

        return "\n".join(lines)

    def run_single_turn(self, verbose: bool = False) -> str:
        """Run a single turn of the simulation.

        Args:
            verbose: Enable verbose logging

        Returns:
            Agent's response
        """
        # Create briefing for new day or continuation
        briefing = self._create_daily_briefing()

        if verbose:
            print("\nUser message to agent:")
            print(f"{briefing[:200]}..." if len(briefing) > 200 else f"{briefing}")

        # Run agent turn
        response = self.runner.run_turn(briefing, verbose=verbose)

        # Update message count
        self.state.total_messages += 1

        if verbose:
            print("\nAgent response:")
            print(f"{response[:200]}..." if len(response) > 200 else f"   {response}")
            print("\nState after turn:")
            print(f"Day: {self.state.current_day}")
            print(f"Balance: ${self.state.bank_balance:.2f}")
            print(f"Machine cash: ${self.state.machine_cash:.2f}")
            print(f"Warehouse items: {self.state.get_warehouse_total_items()}")
            print(f"Tool calls today: {self.state.tool_calls_today}")
        # Log the interaction
        self.logger.log_message(
            role="user",
            content=briefing,
            day=self.state.current_day,
        )
        self.logger.log_message(
            role="assistant",
            content=response,
            day=self.state.current_day,
        )

        # Save state
        self.logger.save_state(self.state)

        return response

    def run(self, verbose: bool = True) -> dict[str, Any]:
        """Run the full simulation.

        Args:
            verbose: Whether to print progress

        Returns:
            Final results dictionary
        """
        # Log run start
        self.logger.log_run_start(
            provider=self.provider,
            model=self.model,
            config={
                "max_days": self.max_days,
                "max_messages": self.max_messages,
                "max_consecutive_unpaid": self.max_consecutive_unpaid,
            },
        )

        if verbose:
            print(f"Starting simulation: {self.logger.output_dir}")
            print(f"Provider: {self.provider}, Model: {self.model}")
            print(f"Max days: {self.max_days}, Max messages: {self.max_messages}")
            print("=" * 50)

        try:
            while not self.is_terminated():
                if verbose:
                    print(f"\n{'=' * 60}")
                    print(f"DAY {self.state.current_day} - MESSAGE {self.state.total_messages + 1}")
                    print(f"{'=' * 60}")

                self.run_single_turn(verbose=verbose)

                # Save after each turn
                self.logger.save_state(self.state)

        except KeyboardInterrupt:
            self.termination_reason = "interrupted"
            if verbose:
                print("\nSimulation interrupted by user.")

        except Exception as e:
            self.termination_reason = f"error: {str(e)}"
            if verbose:
                print(f"\nSimulation error: {e}")
            raise

        finally:
            # Log run end
            self.logger.log_run_end(
                state=self.state,
                reason=self.termination_reason or "unknown",
                token_usage=self.runner.get_token_usage(),
            )

        # Prepare results
        results = {
            "termination_reason": self.termination_reason,
            "final_day": self.state.current_day,
            "final_net_worth": self.state.calculate_net_worth(),
            "final_bank_balance": self.state.bank_balance,
            "final_machine_cash": self.state.machine_cash,
            "total_messages": self.state.total_messages,
            "token_usage": self.runner.get_token_usage(),
            "output_dir": str(self.logger.output_dir),
        }

        if verbose:
            print("\n" + "=" * 50)
            print("SIMULATION COMPLETE")
            print(f"Reason: {self.termination_reason}")
            print(f"Final Day: {self.state.current_day}")
            print(f"Final Net Worth: ${self.state.calculate_net_worth():.2f}")
            print(f"Output: {self.logger.output_dir}")

        return results


def resume_simulation(
    output_dir: str | Path,
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> SimulationEngine:
    """Resume a simulation from saved state.

    Args:
        output_dir: Path to existing simulation output
        provider: Optional override for provider
        model: Optional override for model
        api_key: Optional API key

    Returns:
        SimulationEngine ready to continue

    Raises:
        ValueError: If state cannot be loaded
    """
    from src.logging.logger import load_existing_run

    logger, state = load_existing_run(output_dir)

    if state is None:
        raise ValueError(f"Could not load state from {output_dir}")

    # Try to get provider/model from run info
    if logger.run_info_file.exists():
        import json

        with open(logger.run_info_file) as f:
            run_info = json.load(f)
            provider = provider or run_info.get("provider")
            model = model or run_info.get("model")

    if not provider or not model:
        raise ValueError("Provider and model must be specified or available in run info")

    # Create engine with existing state
    engine = SimulationEngine(
        provider=provider,
        model=model,
        api_key=api_key,
        output_dir=output_dir,
    )
    engine.state = state
    engine.logger = logger

    # Recreate runner with loaded state
    engine.runner = get_runner(provider, model, state, api_key, logger)

    return engine
