"""Integration tests for the OpenVend simulation."""

import json
import tempfile
from pathlib import Path

from src.agents.tools import execute_tool
from src.logging.logger import SimulationLogger
from src.simulation.economy import process_end_of_day
from src.simulation.state import GameState, OrderStatus, SlotSize, WarehouseItem


class TestFullDayCycle:
    """Test a complete day cycle from start to finish."""

    def test_complete_day_with_sales(self):
        """Test a complete day cycle with inventory and sales."""
        state = GameState()

        # Set up inventory in warehouse
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Test Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        # Restock machine
        result = execute_tool(
            state, "restock_machine", {"product_id": "chips", "slot_id": 0, "quantity": 10}
        )
        assert "Loaded" in result

        # Set price
        result = execute_tool(state, "set_prices", {"prices": {0: 1.75}})
        assert "Price changes" in result

        # Verify machine state
        result = execute_tool(state, "view_machine_inventory", {})
        assert "Test Chips" in result
        assert "1.75" in result

        # Process end of day
        process_end_of_day(state)

        # Day should advance
        assert state.current_day == 2
        # Tool calls should reset
        assert state.tool_calls_today == 0


class TestSupplierOrderFlow:
    """Test the complete supplier interaction flow."""

    def test_search_email_order_pay_deliver(self):
        """Test finding suppliers, ordering, paying, and receiving delivery."""
        state = GameState()

        # 1. Search for suppliers
        result = execute_tool(state, "search_internet", {"query": "candy suppliers"})
        assert "CandyKing" in result

        # 2. Send email to supplier
        result = execute_tool(
            state,
            "send_email",
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Order Request",
                "content": "I would like to order 48 Snickers bars",
            },
        )
        assert "Email sent" in result

        # 3. Process end of day (supplier responds, order created)
        process_end_of_day(state)

        # Should have an order
        assert len(state.orders) == 1
        assert state.orders[0].status == OrderStatus.PENDING

        # 4. Check inbox for response
        result = execute_tool(state, "read_email_inbox", {})
        assert "candyking" in result.lower() or len([e for e in state.emails if not e.read]) > 0

        # 5. Pay for order
        order = state.orders[0]
        result = execute_tool(
            state,
            "send_money",
            {"recipient": "sales@candyking-dist.com", "amount": order.total_cost},
        )
        assert "paid" in result.lower()
        assert state.orders[0].status == OrderStatus.PAID

        # 6. Wait for delivery (advance days until delivery day passes)
        delivery_day = state.orders[0].delivery_day
        while state.current_day <= delivery_day:
            process_end_of_day(state)

        # 7. Order should be delivered
        assert state.orders[0].status == OrderStatus.DELIVERED
        assert "candy_snickers" in state.warehouse

        # 8. Check storage
        result = execute_tool(state, "check_storage_quantities", {})
        assert "48" in result or "Snickers" in result


class TestMemoryPersistence:
    """Test that memory persists across days."""

    def test_memory_persists_across_days(self):
        state = GameState()

        # Write some memory
        execute_tool(state, "write_value", {"key": "strategy", "value": "Focus on drinks"})
        execute_tool(state, "write_value", {"key": "best_price", "value": "1.75"})

        # Advance several days
        for _ in range(5):
            process_end_of_day(state)

        # Memory should persist
        result = execute_tool(state, "get_value", {"key": "strategy"})
        assert result == "Focus on drinks"

        result = execute_tool(state, "get_keys", {})
        assert "strategy" in result
        assert "best_price" in result


class TestBankruptcyCondition:
    """Test bankruptcy detection."""

    def test_bankruptcy_after_unpaid_days(self):
        state = GameState()
        state.bank_balance = 0.0  # No money

        # Process 10 days without paying fees
        for i in range(10):
            process_end_of_day(state)
            if state.consecutive_unpaid_days >= 10:
                break

        assert state.consecutive_unpaid_days >= 10


class TestLoggerIntegration:
    """Test the logging system integration."""

    def test_logger_saves_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = SimulationLogger(tmpdir)

            state = GameState()
            state.current_day = 5
            state.bank_balance = 350.0

            logger.save_state(state)

            # Load back
            loaded = logger.load_state()
            assert loaded is not None
            assert loaded.current_day == 5
            assert loaded.bank_balance == 350.0

    def test_logger_run_info(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = SimulationLogger(tmpdir)

            logger.log_run_start(provider="openai", model="gpt-4o", config={"max_days": 30})

            state = GameState()
            state.current_day = 10
            logger.log_run_end(state, reason="completed", token_usage={"total_tokens": 1000})

            # Check run info was saved
            run_info_path = Path(tmpdir) / "run_info.json"
            assert run_info_path.exists()

            with open(run_info_path) as f:
                info = json.load(f)

            assert info["provider"] == "openai"
            assert info["end_reason"] == "completed"

    def test_logger_message_logging(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = SimulationLogger(tmpdir)

            logger.log_message(role="user", content="Test message", day=1)
            logger.log_message(role="assistant", content="Response", day=1)

            # Check messages file
            messages_path = Path(tmpdir) / "messages.jsonl"
            assert messages_path.exists()

            lines = messages_path.read_text().strip().split("\n")
            assert len(lines) == 2

    def test_logger_tool_call_logging(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = SimulationLogger(tmpdir)

            logger.log_tool_call(
                tool_name="get_money_balance",
                arguments={},
                result="$500.00",
                day=1,
            )

            # Check tool calls file
            tool_calls_path = Path(tmpdir) / "tool_calls.jsonl"
            assert tool_calls_path.exists()

            with open(tool_calls_path) as f:
                entry = json.loads(f.readline())

            assert entry["tool_name"] == "get_money_balance"


class TestToolChaining:
    """Test that tools work correctly in sequence."""

    def test_restock_then_set_price_then_sell(self):
        state = GameState()

        # Add product to warehouse
        state.warehouse["soda"] = WarehouseItem(
            product_id="soda",
            name="Cola",
            quantity=30,
            unit_cost=0.45,
            size=SlotSize.LARGE,
        )

        # Restock (large items go to slot 6+)
        result = execute_tool(
            state, "restock_machine", {"product_id": "soda", "slot_id": 6, "quantity": 8}
        )
        assert "Loaded" in result

        # Set price
        result = execute_tool(state, "set_prices", {"prices": {6: 1.75}})
        assert state.machine_slots[6].price == 1.75

        # View inventory
        result = execute_tool(state, "view_machine_inventory", {})
        assert "Cola" in result
        assert "8" in result  # quantity

        # Process day (should get sales)
        process_end_of_day(state)

        # Collect any cash
        result = execute_tool(state, "collect_cash", {})
        # May or may not have cash depending on random sales

    def test_collect_cash_increases_balance(self):
        state = GameState()
        state.bank_balance = 100.0
        state.machine_cash = 50.0

        execute_tool(state, "collect_cash", {})

        assert state.bank_balance == 150.0
        assert state.machine_cash == 0.0


class TestNetWorthCalculation:
    """Test net worth calculation at different stages."""

    def test_initial_net_worth(self):
        state = GameState()
        # Starting with $500
        assert state.calculate_net_worth() == 500.0

    def test_net_worth_with_inventory(self):
        state = GameState()
        state.bank_balance = 400.0
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=100,
            unit_cost=0.50,
            size=SlotSize.SMALL,
        )
        # 400 + (100 * 0.50) = 450
        assert state.calculate_net_worth() == 450.0

    def test_net_worth_with_machine_cash(self):
        state = GameState()
        state.bank_balance = 400.0
        state.machine_cash = 75.0
        # 400 + 75 = 475
        assert state.calculate_net_worth() == 475.0

    def test_net_worth_comprehensive(self):
        state = GameState()
        state.bank_balance = 300.0
        state.machine_cash = 50.0
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=100,
            unit_cost=0.50,  # $50 value
            size=SlotSize.SMALL,
        )
        # Also add the same product to machine
        state.machine_slots[0].product_id = "chips"
        state.machine_slots[0].quantity = 20  # 20 * 0.50 = $10

        # 300 + 50 + 50 + 10 = 410
        assert state.calculate_net_worth() == 410.0
