"""Calendar protocol implementation for magentic-marketplace."""

import uuid
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from magentic_marketplace.platform.database.base import BaseDatabaseController
from magentic_marketplace.platform.protocol.base import BaseMarketplaceProtocol
from magentic_marketplace.platform.shared.models import (
    ActionExecutionRequest,
    ActionExecutionResult,
    AgentProfile,
    BaseAction,
)

from .actions import (
    AddEvent,
    DeleteEvent,
    GetEventDetails,
    GetEvents,
    UpdateEvent,
)
from .entities import Event, TimeRange


class CalendarProtocol(BaseMarketplaceProtocol):
    """Calendar protocol for managing events (standalone and recurring).

    This protocol stores calendar data by executing actions that get stored in the
    actions table. Calendar state is reconstructed by querying past AddEvent actions.
    """

    def __init__(self):
        """Initialize the calendar protocol."""
        from .utils.query_service import CalendarQueryService

        self._actions = [
            GetEvents,
            GetEventDetails,
            AddEvent,
            UpdateEvent,
            DeleteEvent,
        ]
        self._query_service = CalendarQueryService()

    def get_actions(self) -> Sequence[type[BaseAction]]:
        """Get available calendar actions."""
        return self._actions

    async def initialize(self, database: BaseDatabaseController) -> None:
        """Initialize calendar protocol (no custom tables needed)."""
        # No custom tables - we use the actions table
        pass

    async def execute_action(
        self,
        *,
        agent: AgentProfile,
        action: ActionExecutionRequest,
        database: BaseDatabaseController,
    ) -> ActionExecutionResult:
        """Execute a calendar action."""
        from .actions import (
            AddEvent,
            DeleteEvent,
            GetEventDetails,
            GetEvents,
            UpdateEvent,
        )

        action_name = action.name
        params = action.parameters

        try:
            if action_name == GetEvents.get_name():
                result = await self._get_events(
                    agent_id=agent.id,
                    start_datetime=params["start_datetime"],
                    end_datetime=params["end_datetime"],
                    database=database,
                )
                return ActionExecutionResult(content=result)

            elif action_name == GetEventDetails.get_name():
                result = await self._get_event_details(
                    agent_id=agent.id,
                    event_id=params["event_id"],
                    database=database,
                )
                return ActionExecutionResult(content=result)

            elif action_name == AddEvent.get_name():
                event_id = str(uuid.uuid4())
                event = self._create_event_from_params(
                    event_id=event_id,
                    organizer_id=agent.id,
                    params=params,
                )
                is_recurring = event.is_recurring
                return ActionExecutionResult(
                    content=event.model_dump(),
                    metadata={"event_id": event_id, "is_recurring": is_recurring},
                )

            elif action_name == UpdateEvent.get_name():
                from .entities import Modification
                from .utils.event_utils import parse_instance_id

                event_id = params["event_id"]

                # Check if this is a series instance update
                parsed = parse_instance_id(event_id)
                if parsed:
                    parent_id, instance_date_str = parsed

                    # Validate that parent event exists and agent is the organizer
                    parent_event = await self._get_event_by_id(parent_id, database)
                    if not parent_event:
                        return ActionExecutionResult(
                            content={"error": f"Parent event not found: {parent_id}"},
                            is_error=True,
                        )
                    if parent_event.organizer_id != agent.id:
                        return ActionExecutionResult(
                            content={"error": "Only the organizer can update event instances"},
                            is_error=True,
                        )
                    if not parent_event.is_recurring:
                        return ActionExecutionResult(
                            content={"error": f"Event {parent_id} is not a recurring event"},
                            is_error=True,
                        )

                    # Create modification from update parameters
                    modification = Modification(
                        is_cancelled=False,
                        new_start=(
                            datetime.fromisoformat(params["start_datetime"])
                            if params.get("start_datetime")
                            else None
                        ),
                        new_end=(
                            datetime.fromisoformat(params["end_datetime"])
                            if params.get("end_datetime")
                            else None
                        ),
                        title_override=params.get("title"),
                        description_override=params.get("description"),
                        participants_override=params.get("participants"),
                    )

                    return ActionExecutionResult(
                        content={"event_id": event_id, "updates": params},
                        metadata={
                            "type": "instance_modification",
                            "parent_id": parent_id,
                            "instance_date": instance_date_str,
                            "modification": modification.model_dump(),
                        },
                    )

                # Regular event or series parent update - validate event exists
                event = await self._get_event_by_id(event_id, database)
                if not event:
                    return ActionExecutionResult(
                        content={"error": f"Event not found: {event_id}"},
                        is_error=True,
                    )
                if event.organizer_id != agent.id:
                    return ActionExecutionResult(
                        content={"error": "Only the organizer can update events"},
                        is_error=True,
                    )

                return ActionExecutionResult(
                    content={"event_id": event_id, "updates": params},
                    metadata={"type": "event_update"},
                )

            elif action_name == DeleteEvent.get_name():
                from .utils.event_utils import parse_instance_id

                event_id = params["event_id"]

                # Check if this is a series instance cancellation
                parsed = parse_instance_id(event_id)
                if parsed:
                    parent_id, instance_date_str = parsed

                    # Validate that parent event exists and agent is the organizer
                    parent_event = await self._get_event_by_id(parent_id, database)
                    if not parent_event:
                        return ActionExecutionResult(
                            content={"error": f"Parent event not found: {parent_id}"},
                            is_error=True,
                        )
                    if parent_event.organizer_id != agent.id:
                        return ActionExecutionResult(
                            content={"error": "Only the organizer can delete event instances"},
                            is_error=True,
                        )
                    if not parent_event.is_recurring:
                        return ActionExecutionResult(
                            content={"error": f"Event {parent_id} is not a recurring event"},
                            is_error=True,
                        )

                    return ActionExecutionResult(
                        content={"event_id": event_id, "cancelled": True},
                        metadata={
                            "type": "instance_cancellation",
                            "parent_id": parent_id,
                            "instance_date": instance_date_str,
                        },
                    )

                # Regular event or series parent deletion - validate event exists
                event = await self._get_event_by_id(event_id, database)
                if not event:
                    return ActionExecutionResult(
                        content={"error": f"Event not found: {event_id}"},
                        is_error=True,
                    )
                if event.organizer_id != agent.id:
                    return ActionExecutionResult(
                        content={"error": "Only the organizer can delete events"},
                        is_error=True,
                    )

                return ActionExecutionResult(
                    content={"event_id": event_id, "deleted": True},
                    metadata={"type": "event_delete"},
                )

            else:
                return ActionExecutionResult(
                    content={"error": f"Unknown action: {action_name}"},
                    is_error=True,
                )

        except Exception as e:
            return ActionExecutionResult(
                content={"error": str(e)},
                is_error=True,
            )

    def _create_event_from_params(
        self,
        event_id: str,
        organizer_id: str,
        params: dict[str, Any],
    ) -> Event:
        """Create an Event from action parameters (standalone or recurring)."""
        from .entities import RecurrenceRule

        participants = params.get("participants", [])
        if organizer_id not in participants:
            participants.append(organizer_id)

        # Check if this is a recurring event
        recurrence = params.get("recurrence")
        recurrence_rule = RecurrenceRule.model_validate(recurrence) if recurrence else None

        return Event(
            id=event_id,
            recurrence_rule=recurrence_rule,
            organizer_id=organizer_id,
            start_datetime=datetime.fromisoformat(params["start_datetime"]),
            end_datetime=datetime.fromisoformat(params["end_datetime"]),
            title=params["title"],
            description=params["description"],
            participants=participants,
            instance_modifications=None if recurrence_rule else None,
        )

    async def _get_events(
        self,
        agent_id: str,
        start_datetime: str,
        end_datetime: str,
        database: BaseDatabaseController,
    ) -> list[dict[str, Any]]:
        """Get all events for an agent in a datetime range by querying actions table.

        Returns events where the agent is either:
        1. The organizer (created the event)
        2. A participant (invited to the event)
        """
        start = datetime.fromisoformat(start_datetime)
        end = datetime.fromisoformat(end_datetime)
        range_obj = TimeRange(start=start, end=end)

        # Use query service to fetch and expand events
        events = await self._query_service.get_events_for_agent(
            agent_id,
            range_obj,
            database,
        )

        return [e.model_dump() for e in events]

    async def _get_event_by_id(
        self,
        event_id: str,
        database: BaseDatabaseController,
    ) -> Event | None:
        """Retrieve an event by ID from the database.

        Args:
            event_id: Event ID to retrieve
            database: Database controller

        Returns:
            Event if found, None otherwise
        """
        from magentic_marketplace.platform.database.queries import actions as action_queries

        # Query all AddEvent actions
        query = action_queries.request_name(value="AddEvent", operator="=")
        add_event_actions = await database.actions.find(query)

        # Search for the event with matching ID
        for action_row in add_event_actions:
            event_data = action_row.data.result.content
            if event_data.get("id") == event_id:
                return Event.model_validate(event_data)

        return None

    async def _get_event_details(
        self,
        agent_id: str,
        event_id: str,
        database: BaseDatabaseController,
    ) -> dict[str, Any] | None:
        """Get details of a specific event."""
        # Query for the specific event
        # For now, simplified implementation
        return {"event_id": event_id, "details": "Not yet fully implemented"}
