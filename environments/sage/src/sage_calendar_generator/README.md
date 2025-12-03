# sage_calendar_generator

LLM-based generation of multi-agent scheduling scenarios with realistic calendars and goal events.

## Installation

```bash
uv sync
```

## Quick Start

```bash
export OPENAI_API_KEY=sk-your-api-key-here

python -m sage_calendar_generator \
    --num-participants 3 \
    --timezones "America/New_York:3" \
    --seed-days 1 \
    --goal-event-participants 3
```

## How It Works

The orchestrator runs a 6-phase pipeline:

1. **Scenario Description** - LLM generates a themed scenario (e.g., "Tech startup planning Q4 roadmap")
2. **Participant Generation** - Creates N participant profiles with roles, timezones, and optional goals
3. **Goal Event** - Defines the unscheduled event that agents must coordinate (the scheduling challenge)
4. **Blocking Events** - Generates conflicts for goal participants to make scheduling non-trivial
5. **Baseline Calendars** - Populates each participant with recurring and standalone events
6. **Verification** - Checks for unintended overlaps within each participant's calendar

## Usage

### CLI Options

| Option | Description |
|--------|-------------|
| `--num-participants` | Total participants to generate (2-10) |
| `--timezones` | Distribution like `"America/New_York:2,Europe/London:1"` |
| `--seed-days` | Days of calendar data to generate (1-90) |
| `--goal-event-participants` | Required attendees for the goal event |
| `--scenario-hint` | Optional theme hint (e.g., "quarterly planning") |
| `--model` | OpenAI model (default: gpt-4.1-mini) |
| `--output-dir` | Where to save generated scenarios |
| `--seed` | Random seed for reproducibility |

### Examples

Multi-timezone scenario with custom model:

```bash
python -m sage_calendar_generator \
    --num-participants 4 \
    --timezones "America/New_York:2,Europe/London:1,Asia/Tokyo:1" \
    --seed-days 2 \
    --goal-event-participants 3 \
    --model gpt-4 \
    --scenario-hint "quarterly planning meeting" \
    --seed 42
```

### Output

Generates a JSON file containing:

- `scenario` - Description, participants, goal event, organizer
- `events` - All calendar events (recurring have `recurrence_rule` set)
- `seed_range` - Date range covered
- `generation_params` - Parameters used for generation
