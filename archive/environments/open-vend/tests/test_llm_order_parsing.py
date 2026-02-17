"""Tests for LLM-based order parsing."""

from src.simulation.suppliers import OrderItem, ParsedOrder, parse_order_from_email


class MockLLMClient:
    """Mock LLM client for testing."""

    def __init__(self, parsed_order: ParsedOrder):
        self.parsed_order = parsed_order

    def generate_structured(self, prompt: str, response_model: type) -> ParsedOrder:
        """Return the pre-configured parsed order."""
        return self.parsed_order


class TestLLMOrderParsing:
    """Test LLM-based order parsing functionality."""

    def test_parse_valid_order_with_llm(self):
        """Test parsing a valid order using LLM."""
        # Mock LLM response
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="Snickers Bar", quantity=48),
                OrderItem(product_name="Kit Kat Bar", quantity=48),
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # Parse order
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "Hi, I'd like to order 48 Snickers and 48 Kit Kats please.",
            mock_client,
        )

        assert result is not None
        assert result["supplier_email"] == "sales@candyking-dist.com"
        assert len(result["items"]) == 2
        assert result["items"][0]["product_id"] == "candy_snickers"
        assert result["items"][0]["quantity"] == 48
        assert result["items"][1]["product_id"] == "candy_kitkat"
        assert result["items"][1]["quantity"] == 48
        assert result["total_cost"] == 48 * 0.50 + 48 * 0.48  # $47.04

    def test_parse_inquiry_not_order(self):
        """Test that inquiries are not parsed as orders."""
        # Mock LLM response for an inquiry
        mock_order = ParsedOrder(
            items=[],
            contains_order=False,
        )
        mock_client = MockLLMClient(mock_order)

        # Parse inquiry
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "What products do you have available?",
            mock_client,
        )

        assert result is None

    def test_parse_below_minimum_quantity(self):
        """Test that orders below minimum quantity are rejected."""
        # Mock LLM response with quantity below minimum
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="Snickers Bar", quantity=10),  # Min is 48
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # Parse order
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "I need 10 Snickers bars.",
            mock_client,
        )

        assert result is None

    def test_parse_below_minimum_order_value(self):
        """Test that orders below minimum value are rejected."""
        # CandyKing has $20 minimum order value
        # Orbit gum is $0.40 each, min qty 60 = $24 (valid single item)
        # But if we order less total value...

        # Mock LLM response
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="Orbit Gum Pack", quantity=40),  # $16 < $20 min
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # This won't match because 40 < min_quantity of 60
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "I need 40 packs of Orbit gum.",
            mock_client,
        )

        assert result is None

    def test_parse_product_name_fuzzy_matching(self):
        """Test that product names are fuzzy matched."""
        # Mock LLM response with slight variation in product name
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="snickers bar", quantity=48),  # lowercase
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # Parse order
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "I want 48 snickers bars",
            mock_client,
        )

        assert result is not None
        assert result["items"][0]["product_id"] == "candy_snickers"

    def test_fallback_to_regex_when_no_llm(self):
        """Test that regex parsing is used when no LLM client provided."""
        # Parse order without LLM client
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "48 Snickers bars please",
            None,  # No LLM client
        )

        assert result is not None
        assert result["items"][0]["product_id"] == "candy_snickers"
        assert result["items"][0]["quantity"] == 48

    def test_fallback_to_regex_when_llm_fails(self):
        """Test that regex parsing is used when LLM fails."""

        class FailingLLMClient:
            def generate_structured(self, prompt: str, response_model: type):
                raise Exception("LLM error")

        # Parse order with failing LLM
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "48 Snickers bars please",
            FailingLLMClient(),
        )

        assert result is not None
        assert result["items"][0]["product_id"] == "candy_snickers"
        assert result["items"][0]["quantity"] == 48

    def test_parse_multiple_items_order(self):
        """Test parsing an order with multiple different items."""
        # Mock LLM response
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="Lay's Classic Chips", quantity=24),
                OrderItem(product_name="Doritos Nacho Cheese", quantity=24),
                OrderItem(product_name="Cheetos Crunchy", quantity=24),
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # Parse order
        result = parse_order_from_email(
            "orders@snackworld-wholesale.com",
            "I need 24 of each: Lays, Doritos, and Cheetos",
            mock_client,
        )

        assert result is not None
        assert len(result["items"]) == 3
        total_cost = 24 * 0.75 + 24 * 0.80 + 24 * 0.70  # $54.00
        assert abs(result["total_cost"] - total_cost) < 0.01

    def test_parse_order_includes_delivery_days(self):
        """Test that parsed order includes correct delivery days."""
        # Mock LLM response
        # BeveragePlus has $30 minimum, Coke is $0.45/unit, so need 67+ units
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="Coca-Cola Can 12oz", quantity=72),
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # BeveragePlus has 3-day delivery
        result = parse_order_from_email(
            "wholesale@beverageplus.com",
            "72 cans of Coke please",
            mock_client,
        )

        assert result is not None
        assert result["delivery_days"] == 3

    def test_parse_unknown_product(self):
        """Test that unknown products are not included in order."""
        # Mock LLM response with unknown product
        mock_order = ParsedOrder(
            items=[
                OrderItem(product_name="Mystery Product", quantity=100),
            ],
            contains_order=True,
        )
        mock_client = MockLLMClient(mock_order)

        # Parse order
        result = parse_order_from_email(
            "sales@candyking-dist.com",
            "I want 100 Mystery Products",
            mock_client,
        )

        # Should return None because no valid products matched
        assert result is None
