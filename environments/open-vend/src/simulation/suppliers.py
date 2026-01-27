"""Supplier catalog and LLM-generated response system."""

from __future__ import annotations

import re
import uuid
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.simulation.state import GameState

# =============================================================================
# Order Parsing Models
# =============================================================================


class OrderItem(BaseModel):
    """A single item in an order."""

    product_name: str = Field(description="The exact product name from the email")
    quantity: int = Field(description="The quantity ordered", gt=0)


class ParsedOrder(BaseModel):
    """Structured order extracted from email."""

    items: list[OrderItem] = Field(
        description="List of products and quantities being ordered. Empty list if no order found."
    )
    contains_order: bool = Field(
        description="Whether the email contains a clear order request (not just an inquiry)"
    )


# =============================================================================
# Supplier Catalog
# =============================================================================

SUPPLIERS: dict[str, dict[str, Any]] = {
    "orders@snackworld-wholesale.com": {
        "name": "SnackWorld Wholesale",
        "description": "Major distributor of chips, crackers, and savory snacks",
        "delivery_days": 2,
        "min_order_value": 25.0,
        "products": [
            {
                "id": "chips_lays_classic",
                "name": "Lay's Classic Chips",
                "size": "small",
                "wholesale_price": 0.75,
                "suggested_retail": 1.75,
                "min_quantity": 24,
            },
            {
                "id": "chips_doritos_nacho",
                "name": "Doritos Nacho Cheese",
                "size": "small",
                "wholesale_price": 0.80,
                "suggested_retail": 1.85,
                "min_quantity": 24,
            },
            {
                "id": "chips_cheetos_crunchy",
                "name": "Cheetos Crunchy",
                "size": "small",
                "wholesale_price": 0.70,
                "suggested_retail": 1.65,
                "min_quantity": 24,
            },
            {
                "id": "crackers_ritz",
                "name": "Ritz Crackers Pack",
                "size": "small",
                "wholesale_price": 0.60,
                "suggested_retail": 1.50,
                "min_quantity": 36,
            },
            {
                "id": "pretzels_snyder",
                "name": "Snyder's Pretzels",
                "size": "small",
                "wholesale_price": 0.55,
                "suggested_retail": 1.40,
                "min_quantity": 36,
            },
        ],
    },
    "sales@candyking-dist.com": {
        "name": "CandyKing Distributors",
        "description": "Premium candy and chocolate supplier",
        "delivery_days": 2,
        "min_order_value": 20.0,
        "products": [
            {
                "id": "candy_snickers",
                "name": "Snickers Bar",
                "size": "small",
                "wholesale_price": 0.50,
                "suggested_retail": 1.50,
                "min_quantity": 48,
            },
            {
                "id": "candy_twix",
                "name": "Twix Bar",
                "size": "small",
                "wholesale_price": 0.50,
                "suggested_retail": 1.50,
                "min_quantity": 48,
            },
            {
                "id": "candy_mm_peanut",
                "name": "M&M's Peanut",
                "size": "small",
                "wholesale_price": 0.55,
                "suggested_retail": 1.60,
                "min_quantity": 48,
            },
            {
                "id": "candy_kitkat",
                "name": "Kit Kat Bar",
                "size": "small",
                "wholesale_price": 0.48,
                "suggested_retail": 1.45,
                "min_quantity": 48,
            },
            {
                "id": "gum_orbit",
                "name": "Orbit Gum Pack",
                "size": "small",
                "wholesale_price": 0.40,
                "suggested_retail": 1.25,
                "min_quantity": 60,
            },
        ],
    },
    "wholesale@beverageplus.com": {
        "name": "BeveragePlus Wholesale",
        "description": "Drinks and beverages for vending machines",
        "delivery_days": 3,
        "min_order_value": 30.0,
        "products": [
            {
                "id": "drink_coke_can",
                "name": "Coca-Cola Can 12oz",
                "size": "large",
                "wholesale_price": 0.45,
                "suggested_retail": 1.75,
                "min_quantity": 24,
            },
            {
                "id": "drink_pepsi_can",
                "name": "Pepsi Can 12oz",
                "size": "large",
                "wholesale_price": 0.45,
                "suggested_retail": 1.75,
                "min_quantity": 24,
            },
            {
                "id": "drink_sprite_can",
                "name": "Sprite Can 12oz",
                "size": "large",
                "wholesale_price": 0.45,
                "suggested_retail": 1.75,
                "min_quantity": 24,
            },
            {
                "id": "water_dasani",
                "name": "Dasani Water Bottle 16oz",
                "size": "large",
                "wholesale_price": 0.35,
                "suggested_retail": 1.50,
                "min_quantity": 24,
            },
            {
                "id": "energy_redbull",
                "name": "Red Bull 8.4oz",
                "size": "large",
                "wholesale_price": 1.20,
                "suggested_retail": 3.00,
                "min_quantity": 24,
            },
            {
                "id": "energy_monster",
                "name": "Monster Energy 16oz",
                "size": "large",
                "wholesale_price": 1.10,
                "suggested_retail": 2.75,
                "min_quantity": 24,
            },
        ],
    },
    "info@healthysnacks-co.com": {
        "name": "HealthySnacks Co.",
        "description": "Organic and healthy snack alternatives",
        "delivery_days": 3,
        "min_order_value": 35.0,
        "products": [
            {
                "id": "bar_kind_almond",
                "name": "KIND Almond Bar",
                "size": "small",
                "wholesale_price": 0.90,
                "suggested_retail": 2.25,
                "min_quantity": 24,
            },
            {
                "id": "bar_clif_chocolate",
                "name": "Clif Bar Chocolate Chip",
                "size": "small",
                "wholesale_price": 0.85,
                "suggested_retail": 2.15,
                "min_quantity": 24,
            },
            {
                "id": "nuts_almonds",
                "name": "Roasted Almonds Pack",
                "size": "small",
                "wholesale_price": 0.95,
                "suggested_retail": 2.35,
                "min_quantity": 24,
            },
            {
                "id": "fruit_dried_mix",
                "name": "Dried Fruit Mix",
                "size": "small",
                "wholesale_price": 0.80,
                "suggested_retail": 2.00,
                "min_quantity": 24,
            },
        ],
    },
}


def search_suppliers(query: str) -> str:
    """Search for suppliers based on a query.

    Args:
        query: Search query (e.g., "snacks", "drinks", "wholesale")

    Returns:
        Formatted search results
    """
    query_lower = query.lower()
    results = []

    # Keywords that match different suppliers
    keyword_map = {
        "orders@snackworld-wholesale.com": [
            "snack",
            "chip",
            "cracker",
            "pretzel",
            "cheeto",
            "dorito",
            "lay",
        ],
        "sales@candyking-dist.com": [
            "candy",
            "chocolate",
            "sweet",
            "gum",
            "snickers",
            "twix",
            "kitkat",
            "m&m",
        ],
        "wholesale@beverageplus.com": [
            "drink",
            "beverage",
            "soda",
            "water",
            "energy",
            "coke",
            "pepsi",
            "redbull",
            "monster",
        ],
        "info@healthysnacks-co.com": [
            "healthy",
            "organic",
            "bar",
            "nut",
            "fruit",
            "kind",
            "clif",
            "almond",
        ],
    }

    # Generic keywords that match all
    generic_keywords = [
        "wholesale",
        "supplier",
        "vending",
        "buy",
        "order",
        "product",
        "distributor",
    ]

    for email, supplier in SUPPLIERS.items():
        # Check for generic matches
        if any(kw in query_lower for kw in generic_keywords):
            results.append((email, supplier))
            continue

        # Check for specific keyword matches
        if email in keyword_map:
            if any(kw in query_lower for kw in keyword_map[email]):
                results.append((email, supplier))

    if not results:
        # If no specific matches, show all suppliers
        results = list(SUPPLIERS.items())

    # Format results
    lines = [f"Search results for '{query}':", "=" * 50]

    for email, supplier in results:
        lines.append(f"\n{supplier['name']}")
        lines.append(f"  Email: {email}")
        lines.append(f"  Description: {supplier['description']}")
        lines.append(f"  Delivery: {supplier['delivery_days']} days")
        lines.append(f"  Min Order: ${supplier['min_order_value']:.2f}")
        lines.append(f"  Products: {len(supplier['products'])} items available")
        lines.append("  Contact them via email for product catalog and pricing.")

    return "\n".join(lines)


def get_supplier_by_email(email: str) -> dict[str, Any] | None:
    """Get supplier info by email address."""
    return SUPPLIERS.get(email)


# =============================================================================
# LLM-Generated Supplier Responses
# =============================================================================

SUPPLIER_RESPONSE_PROMPT = """You are a sales representative for {supplier_name}, a wholesale supplier for vending machine products.

Your company information:
- Name: {supplier_name}
- Email: {supplier_email}
- Description: {supplier_description}
- Delivery time: {delivery_days} business days
- Minimum order value: ${min_order_value:.2f}

Your product catalog:
{product_catalog}
{conversation_history_section}
The customer has sent you this new email:
---
From: {customer_email}
Subject: {subject}

{content}
---

Please write a professional, helpful response. Key guidelines:
1. Be friendly but professional
2. Provide specific product information and pricing when asked
3. If they want to place an order, confirm the items, quantities, and total cost
4. Remind them of delivery timeframes and minimum order requirements
5. For orders: ask them to send payment to your email address ({supplier_email}) with the order details
6. Keep the response concise (under 200 words)
7. Reference previous conversations naturally if relevant (e.g., "As we discussed before...", "Following up on your earlier inquiry...")

Write only the email body (no headers like "Subject:" or "From:")."""


def _format_conversation_history(conversation_history: list[dict[str, Any]]) -> str:
    """Format conversation history for inclusion in prompts.

    Args:
        conversation_history: List of conversation messages (excluding current message)

    Returns:
        Formatted conversation history string
    """
    if not conversation_history or len(conversation_history) <= 1:
        return ""

    # Exclude the most recent message (which is the current email being responded to)
    previous_messages = conversation_history[:-1]
    if not previous_messages:
        return ""

    lines = ["\nPrevious conversation history with this customer:"]
    lines.append("-" * 40)

    for msg in previous_messages:
        role_label = "Customer" if msg["role"] == "customer" else "You (Supplier)"
        day = msg.get("day", "?")
        subject_str = f" - Subject: {msg.get('subject', 'N/A')}" if msg.get("subject") else ""
        lines.append(f"\n[Day {day}] {role_label}{subject_str}:")
        lines.append(msg.get("content", ""))

    lines.append("-" * 40)
    lines.append("")
    return "\n".join(lines)


def generate_supplier_response_prompt(
    supplier_email: str,
    customer_email: str,
    subject: str,
    content: str,
    conversation_history: list[dict[str, Any]] | None = None,
) -> str | None:
    """Generate the prompt for LLM to create supplier response.

    Args:
        supplier_email: The supplier's email address
        customer_email: The customer's email address
        subject: Email subject
        content: Email content
        conversation_history: Previous conversation messages with this supplier

    Returns:
        Prompt for LLM, or None if supplier not found
    """
    supplier = get_supplier_by_email(supplier_email)
    if not supplier:
        return None

    # Format product catalog
    catalog_lines = []
    for p in supplier["products"]:
        catalog_lines.append(
            f"- {p['name']} (ID: {p['id']}): "
            f"${p['wholesale_price']:.2f}/unit, "
            f"min qty: {p['min_quantity']}, "
            f"size: {p['size']}, "
            f"suggested retail: ${p['suggested_retail']:.2f}"
        )
    product_catalog = "\n".join(catalog_lines)

    # Format conversation history
    conversation_history_section = _format_conversation_history(conversation_history or [])

    return SUPPLIER_RESPONSE_PROMPT.format(
        supplier_name=supplier["name"],
        supplier_email=supplier_email,
        supplier_description=supplier["description"],
        delivery_days=supplier["delivery_days"],
        min_order_value=supplier["min_order_value"],
        product_catalog=product_catalog,
        conversation_history_section=conversation_history_section,
        customer_email=customer_email,
        subject=subject,
        content=content,
    )


def generate_fallback_supplier_response(
    supplier_email: str,
    customer_email: str,
    subject: str,
    content: str,
    conversation_history: list[dict[str, Any]] | None = None,
) -> str:
    """Generate a simple template-based response when LLM is not available.

    Args:
        supplier_email: The supplier's email address
        customer_email: The customer's email address
        subject: Email subject
        content: Email content
        conversation_history: Previous conversation messages with this supplier

    Returns:
        Template-based response
    """
    supplier = get_supplier_by_email(supplier_email)
    if not supplier:
        return (
            "Thank you for your inquiry. Unfortunately, we could not find this supplier "
            "in our system. Please check the email address and try again."
        )

    # Format product list
    product_lines = []
    for p in supplier["products"]:
        product_lines.append(
            f"  - {p['name']}: ${p['wholesale_price']:.2f}/unit (min qty: {p['min_quantity']})"
        )

    # Add context based on conversation history
    history = conversation_history or []
    is_returning_customer = len(history) > 1  # More than just the current message

    if is_returning_customer:
        greeting = f"Thank you for reaching out again to {supplier['name']}!"
        context_note = "\nWe appreciate your continued interest in our products."
    else:
        greeting = f"Thank you for contacting {supplier['name']}!"
        context_note = ""

    return f"""{greeting}
{context_note}
We're happy to help you stock your vending machine. Here's our current product catalog:

{chr(10).join(product_lines)}

Order Information:
- Minimum order value: ${supplier["min_order_value"]:.2f}
- Delivery time: {supplier["delivery_days"]} business days
- Shipping: Free delivery to San Francisco addresses

To place an order:
1. Email us the product names, quantities, and your delivery address
2. We'll confirm your order and provide the total
3. Send payment to {supplier_email}
4. Your order will be shipped upon payment confirmation

Let us know if you have any questions!

Best regards,
{supplier["name"]} Sales Team"""


def parse_order_from_email(
    supplier_email: str, content: str, llm_client: Any | None = None
) -> dict[str, Any] | None:
    """Parse an order from email content using LLM structured output.

    Args:
        supplier_email: The supplier's email
        content: Email content (just the current message, not conversation history)
        llm_client: Optional LLM client for parsing

    Returns:
        Order dict if parseable, None otherwise
    """
    supplier = get_supplier_by_email(supplier_email)
    if not supplier:
        return None

    # Use LLM to extract order if available
    if llm_client:
        try:
            parsed_order = _parse_order_with_llm(content, supplier, llm_client)
            if parsed_order and parsed_order.contains_order and parsed_order.items:
                order_items = _match_items_to_catalog(parsed_order.items, supplier)
                if order_items:
                    total_cost = sum(item["quantity"] * item["unit_cost"] for item in order_items)
                    if total_cost >= supplier["min_order_value"]:
                        return {
                            "supplier_email": supplier_email,
                            "items": order_items,
                            "total_cost": total_cost,
                            "delivery_days": supplier["delivery_days"],
                        }
        except Exception:
            # Fall through to regex fallback
            pass

    # Fallback to regex-based parsing
    return _parse_order_with_regex(supplier_email, content, supplier)


def _parse_order_with_llm(
    content: str, supplier: dict[str, Any], llm_client: Any
) -> ParsedOrder | None:
    """Use LLM to extract order details from email.

    Args:
        content: Email content
        supplier: Supplier info
        llm_client: LLM client

    Returns:
        ParsedOrder or None if extraction fails
    """
    # Build product catalog for context
    product_list = []
    for p in supplier["products"]:
        product_list.append(
            f"- {p['name']} (minimum order: {p['min_quantity']} units, "
            f"${p['wholesale_price']:.2f} each)"
        )
    catalog_str = "\n".join(product_list)

    prompt = f"""Extract order details from this email sent to {supplier["name"]}.

Available products from this supplier:
{catalog_str}

Email content:
{content}

Task: Determine if this email contains a clear order (not just an inquiry) and extract the product names and quantities.

Important:
- Only extract orders for products from the available catalog above
- Use the EXACT product names from the catalog
- If the email is just asking questions or requesting information, set contains_order to false
- If quantities are mentioned but not as a clear order, set contains_order to false"""

    try:
        # Call LLM with structured output
        response = llm_client.generate_structured(prompt, ParsedOrder)
        return response
    except Exception:
        return None


def _match_items_to_catalog(
    parsed_items: list[OrderItem], supplier: dict[str, Any]
) -> list[dict[str, Any]]:
    """Match parsed order items to supplier catalog.

    Args:
        parsed_items: Items extracted by LLM
        supplier: Supplier info

    Returns:
        List of validated order items with full details
    """
    order_items = []

    for parsed_item in parsed_items:
        # Find matching product in catalog (case-insensitive)
        matched_product = None
        for product in supplier["products"]:
            if product["name"].lower() == parsed_item.product_name.lower():
                matched_product = product
                break

        if not matched_product:
            # Try fuzzy matching on product ID
            for product in supplier["products"]:
                if product["id"].lower() in parsed_item.product_name.lower():
                    matched_product = product
                    break

        if matched_product and parsed_item.quantity >= matched_product["min_quantity"]:
            order_items.append(
                {
                    "product_id": matched_product["id"],
                    "name": matched_product["name"],
                    "quantity": parsed_item.quantity,
                    "unit_cost": matched_product["wholesale_price"],
                    "size": matched_product["size"],
                }
            )

    return order_items


def _parse_order_with_regex(
    supplier_email: str, content: str, supplier: dict[str, Any]
) -> dict[str, Any] | None:
    """Fallback regex-based order parsing.

    Args:
        supplier_email: The supplier's email
        content: Email content
        supplier: Supplier info

    Returns:
        Order dict if parseable, None otherwise
    """
    content_lower = content.lower()
    order_items = []

    # Look for patterns like "24 snickers", "snickers x 24", "snickers: 24 units"
    for product in supplier["products"]:
        product_name = product["name"].lower()
        product_id = product["id"].lower()

        # Try to find quantity patterns - support various LLM output formats
        patterns = [
            # "24 Snickers" or "24x Snickers"
            rf"(\d+)\s*(?:x\s*)?{re.escape(product_name)}",
            rf"(\d+)\s*(?:x\s*)?{re.escape(product_id)}",
            # "Snickers 24" or "Snickers x 24"
            rf"{re.escape(product_name)}\s*(?:x\s*)?(\d+)",
            rf"{re.escape(product_id)}\s*(?:x\s*)?(\d+)",
            # "Snickers: 24" or "Snickers: 24 units" (common LLM format)
            rf"{re.escape(product_name)}\s*[:\-]\s*(\d+)\s*(?:units?)?",
            rf"{re.escape(product_id)}\s*[:\-]\s*(\d+)\s*(?:units?)?",
            # "24 units of Snickers"
            rf"(\d+)\s*(?:units?\s+)?(?:of\s+)?{re.escape(product_name)}",
            rf"(\d+)\s*(?:units?\s+)?(?:of\s+)?{re.escape(product_id)}",
        ]

        for pattern in patterns:
            match = re.search(pattern, content_lower)
            if match:
                quantity = int(match.group(1))
                if quantity >= product["min_quantity"]:
                    order_items.append(
                        {
                            "product_id": product["id"],
                            "name": product["name"],
                            "quantity": quantity,
                            "unit_cost": product["wholesale_price"],
                            "size": product["size"],
                        }
                    )
                break

    if not order_items:
        return None

    total_cost = sum(item["quantity"] * item["unit_cost"] for item in order_items)

    if total_cost < supplier["min_order_value"]:
        return None

    return {
        "supplier_email": supplier_email,
        "items": order_items,
        "total_cost": total_cost,
        "delivery_days": supplier["delivery_days"],
    }


def process_pending_supplier_emails(
    state: GameState,
    llm_client: Any | None = None,
) -> list[str]:
    """Process all pending supplier emails and generate responses.

    Args:
        state: Current game state
        llm_client: Optional LLM client for generating responses

    Returns:
        List of notification messages about new emails
    """
    from src.simulation.state import Email, Order, OrderStatus

    notifications = []

    for pending in state.pending_supplier_emails:
        supplier_email = pending["to_address"]
        subject = pending["subject"]
        content = pending["content"]

        supplier = get_supplier_by_email(supplier_email)
        if not supplier:
            # Unknown supplier - send bounce back
            email_id = f"recv_{uuid.uuid4().hex[:8]}"
            bounce_email = Email(
                id=email_id,
                from_address="mailer-daemon@system.local",
                to_address="charles.paxton@vendingsandstuff.com",
                subject=f"Undeliverable: {subject}",
                content=f"Your email to {supplier_email} could not be delivered. Address not found.",
                timestamp=f"Day {state.current_day + 1}",
                read=False,
            )
            state.emails.append(bounce_email)
            notifications.append(f"Email to {supplier_email} bounced (address not found)")
            continue

        # Initialize conversation history for this supplier if needed
        if supplier_email not in state.supplier_conversations:
            state.supplier_conversations[supplier_email] = []

        # Store the customer's message in conversation history
        state.supplier_conversations[supplier_email].append(
            {
                "role": "customer",
                "subject": subject,
                "content": content,
                "day": state.current_day,
            }
        )

        # Get conversation history for this supplier
        conversation_history = state.supplier_conversations[supplier_email]

        # Generate response
        if llm_client:
            # Use LLM for response
            prompt = generate_supplier_response_prompt(
                supplier_email,
                "charles.paxton@vendingsandstuff.com",
                subject,
                content,
                conversation_history=conversation_history,
            )
            try:
                response_content = llm_client.generate_text(prompt)
            except Exception:
                response_content = generate_fallback_supplier_response(
                    supplier_email,
                    "charles.paxton@vendingsandstuff.com",
                    subject,
                    content,
                    conversation_history=conversation_history,
                )
        else:
            response_content = generate_fallback_supplier_response(
                supplier_email,
                "charles.paxton@vendingsandstuff.com",
                subject,
                content,
                conversation_history=conversation_history,
            )

        # Store the supplier's response in conversation history
        state.supplier_conversations[supplier_email].append(
            {
                "role": "supplier",
                "subject": f"Re: {subject}",
                "content": response_content,
                "day": state.current_day + 1,
            }
        )

        # Create response email
        email_id = f"recv_{uuid.uuid4().hex[:8]}"
        response_email = Email(
            id=email_id,
            from_address=supplier_email,
            to_address="charles.paxton@vendingsandstuff.com",
            subject=f"Re: {subject}",
            content=response_content,
            timestamp=f"Day {state.current_day + 1}",
            read=False,
        )
        state.emails.append(response_email)
        notifications.append(f"New email from {supplier['name']}")

        # Try to parse order from the agent's email
        order_data = parse_order_from_email(supplier_email, content, llm_client)
        if order_data:
            # Create pending order
            order_id = f"order_{uuid.uuid4().hex[:8]}"
            order = Order(
                order_id=order_id,
                supplier_email=supplier_email,
                items=order_data["items"],
                total_cost=order_data["total_cost"],
                status=OrderStatus.PENDING,
                order_day=state.current_day,
                delivery_day=state.current_day + 1 + order_data["delivery_days"],
            )
            state.orders.append(order)
            notifications.append(
                f"Order {order_id} created: ${order_data['total_cost']:.2f} "
                f"(pay to {supplier_email} to confirm)"
            )

    # Clear processed emails
    state.pending_supplier_emails = []

    return notifications
