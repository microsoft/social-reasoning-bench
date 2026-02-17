"""Utility functions for event operations."""

from datetime import date


def parse_instance_id(event_id: str) -> tuple[str, str] | None:
    """Parse an instance ID to extract parent ID and instance date.

    Args:
        event_id: Event ID that may be an instance (format: parent_id_YYYY-MM-DD)

    Returns:
        Tuple of (parent_id, instance_date_str) if valid instance ID, None otherwise
    """
    # Check if this looks like an instance ID (contains underscore with 10-char date)
    if "_" not in event_id or len(event_id.split("_")[-1]) != 10:
        return None

    # Parse instance ID to extract parent_id and date
    parts = event_id.rsplit("_", 1)
    parent_id = parts[0]
    instance_date_str = parts[1]

    # Validate date format
    try:
        date.fromisoformat(instance_date_str)
        return parent_id, instance_date_str
    except ValueError:
        return None
