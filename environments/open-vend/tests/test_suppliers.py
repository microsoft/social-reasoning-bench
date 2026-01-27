"""Tests for the supplier system."""

from src.simulation.state import GameState
from src.simulation.suppliers import (
    SUPPLIERS,
    generate_fallback_supplier_response,
    generate_supplier_response_prompt,
    get_supplier_by_email,
    parse_order_from_email,
    process_pending_supplier_emails,
    search_suppliers,
)


class TestSupplierCatalog:
    def test_suppliers_exist(self):
        assert len(SUPPLIERS) > 0
        # Check we have variety
        assert "orders@snackworld-wholesale.com" in SUPPLIERS
        assert "sales@candyking-dist.com" in SUPPLIERS
        assert "wholesale@beverageplus.com" in SUPPLIERS

    def test_supplier_has_required_fields(self):
        for email, supplier in SUPPLIERS.items():
            assert "name" in supplier
            assert "description" in supplier
            assert "delivery_days" in supplier
            assert "min_order_value" in supplier
            assert "products" in supplier
            assert len(supplier["products"]) > 0

    def test_product_has_required_fields(self):
        for email, supplier in SUPPLIERS.items():
            for product in supplier["products"]:
                assert "id" in product
                assert "name" in product
                assert "size" in product
                assert product["size"] in ["small", "large"]
                assert "wholesale_price" in product
                assert "min_quantity" in product

    def test_get_supplier_by_email(self):
        supplier = get_supplier_by_email("orders@snackworld-wholesale.com")
        assert supplier is not None
        assert supplier["name"] == "SnackWorld Wholesale"

    def test_get_supplier_not_found(self):
        supplier = get_supplier_by_email("nonexistent@test.com")
        assert supplier is None


class TestSupplierSearch:
    def test_search_generic(self):
        result = search_suppliers("wholesale suppliers")
        assert "SnackWorld" in result
        assert "CandyKing" in result
        assert "BeveragePlus" in result

    def test_search_snacks(self):
        result = search_suppliers("snacks chips")
        assert "SnackWorld" in result

    def test_search_drinks(self):
        result = search_suppliers("drinks beverages soda")
        assert "BeveragePlus" in result

    def test_search_candy(self):
        result = search_suppliers("candy chocolate")
        assert "CandyKing" in result

    def test_search_returns_email(self):
        result = search_suppliers("suppliers")
        # Should include email addresses
        assert "@" in result


class TestOrderParsing:
    def test_parse_order_simple(self):
        content = "I would like to order 48 Snickers bars"
        order = parse_order_from_email("sales@candyking-dist.com", content)

        assert order is not None
        assert len(order["items"]) == 1
        assert order["items"][0]["quantity"] == 48

    def test_parse_order_multiple_items(self):
        content = """
        Please send me:
        48 Snickers bars
        48 Twix bars
        """
        order = parse_order_from_email("sales@candyking-dist.com", content)

        assert order is not None
        assert len(order["items"]) >= 1

    def test_parse_order_below_minimum(self):
        # Below minimum quantity should not parse
        content = "I want 10 Snickers bars"  # min is 48
        order = parse_order_from_email("sales@candyking-dist.com", content)

        assert order is None

    def test_parse_order_unknown_supplier(self):
        content = "Order 48 Snickers"
        order = parse_order_from_email("unknown@test.com", content)

        assert order is None

    def test_parse_order_calculates_total(self):
        content = "I want 48 Snickers bars"  # 48 * 0.50 = $24
        order = parse_order_from_email("sales@candyking-dist.com", content)

        if order:
            assert order["total_cost"] == 48 * 0.50


class TestSupplierResponses:
    def test_generate_response_prompt(self):
        prompt = generate_supplier_response_prompt(
            supplier_email="orders@snackworld-wholesale.com",
            customer_email="charles.paxton@vendingsandstuff.com",
            subject="Product Inquiry",
            content="What chips do you have?",
        )

        assert prompt is not None
        assert "SnackWorld" in prompt
        assert "What chips do you have?" in prompt

    def test_generate_response_prompt_unknown_supplier(self):
        prompt = generate_supplier_response_prompt(
            supplier_email="unknown@test.com",
            customer_email="test@test.com",
            subject="Test",
            content="Test",
        )

        assert prompt is None

    def test_fallback_response(self):
        response = generate_fallback_supplier_response(
            supplier_email="orders@snackworld-wholesale.com",
            customer_email="charles.paxton@vendingsandstuff.com",
            subject="Inquiry",
            content="Tell me about your products",
        )

        assert "SnackWorld" in response
        assert "$" in response  # Should include prices
        assert "delivery" in response.lower()

    def test_fallback_response_unknown_supplier(self):
        response = generate_fallback_supplier_response(
            supplier_email="unknown@test.com",
            customer_email="test@test.com",
            subject="Test",
            content="Test",
        )

        assert "could not find" in response.lower()


class TestPendingEmailProcessing:
    def test_process_valid_supplier_email(self):
        state = GameState()
        state.pending_supplier_emails.append(
            {
                "to_address": "orders@snackworld-wholesale.com",
                "subject": "Product Inquiry",
                "content": "What do you have?",
                "email_id": "sent_001",
            }
        )

        notifications = process_pending_supplier_emails(state, llm_client=None)

        assert len(notifications) > 0
        assert len(state.emails) > 0
        # Should have received a response
        response_emails = [
            e for e in state.emails if e.from_address == "orders@snackworld-wholesale.com"
        ]
        assert len(response_emails) == 1

    def test_process_unknown_supplier_bounces(self):
        state = GameState()
        state.pending_supplier_emails.append(
            {
                "to_address": "fake@nonexistent.com",
                "subject": "Test",
                "content": "Test",
                "email_id": "sent_001",
            }
        )

        process_pending_supplier_emails(state, llm_client=None)

        # Should get a bounce notification
        bounce_emails = [e for e in state.emails if "Undeliverable" in e.subject]
        assert len(bounce_emails) == 1

    def test_process_clears_pending_emails(self):
        state = GameState()
        state.pending_supplier_emails.append(
            {
                "to_address": "orders@snackworld-wholesale.com",
                "subject": "Test",
                "content": "Test",
                "email_id": "sent_001",
            }
        )

        process_pending_supplier_emails(state, llm_client=None)

        assert len(state.pending_supplier_emails) == 0

    def test_process_email_with_order_creates_order(self):
        state = GameState()
        state.pending_supplier_emails.append(
            {
                "to_address": "sales@candyking-dist.com",
                "subject": "Order Request",
                "content": "Please send 48 Snickers bars to my address.",
                "email_id": "sent_001",
            }
        )

        notifications = process_pending_supplier_emails(state, llm_client=None)

        # Should have created an order
        order_notifications = [n for n in notifications if "Order" in n and "created" in n]
        assert len(order_notifications) == 1
        assert len(state.orders) == 1
