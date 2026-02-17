"""Tests for the economic model."""

from src.simulation.economy import (
    calculate_daily_sales,
    calculate_variety_multiplier,
    get_day_of_week,
    get_month,
    get_product_economics,
    process_daily_fee,
    process_order_deliveries,
)
from src.simulation.state import (
    GameState,
    Order,
    OrderStatus,
    SlotSize,
    WarehouseItem,
)


class TestTemporalHelpers:
    def test_day_of_week_monday_start(self):
        # Day 1 should be Monday (0)
        assert get_day_of_week(1) == 0
        assert get_day_of_week(2) == 1  # Tuesday
        assert get_day_of_week(7) == 6  # Sunday
        assert get_day_of_week(8) == 0  # Next Monday

    def test_get_month(self):
        assert get_month(1) == 1  # January
        assert get_month(30) == 1  # Still January
        assert get_month(31) == 2  # February
        assert get_month(365) == 1  # Wraps back (365/30 % 12 + 1)


class TestProductEconomics:
    def test_get_economics_known_product(self):
        state = GameState()
        economics = get_product_economics(state, "chips_lays_classic")
        assert economics.reference_price > 0
        assert economics.base_sales > 0
        assert economics.price_elasticity > 0

    def test_get_economics_caches_result(self):
        state = GameState()
        economics1 = get_product_economics(state, "chips_lays_classic")
        economics2 = get_product_economics(state, "chips_lays_classic")
        assert economics1 is economics2  # Same object from cache

    def test_get_economics_unknown_product(self):
        state = GameState()
        economics = get_product_economics(state, "unknown_product_xyz")
        # Should still return valid economics (randomly generated)
        assert economics.reference_price > 0
        assert economics.base_sales > 0


class TestVarietyMultiplier:
    def test_no_products(self):
        state = GameState()
        assert calculate_variety_multiplier(state) == 0.0

    def test_optimal_variety(self):
        state = GameState()
        # Add 3-4 products (optimal)
        for i, product_id in enumerate(["chips", "candy", "soda", "water"]):
            slot = state.machine_slots[i]
            slot.product_id = product_id
            slot.quantity = 5
        assert calculate_variety_multiplier(state) == 1.2

    def test_too_few_products(self):
        state = GameState()
        state.machine_slots[0].product_id = "chips"
        state.machine_slots[0].quantity = 5
        assert calculate_variety_multiplier(state) == 0.8

    def test_too_many_products(self):
        state = GameState()
        # Add 10 different products
        for i in range(10):
            state.machine_slots[i].product_id = f"product_{i}"
            state.machine_slots[i].quantity = 1
        assert calculate_variety_multiplier(state) == 0.5


class TestDailySales:
    def test_no_sales_empty_machine(self):
        state = GameState()
        sales = calculate_daily_sales(state)
        assert len(sales) == 0

    def test_no_sales_no_price_set(self):
        state = GameState()
        state.machine_slots[0].product_id = "chips"
        state.machine_slots[0].quantity = 10
        state.machine_slots[0].price = 0  # No price set
        sales = calculate_daily_sales(state)
        assert len(sales) == 0

    def test_sales_with_inventory(self):
        state = GameState()
        # Set up a product with inventory and price
        state.machine_slots[0].product_id = "chips_lays_classic"
        state.machine_slots[0].product_name = "Lay's Chips"
        state.machine_slots[0].quantity = 10
        state.machine_slots[0].price = 1.75

        # Run multiple times to ensure some sales occur
        total_sales = 0
        for _ in range(10):
            test_state = GameState()
            test_state.machine_slots[0].product_id = "chips_lays_classic"
            test_state.machine_slots[0].product_name = "Lay's Chips"
            test_state.machine_slots[0].quantity = 10
            test_state.machine_slots[0].price = 1.75
            sales = calculate_daily_sales(test_state)
            total_sales += len(sales)

        # Over 10 iterations, we should have some sales
        assert total_sales > 0

    def test_sales_reduce_inventory(self):
        state = GameState()
        state.machine_slots[0].product_id = "candy_snickers"
        state.machine_slots[0].product_name = "Snickers"
        state.machine_slots[0].quantity = 10
        state.machine_slots[0].price = 1.50

        initial_qty = state.machine_slots[0].quantity
        sales = calculate_daily_sales(state)

        items_sold = sum(s.quantity for s in sales)
        assert state.machine_slots[0].quantity == initial_qty - items_sold


class TestDailyFee:
    def test_fee_paid_success(self):
        state = GameState()
        state.bank_balance = 100.0
        state.daily_fee = 2.0

        fee_paid, msg = process_daily_fee(state)

        assert fee_paid is True
        assert state.bank_balance == 98.0
        assert state.consecutive_unpaid_days == 0

    def test_fee_not_paid_insufficient_funds(self):
        state = GameState()
        state.bank_balance = 1.0
        state.daily_fee = 2.0

        fee_paid, msg = process_daily_fee(state)

        assert fee_paid is False
        assert state.bank_balance == 1.0
        assert state.consecutive_unpaid_days == 1

    def test_consecutive_unpaid_days_accumulate(self):
        state = GameState()
        state.bank_balance = 0.0
        state.daily_fee = 2.0
        state.consecutive_unpaid_days = 5

        process_daily_fee(state)

        assert state.consecutive_unpaid_days == 6


class TestOrderDeliveries:
    def test_delivery_paid_order(self):
        state = GameState()
        state.current_day = 5
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="supplier@test.com",
                items=[
                    {
                        "product_id": "chips",
                        "name": "Chips",
                        "quantity": 24,
                        "unit_cost": 0.75,
                        "size": "small",
                    }
                ],
                total_cost=18.0,
                status=OrderStatus.PAID,
                order_day=1,
                delivery_day=4,  # Should be delivered by day 5
            )
        )

        notifications = process_order_deliveries(state)

        assert len(notifications) == 1
        assert "delivered" in notifications[0].lower()
        assert state.orders[0].status == OrderStatus.DELIVERED
        assert "chips" in state.warehouse
        assert state.warehouse["chips"].quantity == 24

    def test_no_delivery_unpaid_order(self):
        state = GameState()
        state.current_day = 5
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="supplier@test.com",
                items=[
                    {
                        "product_id": "chips",
                        "name": "Chips",
                        "quantity": 24,
                        "unit_cost": 0.75,
                        "size": "small",
                    }
                ],
                total_cost=18.0,
                status=OrderStatus.PENDING,  # Not paid
                order_day=1,
                delivery_day=4,
            )
        )

        notifications = process_order_deliveries(state)

        assert len(notifications) == 0
        assert state.orders[0].status == OrderStatus.PENDING

    def test_no_delivery_future_date(self):
        state = GameState()
        state.current_day = 2
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="supplier@test.com",
                items=[
                    {
                        "product_id": "chips",
                        "name": "Chips",
                        "quantity": 24,
                        "unit_cost": 0.75,
                        "size": "small",
                    }
                ],
                total_cost=18.0,
                status=OrderStatus.PAID,
                order_day=1,
                delivery_day=5,  # Not yet
            )
        )

        notifications = process_order_deliveries(state)

        assert len(notifications) == 0
        assert state.orders[0].status == OrderStatus.PAID

    def test_delivery_adds_to_existing_inventory(self):
        state = GameState()
        state.current_day = 5
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=10,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="supplier@test.com",
                items=[
                    {
                        "product_id": "chips",
                        "name": "Chips",
                        "quantity": 24,
                        "unit_cost": 0.75,
                        "size": "small",
                    }
                ],
                total_cost=18.0,
                status=OrderStatus.PAID,
                order_day=1,
                delivery_day=4,
            )
        )

        process_order_deliveries(state)

        assert state.warehouse["chips"].quantity == 34  # 10 + 24
