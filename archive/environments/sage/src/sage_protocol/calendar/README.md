# SAGE Calendar Protocol

Multi-agent calendar management protocol for the SAGE marketplace with support for standalone events and recurring series.

## Features

- **Event Management**: Create, read, update, and delete standalone events
- **Recurring Series**: Flexible recurring patterns (daily, weekly, monthly, yearly)
- **Multi-agent Coordination**: Shared calendar across agents
- **Timezone-aware**: All datetimes include timezone information
- **Query Service**: Efficient event retrieval and series expansion

## Actions

- `GetEvents` - Get events in a datetime range
- `GetEventDetails` - Get detailed event information
- `AddEvent` - Create standalone event
- `AddSeries` - Create recurring event series
- `UpdateEvent` - Update single event
- `UpdateSeries` - Update recurring series template
- `DeleteEvent` - Delete event or cancel series instance
- `DeleteSeries` - Delete entire series

## Usage

### Start the server

```bash
# Basic server
python -m sage_protocol.calendar.cli

# With database management
python -m sage_protocol.calendar.cli --resume
python -m sage_protocol.calendar.cli --overwrite

# With scenario
python -m sage_protocol.calendar.cli --scenario-json scenarios/test.json --overwrite
```

### Example: Create event

```bash
curl -X POST http://localhost:8002/actions/execute \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "name": "AddEvent",
    "parameters": {
      "title": "Team Meeting",
      "description": "Weekly sync",
      "start_datetime": "2024-01-15T14:00:00-08:00",
      "end_datetime": "2024-01-15T15:00:00-08:00",
      "participants": []
    }
  }'
```

### Example: Create recurring series

```bash
curl -X POST http://localhost:8002/actions/execute \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "name": "AddSeries",
    "parameters": {
      "title": "Weekly Standup",
      "description": "Team standup meeting",
      "first_start_datetime": "2024-01-15T09:00:00-08:00",
      "first_end_datetime": "2024-01-15T09:30:00-08:00",
      "recurrence": {
        "frequency": "WEEKLY",
        "interval": 1,
        "by_day": ["MONDAY"],
        "end_condition": {"type": "NEVER"}
      },
      "participants": []
    }
  }'
```

## Key Concepts

- **Events**: Standalone calendar entries with specific start/end datetimes
- **Series**: Recurring event templates that generate instances based on recurrence rules
- **TimeRange**: Internal model for datetime ranges (always timezone-aware)
- **Recurrence Rules**: iCalendar-style patterns (RRULE) for series expansion
- **Instance Modifications**: Override specific series instances (reschedule, cancel)

## Architecture

- `actions.py` - Action definitions (API contract)
- `protocol.py` - Action execution and state management
- `entities.py` - Core domain models (Event, Series, TimeRange, RecurrenceRule)
- `query_service.py` - Event querying and series expansion
- `utils/` - Date/time utilities and series expansion logic
