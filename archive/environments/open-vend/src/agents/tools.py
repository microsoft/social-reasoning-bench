"""Tool implementations for the OpenVend agent."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.simulation.state import GameState

from src.simulation.state import (
    Email,
    OrderStatus,
)

# =============================================================================
# Memory Tools
# =============================================================================


def write_value(state: GameState, key: str, value: str) -> str:
    """Store a value in the agent's key-value memory.

    Args:
        state: Current game state
        key: The key to store the value under
        value: The value to store

    Returns:
        Confirmation message
    """
    state.memory[key] = value
    return f"Stored value under key '{key}'."


def get_value(state: GameState, key: str) -> str:
    """Retrieve a value from the agent's key-value memory.

    Args:
        state: Current game state
        key: The key to retrieve

    Returns:
        The stored value or error message if key not found
    """
    if key in state.memory:
        return state.memory[key]
    return f"Key '{key}' not found in memory."


def get_keys(state: GameState) -> str:
    """Get all keys stored in the agent's memory.

    Args:
        state: Current game state

    Returns:
        List of all keys or message if memory is empty
    """
    if not state.memory:
        return "Memory is empty. No keys stored."
    keys = list(state.memory.keys())
    return f"Stored keys: {', '.join(keys)}"


# =============================================================================
# Email Tools
# =============================================================================


def send_email(state: GameState, to_address: str, subject: str, content: str) -> str:
    """Send an email to a specific address.

    Args:
        state: Current game state
        to_address: Recipient email address
        subject: Email subject line
        content: Email body content

    Returns:
        Confirmation with email ID
    """
    email_id = f"sent_{uuid.uuid4().hex[:8]}"
    timestamp = f"Day {state.current_day}"

    # Store the sent email
    email = Email(
        id=email_id,
        from_address="charles.paxton@vendingsandstuff.com",
        to_address=to_address,
        subject=subject,
        content=content,
        timestamp=timestamp,
        read=True,  # Sent emails are marked as read
    )
    state.emails.append(email)

    # Queue for supplier response processing at end of day
    state.pending_supplier_emails.append(
        {"to_address": to_address, "subject": subject, "content": content, "email_id": email_id}
    )

    return f"Email sent to {to_address}. Email ID: {email_id}. Responses will arrive overnight."


def read_email(state: GameState, email_id: str) -> str:
    """Read a specific email by ID.

    Args:
        state: Current game state
        email_id: The ID of the email to read

    Returns:
        Email content or error if not found
    """
    for email in state.emails:
        if email.id == email_id:
            email.read = True
            return (
                f"From: {email.from_address}\n"
                f"To: {email.to_address}\n"
                f"Subject: {email.subject}\n"
                f"Date: {email.timestamp}\n"
                f"---\n"
                f"{email.content}"
            )
    return f"Email with ID '{email_id}' not found."


def read_email_inbox(state: GameState, show_all: bool = False) -> str:
    """Get emails from the inbox.

    Args:
        state: Current game state
        show_all: If True, show all emails. If False, show only unread.

    Returns:
        Summary of emails in inbox
    """
    if show_all:
        emails = state.emails
    else:
        emails = [e for e in state.emails if not e.read]

    if not emails:
        if show_all:
            return "Your inbox is empty."
        return "No unread emails."

    lines = []
    for email in emails:
        status = "" if email.read else "[UNREAD] "
        lines.append(
            f"{status}ID: {email.id} | From: {email.from_address} | Subject: {email.subject}"
        )

    header = "All emails:" if show_all else "Unread emails:"
    return f"{header}\n" + "\n".join(lines)


# =============================================================================
# Search Tools
# =============================================================================


def search_internet(state: GameState, query: str) -> str:
    """Search the internet for suppliers and products.

    NOTE: This is a simulated search that returns predefined supplier information.

    Args:
        state: Current game state
        query: Search query

    Returns:
        Search results with supplier information
    """
    # Import here to avoid circular dependency
    from src.simulation.suppliers import search_suppliers

    return search_suppliers(query)


# =============================================================================
# Financial Tools
# =============================================================================


def get_money_balance(state: GameState) -> str:
    """Get the current bank account balance.

    Args:
        state: Current game state

    Returns:
        Current balance information
    """
    return (
        f"Bank Account Balance: ${state.bank_balance:.2f}\n"
        f"Cash in Machine: ${state.machine_cash:.2f}\n"
        f"Total Liquid Assets: ${state.bank_balance + state.machine_cash:.2f}"
    )


def send_money(state: GameState, recipient: str, amount: float, memo: str = "") -> str:
    """Send money to a recipient (typically for order payment).

    Args:
        state: Current game state
        recipient: Email/identifier of recipient
        amount: Amount to send
        memo: Optional payment memo/reference

    Returns:
        Confirmation or error message
    """
    if amount <= 0:
        return "Error: Amount must be positive."

    if amount > state.bank_balance:
        return f"Error: Insufficient funds. Balance: ${state.bank_balance:.2f}, Requested: ${amount:.2f}"

    state.bank_balance -= amount

    # Check if this payment is for a pending order
    for order in state.orders:
        if order.status == OrderStatus.PENDING and order.supplier_email == recipient:
            if abs(order.total_cost - amount) < 0.01:  # Match payment to order
                order.status = OrderStatus.PAID
                return (
                    f"Payment of ${amount:.2f} sent to {recipient}.\n"
                    f"Order {order.order_id} marked as paid. Delivery expected on day {order.delivery_day}.\n"
                    f"New balance: ${state.bank_balance:.2f}"
                )

    return f"Payment of ${amount:.2f} sent to {recipient}. Memo: {memo}\nNew balance: ${state.bank_balance:.2f}"


# =============================================================================
# Warehouse/Storage Tools
# =============================================================================


def check_storage_quantities(state: GameState) -> str:
    """Check the quantities of items in warehouse storage.

    Args:
        state: Current game state

    Returns:
        Summary of warehouse inventory quantities
    """
    if not state.warehouse:
        return "Warehouse is empty."

    total_items = state.get_warehouse_total_items()
    lines = [f"Warehouse Inventory ({total_items}/{state.max_warehouse_capacity} capacity):"]

    for product_id, item in state.warehouse.items():
        lines.append(
            f"  {item.name}: {item.quantity} units (${item.unit_cost:.2f}/unit, {item.size.value})"
        )

    return "\n".join(lines)


def list_storage_products(state: GameState) -> str:
    """Get detailed information about products in storage.

    Args:
        state: Current game state

    Returns:
        Detailed product information
    """
    if not state.warehouse:
        return "Warehouse is empty. No products in storage."

    lines = ["Products in Storage:"]
    for product_id, item in state.warehouse.items():
        total_value = item.quantity * item.unit_cost
        lines.append(
            f"\nProduct ID: {product_id}\n"
            f"  Name: {item.name}\n"
            f"  Size: {item.size.value}\n"
            f"  Quantity: {item.quantity}\n"
            f"  Unit Cost: ${item.unit_cost:.2f}\n"
            f"  Total Value: ${total_value:.2f}"
        )

    return "\n".join(lines)


# =============================================================================
# Vending Machine Tools
# =============================================================================


def view_machine_inventory(state: GameState) -> str:
    """View the current inventory in the vending machine.

    Args:
        state: Current game state

    Returns:
        Current machine inventory status
    """
    lines = ["Vending Machine Inventory:"]
    lines.append("=" * 40)

    # Group by rows
    for row in range(4):
        row_type = "SMALL" if row < 2 else "LARGE"
        lines.append(f"\nRow {row + 1} ({row_type}):")
        for col in range(3):
            slot_id = row * 3 + col
            slot = state.machine_slots[slot_id]
            if slot.product_id:
                lines.append(
                    f"Slot {slot_id}: {slot.product_name} - "
                    f"{slot.quantity}/{slot.capacity} @ ${slot.price:.2f}"
                )
            else:
                lines.append(f"Slot {slot_id}: [EMPTY]")

    lines.append(f"\nCash in machine: ${state.machine_cash:.2f}")
    return "\n".join(lines)


def restock_machine(state: GameState, product_id: str, slot_id: int, quantity: int) -> str:
    """Load items from warehouse into a vending machine slot.

    Args:
        state: Current game state
        product_id: ID of product to load
        slot_id: Which slot to load (0-11)
        quantity: How many items to load

    Returns:
        Confirmation or error message
    """
    # Validate slot
    if slot_id < 0 or slot_id >= 12:
        return f"Error: Invalid slot ID {slot_id}. Must be 0-11."

    slot = state.machine_slots[slot_id]

    # Check if product exists in warehouse
    if product_id not in state.warehouse:
        return f"Error: Product '{product_id}' not found in warehouse."

    warehouse_item = state.warehouse[product_id]

    # Check size compatibility
    if warehouse_item.size != slot.size:
        return (
            f"Error: Product size mismatch. Product is {warehouse_item.size.value}, "
            f"but slot {slot_id} is for {slot.size.value} items."
        )

    # Check if slot has different product
    if slot.product_id and slot.product_id != product_id:
        return (
            f"Error: Slot {slot_id} already contains {slot.product_name}. "
            f"Clear it first or choose a different slot."
        )

    # Check warehouse quantity
    if quantity > warehouse_item.quantity:
        return (
            f"Error: Not enough in warehouse. Requested: {quantity}, "
            f"Available: {warehouse_item.quantity}"
        )

    # Check slot capacity
    space_available = slot.capacity - slot.quantity
    if quantity > space_available:
        return (
            f"Error: Not enough space in slot. Requested: {quantity}, "
            f"Available space: {space_available}"
        )

    # Perform the restock
    warehouse_item.quantity -= quantity
    slot.product_id = product_id
    slot.product_name = warehouse_item.name
    slot.quantity += quantity

    # If price not set, suggest setting it
    price_note = ""
    if slot.price == 0:
        price_note = " Note: Price not set for this slot. Use set_prices to set a price."

    # Clean up empty warehouse items
    if warehouse_item.quantity == 0:
        del state.warehouse[product_id]

    return (
        f"Loaded {quantity} units of {warehouse_item.name} into slot {slot_id}. "
        f"Slot now has {slot.quantity}/{slot.capacity} units.{price_note}"
    )


def set_prices(state: GameState, prices: dict[int, float] | list[dict]) -> str:
    """Set prices for vending machine slots.

    Args:
        state: Current game state
        prices: Dictionary mapping slot_id to price, or list of {slot_id, price} objects

    Returns:
        Confirmation of price changes
    """
    changes = []
    errors = []

    # Normalize prices to list of (slot_id, price) tuples
    price_items: list[tuple[int, float]] = []

    if isinstance(prices, list):
        # Handle list format: [{"slot_id": 0, "price": 1.25}, ...]
        for item in prices:
            if isinstance(item, dict) and "slot_id" in item and "price" in item:
                price_items.append((int(item["slot_id"]), float(item["price"])))
            else:
                errors.append(f"Invalid price item format: {item}")
    elif isinstance(prices, dict):
        # Handle dict format: {0: 1.25, "1": 1.50, ...}
        for slot_id, price in prices.items():
            try:
                price_items.append((int(slot_id), float(price)))
            except (ValueError, TypeError):
                errors.append(f"Invalid slot_id or price: {slot_id}={price}")
    else:
        return f"Error: prices must be a dict or list, got {type(prices).__name__}"

    for slot_id, price in price_items:
        if slot_id < 0 or slot_id >= 12:
            errors.append(f"Invalid slot ID: {slot_id}")
            continue

        if price < 0:
            errors.append(f"Slot {slot_id}: Price cannot be negative")
            continue

        slot = state.machine_slots[slot_id]
        old_price = slot.price
        slot.price = price
        changes.append(f"Slot {slot_id}: ${old_price:.2f} -> ${price:.2f}")

    result_parts = []
    if changes:
        result_parts.append("Price changes:\n" + "\n".join(changes))
    if errors:
        result_parts.append("Errors:\n" + "\n".join(errors))

    return "\n\n".join(result_parts) if result_parts else "No price changes made."


def collect_cash(state: GameState) -> str:
    """Collect cash from the vending machine and deposit to bank account.

    Args:
        state: Current game state

    Returns:
        Confirmation of cash collected
    """
    if state.machine_cash <= 0:
        return "No cash to collect from the machine."

    collected = state.machine_cash
    state.bank_balance += collected
    state.machine_cash = 0

    return (
        f"Collected ${collected:.2f} from the vending machine.\n"
        f"New bank balance: ${state.bank_balance:.2f}"
    )


# =============================================================================
# Lifecycle Tools
# =============================================================================


def wait_until_next_day(state: GameState) -> str:
    """Advance the simulation to the next day.

    This triggers:
    1. End-of-day sales calculation
    2. Daily fee deduction
    3. Supplier email responses
    4. Order deliveries

    Args:
        state: Current game state

    Returns:
        Summary of what happened overnight
    """
    # Import here to avoid circular dependency
    from src.simulation.economy import process_end_of_day

    return process_end_of_day(state)


# =============================================================================
# Tool Registry
# =============================================================================


TOOLS: dict[str, dict[str, Any]] = {
    "write_value": {
        "function": write_value,
        "description": "Store a value in your personal key-value memory for later retrieval.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to store the value under"},
                "value": {"type": "string", "description": "The value to store"},
            },
            "required": ["key", "value"],
        },
    },
    "get_value": {
        "function": get_value,
        "description": "Retrieve a value from your personal key-value memory.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to retrieve"},
            },
            "required": ["key"],
        },
    },
    "get_keys": {
        "function": get_keys,
        "description": "Get a list of all keys stored in your memory.",
        "parameters": {"type": "object", "properties": {}},
    },
    "send_email": {
        "function": send_email,
        "description": "Send an email. Use this to contact suppliers, place orders, or communicate.",
        "parameters": {
            "type": "object",
            "properties": {
                "to_address": {"type": "string", "description": "Recipient email address"},
                "subject": {"type": "string", "description": "Email subject line"},
                "content": {"type": "string", "description": "Email body content"},
            },
            "required": ["to_address", "subject", "content"],
        },
    },
    "read_email": {
        "function": read_email,
        "description": "Read a specific email by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_id": {"type": "string", "description": "The ID of the email to read"},
            },
            "required": ["email_id"],
        },
    },
    "read_email_inbox": {
        "function": read_email_inbox,
        "description": "View your email inbox. By default shows unread emails only.",
        "parameters": {
            "type": "object",
            "properties": {
                "show_all": {
                    "type": "boolean",
                    "description": "If true, show all emails including read ones",
                    "default": False,
                },
            },
        },
    },
    "search_internet": {
        "function": search_internet,
        "description": "Search the internet for suppliers and vending machine products.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
    },
    "get_money_balance": {
        "function": get_money_balance,
        "description": "Check your current bank account balance and cash in the machine.",
        "parameters": {"type": "object", "properties": {}},
    },
    "send_money": {
        "function": send_money,
        "description": "Send money to pay for orders or other expenses. This is irreversible.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {"type": "string", "description": "Email/identifier of recipient"},
                "amount": {"type": "number", "description": "Amount to send in dollars"},
                "memo": {"type": "string", "description": "Optional payment memo/reference"},
            },
            "required": ["recipient", "amount"],
        },
    },
    "check_storage_quantities": {
        "function": check_storage_quantities,
        "description": "Check the quantities of items in your warehouse storage.",
        "parameters": {"type": "object", "properties": {}},
    },
    "list_storage_products": {
        "function": list_storage_products,
        "description": "Get detailed information about all products in your warehouse.",
        "parameters": {"type": "object", "properties": {}},
    },
    "view_machine_inventory": {
        "function": view_machine_inventory,
        "description": "View the current inventory and prices in the vending machine.",
        "parameters": {"type": "object", "properties": {}},
    },
    "restock_machine": {
        "function": restock_machine,
        "description": "Load items from your warehouse into a vending machine slot.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "ID of product to load"},
                "slot_id": {
                    "type": "integer",
                    "description": "Slot to load (0-5 small, 6-11 large)",
                },
                "quantity": {"type": "integer", "description": "Number of items to load"},
            },
            "required": ["product_id", "slot_id", "quantity"],
        },
    },
    "set_prices": {
        "function": set_prices,
        "description": "Set or update prices for vending machine slots.",
        "parameters": {
            "type": "object",
            "properties": {
                "prices": {
                    "type": "object",
                    "description": "Dictionary mapping slot_id (0-11) to price in dollars",
                    "additionalProperties": {"type": "number"},
                },
            },
            "required": ["prices"],
        },
    },
    "collect_cash": {
        "function": collect_cash,
        "description": "Collect cash from the vending machine and deposit to your bank account.",
        "parameters": {"type": "object", "properties": {}},
    },
    "wait_until_next_day": {
        "function": wait_until_next_day,
        "description": "End the current day and advance to the next day. Sales are processed overnight.",
        "parameters": {"type": "object", "properties": {}},
    },
}


def execute_tool(state: GameState, tool_name: str, arguments: dict[str, Any], logger=None) -> str:
    """Execute a tool by name with given arguments.

    Args:
        state: Current game state
        tool_name: Name of the tool to execute
        arguments: Tool arguments
        logger: Optional logger to record tool calls

    Returns:
        Tool result string
    """
    if tool_name not in TOOLS:
        return f"Error: Unknown tool '{tool_name}'"

    tool_func = TOOLS[tool_name]["function"]

    # Increment tool call counter
    state.tool_calls_today += 1

    # Check daily limit (except for wait_until_next_day which resets it)
    if tool_name != "wait_until_next_day":
        if state.tool_calls_today > state.max_tool_calls_per_day:
            return (
                f"Error: Daily tool call limit reached ({state.max_tool_calls_per_day}). "
                f"Use wait_until_next_day to advance to the next day."
            )

    try:
        result = tool_func(state, **arguments)

        # Log tool call if logger provided
        if logger:
            logger.log_tool_call(
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                day=state.current_day,
            )

        return result
    except TypeError as e:
        return f"Error: Invalid arguments for {tool_name}: {e}"
    except Exception as e:
        return f"Error executing {tool_name}: {e}"


def get_tool_definitions() -> list[dict[str, Any]]:
    """Get tool definitions in OpenAI function calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
        }
        for name, tool in TOOLS.items()
    ]
