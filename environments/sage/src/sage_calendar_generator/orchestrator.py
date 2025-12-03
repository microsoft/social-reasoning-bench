"""Main orchestrator for the LLM-based scenario generation pipeline."""

import logging
import os
import random
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from openai import AsyncOpenAI
from sage_protocol.calendar.entities import Event, ParticipantProfile, TimeRange
from sage_protocol.calendar.utils.series_expansion import SeriesExpander

from .context import (
    BaselineCalendarContext,
    BlockingEventContext,
    GenerationContext,
    GoalEventContext,
    ParticipantContext,
    ScenarioContext,
)
from .entities import GenerationParams, GoalEvent, Scenario
from .generators import (
    BaselineCalendarGenerator,
    ConflictEventGenerator,
    GoalEventGenerator,
    ParticipantGenerator,
    ScenarioGenerator,
)

# Configure logger
logger = logging.getLogger(__name__)


class GenerationOrchestrator:
    """
    Orchestrates the LLM-based scenario generation pipeline.

    Phases:
    1. Scenario description generation
    2. Participant profile generation (N participants)
    3. Goal event generation
    4. Blocking event generation (create conflicts)
    5. Baseline calendar population (recurring + standalone events)
    6. Conflict verification
    7. Output (JSON)
    """

    def __init__(self, params: GenerationParams):
        """
        Initialize the orchestrator.

        Args:
            params: Generation parameters
        """
        self.params = params

        # Initialize OpenAI client
        api_key = params.llm_config.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key required (set OPENAI_API_KEY env var or pass in llm_config)"
            )

        self.client = AsyncOpenAI(api_key=api_key)

        # Initialize generators
        model = params.llm_config.model
        self.scenario_gen = ScenarioGenerator(self.client, model)
        self.participant_gen = ParticipantGenerator(self.client, model)
        self.goal_event_gen = GoalEventGenerator(self.client, model)
        self.conflict_gen = ConflictEventGenerator(self.client, model)
        self.baseline_gen = BaselineCalendarGenerator(self.client, model)

        # Initialize shared context
        self.context = GenerationContext()

        # Set random seed if provided
        if params.seed is not None:
            random.seed(params.seed)

    async def generate(self) -> dict[str, Any]:
        """
        Execute the complete generation pipeline.

        Returns:
            Dict containing:
            - scenario: The generated Scenario object
            - events: List of all generated Event objects (recurring and standalone)
            - metadata: Generation metadata
        """
        logger.info("Starting scenario generation pipeline")

        # Calculate seed range
        start_date = datetime.now(tz=ZoneInfo("UTC")).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_date = start_date + timedelta(days=self.params.seed_days)
        seed_range = TimeRange(start=start_date, end=end_date)
        self.context.seed_range = seed_range
        logger.info(f"Seed range: {seed_range.start.date()} to {seed_range.end.date()}")

        # Phase 1: Generate scenario description
        logger.info("Phase 1: Generating scenario description...")
        scenario_desc = await self._generate_scenario()
        logger.info(f"Scenario generated: {scenario_desc.theme}")

        # Phase 2: Generate participants
        logger.info(f"Phase 2: Generating {self.params.num_participants} participants...")
        participants = await self._generate_participants(scenario_desc.description)
        logger.info(f"Generated {len(participants)} participants")

        # Phase 3: Generate goal event
        logger.info("Phase 3: Generating goal event...")
        organizer, attendees = self._select_goal_participants(participants)
        goal_event = await self._generate_goal_event(
            scenario_desc.description,
            organizer,
            attendees,
        )
        logger.info(
            f"Goal event: {goal_event.title} ({goal_event.duration_minutes} min, {len(attendees)} attendees)"
        )

        # Create Scenario object
        scenario = Scenario(
            description=scenario_desc.description,
            participants=participants,
            goal_event=goal_event,
            organizer_id=organizer.id,
        )
        self.context.scenario = scenario

        # Store metadata separately in context
        self.context.metadata = {
            "theme": scenario_desc.theme,
            "suggested_goal_title": scenario_desc.suggested_goal_title,
            "generated_at": datetime.now().isoformat(),
            "generation_params": self.params.model_dump(),
        }

        # Phase 4 & 5: Generate events for each participant
        logger.info(f"Phase 4-5: Generating calendars for {len(participants)} participants...")
        all_events: list[Event] = []

        for i, participant in enumerate(participants, 1):
            logger.info(
                f"  [{i}/{len(participants)}] Generating calendar for {participant.name}..."
            )

            events_list = await self._generate_participant_calendar(
                participant,
                goal_event,
                seed_range,
            )

            all_events.extend(events_list)
            recurring_count = sum(1 for e in events_list if e.is_recurring)
            standalone_count = len(events_list) - recurring_count
            logger.info(
                f"  {participant.name}: {recurring_count} recurring, {standalone_count} standalone events"
            )

        # Phase 6: Verify no conflicts exist within each participant's calendar
        logger.info("Phase 6: Verifying calendars...")
        self._verify_no_conflicts(all_events, seed_range, participants)
        logger.info("Calendar verification complete")

        logger.info("=" * 60)
        recurring_total = sum(1 for e in all_events if e.is_recurring)
        standalone_total = len(all_events) - recurring_total
        logger.info(
            f"Generated {recurring_total} recurring events, {standalone_total} standalone events"
        )
        logger.info("Scenario generation complete!")
        logger.info("=" * 60)

        return {
            "scenario": scenario,
            "events": all_events,
            "seed_range": seed_range,
            "metadata": self.context.metadata,
        }

    async def _generate_scenario(self):
        """Phase 1: Generate scenario description."""
        context = ScenarioContext(
            num_participants=self.params.num_participants,
            scenario_hint=self.params.scenario_hint,
            seed=self.params.seed,
        )

        scenario_desc = await self.scenario_gen.generate(
            context,
            self.context.messages,
        )

        return scenario_desc

    async def _generate_participants(
        self,
        scenario_description: str,
    ) -> list[ParticipantProfile]:
        """Phase 2: Generate N participant profiles."""
        participants: list[ParticipantProfile] = []

        # Build timezone list from distribution
        timezone_list: list[str] = []
        for tz, count in self.params.timezone_distribution.items():
            timezone_list.extend([tz] * count)

        # Generate each participant
        # Only the first participant (index 0) has a goal - they will be the organizer
        for i in range(self.params.num_participants):
            has_goal = i == 0  # Only first participant has a goal

            context = ParticipantContext(
                scenario_description=scenario_description,
                num_participants=self.params.num_participants,
                existing_participants=participants,
                timezone_hint=timezone_list[i],
                participant_index=i,
                has_goal=has_goal,
                email_hint=None,
            )

            participant = await self.participant_gen.generate(
                context,
                self.context.messages,
            )

            participants.append(participant)
            goal_marker = " [ORGANIZER]" if has_goal else ""
            logger.info(
                f"  [{i + 1}/{self.params.num_participants}] {participant.name} ({participant.timezone}){goal_marker}"
            )

        return participants

    def _select_goal_participants(
        self,
        participants: list[ParticipantProfile],
    ) -> tuple[ParticipantProfile, list[ParticipantProfile]]:
        """Phase 3 helper: Select organizer and attendees for goal event."""
        # The organizer is always the first participant (the one with a goal)
        organizer = participants[0]

        # Select required attendees (including organizer)
        if self.params.goal_event_size >= len(participants):
            attendees = participants
        else:
            # Randomly select other attendees
            other_participants = participants[1:]
            selected_others = random.sample(
                other_participants,
                self.params.goal_event_size - 1,
            )
            attendees = [organizer] + selected_others

        return organizer, attendees

    async def _generate_goal_event(
        self,
        scenario_description: str,
        organizer: ParticipantProfile,
        attendees: list[ParticipantProfile],
    ) -> GoalEvent:
        """Phase 3: Generate the goal event."""
        assert self.context.seed_range is not None, (
            "Seed range must be set before generating goal event"
        )

        context = GoalEventContext(
            scenario_description=scenario_description,
            organizer=organizer,
            required_attendees=attendees,
            duration_minutes=60,  # Default to 1 hour, LLM can adjust
            seed_range=self.context.seed_range,
        )

        goal_event = await self.goal_event_gen.generate(
            context,
            self.context.messages,
        )

        return goal_event

    async def _generate_participant_calendar(
        self,
        participant: ParticipantProfile,
        goal_event: GoalEvent,
        seed_range: TimeRange,
    ) -> list[Event]:
        """Phases 4 & 5: Generate complete calendar for a participant."""
        events: list[Event] = []

        # Phase 4: Generate blocking events if participant is required for goal
        if participant.id in goal_event.required_attendees:
            blocking_events = await self._generate_blocking_events(
                participant,
                goal_event,
                seed_range,
            )
            events.extend(blocking_events)

        # Phase 5: Generate baseline calendar
        baseline_events = await self._generate_baseline_calendar(
            participant,
            events,
            seed_range,
        )
        events.extend(baseline_events)

        return events

    async def _generate_blocking_events(
        self,
        participant: ParticipantProfile,
        goal_event: GoalEvent,
        seed_range: TimeRange,
    ) -> list[Event]:
        """Phase 4: Generate blocking events that create conflicts."""
        assert self.context.scenario is not None, (
            "Scenario must be set before generating blocking events"
        )

        # Generate 1-3 blocking events per required participant
        num_blocking = random.randint(1, 3)

        context = BlockingEventContext(
            scenario_description=self.context.scenario.description,
            participant=participant,
            goal_event=goal_event,
            date_range=seed_range,
            num_blocking_events=num_blocking,
        )

        blocking_events: list[Event] = []
        for _ in range(num_blocking):
            event = await self.conflict_gen.generate(
                context,
                self.context.messages,
            )
            blocking_events.append(event)

        return blocking_events

    async def _generate_baseline_calendar(
        self,
        participant: ParticipantProfile,
        existing_events: list[Event],
        seed_range: TimeRange,
    ) -> list[Event]:
        """Phase 5: Generate baseline recurring and standalone events."""
        assert self.context.scenario is not None, (
            "Scenario must be set before generating baseline calendar"
        )

        # Generate 3-7 recurring events
        num_recurring = random.randint(3, 7)

        # Target density: 30-60% of work hours filled
        target_density = random.uniform(0.3, 0.6)

        context = BaselineCalendarContext(
            scenario_description=self.context.scenario.description,
            participant=participant,
            existing_events=existing_events,
            date_range=seed_range,
            target_series_count=num_recurring,
            target_event_density=target_density,
        )

        events: list[Event] = []

        # Generate recurring events
        for i in range(num_recurring):
            event = await self.baseline_gen.generate_recurring_event(
                context,
                self.context.messages,
                i,
            )
            events.append(event)

        # Generate standalone events to fill gaps
        # Simple heuristic: 5-10 standalone events
        num_standalone = random.randint(5, 10)
        for i in range(num_standalone):
            event = await self.baseline_gen.generate_standalone_event(
                context,
                self.context.messages,
                i,
            )
            events.append(event)

        return events

    def _verify_no_conflicts(
        self,
        all_events: list[Event],
        seed_range: TimeRange,
        participants: list[ParticipantProfile],
    ) -> None:
        """Phase 6: Verify no pre-existing conflicts in calendars."""
        # Group events by participant (organizer)
        for participant in participants:
            participant_events: list[Event] = []

            for event in all_events:
                if event.organizer_id != participant.id:
                    continue

                if event.is_recurring:
                    # Expand recurring events into instances
                    expanded_events = SeriesExpander.expand_event_to_instances(
                        event,
                        seed_range,
                        include_cancelled=False,
                    )
                    participant_events.extend(expanded_events)
                else:
                    participant_events.append(event)

            # Check for overlaps within this participant's events
            for i, event1 in enumerate(participant_events):
                for event2 in participant_events[i + 1 :]:
                    if event1.overlaps(event2):
                        # Log warning but don't fail - LLM might generate overlaps
                        logger.warning(
                            f"Conflict detected in {participant.name}'s calendar: "
                            f"{event1.title} overlaps with {event2.title}"
                        )
