"""CLI for generating calendar scenarios using LLM-based generation.

This CLI provides a command-line interface to the calendar scenario generation
system, which creates realistic meeting scenarios with participants, goals, and
baseline calendars.

Usage:
    # Basic generation with 3 participants
    python -m calendar_generator \
        --num-participants 3 \
        --timezones "America/New_York:2,Europe/London:1" \
        --seed-days 1 \
        --goal-event-participants 3

    # With custom model and scenario hint
    python -m calendar_generator \
        --num-participants 4 \
        --timezones "America/New_York:2,Asia/Tokyo:1,Europe/Paris:1" \
        --seed-days 2 \
        --goal-event-participants 3 \
        --model gpt-4 \
        --scenario-hint "quarterly planning meeting" \
        --seed 42

    # Specify output directory
    python -m calendar_generator \
        --num-participants 3 \
        --timezones "America/New_York:3" \
        --seed-days 1 \
        --goal-event-participants 3 \
        --output-dir my_scenarios
"""

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from .entities import GenerationParams, LLMConfig
from .orchestrator import GenerationOrchestrator


def parse_timezone_distribution(tz_string: str) -> dict[str, int]:
    """Parse timezone distribution from CLI string format.

    Args:
        tz_string: Format "America/New_York:2,Europe/London:1"

    Returns:
        Dict mapping timezone names to participant counts

    Example:
        >>> parse_timezone_distribution("America/New_York:2,Europe/London:1")
        {"America/New_York": 2, "Europe/London": 1}
    """
    result = {}
    for part in tz_string.split(","):
        tz, count = part.strip().rsplit(":", 1)
        result[tz] = int(count)
    return result


async def main():
    """Run the calendar scenario generation CLI."""
    parser = argparse.ArgumentParser(
        description="Generate calendar scenarios using LLM-based generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic 3-participant scenario
  python -m calendar_generator \\
      --num-participants 3 \\
      --timezones "America/New_York:3" \\
      --seed-days 1 \\
      --goal-event-participants 3

  # Multi-timezone with custom model
  python -m calendar_generator \\
      --num-participants 4 \\
      --timezones "America/New_York:2,Europe/London:1,Asia/Tokyo:1" \\
      --seed-days 2 \\
      --goal-event-participants 3 \\
      --model gpt-4 \\
      --scenario-hint "quarterly planning meeting"
        """,
    )

    # Required parameters
    parser.add_argument(
        "--num-participants",
        type=int,
        required=True,
        help="Number of participants (2-10)",
    )
    parser.add_argument(
        "--timezones",
        type=str,
        required=True,
        help='Timezone distribution (format: "America/New_York:2,Europe/London:1")',
    )
    parser.add_argument(
        "--seed-days",
        type=int,
        required=True,
        help="Number of days to pre-generate events for (1-90)",
    )
    parser.add_argument(
        "--goal-event-participants",
        type=int,
        required=True,
        help="Number of required attendees for goal event (>= 2)",
    )

    # Optional parameters
    parser.add_argument(
        "--scenario-hint",
        type=str,
        default=None,
        help="Hint or theme for scenario generation (e.g., 'quarterly planning')",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility",
    )

    # LLM configuration
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1-mini",
        help="OpenAI model to use (default: gpt-4.1-mini)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="LLM temperature (0.0-2.0, default: model default)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Maximum tokens per LLM request",
    )
    parser.add_argument(
        "--openai-api-key",
        type=str,
        default=None,
        help="OpenAI API key (or set OPENAI_API_KEY env var)",
    )

    # Output configuration
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("scenarios"),
        help="Output directory for generated scenarios (default: scenarios/)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=None,
        help="Output filename (default: scenario_TIMESTAMP.json)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output (only show final summary)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed generation logs",
    )

    args = parser.parse_args()

    # Configure logging
    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
    )

    # Check for API key
    api_key = args.openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found")
        print(
            "Please provide it via --openai-api-key or set the OPENAI_API_KEY environment variable"
        )
        print("\nExample:")
        print("  export OPENAI_API_KEY=sk-your-api-key-here")
        raise SystemExit(1)

    # Parse timezone distribution
    try:
        timezone_distribution = parse_timezone_distribution(args.timezones)
    except Exception as e:
        print(f"Error parsing --timezones: {e}")
        print('Expected format: "America/New_York:2,Europe/London:1"')
        raise SystemExit(1)

    # Validate timezone distribution matches num_participants
    total_tz = sum(timezone_distribution.values())
    if total_tz != args.num_participants:
        print(
            f"Error: Timezone distribution ({total_tz}) doesn't match num_participants ({args.num_participants})"
        )
        print(f"Timezone distribution: {timezone_distribution}")
        raise SystemExit(1)

    # Build generation parameters
    params = GenerationParams(
        num_participants=args.num_participants,
        timezone_distribution=timezone_distribution,
        seed_days=args.seed_days,
        goal_event_size=args.goal_event_participants,
        scenario_hint=args.scenario_hint,
        llm_config=LLMConfig(
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            api_key=api_key,
        ),
        seed=args.seed,
    )

    # Display configuration
    if not args.quiet:
        print("=" * 70)
        print("Calendar Scenario Generation")
        print("=" * 70)
        print("\nParameters:")
        print(f"  Participants: {params.num_participants}")
        print(f"  Timezones: {params.timezone_distribution}")
        print(f"  Seed days: {params.seed_days}")
        print(f"  Goal event attendees: {params.goal_event_size}")
        if params.scenario_hint:
            print(f"  Scenario hint: {params.scenario_hint}")
        if params.seed is not None:
            print(f"  Random seed: {params.seed}")
        print("\nLLM Configuration:")
        print(f"  Model: {params.llm_config.model}")
        if params.llm_config.temperature is not None:
            print(f"  Temperature: {params.llm_config.temperature}")
        print("\nGenerating scenario... (this may take 1-2 minutes)")
        print()

    # Create orchestrator and generate
    orchestrator = GenerationOrchestrator(params)

    try:
        result = await orchestrator.generate()
    except Exception as e:
        print(f"\nError during generation: {e}")
        if args.verbose:
            raise
        else:
            print("\nRun with --verbose for detailed error information")
            raise SystemExit(1)

    scenario = result["scenario"]
    all_events = result["events"]
    seed_range = result["seed_range"]

    # Display results
    print("\n" + "=" * 70)
    print("Generation Complete!")
    print("=" * 70)

    print(f"\nScenario: {scenario.description}")
    print("\nParticipants:")
    for p in scenario.participants:
        is_organizer = p.id == scenario.organizer_id
        marker = " [ORGANIZER]" if is_organizer else ""
        print(f"  - {p.name} ({p.timezone}){marker}")
        print(f"    ID: {p.id}")
        print(f"    Role: {p.description[:80]}...")
        if p.goal:
            print(f"    Goal: {p.goal[:80]}...")

    print(f"\nGoal Event: {scenario.goal_event.title}")
    print(f"  Description: {scenario.goal_event.description[:80]}...")
    print(f"  Duration: {scenario.goal_event.duration_minutes} minutes")
    print(f"  Required attendees: {len(scenario.goal_event.required_attendees)}")
    organizer = scenario.get_organizer()
    organizer_name = organizer.name if organizer else "Unknown"
    print(f"  Organizer: {organizer_name} ({scenario.organizer_id})")

    # Display calendar summaries by participant
    print("\nEvents Generated:")
    for participant in scenario.participants:
        recurring_count = len(
            [e for e in all_events if e.organizer_id == participant.id and e.is_recurring]
        )
        standalone_count = len(
            [e for e in all_events if e.organizer_id == participant.id and not e.is_recurring]
        )
        print(
            f"  - {participant.name}: {recurring_count} recurring, {standalone_count} standalone events"
        )

    recurring_total = sum(1 for e in all_events if e.is_recurring)
    standalone_total = len(all_events) - recurring_total
    print(f"\nTotal: {recurring_total} recurring events, {standalone_total} standalone events")
    print(f"Seed range: {seed_range.start.date()} to {seed_range.end.date()}")

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Determine output filename
    if args.output_name:
        output_file = args.output_dir / args.output_name
        if not output_file.suffix:
            output_file = output_file.with_suffix(".json")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = args.output_dir / f"scenario_{timestamp}.json"

    # Convert to JSON-serializable format (exclude API key for security)
    output_data = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "generation_params": params.model_dump(exclude={"llm_config": {"api_key"}}),
        "scenario": scenario.model_dump(),
        "events": [e.model_dump() for e in all_events],
        "seed_range": seed_range.model_dump(),
    }

    # Save to JSON
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2, default=str)

    print(f"\nScenario saved to: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
