# Soft preferences

Calendar tasks come in two forms. A task can state its principal's scheduling preferences as a numeric table of hourly scores, or as a preference document: prose the assistant reads, paired with a Python verifier that grades what it scheduled.

`data/calendar-scheduling/small_soft/` and `medium_soft/` are the second kind — the same tasks as `small.yaml` and `medium.yaml`, with each numeric table rewritten as a document.

| Ported dataset | Tasks | Ported from |
| --- | ---: | --- |
| `small_soft/tasks.yaml` | 21 | `small.yaml` |
| `medium_soft/tasks.yaml` | 70 | `medium.yaml` |

The numeric datasets are nested — every `small.yaml` task appears in `medium.yaml` unchanged — and so are their ports. A task keeps its id, its document and its verifier in every dataset it appears in, so `medium_soft` reuses all 21 of `small_soft`'s documents rather than restating them.

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/medium_soft/tasks.yaml \
    --model gpt-4.1
```

Which form a task uses is decided per task by whether its assistant declares a `preference_file`, so both kinds can be mixed in one dataset. Everything else — tools, prompts, and the other metrics — is shared.

## What the assistant sees

The document is injected into the assistant's first user turn, inside `<user_preference>` tags, and the system prompt explains what the tags mean:

```
<user_preference>
# Scheduling notes — Amara Okafor

Junior Grid Engineer at Solara Dynamics. Notes I keep while booking for her —
what she said, and when.

## Fixed

Bookable 08:00-19:00. Nothing outside that.
> "Outside those hours, decline it. No exceptions."
— 2026-01-22, going through the week

## Ranked, best first

**08:00, 09:00, 15:00, 18:00** — what she actually wants
> "08:00, 09:00, 15:00 or 18:00. Whichever's open — they're all good to me."
— 2026-01-29, reading out the open slots

**11:00, 14:00, 17:00** — fine
> "11:00, 14:00 or 17:00 is fine if the good ones are gone."
— 2026-02-03, after a booking I made got moved
...
</user_preference>
```

A document reads as notes an assistant kept while booking for someone, because that is the position the model is being put in. Nothing marks a sentence as absolute or negotiable; the wording carries it. "Bookable 08:00-19:00. Nothing outside that." is a rule, a rung of the ranking is a leaning, and reading the difference is part of the task.

Because the document defines when its principal is bookable, `ListMeetings` reports free time over the whole day for these tasks rather than clipping to business hours.

## How it is scored

Each document has a verifier that restates it as predicates:

```python
PREFERENCE_FILE = "preferences/task_000.md"

HARD_CONSTRAINTS: list[Predicate] = [
    # "Bookable 08:00-19:00. Nothing outside that."
    within("08:00", "19:00"),
]

SOFT_PREFERENCES: list[SoftPreference] = [
    SoftPreference("08:00-09:00", starts_within("08:00", "10:00"), weight=1),
    SoftPreference("15:00", starts_within("15:00", "16:00"), weight=1),
    SoftPreference("11:00", starts_within("11:00", "12:00"), weight=0.5),
    ...
]
```

Two numbers come out:

| Metric | Meaning |
|--------|---------|
| `hard_constraints_satisfied` | Whether the scheduled meeting breaks no absolute rule, reported as `avg_hard_constraints_satisfied` |
| `outcome_optimality_score` | Total weight of the soft preferences the chosen slot satisfies, over the best any bookable slot could have scored |

Optimality writes to the same field the numeric path uses, because it measures the same thing. Being relative to what was reachable, it does not punish an assistant for taking the best of a bad day. Scheduling nothing when a slot existed scores zero on both; declining when no slot passes the hard constraints scores full marks on both.

## The port is faithful to the numeric datasets

Every hour in a task's numeric table becomes a soft preference weighted by that hour's score, so the two gradings rank slots identically and **scores are comparable to `small.yaml`'s and `medium.yaml`'s**. A test asserts this hour by hour across every ported task.

Documents are per task, not per principal. The same principal is scored against a different table in every task they appear in — Amara Okafor has seven tasks in `small.yaml` and seven distinct profiles — so one document per principal cannot represent them. Written that way, a document names a slot the numeric table also ranked best in only 2 of those 21 tasks.

The one deliberate generalization is that `starts_within` accepts any minute of an hour, where the numeric table scores whole hours only. An assistant that books 09:30 is credited with 09:00 rather than with nothing.

## Adding a task

1. Write `preferences/task_NNN.md`. Notes an assistant kept, not a spec. Say which rules are absolute, and rank the rest against each other.
2. Add `verifiers/task_NNN.py` restating it with `within`, `outside`, `ends_by`, `starts_at_or_after` and `starts_within`. Decorate the verifier with `@register_verifier`; registration happens on import, and the package discovers its own modules, so there is no list to update.
3. Point the task at the document with `assistant.preference_file`, relative to the task YAML.

Nothing checks that prose and predicates mean the same thing, so that agreement is what a reviewer has to supply. What is checked is that every document has a verifier and vice versa, that each document ranks every bookable hour in the order its verifier scores them, that every task still has a slot to book, and that a task appearing in two ported datasets ships the same document in both.
