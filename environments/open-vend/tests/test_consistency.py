"""Comprehensive consistency tests for environmental coherence.

These tests verify that the simulation environment is consistent and coherent,
which is critical for evaluating LLM long-term reasoning abilities.
"""

import random

from src.agents.tools import (
    collect_cash,
    restock_machine,
    send_money,
    set_prices,
)
from src.simulation.economy import (
    DEFAULT_ECONOMICS,
    calculate_daily_sales,
    calculate_variety_multiplier,
    get_day_of_week,
    get_month,
    get_product_economics,
    process_daily_fee,
    process_end_of_day,
    process_order_deliveries,
)
from src.simulation.state import (
    GameState,
    Order,
    OrderStatus,
    SlotSize,
    WarehouseItem,
)
from src.simulation.suppliers import (
    SUPPLIERS,
    generate_fallback_supplier_response,
    get_supplier_by_email,
    parse_order_from_email,
    process_pending_supplier_emails,
    search_suppliers,
)

# =============================================================================
# SUPPLIER CONSISTENCY TESTS
# =============================================================================


class TestSupplierCatalogConsistency:
    """Test that supplier catalogs are always consistent."""

    def test_supplier_prices_never_change(self):
        """Verify supplier prices are constant across multiple accesses."""
        for email, supplier in SUPPLIERS.items():
            for product in supplier["products"]:
                original_price = product["wholesale_price"]
                # Access multiple times
                for _ in range(10):
                    supplier_again = get_supplier_by_email(email)
                    for p in supplier_again["products"]:
                        if p["id"] == product["id"]:
                            assert p["wholesale_price"] == original_price, (
                                f"Price changed for {product['name']}"
                            )

    def test_supplier_delivery_times_consistent(self):
        """Verify delivery times are always the same."""
        for email, supplier in SUPPLIERS.items():
            original_days = supplier["delivery_days"]
            for _ in range(10):
                assert get_supplier_by_email(email)["delivery_days"] == original_days

    def test_supplier_min_order_values_consistent(self):
        """Verify minimum order values don't change."""
        for email, supplier in SUPPLIERS.items():
            original_min = supplier["min_order_value"]
            for _ in range(10):
                assert get_supplier_by_email(email)["min_order_value"] == original_min

    def test_supplier_product_list_stable(self):
        """Verify suppliers always offer the same products."""
        for email, supplier in SUPPLIERS.items():
            original_product_ids = {p["id"] for p in supplier["products"]}
            for _ in range(10):
                current_ids = {p["id"] for p in get_supplier_by_email(email)["products"]}
                assert current_ids == original_product_ids, (
                    f"Product list changed for {supplier['name']}"
                )

    def test_supplier_min_quantities_consistent(self):
        """Verify minimum quantities don't change."""
        for email, supplier in SUPPLIERS.items():
            for product in supplier["products"]:
                original_min_qty = product["min_quantity"]
                for _ in range(10):
                    for p in get_supplier_by_email(email)["products"]:
                        if p["id"] == product["id"]:
                            assert p["min_quantity"] == original_min_qty


class TestSupplierResponseConsistency:
    """Test that supplier responses are consistent."""

    def test_fallback_response_contains_correct_catalog(self):
        """Verify fallback responses always include correct product info."""
        for email, supplier in SUPPLIERS.items():
            response = generate_fallback_supplier_response(
                supplier_email=email,
                customer_email="test@test.com",
                subject="Catalog Request",
                content="Please send catalog",
            )

            # Response should include supplier name
            assert supplier["name"] in response

            # Response should include all products with prices
            for product in supplier["products"]:
                assert product["name"] in response
                assert f"${product['wholesale_price']}" in response

    def test_fallback_response_idempotent(self):
        """Verify same query produces same response structure."""
        email = "orders@snackworld-wholesale.com"

        responses = []
        for _ in range(5):
            response = generate_fallback_supplier_response(
                supplier_email=email,
                customer_email="test@test.com",
                subject="Catalog",
                content="Send catalog please",
            )
            responses.append(response)

        # All responses should be identical
        for r in responses[1:]:
            assert r == responses[0]

    def test_search_results_consistent(self):
        """Verify search returns consistent results for same query."""
        queries = ["snacks", "drinks", "candy", "wholesale suppliers", "chips"]

        for query in queries:
            results = []
            for _ in range(5):
                results.append(search_suppliers(query))

            # All results should be identical
            for r in results[1:]:
                assert r == results[0], f"Search results differ for query: {query}"


class TestOrderParsingConsistency:
    """Test that order parsing is deterministic."""

    def test_same_email_parses_same_way(self):
        """Verify identical emails always parse to identical orders."""
        test_emails = [
            ("sales@candyking-dist.com", "Please send 48 Snickers bars"),
            ("orders@snackworld-wholesale.com", "Order: Lay's Classic Chips: 24 units"),
            ("wholesale@beverageplus.com", "I want 24 Coca-Cola cans and 24 Dasani water"),
        ]

        for supplier_email, content in test_emails:
            orders = []
            for _ in range(10):
                order = parse_order_from_email(supplier_email, content)
                orders.append(order)

            # All orders should be identical
            for i, order in enumerate(orders[1:], 1):
                if orders[0] is None:
                    assert order is None
                else:
                    assert order is not None
                    assert order["total_cost"] == orders[0]["total_cost"]
                    assert len(order["items"]) == len(orders[0]["items"])

    def test_order_total_calculation_accurate(self):
        """Verify order totals are calculated correctly."""
        # Test with known products and quantities
        content = "48 Snickers bars and 48 Twix bars"
        order = parse_order_from_email("sales@candyking-dist.com", content)

        assert order is not None
        expected_total = 48 * 0.50 + 48 * 0.50  # Snickers + Twix @ $0.50 each
        assert abs(order["total_cost"] - expected_total) < 0.01


# =============================================================================
# DEMAND MODEL CONSISTENCY TESTS
# =============================================================================


class TestDemandModelDeterminism:
    """Test that demand model is deterministic with same random seed."""

    def test_sales_reproducible_with_seed(self):
        """Verify same seed produces same sales."""

        def run_sales_simulation(seed):
            random.seed(seed)
            state = GameState()
            state.machine_slots[0].product_id = "chips_lays_classic"
            state.machine_slots[0].product_name = "Lay's Chips"
            state.machine_slots[0].quantity = 100
            state.machine_slots[0].price = 1.75

            sales = calculate_daily_sales(state)
            return [(s.product_id, s.quantity, s.total_revenue) for s in sales]

        # Run with same seed multiple times
        seed = 12345
        results = [run_sales_simulation(seed) for _ in range(5)]

        # All results should be identical
        for r in results[1:]:
            assert r == results[0], "Sales not reproducible with same seed"

    def test_different_seeds_produce_different_results(self):
        """Verify different seeds produce different results."""

        def run_sales_simulation(seed):
            random.seed(seed)
            state = GameState()
            state.machine_slots[0].product_id = "chips_lays_classic"
            state.machine_slots[0].product_name = "Lay's Chips"
            state.machine_slots[0].quantity = 100
            state.machine_slots[0].price = 1.75

            sales = calculate_daily_sales(state)
            return sum(s.quantity for s in sales)

        # Run with different seeds
        results = [run_sales_simulation(seed) for seed in range(100, 110)]

        # Results should vary (not all the same)
        assert len(set(results)) > 1, "Different seeds produced identical results"


class TestProductEconomicsConsistency:
    """Test that product economics are consistent."""

    def test_known_products_have_fixed_economics(self):
        """Verify known products always have the same economics."""
        state = GameState()

        for product_id, expected in DEFAULT_ECONOMICS.items():
            economics = get_product_economics(state, product_id)
            assert economics.reference_price == expected["reference_price"]
            assert economics.base_sales == expected["base_sales"]
            assert economics.price_elasticity == expected["elasticity"]

    def test_economics_cached_correctly(self):
        """Verify economics are cached and returned consistently."""
        state = GameState()

        # Get economics for a product
        e1 = get_product_economics(state, "chips_lays_classic")
        e2 = get_product_economics(state, "chips_lays_classic")

        # Should be same object (cached)
        assert e1 is e2

    def test_unknown_product_economics_cached(self):
        """Verify unknown product economics are generated once and cached."""
        state = GameState()
        random.seed(42)  # Set seed for reproducibility

        e1 = get_product_economics(state, "unknown_product_xyz")
        e2 = get_product_economics(state, "unknown_product_xyz")

        # Should be same object (cached)
        assert e1 is e2
        assert e1.reference_price == e2.reference_price


class TestTemporalMultiplierConsistency:
    """Test that temporal multipliers are applied correctly."""

    def test_day_of_week_mapping_correct(self):
        """Verify day of week calculation is correct."""
        # Day 1 = Monday (0)
        assert get_day_of_week(1) == 0  # Monday
        assert get_day_of_week(2) == 1  # Tuesday
        assert get_day_of_week(3) == 2  # Wednesday
        assert get_day_of_week(4) == 3  # Thursday
        assert get_day_of_week(5) == 4  # Friday
        assert get_day_of_week(6) == 5  # Saturday
        assert get_day_of_week(7) == 6  # Sunday
        assert get_day_of_week(8) == 0  # Monday again

    def test_month_mapping_correct(self):
        """Verify month calculation is correct."""
        assert get_month(1) == 1  # January
        assert get_month(30) == 1  # Still January
        assert get_month(31) == 2  # February
        assert get_month(60) == 2  # Still February
        assert get_month(61) == 3  # March

    def test_dow_multipliers_applied(self):
        """Verify day of week multipliers affect sales."""
        random.seed(42)

        # Create baseline state
        def create_test_state(day):
            state = GameState()
            state.current_day = day
            state.machine_slots[0].product_id = "candy_snickers"
            state.machine_slots[0].product_name = "Snickers"
            state.machine_slots[0].quantity = 100
            state.machine_slots[0].price = 1.50
            return state

        # Friday (day 5) should have higher sales than Sunday (day 7)
        friday_sales = []
        sunday_sales = []

        for _ in range(20):
            random.seed(42)
            state = create_test_state(5)  # Friday
            sales = calculate_daily_sales(state)
            friday_sales.append(sum(s.quantity for s in sales))

            random.seed(42)
            state = create_test_state(7)  # Sunday
            sales = calculate_daily_sales(state)
            sunday_sales.append(sum(s.quantity for s in sales))

        # Friday should generally have higher sales
        assert sum(friday_sales) > sum(sunday_sales), (
            "Friday sales should exceed Sunday sales due to DOW multipliers"
        )


class TestPriceElasticityConsistency:
    """Test that price elasticity works correctly."""

    def test_higher_price_reduces_sales(self):
        """Verify higher prices lead to lower sales on average."""
        random.seed(42)

        def get_average_sales(price, iterations=50):
            total = 0
            for i in range(iterations):
                random.seed(i)
                state = GameState()
                state.machine_slots[0].product_id = "candy_snickers"
                state.machine_slots[0].product_name = "Snickers"
                state.machine_slots[0].quantity = 100
                state.machine_slots[0].price = price
                sales = calculate_daily_sales(state)
                total += sum(s.quantity for s in sales)
            return total / iterations

        # Reference price is $1.50
        sales_at_1_50 = get_average_sales(1.50)
        sales_at_2_00 = get_average_sales(2.00)
        sales_at_3_00 = get_average_sales(3.00)

        assert sales_at_1_50 > sales_at_2_00 > sales_at_3_00, (
            f"Higher prices should reduce sales: "
            f"@$1.50={sales_at_1_50:.1f}, @$2.00={sales_at_2_00:.1f}, @$3.00={sales_at_3_00:.1f}"
        )

    def test_lower_price_increases_sales(self):
        """Verify lower prices lead to higher sales."""

        def get_average_sales(price, iterations=50):
            total = 0
            for i in range(iterations):
                random.seed(i)
                state = GameState()
                state.machine_slots[0].product_id = "candy_snickers"
                state.machine_slots[0].product_name = "Snickers"
                state.machine_slots[0].quantity = 100
                state.machine_slots[0].price = price
                sales = calculate_daily_sales(state)
                total += sum(s.quantity for s in sales)
            return total / iterations

        # Reference price is $1.50
        sales_at_1_00 = get_average_sales(1.00)
        sales_at_1_50 = get_average_sales(1.50)

        assert sales_at_1_00 > sales_at_1_50, (
            f"Lower prices should increase sales: @$1.00={sales_at_1_00:.1f} vs @$1.50={sales_at_1_50:.1f}"
        )


class TestVarietyMultiplierConsistency:
    """Test variety multiplier is calculated correctly."""

    def test_variety_multiplier_values(self):
        """Verify variety multiplier matches documented values."""
        state = GameState()

        # 0 products = 0.0
        assert calculate_variety_multiplier(state) == 0.0

        # 1 product = 0.8
        state.machine_slots[0].product_id = "p1"
        state.machine_slots[0].quantity = 5
        assert calculate_variety_multiplier(state) == 0.8

        # 2 products = 0.8
        state.machine_slots[1].product_id = "p2"
        state.machine_slots[1].quantity = 5
        assert calculate_variety_multiplier(state) == 0.8

        # 3-4 products = 1.2 (optimal)
        state.machine_slots[2].product_id = "p3"
        state.machine_slots[2].quantity = 5
        assert calculate_variety_multiplier(state) == 1.2

        state.machine_slots[3].product_id = "p4"
        state.machine_slots[3].quantity = 5
        assert calculate_variety_multiplier(state) == 1.2

        # 5-6 products = 1.0
        state.machine_slots[4].product_id = "p5"
        state.machine_slots[4].quantity = 5
        assert calculate_variety_multiplier(state) == 1.0

        state.machine_slots[5].product_id = "p6"
        state.machine_slots[5].quantity = 5
        assert calculate_variety_multiplier(state) == 1.0


# =============================================================================
# STATE/ACTION CONSISTENCY TESTS
# =============================================================================


class TestInventoryTracking:
    """Test that inventory is tracked accurately."""

    def test_restocking_updates_warehouse_and_machine(self):
        """Verify restocking moves items correctly between warehouse and machine."""
        state = GameState()

        # Add to warehouse
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        # Restock machine
        restock_machine(state, "chips", 0, 10)

        # Verify warehouse decreased
        assert state.warehouse["chips"].quantity == 40

        # Verify machine increased
        assert state.machine_slots[0].quantity == 10
        assert state.machine_slots[0].product_id == "chips"

    def test_sales_reduce_machine_inventory(self):
        """Verify sales correctly reduce machine inventory."""
        random.seed(42)

        state = GameState()
        state.machine_slots[0].product_id = "candy_snickers"
        state.machine_slots[0].product_name = "Snickers"
        state.machine_slots[0].quantity = 10
        state.machine_slots[0].price = 1.50

        initial_qty = state.machine_slots[0].quantity
        sales = calculate_daily_sales(state)
        sold = sum(s.quantity for s in sales)

        assert state.machine_slots[0].quantity == initial_qty - sold

    def test_delivery_adds_to_warehouse(self):
        """Verify deliveries correctly add to warehouse."""
        state = GameState()
        state.current_day = 5

        state.orders.append(
            Order(
                order_id="test_order",
                supplier_email="test@test.com",
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

        assert "chips" in state.warehouse
        assert state.warehouse["chips"].quantity == 24


class TestFinancialIntegrity:
    """Test that financial transactions are accurate."""

    def test_payment_deducts_correct_amount(self):
        """Verify payments deduct exact amount from balance."""
        state = GameState()
        state.bank_balance = 500.0

        send_money(state, "supplier@test.com", 123.45, "Test payment")

        assert abs(state.bank_balance - 376.55) < 0.01

    def test_sales_revenue_calculation(self):
        """Verify sales revenue is calculated correctly."""
        random.seed(42)

        state = GameState()
        state.machine_slots[0].product_id = "candy_snickers"
        state.machine_slots[0].product_name = "Snickers"
        state.machine_slots[0].quantity = 10
        state.machine_slots[0].price = 1.50

        initial_balance = state.bank_balance
        initial_cash = state.machine_cash

        sales = calculate_daily_sales(state)

        # Calculate expected revenue
        expected_revenue = sum(s.quantity * s.price_per_item for s in sales)
        actual_revenue_change = (state.bank_balance - initial_balance) + (
            state.machine_cash - initial_cash
        )

        assert abs(expected_revenue - actual_revenue_change) < 0.01

    def test_daily_fee_exact_amount(self):
        """Verify daily fee is exactly $2.00."""
        state = GameState()
        state.bank_balance = 100.0
        state.daily_fee = 2.0

        process_daily_fee(state)

        assert state.bank_balance == 98.0

    def test_cash_collection_transfers_exactly(self):
        """Verify cash collection transfers exact amount."""
        state = GameState()
        state.bank_balance = 100.0
        state.machine_cash = 25.50

        collect_cash(state)

        assert state.bank_balance == 125.50
        assert state.machine_cash == 0.0

    def test_net_worth_calculation_accurate(self):
        """Verify net worth includes all assets correctly."""
        state = GameState()
        state.bank_balance = 100.0
        state.machine_cash = 20.0

        # Add warehouse items
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        expected_net_worth = 100.0 + 20.0 + (50 * 0.75)
        assert abs(state.calculate_net_worth() - expected_net_worth) < 0.01


class TestOrderFlowConsistency:
    """Test the complete order flow is consistent."""

    def test_order_created_with_correct_delivery_date(self):
        """Verify orders have correct delivery dates based on supplier."""
        state = GameState()
        state.current_day = 1

        # CandyKing has 2-day delivery
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Order",
                "content": "48 Snickers bars please",
                "email_id": "sent_001",
            }
        )

        process_pending_supplier_emails(state)

        assert len(state.orders) == 1
        # Delivery = current_day + 1 (overnight processing) + delivery_days
        # So day 1 + 1 + 2 = day 4
        assert state.orders[0].delivery_day == 4

    def test_payment_marks_order_paid(self):
        """Verify payment correctly marks matching order as paid."""
        state = GameState()
        state.bank_balance = 500.0

        # Create pending order
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="sales@candyking-dist.com",
                items=[
                    {
                        "product_id": "candy_snickers",
                        "name": "Snickers",
                        "quantity": 48,
                        "unit_cost": 0.50,
                        "size": "small",
                    }
                ],
                total_cost=24.0,
                status=OrderStatus.PENDING,
                order_day=1,
                delivery_day=3,
            )
        )

        # Pay for order
        send_money(state, "sales@candyking-dist.com", 24.0, "Payment")

        assert state.orders[0].status == OrderStatus.PAID


class TestStateTransitionConsistency:
    """Test that state transitions are consistent."""

    def test_day_advances_correctly(self):
        """Verify day counter advances by exactly 1."""
        state = GameState()
        state.current_day = 5

        process_end_of_day(state)

        assert state.current_day == 6

    def test_tool_calls_reset_daily(self):
        """Verify tool call counter resets each day."""
        state = GameState()
        state.tool_calls_today = 25

        process_end_of_day(state)

        assert state.tool_calls_today == 0

    def test_state_serialization_preserves_data(self):
        """Verify state can be serialized and restored exactly."""
        state = GameState()
        state.bank_balance = 123.45
        state.machine_cash = 67.89
        state.current_day = 15
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=42,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        # Serialize and restore
        state_dict = state.to_dict()
        restored = GameState.from_dict(state_dict)

        assert restored.bank_balance == state.bank_balance
        assert restored.machine_cash == state.machine_cash
        assert restored.current_day == state.current_day
        assert restored.warehouse["chips"].quantity == 42


# =============================================================================
# MULTI-DAY SIMULATION CONSISTENCY TESTS
# =============================================================================


class TestMultiDayConsistency:
    """Test that the simulation remains consistent over many days."""

    def test_30_day_financial_consistency(self):
        """Verify financial tracking is accurate over 30 days."""
        random.seed(42)

        state = GameState()
        state.bank_balance = 500.0

        # Stock the machine
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=500,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        restock_machine(state, "chips", 0, 10)
        set_prices(state, {0: 1.75})

        # Run 30 days
        for day in range(30):
            # Restock if needed
            if state.machine_slots[0].quantity < 5:
                restock_machine(state, "chips", 0, 10)

            process_end_of_day(state)

            # Verify day advanced
            assert state.current_day == day + 2

            # Verify balance didn't become negative unexpectedly
            assert state.bank_balance >= -100  # Allow small negative

            # Verify net worth is calculable
            net_worth = state.calculate_net_worth()
            assert net_worth > 0

    def test_multi_day_inventory_tracking(self):
        """Verify inventory is tracked correctly over multiple days."""
        random.seed(42)

        state = GameState()

        # Add known inventory
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=100,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        # Track total items in system
        def count_total_items():
            warehouse_items = sum(w.quantity for w in state.warehouse.values())
            machine_items = sum(s.quantity for s in state.machine_slots)
            return warehouse_items + machine_items

        initial_total = count_total_items()

        # Stock machine
        restock_machine(state, "chips", 0, 10)
        restock_machine(state, "chips", 1, 10)

        # Total should stay same (just moved location)
        assert count_total_items() == initial_total

        # Set prices and run a day
        set_prices(state, {0: 1.50, 1: 1.50})
        process_end_of_day(state)

        # After sales, total should decrease by amount sold
        items_sold = sum(s.total_items_sold for s in state.daily_summaries)
        assert count_total_items() == initial_total - items_sold

    def test_daily_summaries_accurate(self):
        """Verify daily summaries accurately reflect what happened."""
        random.seed(42)

        state = GameState()
        state.bank_balance = 500.0

        # Stock and price
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=100,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        restock_machine(state, "chips", 0, 10)
        set_prices(state, {0: 1.75})

        # Run 5 days
        for day in range(5):
            process_end_of_day(state)

            summary = state.daily_summaries[-1]

            # Verify summary matches state changes
            assert summary.day == day + 1

            # Verify sales count matches
            sales_from_summary = sum(s.quantity for s in summary.sales)
            assert sales_from_summary == summary.total_items_sold

    def test_order_lifecycle_complete(self):
        """Verify orders go through complete lifecycle correctly."""
        state = GameState()
        state.current_day = 1
        state.bank_balance = 500.0

        # Place an order
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Order",
                "content": "48 Snickers bars please",
                "email_id": "sent_001",
            }
        )

        # Process end of day 1 (order created)
        process_end_of_day(state)
        assert len(state.orders) == 1
        assert state.orders[0].status == OrderStatus.PENDING

        # Pay for order on day 2
        send_money(state, "sales@candyking-dist.com", 24.0, "Payment")
        assert state.orders[0].status == OrderStatus.PAID
        delivery_day = state.orders[0].delivery_day

        # Process days until delivery
        while state.current_day < delivery_day:
            process_end_of_day(state)

        # After delivery day, order should be delivered
        process_end_of_day(state)
        assert state.orders[0].status == OrderStatus.DELIVERED

        # Items should be in warehouse
        assert "candy_snickers" in state.warehouse
        assert state.warehouse["candy_snickers"].quantity == 48


# =============================================================================
# SUPPLIER MEMORY / NEGOTIATION TESTS
# =============================================================================


class TestSupplierMemory:
    """Test supplier conversation memory functionality.

    Suppliers now store conversation history so they can reference past interactions
    when responding to emails. This enables negotiation, follow-ups, and contextual responses.
    """

    def test_conversation_history_stored(self):
        """Verify conversation history is stored correctly for each supplier."""
        state = GameState()

        # Send first email to supplier
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Initial inquiry",
                "content": "What products do you have?",
                "email_id": "sent_1",
            }
        )

        process_pending_supplier_emails(state)

        # Verify conversation history was created
        assert "sales@candyking-dist.com" in state.supplier_conversations
        history = state.supplier_conversations["sales@candyking-dist.com"]

        # Should have customer message + supplier response
        assert len(history) == 2
        assert history[0]["role"] == "customer"
        assert history[0]["content"] == "What products do you have?"
        assert history[1]["role"] == "supplier"

    def test_conversation_history_accumulates(self):
        """Verify conversation history accumulates across multiple emails."""
        state = GameState()

        # Send first email
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "First inquiry",
                "content": "What products do you have?",
                "email_id": "sent_1",
            }
        )
        process_pending_supplier_emails(state)

        # Advance day and send another email
        state.current_day = 2
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Follow up",
                "content": "Can I get a discount?",
                "email_id": "sent_2",
            }
        )
        process_pending_supplier_emails(state)

        # Verify history has all 4 messages (2 customer + 2 supplier)
        history = state.supplier_conversations["sales@candyking-dist.com"]
        assert len(history) == 4
        assert history[0]["role"] == "customer"
        assert history[1]["role"] == "supplier"
        assert history[2]["role"] == "customer"
        assert history[3]["role"] == "supplier"

    def test_different_suppliers_have_separate_history(self):
        """Verify each supplier has their own conversation history."""
        state = GameState()

        # Send email to two different suppliers
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Candy inquiry",
                "content": "I need candy",
                "email_id": "sent_1",
            }
        )
        state.pending_supplier_emails.append(
            {
                "to_address": "wholesale@beverageplus.com",
                "subject": "Drink inquiry",
                "content": "I need drinks",
                "email_id": "sent_2",
            }
        )
        process_pending_supplier_emails(state)

        # Verify separate histories
        assert len(state.supplier_conversations) == 2
        assert "sales@candyking-dist.com" in state.supplier_conversations
        assert "wholesale@beverageplus.com" in state.supplier_conversations

        candy_history = state.supplier_conversations["sales@candyking-dist.com"]
        beverage_history = state.supplier_conversations["wholesale@beverageplus.com"]

        assert candy_history[0]["content"] == "I need candy"
        assert beverage_history[0]["content"] == "I need drinks"

    def test_returning_customer_gets_different_greeting(self):
        """Verify returning customers get a different greeting in fallback response."""
        state = GameState()

        # First email
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "First inquiry",
                "content": "What products do you have?",
                "email_id": "sent_1",
            }
        )
        process_pending_supplier_emails(state)

        first_response = state.emails[-1].content

        # Second email (as returning customer)
        state.current_day = 2
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Second inquiry",
                "content": "I want to order more",
                "email_id": "sent_2",
            }
        )
        process_pending_supplier_emails(state)

        second_response = state.emails[-1].content

        # First response should be standard greeting
        assert "Thank you for contacting" in first_response

        # Second response should acknowledge returning customer
        assert "reaching out again" in second_response or "continued interest" in second_response

    def test_conversation_history_persists_in_state(self):
        """Verify conversation history survives state serialization."""
        state = GameState()

        # Create conversation
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Test",
                "content": "Hello",
                "email_id": "sent_1",
            }
        )
        process_pending_supplier_emails(state)

        # Serialize and deserialize
        state_dict = state.to_dict()
        loaded_state = GameState.from_dict(state_dict)

        # Verify history preserved
        assert "sales@candyking-dist.com" in loaded_state.supplier_conversations
        assert len(loaded_state.supplier_conversations["sales@candyking-dist.com"]) == 2

    def test_suppliers_have_no_negotiation_memory(self):
        """Document that suppliers still use static catalogs.

        While suppliers now have conversation history, the fallback response
        still uses the same static catalog. True negotiation would require
        an LLM to interpret the history and adjust pricing.
        """
        state = GameState()

        # Send multiple emails to same supplier
        for i in range(3):
            state.pending_supplier_emails.append(
                {
                    "to_address": "sales@candyking-dist.com",
                    "subject": f"Request {i}",
                    "content": f"Can I get a discount? Attempt {i}",
                    "email_id": f"sent_{i}",
                }
            )

        process_pending_supplier_emails(state)

        # All responses should be identical catalog info
        responses = [e for e in state.emails if e.from_address == "sales@candyking-dist.com"]

        assert len(responses) == 3

        # All responses contain the same prices (no discount)
        for response in responses:
            assert "$0.50" in response.content  # Snickers price
            assert "$0.48" in response.content  # Kit Kat price


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestEdgeCases:
    """Test edge cases for robustness."""

    def test_zero_inventory_no_sales(self):
        """Verify no sales occur with zero inventory."""
        state = GameState()
        state.machine_slots[0].product_id = "chips"
        state.machine_slots[0].quantity = 0
        state.machine_slots[0].price = 1.75

        sales = calculate_daily_sales(state)
        assert len(sales) == 0

    def test_zero_price_no_sales(self):
        """Verify no sales occur with zero price."""
        state = GameState()
        state.machine_slots[0].product_id = "chips"
        state.machine_slots[0].quantity = 10
        state.machine_slots[0].price = 0

        sales = calculate_daily_sales(state)
        assert len(sales) == 0

    def test_insufficient_funds_payment_fails(self):
        """Verify payment fails with insufficient funds."""
        state = GameState()
        state.bank_balance = 10.0

        result = send_money(state, "test@test.com", 100.0, "Test")

        assert "Insufficient" in result
        assert state.bank_balance == 10.0

    def test_overstocking_prevented(self):
        """Verify cannot overstock machine slots."""
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=100,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )

        # Try to stock more than capacity (10 for small slots)
        result = restock_machine(state, "chips", 0, 15)

        assert "Not enough space" in result

    def test_size_mismatch_prevented(self):
        """Verify cannot stock wrong size in slot."""
        state = GameState()
        state.warehouse["drink"] = WarehouseItem(
            product_id="drink",
            name="Drink",
            quantity=100,
            unit_cost=0.50,
            size=SlotSize.LARGE,
        )

        # Try to stock large item in small slot (slots 0-5 are small)
        result = restock_machine(state, "drink", 0, 5)

        assert "size mismatch" in result.lower()
