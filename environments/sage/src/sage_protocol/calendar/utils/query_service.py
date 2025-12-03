"""Service for querying calendar data from the marketplace database."""

from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.database.queries import actions as action_queries

from ..entities import Event, TimeRange
from .series_expansion import SeriesExpander


class CalendarQueryService:
    """Handles calendar data querying and reconstruction from action history.

    This service encapsulates all logic for:
    - Querying the actions table for calendar data
    - Filtering events by participant and date range
    - Expanding recurring events into individual instances
    - Sorting and aggregating results
    """

    async def get_events_for_agent(
        self,
        agent_id: str,
        date_range: TimeRange,
        database: BaseDatabaseController,
    ) -> list[Event]:
        """Query all events for an agent in a date range.

        Returns events where the agent is either:
        1. The organizer (created the event)
        2. A participant (invited to the event)

        Args:
            agent_id: The agent's ID
            date_range: Date range to query
            database: Database controller

        Returns:
            List of events sorted by start time
        """
        # 1. Load all AddEvent actions to get parent events
        query = action_queries.request_name(value="AddEvent", operator="=")
        add_event_actions = await database.actions.find(query)

        # Build events map for efficient lookups
        events_map: dict[str, Event] = {}
        for action_row in add_event_actions:
            event_data = action_row.data.result.content
            event = Event.model_validate(event_data)
            events_map[event.id] = event

        # 2. Apply action history (modifications and cancellations) to parent events
        await self._apply_action_history(events_map, database)

        # 3. Expand series and filter by participant and date range
        events: list[Event] = []
        for event in events_map.values():
            # Only include if agent is a participant
            if agent_id not in event.participants:
                continue

            # Add event if its time range overlaps with query range
            event_range = TimeRange(start=event.start_datetime, end=event.end_datetime)
            if date_range.overlaps(event_range):
                events.append(event)

            # If recurring, also expand future instances (excluding first occurrence)
            if event.is_recurring:
                expanded_events = SeriesExpander.expand_event_to_instances(
                    event,
                    date_range,
                    include_cancelled=False,
                    skip_first_occurrence=True,
                )
                events.extend(expanded_events)

        # Sort by start time
        events.sort(key=lambda e: e.start_datetime)

        return events

    async def _apply_action_history(
        self,
        events_map: dict[str, Event],
        database: BaseDatabaseController,
    ) -> None:
        """Apply UpdateEvent and DeleteEvent actions to reconstruct event state.

        Args:
            events_map: Map of event_id to Event (modified in place)
            database: Database controller
        """
        from datetime import date

        from ..entities import Modification

        # Apply UpdateEvent modifications
        update_query = action_queries.request_name(value="UpdateEvent", operator="=")
        update_actions = await database.actions.find(update_query)

        for action_row in update_actions:
            metadata = action_row.data.result.metadata
            if metadata and metadata.get("type") == "instance_modification":
                parent_id = metadata.get("parent_id")
                instance_date_str = metadata.get("instance_date")
                mod_data = metadata.get("modification")

                if parent_id and instance_date_str and mod_data:
                    # Find parent event
                    parent_event = events_map.get(parent_id)
                    if parent_event and parent_event.is_recurring:
                        # Parse instance date and apply modification
                        instance_date = date.fromisoformat(instance_date_str)
                        modification = Modification.model_validate(mod_data)
                        parent_event.set_modification(instance_date, modification)

        # Apply DeleteEvent cancellations
        delete_query = action_queries.request_name(value="DeleteEvent", operator="=")
        delete_actions = await database.actions.find(delete_query)

        for action_row in delete_actions:
            metadata = action_row.data.result.metadata
            if metadata and metadata.get("type") == "instance_cancellation":
                parent_id = metadata.get("parent_id")
                instance_date_str = metadata.get("instance_date")

                if parent_id and instance_date_str:
                    # Find parent event
                    parent_event = events_map.get(parent_id)
                    if parent_event and parent_event.is_recurring:
                        # Parse instance date and mark as cancelled
                        instance_date = date.fromisoformat(instance_date_str)
                        cancellation = Modification(is_cancelled=True)
                        parent_event.set_modification(instance_date, cancellation)
