# Soft preferences

Calendar tasks come in two forms. A task can state its principal's scheduling preferences as a numeric table of hourly scores, or as a preference document: prose the assistant reads, paired with a Python verifier that grades what it scheduled.

`data/calendar-scheduling/small_soft/` is the second kind — the same 21 tasks as `small.yaml`, with each numeric table replaced by its principal's document.

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small_soft/tasks.yaml \
    --model gpt-4.1
```

Which form a task uses is decided per task by whether its assistant declares a `preference_file`, so both kinds can be mixed in one dataset. Everything else — tools, prompts, and the other metrics — is shared.

## What the assistant sees

The document is injected into the assistant's first user turn, inside `<user_preference>` tags, and the system prompt explains what the tags mean:

```
<user_preference>
User is bookable between 08:00 and 19:00. Anything outside those hours is off
limits, evenings included.

User never gives up 12:00 to 13:00. It is the one real break in a day that is
otherwise wall-to-wall, and she takes it away from her desk.

What matters most to User is that meetings land later in the afternoon, from
15:00 onward, once the standup and review cycle is behind her.
...
</user_preference>
```

Nothing marks a sentence as absolute or negotiable; the wording carries it. "Never gives up 12:00 to 13:00" is a rule, "would rather not be booked between 14:00 and 15:00" is a leaning, and reading the difference is part of the task.

Because the document defines when its principal is bookable, `ListMeetings` reports free time over the whole day for these tasks rather than clipping to business hours.

## How it is scored

Each document has a verifier that restates it as predicates:

```python
HARD_CONSTRAINTS: list[Predicate] = [
    # "User is bookable between 08:00 and 19:00. Anything outside those hours
    #  is off limits, evenings included."
    within("08:00", "19:00"),
    # "User never gives up 12:00 to 13:00."
    outside("12:00", "13:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    # "What matters most to User is that meetings land later in the afternoon,
    #  from 15:00 onward."
    SoftPreference("later afternoon", starts_at_or_after("15:00"), weight=4.0),
    ...
]
```

Two numbers come out:

| Metric | Meaning |
|--------|---------|
| `hard_constraints_satisfied` | Whether the scheduled meeting breaks no absolute rule, reported as `avg_hard_constraints_satisfied` |
| `outcome_optimality` | Total weight of the soft preferences the chosen slot satisfies, over the best any slot passing the hard constraints could have scored |

Optimality is relative to what was reachable, so a task whose calendars leave only mediocre slots does not punish an assistant for taking the best one. Scheduling nothing when a slot existed scores zero on both; declining when no slot passes the hard constraints scores full marks on both.

Weights encode the ranking the prose states and nothing more. Each is larger than the sum of every weight below it, so a preference the document calls more important can never be outvoted by the ones it outranks.

Scores from this dataset are **not** comparable to `small.yaml` scores. The two describe different preferences over the same calendars.

## Adding a persona

1. Write `preferences/<name>.md`. Third person, no scoring language. Say which rules are absolute, and rank the rest against each other.
2. Add `verifiers/<name>.py` restating it with `within`, `outside`, `ends_by` and `starts_at_or_after`, quoting each sentence above the predicate that encodes it. Decorate the verifier with `@register_verifier`, and import the module from `verifiers/__init__.py` — registration only happens on import.
3. Point tasks at the document with `assistant.preference_file`, relative to the task YAML.
4. Add the task's feasible and best slots to `EXPECTED_SLOTS` in `test_calendar_soft_dataset.py`.

Nothing checks that a document and its verifier say the same thing, so keeping the quoted sentences accurate is what holds them together. The pinned slots turn any drift into a test failure.
