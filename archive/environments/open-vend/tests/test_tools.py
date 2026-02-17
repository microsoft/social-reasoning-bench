"""Tests for tool implementations."""

from src.agents.tools import (
    check_storage_quantities,
    collect_cash,
    execute_tool,
    get_keys,
    get_money_balance,
    get_tool_definitions,
    get_value,
    list_storage_products,
    read_email,
    read_email_inbox,
    restock_machine,
    send_email,
    send_money,
    set_prices,
    view_machine_inventory,
    write_value,
)
from src.simulation.state import (
    Email,
    GameState,
    Order,
    OrderStatus,
    SlotSize,
    WarehouseItem,
)


class TestMemoryTools:
    def test_write_and_get_value(self):
        state = GameState()
        result = write_value(state, "test_key", "test_value")
        assert "Stored" in result
        assert state.memory["test_key"] == "test_value"

        result = get_value(state, "test_key")
        assert result == "test_value"

    def test_get_nonexistent_key(self):
        state = GameState()
        result = get_value(state, "nonexistent")
        assert "not found" in result

    def test_get_keys_empty(self):
        state = GameState()
        result = get_keys(state)
        assert "empty" in result.lower()

    def test_get_keys_with_data(self):
        state = GameState()
        state.memory["key1"] = "value1"
        state.memory["key2"] = "value2"
        result = get_keys(state)
        assert "key1" in result
        assert "key2" in result


class TestEmailTools:
    def test_send_email(self):
        state = GameState()
        result = send_email(
            state,
            to_address="supplier@test.com",
            subject="Product Inquiry",
            content="What products do you have?",
        )
        assert "Email sent" in result
        assert len(state.emails) == 1
        assert len(state.pending_supplier_emails) == 1

    def test_read_email(self):
        state = GameState()
        email = Email(
            id="test_001",
            from_address="supplier@test.com",
            to_address="charles.paxton@vendingsandstuff.com",
            subject="Response",
            content="Here are our products...",
            timestamp="Day 1",
            read=False,
        )
        state.emails.append(email)

        result = read_email(state, "test_001")
        assert "Here are our products" in result
        assert state.emails[0].read is True

    def test_read_email_not_found(self):
        state = GameState()
        result = read_email(state, "nonexistent")
        assert "not found" in result

    def test_read_inbox_empty(self):
        state = GameState()
        result = read_email_inbox(state)
        assert "No unread" in result

    def test_read_inbox_with_emails(self):
        state = GameState()
        state.emails.append(
            Email(
                id="email_001",
                from_address="supplier@test.com",
                to_address="agent@test.com",
                subject="New Products",
                content="Content",
                timestamp="Day 1",
                read=False,
            )
        )
        state.emails.append(
            Email(
                id="email_002",
                from_address="other@test.com",
                to_address="agent@test.com",
                subject="Order Confirmation",
                content="Content",
                timestamp="Day 1",
                read=True,
            )
        )

        # Unread only
        result = read_email_inbox(state, show_all=False)
        assert "email_001" in result
        assert "email_002" not in result

        # All emails
        result = read_email_inbox(state, show_all=True)
        assert "email_001" in result
        assert "email_002" in result


class TestFinancialTools:
    def test_get_money_balance(self):
        state = GameState()
        state.bank_balance = 450.50
        state.machine_cash = 25.75
        result = get_money_balance(state)
        assert "450.50" in result
        assert "25.75" in result

    def test_send_money_success(self):
        state = GameState()
        state.bank_balance = 500.0
        result = send_money(state, "supplier@test.com", 100.0, "Payment for order")
        assert "Payment of $100.00 sent" in result
        assert state.bank_balance == 400.0

    def test_send_money_insufficient_funds(self):
        state = GameState()
        state.bank_balance = 50.0
        result = send_money(state, "supplier@test.com", 100.0)
        assert "Insufficient funds" in result
        assert state.bank_balance == 50.0

    def test_send_money_negative_amount(self):
        state = GameState()
        result = send_money(state, "supplier@test.com", -50.0)
        assert "must be positive" in result

    def test_send_money_marks_order_paid(self):
        state = GameState()
        state.bank_balance = 500.0
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="supplier@test.com",
                items=[],
                total_cost=100.0,
                status=OrderStatus.PENDING,
                order_day=1,
                delivery_day=3,
            )
        )

        result = send_money(state, "supplier@test.com", 100.0)
        assert "marked as paid" in result
        assert state.orders[0].status == OrderStatus.PAID


class TestInventoryTools:
    def test_check_storage_empty(self):
        state = GameState()
        result = check_storage_quantities(state)
        assert "empty" in result.lower()

    def test_check_storage_with_items(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Lay's Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        result = check_storage_quantities(state)
        assert "Lay's Chips" in result
        assert "50" in result

    def test_list_storage_products(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Lay's Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        result = list_storage_products(state)
        assert "chips" in result
        assert "0.75" in result


class TestMachineTools:
    def test_view_machine_inventory_empty(self):
        state = GameState()
        result = view_machine_inventory(state)
        assert "EMPTY" in result
        assert "Slot 0" in result

    def test_restock_machine_success(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Lay's Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        result = restock_machine(state, "chips", 0, 10)
        assert "Loaded 10 units" in result
        assert state.machine_slots[0].quantity == 10
        assert state.warehouse["chips"].quantity == 40

    def test_restock_machine_invalid_slot(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Lay's Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        result = restock_machine(state, "chips", 15, 10)
        assert "Invalid slot" in result

    def test_restock_machine_size_mismatch(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Lay's Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        # Try to put small item in large slot (slot 6+)
        result = restock_machine(state, "chips", 6, 10)
        assert "size mismatch" in result.lower()

    def test_restock_machine_not_enough_warehouse(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Lay's Chips",
            quantity=5,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        result = restock_machine(state, "chips", 0, 10)
        assert "Not enough in warehouse" in result

    def test_set_prices(self):
        state = GameState()
        result = set_prices(state, {0: 1.75, 1: 1.50, 2: 2.00})
        assert "Price changes" in result
        assert state.machine_slots[0].price == 1.75
        assert state.machine_slots[1].price == 1.50
        assert state.machine_slots[2].price == 2.00

    def test_set_prices_invalid_slot(self):
        state = GameState()
        result = set_prices(state, {15: 1.75})
        assert "Invalid slot" in result

    def test_collect_cash(self):
        state = GameState()
        state.machine_cash = 50.0
        state.bank_balance = 400.0
        result = collect_cash(state)
        assert "Collected $50.00" in result
        assert state.machine_cash == 0.0
        assert state.bank_balance == 450.0

    def test_collect_cash_empty(self):
        state = GameState()
        state.machine_cash = 0.0
        result = collect_cash(state)
        assert "No cash" in result


class TestToolExecution:
    def test_execute_tool_unknown(self):
        state = GameState()
        result = execute_tool(state, "unknown_tool", {})
        assert "Unknown tool" in result

    def test_execute_tool_tracks_calls(self):
        state = GameState()
        state.tool_calls_today = 0
        execute_tool(state, "get_money_balance", {})
        assert state.tool_calls_today == 1

    def test_execute_tool_daily_limit(self):
        state = GameState()
        state.tool_calls_today = 50
        state.max_tool_calls_per_day = 50
        result = execute_tool(state, "get_money_balance", {})
        assert "Daily tool call limit" in result

    def test_get_tool_definitions(self):
        definitions = get_tool_definitions()
        assert len(definitions) > 0
        assert all("type" in d and d["type"] == "function" for d in definitions)
        assert all("function" in d for d in definitions)

        # Check some specific tools exist
        tool_names = [d["function"]["name"] for d in definitions]
        assert "write_value" in tool_names
        assert "get_money_balance" in tool_names
        assert "wait_until_next_day" in tool_names
